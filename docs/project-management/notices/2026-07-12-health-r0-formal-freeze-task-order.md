# 健康大管家 HM-R0 开发阶段正式冻结任务通知

- 通知状态：正式下达（模块工作项待最终基线同步后激活）
- 日期：2026-07-12
- 平台派发工作项：`AIW-20260712-HEALTH-R0-FORMAL-FREEZE-DISPATCH`
- 模块工作项：`AIW-20260712-HEALTH-R0-FORMAL-FREEZE`
- Owner：Health Manager module agent / 健康大管家负责人
- 分支：`codex/health-manager-r0-formal-freeze`
- 工作树：`C:/Users/shugo/Documents/worktrees/heaotang-health-r0-formal-freeze`

## 目标

把 HM-R0 / V1.0 Final Candidate 从“Technical Go / Professional Freeze Pending”收口为唯一、可追溯的 **Accepted for development planning**。该结论只允许后续开发规划，不等于生产医疗授权、真实身份/资质核验、真实健康数据、环境部署、收费或生产 Go。

## 已有事实与输入

1. Draft PR #1 的六个授权成果是原始候选，保持 Draft，未经本切片裁决不得自动合并。
2. Draft PR #2 是 MVP-90 PRD Review Candidate，保持独立，不因 HM-R0 冻结自动合并。
3. 已集成的 M0、M1、P2 synthetic 合同和验证结果只能作为当前开发事实对齐，不得反向把真实活动或生产门禁改为 Accepted。
4. 开发阶段专业审核结论仅在其已签署 scope/version 内引用；不得扩大到全量 C4-H06、真实会员或生产医疗服务。

## 授权范围

- 对齐 V1.0 产品宪法与当前 M0/M1/P2 synthetic 事实；
- 形成 `hm-r0-formal-freeze.v1` JSON/Schema 和人类可读冻结决定；
- 将 27 项决定按 `blocks-development`、`blocks-real-data-environment`、`does-not-block-synthetic` 分类；
- 每项保持 `Accepted`、`Exact revision` 或 `Pending with owner`，并记录 evidence、owner、复审触发；
- 明确唯一冻结状态、适用范围、失效条件、变更控制、receipt 与 Handoff；
- 明确 PR #1 保持 Draft、更新或申请受控合并的建议；PR #2 单独裁决。

## 精确允许路径

- `docs/project-management/modules/health-manager/health-manager-r0-formal-freeze-decision.md`
- `contracts/modules/health-manager/hm-r0-formal-freeze.v1.json`
- `contracts/modules/health-manager/hm-r0-formal-freeze.v1.schema.json`
- `contracts/modules/health-manager/development-checklists/2026-07-12-health-r0-formal-freeze*.json`
- `contracts/modules/health-manager/governance-exams/2026-07-12-health-r0-formal-freeze*.json`
- `contracts/modules/health-manager/implementation-records/2026-07-12-health-r0-formal-freeze*.json`

PR #1 的三份既有产品宪法/receipt/Handoff 是只读输入，仍由原 `AIW-20260711-HEALTH-V1-REQUIREMENTS-DOCS` 所有；本工作项不得修改。冻结结论通过新增 decision 与机器合同表达，待平台最终复核后再单独裁定是否更新或合并 PR #1。

## 明确禁止

- 业务代码、共享前后端、API、数据库和页面实现；
- 环境、部署、真实身份、真实会员/健康数据；
- 医疗服务、收费、资金、生产；
- 自动合并 PR #1/#2；
- 自动激活 P3 或其他技术切片；
- 用“开发规划冻结”替代生产身份/资质/组织授权门禁。

## 检查点

1. R0-F0：preflight、当前检查单、考试 100、receipt。
2. R0-F1：27 项分类、证据闭包、唯一冻结状态与 Schema 负例。
3. R0-F2：专业边界、风险升级、管理师准入/监督/容量、数据权利/特殊人群、15 风险底线和责任主体逐项审计。
4. R0-F3：PR 处置建议、变更控制、Handoff、独立平台复核。

模块必须短检查点提交；平台逐段独立复核。最终平台 Go 前不得把工作项标为 integrated。
