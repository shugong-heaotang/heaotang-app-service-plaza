import { ApiError } from "../../infrastructure/apiClient";

export const protectionMallCatalogVersion = "mall.catalog.v1";

export type ProtectionMallCatalogKind = "product" | "service" | "course" | "activity";

export type ProtectionMallResponsibility = {
  mallType: "protection_mall" | "club_mall";
  productType: "physical" | "service";
  sellerId: string;
  fulfillmentOwnerId: string;
  afterSaleOwnerId: string;
};

export type ProtectionMallPriceSnapshot = {
  snapshotId: string;
  version: number;
  currency: string;
  amountMinor: number;
};

export type ProtectionMallBenefitGrant = {
  code: string;
  quantity: number;
};

export type ProtectionMallBenefitSnapshot = {
  snapshotId: string;
  version: number;
  grants: ProtectionMallBenefitGrant[];
};

export type ProtectionMallCatalogEntry = {
  contractVersion: typeof protectionMallCatalogVersion;
  id: string;
  kind: ProtectionMallCatalogKind;
  title: string;
  sceneIds: string[];
  responsibility: ProtectionMallResponsibility;
  price: ProtectionMallPriceSnapshot;
  benefits: ProtectionMallBenefitSnapshot;
};

export type ProtectionMallCatalog = {
  contractVersion: typeof protectionMallCatalogVersion;
  items: ProtectionMallCatalogEntry[];
};

type JsonObject = Record<string, unknown>;

const catalogKinds = new Set<ProtectionMallCatalogKind>([
  "product",
  "service",
  "course",
  "activity",
]);

function invalidCatalogResponse(detail: string): never {
  throw new ApiError(
    `商城目录响应不符合 ${protectionMallCatalogVersion}：${detail}`,
    502,
    "MALL_CATALOG_INVALID_RESPONSE",
  );
}

function objectAt(value: unknown, path: string): JsonObject {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    invalidCatalogResponse(`${path} 必须是对象`);
  }
  return value as JsonObject;
}

function exactObjectAt(value: unknown, path: string, keys: readonly string[]): JsonObject {
  const source = objectAt(value, path);
  const allowed = new Set(keys);
  const unexpected = Object.keys(source).find((key) => !allowed.has(key));
  if (unexpected) invalidCatalogResponse(`${path}.${unexpected} 是未声明字段`);
  return source;
}

function stringAt(value: unknown, path: string): string {
  if (typeof value !== "string" || value.trim() === "") {
    invalidCatalogResponse(`${path} 必须是非空字符串`);
  }
  return value;
}

function positiveIntegerAt(value: unknown, path: string): number {
  if (!Number.isSafeInteger(value) || (value as number) <= 0) {
    invalidCatalogResponse(`${path} 必须是正安全整数`);
  }
  return value as number;
}

function decodeResponsibility(value: unknown, kind: ProtectionMallCatalogKind): ProtectionMallResponsibility {
  const source = exactObjectAt(value, "responsibility", [
    "mall_type",
    "product_type",
    "seller_id",
    "fulfillment_owner_id",
    "after_sale_owner_id",
  ]);
  const mallType = stringAt(source.mall_type, "responsibility.mall_type");
  if (mallType !== "protection_mall" && mallType !== "club_mall") {
    invalidCatalogResponse("responsibility.mall_type 非法");
  }
  const productType = stringAt(source.product_type, "responsibility.product_type");
  const expectedProductType = kind === "product" ? "physical" : "service";
  if (productType !== expectedProductType) {
    invalidCatalogResponse(`${kind} 必须映射为 ${expectedProductType}`);
  }
  return {
    mallType,
    productType,
    sellerId: stringAt(source.seller_id, "responsibility.seller_id"),
    fulfillmentOwnerId: stringAt(
      source.fulfillment_owner_id,
      "responsibility.fulfillment_owner_id",
    ),
    afterSaleOwnerId: stringAt(
      source.after_sale_owner_id,
      "responsibility.after_sale_owner_id",
    ),
  };
}

