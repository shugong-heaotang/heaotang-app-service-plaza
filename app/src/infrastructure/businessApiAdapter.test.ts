import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { ApiError, tokenStorage } from "./apiClient";
import {
  createBusinessApiAdapter,
  defineBusinessRead,
  defineBusinessWrite,
} from "./businessApiAdapter";

const response = (data: unknown, status = 200) => new Response(JSON.stringify(
  status < 400
    ? { success: true, data }
    : { success: false, code: "BUSINESS_REJECTED", error: "业务拒绝" },
), { status, headers: { "Content-Type": "application/json" } });

describe("businessApiAdapter", () => {
  beforeEach(() => {
    sessionStorage.clear();
    tokenStorage.set("module-token");
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("读操作自动使用会话、严格 v1 信封、关联 ID 和安全重试", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(response({}, 503))
      .mockResolvedValueOnce(response({ items: [1] }));
    const adapter = createBusinessApiAdapter("example-service");
    const listRecords = defineBusinessRead<void, { items: number[] }>({
      operationId: "list-records",
      path: () => "/api/v1/example/records",
    });

    await expect(adapter.execute(listRecords, undefined, {
      requestId: "req-adapter-read",
    })).resolves.toEqual({ items: [1] });

    expect(fetchMock).toHaveBeenCalledTimes(2);
    const firstHeaders = fetchMock.mock.calls[0][1]?.headers as Headers;
    const secondHeaders = fetchMock.mock.calls[1][1]?.headers as Headers;
    expect(firstHeaders.get("Authorization")).toBe("Bearer module-token");
    expect(firstHeaders.get("X-Request-ID")).toBe("req-adapter-read");
    expect(secondHeaders.get("X-Request-ID")).toBe("req-adapter-read");
  });

  it("认证是适配器策略而不是板块手工 Header", async () => {
    tokenStorage.clear();
    const fetchMock = vi.spyOn(globalThis, "fetch");
    const adapter = createBusinessApiAdapter("example-service");
    const privateRead = defineBusinessRead<void, unknown>({
      operationId: "private-read",
      path: () => "/api/v1/example/private",
    });

    await expect(adapter.execute(privateRead, undefined)).rejects.toMatchObject({
      code: "AUTH_REQUIRED",
      status: 401,
    });
    expect(fetchMock).not.toHaveBeenCalled();

    fetchMock.mockResolvedValue(response({ ok: true }));
    const publicRead = defineBusinessRead<void, { ok: boolean }>({
      operationId: "public-read",
      path: () => "/api/v1/example/public",
      authMode: "anonymous",
    });
    await expect(adapter.execute(publicRead, undefined)).resolves.toEqual({ ok: true });
    const headers = fetchMock.mock.calls[0][1]?.headers as Headers;
    expect(headers.get("Authorization")).toBeNull();
  });

  it("写操作自动生成幂等键，并在受控重试时复用同一个键", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(response({}, 503))
      .mockResolvedValueOnce(response({ id: 9 }));
    const adapter = createBusinessApiAdapter("example-service");
    const createRecord = defineBusinessWrite<{ title: string }, { id: number }>({
      operationId: "create-record",
      method: "POST",
      path: () => "/api/v1/example/records",
      body: (input) => input,
    });

    await expect(adapter.execute(createRecord, { title: "记录" })).resolves.toEqual({ id: 9 });

    const firstKey = (fetchMock.mock.calls[0][1]?.headers as Headers).get("Idempotency-Key");
    const secondKey = (fetchMock.mock.calls[1][1]?.headers as Headers).get("Idempotency-Key");
    expect(firstKey).toMatch(/^example-service-create-record-/);
    expect(secondKey).toBe(firstKey);
  });

  it("允许显式复用同一逻辑写入的幂等键", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(response({ id: 9 }));
    const adapter = createBusinessApiAdapter("example-service");
    const createRecord = defineBusinessWrite<{ title: string }, { id: number }>({
      operationId: "create-record",
      method: "POST",
      path: () => "/api/v1/example/records",
      body: (input) => input,
    });

    await adapter.execute(createRecord, { title: "记录" }, { idempotencyKey: "logical-write-001" });

    const headers = fetchMock.mock.calls[0][1]?.headers as Headers;
    expect(headers.get("Idempotency-Key")).toBe("logical-write-001");
  });

  it("原样保留统一 SDK 的机器错误码与请求 ID", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(JSON.stringify({
      success: false,
      code: "VALIDATION_ERROR",
      error: "字段错误",
    }), {
      status: 400,
      headers: { "Content-Type": "application/json", "X-Request-ID": "server-req-8" },
    }));
    const adapter = createBusinessApiAdapter("example-service");
    const read = defineBusinessRead<void, unknown>({
      operationId: "read-record",
      path: () => "/api/v1/example/record",
    });

    const error = await adapter.execute(read, undefined).catch((reason: unknown) => reason);
    expect(error).toBeInstanceOf(ApiError);
    expect(error).toMatchObject({ code: "VALIDATION_ERROR", requestId: "server-req-8" });
  });

  it("在发网前拒绝非 v1 地址、非法标识和非法幂等键", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch");
    expect(() => createBusinessApiAdapter("Example Service")).toThrow("kebab-case");

    const adapter = createBusinessApiAdapter("example-service");
    const legacyRead = defineBusinessRead<void, unknown>({
      operationId: "legacy-read",
      path: () => "/api/legacy/records",
    });
    await expect(adapter.execute(legacyRead, undefined)).rejects.toMatchObject({
      code: "INVALID_ADAPTER_DEFINITION",
    });
    const traversalRead = defineBusinessRead<void, unknown>({
      operationId: "traversal-read",
      path: () => "/api/v1/example/../admin",
    });
    await expect(adapter.execute(traversalRead, undefined)).rejects.toMatchObject({
      code: "INVALID_ADAPTER_DEFINITION",
    });

    const write = defineBusinessWrite<void, unknown>({
      operationId: "create-record",
      method: "POST",
      path: () => "/api/v1/example/records",
      body: () => ({}),
    });
    await expect(adapter.execute(write, undefined, { idempotencyKey: "bad key" })).rejects.toMatchObject({
      code: "INVALID_IDEMPOTENCY_KEY",
    });
    await expect(adapter.execute(write, undefined, { idempotencyKey: " logical-write-001 " })).rejects.toMatchObject({
      code: "INVALID_IDEMPOTENCY_KEY",
    });
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
