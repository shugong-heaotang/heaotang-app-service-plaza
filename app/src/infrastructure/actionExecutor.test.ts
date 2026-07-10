import { describe, expect, it } from "vitest";
import type { ServiceAction } from "../domain/serviceActions";
import {
  evaluateActionAccess,
  guestActionSession,
  validateActionDefinition,
} from "./actionExecutor";

const action = (overrides: Partial<ServiceAction> = {}): ServiceAction => ({
  action_id: "test-action",
  region: "common_services",
  sort_order: 10,
  label: "测试动作",
  action_type: "service_entry",
  target: "/services/test",
  lifecycle_status: "active",
  access: { auth_mode: "anonymous", required_scopes: [] },
  return_target: "/services",
  telemetry_event: "service_plaza.test_action.open",
  ...overrides,
});

describe("标准动作执行策略", () => {
  it("未登录用户不能执行共享会话动作", () => {
    expect(
      evaluateActionAccess(
        action({ access: { auth_mode: "shared_session", required_scopes: [] } }),
        guestActionSession,
      ),
    ).toEqual({ allowed: false, reason: "authentication_required" });
  });

  it("缺少 scope 时默认拒绝并列出缺失项", () => {
    expect(
      evaluateActionAccess(
        action({ access: { auth_mode: "shared_session", required_scopes: ["club:manage"] } }),
        { authenticated: true, scopes: ["club:read"] },
      ),
    ).toEqual({ allowed: false, reason: "scope_required", missingScopes: ["club:manage"] });
  });

  it("scope 完整时允许执行", () => {
    expect(
      evaluateActionAccess(
        action({ access: { auth_mode: "shared_session", required_scopes: ["club:manage"] } }),
        { authenticated: true, scopes: ["club:manage"] },
      ),
    ).toEqual({ allowed: true });
  });

  it("拒绝把平台共享会话带到外部 HTTPS", () => {
    expect(() =>
      validateActionDefinition(
        action({
          target: "https://partner.example/app",
          access: { auth_mode: "shared_session", required_scopes: [] },
        }),
      ),
    ).toThrow("不得接收平台共享会话");
  });

  it("OIDC 外部动作在没有受控启动器时不可执行", () => {
    const oidcAction = action({
      target: "https://partner.example/app",
      access: { auth_mode: "oidc_pkce", required_scopes: [] },
    });
    validateActionDefinition(oidcAction);
    expect(
      evaluateActionAccess(oidcAction, { authenticated: true, scopes: [] }),
    ).toEqual({ allowed: false, reason: "handler_unavailable" });
  });

  it("平台命令必须由白名单处理器执行", () => {
    const command = action({
      action_type: "platform_command",
      target: "heaotang://ai-assistant",
    });
    expect(evaluateActionAccess(command, guestActionSession)).toEqual({
      allowed: false,
      reason: "handler_unavailable",
    });
    expect(evaluateActionAccess(command, guestActionSession, { platformCommand: true })).toEqual({
      allowed: true,
    });
  });
});
