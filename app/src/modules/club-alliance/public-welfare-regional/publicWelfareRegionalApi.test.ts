import { afterEach, describe, expect, it, vi } from "vitest";
import { tokenStorage } from "../../../infrastructure/apiClient";
import { publicWelfareRegionalApi } from "./publicWelfareRegionalApi";

const response = (data: unknown) => new Response(JSON.stringify({ success: true, data }), {
  status: 200, headers: { "Content-Type": "application/json" },
});
const urlOf = (input: RequestInfo | URL) => typeof input === "string" ? input : input instanceof URL ? input.toString() : input.url;

describe("publicWelfareRegionalApi", () => {
  afterEach(() => { vi.restoreAllMocks(); sessionStorage.clear(); });

  it("submits standard+charity establishment conditions and PDCAR with an idempotency key", async () => {
    tokenStorage.set("synthetic-token");
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(response({ application: { id: 1, status: "submitted" } }));
    await publicWelfareRegionalApi.submitEstablishment({
      name: "合成公益俱乐部", province: "浙江省", city: "杭州市", district: "西湖区", mission: "助老",
      eligibility: "三名发起人", resources: "志愿者", governance: "理事会", risks: "隐私风险",
      pdcar: { plan: "计划", do: "执行", check: "检查", act: "改进", record: "记录" },
    }, { idempotencyKey: "pw-establishment-001" });
    const [input, init] = fetchMock.mock.calls[0];
    expect(urlOf(input)).toContain("/api/v1/clubs/public-welfare-establishment-applications");
    expect(init?.method).toBe("POST");
    expect(new Headers(init?.headers).get("Idempotency-Key")).toBe("pw-establishment-001");
    expect(JSON.parse(String(init?.body))).toMatchObject({ type: "standard", category: "charity", pdcar: { record: "记录" } });
  });

  it("keeps center lookup anonymous and applies all address filters", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(response({ items: [], total: 0 }));
    await publicWelfareRegionalApi.searchCenters({ province: "浙江省", city: "杭州市", district: "西湖区", query: "古荡", kind: "public_welfare_service_center" });
    const [input, init] = fetchMock.mock.calls[0];
    const url = new URL(urlOf(input), "https://heaotang.invalid");
    expect(url.pathname).toBe("/api/v1/club-alliance/service-centers");
    expect(Object.fromEntries(url.searchParams)).toEqual({ province: "浙江省", city: "杭州市", district: "西湖区", query: "古荡", kind: "public_welfare_service_center" });
    expect(new Headers(init?.headers).has("Authorization")).toBe(false);
  });

  it("records a required review note when approving a regional role", async () => {
    tokenStorage.set("synthetic-token");
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(response({ application: { id: 9, status: "approved" } }));
    await publicWelfareRegionalApi.reviewRegionalRole({ applicationId: 9, decision: "approved", note: "条件完整，同意任职" }, { idempotencyKey: "regional-review-009" });
    const [input, init] = fetchMock.mock.calls[0];
    expect(urlOf(input)).toContain("/api/v1/club-alliance/regional-role-applications/9/review");
    expect(JSON.parse(String(init?.body))).toEqual({ decision: "approved", note: "条件完整，同意任职" });
  });
});
