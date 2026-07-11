import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { createMemoryRouter, MemoryRouter, RouterProvider } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";
import { ActionRuntimeProvider } from "../../auth/ActionRuntimeContext";
import { AuthProvider } from "../../auth/AuthContext";
import { serviceActionContractVersion, type ServiceAction } from "../../domain/serviceActions";
import { servicePlazaContractVersion, type ServiceCatalog } from "../../domain/serviceCatalog";
import {
  mockActions,
  mockServiceCatalogRepository,
  realServiceCatalogRepository,
  type ServiceCatalogRepository,
} from "../../infrastructure/serviceCatalogRepository";
import { reportActionEvent } from "../../infrastructure/actionTelemetry";
import { ClubAllianceRoute } from "./ClubAllianceRoute";
import clubAllianceCss from "./ClubAlliancePage.css?inline";

vi.mock("../../infrastructure/actionTelemetry", () => ({
  primeFeatureFlags: vi.fn(async () => undefined),
  reportActionEvent: vi.fn(async () => undefined),
}));

const cloneActions = () => mockActions.map((action) => structuredClone(action));

const repositoryWith = (
  actions: readonly ServiceAction[],
  catalog?: ServiceCatalog,
): ServiceCatalogRepository => ({
  getCatalog: () => catalog ? Promise.resolve(catalog) : mockServiceCatalogRepository.getCatalog(),
  async getActions() {
    return {
      contract_version: serviceActionContractVersion,
      count: actions.length,
      items: [...actions],
    };
  },
});

const renderRoute = (
  route = "/services/club-alliance",
  repository: ServiceCatalogRepository = mockServiceCatalogRepository,
) =>
  render(
    <MemoryRouter initialEntries={[route]}>
      <ClubAllianceRoute repository={repository} />
    </MemoryRouter>,
  );

const renderAuthenticatedRoute = (
  route: string,
  scopes: readonly string[],
  repository: ServiceCatalogRepository = mockServiceCatalogRepository,
) => {
  sessionStorage.setItem("heaotang_access_token", "synthetic-test-token");
  sessionStorage.setItem(
    "heaotang_user",
    JSON.stringify({ id: 1001, nickname: "合成测试用户", scopes }),
  );
  return render(
    <MemoryRouter initialEntries={[route]}>
      <AuthProvider>
        <ActionRuntimeProvider>
          <ClubAllianceRoute repository={repository} />
        </ActionRuntimeProvider>
      </AuthProvider>
    </MemoryRouter>,
  );
};

const actionWith = (
  actionId: string,
  patch: Partial<ServiceAction>,
) => cloneActions().map((action) =>
  action.action_id === actionId ? { ...action, ...patch } : action,
);

const jsonResponse = (data: unknown) =>
  new Response(JSON.stringify({ success: true, data }), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });

const requestUrl = (input: RequestInfo | URL) => {
  if (typeof input === "string") return input;
  return input instanceof URL ? input.toString() : input.url;
};

