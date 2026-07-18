import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AuthProvider } from "../../../auth/AuthContext";
import { ApiError, tokenStorage } from "../../../infrastructure/apiClient";
import { SelfCreatedClubRoute } from "./SelfCreatedClubRoute";
import type {
  SelfCreatedClubApi,
  SelfCreatedClubJoinResult,
} from "./selfCreatedClubApi";
import selfCreatedClubCss from "./SelfCreatedClubPage.css?inline";

const summary = {
  id: 101,
  name: "合成晨光俱乐部",
  intro: "仅用于自动化的虚构简介",
  city: "合成城市",
};

const detail = {
  ...summary,
  memberCount: 9,
  createdAt: "2026-07-12T00:00:00Z",
};

const application = {
  id: 701,
  clubId: 101,
  message: "希望加入",
  status: "pending" as const,
  reviewNote: "",
  createdAt: "2026-07-12T00:00:00Z",
};

const api = (patch: Partial<SelfCreatedClubApi> = {}): SelfCreatedClubApi => ({
  search: vi.fn(async () => ({ items: [summary], total: 1, page: 1, size: 20 })),
  detail: vi.fn(async () => detail),
  join: vi.fn(async () => ({
    status: "created" as const,
    application,
    meta: { status: 201, requestId: "synthetic-join-1", idempotencyReplayed: false },
  })),
  myApplications: vi.fn(async () => ({ items: [application], total: 1, page: 1, size: 20 })),
  ...patch,
});

const setAuthenticatedSession = () => {
  tokenStorage.set("synthetic-sc-page-token");
  sessionStorage.setItem("heaotang_user", JSON.stringify({
    id: 1001,
    nickname: "合成候选用户A",
    scopes: [],
  }));
};

const renderRoute = (
  route: string,
  mode: "list" | "detail" | "applications",
  testApi: SelfCreatedClubApi,
) => render(
  <MemoryRouter initialEntries={[route]}>
    <AuthProvider>
      <Routes>
        <Route
          path={
            mode === "list"
              ? "/services/club-alliance/self-created"
              : mode === "applications"
                ? "/services/club-alliance/self-created/applications"
                : "/services/club-alliance/self-created/:clubId"
          }
          element={<SelfCreatedClubRoute mode={mode} api={testApi} />}
        />
      </Routes>
    </AuthProvider>
  </MemoryRouter>,
);

