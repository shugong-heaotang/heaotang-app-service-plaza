import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { afterEach, vi } from "vitest";
import { AppRoutes } from "./App";
import { AuthProvider } from "./auth/AuthContext";
import { ActionRuntimeProvider } from "./auth/ActionRuntimeContext";
import { tokenStorage } from "./infrastructure/apiClient";

const renderAt = (route: string) =>
  render(
    <MemoryRouter initialEntries={[route]}>
      <AuthProvider>
        <ActionRuntimeProvider>
          <AppRoutes />
        </ActionRuntimeProvider>
      </AuthProvider>
    </MemoryRouter>,
  );

const jsonResponse = (data: unknown, status = 200, headers: Record<string, string> = {}) =>
  new Response(JSON.stringify({ success: true, data }), {
    status,
    headers: { "Content-Type": "application/json", ...headers },
  });

const requestUrl = (input: RequestInfo | URL) => {
  if (typeof input === "string") return input;
  return input instanceof URL ? input.toString() : input.url;
};

const setAuthenticatedSession = () => {
  tokenStorage.set("app-route-token");
  sessionStorage.setItem("heaotang_user", JSON.stringify({
    id: 7,
    nickname: "路由测试用户",
    scopes: [],
  }));
};

describe("服务广场主链路", () => {
  afterEach(() => {
    sessionStorage.clear();
    vi.restoreAllMocks();
  });

  it("通过标准目录展示定版的三大核心服务与常用服务", async () => {
    renderAt("/services");

    expect(screen.getByRole("heading", { name: "服务广场" })).toBeInTheDocument();
    expect(await screen.findByRole("link", { name: /生命导航/ })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "俱乐部联盟" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /健康大管家/ })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /活动广场/ })).toBeInTheDocument();
  });

  it("所有板块共享当前账号和退出入口", async () => {
    const user = userEvent.setup();
    setAuthenticatedSession();
    renderAt("/services");

    expect(await screen.findByLabelText("当前登录账号")).toHaveTextContent("路由测试用户");
    await user.click(screen.getByRole("button", { name: "退出登录" }));
    expect(screen.queryByLabelText("当前登录账号")).not.toBeInTheDocument();
    expect(tokenStorage.get()).toBeNull();
  });

  it("管理权限不足时提供可见反馈而不是静默无响应", async () => {
    const user = userEvent.setup();
    setAuthenticatedSession();
    renderAt("/services");

    await user.click(await screen.findByRole("link", { name: "管理中心" }));
    expect(screen.getByRole("alert")).toHaveTextContent("缺少 club:manage 权限");
  });

  it("可以进入生命导航、提交申请并返回服务广场", async () => {
    const user = userEvent.setup();
    setAuthenticatedSession();
    let historyReads = 0;
    const application = {
      id: 81,
      user_id: 7,
      dimension_id: "yun",
      record_type: "application",
      title: "服务广场导航申请",
      note: "希望梳理事业方向",
      created_at: "2026-07-11T00:00:00Z",
    };
    const fetchMock = vi.spyOn(globalThis, "fetch").mockImplementation(async (input, init) => {
      const url = requestUrl(input);
      const method = (init?.method ?? "GET").toUpperCase();

      if (url.includes("/api/v1/life-nav/records?limit=30") && method === "GET") {
        historyReads += 1;
        return jsonResponse({ items: historyReads === 1 ? [] : [application] });
      }
      if (url.endsWith("/api/v1/life-nav/records") && method === "POST") {
        return jsonResponse(application, 201, { "X-Request-ID": "route-created-1" });
      }
      if (url.endsWith("/api/v1/service-plaza/feature-flags") && method === "GET") {
        return jsonResponse({ items: [] });
      }

      throw new Error(`路由测试出现未声明的请求：${method} ${url}`);
    });
    renderAt("/services");

    await user.click(await screen.findByRole("link", { name: /生命导航/ }));
    expect(screen.getByRole("heading", { level: 1, name: "生命导航" })).toBeInTheDocument();
    expect(await screen.findByText("暂无申请记录。")).toBeInTheDocument();
    expect(screen.queryByLabelText("联调状态切换")).not.toBeInTheDocument();

    await user.type(screen.getByLabelText("申请说明（选填）"), "希望梳理事业方向");
    await user.click(screen.getByRole("button", { name: "提交申请" }));
    expect(await screen.findByText("申请提交成功。")).toBeInTheDocument();
    expect(await screen.findByText("希望梳理事业方向")).toBeInTheDocument();
    const lifeNavigationCalls = fetchMock.mock.calls.map(([input, init]) => ({
      method: (init?.method ?? "GET").toUpperCase(),
      url: requestUrl(input),
    })).filter(({ url }) => url.includes("/api/v1/life-nav/records"));
    expect(lifeNavigationCalls).toEqual([
      { method: "GET", url: "/api/v1/life-nav/records?limit=30" },
      { method: "POST", url: "/api/v1/life-nav/records" },
      { method: "GET", url: "/api/v1/life-nav/records?limit=30" },
    ]);

    const returnLinks = screen.getAllByRole("link", { name: /返回服务广场/ });
    await user.click(returnLinks[returnLinks.length - 1]);
    expect(screen.getByRole("heading", { name: "服务广场" })).toBeInTheDocument();
  });

  it("俱乐部联盟使用独立标准首页路由，不再落入通用业务页", async () => {
    renderAt("/services/club-alliance");

    expect(await screen.findByRole("heading", { level: 2, name: "选择俱乐部服务" })).toBeInTheDocument();
    expect(screen.getByText("公益俱乐部")).toBeInTheDocument();
    expect(screen.getByText("俱乐部友联体")).toBeInTheDocument();
    expect(screen.queryByLabelText("联调状态切换")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "申请加入俱乐部" })).not.toBeInTheDocument();
    expect(screen.getByRole("link", { name: "← 返回服务广场" })).toBeInTheDocument();
  });

  it("本人申请静态路由优先于 :clubId 并且只读取本人列表", async () => {
    setAuthenticatedSession();
    const fetchMock = vi.spyOn(globalThis, "fetch").mockImplementation(async (input, init) => {
      const url = requestUrl(input);
      const method = (init?.method ?? "GET").toUpperCase();
      if (
        url === "/api/v1/clubs/join-applications/my?page=1&size=20" &&
        method === "GET"
      ) {
        return jsonResponse({ items: [], total: 0, page: 1, size: 20 });
      }
      throw new Error(`SC 路由测试出现未声明的请求：${method} ${url}`);
    });

    renderAt("/services/club-alliance/self-created/applications");

    expect(await screen.findByRole("heading", { name: "我的加入申请" })).toBeInTheDocument();
    expect(screen.getByText("暂无加入申请")).toBeInTheDocument();
    expect(fetchMock.mock.calls.map(([input]) => requestUrl(input))).toEqual([
      "/api/v1/clubs/join-applications/my?page=1&size=20",
    ]);
  });

  it("健康大管家使用独立模块路由挂载边界", () => {
    renderAt("/services/health-manager");

    expect(screen.getByTestId("health-manager-module-route")).toBeInTheDocument();
    expect(screen.getByRole("heading", { level: 1, name: "健康大管家" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "← 返回服务广场" })).toBeInTheDocument();
    expect(screen.queryByLabelText("联调状态切换")).not.toBeInTheDocument();
    expect(screen.queryByText(/开发联调/)).not.toBeInTheDocument();
  });

  it("未知路由提供返回服务广场的恢复路径", () => {
    renderAt("/missing");

    expect(screen.getByText("这个页面不存在")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "返回服务广场" })).toBeInTheDocument();
  });

  it("开发与测试环境提供内部只读 Project Brain 路由", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(JSON.stringify({
      contract_version: "project-brain.snapshot.v1",
      generated_at: "2026-07-12T00:00:00Z",
      source_commit: "test-commit",
      source_freshness: "current",
      overall_verdict: "no-go",
      modules: [], work_summary: {}, active_work: [], pending_decisions: [], risks: [],
      acceptance_queue: [], recent_integrations: [], audit_summary: { error: 1 },
    }), { status: 200, headers: { "Content-Type": "application/json" } }));

    renderAt("/internal/project-brain");
    expect(await screen.findByRole("heading", { name: "和奥堂项目大脑" })).toBeInTheDocument();
    expect(screen.getByText("暂不可推进")).toBeInTheDocument();
    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });
});
