import { afterEach, describe, expect, it, vi } from "vitest";
import { ApiError, tokenStorage } from "../../../infrastructure/apiClient";
import { loadMemberHome, mapMemberHomePayload, memberHomeEndpoint } from "./memberHomeApi";

const explore = [
  { actionId: "public-benefit-club", label: "公益俱乐部", href: "?category=公益俱乐部" },
  { actionId: "self-created-club", label: "自建俱乐部", href: "?category=自建俱乐部" },
  { actionId: "family-club", label: "家庭俱乐部", href: "?category=家庭俱乐部" },
  { actionId: "club-federation", label: "俱乐部友联体", href: "?category=俱乐部友联体" },
];
const payload = {
  display_name: "合成会员",
  joined_club_count: 1,
  pending_task_count: 1,
  unread_count: 0,
  clubs: [{ club_id: "c1", name: "合成俱乐部", kind: "自建俱乐部", member_role: "成员", club_status: "active", membership_status: "active", target: "/clubs/c1" }],
  tasks: [{ task_id: "t1", title: "查看申请", context: "待处理", target: "/tasks/t1" }],
  activities: [],
  feed: [],
  can_manage: false,
};

afterEach(() => { vi.restoreAllMocks(); tokenStorage.clear(); });

describe("memberHomeApi", () => {
  it("maps strict data and uses backend can_manage", () => {
    const model = mapMemberHomePayload({ ...payload, can_manage: true }, explore);
    expect(model).toMatchObject({ state: "ready", canManage: true });
    expect(model.clubs?.[0]).toMatchObject({ clubId: "c1", clubStatus: "active", membershipStatus: "active" });
    expect(model.explore).toEqual(explore);
  });

  it("maps declared section failures to fixed safe messages", () => {
    const model = mapMemberHomePayload({ ...payload, section_errors: { tasks: "CMH_TASKS_UNAVAILABLE" } }, explore);
    expect(model.state).toBe("partial-error");
    expect(model.sectionErrors).toEqual({ tasks: "待办暂时无法读取" });
    expect(JSON.stringify(model)).not.toContain("CMH_TASKS_UNAVAILABLE");
  });

  it.each([
    {},
    { ...payload, clubs: null },
    { ...payload, joined_club_count: -1 },
    { ...payload, can_manage: "yes" },
    { ...payload, clubs: [{ ...payload.clubs[0], kind: "友联体" }] },
    { ...payload, clubs: [{ ...payload.clubs[0], status: "正常" }] },
    { ...payload, clubs: [{ ...payload.clubs[0], club_status: undefined }] },
    { ...payload, clubs: [{ ...payload.clubs[0], membership_status: undefined }] },
    { ...payload, clubs: [{ ...payload.clubs[0], membership_status: "pending" }] },
    { ...payload, clubs: [{ ...payload.clubs[0], membership_status: "rejected" }] },
    { ...payload, clubs: [{ ...payload.clubs[0], membership_status: "left" }] },
    { ...payload, clubs: [{ ...payload.clubs[0], membership_status: "dissolved" }] },
    { ...payload, clubs: [{ ...payload.clubs[0], club_status: "dissolved" }] },
    { ...payload, section_errors: { unknown: "CMH_UNKNOWN" } },
    { ...payload, section_errors: { tasks: 503 } },
  ])("fails malformed data closed", (data) => {
    expect(() => mapMemberHomePayload(data, explore)).toThrowError(ApiError);
    try { mapMemberHomePayload(data, explore); } catch (error) {
      expect((error as ApiError).code).toBe("CMH_CONTRACT_INVALID");
    }
  });

  it("keeps optional suspended membership distinct from club lifecycle", () => {
    const model = mapMemberHomePayload({ ...payload, clubs: [{ ...payload.clubs[0], membership_status: "suspended" }] }, explore);
    expect(model.clubs?.[0]).toMatchObject({ clubStatus: "active", membershipStatus: "suspended" });
  });

  it("uses one authenticated strict endpoint", async () => {
    tokenStorage.set("synthetic-token");
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(JSON.stringify({ success: true, data: payload }), { status: 200, headers: { "Content-Type": "application/json" } }));
    await loadMemberHome(explore);
    expect(fetchMock).toHaveBeenCalledTimes(1);
    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toBe(memberHomeEndpoint);
    expect(new Headers(init?.headers).get("Authorization")).toBe("Bearer synthetic-token");
  });

  it("rejects a legacy non-envelope response", async () => {
    tokenStorage.set("synthetic-token");
    vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(JSON.stringify(payload), { status: 200, headers: { "Content-Type": "application/json" } }));
    await expect(loadMemberHome(explore)).rejects.toMatchObject({ code: "INVALID_API_ENVELOPE" });
  });

  it("never falls back to mock or empty arrays", () => {
    expect(loadMemberHome.toString()).not.toMatch(/catch|mock|return\s*\[\]/i);
  });
});
