import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { ActivityM1 } from "./ActivityM1";
import { createActivityM1MockRepository } from "./activityMockRepository";
import type { ActivityM1Model } from "./activityModels";
import css from "./ActivityM1.css?inline";

const ready = createActivityM1MockRepository().load();

describe("ActivityM1", () => {
  it("renders public discovery, detail, proposal and isolation boundary", () => {
    render(<ActivityM1 model={ready} />);
    expect(screen.getByRole("heading", { name: "发现活动与我的进度" })).toBeInTheDocument();
    expect(screen.getByText("俱乐部周末共创会")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "查看详情" })).toHaveAttribute("href", "/services/activity/activity-synthetic-001");
    expect(screen.getByText("俱乐部审核中")).toBeInTheDocument();
    expect(screen.getByLabelText("M1 隔离边界")).toHaveTextContent("不调用 AI、关系推荐、消息、商城、订单或支付");
  });

  it("keeps registration user initiated and free", () => {
    const onRegister = vi.fn();
    render(<ActivityM1 model={ready} onRegister={onRegister} />);
    fireEvent.click(screen.getByRole("button", { name: "确认免费报名" }));
    expect(onRegister).toHaveBeenCalledTimes(1);
    expect(onRegister).toHaveBeenCalledWith("activity-synthetic-001");
  });

  it("does not render a registration button without an explicit handler", () => {
    render(<ActivityM1 model={ready} />);
    expect(screen.queryByRole("button", { name: "确认免费报名" })).not.toBeInTheDocument();
  });

  it.each([
    ["registered", "已报名"],
    ["full", "名额已满"],
    ["ineligible", "暂不符合资格"],
  ] as const)("renders %s without an action", (status, label) => {
    const model: ActivityM1Model = {
      ...ready,
      activities: [{ ...ready.activities![0], registrationStatus: status }],
    };
    render(<ActivityM1 model={model} onRegister={vi.fn()} />);
    expect(screen.getByText(label)).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "确认免费报名" })).not.toBeInTheDocument();
  });

  it("renders empty state without fallback records", () => {
    render(<ActivityM1 model={{ state: "empty", activities: [], proposals: [] }} />);
    expect(screen.getByText("当前没有可公开发现的活动。")).toBeInTheDocument();
    expect(screen.getByText("暂无本人提案。")).toBeInTheDocument();
  });

  it.each([
    ["loading", "正在加载活动"],
    ["unauthorized", "登录后查看本人活动"],
    ["error", "活动暂时无法读取"],
  ] as const)("renders %s state", (state, title) => {
    render(<ActivityM1 model={{ state }} />);
    expect(screen.getByRole(state === "error" ? "alert" : "status")).toHaveTextContent(title);
  });

  it("declares responsive and keyboard focus rules", () => {
    expect(css).toContain("@media (min-width:720px)");
    expect(css).toContain("@media (max-width:479px)");
    expect(css).toContain(":focus-visible");
    expect(css).toContain("min-width:0");
  });
});
