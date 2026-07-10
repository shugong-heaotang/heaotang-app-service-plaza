import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, describe, expect, it } from "vitest";
import { ActionRuntimeProvider } from "../auth/ActionRuntimeContext";
import { AuthProvider } from "../auth/AuthContext";
import { CoreServicePage } from "./CoreServicePage";

function renderManageView(scopes: string[]) {
  sessionStorage.setItem("heaotang_access_token", "test-token");
  sessionStorage.setItem(
    "heaotang_user",
    JSON.stringify({ id: 7, nickname: "测试用户", scopes }),
  );
  render(
    <MemoryRouter initialEntries={["/services/club-alliance?view=manage"]}>
      <AuthProvider>
        <ActionRuntimeProvider>
          <Routes>
            <Route path="/services/:serviceKey" element={<CoreServicePage />} />
          </Routes>
        </ActionRuntimeProvider>
      </AuthProvider>
    </MemoryRouter>,
  );
}

describe("俱乐部管理试用入口", () => {
  afterEach(() => sessionStorage.clear());

  it("普通会员进入后显示真实权限拒绝，不展示加入表单", async () => {
    renderManageView([]);

    expect(screen.getByText("暂时没有俱乐部管理权限")).toBeInTheDocument();
    expect(screen.queryByLabelText("选择俱乐部")).not.toBeInTheDocument();
  });

  it("具备 club:manage 时显示试用状态，不伪装业务管理功能已完成", () => {
    renderManageView(["club:manage"]);

    expect(screen.getByText("管理权限验证通过 · 试用入口")).toBeInTheDocument();
    expect(screen.getByText(/业务管理功能将在需求冻结后/)).toBeInTheDocument();
    expect(screen.queryByLabelText("选择俱乐部")).not.toBeInTheDocument();
  });
});