describe("ClubAllianceRoute exact eight-state shell", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    sessionStorage.clear();
  });

  it("renders a real loading state while both versioned catalogs are pending", () => {
    const repository: ServiceCatalogRepository = {
      getCatalog: () => new Promise(() => undefined),
      getActions: () => new Promise(() => undefined),
    };
    renderRoute("/services/club-alliance", repository);
    expect(screen.getByText("正在读取服务目录与动作目录…")).toBeInTheDocument();
    expect(document.querySelector('[data-page-state="loading"]')).toBeInTheDocument();
    expect(screen.getByRole("status")).toHaveAttribute("data-page-state", "loading");
  });

  it("renders empty when the authoritative service manifest is absent", async () => {
    const catalog = await mockServiceCatalogRepository.getCatalog();
    renderRoute(
      "/services/club-alliance",
      repositoryWith(cloneActions(), {
        ...catalog,
        items: catalog.items.filter((item) => item.service_id !== "club-alliance"),
      }),
    );
    expect(await screen.findByText("暂时没有可用入口")).toBeInTheDocument();
    expect(document.querySelector('[data-page-state="empty"]')).toBeInTheDocument();
  });

  it("renders load error and retries the real repository operation", async () => {
    const user = userEvent.setup();
    let attempts = 0;
    const repository: ServiceCatalogRepository = {
      getCatalog: () => mockServiceCatalogRepository.getCatalog(),
      async getActions() {
        attempts += 1;
        if (attempts === 1) throw new Error("catalog unavailable");
        return mockServiceCatalogRepository.getActions();
      },
    };
    renderRoute("/services/club-alliance", repository);
    expect(await screen.findByText("catalog unavailable")).toBeInTheDocument();
    expect(screen.getByRole("alert")).toHaveAttribute("data-page-state", "error");
    await user.click(screen.getByRole("button", { name: "重新加载" }));
    expect(await screen.findByRole("heading", { name: "选择俱乐部服务" })).toBeInTheDocument();
    expect(attempts).toBe(2);
  });

  it("renders home from the shared adapter with four entries and one adjunct", async () => {
    renderRoute();
    expect(await screen.findByRole("heading", { name: "选择俱乐部服务" })).toBeInTheDocument();
    expect(document.querySelector('[data-page-state="home"]')).toBeInTheDocument();
    const categoryRegion = screen.getByRole("region", { name: "俱乐部联盟四类入口" });
    expect(categoryRegion.querySelectorAll("[data-action-id]")).toHaveLength(4);
    expect(categoryRegion.querySelector('[data-action-id="club-manage"]')).not.toBeInTheDocument();
    expect(screen.getByLabelText("俱乐部联盟管理附属入口")).toHaveTextContent("管理中心");
    expect(screen.getByRole("link", { name: "公益俱乐部" })).toHaveAttribute(
      "data-access-state",
      "authentication_required",
    );
    expect(
      Array.from(categoryRegion.querySelectorAll<HTMLAnchorElement>("a")).map((link) => link.href),
    ).toEqual([
      expect.stringContaining("/services/club-alliance?category=%E5%85%AC%E7%9B%8A%E4%BF%B1%E4%B9%90%E9%83%A8"),
      expect.stringContaining("/services/club-alliance?category=%E8%87%AA%E5%BB%BA%E4%BF%B1%E4%B9%90%E9%83%A8"),
      expect.stringContaining("/services/club-alliance?category=%E5%AE%B6%E5%BA%AD%E4%BF%B1%E4%B9%90%E9%83%A8"),
      expect.stringContaining("/services/club-alliance?category=%E4%BF%B1%E4%B9%90%E9%83%A8%E5%8F%8B%E8%81%94%E4%BD%93"),
    ]);
    expect(screen.getByRole("link", { name: "管理中心" })).toHaveAttribute(
      "data-access-state",
      "authentication_required",
    );
    expect(screen.getByRole("link", { name: "管理中心" })).toHaveAttribute(
      "data-telemetry-event",
      "service_plaza.club_manage.open",
    );
  });

  it("keeps the home shell keyboard reachable and exposes state semantics", async () => {
    const user = userEvent.setup();
    renderRoute();

    const back = await screen.findByRole("link", { name: "返回服务广场" });
    const publicBenefit = screen.getByRole("link", { name: "公益俱乐部" });
    await user.tab();
    expect(back).toHaveFocus();
    await user.tab();
    expect(publicBenefit).toHaveFocus();
    await user.keyboard("{Enter}");

    expect(await screen.findByText("需要登录或相应权限")).toBeInTheDocument();
    expect(document.querySelector('[data-page-state="unauthorized"]')).toBeInTheDocument();
  });

  it.each(["planned", "maintenance", "offline"] as const)(
    "does not elevate a %s category into an enabled home action",
    async (lifecycle) => {
      renderRoute(
        "/services/club-alliance",
        repositoryWith(actionWith("family-club", { lifecycle_status: lifecycle })),
      );

      expect(await screen.findByRole("button", { name: "家庭俱乐部" })).toBeDisabled();
      expect(screen.getByText(lifecycle)).toBeInTheDocument();
    },
  );

  it("reuses ActionControl lifecycle and telemetry behavior", async () => {
    const user = userEvent.setup();
    renderRoute(
      "/services/club-alliance",
      repositoryWith(actionWith("family-club", { lifecycle_status: "maintenance" })),
    );
    const maintenanceEntry = await screen.findByRole("button", { name: "家庭俱乐部" });
    expect(maintenanceEntry).toBeDisabled();

    await user.click(screen.getByRole("link", { name: "公益俱乐部" }));
    await waitFor(() => {
      expect(reportActionEvent).toHaveBeenCalledWith(
        expect.objectContaining({ action_id: "public-benefit-club" }),
        "blocked",
        "authentication_required",
      );
    });
  });

  it("reuses ActionControl activated telemetry for an allowed category", async () => {
    const user = userEvent.setup();
    renderRoute(
      "/services/club-alliance",
      repositoryWith(
        actionWith("public-benefit-club", {
          access: { auth_mode: "anonymous", required_scopes: [] },
        }),
      ),
    );

    await user.click(await screen.findByRole("link", { name: "公益俱乐部" }));
    await waitFor(() => {
      expect(reportActionEvent).toHaveBeenCalledWith(
        expect.objectContaining({ action_id: "public-benefit-club" }),
        "activated",
        "none",
      );
    });
  });

  it("renders focused for an allowed category and exposes exact selected_action_id", async () => {
    const actions = actionWith("public-benefit-club", {
      access: { auth_mode: "anonymous", required_scopes: [] },
    });
    renderRoute(
      "/services/club-alliance?category=公益俱乐部",
      repositoryWith(actions),
    );
    expect(await screen.findByText("selected_action_id=public-benefit-club")).toBeInTheDocument();
    expect(document.querySelector('[data-page-state="focused"]')).toBeInTheDocument();
  });

  it("renders unauthorized from the shared evaluator without starting business APIs", async () => {
    renderRoute("/services/club-alliance?category=公益俱乐部");
    expect(await screen.findByText("需要登录或相应权限")).toBeInTheDocument();
    expect(screen.getByText("authentication_required")).toBeInTheDocument();
    expect(document.querySelector('[data-page-state="unauthorized"]')).toBeInTheDocument();
  });

  it("renders exact scope-required details from the shared evaluator", async () => {
    const actions = actionWith("public-benefit-club", {
      access: { auth_mode: "anonymous", required_scopes: ["club:special"] },
    });
    renderRoute(
      "/services/club-alliance?category=公益俱乐部",
      repositoryWith(actions),
    );
    expect(await screen.findByText("scope_required")).toBeInTheDocument();
    expect(screen.getByText("缺少权限：club:special")).toBeInTheDocument();
  });

  it("fails the direct management view closed for a guest", async () => {
    renderRoute("/services/club-alliance?view=manage");

    expect(await screen.findByText("authentication_required")).toBeInTheDocument();
    expect(screen.getByText("管理中心当前不可访问。")).toBeInTheDocument();
    expect(document.querySelector('[data-page-state="unauthorized"]')).toBeInTheDocument();
  });

  it("fails the direct management view closed when club:manage is missing", async () => {
    renderAuthenticatedRoute("/services/club-alliance?view=manage", []);

    expect(await screen.findByText("scope_required")).toBeInTheDocument();
    expect(screen.getByText("缺少权限：club:manage")).toBeInTheDocument();
    expect(document.querySelector('[data-page-state="unauthorized"]')).toBeInTheDocument();
  });

  it("renders the management adjunct focused only with club:manage", async () => {
    renderAuthenticatedRoute("/services/club-alliance?view=manage", ["club:manage"]);

    expect(await screen.findByText("selected_action_id=club-manage")).toBeInTheDocument();
    expect(document.querySelector('[data-page-state="focused"]')).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "俱乐部联盟四类入口" })).toBeInTheDocument();
  });

  it("reports a blocked management click without changing the home URL state", async () => {
    const user = userEvent.setup();
    renderAuthenticatedRoute("/services/club-alliance", []);
    await user.click(await screen.findByRole("link", { name: "管理中心" }));

    expect(screen.getByRole("heading", { name: "选择俱乐部服务" })).toBeInTheDocument();
    expect(document.querySelector('[data-page-state="home"]')).toBeInTheDocument();
    await waitFor(() => {
      expect(reportActionEvent).toHaveBeenCalledWith(
        expect.objectContaining({ action_id: "club-manage" }),
        "blocked",
        "scope_required",
      );
    });
  });

  it.each([
    ["maintenance", "入口维护中"],
    ["offline", "入口已下线"],
  ] as const)("renders %s from upstream lifecycle", async (lifecycle, title) => {
    renderRoute(
      "/services/club-alliance?category=公益俱乐部",
      repositoryWith(actionWith("public-benefit-club", { lifecycle_status: lifecycle })),
    );
    expect(await screen.findByText(title)).toBeInTheDocument();
    expect(document.querySelector(`[data-page-state="${lifecycle}"]`)).toBeInTheDocument();
  });

  it("fails invalid query closed with a stable language-neutral error id", async () => {
    renderRoute("/services/club-alliance?category=%20");
    expect(await screen.findByText("CAH0_QUERY_BLANK")).toBeInTheDocument();
    expect(document.querySelector('[data-page-state="error"]')).toBeInTheDocument();
  });

  it.each([
    ["missing", "/services/club-alliance"],
    ["blank", "/services/club-alliance?category=%20"],
    ["repeated", "/services/club-alliance?category=公益俱乐部&category=公益俱乐部"],
    ["multiple", "/services/club-alliance?category=公益俱乐部&category=自建俱乐部"],
    ["malformed", "http://["],
  ])("fails the no-query home state closed for a %s category target", async (_kind, target) => {
    renderRoute(
      "/services/club-alliance",
      repositoryWith(actionWith("public-benefit-club", { target })),
    );

    expect(await screen.findByText("CAH1_ACTION_TARGET_INVALID")).toBeInTheDocument();
    expect(document.querySelector('[data-page-state="error"]')).toBeInTheDocument();
    expect(document.querySelector('[data-page-state="home"]')).not.toBeInTheDocument();
  });

  it("fails the no-query home state closed when two actions map to one category", async () => {
    const actions = cloneActions();
    const publicBenefit = actions.find(
      (action) => action.action_id === "public-benefit-club",
    ) as ServiceAction;
    renderRoute(
      "/services/club-alliance",
      repositoryWith(
        actions.map((action) =>
          action.action_id === "self-created-club"
            ? { ...action, target: publicBenefit.target }
            : action,
        ),
      ),
    );

    expect(await screen.findByText("CAH1_ACTION_TARGET_INVALID")).toBeInTheDocument();
    expect(document.querySelector('[data-page-state="error"]')).toBeInTheDocument();
  });

  it("replays direct query and supports browser back plus the fixed return route", async () => {
    const user = userEvent.setup();
    const router = createMemoryRouter(
      [
        { path: "/services", element: <p>service-plaza-return-target</p> },
        {
          path: "/services/club-alliance",
          element: <ClubAllianceRoute repository={mockServiceCatalogRepository} />,
        },
      ],
      {
        initialEntries: [
          "/services",
          "/services/club-alliance?category=公益俱乐部",
        ],
        initialIndex: 1,
      },
    );
    render(<RouterProvider router={router} />);

    expect(await screen.findByText("需要登录或相应权限")).toBeInTheDocument();
    expect(document.querySelector('[data-page-state="unauthorized"]')).toBeInTheDocument();
    await router.navigate(-1);
    expect(await screen.findByText("service-plaza-return-target")).toBeInTheDocument();

    await router.navigate("/services/club-alliance");
    await screen.findByRole("heading", { name: "选择俱乐部服务" });
    await user.click(screen.getByRole("link", { name: "← 返回服务广场" }));
    expect(await screen.findByText("service-plaza-return-target")).toBeInTheDocument();
  });

  it("replays the same direct query after a route remount", async () => {
    const route = "/services/club-alliance?category=公益俱乐部";
    const repository = repositoryWith(
      actionWith("public-benefit-club", {
        access: { auth_mode: "anonymous", required_scopes: [] },
      }),
    );
    const first = renderRoute(route, repository);
    expect(await screen.findByText("selected_action_id=public-benefit-club")).toBeInTheDocument();
    first.unmount();

    renderRoute(route, repository);
    expect(await screen.findByText("selected_action_id=public-benefit-club")).toBeInTheDocument();
  });

  it("自建 focused 只增加 action_id 驱动的子项目 CTA，不在 H1 发业务请求", async () => {
    const actions = actionWith("self-created-club", {
      access: { auth_mode: "anonymous", required_scopes: [] },
    });
    renderRoute(
      "/services/club-alliance?category=自建俱乐部",
      repositoryWith(actions),
    );

    expect(await screen.findByText("selected_action_id=self-created-club")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "进入自建俱乐部" })).toHaveAttribute(
      "href",
      "/services/club-alliance/self-created",
    );
  });
});

