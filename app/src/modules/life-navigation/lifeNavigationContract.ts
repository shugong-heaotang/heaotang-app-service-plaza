import {
  servicePlazaContractVersion,
  type ServiceLifecycleStatus,
  type ServiceManifest,
} from "../../domain/serviceCatalog";

export const lifeNavigationServiceId = "life-navigation" as const;
export const lifeNavigationRoute = "/services/life-navigation" as const;

export type LifeNavigationModuleContract = {
  contractVersion: typeof servicePlazaContractVersion;
  serviceId: typeof lifeNavigationServiceId;
  displayName: string;
  summary: string;
  lifecycleStatus: ServiceLifecycleStatus;
  returnTarget: string;
  providerId: string;
  requiredScopes: readonly string[];
};

/**
 * Maps the platform-owned manifest to the narrow boundary consumed by the
 * replaceable Life Navigation feature. Business fields deliberately do not
 * belong here: they remain owned by whichever feature adapter is mounted.
 */
export const mapLifeNavigationManifest = (
  manifest: ServiceManifest,
): LifeNavigationModuleContract => {
  if (manifest.contract_version !== servicePlazaContractVersion) {
    throw new Error(`生命导航不支持接入协议：${manifest.contract_version}`);
  }

  if (manifest.service_id !== lifeNavigationServiceId) {
    throw new Error(`生命导航收到错误的服务标识：${manifest.service_id}`);
  }

  if (
    manifest.entry.type !== "internal_route" ||
    manifest.entry.target !== lifeNavigationRoute
  ) {
    throw new Error("生命导航必须通过标准内部路由接入");
  }

  if (!manifest.entry.return_target.startsWith("/services")) {
    throw new Error("生命导航缺少受平台治理的返回路径");
  }

  return {
    contractVersion: manifest.contract_version,
    serviceId: lifeNavigationServiceId,
    displayName: manifest.display_name,
    summary: manifest.summary,
    lifecycleStatus: manifest.lifecycle_status,
    returnTarget: manifest.entry.return_target,
    providerId: manifest.provider.provider_id,
    requiredScopes: [...manifest.access.required_scopes],
  };
};
