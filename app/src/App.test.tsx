import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { AppRoutes } from "./App";
import { AuthProvider } from "./auth/AuthContext";

const renderAt = (route: string) =>
  render(
    <MemoryRouter initialEntries={[route]}>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </MemoryRouter>,
  );

describe("服务广场主链路", () => {
  it("通过标准目录展示定版的三大核心服务与常用服务", async () => {
    renderAt("/services");

    expect(screen.getByRole("heading", { name: "服务广场" })).toBeInTheDocument();
    expect(await screen.findByRole("link", { name: /生命导航/ })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "俱乐部联盟" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /健康大管家/ })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /活动广场/ })).toBeInTheDocument();
  });

  it("可以进入生命导航、提交申请并返回服务广场", async () => {
    const user = userEvent.setup();
    renderAt("/services");

    await user.click(await screen.findByRole("link", { name: /生命导航/ }));
    expect(screen.getByRole("heading", { level: 1, name: "生命导航" })).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: "提交导航申请" }));
    expect(await screen.findByText("导航申请已提交，等待服务人员处理。")).toBeInTheDocument();

    await user.click(screen.getByRole("link", { name: "← 返回服务广场" }));
    expect(screen.getByRole("heading", { name: "服务广场" })).toBeInTheDocument();
  });

  it("无权限状态会显示恢复说明且不展示主动作", async () => {
    const user = userEvent.setup();
    renderAt("/services/club-alliance");

    await user.click(screen.getByRole("button", { name: "无权限" }));
    expect(screen.getByText("暂时没有访问权限")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "申请加入俱乐部" })).not.toBeInTheDocument();
    expect(screen.getByRole("link", { name: "← 返回服务广场" })).toBeInTheDocument();
  });

  it("未知路由提供返回服务广场的恢复路径", () => {
    renderAt("/missing");

    expect(screen.getByText("这个页面不存在")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "返回服务广场" })).toBeInTheDocument();
  });
});
