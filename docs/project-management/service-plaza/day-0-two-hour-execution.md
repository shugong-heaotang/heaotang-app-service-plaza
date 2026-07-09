# 服务广场 Day 0 两小时执行清单

本文件用于今天立即推进服务广场第一轮联调启动。目标是在 2 小时内完成第一批 P0 本地确认、证据登记、启动确认准备和当日门禁复核。

执行完成后，必须填写 `day-0-execution-record.md`。未填写执行记录时，Day 0 不视为完成。

## 一、2 小时目标

| 目标 | 完成标准 |
| --- | --- |
| 第一批 P0 确认完成登记 | `outbound-message-dispatch-log.md` 和 `external-confirmation-tracker.md` 均更新为确认批次和确认状态 |
| 启动确认进入准备 | 项目负责人可基于 `round-1-kickoff-invitation.md` 做本地启动确认 |
| 确认结果收口路径明确 | 所有确认结果进入 `reply-intake-tracker.md` |
| 当日门禁复核完成 | `phase-gate-status.md`、`first-integration-go-checklist.md` 结论保持一致 |

## 二、执行顺序

| 顺序 | 时间 | 动作 | 文件 | 处理角色 |
| --- | --- | --- | --- | --- |
| 1 | 0-10 分钟 | 打开项目状态和阶段报告，确认当前口径 | `project-status-one-page.md`、`phase-progress-report.md` | 规划 Agent |
| 2 | 10-25 分钟 | 读取第一批确认口径 | `communication-message-pack.md` | 规划 Agent、文档 Agent |
| 3 | 25-40 分钟 | 逐项做本地确认判断，不能确认的标为待补齐 | `external-confirmation-tracker.md` | 项目负责人、审计 Agent |
| 4 | 40-55 分钟 | 登记确认批次和确认状态 | `outbound-message-dispatch-log.md`、`external-confirmation-tracker.md` | 文档 Agent |
| 5 | 55-75 分钟 | 准备第一轮联调启动确认 | `round-1-kickoff-invitation.md` | 规划 Agent、文档 Agent |
| 6 | 75-90 分钟 | 登记已有确认结果 | `reply-intake-tracker.md` | 文档 Agent |
| 7 | 90-105 分钟 | 检查信息不完整或缺证据高风险项 | `reply-followup-cadence.md`、`blocker-escalation-decision-log.md` | 审计 Agent |
| 8 | 105-120 分钟 | 做当日门禁和一致性审计 | `first-integration-go-checklist.md`、`phase-gate-status.md`、`consistency-and-gate-audit.md` | 审计 Agent、项目负责人 |

## 三、第一批必须确认事项

| 确认事项 | 目的 | 证据来源 |
| --- | --- | --- |
| 项目负责人裁决机制 | 确认本项目按单人决策推进 | `communication-message-pack.md`、`agent-coordination-board.md` |
| Agent 分工 | 确认规划、执行、文档、审计 Agent 分工 | `collaboration-tool-setup.md` |
| 第一轮范围 | 确认服务广场总入口和三大核心服务进入第一轮 | `round-1-readiness-report.md` |
| 三大核心服务主动作 | 确认主动作、页面策略、Handoff 和验收口径 | `core-service-main-action-confirmation.md` |
| 平台条件 | 确认路由、环境、账号、数据、权限和联调条件 | `routing-and-temporary-page-spec.md`、`test-accounts-and-data.md` |
| Handoff 状态 | 确认三大核心服务首轮 Handoff 是否可复核 | `round-1-handoff-forms.md`、`handoff-quality-review.md` |
| 验收责任和证据 | 确认第一阶段验收前置证据 | `acceptance-evidence-register.md` |

## 四、2 小时结束时必须更新

| 文件 | 必须更新内容 |
| --- | --- |
| `outbound-message-dispatch-log.md` | 第一批确认事项、确认方式、确认时间、证据编号 |
| `external-confirmation-tracker.md` | EXT-001 至 EXT-008 的确认状态 |
| `reply-intake-tracker.md` | 已形成的确认结果 |
| `reply-followup-cadence.md` | 待补齐事项的下一次处理时间 |
| `phase-gate-status.md` | 当日 Go / No-Go 结论 |
| `consistency-and-gate-audit.md` | 当日一致性审计结论 |
| `day-0-execution-record.md` | Day 0 实际完成情况、确认结果、证据和门禁复核 |

## 五、2 小时结束时的预期结论

如果只是完成本地确认登记，预期结论仍然是：

| 阶段 | 预期判断 | 原因 |
| --- | --- | --- |
| 第一轮联调启动确认 | Go | 材料已齐，可继续补齐台账证据 |
| 首次真实联调 | No-Go | 等待真实 Handoff 复核、账号数据和路由证据 |
| 第一阶段验收 | No-Go | 尚无联调记录和验收证据 |

## 六、禁止事项

- 不重新讨论服务广场架构。
- 不把未形成证据的事项口头视为已确认。
- 不在未登记确认批次的情况下解除门禁。
- 不在 Handoff 未通过质量复核时启动真实联调。
- 不在无联调记录和证据登记时进入验收。
