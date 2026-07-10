import { isEnabledAction, type ServiceAction } from "../domain/serviceActions";

export type ActionSession = {
  authenticated: boolean;
  scopes: readonly string[];
};

export type ActionAccessDecision =
  | { allowed: true }
  | {
      allowed: false;
      reason:
        | "lifecycle_unavailable"
        | "authentication_required"
        | "scope_required"
        | "handler_unavailable";
      missingScopes?: string[];
    };

export const guestActionSession: ActionSession = {
  authenticated: false,
  scopes: [],
};

const isInternalTarget = (target: string) => target.startsWith("/");
const isExternalTarget = (target: string) => target.startsWith("https://");
const isPlatformTarget = (target: string) => target.startsWith("heaotang://");

export function validateActionDefinition(action: ServiceAction): void {
  if (action.action_type === "platform_command") {
    if (!isPlatformTarget(action.target)) {
      throw new Error(`平台命令 ${action.action_id} 必须使用 heaotang:// 目标`);
    }
    return;
  }

  if (!isInternalTarget(action.target) && !isExternalTarget(action.target)) {
    throw new Error(`动作 ${action.action_id} 使用了未登记的目标协议`);
  }
  if (isExternalTarget(action.target) && action.access.auth_mode === "shared_session") {
    throw new Error(`外部动作 ${action.action_id} 不得接收平台共享会话`);
  }
  if (action.access.auth_mode === "oidc_pkce" && !isExternalTarget(action.target)) {
    throw new Error(`OIDC/PKCE 动作 ${action.action_id} 必须指向 HTTPS 外部服务`);
  }
}

export function evaluateActionAccess(
  action: ServiceAction,
  session: ActionSession,
  handlers: { platformCommand?: boolean; oidcLaunch?: boolean } = {},
): ActionAccessDecision {
  if (!isEnabledAction(action)) {
    return { allowed: false, reason: "lifecycle_unavailable" };
  }
  if (action.access.auth_mode !== "anonymous" && !session.authenticated) {
    return { allowed: false, reason: "authentication_required" };
  }

  const granted = new Set(session.scopes);
  const missingScopes = action.access.required_scopes.filter((scope) => !granted.has(scope));
  if (missingScopes.length > 0) {
    return { allowed: false, reason: "scope_required", missingScopes };
  }
  if (action.action_type === "platform_command" && !handlers.platformCommand) {
    return { allowed: false, reason: "handler_unavailable" };
  }
  if (action.access.auth_mode === "oidc_pkce" && !handlers.oidcLaunch) {
    return { allowed: false, reason: "handler_unavailable" };
  }
  return { allowed: true };
}
