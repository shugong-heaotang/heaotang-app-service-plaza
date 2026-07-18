import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { ProjectBrainPage } from "./ProjectBrainPage";
import type { ProjectBrainSnapshot } from "./projectBrainTypes";

const snapshot: ProjectBrainSnapshot = {
  contract_version: "project-brain.snapshot.v1",
  generated_at: "2026-07-12T00:00:00Z",
  source_commit: "0123456789abcdef",
  source_freshness: "current",
  overall_verdict: "partial-go",
  work_summary: { active: 1, "handoff-ready": 1, blocked: 0 },
  active_work: [
    {
      work_id: "AIW-001",
      title: "项目大脑第一版",
      status: "active",
      next_checkpoint: "完成独立验收",
      handoff_record: "docs/project-brain/handoff.md",
    },
  ],
  modules: [
    {
      module_id: "life-navigation",
      name: "生命导航",
      status: "active",
      next_checkpoint: "完成申请历史",
      source_path: "docs/modules/life-navigation/README.md",
      source_updated_at: "2026-07-12T00:00:00Z",
    },
  ],
  pending_decisions: [
    {
      decision_id: "PB-DEC-002",
      question: "是否开放生产入口",
      status: "pending",
      recommendation: "第一版保持关闭",
      source_path: "docs/project-brain/requirements.md",
    },
  ],
  risks: [
    {
      risk_id: "PB-RISK-001",
      title: "状态来源冲突",
      status: "open",
      impact: "high",
      mitigation: "只允许一个权威来源",
      source_path: "docs/project-brain/requirements.md",
    },
  ],
  acceptance_queue: [],
  recent_integrations: [],
  audit_summary: { warning: 1 },
};

const jsonResponse = (value: unknown) => new Response(JSON.stringify(value), {
  status: 200,
  headers: { "Content-Type": "application/json" },
});

const expectMalformedSnapshotToFailClosed = async (value: unknown) => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse(value)));
  render(<ProjectBrainPage />);
  expect(await screen.findByRole("heading", { name: "项目大脑暂不可用" })).toBeInTheDocument();
  expect(screen.getByText("Project Brain 快照版本无效")).toBeInTheDocument();
  expect(screen.queryByText(/Cannot read|Unexpected token|TypeError|undefined is not/)).not.toBeInTheDocument();
};

afterEach(() => vi.unstubAllGlobals());

describe("ProjectBrainPage", () => {
  it("shows the owner summary, sources, next checkpoint, decisions and risks", () => {
    render(<ProjectBrainPage snapshot={snapshot} />);
    expect(screen.getByRole("heading", { name: "和奥堂项目大脑" })).toBeInTheDocument();
    expect(screen.getByText("部分可推进")).toBeInTheDocument();
    expect(screen.getByText("完成独立验收")).toBeInTheDocument();
    expect(screen.getByText("是否开放生产入口")).toBeInTheDocument();
    expect(screen.getByText("状态来源冲突")).toBeInTheDocument();
    expect(screen.getByText(/docs\/modules\/life-navigation\/README.md/)).toBeInTheDocument();
    expect(screen.getByText(/来源提交：0123456789abcdef/)).toBeInTheDocument();
  });

  it("keeps no-go visible and never upgrades it", () => {
    render(<ProjectBrainPage snapshot={{ ...snapshot, overall_verdict: "no-go", audit_summary: { error: 3 } }} />);
    expect(screen.getByText("暂不可推进")).toBeInTheDocument();
    expect(screen.getByText("审计错误").previousSibling).toHaveTextContent("3");
    expect(screen.queryByText("可以推进")).not.toBeInTheDocument();
  });

  it("contains no write, approve, deploy or delete control", () => {
    const { container } = render(<ProjectBrainPage snapshot={snapshot} />);
    expect(screen.queryByRole("button")).not.toBeInTheDocument();
    expect(container.querySelector("form, input, select, textarea")).toBeNull();
    expect(screen.queryByRole("link", { name: /批准|部署|删除|修改/ })).not.toBeInTheDocument();
  });

  it("shows Unknown semantics when loading fails", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false, status: 503 }));
    render(<ProjectBrainPage />);
    expect(await screen.findByRole("heading", { name: "项目大脑暂不可用" })).toBeInTheDocument();
    expect(screen.getByText(/Unknown/)).toBeInTheDocument();
  });

  it("fails closed on HTML fallback without exposing a raw parser error", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("<!doctype html>", {
      status: 200,
      headers: { "Content-Type": "text/html" },
    })));
    render(<ProjectBrainPage />);
    expect(await screen.findByRole("heading", { name: "项目大脑暂不可用" })).toBeInTheDocument();
    expect(screen.getByText("Project Brain 快照格式不可用")).toBeInTheDocument();
    expect(screen.queryByText(/Unexpected token|<!doctype/)).not.toBeInTheDocument();
  });

  it("loads a complete valid snapshot from the generated JSON contract", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse(snapshot)));
    render(<ProjectBrainPage />);
    expect(await screen.findByRole("heading", { name: "和奥堂项目大脑" })).toBeInTheDocument();
    expect(screen.queryByRole("heading", { name: "项目大脑暂不可用" })).not.toBeInTheDocument();
  });

  it.each([
    ["null collection member", { ...snapshot, active_work: [null] }],
    ["missing required member field", { ...snapshot, modules: [{ ...snapshot.modules[0], source_path: undefined }] }],
    ["wrong member field type", { ...snapshot, risks: [{ ...snapshot.risks[0], title: 42 }] }],
    ["invalid enum", { ...snapshot, overall_verdict: "ready" }],
    ["invalid work_summary value", { ...snapshot, work_summary: { active: -1 } }],
    ["invalid audit_summary value", { ...snapshot, audit_summary: { error: "1" } }],
  ])("fails closed for %s without exposing parser or render errors", async (_label, malformed) => {
    await expectMalformedSnapshotToFailClosed(malformed);
  });

  it("renders empty authoritative sections without inventing progress", () => {
    render(
      <ProjectBrainPage
        snapshot={{ ...snapshot, active_work: [], modules: [], pending_decisions: [], risks: [] }}
      />,
    );
    expect(screen.getByText("当前没有活动工作项")).toBeInTheDocument();
    expect(screen.getByText("模块权威登记尚未建立")).toBeInTheDocument();
    expect(screen.getByText("当前没有登记待决定事项")).toBeInTheDocument();
    expect(screen.getByText("风险权威登记尚未建立")).toBeInTheDocument();
  });
});
