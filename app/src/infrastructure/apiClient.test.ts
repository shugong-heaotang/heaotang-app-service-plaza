import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { apiRequest, apiRequestWithMeta, tokenStorage } from "./apiClient";

function jsonResponse(body: unknown, status = 200, headers: Record<string, string> = {}): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", ...headers },
  });
}

function abortablePendingFetch(): ReturnType<typeof vi.fn> {
  return vi.fn((_input: RequestInfo | URL, init?: RequestInit) =>
    new Promise<Response>((_resolve, reject) => {
      const signal = init?.signal;
      if (signal?.aborted) {
        reject(signal.reason);
        return;
      }
      signal?.addEventListener("abort", () => reject(signal.reason), { once: true });
    }),
  );
}

describe("apiRequest", () => {
  beforeEach(() => {
    sessionStorage.clear();
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("只在需要认证时附加 Bearer 令牌，并发送请求关联 ID", async () => {
    tokenStorage.set("test-token-value");
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      jsonResponse({ success: true, data: { ok: true } }),
    );

    await apiRequest("/api/v1/example", {}, { auth: true, requestId: "req-fixed-001" });

    const headers = fetchMock.mock.calls[0][1]?.headers as Headers;
    expect(headers.get("Authorization")).toBe("Bearer test-token-value");
    expect(headers.get("X-Request-ID")).toBe("req-fixed-001");
  });

  it("自动生成关联 ID，并在受控重试中保持同一个 ID", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(jsonResponse({ success: false }, 503))
      .mockResolvedValueOnce(jsonResponse({ success: true, data: { ok: true } }));

    await expect(apiRequest<{ ok: boolean }>("/api/v1/example", {}, {
      retry: { maxAttempts: 2, baseDelayMs: 0 },
    })).resolves.toEqual({ ok: true });

    const firstId = (fetchMock.mock.calls[0][1]?.headers as Headers).get("X-Request-ID");
    const secondId = (fetchMock.mock.calls[1][1]?.headers as Headers).get("X-Request-ID");
    expect(firstId).toBeTruthy();
    expect(secondId).toBe(firstId);
  });

  it("可选元数据接口暴露最终状态、服务端请求 ID 和幂等重放标记", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      jsonResponse(
        { success: true, data: { id: 7 } },
        200,
        { "X-Request-ID": "server-replay-001", "Idempotency-Replayed": "true" },
      ),
    );

    await expect(apiRequestWithMeta<{ id: number }>("/api/v1/records")).resolves.toEqual({
      data: { id: 7 },
      meta: {
        status: 200,
        requestId: "server-replay-001",
        idempotencyReplayed: true,
      },
    });
  });

  it("沿用调用方 Header 中已有的关联 ID", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      jsonResponse({ success: true, data: { ok: true } }),
    );

    await apiRequest("/api/v1/example", { headers: { "X-Request-ID": "upstream-req-001" } });

    const headers = fetchMock.mock.calls[0][1]?.headers as Headers;
    expect(headers.get("X-Request-ID")).toBe("upstream-req-001");
  });

  it("认证失败时清除会话令牌并保留服务端机器错误码和关联 ID", async () => {
    tokenStorage.set("expired-token");
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      jsonResponse(
        { success: false, code: "AUTH_TOKEN_INVALID", error: "unauthorized" },
        401,
        { "X-Request-ID": "server-request-001" },
      ),
    );

    const request = apiRequest("/api/v1/example", {}, { auth: true });
    await expect(request).rejects.toMatchObject({
      name: "ApiError",
      status: 401,
      code: "AUTH_TOKEN_INVALID",
      requestId: "server-request-001",
    });
    expect(tokenStorage.get()).toBeNull();
  });

  it("达到可配置超时后中止 fetch 并返回稳定机器错误码", async () => {
    vi.useFakeTimers();
    vi.stubGlobal("fetch", abortablePendingFetch());

    const request = apiRequest("/api/v1/slow", {}, { timeoutMs: 25 });
    const rejection = expect(request).rejects.toMatchObject({
      name: "ApiError",
      status: 0,
      code: "REQUEST_TIMEOUT",
    });
    await vi.advanceTimersByTimeAsync(25);

    await rejection;
  });

  it("调用方 AbortSignal 可取消请求且不会误报为超时", async () => {
    vi.stubGlobal("fetch", abortablePendingFetch());
    const controller = new AbortController();

    const request = apiRequest("/api/v1/example", {}, { signal: controller.signal, timeoutMs: 1_000 });
    controller.abort();

    await expect(request).rejects.toMatchObject({
      name: "ApiError",
      status: 0,
      code: "REQUEST_ABORTED",
    });
  });

  it("取消请求后即使配置了重试也不会再次发送", async () => {
    const fetchMock = abortablePendingFetch();
    vi.stubGlobal("fetch", fetchMock);
    const controller = new AbortController();

    const request = apiRequest("/api/v1/example", {}, {
      signal: controller.signal,
      retry: { maxAttempts: 3, baseDelayMs: 0 },
    });
    controller.abort();

    await expect(request).rejects.toMatchObject({ code: "REQUEST_ABORTED" });
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("只在显式策略允许时重试瞬时读请求", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch")
      .mockRejectedValueOnce(new TypeError("connection reset"))
      .mockResolvedValueOnce(jsonResponse({ success: true, data: { ok: true } }));

    await expect(apiRequest<{ ok: boolean }>("/api/v1/example", {}, {
      retry: { maxAttempts: 2, baseDelayMs: 0 },
    })).resolves.toEqual({ ok: true });
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("未声明重试策略的写请求遇到瞬时错误也只发送一次", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      jsonResponse({ success: false, code: "UPSTREAM_UNAVAILABLE", error: "unavailable" }, 503),
    );

    await expect(apiRequest("/api/v1/records", {
      method: "POST",
      body: JSON.stringify({ value: 1 }),
    })).rejects.toMatchObject({ code: "UPSTREAM_UNAVAILABLE", status: 503 });
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("拒绝没有幂等键的写请求重试策略，并且不发送网络请求", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch");

    await expect(apiRequest("/api/v1/records", { method: "POST" }, {
      retry: { maxAttempts: 2, baseDelayMs: 0 },
    })).rejects.toMatchObject({
      name: "ApiError",
      code: "INVALID_REQUEST_OPTIONS",
    });
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("写请求只有携带幂等键并明确声明后才允许受控重试", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(jsonResponse({ success: false }, 503))
      .mockResolvedValueOnce(jsonResponse({ success: true, data: { id: 7 } }));

    await expect(apiRequest<{ id: number }>("/api/v1/records", {
      method: "POST",
      headers: { "Idempotency-Key": "idem-001" },
      body: JSON.stringify({ value: 1 }),
    }, {
      retry: { mode: "idempotency-key", maxAttempts: 2, baseDelayMs: 0 },
    })).resolves.toEqual({ id: 7 });
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("非瞬时业务错误不会被重试", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      jsonResponse({ success: false, code: "VALIDATION_ERROR", error: "invalid" }, 400),
    );

    await expect(apiRequest("/api/v1/example", {}, {
      retry: { maxAttempts: 3, baseDelayMs: 0 },
    })).rejects.toMatchObject({ code: "VALIDATION_ERROR", status: 400 });
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("网络失败统一为 ApiError，不泄漏 fetch 的原始异常", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new TypeError("connection reset"));

    await expect(apiRequest("/api/v1/example")).rejects.toEqual(
      expect.objectContaining({
        name: "ApiError",
        status: 0,
        code: "NETWORK_ERROR",
      }),
    );
  });

  it("版本化接口拒绝缺少 success/data 的漂移响应", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(jsonResponse({ id: 7 }));

    await expect(apiRequest("/api/v1/example")).rejects.toMatchObject({
      code: "INVALID_API_ENVELOPE",
      status: 200,
    });
  });

  it("只有显式兼容模式才接受已登记的旧接口形状", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(jsonResponse({ id: 7 }));

    await expect(
      apiRequest<{ id: number }>("/api/legacy", {}, { envelope: "compatible" }),
    ).resolves.toEqual({ id: 7 });
  });
});
