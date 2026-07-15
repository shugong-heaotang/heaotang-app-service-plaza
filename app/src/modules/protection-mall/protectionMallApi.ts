import {
  createBusinessApiAdapter,
  defineBusinessRead,
  type BusinessApiExecutionOptions,
} from "../../infrastructure/businessApiAdapter";
import {
  decodeProtectionMallCatalog,
  type ProtectionMallCatalog,
} from "./protectionMallContract";

export type ProtectionMallSceneId =
  | "all"
  | "family-care"
  | "health-care"
  | "quality-life"
  | "member";

export type ProtectionMallCatalogQuery = {
  sceneId: ProtectionMallSceneId;
};

export type ProtectionMallCatalogApi = {
  loadCatalog(
    query: ProtectionMallCatalogQuery,
    options?: BusinessApiExecutionOptions,
  ): Promise<ProtectionMallCatalog>;
};

const adapter = createBusinessApiAdapter("protection-mall");

const readCatalog = defineBusinessRead<ProtectionMallCatalogQuery, unknown>({
  operationId: "read-catalog",
  path: ({ sceneId }) =>
    sceneId === "all"
      ? "/api/v1/mall/catalog"
      : `/api/v1/mall/catalog?scene_id=${encodeURIComponent(sceneId)}`,
});

export const protectionMallCatalogApi: ProtectionMallCatalogApi = {
  async loadCatalog(query, options = {}) {
    return decodeProtectionMallCatalog(await adapter.execute(readCatalog, query, options));
  },
};
