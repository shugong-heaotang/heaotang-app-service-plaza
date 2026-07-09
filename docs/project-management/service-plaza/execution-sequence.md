# 服务广场第一轮执行顺序清单

本文件按执行顺序排列第一轮联调前后的动作。当前项目按项目负责人决策、agent 协同和本地台账推进，不再使用多人外发、等回执、催办的执行链路。

## 一、执行顺序

| 顺序 | 动作 | 目标文件 | 处理角色 | 当前状态 |
| --- | --- | --- | --- | --- |
| 1 | 查看项目当前状态 | `project-status-one-page.md` | 规划 Agent | 已具备 |
| 2 | 读取第一批确认口径 | `communication-message-pack.md` | 规划 Agent、文档 Agent | 待执行 |
| 3 | 登记第一批确认批次 | `outbound-message-dispatch-log.md` | 文档 Agent | 待执行 |
| 4 | 登记 P0 确认事项状态 | `external-confirmation-tracker.md` | 文档 Agent | 待执行 |
| 5 | 登记 Day 0 执行结果并转换到启动确认动作 | `day-0-execution-record.md`、`day-0-to-kickoff-transition.md` | 文档 Agent、审计 Agent | 待执行 |
| 6 | 对未补齐事项设置补齐节奏 | `reply-followup-cadence.md` | 执行 Agent | 待执行 |
| 7 | 登记确认结果 | `reply-intake-tracker.md` | 文档 Agent | 待执行 |
| 8 | 按批次处理确认结果 | `reply-processing-batch-log.md` | 文档 Agent、审计 Agent | 待执行 |
| 9 | 进行本地启动确认并登记行动项 | `round-1-kickoff-meeting-minutes.md`、`kickoff-action-tracker.md` | 项目负责人、文档 Agent | 待执行 |
| 10 | 按启动确认到首次联调转换表复核结论 | `kickoff-to-first-integration-transition.md` | 审计 Agent | 待执行 |
| 11 | 按确认转换规则更新主动作、路由、账号、数据、Handoff | `reply-to-gate-transition.md`、多个台账文件 | 执行 Agent、文档 Agent | 待执行 |
| 12 | 复核 Handoff 是否合格，缺失则退回补齐 | `handoff-quality-review.md` | 审计 Agent | 待执行 |
| 13 | 对退回、缺证据、P0 阻塞进行补齐或裁决 | `blocker-escalation-decision-log.md` | 审计 Agent、项目负责人 | 待执行 |
| 14 | 复核首次真实联调 Go / Partial Go / No-Go | `first-integration-go-checklist.md` | 审计 Agent、项目负责人 | No-Go |
| 15 | 如果 Go 或 Partial Go，安排首次真实联调 | `round-1-integration-schedule.md` | 执行 Agent | 待执行 |
| 16 | 填写首次联调记录 | `round-1-integration-run-record.md` | 文档 Agent | 待执行 |
| 17 | 按首次联调到问题关闭转换表分流问题 | `first-integration-to-issue-closure-transition.md` | 审计 Agent | 待执行 |
| 18 | 关闭或延期主链路问题 | `round-1-issue-closure-tracker.md` | 执行 Agent、审计 Agent | 待执行 |
| 19 | 登记验收证据和缺证据回退动作 | `acceptance-evidence-register.md` | 文档 Agent、审计 Agent | 待执行 |
| 20 | 按联调到验收转换规则复核验收门禁 | `integration-to-acceptance-transition.md`、`phase-1-acceptance-checklist.md` | 审计 Agent、项目负责人 | No-Go |
| 21 | 填写第一阶段验收执行记录 | `phase-1-acceptance-run-record.md` | 文档 Agent | 待执行 |

## 二、当前卡点

| 卡点 | 处理方式 |
| --- | --- |
| agent 分工未形成确认记录 | 文档 Agent 补齐本地确认记录，项目负责人裁决 |
| 确认批次未登记 | 补 `outbound-message-dispatch-log.md`，否则不进入门禁解除 |
| 三大核心服务主动作未签核 | 执行 Agent 补齐主动作确认，项目负责人裁决 |
| 平台路由、账号、数据未确认 | 执行 Agent 补齐平台联调环境证据 |
| Handoff 信息不完整 | 用 Handoff 质量复核清单退回补齐 |
| 启动确认行动项未登记 | 补 `kickoff-action-tracker.md`，否则不解除门禁 |
| P0 阻塞未解决 | 登记阻塞补齐与裁决记录 |
| 首次真实联调 No-Go | 用确认转换规则和 Go 判定清单逐项解除 |

## 三、完成到什么程度才算进入下一步

| 下一步 | 必须满足 |
| --- | --- |
| 启动确认 | 材料已齐，完成第一批 P0 本地确认登记，并按 `day-0-to-kickoff-transition.md` 完成会前转换 |
| 首次真实联调 | 按 `kickoff-to-first-integration-transition.md` 完成启动确认后转换，Go 判定清单全部满足，且 Handoff 通过质量复核；或单板块 Partial Go |
| 问题关闭 | 首次联调记录已产生问题清单，并按 `first-integration-to-issue-closure-transition.md` 完成关闭、延期和裁决判断 |
| 第一阶段验收 | 主链路问题关闭或延期，验收前置证据和证据登记齐全，完成联调到验收转换，并填写 `phase-1-acceptance-run-record.md` |