describe("ClubAlliancePage local responsive contract", () => {
  it("covers 320, 360, 768 and desktop layouts without fixed content width", () => {
    expect(clubAllianceCss).toContain("min-width: 0");
    expect(clubAllianceCss).toContain("@media (max-width: 359px)");
    expect(clubAllianceCss).toContain("@media (min-width: 560px)");
    expect(clubAllianceCss).toContain("@media (min-width: 900px)");
    expect(clubAllianceCss).toContain("grid-template-columns: repeat(2, minmax(0, 1fr))");
    expect(clubAllianceCss).toContain("grid-template-columns: minmax(0, 2fr) minmax(240px, 1fr)");
    expect(clubAllianceCss).toContain("width: min(calc(100vw - 48px), 760px)");
    expect(clubAllianceCss).toContain("width: min(calc(100vw - 64px), 960px)");
    expect(clubAllianceCss).toContain(":focus-visible");
    expect(clubAllianceCss).toContain(".back-button:focus-visible");
    expect(clubAllianceCss).toContain(".club-alliance-management a:focus-visible");
    expect(clubAllianceCss).toContain(".club-alliance-state button:focus-visible");
    expect(clubAllianceCss).toContain(".club-alliance-return:focus-visible");
    expect(clubAllianceCss).not.toMatch(/\.phone\s*\{[^}]*\n\s*width:\s*\d+px/s);
  });
});

