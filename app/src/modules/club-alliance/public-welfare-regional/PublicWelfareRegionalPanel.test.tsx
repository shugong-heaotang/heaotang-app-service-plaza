import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { PublicWelfareRegionalPanel } from "./PublicWelfareRegionalPanel";
import type { PublicWelfareRegionalApi } from "./publicWelfareRegionalApi";

const api = (): PublicWelfareRegionalApi => ({
  submitEstablishment: vi.fn(async (input) => ({ ...input, id: 11, applicant_id: 2, status: "submitted", review_note: "", created_at: "2026-07-15T00:00:00Z" })),
  listMyEstablishments: vi.fn(async () => []), listEstablishments: vi.fn(async () => []),
  reviewEstablishment: vi.fn(async () => { throw new Error("not used"); }),
  submitRegionalRole: vi.fn(async (input) => ({ ...input, id: 21, applicant_id: 2, status: "submitted", review_note: "", created_at: "2026-07-15T00:00:00Z" })),
  listMyRegionalRoles: vi.fn(async () => []), listRegionalRoles: vi.fn(async () => []),
  reviewRegionalRole: vi.fn(async () => { throw new Error("not used"); }),
  searchCenters: vi.fn(async () => [{ id: 31, kind: "public_welfare_service_center" as const, name: "西湖公益服务中心", province: "浙江省", city: "杭州市", district: "西湖区", address: "古荡街道1号", contact_name: "王老师", contact_phone_masked: "138****0000", service_hours: "周一至周五" }]),
});

describe("PublicWelfareRegionalPanel", () => {
  it("explains approval-only creation and submits all PDCAR fields", async () => {
    const user = userEvent.setup(); const client = api();
    render(<PublicWelfareRegionalPanel mode="public-welfare" api={client} />);
    expect(screen.getByText(/不能从普通“创建俱乐部”入口直接创建/)).toBeInTheDocument();
    const inputs = ["拟创办名称", "省", "市", "区/县"];
    for (const name of inputs) await user.type(screen.getByLabelText(name), "合成值");
    for (const name of ["公益使命", "申请资格与团队条件", "可投入资源", "治理与责任分工", "风险、合规及应对", "P · 计划", "D · 执行", "C · 检查", "A · 改进", "R · 记录与复盘"]) await user.type(screen.getByLabelText(name), "完整说明");
    await user.click(screen.getByRole("button", { name: "提交创办申请" }));
    expect(client.submitEstablishment).toHaveBeenCalledWith(expect.objectContaining({ pdcar: { plan: "完整说明", do: "完整说明", check: "完整说明", act: "完整说明", record: "完整说明" } }));
    expect(await screen.findByText(/联盟审核批准后/)).toBeInTheDocument();
  });

  it("searches both center kinds and offers director/deputy application", async () => {
    const user = userEvent.setup(); const client = api();
    render(<PublicWelfareRegionalPanel mode="regional-public" api={client} />);
    expect(await screen.findByText("西湖公益服务中心")).toBeInTheDocument();
    expect(screen.getByRole("option", { name: "区域管理中心" })).toBeInTheDocument();
    expect(screen.getByRole("option", { name: "公益服务中心" })).toBeInTheDocument();
    expect(screen.getByRole("option", { name: "主任" })).toBeInTheDocument();
    expect(screen.getByRole("option", { name: "副主任" })).toBeInTheDocument();
    await user.type(screen.getByRole("textbox", { name: "名称或地址" }), "古荡");
    await user.click(screen.getByRole("button", { name: "查找" }));
    expect(client.searchCenters).toHaveBeenLastCalledWith(expect.objectContaining({ query: "古荡" }));
  });

  it("requires a review note before an administrator can approve", async () => {
    const user = userEvent.setup(); const client = api();
    vi.mocked(client.listEstablishments).mockResolvedValue([{ id: 41, applicant_id: 2, status: "submitted", review_note: "", created_at: "2026-07-15", name: "合成公益", province: "浙江", city: "杭州", district: "西湖", mission: "助老", eligibility: "团队", resources: "场地", governance: "理事会", risks: "隐私", pdcar: { plan: "p", do: "d", check: "c", act: "a", record: "r" } }]);
    vi.mocked(client.reviewEstablishment).mockImplementation(async (input) => ({ ...(await vi.mocked(client.listEstablishments)())[0], status: input.decision, review_note: input.note }));
    render(<PublicWelfareRegionalPanel mode="management" api={client} />);
    const approve = await screen.findByRole("button", { name: "批准" });
    expect(approve).toBeDisabled(); await user.type(screen.getByLabelText("统一审核意见"), "条件完整"); await user.click(approve);
    expect(client.reviewEstablishment).toHaveBeenCalledWith({ applicationId: 41, decision: "approved", note: "条件完整" });
  });
});
