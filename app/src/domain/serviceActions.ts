import type { ServiceLifecycleStatus } from "./serviceCatalog";

export const serviceActionContractVersion = "service-plaza.action.v1" as const;

export type ServiceActionRegion =
  | "topbar"
  | "core_services"
  | "club_alliance"
  | "common_services"
  | "primary_navigation";

export type ServiceActionType =
  | "service_entry"
  | "service_variant"
  | "platform_command"
  | "primary_navigation";

export type ServiceAction = {
  action_id: string;
  region: ServiceActionRegion;
  sort_order: number;
  label: string;
  action_type: ServiceActionType;
  target: string;
  lifecycle_status: ServiceLifecycleStatus;
  access: {
    auth_mode: "shared_session" | "oidc_pkce" | "anonymous";
    required_scopes: string[];
  };
  service_id?: string | null;
  return_target: string;
  telemetry_event: string;
};

export type ServiceActionCatalog = {
  contract_version: typeof serviceActionContractVersion;
  count: number;
  items: ServiceAction[];
};

export const servicePlazaActionIds = [
  "page-ai-assistant",
  "life-navigation",
  "club-alliance",
  "club-manage",
  "public-benefit-club",
  "self-created-club",
  "family-club",
  "club-federation",
  "health-manager",
  "common-more",
  "activity-plaza",
  "network-center",
  "protection-mall",
  "secondhand-market",
  "ai-assistant",
  "learning-plaza",
  "primary-home",
  "primary-services",
  "primary-discover",
  "primary-profile",
] as const;

export const isEnabledAction = (action: ServiceAction) =>
  action.lifecycle_status === "active" || action.lifecycle_status === "preview";

export const actionsInRegion = (
  actions: readonly ServiceAction[],
  region: ServiceActionRegion,
) =>
  actions
    .filter((action) => action.region === region)
    .sort((left, right) => left.sort_order - right.sort_order);