describe("ClubAllianceRoute network boundary", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("allows only catalog/actions reads and denies all club business endpoints", async () => {
    const user = userEvent.setup();
    const catalog = await mockServiceCatalogRepository.getCatalog();
    const actions = await mockServiceCatalogRepository.getActions();
    const fetchMock = vi.spyOn(globalThis, "fetch").mockImplementation(async (input) => {
      const url = requestUrl(input);
      if (url.endsWith("/api/v1/service-plaza/catalog")) return jsonResponse(catalog);
      if (url.endsWith("/api/v1/service-plaza/actions")) return jsonResponse(actions);
      throw new Error(`Club Alliance H1 made a denied request: ${url}`);
    });

    renderRoute("/services/club-alliance", realServiceCatalogRepository);
    await user.click(await screen.findByRole("link", { name: "公益俱乐部" }));
    expect(await screen.findByText("需要登录或相应权限")).toBeInTheDocument();
    expect(document.querySelector('[data-page-state="unauthorized"]')).toBeInTheDocument();

    const requests = fetchMock.mock.calls.map(([input]) => requestUrl(input));
    expect(requests).toEqual([
      "/api/v1/service-plaza/catalog",
      "/api/v1/service-plaza/actions",
    ]);
    const denied = /club.*(search|create|join|review|member|payment|charity|federation)/i;
    expect(requests.some((url) => denied.test(url))).toBe(false);
  });

  it("keeps an allowed focused action inside the same catalog/actions allowlist", async () => {
    const user = userEvent.setup();
    const catalog = await mockServiceCatalogRepository.getCatalog();
    const actions = await mockServiceCatalogRepository.getActions();
    const allowedActions = {
      ...actions,
      items: actions.items.map((action) =>
        action.action_id === "public-benefit-club"
          ? { ...action, access: { auth_mode: "anonymous" as const, required_scopes: [] } }
          : action,
      ),
    };
    const fetchMock = vi.spyOn(globalThis, "fetch").mockImplementation(async (input) => {
      const url = requestUrl(input);
      if (url.endsWith("/api/v1/service-plaza/catalog")) return jsonResponse(catalog);
      if (url.endsWith("/api/v1/service-plaza/actions")) return jsonResponse(allowedActions);
      throw new Error(`Club Alliance H1 made a denied request: ${url}`);
    });

    renderRoute("/services/club-alliance", realServiceCatalogRepository);
    await user.click(await screen.findByRole("link", { name: "公益俱乐部" }));
    expect(await screen.findByText("selected_action_id=public-benefit-club")).toBeInTheDocument();
    expect(fetchMock.mock.calls.map(([input]) => requestUrl(input))).toEqual([
      "/api/v1/service-plaza/catalog",
      "/api/v1/service-plaza/actions",
    ]);
  });
});
