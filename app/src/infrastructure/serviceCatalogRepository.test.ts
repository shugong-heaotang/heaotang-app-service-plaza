import { afterEach, describe, expect, it, vi } from "vitest";
import { servicePlazaContractVersion } from "../domain/serviceCatalog";
import { serviceActionContractVersion } from "../domain/serviceActions";
import actionBaseline from "../../../contracts/service-plaza/service-plaza-actions.v1.json";
import {
  mockActions,
  mockServiceCatalogRepository,
  realServiceCatalogRepository,
} from "./serviceCatalogRepository";

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("标准服务目录适配器", () => {
  it("从统一目录接口读取版本化清单", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(
        JSON.stringify({
          success: true,
          data: { contract_version: servicePlazaContractVersion, items: [] },
        }),
        { status: 200, headers: { "Content-Type": "application/json" } },
      ),
    );
    vi.stubGlobal("fetch", fetchMock);

    const catalog = await realServiceCatalogRepository.getCatalog();

    expect(fetchMock).toHaveBeenCalledWith(
      "/api/v1/service-plaza/catalog",
      expect.objectContaining({ headers: expect.any(Headers) }),
    );
    expect(catalog.contract_version).toBe(servicePlazaContractVersion);
  });

  it("拒绝未支持的接入协议版本", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({ success: true, data: { contract_version: "service-plaza.v2", items: [] } }),
          { status: 200, headers: { "Content-Type": "application/json" } },
        ),
      ),
    );

    await expect(realServiceCatalogRepository.getCatalog()).rejects.toThrow("不支持的服务接入协议");
  });

  it("测试目录提供恰好 20 个唯一标准动作", async () => {
    const catalog = await mockServiceCatalogRepository.getActions();

    expect(catalog.contract_version).toBe(serviceActionContractVersion);
    expect(catalog.count).toBe(20);
    expect(new Set(catalog.items.map((action) => action.action_id)).size).toBe(20);
  });

  it("mock 动作逐字段对齐机器可读基线", () => {
    expect(mockActions).toEqual(actionBaseline.actions);
  });

  it("从统一动作接口读取并校验版本化动作清单", async () => {
    const mockCatalog = await mockServiceCatalogRepository.getActions();
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(
        JSON.stringify({ success: true, data: mockCatalog }),
        { status: 200, headers: { "Content-Type": "application/json" } },
      ),
    );
    vi.stubGlobal("fetch", fetchMock);

    const catalog = await realServiceCatalogRepository.getActions();

    expect(fetchMock).toHaveBeenCalledWith(
      "/api/v1/service-plaza/actions",
      expect.objectContaining({ headers: expect.any(Headers) }),
    );
    expect(catalog.count).toBe(20);
  });

  it("拒绝数量不一致的动作清单", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            success: true,
            data: {
              contract_version: serviceActionContractVersion,
              count: 1,
              items: [],
            },
          }),
          { status: 200, headers: { "Content-Type": "application/json" } },
        ),
      ),
    );

    await expect(realServiceCatalogRepository.getActions()).rejects.toThrow("数量与清单不一致");
  });
});
