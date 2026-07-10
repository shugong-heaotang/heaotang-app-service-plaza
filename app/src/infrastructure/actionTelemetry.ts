import type { ActionAccessDecision } from "./actionExecutor";
import { apiRequest, tokenStorage } from "./apiClient";
import type { ServiceAction } from "../domain/serviceActions";

type FeatureFlag = {
  key: string;
  enabled: boolean;
};

type FeatureFlagResponse = {
  items: FeatureFlag[];
};

type ActionEventResult = {
  accepted: boolean;
  reason?: "feature_disabled";
};

export type ActionEventOutcome = "activated" | "blocked";
export type ActionEventReason = "none" | Exclude<ActionAccessDecision, { allowed: true }>["reason"];

const actionTelemetryFlag = "action_telemetry";
const featureFlagCacheTtlMs = 60_000;
let featureFlagsPromise: Promise<ReadonlyMap<string, boolean>> | undefined;
let featureFlagsLoadedAt = 0;

const loadFeatureFlags = async (): Promise<ReadonlyMap<string, boolean>> => {
  try {
    const result = await apiRequest<FeatureFlagResponse>(
      "/api/v1/service-plaza/feature-flags",
      {},
      { retry: true },
    );
    return new Map(result.items.map((flag) => [flag.key, flag.enabled]));
  } catch {
    // Configuration failures are intentionally fail-closed.
    return new Map();
  }
};

export const primeFeatureFlags = () => {
  const now = Date.now();
  if (!featureFlagsPromise || now - featureFlagsLoadedAt >= featureFlagCacheTtlMs) {
    featureFlagsLoadedAt = now;
    featureFlagsPromise = loadFeatureFlags();
  }
  return featureFlagsPromise;
};

export const invalidateFeatureFlagCache = () => {
  featureFlagsPromise = undefined;
  featureFlagsLoadedAt = 0;
};

export async function reportActionEvent(
  action: ServiceAction,
  outcome: ActionEventOutcome,
  reason: ActionEventReason,
): Promise<ActionEventResult> {
  const flags = await primeFeatureFlags();
  if (flags.get(actionTelemetryFlag) !== true) {
    return { accepted: false, reason: "feature_disabled" };
  }

  try {
    return await apiRequest<ActionEventResult>(
      "/api/v1/service-plaza/action-events",
      {
        method: "POST",
        body: JSON.stringify({
          action_id: action.action_id,
          telemetry_event: action.telemetry_event,
          outcome,
          reason,
        }),
      },
      { auth: Boolean(tokenStorage.get()) },
    );
  } catch {
    // Telemetry must never block the user's navigation path.
    return { accepted: false };
  }
}
