# Project Brain v2 M0 立项与 registry recovery 任务令

- 日期：2026-07-14
- recovery work item：`AIW-20260714-PROJECT-BRAIN-V2-REGISTRY-DISPATCH-RECOVERY`
- operations work item：`AIW-20260714-PROJECT-BRAIN-V2-OPERATIONS`
- 权威来源分支：`origin/codex/service-plaza-phase1-integration`
- frozen exact base：`09cbdc5d7f21c81e8bd3ddb52216392f68caa834`

## 1. 恢复授权与目的

原 `AIW-20260714-PROJECT-BRAIN-V2-REGISTRY-DISPATCH` 通道在创建治理工作树前等待系统审批超过 5 分钟，且其工作项从未进入权威 registry。项目最高负责人将本次**单一 registry-dispatch 执行权**转移给 recovery 负责人。

本检查点只完成两件事：

1. 登记 recovery 工作项并形成可审计的检查单、考试、实施记录和 Handoff 状态；
2. 将 Project Brain v2 operations 登记为 `planned`，冻结 M0 角色、路径、停止线与 M1–M5 No-Go。

这不是 v2 实现、验收、集成或生产授权。

## 2. 角色分离

| 职责 | 角色 |
| --- | --- |
| M0 developer | Project Brain v2 project owner |
| 独立 reviewer | independent Project Brain v2 reviewer |
| 最终 approver | 项目最高负责人 |
| registry 与受控集成 owner | 平台集成负责人 |
| 本检查点执行者 | 平台集成负责人授权的 registry-dispatch 恢复负责人 |

开发者不得自验收，reviewer 不得参与实现，approver 不由 developer 或 reviewer 代替，任何 registry 状态推进与最终集成均回到平台集成负责人。

## 3. Recovery 允许范围

- `contracts/foundation/agent-collaboration.v1.json`
- `docs/project-management/notices/2026-07-14-project-brain-v2-m0-task-order.md`
- `contracts/foundation/development-checklists/2026-07-14-project-brain-v2-registry-dispatch-recovery*.json`
- `contracts/foundation/governance-exams/2026-07-14-project-brain-v2-registry-dispatch-recovery*.json`
- `contracts/foundation/implementation-records/2026-07-14-project-brain-v2-registry-dispatch-recovery*.json`

原停滞工作树 `C:/Users/shugo/Documents/APP系统/.codex-worktrees/project-brain-v2-registry-dispatch` 只读，禁止修改、提交或推送。

## 4. Operations M0 精确允许范围

- `docs/project-management/notices/2026-07-14-project-brain-v2-operations-task-order.md`
- `docs/project-management/project-brain-v2/README.md`
- `docs/project-management/project-brain-v2/task-comprehension-receipt-m0.md`
- `docs/project-management/project-brain-v2/requirements-v2.md`
- `docs/project-management/project-brain-v2/architecture-v2.md`
- `docs/project-management/project-brain-v2/data-classification-v2.md`
- `docs/project-management/project-brain-v2/delivery-plan-v2.md`
- `docs/project-management/project-brain-v2/acceptance-v2.md`
- `docs/project-management/project-brain-v2/handoff-v2.md`
- `docs/decisions/0021-project-brain-v2-operational-read-model.md`
- `contracts/foundation/development-checklists/2026-07-14-project-brain-v2-m0*.json`
- `contracts/foundation/governance-exams/2026-07-14-project-brain-v2-m0*.json`
- `contracts/foundation/implementation-records/2026-07-14-project-brain-v2-m0*.json`

Operations 仍为 `planned`。平台集成负责人受控集成本 recovery 后，必须重新确认最新 exact base、工作树洁净、路径无冲突，并注册 `project-brain-v2` 治理 overlay，才可决定是否改为 `active`。

## 5. M0 目标与验收条件

M0 只冻结项目章程、需求边界、只读架构、数据分级、交付计划、验收标准、任务理解回执、ADR 和 Handoff。通过需同时满足：

1. Project Brain v1 仍是自身范围内的权威事实，v2 不复制或改写 v1 权威；
2. 每类经营事实只有一个权威来源，缺失、过期、冲突或审计失败均显示 `Unknown/No-Go`；
3. scheduler 与 dashboard 只读、不回写；生产默认关闭；代码集成不等于生产启用；
4. 数据分级至少覆盖项目治理、会员、健康、交易资金、商家、活动、客服；首期只允许治理事实和去标识汇总；
5. 行级会员、健康、交易、客服数据，真实数据、凭据、环境、部署和 production 保持禁止；
6. developer/reviewer/approver/integration owner 四类职责分离；
7. current checklist 完成、随机考试 100 分、实施记录和独立审查证据齐全。

## 6. M1–M5 No-Go 与明确排除

M1 经营事实合同必须等待 M0 独立 Go 后另行授权；M2 定时刷新、M3 生产级老板只读驾驶舱、M4 权限发布回滚、M5 独立验收与受控集成均保持 No-Go。

本任务禁止修改：

- `app/**` 与 `scripts/**`；
- recovery 明确范围外的 registry、foundation 或公共接口；
- `docs/project-management/project-brain/**` 及 `contracts/project-brain/**`（Project Brain v1）；
- 任何 SC remediation 文件；
- 数据库、后端、环境、部署、生产、真实数据、凭据或秘密。

## 7. 检查点与失败关闭

Recovery 必须依次完成 current checklist、考试 100 分、collaboration/schema/总合同/范围/UTF-8/秘密检查、freshness gate、实施记录、提交和仅推送 recovery 专用分支。任一门禁失败即停止；同一命令连续失败两次立即升级，不得弱化标准或改写失败证据。

Recovery 完成后只可转为 `handoff-ready`，不得自行集成。Operations 继续保持 `planned`。
