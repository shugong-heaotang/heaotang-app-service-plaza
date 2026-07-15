import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AuthProvider } from "../../auth/AuthContext";
import { ApiError } from "../../infrastructure/apiClient";
import type { ProtectionMallCatalogApi } from "./protectionMallApi";
import type { ProtectionMallCatalog } from "./protectionMallContract";
import { ProtectionMallPage } from "./ProtectionMallPage";

vi.mock("../../infrastructure/serviceCatalogRepository", () => ({
  serviceCatalogRepository: { getActions: vi.fn(async () => ({ items: [] })) },
}));

const emptyCatalog: ProtectionMallCatalog = {
  contractVersion: "mall.catalog.v1",
  items: [],
};

const readyCatalog: ProtectionMallCatalog = {
  contractVersion: "mall.catalog.v1",
  items: [{
    contractVersion: "mall.catalog.v1",
    id: "item-1",
    kind: "product",
    title: "家庭照护包",
    sceneIds: ["family-care"],
    responsibility: {
      mallType: "protection_mall",
      productType: "physical",
      sellerId: "seller-1",
      fulfillmentOwnerId: "warehouse-1",
      afterSaleOwnerId: "support-1",
    },
    price: { snapshotId: "price-1", version: 1, currency: "CNY", amountMinor: 9900 },
    benefits: {
      snapshotId: "benefit-1",
      version: 1,
      grants: [{ code: "assurance", quantity: 1 }],
    },
  }],
};

function authenticatedSession() {
  sessionStorage.setItem("heaotang_access_token", "test-token");
  sessionStorage.setItem("heaotang_user", JSON.stringify({ id: 7, nickname: "测试用户", scopes: [] }));
}

function api(loadCatalog: ProtectionMallCatalogApi["loadCatalog"]): ProtectionMallCatalogApi {
  return { loadCatalog: vi.fn(loadCatalog) };
}

function renderPage(catalogApi: ProtectionMallCatalogApi, authenticated = true) {
  if (authenticated) authenticatedSession();
  return render(
    <MemoryRouter initialEntries={["/services/protection-mall"]}>
      <AuthProvider>
        <ProtectionMallPage api={catalogApi} />
      </AuthProvider>
    </MemoryRouter>,
  );
}

function deferred<T>() {
  let resolve!: (value: T) => void;
  let reject!: (reason: unknown) => void;
  const promise = new Promise<T>((success, failure) => {
    resolve = success;
    reject = failure;
  });
  return { promise, resolve, reject };
}

describe("ProtectionMallPage", () => {
  afterEach(() => {
    sessionStorage.clear();
    vi.restoreAllMocks();
  });

  it("未登录时展示真实登录交接且不读取目录", () => {
    const catalogApi = api(async () => emptyCatalog);
    renderPage(catalogApi, false);

    expect(screen.getByRole("heading", { name: "登录后使用核心服务" })).toBeInTheDocument();
    expect(catalogApi.loadCatalog).not.toHaveBeenCalled();
  });

  it("加载期间抑制重复请求并在卸载时取消", () => {
    let signal: AbortSignal | undefined;
    const catalogApi = api((_query, options) => {
      signal = options?.signal;
      return new Promise<ProtectionMallCatalog>(() => undefined);
    });
    const view = renderPage(catalogApi);

    expect(screen.getByRole("status")).toHaveTextContent("正在加载商城目录");
    expect(catalogApi.loadCatalog).toHaveBeenCalledTimes(1);
    expect(screen.getByRole("button", { name: "全部" })).toBeDisabled();
    expect(signal?.aborted).toBe(false);
    view.unmount();
    expect(signal?.aborted).toBe(true);
  });

  it("呈现空状态和真实目录快照", async () => {
    const loadCatalog = vi
      .fn<ProtectionMallCatalogApi["loadCatalog"]>()
      .mockResolvedValueOnce(emptyCatalog)
      .mockResolvedValueOnce(readyCatalog);
    const user = userEvent.setup();
    renderPage({ loadCatalog });

    expect(await screen.findByText("当前场景暂无内容")).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "家庭关怀" }));
    expect(await screen.findByRole("heading", { name: "家庭照护包" })).toBeInTheDocument();
    expect(screen.getByText("¥99.00")).toBeInTheDocument();
    expect(screen.getByText(/售后关闭后生效/)).toBeInTheDocument();
  });

  it("失败后聚焦重试并只触发一次恢复请求", async () => {
    const loadCatalog = vi
      .fn<ProtectionMallCatalogApi["loadCatalog"]>()
      .mockRejectedValueOnce(new ApiError("busy", 503, "UPSTREAM_UNAVAILABLE", "req-mall-001"))
      .mockResolvedValueOnce(emptyCatalog);
    const user = userEvent.setup();
    renderPage({ loadCatalog });

    const retry = await screen.findByRole("button", { name: "重新加载" });
    expect(retry).toHaveFocus();
    expect(screen.getByText("req-mall-001")).toBeInTheDocument();
    await user.click(retry);
    expect(await screen.findByText("当前场景暂无内容")).toBeInTheDocument();
    expect(loadCatalog).toHaveBeenCalledTimes(2);
  });

  it("认证失效会清理会话并回到真实登录交接", async () => {
    const catalogApi = api(async () => {
      throw new ApiError("expired", 401, "AUTH_REQUIRED");
    });
    renderPage(catalogApi);

    expect(await screen.findByRole("heading", { name: "登录后使用核心服务" })).toBeInTheDocument();
    expect(sessionStorage.getItem("heaotang_access_token")).toBeNull();
    expect(sessionStorage.getItem("heaotang_user")).toBeNull();
  });

  it("切换场景会取消旧请求，且迟到响应不能覆盖新结果", async () => {
    const first = deferred<ProtectionMallCatalog>();
    const second = deferred<ProtectionMallCatalog>();
    const signals: AbortSignal[] = [];
    const loadCatalog = vi
      .fn<ProtectionMallCatalogApi["loadCatalog"]>()
      .mockImplementationOnce((_query, options) => {
        if (options?.signal) signals.push(options.signal);
        return first.promise;
      })
      .mockImplementationOnce((_query, options) => {
        if (options?.signal) signals.push(options.signal);
        return second.promise;
      });
    const user = userEvent.setup();
    renderPage({ loadCatalog });

    await user.click(screen.getByRole("button", { name: "健康照护" }));
    expect(signals[0].aborted).toBe(true);
    second.resolve(emptyCatalog);
    expect(await screen.findByText("当前场景暂无内容")).toBeInTheDocument();
    first.resolve(readyCatalog);
    await waitFor(() => expect(screen.queryByText("家庭照护包")).not.toBeInTheDocument());
    expect(loadCatalog).toHaveBeenNthCalledWith(
      2,
      { sceneId: "health-care" },
      expect.objectContaining({ signal: expect.any(AbortSignal) }),
    );
  });

  it("场景筛选支持键盘激活", async () => {
    const catalogApi = api(async () => emptyCatalog);
    const user = userEvent.setup();
    renderPage(catalogApi);
    await screen.findByText("当前场景暂无内容");

    const member = screen.getByRole("button", { name: "会员精选" });
    member.focus();
    await user.keyboard("{Enter}");
    expect(member).toHaveAttribute("aria-pressed", "true");
    expect(catalogApi.loadCatalog).toHaveBeenCalledTimes(2);
  });
});
