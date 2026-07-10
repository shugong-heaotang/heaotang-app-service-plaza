import { fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import type { ServiceAction } from "../domain/serviceActions";
import { ActionControl } from "./ActionControl";

const createAction = (
  lifecycleStatus: ServiceAction["lifecycle_status"],
): ServiceAction => ({
  action_id: `test-${lifecycleStatus}`,
  region: "common_services",
  sort_order: 10,
  label: lifecycleStatus,
  action_type: "service_entry",
  target: `/target/${lifecycleStatus}`,
  lifecycle_status: lifecycleStatus,
  access: { auth_mode: "anonymous", required_scopes: [] },
  service_id: null,
  return_target: "/services",
  telemetry_event: `test.${lifecycleStatus}`,
});

describe("标准动作控件", () => {
  it.each(["planned", "maintenance", "offline"] as const)(
    "%s 动作不可执行",
    (status) => {
      render(
        <MemoryRouter>
          <ActionControl action={createAction(status)} />
        </MemoryRouter>,
      );

      expect(screen.getByRole("button", { name: status })).toBeDisabled();
      expect(screen.queryByRole("link", { name: status })).not.toBeInTheDocument();
    },
  );

  it("active 动作只使用清单提供的目标", () => {
    render(
      <MemoryRouter>
        <ActionControl action={createAction("active")} />
      </MemoryRouter>,
    );

    expect(screen.getByRole("link", { name: "active" })).toHaveAttribute(
      "href",
      "/target/active",
    );
  });

  it("内部共享会话入口未登录时仍可进入登录承接页", () => {
    const shared = createAction("active");
    shared.access = { auth_mode: "shared_session", required_scopes: ["service:use"] };
    render(
      <MemoryRouter>
        <ActionControl action={shared} />
      </MemoryRouter>,
    );

    expect(screen.getByRole("link", { name: "active" })).toHaveAttribute(
      "data-access-state",
      "authentication_required",
    );
  });

  it("外部 OIDC 动作没有受控 PKCE 启动器时禁止执行", () => {
    const external = createAction("active");
    external.target = "https://partner.example/app";
    external.access = { auth_mode: "oidc_pkce", required_scopes: [] };
    render(
      <MemoryRouter>
        <ActionControl action={external} />
      </MemoryRouter>,
    );

    expect(screen.getByRole("button", { name: "active" })).toBeDisabled();
  });

  it("内部入口权限预检失败会发出不含用户数据的审计事件", () => {
    const shared = createAction("active");
    shared.access = { auth_mode: "shared_session", required_scopes: ["club:manage"] };
    const listener = vi.fn();
    window.addEventListener("heaotang:action-access-required", listener);
    render(
      <MemoryRouter>
        <ActionControl
          action={shared}
          session={{ authenticated: true, scopes: [] }}
        />
      </MemoryRouter>,
    );

    fireEvent.click(screen.getByRole("link", { name: "active" }));

    expect(listener).toHaveBeenCalledTimes(1);
    expect((listener.mock.calls[0][0] as CustomEvent).detail).toEqual({
      action_id: "test-active",
      reason: "scope_required",
      missing_scopes: ["club:manage"],
      telemetry_event: "test.active",
    });
    window.removeEventListener("heaotang:action-access-required", listener);
  });
});
