import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import {
  servicePlazaContractVersion,
  type ServiceManifest,
} from "../../domain/serviceCatalog";
import { LifeNavigationModule } from "./LifeNavigationModule";
import { mapLifeNavigationManifest } from "./lifeNavigationContract";

const createManifest = (
  overrides: Partial<ServiceManifest> = {},
): ServiceManifest => ({
  contract_version: servicePlazaContractVersion,
  service_id: "life-navigation",
  display_name: "生命导航",
  summary: "帮助会员发现生命导航服务",
  category: "core",
  sort_order: 10,
  lifecycle_status: "active",
  entry: {
    type: "internal_route",
    target: "/services/life-navigation",
    return_target: "/services",
  },
  access: { auth_mode: "shared_session", required_scopes: ["life:read"] },
  provider: { provider_id: "heaotang", display_name: "和奥堂" },
  capabilities: ["navigate"],
  privacy_level: "account",
  business_api_version: "v1",
  ...overrides,
});

describe("生命导航标准接入模块", () => {
  it("将平台清单缩窄为不含具体业务字段的模块契约", () => {
    const contract = mapLifeNavigationManifest(createManifest());

    expect(contract).toEqual({
      contractVersion: "service-plaza.v1",
      serviceId: "life-navigation",
      displayName: "生命导航",
      summary: "帮助会员发现生命导航服务",
      lifecycleStatus: "active",
      returnTarget: "/services",
      providerId: "heaotang",
      requiredScopes: ["life:read"],
    });
  });

  it("拒绝将其他板块或非标准路由误装载为生命导航", () => {
    expect(() =>
      mapLifeNavigationManifest(createManifest({ service_id: "club-alliance" })),
    ).toThrow("错误的服务标识");

    expect(() =>
      mapLifeNavigationManifest(
        createManifest({
          entry: {
            type: "internal_route",
            target: "/legacy/life",
            return_target: "/services",
          },
        }),
      ),
    ).toThrow("标准内部路由");
  });

  it("通过可替换适配器渲染内容并把标准返回路径交还宿主", () => {
    const onReturn = vi.fn();
    const renderFeature = vi.fn(({ contract }) => (
      <p>独立功能入口：{contract.serviceId}</p>
    ));

    render(
      <LifeNavigationModule
        manifest={createManifest()}
        adapter={{ render: renderFeature }}
        onReturn={onReturn}
      />,
    );

    expect(screen.getByRole("heading", { name: "生命导航" })).toBeInTheDocument();
    expect(screen.getByText("独立功能入口：life-navigation")).toBeInTheDocument();
    expect(renderFeature).toHaveBeenCalledWith(
      expect.objectContaining({
        contract: expect.objectContaining({ contractVersion: "service-plaza.v1" }),
      }),
    );

    fireEvent.click(screen.getByRole("button", { name: "返回服务广场" }));
    expect(onReturn).toHaveBeenCalledWith("/services");
  });
});
