import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { tokenStorage } from "./apiClient";
import { realSubmissionRepository } from "./submissionRepository";

const successResponse = (data: unknown = { id: 1 }) =>
  new Response(JSON.stringify({ success: true, data }), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });

describe("realSubmissionRepository", () => {
  beforeEach(() => {
    sessionStorage.clear();
    tokenStorage.set("contract-test-token");
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("将生命导航申请映射到生命记录接口", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(successResponse());

    await realSubmissionRepository.submit("life-navigation", { note: "希望梳理事业方向" });

    expect(fetchMock.mock.calls[0][0]).toBe("/api/v1/life-nav/records");
    const body = JSON.parse(String(fetchMock.mock.calls[0][1]?.body));
    expect(body).toMatchObject({
      dimension_id: "yun",
      record_type: "application",
      title: "服务广场导航申请",
      note: "希望梳理事业方向",
    });
    const headers = fetchMock.mock.calls[0][1]?.headers as Headers;
    expect(headers.get("Idempotency-Key")).toMatch(/^life-navigation-/);
  });

  it("将俱乐部申请映射到指定俱乐部加入接口", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      successResponse({ status: "pending", application: { id: 72, status: "pending" } }),
    );

    const submission = await realSubmissionRepository.submit("club-alliance", { clubId: 12, note: "希望加入" });

    expect(fetchMock.mock.calls[0][0]).toBe("/api/v1/clubs/12/join");
    expect(JSON.parse(String(fetchMock.mock.calls[0][1]?.body))).toEqual({ message: "希望加入" });
    expect(submission.id).toBe("72");
    const headers = fetchMock.mock.calls[0][1]?.headers as Headers;
    expect(headers.get("Idempotency-Key")).toMatch(/^club-alliance-/);
  });

  it("俱乐部申请缺少俱乐部时拒绝提交", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch");
    await expect(realSubmissionRepository.submit("club-alliance")).rejects.toThrow(
      "请选择要申请加入的俱乐部",
    );
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("将健康需求映射到健康咨询接口", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(successResponse());

    await realSubmissionRepository.submit("health-manager", {
      patientName: "测试用户",
      symptoms: "近期睡眠不佳",
    });

    expect(fetchMock.mock.calls[0][0]).toBe("/api/v1/health/consultations");
    expect(JSON.parse(String(fetchMock.mock.calls[0][1]?.body))).toEqual({
      patient_name: "测试用户",
      symptoms: "近期睡眠不佳",
    });
    const headers = fetchMock.mock.calls[0][1]?.headers as Headers;
    expect(headers.get("Idempotency-Key")).toMatch(/^health-manager-/);
  });

  it("用户未填写症状时绝不伪造健康内容", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(
        JSON.stringify({
          success: false,
          code: "HEALTH_SYMPTOMS_REQUIRED",
          error: "symptoms is required",
        }),
        { status: 400, headers: { "Content-Type": "application/json" } },
      ),
    );

    await expect(
      realSubmissionRepository.submit("health-manager", {
        patientName: "合成测试用户",
        symptoms: "   ",
      }),
    ).rejects.toMatchObject({ code: "HEALTH_SYMPTOMS_REQUIRED" });

    const requestBody = String(fetchMock.mock.calls[0][1]?.body);
    expect(JSON.parse(requestBody)).toEqual({
      patient_name: "合成测试用户",
      symptoms: "",
    });
    expect(requestBody).not.toContain("希望获得健康咨询");
  });
});
