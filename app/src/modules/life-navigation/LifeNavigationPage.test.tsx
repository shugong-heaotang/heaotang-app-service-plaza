import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AuthProvider } from "../../auth/AuthContext";
import { ApiError } from "../../infrastructure/apiClient";
import type {
  LifeNavigationApplicationRecord,
  LifeNavigationHistoryState,
  LifeNavigationSubmissionResult,
} from "./lifeNavigationApi";
import {
  LifeNavigationPage,
  type LifeNavigationPageApi,
} from "./LifeNavigationPage";

const record: LifeNavigationApplicationRecord = {
  id: "81",
  dimensionId: "yun",
  title: "服务广场导航申请",
  note: "希望获得职业方向导航",
  createdAt: "2026-07-10T16:20:00Z",
  displayStatus: "submitted",
};

const createdResult: LifeNavigationSubmissionResult = {
  status: "created",
  record,
  meta: { status: 201, requestId: "req-created", idempotencyReplayed: false },
};

const replayedResult: LifeNavigationSubmissionResult = {
  status: "replayed",
  record,
  meta: { status: 200, requestId: "req-replayed", idempotencyReplayed: true },
};

function createApi(overrides: Partial<LifeNavigationPageApi> = {}): LifeNavigationPageApi {
  return {
    loadHistory: vi.fn<LifeNavigationPageApi["loadHistory"]>(async () => ({ status: "empty" })),
    submitApplication: vi.fn(async () => createdResult),
    ...overrides,
  };
}

function setAuthenticatedSession() {
  sessionStorage.setItem("heaotang_access_token", "test-token");
  sessionStorage.setItem(
    "heaotang_user",
    JSON.stringify({ id: 7, nickname: "测试用户", scopes: [] }),
  );
}

function renderPage(api: LifeNavigationPageApi, authenticated = true) {
  if (authenticated) setAuthenticatedSession();
  return render(
    <MemoryRouter initialEntries={["/services/life-navigation"]}>
      <AuthProvider>
        <Routes>
          <Route path="/services/life-navigation" element={<LifeNavigationPage api={api} />} />
          <Route path="/services" element={<h1>服务广场目标页</h1>} />
        </Routes>
      </AuthProvider>
    </MemoryRouter>,
  );
}

