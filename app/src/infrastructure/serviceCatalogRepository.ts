import {
  servicePlazaContractVersion,
  type ServiceCatalog,
  type ServiceManifest,
} from "../domain/serviceCatalog";
import {
  serviceActionContractVersion,
  servicePlazaActionIds,
  type ServiceAction,
  type ServiceActionCatalog,
  type ServiceActionRegion,
} from "../domain/serviceActions";
import { apiRequest } from "./apiClient";
import { validateActionDefinition } from "./actionExecutor";

export interface ServiceCatalogRepository {
  getCatalog(): Promise<ServiceCatalog>;
  getActions(): Promise<ServiceActionCatalog>;
}

const manifest = (
  serviceId: string,
  displayName: string,
  category: "core" | "common",
  sortOrder: number,
  lifecycleStatus: ServiceManifest["lifecycle_status"],
  target: string,
): ServiceManifest => ({
  contract_version: servicePlazaContractVersion,
  service_id: serviceId,
  display_name: displayName,
  summary: `${displayName}标准接入服务`,
  category,
  sort_order: sortOrder,
  lifecycle_status: lifecycleStatus,
  entry: { type: "internal_route", target, return_target: "/services" },
  access: { auth_mode: "shared_session", required_scopes: [] },
  provider: { provider_id: "heaotang", display_name: "和奥堂" },
  capabilities: ["navigate"],
  privacy_level: serviceId === "health-manager" ? "sensitive" : "account",
  business_api_version: "v1",
});

const mockItems = [
  manifest("life-navigation", "生命导航", "core", 10, "active", "/services/life-navigation"),
  manifest("club-alliance", "俱乐部联盟", "core", 20, "active", "/services/club-alliance"),
  manifest("health-manager", "健康大管家", "core", 30, "active", "/services/health-manager"),
  manifest("activity-plaza", "活动广场", "common", 110, "planned", "/services/activity-plaza"),
  manifest("network-center", "人脉中心", "common", 120, "planned", "/services/network-center"),
  manifest("protection-mall", "保障商城", "common", 130, "planned", "/services/protection-mall"),
  manifest("secondhand-market", "二手集市", "common", 140, "planned", "/services/secondhand-market"),
  manifest("ai-assistant", "AI", "common", 150, "planned", "/services/ai-assistant"),
  manifest("learning-plaza", "学习广场", "common", 160, "planned", "/services/learning-plaza"),
];

const action = (
  actionId: string,
  region: ServiceActionRegion,
  sortOrder: number,
  label: string,
  actionType: ServiceAction["action_type"],
  target: string,
  lifecycleStatus: ServiceAction["lifecycle_status"],
  telemetryEvent: string,
  serviceId: string | null = null,
  authMode: ServiceAction["access"]["auth_mode"] = "shared_session",
  requiredScopes: string[] = [],
): ServiceAction => ({
  action_id: actionId,
  region,
  sort_order: sortOrder,
  label,
  action_type: actionType,
  target,
  lifecycle_status: lifecycleStatus,
  access: { auth_mode: authMode, required_scopes: requiredScopes },
  ...(serviceId ? { service_id: serviceId } : {}),
  return_target: "/services",
  telemetry_event: telemetryEvent,
});

