# Project Brain v2 经营管理接入 M0 治理冻结任务令

- 日期：2026-07-15
- work item：`AIW-20260714-PROJECT-BRAIN-V2-OPERATIONS`
- record：`IR-20260714-PROJECT-BRAIN-V2-M0`
- resumed authority：`a47bbbacae21596be6511b70539d92f0666715a5`
- 工作树：`C:/Users/shugo/Documents/APP系统/.codex-worktrees/project-brain-v2-operations`
- 分支：`codex/project-brain-v2-operations`

## 1. 唯一目标

M0 只冻结 Project Brain v2 的项目章程、角色分离、范围、只读架构、数据分级、交付里程碑、验收标准、ADR 和 Handoff。M0 不接入数据、不实现调度器或驾驶舱、不修改 Project Brain v1，也不授权环境、部署或生产。

## 2. 角色与决策权

| 角色 | 责任 | 禁止事项 |
| --- | --- | --- |
| 项目最高负责人 | 业务目标、风险偏好、最终批准 | 不以口头批准替代证据门禁 |
| Project Brain v2 项目负责人 | M0 需求、架构和交付证据 | 不自验收、不改 registry |
| 独立验收负责人 | 按冻结标准给出 Go/No-Go | 不参与实现、不降低标准 |
| 平台集成负责人 | registry、受控集成与权威 freshness | 不代替业务验收、不启用生产 |
| 数据/业务事实 Owner | 声明事实含义、权威来源、时效与质量 | 不向 Brain 让渡源系统写权 |
| 安全与发布审批者 | M4 权限、审计、发布、回滚授权 | 与开发、验收保持职责分离 |

## 3. 硬边界

- Project Brain v1 在其既有范围内继续是权威；v2 只能引用，不得复制、改写或制造第二权威。
- 首期仅允许项目治理事实与通过分级、最小化、阈值和去标识审查的经营聚合。
- 行级会员、健康、交易资金、客服数据一律禁止；M0 也禁止任何真实数据。
- scheduler 与 dashboard 必须只读、无回写能力；来源缺失、过期、冲突或质量失败时输出 `Unknown/No-Go`。
- production routes、snapshots、jobs、dashboard 全部默认关闭；代码集成不等于生产启用。
- M1-M5 必须逐阶段另行授权、独立验收和受控集成，不得借 M0 前移。

## 4. 完成条件

起飞 checklist current、考试 100、十份治理内容齐全、ADR0021 可审计、IR verified、总合同/UTF-8/scope/secret/freshness 通过，并由独立 reviewer 接收 Handoff。候选提交和推送不等于集成或生产授权。
