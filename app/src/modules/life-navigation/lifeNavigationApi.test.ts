import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { ApiError, tokenStorage } from "../../infrastructure/apiClient";
import {
  defaultLifeNavigationHistoryLimit,
  fetchLifeNavigationApplicationHistory,
  loadLifeNavigationApplicationHistory,
  resolveLifeNavigationHistoryLimit,
  submitLifeNavigationApplication,
  type LifeNavigationRecordDto,
} from "./lifeNavigationApi";

const record = (
  overrides: Partial<LifeNavigationRecordDto> = {},
): LifeNavigationRecordDto => ({
  id: 11,
  user_id: 99,
  dimension_id: "yun",
  record_type: "application",
  title: "服务广场导航申请",
  note: "希望梳理事业方向",
  created_at: "2026-07-11T00:00:00Z",
  ...overrides,
});

const successResponse = (
  data: unknown,
  status = 200,
  headers: Record<string, string> = {},
) => new Response(JSON.stringify({ success: true, data }), {
  status,
  headers: { "Content-Type": "application/json", ...headers },
});

describe("lifeNavigationApi", () => {
  beforeEach(() => {
    sessionStorage.clear();
    tokenStorage.set("life-navigation-token");
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it.each([
    [0, defaultLifeNavigationHistoryLimit],
    [1, 1],
    [30, 30],
    [31, defaultLifeNavigationHistoryLimit],
  ])("将 limit=%s 安全解析为 %s", (input, expected) => {
    expect(resolveLifeNavigationHistoryLimit(input)).toBe(expected);
  });

  it("默认请求本人最近 30 条记录并只保留 application", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(successResponse({
      items: [record(), record({ id: 12, record_type: "action" })],
    }));

    await expect(fetchLifeNavigationApplicationHistory()).resolves.toEqual([
      {
        id: "11",
        dimensionId: "yun",
        title: "服务广场导航申请",
        note: "希望梳理事业方向",
        createdAt: "2026-07-11T00:00:00Z",
        displayStatus: "submitted",
      },
    ]);

    expect(fetchMock.mock.calls[0][0]).toBe("/api/v1/life-nav/records?limit=30");
  });

  it.each([
    [0, 30],
    [1, 1],
    [30, 30],
    [31, 30],
  ])("GET limit=%s 时只发送允许的 limit=%s", async (input, expected) => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      successResponse({ items: [] }),
    );

    await fetchLifeNavigationApplicationHistory(input);

    expect(fetchMock.mock.calls[0][0]).toBe(`/api/v1/life-nav/records?limit=${expected}`);
  });

  it("将无 application 的响应映射为空状态", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(successResponse({
      items: [record({ record_type: "action" })],
    }));

    await expect(loadLifeNavigationApplicationHistory()).resolves.toEqual({ status: "empty" });
  });

  it("将 application 响应映射为 ready/submitted 状态", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(successResponse({ items: [record()] }));

    await expect(loadLifeNavigationApplicationHistory(1)).resolves.toMatchObject({
      status: "ready",
      items: [{ id: "11", displayStatus: "submitted" }],
    });
  });

  it("在 error 状态中保留共享 ApiError 的机器码和请求 ID", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(JSON.stringify({
      success: false,
      code: "LIFE_RECORD_DAILY_LIMIT",
      error: "daily record limit reached",
    }), {
      status: 429,
      headers: {
        "Content-Type": "application/json",
        "X-Request-ID": "life-history-error-1",
      },
    }));

    const state = await loadLifeNavigationApplicationHistory();

    expect(state.status).toBe("error");
    if (state.status === "error") {
      expect(state.error).toBeInstanceOf(ApiError);
      expect(state.error).toMatchObject({
        status: 429,
        code: "LIFE_RECORD_DAILY_LIMIT",
        requestId: "life-history-error-1",
      });
    }
  });

  it("用固定 application 载荷提交并根据 201 meta 返回 created", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(successResponse(
      record(),
      201,
      { "X-Request-ID": "life-created-1" },
    ));

    await expect(submitLifeNavigationApplication(
      { note: "  希望梳理事业方向  " },
      { idempotencyKey: "life-application-001" },
    )).resolves.toMatchObject({
      status: "created",
      record: { id: "11", displayStatus: "submitted" },
      meta: {
        status: 201,
        requestId: "life-created-1",
        idempotencyReplayed: false,
      },
    });

    expect(fetchMock.mock.calls[0][0]).toBe("/api/v1/life-nav/records");
    expect(JSON.parse(String(fetchMock.mock.calls[0][1]?.body))).toEqual({
      dimension_id: "yun",
      record_type: "application",
      title: "服务广场导航申请",
      note: "希望梳理事业方向",
    });
  });

  it("根据 200 replay meta 返回 replayed 并复用显式幂等键", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(successResponse(
      record(),
      200,
      {
        "X-Request-ID": "life-replayed-1",
        "Idempotency-Replayed": "true",
      },
    ));

    await expect(submitLifeNavigationApplication(
      { note: "同一逻辑申请" },
      { idempotencyKey: "life-application-replay-001" },
    )).resolves.toMatchObject({
      status: "replayed",
      meta: {
        status: 200,
        requestId: "life-replayed-1",
        idempotencyReplayed: true,
      },
    });

    const headers = fetchMock.mock.calls[0][1]?.headers as Headers;
    expect(headers.get("Idempotency-Key")).toBe("life-application-replay-001");
  });
});