export const mockActions: ServiceAction[] = [
  action("page-ai-assistant", "topbar", 10, "页面 AI 助手", "platform_command", "heaotang://ai-assistant?context=service-plaza", "planned", "service_plaza.page_ai_assistant.open"),
  action("life-navigation", "core_services", 20, "生命导航", "service_entry", "/services/life-navigation", "active", "service_plaza.life_navigation.open", "life-navigation"),
  action("club-alliance", "club_alliance", 30, "俱乐部联盟", "service_entry", "/services/club-alliance", "active", "service_plaza.club_alliance.open", "club-alliance"),
  action("club-manage", "club_alliance", 40, "管理中心", "service_variant", "/services/club-alliance?view=manage", "preview", "service_plaza.club_manage.open", "club-alliance", "shared_session", ["club:manage"]),
  action("public-benefit-club", "club_alliance", 50, "公益俱乐部", "service_variant", "/services/club-alliance?category=%E5%85%AC%E7%9B%8A%E4%BF%B1%E4%B9%90%E9%83%A8", "active", "service_plaza.public_benefit_club.open", "club-alliance"),
  action("self-created-club", "club_alliance", 60, "自建俱乐部", "service_variant", "/services/club-alliance?category=%E8%87%AA%E5%BB%BA%E4%BF%B1%E4%B9%90%E9%83%A8", "active", "service_plaza.self_created_club.open", "club-alliance"),
  action("family-club", "club_alliance", 70, "家庭俱乐部", "service_variant", "/services/club-alliance?category=%E5%AE%B6%E5%BA%AD%E4%BF%B1%E4%B9%90%E9%83%A8", "active", "service_plaza.family_club.open", "club-alliance"),
  action("club-federation", "club_alliance", 80, "俱乐部友联体", "service_variant", "/services/club-alliance?category=%E4%BF%B1%E4%B9%90%E9%83%A8%E5%8F%8B%E8%81%94%E4%BD%93", "active", "service_plaza.club_federation.open", "club-alliance"),
  action("health-manager", "core_services", 90, "健康大管家", "service_entry", "/services/health-manager", "active", "service_plaza.health_manager.open", "health-manager"),
  action("common-more", "common_services", 100, "更多", "platform_command", "heaotang://service-plaza/more", "planned", "service_plaza.common_more.open", null, "anonymous"),
  action("activity-plaza", "common_services", 110, "活动广场", "service_entry", "/services/activity-plaza", "planned", "service_plaza.activity_plaza.open", "activity-plaza"),
  action("network-center", "common_services", 120, "人脉中心", "service_entry", "/services/network-center", "planned", "service_plaza.network_center.open", "network-center"),
  action("protection-mall", "common_services", 130, "保障商城", "service_entry", "/services/protection-mall", "planned", "service_plaza.protection_mall.open", "protection-mall"),
  action("secondhand-market", "common_services", 140, "二手集市", "service_entry", "/services/secondhand-market", "planned", "service_plaza.secondhand_market.open", "secondhand-market"),
  action("ai-assistant", "common_services", 150, "AI", "service_entry", "/services/ai-assistant", "planned", "service_plaza.ai_assistant.open", "ai-assistant"),
  action("learning-plaza", "common_services", 160, "学习广场", "service_entry", "/services/learning-plaza", "planned", "service_plaza.learning_plaza.open", "learning-plaza"),
  action("primary-home", "primary_navigation", 170, "首页", "primary_navigation", "/", "planned", "service_plaza.primary_home.open", null, "anonymous"),
  action("primary-services", "primary_navigation", 180, "服务", "primary_navigation", "/services", "active", "service_plaza.primary_services.open", null, "anonymous"),
  action("primary-discover", "primary_navigation", 190, "发现", "primary_navigation", "/discover", "planned", "service_plaza.primary_discover.open", null, "anonymous"),
  action("primary-profile", "primary_navigation", 200, "我的", "primary_navigation", "/me", "planned", "service_plaza.primary_profile.open"),
];

const validateActionCatalog = (catalog: ServiceActionCatalog) => {
  if (catalog.contract_version !== serviceActionContractVersion) {
    throw new Error(`不支持的动作接入协议：${catalog.contract_version}`);
  }
  if (catalog.count !== catalog.items.length) {
    throw new Error("动作目录数量与清单不一致");
  }
  if (new Set(catalog.items.map((item) => item.action_id)).size !== catalog.items.length) {
    throw new Error("动作目录包含重复 action_id");
  }
  const baselineMismatch = catalog.items.find(
    (item, index) =>
      item.action_id !== servicePlazaActionIds[index] ||
      item.sort_order !== (index + 1) * 10,
  );
  if (baselineMismatch) {
    throw new Error("动作目录顺序、action_id 或 sort_order 不符合 v1 基线");
  }
  catalog.items.forEach(validateActionDefinition);
  return catalog;
};

export const mockServiceCatalogRepository: ServiceCatalogRepository = {
  async getCatalog() {
    return { contract_version: servicePlazaContractVersion, items: mockItems };
  },
  async getActions() {
    return validateActionCatalog({
      contract_version: serviceActionContractVersion,
      count: mockActions.length,
      items: mockActions,
    });
  },
};

export const realServiceCatalogRepository: ServiceCatalogRepository = {
  async getCatalog() {
    const catalog = await apiRequest<ServiceCatalog>("/api/v1/service-plaza/catalog");
    if (catalog.contract_version !== servicePlazaContractVersion) {
      throw new Error(`不支持的服务接入协议：${catalog.contract_version}`);
    }
    return catalog;
  },
  async getActions() {
    const catalog = await apiRequest<ServiceActionCatalog>("/api/v1/service-plaza/actions");
    return validateActionCatalog(catalog);
  },
};

export const serviceCatalogRepository =
  import.meta.env.MODE === "test" ? mockServiceCatalogRepository : realServiceCatalogRepository;
