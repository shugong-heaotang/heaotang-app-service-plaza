# 服务广场启动确认到首次真实联调转换表

日期：2026-07-09

本文件用于把第一轮联调启动确认结论转换为首次真实联调动作。启动确认结束后，审计 Agent 必须按本表判断：哪些事项已经解除门禁，哪些事项仍需行动项补齐，哪些板块可以 Partial Go，哪些阻塞必须提交项目负责人裁决。

## 一、转换结论

| 项目 | 当前状态 | 结论 |
| --- | --- | --- |
| 第一轮联调启动会 | 未真实召开 | 尚无真实会议结论 |
| 本地启动确认 | 未完成 | `kickoff-action-tracker.md` 仍为框架 |
| Handoff 质量复核 | 未通过 | 三大核心服务均待复核 |
| 首次真实联调 | No-Go | 主动作、路由、账号、数据、Handoff 仍缺事实证据 |
| 单板块 Partial Go | No-Go | 任一板块均未满足完整条件 |

## 二、输入文件

| 输入 | 用途 |
| --- | --- |
| `round-1-kickoff-meeting-minutes.md` | 提取启动确认真实结论 |
| `kickoff-action-tracker.md` | 跟踪 P0 行动项和关闭标准 |
| `post-kickoff-update-actions.md` | 确认启动确认后应回写的目标台账 |
| `round-1-signoff-checklist.md` | 判断签核结论是否成立 |
| `handoff-quality-review.md` | 判断 Handoff 是否解除联调门禁 |
| `first-integration-go-checklist.md` | 输出 Go / Partial Go / No-Go |
| `phase-gate-status.md` | 回写阶段门禁 |

## 三、启动确认后 2 小时内必须完成

| 顺序 | 动作 | 处理角色 | 目标文件 | 未完成后果 |
| --- | --- | --- | --- | --- |
| 1 | 填写启动确认纪要 | 文档 Agent | `round-1-kickoff-meeting-minutes.md` | 确认结论不作为门禁依据 |
| 2 | 登记行动项 | 文档 Agent | `kickoff-action-tracker.md` | 后续事项不能关闭 |
| 3 | 回写项目负责人裁决和签核结论 | 文档 Agent、项目负责人 | `owner-roster.md`、`round-1-signoff-checklist.md` | 基础门禁不解除 |
| 4 | 回写主动作和页面方案 | 执行 Agent | `core-service-main-action-confirmation.md`、`routing-and-temporary-page-spec.md` | 板块不能进入 Partial Go |
| 5 | 回写账号、数据、平台范围 | 执行 Agent | `integration-checklist.md`、`test-accounts-and-data.md` | 不能安排真实联调 |
| 6 | 复核 Handoff | 审计 Agent | `handoff-quality-review.md`、`handoff-log.md` | Handoff 不解除门禁 |
| 7 | 复核首次联调门禁 | 审计 Agent、项目负责人 | `first-integration-go-checklist.md`、`phase-gate-status.md` | 仍保持 No-Go |

## 四、转换规则

| 启动确认后状态 | 判断条件 | 转换动作 | 目标文件 |
| --- | --- | --- | --- |
| 会议未真实召开 | 无会议日期、参会人、结论 | 不允许用会议口径解除任何门禁 | `phase-gate-status.md` |
| 本地确认未完成 | 无确认日期、裁决结论、证据编号 | 先补本地确认，不进入联调 | `round-1-kickoff-meeting-minutes.md` |
| 确认已完成但行动项未登记 | 纪要有结论，本表无行动项 | 先补行动项，不进入联调 | `kickoff-action-tracker.md` |
| 行动项已登记但目标台账未回写 | 行动项存在，目标文件仍待确认 | 行动项不能关闭 | `post-kickoff-update-actions.md` |
| 主动作已确认 | 主动作签核完整且有证据编号 | 解除对应基础阻塞 | `core-service-main-action-confirmation.md` |
| 平台条件已确认 | 路由、权限、账号、数据完整 | 解除平台联调阻塞 | `integration-checklist.md`、`test-accounts-and-data.md` |
| Handoff 通过复核 | 必填字段完整，平台接收条件明确 | 解除对应板块 Handoff 阻塞 | `handoff-quality-review.md` |
| Handoff 信息不完整 | 任一必填字段缺失 | 退回补齐，必要时裁决 | `issue-pool.md`、`blocker-escalation-decision-log.md` |
| 单板块条件完整 | 某板块主动作、路由、账号、数据、Handoff 全部满足 | 该板块可进入 Partial Go | `first-integration-go-checklist.md` |
| 三板块条件完整 | 三大核心服务全部满足 Go 条件 | 首次真实联调整体 Go | `phase-gate-status.md`、`round-1-integration-schedule.md` |

## 五、单板块 Partial Go 判定表

| 板块 | 主动作 | 路由或临时页 | 账号数据 | Handoff 复核 | 当前判定 |
| --- | --- | --- | --- | --- | --- |
| 生命导航 | 未确认 | 未确认 | 未准备 | 未通过 | No-Go |
| 俱乐部联盟 | 未确认 | 未确认 | 未准备 | 未通过 | No-Go |
| 健康大管家 | 未确认 | 未确认 | 未准备 | 未通过 | No-Go |

## 六、首次真实联调安排条件

只有满足以下任一条件，执行 Agent 才能登记首次真实联调安排：

1. 整体 Go：三大核心服务全部满足主动作、路由、账号、数据和 Handoff 复核条件。
2. Partial Go：至少一个核心服务完整满足条件，其他板块阻塞已登记并不影响该板块联调。

不满足以上条件时，不得只凭会议口头结论或本地意向安排真实联调。

## 七、输出文件更新顺序

| 顺序 | 动作 | 文件 |
| --- | --- | --- |
| 1 | 填写启动确认结论 | `round-1-kickoff-meeting-minutes.md` |
| 2 | 登记行动项和关闭标准 | `kickoff-action-tracker.md` |
| 3 | 回写启动确认后台账 | `post-kickoff-update-actions.md` |
| 4 | 复核 Handoff | `handoff-quality-review.md` |
| 5 | 更新问题和裁决事项 | `issue-pool.md`、`blocker-escalation-decision-log.md` |
| 6 | 复核首次联调 Go / Partial Go / No-Go | `first-integration-go-checklist.md` |
| 7 | 回写阶段门禁 | `phase-gate-status.md` |
| 8 | 如 Go 或 Partial Go，安排首次真实联调 | `round-1-integration-schedule.md` |

## 八、当前结论

截至 2026-07-09，第一轮联调启动会尚未真实召开，本地启动确认也尚未形成事实证据。当前不能安排首次真实联调，只能继续推进 Day 0 确认、启动确认准备、行动项登记和门禁证据闭环。