describe("LifeNavigationPage", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    sessionStorage.clear();
  });

  it("未登录时提供真实登录交接且不读取个人记录", () => {
    const api = createApi();
    renderPage(api, false);

    expect(screen.getByRole("heading", { name: "登录后使用核心服务" })).toBeInTheDocument();
    expect(screen.getByLabelText("手机号")).toBeInTheDocument();
    expect(api.loadHistory).not.toHaveBeenCalled();
  });

  it("登录后自动进入加载状态并在卸载时中止读取", () => {
    let readSignal: AbortSignal | undefined;
    const api = createApi({
      loadHistory: vi.fn<LifeNavigationPageApi["loadHistory"]>(({ signal } = {}) => {
        readSignal = signal;
        return new Promise<LifeNavigationHistoryState>(() => undefined);
      }),
    });
    const view = renderPage(api);

    expect(screen.getByText("正在加载申请记录…")).toBeInTheDocument();
    expect(readSignal?.aborted).toBe(false);
    view.unmount();
    expect(readSignal?.aborted).toBe(true);
  });

  it("显示个人记录空状态", async () => {
    renderPage(createApi());
    expect(await screen.findByText("暂无申请记录。")).toBeInTheDocument();
  });

  it("历史列表只呈现已提交、时间和申请说明", async () => {
    renderPage(createApi({
      loadHistory: vi.fn<LifeNavigationPageApi["loadHistory"]>(async () => ({
        status: "ready",
        items: [record],
      })),
    }));

    expect(await screen.findByText("已提交")).toBeInTheDocument();
    expect(screen.getByText("希望获得职业方向导航")).toBeInTheDocument();
    expect(screen.getByText(/2026/)).toBeInTheDocument();
    expect(screen.queryByText(record.title)).not.toBeInTheDocument();
    expect(screen.queryByText(record.dimensionId)).not.toBeInTheDocument();
  });

  it("新建成功后展示确认并刷新历史", async () => {
    const user = userEvent.setup();
    const loadHistory = vi
      .fn<LifeNavigationPageApi["loadHistory"]>()
      .mockResolvedValueOnce({ status: "empty" })
      .mockResolvedValueOnce({ status: "ready", items: [record] });
    const api = createApi({ loadHistory, submitApplication: vi.fn(async () => createdResult) });
    renderPage(api);

    await screen.findByText("暂无申请记录。");
    await user.type(screen.getByLabelText("申请说明（选填）"), "希望获得职业方向导航");
    await user.click(screen.getByRole("button", { name: "提交申请" }));

    expect(await screen.findByText("申请提交成功。")).toBeInTheDocument();
    expect(await screen.findByText("希望获得职业方向导航")).toBeInTheDocument();
    expect(loadHistory).toHaveBeenCalledTimes(2);
  });

  it("幂等回放显示非重复提交结果并刷新历史", async () => {
    const user = userEvent.setup();
    const loadHistory = vi
      .fn<LifeNavigationPageApi["loadHistory"]>()
      .mockResolvedValueOnce({ status: "empty" })
      .mockResolvedValueOnce({ status: "ready", items: [record] });
    renderPage(createApi({ loadHistory, submitApplication: vi.fn(async () => replayedResult) }));

    await screen.findByText("暂无申请记录。");
    await user.click(screen.getByRole("button", { name: "提交申请" }));

    expect(await screen.findByText("申请已处理，无需重复提交。")).toBeInTheDocument();
    expect(loadHistory).toHaveBeenCalledTimes(2);
  });

  it("明确展示每日申请上限错误", async () => {
    const user = userEvent.setup();
    const api = createApi({
      submitApplication: vi.fn(async () => {
        throw new ApiError("limit", 429, "LIFE_RECORD_DAILY_LIMIT");
      }),
    });
    renderPage(api);
    await screen.findByText("暂无申请记录。");

    await user.click(screen.getByRole("button", { name: "提交申请" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("今日申请次数已达上限");
  });

  it.each([
    [new ApiError("busy", 409, "IDEMPOTENCY_IN_PROGRESS"), "同一申请正在处理中"],
    [new ApiError("conflict", 409, "IDEMPOTENCY_KEY_REUSED"), "申请凭证与原内容冲突"],
    [new ApiError("network", 0, "NETWORK_ERROR"), "网络连接异常"],
    [new Error("unexpected"), "提交失败，请稍后重试"],
  ])("将业务、网络和未知提交错误转换为可操作提示", async (reason, expected) => {
    const user = userEvent.setup();
    const api = createApi({
      submitApplication: vi.fn(async () => {
        throw reason;
      }),
    });
    renderPage(api);
    await screen.findByText("暂无申请记录。");

    await user.click(screen.getByRole("button", { name: "提交申请" }));
    expect(await screen.findByRole("alert")).toHaveTextContent(expected);
  });

  it("认证错误会清理会话并回到真实登录入口", async () => {
    const user = userEvent.setup();
    const api = createApi({
      submitApplication: vi.fn(async () => {
        throw new ApiError("expired", 401, "AUTH_REQUIRED");
      }),
    });
    renderPage(api);
    await screen.findByText("暂无申请记录。");

    await user.click(screen.getByRole("button", { name: "提交申请" }));
    expect(await screen.findByText("登录状态已失效，请重新登录。")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "登录后使用核心服务" })).toBeInTheDocument();
    expect(sessionStorage.getItem("heaotang_access_token")).toBeNull();
  });

  it("用户登出再登录时不会恢复上一账号的敏感草稿", async () => {
    const user = userEvent.setup();
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ success: true, data: { token: "next-token", user_id: 8, user: { id: 8, nickname: "下一用户", scopes: [] } } }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );
    renderPage(createApi());
    await screen.findByText("暂无申请记录。");
    await user.type(screen.getByLabelText("申请说明（选填）"), "上一用户的敏感草稿");
    await user.click(screen.getByRole("button", { name: "退出登录" }));

    await user.type(screen.getByLabelText("手机号"), "13800138000");
    await user.type(screen.getByLabelText("验证码"), "123456");
    await user.click(screen.getByRole("button", { name: "登录" }));

    expect(await screen.findByLabelText("申请说明（选填）")).toHaveValue("");
    expect(screen.queryByText("上一用户的敏感草稿")).not.toBeInTheDocument();
  });

  it("历史加载失败后可以重试恢复", async () => {
    const user = userEvent.setup();
    const loadHistory = vi
      .fn<LifeNavigationPageApi["loadHistory"]>()
      .mockResolvedValueOnce({
        status: "error",
        error: new ApiError("network", 0, "NETWORK_ERROR"),
      })
      .mockResolvedValueOnce({ status: "empty" });
    renderPage(createApi({ loadHistory }));

    expect(await screen.findByRole("alert")).toHaveTextContent("申请记录加载失败");
    await user.click(screen.getByRole("button", { name: "重新加载" }));
    expect(await screen.findByText("暂无申请记录。")).toBeInTheDocument();
    expect(loadHistory).toHaveBeenCalledTimes(2);
  });

  it("返回动作固定导航到服务广场", async () => {
    const user = userEvent.setup();
    renderPage(createApi());
    await screen.findByText("暂无申请记录。");

    const links = screen.getAllByRole("link", { name: /返回服务广场/ });
    await user.click(links[links.length - 1]);
    await waitFor(() => expect(screen.getByRole("heading", { name: "服务广场目标页" })).toBeInTheDocument());
  });
});
