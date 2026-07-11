import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { serviceActionContractVersion, type ServiceAction } from "../domain/serviceActions";
import {
  mockServiceCatalogRepository,
  type ServiceCatalogRepository,
} from "../infrastructure/serviceCatalogRepository";
import { ServicePlazaPage } from "./ServicePlazaPage";

describe("服务广场动作清单渲染", () => {
  it("20 个位置均使用动作目录目标，不在页面固化跳转地址", async () => {
    const baseActions = await mockServiceCatalogRepository.getActions();
    const repository: ServiceCatalogRepository = {
      getCatalog: () => mockServiceCatalogRepository.getCatalog(),
      async getActions() {
        return {
          contract_version: serviceActionContractVersion,
          count: 20,
          items: baseActions.items.map((action) => ({
            ...action,
            target:
              action.region === "club_alliance" && action.action_id !== "club-manage"
                ? `/contract-target/${action.action_id}${new URL(action.target, "https://heaotang.invalid").search}`
                : `/contract-target/${action.action_id}`,
            lifecycle_status: "active" as const,
            action_type:
              action.region === "club_alliance"
                ? action.action_type
                : ("service_entry" as const),
          })),
        };
      },
    };

    const { container } = render(
      <MemoryRouter initialEntries={["/services"]}>
        <ServicePlazaPage repository={repository} />
      </MemoryRouter>,
    );

    await screen.findByRole("link", { name: "生命导航" });
    const controls = Array.from(
      container.querySelectorAll<HTMLElement>("[data-action-id]"),
    );
    expect(controls).toHaveLength(20);
    expect(new Set(controls.map((control) => control.dataset.actionId)).size).toBe(20);

    await waitFor(() => {
      const links = screen.getAllByRole("link");
      expect(links).toHaveLength(20);
      links.forEach((link) => {
        expect(link.getAttribute("href")).toMatch(/^\/contract-target\//);
      });
    });
  });

  it("与俱乐部首页共用适配器并按上游 sort_order 排列四入口", async () => {
    const baseActions = await mockServiceCatalogRepository.getActions();
    const repository: ServiceCatalogRepository = {
      getCatalog: () => mockServiceCatalogRepository.getCatalog(),
      async getActions() {
        return {
          contract_version: serviceActionContractVersion,
          count: baseActions.count,
          items: [...baseActions.items].reverse(),
        };
      },
    };

    render(
      <MemoryRouter initialEntries={["/services"]}>
        <ServicePlazaPage repository={repository} />
      </MemoryRouter>,
    );

    await screen.findByRole("link", { name: "公益俱乐部" });
    const categoryIds = Array.from(
      document.querySelectorAll<HTMLElement>(".club-grid [data-action-id]"),
    ).map((element) => element.dataset.actionId);
    expect(categoryIds).toEqual([
      "public-benefit-club",
      "self-created-club",
      "family-club",
      "club-federation",
    ]);
    expect(categoryIds).not.toContain("club-manage");
  });

  it.each([
    ["missing", "/services/club-alliance"],
    ["blank", "/services/club-alliance?category=%20"],
    ["repeated", "/services/club-alliance?category=公益俱乐部&category=公益俱乐部"],
    ["multiple", "/services/club-alliance?category=公益俱乐部&category=自建俱乐部"],
    ["malformed", "http://["],
  ])("fails the plaza closed for a %s club category target", async (_kind, target) => {
    const baseActions = await mockServiceCatalogRepository.getActions();
    const repository: ServiceCatalogRepository = {
      getCatalog: () => mockServiceCatalogRepository.getCatalog(),
      async getActions() {
        return {
          ...baseActions,
          items: baseActions.items.map((action) =>
            action.action_id === "public-benefit-club" ? { ...action, target } : action,
          ),
        };
      },
    };

    render(
      <MemoryRouter initialEntries={["/services"]}>
        <ServicePlazaPage repository={repository} />
      </MemoryRouter>,
    );

    expect(await screen.findByText(/CAH1_ACTION_TARGET_INVALID/)).toBeInTheDocument();
    expect(screen.queryByRole("link", { name: "公益俱乐部" })).not.toBeInTheDocument();
  });

  it("fails the plaza closed when different club actions map to one category", async () => {
    const baseActions = await mockServiceCatalogRepository.getActions();
    const publicBenefit = baseActions.items.find(
      (action) => action.action_id === "public-benefit-club",
    ) as ServiceAction;
    const repository: ServiceCatalogRepository = {
      getCatalog: () => mockServiceCatalogRepository.getCatalog(),
      async getActions() {
        return {
          ...baseActions,
          items: baseActions.items.map((action) =>
            action.action_id === "self-created-club"
              ? { ...action, target: publicBenefit.target }
              : action,
          ),
        };
      },
    };

    render(
      <MemoryRouter initialEntries={["/services"]}>
        <ServicePlazaPage repository={repository} />
      </MemoryRouter>,
    );

    expect(await screen.findByText(/CAH1_ACTION_TARGET_INVALID/)).toBeInTheDocument();
  });
});
