import { afterEach, describe, expect, it, vi } from "vitest";
import { tokenStorage } from "../../infrastructure/apiClient";
import { protectionMallCatalogApi } from "./protectionMallApi";

const validCatalog = {
  contract_version: "mall.catalog.v1",
  items: [],
};

function response(data: unknown) {
  return new Response(JSON.stringify({ success: true, data }), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
}

describe("protectionMallCatalogApi", () => {
  afterEach(() => {
    sessionStorage.clear();
    vi.restoreAllMocks();
  });

  it("通过共享适配器读取目录并携带会话和取消信号", async () => {
    tokenStorage.set("catalog-token");
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(response(validCatalog));
    const controller = new AbortController();

    await expect(protectionMallCatalogApi.loadCatalog(
      { sceneId: "family-care" },
      { signal: controller.signal, requestId: "mall-request-001" },
    )).resolves.toEqual({ contractVersion: "mall.catalog.v1", items: [] });

    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(fetchMock.mock.calls[0][0]).toBe("/api/v1/mall/catalog?scene_id=family-care");
    const options = fetchMock.mock.calls[0][1];
    expect((options?.headers as Headers).get("Authorization")).toBe("Bearer catalog-token");
    expect((options?.headers as Headers).get("X-Request-ID")).toBe("mall-request-001");
    expect(options?.signal).toBeInstanceOf(AbortSignal);
  });

  it("把进行中的调用方取消传播为稳定错误", async () => {
    tokenStorage.set("catalog-token");
    vi.spyOn(globalThis, "fetch").mockImplementation((_input, init) =>
      new Promise<Response>((_resolve, reject) => {
        init?.signal?.addEventListener("abort", () => reject(init.signal?.reason), { once: true });
      }),
    );
    const controller = new AbortController();

    const request = protectionMallCatalogApi.loadCatalog(
      { sceneId: "all" },
      { signal: controller.signal },
    );
    controller.abort();

    await expect(request).rejects.toMatchObject({ code: "REQUEST_ABORTED", status: 0 });
  });

  it("拒绝漂移响应，不用示例数据兜底", async () => {
    tokenStorage.set("catalog-token");
    vi.spyOn(globalThis, "fetch").mockResolvedValue(response({ contract_version: "mall.catalog.v2", items: [] }));

    await expect(protectionMallCatalogApi.loadCatalog({ sceneId: "all" })).rejects.toMatchObject({
      code: "MALL_CATALOG_INVALID_RESPONSE",
      status: 502,
    });
  });
});
