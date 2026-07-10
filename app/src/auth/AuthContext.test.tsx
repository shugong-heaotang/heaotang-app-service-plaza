import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AuthProvider, useAuth } from "./AuthContext";

function AuthProbe() {
  const { user, login } = useAuth();
  return (
    <div>
      <button type="button" onClick={() => void login("13800138000", "123456")}>
        登录
      </button>
      <output aria-label="权限">{JSON.stringify(user?.scopes ?? [])}</output>
    </div>
  );
}

describe("AuthProvider scopes", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    sessionStorage.clear();
  });

  it("保存 v1 登录响应中的真实 scopes", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(
        JSON.stringify({
          success: true,
          data: {
            token: "signed-token",
            user_id: 7,
            user: {
              id: 7,
              phone: "13800138000",
              nickname: "管理者",
              scopes: ["club:manage"],
            },
          },
        }),
        { status: 200, headers: { "Content-Type": "application/json" } },
      ),
    );
    const user = userEvent.setup();
    render(
      <AuthProvider>
        <AuthProbe />
      </AuthProvider>,
    );

    await user.click(screen.getByRole("button", { name: "登录" }));

    expect(await screen.findByText('["club:manage"]')).toBeInTheDocument();
    expect(JSON.parse(sessionStorage.getItem("heaotang_user") ?? "null")).toMatchObject({
      id: 7,
      scopes: ["club:manage"],
    });
  });

  it("把旧会话中缺失的 scopes 安全迁移为空数组", () => {
    sessionStorage.setItem("heaotang_access_token", "existing-token");
    sessionStorage.setItem("heaotang_user", JSON.stringify({ id: 8, nickname: "普通用户" }));

    render(
      <AuthProvider>
        <AuthProbe />
      </AuthProvider>,
    );

    expect(screen.getByLabelText("权限")).toHaveTextContent("[]");
  });
});
