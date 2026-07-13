# 健康大管家 HM-R0 R0-F2 专业与责任边界审计任务书

状态：正式派发文件已生成；模块工作项在专用工作树核验完成并由 activation commit 标记 active 后方可编辑。

## 目标

以已 Go 的 R0-F1 开发规划冻结为输入，逐项审计以下六类边界，并形成结构化、可复核的证据包：

1. AI、健康管理师、医生及医生集团的专业允许/禁止动作；
2. 风险识别、停止、升级、紧急引导、转人工和责任交接；
3. 健康管理师准入、资格、监督、负荷与容量；
4. 健康数据权利、授权撤回、最小访问、特殊人群与失败关闭；
5. MVP-A001—A015 的 15 项风险底线；
6. 产品、专业、平台、隐私法律、运营商业各责任主体和会签关系。

F2 的交付是“审计结论和缺口”，不是业务实现。没有相应 owner 的新书面证据时，任何 `Pending with owner` 不得改为 `Accepted`；证据不足时必须记录唯一 owner、missing evidence、blocks、does_not_block 和 next checkpoint。

## 工作项

- work_id: `AIW-20260713-HEALTH-R0-F2-AUDIT`
- owner: `Health Manager module agent`
- owner_role: `健康大管家负责人`
- repository: `C:/Users/shugo/Documents/APP系统`
- branch: `codex/health-manager-r0-f2-audit`
- worktree: `C:/Users/shugo/Documents/worktrees/heaotang-health-r0-f2-audit`
- base: 以包含本任务书、平台注册与 activation 的最终权威 HEAD 为准；激活通知必须回传 exact SHA。

## 精确允许路径

- `docs/project-management/modules/health-manager/health-manager-r0-formal-freeze-decision.md`
- `docs/project-management/modules/health-manager/health-manager-r0-f2-audit.md`
- `docs/project-management/modules/health-manager/health-manager-r0-f2-task-receipt.md`
- `docs/project-management/modules/health-manager/health-manager-r0-f2-handoff.md`
- `contracts/modules/health-manager/hm-r0-formal-freeze.v1.json`
- `contracts/modules/health-manager/hm-r0-formal-freeze.v1.schema.json`
- `contracts/modules/health-manager/hm-r0-f2-audit.v1.json`
- `contracts/modules/health-manager/hm-r0-f2-audit.v1.schema.json`
- `contracts/modules/health-manager/development-checklists/2026-07-13-health-r0-f2-audit*.json`
- `contracts/modules/health-manager/governance-exams/2026-07-13-health-r0-f2-audit*.json`
- `contracts/modules/health-manager/implementation-records/2026-07-13-health-r0-f2-audit*.json`

不得修改 F1 历史 checklist/exam/IR，不得修改 PR #1/#2 原成果，不得进入共享代码路径。

## 两层依赖

平台层：权威 integration 已完成健康/商城分叉调和，协作 registry、治理考试、实施记录、UTF-8 与总合同门禁可用。

模块层：

- R0-F1 source `384436c719396d0a0105f448716ef37aa8ba7ab8` 已独立 Go；
- F1 受控合并 `fb1b882091209897d9f618659ce02733d670b53e`，最终 F1 权威收口 `034e46beae3dd30d5616c873d596e9c591c8d797`；
- F1 只冻结开发规划，`executable=false`；
- F2 可以审计 Pending，但不得因“开始审计”而提升 Pending；
- F2 审计未完成前，R0-F3 与 P3 均 No-Go。

## 短检查点

1. F2-0：preflight、current checklist、考试 100、receipt、现有 27 项证据索引。
2. F2-1：六类审计矩阵与 JSON/Schema；每项 owner、证据、缺口、blocks/does_not_block 完整。
3. F2-2：证据引用与状态负例；擅自提升 Pending、删除 owner、扩大范围、设置 executable、授权真实活动必须失败。
4. F2-3：Handoff 与平台独立复核。F2 Go 只证明审计包完整，不自动进入 F3/P3。

## 持续禁止

禁止 F3/P3、业务代码、共享前后端、API/数据库、真实身份/会员/健康数据、医疗服务、收费、资金、环境、部署和生产。禁止把开发阶段审核人身份外推为生产医疗或法律授权。
