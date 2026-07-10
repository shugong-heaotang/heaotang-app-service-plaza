export const servicePlazaContractVersion = "service-plaza.v1" as const;

export type ServiceLifecycleStatus =
  | "active"
  | "preview"
  | "planned"
  | "maintenance"
  | "offline";

export type ServiceManifest = {
  contract_version: typeof servicePlazaContractVersion;
  service_id: string;
  display_name: string;
  summary: string;
  category: "core" | "common";
  sort_order: number;
  lifecycle_status: ServiceLifecycleStatus;
  entry: {
    type: "internal_route" | "external_https" | "mini_program";
    target: string;
    return_target: string;
  };
  access: {
    auth_mode: "shared_session" | "oidc_pkce" | "anonymous";
    required_scopes: string[];
  };
  provider: {
    provider_id: string;
    display_name: string;
  };
  capabilities: string[];
  privacy_level: "public" | "account" | "sensitive";
  business_api_version: string;
};

export type ServiceCatalog = {
  contract_version: typeof servicePlazaContractVersion;
  schema_url?: string;
  items: ServiceManifest[];
};

export const isNavigableService = (service: ServiceManifest) =>
  service.lifecycle_status === "active" || service.lifecycle_status === "preview";
