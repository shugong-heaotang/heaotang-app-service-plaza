import { describe, expect, it } from "vitest";
import { ActivityContractError, mapActivityM1Payload } from "./activityAdapter";
import { activityM1SyntheticPayload } from "./activityMockRepository";

const clone = () => structuredClone(activityM1SyntheticPayload) as Record<string, any>;

describe("activity M1 strict adapter", () => {
  it("maps the approved public activity and separated proposer approval", () => {
    const model = mapActivityM1Payload(activityM1SyntheticPayload);
    expect(model.state).toBe("ready");
    expect(model.activities?.[0]).toMatchObject({ registrationStatus: "available", remainingCapacity: 12 });
    expect(model.proposals?.[0]).toMatchObject({ status: "club_review", proposerCanApprove: false });
  });

  it("maps an empty payload without inventing data", () => {
    expect(mapActivityM1Payload({ execution_mode: "mock-only", activities: [], proposals: [] })).toEqual({
      state: "empty",
      activities: [],
      proposals: [],
    });
  });

  it.each([
    ["club approval", (p: Record<string, any>) => { p.activities[0].club_approval_status = "pending"; }],
    ["platform review", (p: Record<string, any>) => { p.activities[0].platform_review_status = "pending"; }],
    ["cancelled lifecycle", (p: Record<string, any>) => { p.activities[0].lifecycle_status = "cancelled"; }],
    ["closed discovery window", (p: Record<string, any>) => { p.activities[0].within_discovery_window = false; }],
  ])("fails closed on %s", (_name, mutate) => {
    const payload = clone();
    mutate(payload);
    expect(() => mapActivityM1Payload(payload)).toThrow("公开发现");
  });

  it("rejects paid activity data", () => {
    const payload = clone();
    payload.activities[0].price_minor = 1;
    expect(() => mapActivityM1Payload(payload)).toThrow("仅允许免费报名");
  });

  it.each([
    ["external detail target", (p: Record<string, any>) => { p.activities[0].detail_target = "https://example.test/activity"; }, "内部详情路由"],
    ["invalid schedule", (p: Record<string, any>) => { p.activities[0].starts_at = "tomorrow maybe"; }, "有效时间"],
    ["available without capacity", (p: Record<string, any>) => { p.activities[0].remaining_capacity = 0; }, "剩余名额不一致"],
    ["full with capacity", (p: Record<string, any>) => { p.activities[0].registration_status = "full"; }, "剩余名额不一致"],
  ])("rejects %s", (_name, mutate, message) => {
    const payload = clone();
    mutate(payload);
    expect(() => mapActivityM1Payload(payload)).toThrow(message);
  });

  it("rejects proposer self approval", () => {
    const payload = clone();
    payload.proposals[0].proposer_can_approve = true;
    expect(() => mapActivityM1Payload(payload)).toThrow("提案人不得");
  });

  it("rejects unexpected privacy or payment fields", () => {
    const payload = clone();
    payload.activities[0].participant_names = ["synthetic-person"];
    expect(() => mapActivityM1Payload(payload)).toThrow(ActivityContractError);
  });

  it("rejects non mock execution", () => {
    const payload = clone();
    payload.execution_mode = "production";
    expect(() => mapActivityM1Payload(payload)).toThrow("mock-only");
  });
});
