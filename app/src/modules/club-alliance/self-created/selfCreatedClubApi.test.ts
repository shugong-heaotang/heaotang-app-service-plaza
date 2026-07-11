import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { tokenStorage } from "../../../infrastructure/apiClient";
import { selfCreatedClubApi } from "./selfCreatedClubApi";

const jsonResponse = (
  data: unknown,
  status = 200,
  headers: Record<string, string> = {},
) => new Response(JSON.stringify({ success: true, data }), {
  status,
  headers: { "Content-Type": "application/json", ...headers },
});

const club = (patch: Record<string, unknown> = {}) => ({
  id: 101,
  name: "合成晨光俱乐部",
  intro: "仅用于自动化的虚构简介",
  city: "合成城市",
  type: "standard",
  category: "general",
  status: "active",
  ...patch,
});

const requestUrl = (input: RequestInfo | URL) => {
  if (typeof input === "string") return input;
  return input instanceof URL ? input.toString() : input.url;
};

describe("selfCreatedClubApi", () => {
  beforeEach(() => {
    sessionStorage.clear();
    tokenStorage.set("synthetic-sc-test-token");
  });

  afterEach(() => {
    vi.restoreAllMocks();
    sessionStorage.clear();
  });

  it("只调用服务端 standard+general 权威筛选并保留服务端分页", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(jsonResponse({
      items: [club({ owner_id: 999, description: "禁止展示" })],
      total: 21,
      page: 2,
      size: 5,
    }));

    const result = await selfCreatedClubApi.search({
      page: 2,
      size: 5,
      query: "晨光",
      city: "合成城市",
    });

    expect(requestUrl(fetchMock.mock.calls[0][0])).toBe(
      "/api/v1/clubs/search?type=standard&category=general&page=2&size=5&q=%E6%99%A8%E5%85%89&city=%E5%90%88%E6%88%90%E5%9F%8E%E5%B8%82",
    );
    expect(result).toEqual({
      items: [{
        id: 101,
        name: "合成晨光俱乐部",
        intro: "仅用于自动化的虚构简介",
        city: "合成城市",
      }],
      total: 21,
      page: 2,
      size: 5,
    });
    expect(JSON.stringify(result)).not.toMatch(/owner_id|description/);
    expect(requestUrl(fetchMock.mock.calls[0][0])).not.toBe("/api/v1/clubs");
  });

  it.each([
    ["公益", { category: "charity" }],
    ["家庭", { type: "family" }],
    ["非活跃", { status: "pending" }],
  ])("对%s串类数据失败关闭而不是前端伪筛选", async (_label, patch) => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(jsonResponse({
      items: [club(patch)],
      total: 1,
      page: 1,
      size: 20,
    }));

    await expect(selfCreatedClubApi.search()).rejects.toMatchObject({
      code: "CLUB_CATEGORY_CROSSOVER_DETECTED",
    });
  });

  it("未登录时共享适配器在发请求前失败关闭", async () => {
    tokenStorage.clear();
    const fetchMock = vi.spyOn(globalThis, "fetch");

    await expect(selfCreatedClubApi.search()).rejects.toMatchObject({
      status: 401,
      code: "AUTH_REQUIRED",
    });
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("详情只投影 intro 与允许字段，语义漂移统一按边界错误拒绝", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(jsonResponse({
        ...club(),
        member_count: 9,
        created_at: "2026-07-12T00:00:00Z",
        owner_id: 777,
      }))
      .mockResolvedValueOnce(jsonResponse({
        ...club({ category: "charity" }),
        member_count: 9,
        created_at: "2026-07-12T00:00:00Z",
      }));

    await expect(selfCreatedClubApi.detail(101)).resolves.toEqual({
      id: 101,
      name: "合成晨光俱乐部",
      intro: "仅用于自动化的虚构简介",
      city: "合成城市",
      memberCount: 9,
      createdAt: "2026-07-12T00:00:00Z",
    });
    expect(requestUrl(fetchMock.mock.calls[0][0])).toBe("/api/v1/clubs/101");
    await expect(selfCreatedClubApi.detail(101)).rejects.toMatchObject({
      code: "CLUB_CATEGORY_CROSSOVER_DETECTED",
    });
  });

  it("非法详情 ID 不发网络请求", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch");
    await expect(selfCreatedClubApi.detail(Number.NaN)).rejects.toMatchObject({
      code: "CLUB_ID_INVALID",
      status: 0,
    });
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("加入写入使用显式 Idempotency-Key 并识别服务端重放", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(jsonResponse({
      status: "pending",
      application: {
        id: 701,
        club_id: 101,
        message: "希望加入",
        status: "pending",
        created_at: "2026-07-12T00:00:00Z",
      },
    }, 200, { "Idempotency-Replayed": "true" }));

    const result = await selfCreatedClubApi.join(101, "  希望加入  ", {
      idempotencyKey: "club-alliance-join-synthetic-001",
    });

    expect(requestUrl(fetchMock.mock.calls[0][0])).toBe("/api/v1/clubs/101/join");
    const init = fetchMock.mock.calls[0][1];
    expect((init?.headers as Headers).get("Idempotency-Key")).toBe(
      "club-alliance-join-synthetic-001",
    );
    expect(JSON.parse(String(init?.body))).toEqual({ message: "希望加入" });
    expect(result.status).toBe("replayed");
    expect(result.application.status).toBe("pending");
  });

  it("本人申请只发送分页与状态，不发送或接受 user_id", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(jsonResponse({
      items: [{
        id: 801,
        club_id: 101,
        status: "approved",
        created_at: "2026-07-12T00:00:00Z",
        user_id: 1001,
        reviewed_by: 9001,
      }],
      total: 1,
      page: 1,
      size: 20,
    }));

    const result = await selfCreatedClubApi.myApplications({ status: "approved" });

    expect(requestUrl(fetchMock.mock.calls[0][0])).toBe(
      "/api/v1/clubs/join-applications/my?page=1&size=20&status=approved",
    );
    expect(requestUrl(fetchMock.mock.calls[0][0])).not.toContain("user_id");
    expect(JSON.stringify(result)).not.toMatch(/user_id|reviewed_by/);
    expect(result.items[0].status).toBe("approved");
  });

  it("所有操作保持在 SC allowlist，禁止管理和其他分类能力", async () => {
    const calls: string[] = [];
    vi.spyOn(globalThis, "fetch").mockImplementation(async (input, init) => {
      const url = requestUrl(input);
      calls.push(`${(init?.method ?? "GET").toUpperCase()} ${url}`);
      if (url.includes("/search?")) {
        return jsonResponse({ items: [], total: 0, page: 1, size: 20 });
      }
      if (url.endsWith("/join-applications/my?page=1&size=20")) {
        return jsonResponse({ items: [], total: 0, page: 1, size: 20 });
      }
      if (url.endsWith("/101")) {
        return jsonResponse({ ...club(), member_count: 1, created_at: "2026-07-12T00:00:00Z" });
      }
      if (url.endsWith("/101/join")) {
        return jsonResponse({
          status: "pending",
          application: { id: 1, club_id: 101, status: "pending", created_at: "2026-07-12T00:00:00Z" },
        }, 201);
      }
      throw new Error(`unexpected ${url}`);
    });

    await selfCreatedClubApi.search();
    await selfCreatedClubApi.detail(101);
    await selfCreatedClubApi.join(101, "", { idempotencyKey: "club-alliance-join-synthetic-002" });
    await selfCreatedClubApi.myApplications();

    expect(calls).toHaveLength(4);
    expect(calls.join("\n")).not.toMatch(
      /\/clubs$|create|review|members?|payment|withdraw|refund|subscription|charity|family|federation/i,
    );
  });
});
