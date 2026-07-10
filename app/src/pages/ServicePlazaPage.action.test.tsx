import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { serviceActionContractVersion } from "../domain/serviceActions";
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
            target: `/contract-target/${action.action_id}`,
            lifecycle_status: "active" as const,
            action_type: "service_entry" as const,
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
});
