import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { ServiceAction } from "../domain/serviceActions";
import { invalidateFeatureFlagCache, reportActionEvent } from "./actionTelemetry";
import { tokenStorage } from "./apiClient";

const action: ServiceAction = {
  action_id: "life-navigation",
  region: "core_services",
  sort_order: 20,
  label: "生命导航",
  action_type: "service_entry",
  target: "/services/life-navigation",
  lifecycle_status: "active",
  access: { auth_mode: "shared_session", required_scopes: [] },
  service_id: "life-navigation",
  return_target: "/services",
  telemetry_event: "service_plaza.life_navigation.open",
};

describe("集中动作遥测", () => {
  beforeEach(() => {
    invalidateFeatureFlagCache();
    tokenStorage.clear();
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
  });

  it("配置读取失败时默认关闭且不提交事件", async () => {
    const fetchMock = vi.fn().mockRejectedValue(new Error("offline"));
    vi.stubGlobal("fetch", fetchMock);

    await expect(reportActionEvent(action, "activated", "none")).resolves.toEqual({
      accepted: false,
      reason: "feature_disabled",
    });
    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(fetchMock.mock.calls.every(([url]) => String(url).endsWith("/feature-flags"))).toBe(true);
  });

  it("只有公开开关启用后才提交白名单事件字段", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(new Response(JSON.stringify({
        success: true,
        data: { items: [{ key: "action_telemetry", enabled: true }] },
      }), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({
        success: true,
        data: { accepted: true },
      }), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);

    await expect(reportActionEvent(action, "blocked", "scope_required")).resolves.toEqual({
      accepted: true,
    });

    expect(fetchMock).toHaveBeenCalledTimes(2);
    const [url, init] = fetchMock.mock.calls[1] as [string, RequestInit];
    expect(url).toContain("/api/v1/service-plaza/action-events");
    expect(JSON.parse(String(init.body))).toEqual({
      action_id: "life-navigation",
      telemetry_event: "service_plaza.life_navigation.open",
      outcome: "blocked",
      reason: "scope_required",
    });
    const headers = new Headers(init.headers);
    expect(headers.get("X-Request-ID")).toBeTruthy();
    expect(headers.has("Authorization")).toBe(false);
  });

  it("缓存到期后重新读取开关而不要求用户刷新页面", async () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date("2026-07-10T00:00:00Z"));
    const envelope = (data: unknown) => new Response(JSON.stringify({ success: true, data }), {
      status: 200,
    });
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(envelope({ items: [{ key: "action_telemetry", enabled: true }] }))
      .mockResolvedValueOnce(envelope({ accepted: true }))
      .mockResolvedValueOnce(envelope({ items: [{ key: "action_telemetry", enabled: false }] }));
    vi.stubGlobal("fetch", fetchMock);

    await expect(reportActionEvent(action, "activated", "none")).resolves.toEqual({ accepted: true });
    vi.advanceTimersByTime(60_001);
    await expect(reportActionEvent(action, "activated", "none")).resolves.toEqual({
      accepted: false,
      reason: "feature_disabled",
    });

    expect(fetchMock).toHaveBeenCalledTimes(3);
    expect(String(fetchMock.mock.calls[2][0])).toContain("/feature-flags");
  });
});
