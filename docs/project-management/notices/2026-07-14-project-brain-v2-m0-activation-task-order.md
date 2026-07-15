# Project Brain v2 M0 合法激活任务令

- 日期：2026-07-14
- activation work item：`AIW-20260714-PROJECT-BRAIN-V2-M0-ACTIVATION`
- operations work item：`AIW-20260714-PROJECT-BRAIN-V2-OPERATIONS`
- 权威来源：`origin/codex/service-plaza-phase1-integration`
- frozen exact base：`36b245871dd95d53964fb20cf4c30a05ceb89a77`

## 1. 唯一目标

本检查点只完成 Project Brain v2 operations 从 `planned` 到 `active` 的合法激活：确认最新权威基线、创建干净专用工作树、复核路径互斥、更新协作 registry，并形成 activation 自身的 current checklist、100 分治理考试、实施记录和可审计交接证据。

本检查点不实现 M0 章程、需求、架构、数据分级、验收或 ADR 内容；这些内容只允许由 operations 工作项负责人在本激活分支推送并经平台受控集成后开始。

## 2. 角色分离

| 职责 | 角色 |
| --- | --- |
| activation developer | Project Brain v2 M0 activation dispatch agent |
| M0 developer | Project Brain v2 project owner |
| independent reviewer | independent Project Brain v2 reviewer |
| approver | 项目最高负责人 |
| registry 与 integration owner | 平台集成负责人 |

activation 执行者不实现 M0、不做 M0 独立验收，也不得自行把 activation 或 operations 标为 integrated。

## 3. 权威与工作树证据

- 2026-07-14 执行前已 `fetch` 并确认远端 exact HEAD 为 `36b245871dd95d53964fb20cf4c30a05ceb89a77`。
- activation 工作树：`C:/Users/shugo/Documents/APP系统/.codex-worktrees/project-brain-v2-m0-activation`
- activation 分支：`codex/project-brain-v2-m0-activation`
- operations 工作树：`C:/Users/shugo/Documents/APP系统/.codex-worktrees/project-brain-v2-operations`
- operations 分支：`codex/project-brain-v2-operations`
- 两个工作树均从 exact base 创建，创建时 clean；operations 工作树在本检查点保持只读且不得产生任何文件变更。
- operations 原 M0 allowed paths 与当时 15 个 `active`、`handoff-ready` 或 `blocked` 工作项的活动范围复核为 0 冲突；目标 workspace 复核为 0 冲突。

## 4. Activation 允许范围

- `contracts/foundation/agent-collaboration.v1.json`
- `docs/project-management/notices/2026-07-14-project-brain-v2-m0-activation-task-order.md`
- `contracts/foundation/development-checklists/2026-07-14-project-brain-v2-m0-activation*.json`
- `contracts/foundation/governance-exams/2026-07-14-project-brain-v2-m0-activation*.json`
- `contracts/foundation/implementation-records/2026-07-14-project-brain-v2-m0-activation*.json`

## 5. Operations 激活边界

Operations 只保留 `AIW-20260714-PROJECT-BRAIN-V2-OPERATIONS` 已登记的 M0 allowed paths，不新增、不扩张。`base_commit` 更新为本任务的 exact base，`started_with_clean_worktree=true`，`preexisting_changes_acknowledged=false`。

激活只授权 M0 治理冻结。M1 去标识经营事实合同必须等待 M0 独立 Go 后另立工作项；M2 定时刷新、M3 生产级老板只读驾驶舱、M4 权限发布回滚、M5 独立验收与受控集成继续 No-Go。

## 6. 禁止范围与停止条件

禁止修改或触达：

- operations 工作树内的任何文件；
- `app/**`、`scripts/**`、数据库、后端、环境、部署与 production；
- `docs/project-management/project-brain/**`、`contracts/project-brain/**` 等 Project Brain v1 权威文件；
- SC remediation 文件；
- 行级会员、健康、交易、客服数据，以及任何真实数据、凭据或秘密。

远端不再精确等于 frozen base、工作树不洁净、branch/base 不符、路径冲突、治理门禁失败或需要扩大权限时立即失败关闭。同一命令连续失败两次立即升级，禁止弱化标准。

## 7. 完成门禁

依次要求：

1. APP preflight 通过；
2. activation 与 operations bootstrap dry-run 通过或对纯治理工作给出明确的依赖非适用证据；
3. activation current checklist 完成；
4. 随机治理考试 100 分；
5. implementation record 与本 record/checklist/exam 一致；
6. collaboration/schema、总合同、UTF-8、scope、secret 和 freshness 门禁通过；
7. operations 工作树仍 clean、HEAD/branch/base 精确；
8. activation 状态仅推进到 `handoff-ready`；
9. 仅提交并推送 activation 专用分支，不集成、不部署。

## 8. Handoff

- `blocks`：operations M0 开始治理冻结。
- `does_not_block`：Project Brain v1、SC remediation 和其他隔离工作项。
- activation 下一动作：由独立 Project Brain v2 reviewer 复核 activation 提交，再由平台集成负责人执行受控集成。
- operations 下一检查点：完成 M0 任务理解回执、项目章程、只读架构、数据分级、交付计划、验收标准、ADR 与 Handoff，并提交独立验收。
- 生产、真实数据、环境和部署授权：无。
