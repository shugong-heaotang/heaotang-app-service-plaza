import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AuthProvider } from "../auth/AuthContext";
import { AuthPanel } from "./AuthPanel";

describe("AuthPanel", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    sessionStorage.clear();
  });

  it("发送验证码后不会展示后端返回的验证码", async () => {
    const user = userEvent.setup();
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ success: true, data: { message: "验证码已发送", code: "654321" } }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );

    render(
      <AuthProvider>
        <AuthPanel />
      </AuthProvider>,
    );

    await user.type(screen.getByLabelText("手机号"), "13800138000");
    await user.click(screen.getByRole("button", { name: "发送验证码" }));

    expect(await screen.findByText(/页面不会显示验证码/)).toBeInTheDocument();
    expect(screen.queryByText("654321")).not.toBeInTheDocument();
  });

  it("不足六位的验证码不会提交到服务端", async () => {
    const user = userEvent.setup();
    const fetchMock = vi.spyOn(globalThis, "fetch");
    render(<AuthProvider><AuthPanel /></AuthProvider>);

    await user.type(screen.getByLabelText("手机号"), "13800138000");
    await user.type(screen.getByLabelText("验证码"), "12345");
    await user.click(screen.getByRole("button", { name: "登录" }));

    expect(screen.getByRole("alert")).toHaveTextContent("6 位数字验证码");
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
