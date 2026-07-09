# 服务广场第一轮联调会前材料核对清单

本清单用于第一轮联调启动确认前检查。当前项目按单人决策和 agent 协同推进，因此“会前”指本地确认前的材料核对，不要求多人参会或外部回执。

## 一、会前材料

| 材料 | 文件 | 是否必须 | 状态 | 处理角色 |
| --- | --- | --- | --- | --- |
| 准备度报告 | `round-1-readiness-report.md` | 是 | 已具备，待按证据更新 | 审计 Agent |
| 阶段门禁状态 | `phase-gate-status.md` | 是 | 已具备，首次真实联调 No-Go | 审计 Agent |
| 签核清单 | `round-1-signoff-checklist.md` | 是 | 已具备，待项目负责人裁决 | 项目负责人 |
| 启动会纪要模板 | `round-1-kickoff-meeting-minutes.md` | 是 | 已具备，待真实填写 | 文档 Agent |
| 项目分工口径 | `owner-roster.md` | 是 | 已具备，待改为 agent 分工证据 | 文档 Agent |
| 主动作确认表 | `core-service-main-action-confirmation.md` | 是 | 已具备，待补齐证据 | 执行 Agent |
| 首轮 Handoff 表单 | `round-1-handoff-forms.md` | 是 | 已具备，待真实提交 | 文档 Agent |
| 路由与临时承接页规格 | `routing-and-temporary-page-spec.md` | 是 | 已具备，待平台条件证据 | 执行 Agent |
| 测试账号与测试数据清单 | `test-accounts-and-data.md` | 是 | 已具备，待真实账号和数据 | 执行 Agent |
| 首次联调记录 | `round-1-integration-run-record.md` | 否 | 已具备，待联调后填写 | 文档 Agent |
| 问题关闭跟踪表 | `round-1-issue-closure-tracker.md` | 否 | 已具备，待联调后填写 | 文档 Agent |

## 二、本地确认前必须检查的问题

| 编号 | 问题 | 默认处理 | 是否必须确认 |
| --- | --- | --- | --- |
| PRE-Q001 | 项目负责人是否作为最终裁决人 | 默认由项目负责人裁决 | 是 |
| PRE-Q002 | 规划 Agent、执行 Agent、文档 Agent、审计 Agent 是否分工明确 | 未明确前不得解除门禁 | 是 |
| PRE-Q003 | 三大核心服务主动作是否可作为第一阶段范围 | 默认采用推荐主动作，待证据确认 | 是 |
| PRE-Q004 | 是否采用临时承接页 | 允许采用，见 ADR 0003 | 是 |
| PRE-Q005 | 测试账号和测试数据是否已有真实证据 | 无证据时保持 No-Go | 是 |
| PRE-Q006 | Handoff 是否真实提交并通过复核 | 未通过时保持 No-Go | 是 |

## 三、会前结论模板

```text
材料是否齐全：是 / 否
是否可以进行本地启动确认：是 / 否
必须当场确认的问题：
确认后必须补齐的问题：
是否允许启动首次真实联调：否
No-Go 原因：
```

## 四、当前结论

材料模板已齐，可以进行本地启动确认；但真实确认记录、Handoff、平台条件、账号数据和联调证据尚未形成。首次真实联调保持 No-Go。
