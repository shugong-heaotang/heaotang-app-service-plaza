import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import type { ServiceAction } from "../domain/serviceActions";
import {
  guestActionSession,
  type ActionAccessDecision,
  type ActionSession,
} from "../infrastructure/actionExecutor";
import { useAuth } from "./AuthContext";
import { primeFeatureFlags } from "../infrastructure/actionTelemetry";

type ActionRuntimeValue = {
  session: ActionSession;
  reportAccessRequirement(action: ServiceAction, decision: ActionAccessDecision): void;
};

const dispatchAccessRequirement = (
  action: ServiceAction,
  decision: ActionAccessDecision,
) => {
  if (decision.allowed || typeof window === "undefined") return;
  window.dispatchEvent(
    new CustomEvent("heaotang:action-access-required", {
      detail: {
        action_id: action.action_id,
        reason: decision.reason,
        missing_scopes: decision.missingScopes ?? [],
        telemetry_event: action.telemetry_event,
      },
    }),
  );
};

const ActionRuntimeContext = createContext<ActionRuntimeValue>({
  session: guestActionSession,
  reportAccessRequirement: dispatchAccessRequirement,
});

export function ActionRuntimeProvider({ children }: { children: ReactNode }) {
  const { isAuthenticated, user } = useAuth();
  const [accessNotice, setAccessNotice] = useState("");
  useEffect(() => {
    void primeFeatureFlags();
  }, []);
  const reportAccessRequirement = useCallback((action: ServiceAction, decision: ActionAccessDecision) => {
    dispatchAccessRequirement(action, decision);
    if (decision.allowed) return;
    setAccessNotice(
      decision.reason === "scope_required"
        ? `${action.label}暂不可访问：当前账号缺少 ${decision.missingScopes?.join("、") || "所需"} 权限。`
        : `${action.label}需要先完成登录。`,
    );
  }, []);
  const value = useMemo<ActionRuntimeValue>(
    () => ({
      session: {
        authenticated: isAuthenticated,
        scopes: user?.scopes ?? [],
      },
      reportAccessRequirement,
    }),
    [isAuthenticated, reportAccessRequirement, user?.scopes],
  );
  return (
    <ActionRuntimeContext.Provider value={value}>
      {children}
      {accessNotice && (
        <div className="global-action-notice" role="alert">
          <span>{accessNotice}</span>
          <button type="button" onClick={() => setAccessNotice("")}>关闭</button>
        </div>
      )}
    </ActionRuntimeContext.Provider>
  );
}

export const useActionRuntime = () => useContext(ActionRuntimeContext);