describe("SelfCreatedClubRoute", () => {
  afterEach(() => {
    sessionStorage.clear();
    vi.restoreAllMocks();
  });

  it.each([
    ["list", "/services/club-alliance/self-created"],
    ["detail", "/services/club-alliance/self-created/101"],
    ["applications", "/services/club-alliance/self-created/applications"],
  ] as const)("guest 进入 %s 时显示认证要求且不发业务请求", async (mode, route) => {
    const testApi = api();
    renderRoute(route, mode, testApi);

    expect(screen.getByRole("heading", { name: "登录后使用自建俱乐部" })).toBeInTheDocument();
    expect(document.querySelectorAll("[data-page-state='authentication-required']")).toHaveLength(1);
    expect(screen.getByRole("heading", {
      level: 1,
      name: mode === "applications"
        ? "本人加入申请"
        : mode === "detail"
          ? "自建俱乐部详情"
          : "自建俱乐部",
    })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "发送验证码" })).toBeInTheDocument();
    await waitFor(() => {
      expect(testApi.search).not.toHaveBeenCalled();
      expect(testApi.detail).not.toHaveBeenCalled();
      expect(testApi.myApplications).not.toHaveBeenCalled();
    });
  });

  it.each(["1e2", "0x65", "+101", "00101", "0", "9007199254740992"])(
    "登录用户访问非 canonical 详情编号 %s 时失败关闭且详情和加入均零请求",
    async (clubId) => {
      setAuthenticatedSession();
      const testApi = api();
      renderRoute(`/services/club-alliance/self-created/${clubId}`, "detail", testApi);

      expect(await screen.findByText("CLUB_ID_INVALID")).toBeInTheDocument();
      expect(screen.getByText("俱乐部编号无效。")).toBeInTheDocument();
      expect(testApi.detail).not.toHaveBeenCalled();
      expect(testApi.join).not.toHaveBeenCalled();
    },
  );

  it("登录用户加载服务端列表并生成详情、本人状态和双返回路径", async () => {
    setAuthenticatedSession();
    const testApi = api();
    renderRoute("/services/club-alliance/self-created", "list", testApi);

    expect(await screen.findByRole("heading", { name: "浏览自建俱乐部" })).toBeInTheDocument();
    expect(await screen.findByText("合成晨光俱乐部")).toBeInTheDocument();
    expect(screen.getByText("仅用于自动化的虚构简介")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "查看详情" })).toHaveAttribute(
      "href",
      "/services/club-alliance/self-created/101",
    );
    expect(screen.getByRole("link", { name: "我的加入申请" })).toHaveAttribute(
      "href",
      "/services/club-alliance/self-created/applications",
    );
    expect(screen.getAllByRole("link", { name: /返回俱乐部联盟/ }).length).toBeGreaterThan(0);
    expect(screen.getByRole("link", { name: "返回服务广场" })).toHaveAttribute(
      "href",
      "/services",
    );
    expect(testApi.search).toHaveBeenCalledWith(
      { query: "", city: "", page: 1 },
      expect.objectContaining({ signal: expect.any(AbortSignal) }),
    );
  });

  it("搜索只把查询交给服务端，不在页面本地筛选", async () => {
    setAuthenticatedSession();
    const user = userEvent.setup();
    const search = vi.fn(async (input = {}) => ({
      items: [{ ...summary, name: `服务端结果-${"query" in input ? input.query : ""}` }],
      total: 1,
      page: 1,
      size: 20,
    }));
    renderRoute("/services/club-alliance/self-created", "list", api({ search }));
    await screen.findByText("服务端结果-");

    await user.type(screen.getByLabelText("关键词"), "晨光");
    await user.type(screen.getByLabelText("城市"), "合成城市");
    await user.click(screen.getByRole("button", { name: "搜索" }));

    expect(await screen.findByText("服务端结果-晨光")).toBeInTheDocument();
    expect(search).toHaveBeenLastCalledWith(
      { query: "晨光", city: "合成城市", page: 1 },
      expect.objectContaining({ signal: expect.any(AbortSignal) }),
    );
  });

  it("详情页加载 intro，单次提交期间禁用按钮并阻止重复点击", async () => {
    setAuthenticatedSession();
    const user = userEvent.setup();
    let resolveJoin: ((value: Awaited<ReturnType<SelfCreatedClubApi["join"]>>) => void) | undefined;
    const join = vi.fn(() => new Promise<Awaited<ReturnType<SelfCreatedClubApi["join"]>>>((resolve) => {
      resolveJoin = resolve;
    }));
    const testApi = api({ join });
    renderRoute("/services/club-alliance/self-created/101", "detail", testApi);

    expect(await screen.findByRole("heading", { name: "合成晨光俱乐部" })).toBeInTheDocument();
    expect(screen.getByText("仅用于自动化的虚构简介")).toBeInTheDocument();
    await user.type(screen.getByLabelText("加入说明（选填）"), "希望加入");
    const submit = screen.getByRole("button", { name: "申请加入" });
    await user.click(submit);
    expect(screen.getByRole("button", { name: "正在提交…" })).toBeDisabled();
    await user.click(screen.getByRole("button", { name: "正在提交…" }));
    expect(join).toHaveBeenCalledTimes(1);
    expect(join).toHaveBeenCalledWith(
      101,
      "希望加入",
      expect.objectContaining({ idempotencyKey: expect.stringMatching(/^club-alliance-join-/) }),
    );

    resolveJoin?.({
      status: "created",
      application,
      meta: { status: 201, requestId: "synthetic-join-2", idempotencyReplayed: false },
    });
    expect(await screen.findByText("申请提交成功，可在本人申请中查看状态。")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "申请已提交" })).toBeDisabled();
  });

  it("服务端重放时显示确定的重复提交结果", async () => {
    setAuthenticatedSession();
    const user = userEvent.setup();
    const testApi = api({
      join: vi.fn(async (): Promise<SelfCreatedClubJoinResult> => ({
        status: "replayed",
        application,
        meta: { status: 200, requestId: "synthetic-replay-1", idempotencyReplayed: true },
      })),
    });
    renderRoute("/services/club-alliance/self-created/101", "detail", testApi);
    await screen.findByRole("heading", { name: "合成晨光俱乐部" });
    await user.click(screen.getByRole("button", { name: "申请加入" }));
    expect(await screen.findByText("该申请已处理，无需重复提交。")).toBeInTheDocument();
  });

  it("同一内容失败后重试复用原 Idempotency-Key", async () => {
    setAuthenticatedSession();
    const user = userEvent.setup();
    const join = vi.fn()
      .mockRejectedValueOnce(new ApiError("in progress", 409, "IDEMPOTENCY_IN_PROGRESS"))
      .mockResolvedValueOnce({
        status: "replayed" as const,
        application,
        meta: { status: 200, requestId: "synthetic-replay-2", idempotencyReplayed: true },
      });
    renderRoute(
      "/services/club-alliance/self-created/101",
      "detail",
      api({ join }),
    );
    await screen.findByRole("heading", { name: "合成晨光俱乐部" });
    await user.type(screen.getByLabelText("加入说明（选填）"), "同一申请");
    await user.click(screen.getByRole("button", { name: "申请加入" }));
    expect(await screen.findByText("同一申请正在处理中，请稍后查看本人申请。")).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "申请加入" }));
    expect(await screen.findByText("该申请已处理，无需重复提交。")).toBeInTheDocument();

    const firstKey = join.mock.calls[0][2].idempotencyKey;
    const secondKey = join.mock.calls[1][2].idempotencyKey;
    expect(secondKey).toBe(firstKey);
  });

  it("同键异载荷冲突后废弃旧键并为下一次提交生成新键", async () => {
    setAuthenticatedSession();
    const user = userEvent.setup();
    const join = vi.fn()
      .mockRejectedValueOnce(new ApiError("reused", 409, "IDEMPOTENCY_KEY_REUSED"))
      .mockResolvedValueOnce({
        status: "created" as const,
        application,
        meta: { status: 201, requestId: "synthetic-created-3", idempotencyReplayed: false },
      });
    renderRoute(
      "/services/club-alliance/self-created/101",
      "detail",
      api({ join }),
    );
    await screen.findByRole("heading", { name: "合成晨光俱乐部" });
    await user.type(screen.getByLabelText("加入说明（选填）"), "申请内容");
    await user.click(screen.getByRole("button", { name: "申请加入" }));
    expect(await screen.findByText("申请内容与原凭证冲突，请重新提交。")).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "申请加入" }));
    expect(await screen.findByText("申请提交成功，可在本人申请中查看状态。")).toBeInTheDocument();

    expect(join.mock.calls[1][2].idempotencyKey).not.toBe(
      join.mock.calls[0][2].idempotencyKey,
    );
  });

  it("本人申请展示三态并按服务端分页切换", async () => {
    setAuthenticatedSession();
    const user = userEvent.setup();
    const items = (["pending", "approved", "rejected"] as const).map((status, index) => ({
      ...application,
      id: 703 - index,
      status,
      reviewNote: status === "rejected" ? "资料不足" : "",
    }));
    const myApplications = vi.fn(async (input = {}) => ({
      items,
      total: 21,
      page: "page" in input && typeof input.page === "number" ? input.page : 1,
      size: 20,
    }));
    renderRoute(
      "/services/club-alliance/self-created/applications",
      "applications",
      api({ myApplications }),
    );

    const list = await screen.findByRole("list", { name: "本人加入申请列表" });
    expect(within(list).getByText("待审核")).toBeInTheDocument();
    expect(within(list).getByText("已通过")).toBeInTheDocument();
    expect(within(list).getByText("未通过")).toBeInTheDocument();
    expect(within(list).getByText("审核说明：资料不足")).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "下一页" }));
    expect(myApplications).toHaveBeenLastCalledWith(
      { page: 2, status: "" },
      expect.objectContaining({ signal: expect.any(AbortSignal) }),
    );
  });

  it("401 会清理失效会话并返回认证页面", async () => {
    setAuthenticatedSession();
    const testApi = api({
      search: vi.fn(async () => {
        throw new ApiError("expired", 401, "AUTH_REQUIRED");
      }),
    });
    renderRoute("/services/club-alliance/self-created", "list", testApi);

    expect(await screen.findByText("登录状态已失效，请重新登录。")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "发送验证码" })).toBeInTheDocument();
    expect(tokenStorage.get()).toBeNull();
  });

  it("320px 到桌面保持单列/有界布局并具备键盘焦点样式", () => {
    expect(selfCreatedClubCss).toContain("min-width: 0");
    expect(selfCreatedClubCss).toContain("@media (max-width: 359px)");
    expect(selfCreatedClubCss).toContain("@media (max-width: 559px)");
    expect(selfCreatedClubCss).toContain("@media (min-width: 900px)");
    expect(selfCreatedClubCss).toContain("grid-template-columns: minmax(0, 1fr)");
    expect(selfCreatedClubCss).toContain("width: min(calc(100vw - 64px), 960px)");
    expect(selfCreatedClubCss).toContain(":focus-visible");
    expect(selfCreatedClubCss).not.toMatch(/\.phone\s*\{[^}]*width:\s*\d+px/s);
  });
});
