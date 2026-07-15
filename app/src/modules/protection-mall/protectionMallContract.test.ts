import { describe, expect, it } from "vitest";
import { decodeProtectionMallCatalog } from "./protectionMallContract";

function catalog(overrides: Record<string, unknown> = {}) {
  return {
    contract_version: "mall.catalog.v1",
    items: [{
      contract_version: "mall.catalog.v1",
      id: "item-1",
      kind: "product",
      title: "家庭照护包",
      scene_ids: ["family-care"],
      responsibility: {
        mall_type: "protection_mall",
        product_type: "physical",
        seller_id: "seller-1",
        fulfillment_owner_id: "warehouse-1",
        after_sale_owner_id: "support-1",
      },
      price_snapshot: {
        snapshot_id: "price-1",
        version: 1,
        currency: "CNY",
        amount_minor: 9900,
      },
      benefit_snapshot: {
        snapshot_id: "benefit-1",
        version: 1,
        grants: [{ code: "assurance", quantity: 1 }],
      },
      ...overrides,
    }],
  };
}

describe("decodeProtectionMallCatalog", () => {
  it("解码并映射 mall.catalog.v1 快照", () => {
    expect(decodeProtectionMallCatalog(catalog()).items[0]).toMatchObject({
      id: "item-1",
      kind: "product",
      price: { amountMinor: 9900, currency: "CNY" },
      benefits: { grants: [{ code: "assurance", quantity: 1 }] },
    });
  });

  it.each([
    ["根版本漂移", { contract_version: "mall.catalog.v2", items: [] }],
    ["商品责任类型错配", catalog({ responsibility: { ...catalog().items[0].responsibility, product_type: "service" } })],
    ["金额超出安全整数", catalog({ price_snapshot: { ...catalog().items[0].price_snapshot, amount_minor: Number.MAX_SAFE_INTEGER + 1 } })],
    ["俱乐部商城非法发放保障", catalog({ responsibility: { ...catalog().items[0].responsibility, mall_type: "club_mall" } })],
    ["出现未声明字段", { ...catalog(), debug: true }],
  ])("拒绝%s", (_label, payload) => {
    expect(() => decodeProtectionMallCatalog(payload)).toThrow(expect.objectContaining({
      code: "MALL_CATALOG_INVALID_RESPONSE",
      status: 502,
    }));
  });

  it("拒绝重复目录、场景和权益标识", () => {
    const duplicateId = catalog();
    duplicateId.items.push(structuredClone(duplicateId.items[0]));
    expect(() => decodeProtectionMallCatalog(duplicateId)).toThrow(/目录 ID 不得重复/);
    expect(() => decodeProtectionMallCatalog(catalog({ scene_ids: ["member", "member"] }))).toThrow(/不得重复/);
    expect(() => decodeProtectionMallCatalog(catalog({
      benefit_snapshot: {
        ...catalog().items[0].benefit_snapshot,
        grants: [{ code: "points", quantity: 1 }, { code: "points", quantity: 2 }],
      },
    }))).toThrow(/权益 points 重复/);
  });
});
