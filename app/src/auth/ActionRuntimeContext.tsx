import { createContext, useContext, useEffect, useMemo, type ReactNode } from "react";
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

const reportAccessRequirement = (
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
  reportAccessRequirement,
});

export function ActionRuntimeProvider({ children }: { children: ReactNode }) {
  const { isAuthenticated, user } = useAuth();
  useEffect(() => {
    void primeFeatureFlags();
  }, []);
  const value = useMemo<ActionRuntimeValue>(
    () => ({
      session: {
        authenticated: isAuthenticated,
        scopes: user?.scopes ?? [],
      },
      reportAccessRequirement,
    }),
    [isAuthenticated, user?.scopes],
  );
  return <ActionRuntimeContext.Provider value={value}>{children}</ActionRuntimeContext.Provider>;
}

export const useActionRuntime = () => useContext(ActionRuntimeContext);