function decodePrice(value: unknown): ProtectionMallPriceSnapshot {
  const source = exactObjectAt(value, "price_snapshot", [
    "snapshot_id",
    "version",
    "currency",
    "amount_minor",
  ]);
  const amountMinor = source.amount_minor;
  if (!Number.isSafeInteger(amountMinor) || (amountMinor as number) < 0) {
    invalidCatalogResponse("price_snapshot.amount_minor 必须是非负安全整数");
  }
  const currency = stringAt(source.currency, "price_snapshot.currency");
  if (!/^[A-Z]{3}$/.test(currency)) {
    invalidCatalogResponse("price_snapshot.currency 必须是三位大写币种");
  }
  return {
    snapshotId: stringAt(source.snapshot_id, "price_snapshot.snapshot_id"),
    version: positiveIntegerAt(source.version, "price_snapshot.version"),
    currency,
    amountMinor: amountMinor as number,
  };
}

function decodeBenefits(
  value: unknown,
  mallType: ProtectionMallResponsibility["mallType"],
): ProtectionMallBenefitSnapshot {
  const source = exactObjectAt(value, "benefit_snapshot", ["snapshot_id", "version", "grants"]);
  if (!Array.isArray(source.grants)) {
    invalidCatalogResponse("benefit_snapshot.grants 必须是数组");
  }
  const seen = new Set<string>();
  const grants = source.grants.map((value, index) => {
    const grant = exactObjectAt(value, `benefit_snapshot.grants[${index}]`, ["code", "quantity"]);
    const code = stringAt(grant.code, `benefit_snapshot.grants[${index}].code`);
    if (seen.has(code)) invalidCatalogResponse(`权益 ${code} 重复`);
    seen.add(code);
    return {
      code,
      quantity: positiveIntegerAt(
        grant.quantity,
        `benefit_snapshot.grants[${index}].quantity`,
      ),
    };
  });
  if (mallType === "club_mall" && grants.some(({ code }) => code.toLowerCase() === "assurance")) {
    invalidCatalogResponse("club_mall 不得包含 assurance 权益");
  }
  return {
    snapshotId: stringAt(source.snapshot_id, "benefit_snapshot.snapshot_id"),
    version: positiveIntegerAt(source.version, "benefit_snapshot.version"),
    grants,
  };
}

function decodeEntry(value: unknown, index: number): ProtectionMallCatalogEntry {
  const source = exactObjectAt(value, `items[${index}]`, [
    "contract_version",
    "id",
    "kind",
    "title",
    "scene_ids",
    "responsibility",
    "price_snapshot",
    "benefit_snapshot",
  ]);
  if (source.contract_version !== protectionMallCatalogVersion) {
    invalidCatalogResponse(`items[${index}].contract_version 不匹配`);
  }
  const kind = source.kind;
  if (typeof kind !== "string" || !catalogKinds.has(kind as ProtectionMallCatalogKind)) {
    invalidCatalogResponse(`items[${index}].kind 非法`);
  }
  if (!Array.isArray(source.scene_ids) || source.scene_ids.length === 0) {
    invalidCatalogResponse(`items[${index}].scene_ids 必须是非空数组`);
  }
  const sceneIds = source.scene_ids.map((scene, sceneIndex) =>
    stringAt(scene, `items[${index}].scene_ids[${sceneIndex}]`),
  );
  if (new Set(sceneIds).size !== sceneIds.length) {
    invalidCatalogResponse(`items[${index}].scene_ids 不得重复`);
  }
  const responsibility = decodeResponsibility(
    source.responsibility,
    kind as ProtectionMallCatalogKind,
  );
  return {
    contractVersion: protectionMallCatalogVersion,
    id: stringAt(source.id, `items[${index}].id`),
    kind: kind as ProtectionMallCatalogKind,
    title: stringAt(source.title, `items[${index}].title`),
    sceneIds,
    responsibility,
    price: decodePrice(source.price_snapshot),
    benefits: decodeBenefits(source.benefit_snapshot, responsibility.mallType),
  };
}

export function decodeProtectionMallCatalog(value: unknown): ProtectionMallCatalog {
  const source = exactObjectAt(value, "catalog", ["contract_version", "items"]);
  if (source.contract_version !== protectionMallCatalogVersion) {
    invalidCatalogResponse("contract_version 不匹配");
  }
  if (!Array.isArray(source.items)) invalidCatalogResponse("items 必须是数组");
  const items = source.items.map(decodeEntry);
  if (new Set(items.map(({ id }) => id)).size !== items.length) {
    invalidCatalogResponse("目录 ID 不得重复");
  }
  return { contractVersion: protectionMallCatalogVersion, items };
}
