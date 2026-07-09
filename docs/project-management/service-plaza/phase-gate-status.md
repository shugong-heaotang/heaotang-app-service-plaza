# 服务广场阶段门禁状态

本文件用于判断服务广场从准备、启动会、首次联调、问题关闭到第一阶段验收的门禁状态。

## 一、阶段门禁

| 阶段 | 进入条件 | 当前状态 | 判断 |
| --- | --- | --- | --- |
| 准备阶段 | 架构定版、推进方案、台账建立 | 已完成 | Go |
| 启动会阶段 | 签核清单、启动会纪要、Handoff 表单、启动会行动项跟踪表准备完成 | 已完成 | Go |
| 首次联调阶段 | 负责人、主动作、路由、账号、数据确认，Handoff 通过质量复核，并按确认转换规则复核 | 未完成 | No-Go |
| 问题关闭阶段 | 首次联调完成并产生问题清单 | 未开始 | No-Go |
| 第一阶段验收 | 联调记录完整、主链路问题关闭或延期、验收证据登记齐全，并完成联调到验收转换 | 未开始 | No-Go |

## 二、当前可执行动作

| 动作 | 是否可执行 | 说明 |
| --- | --- | --- |
| 确认第一轮联调启动会准备 | 是 | 材料已齐，可先完成启动会准备确认 |
| 正式召开第一轮联调启动会 | 是 | 正式召开前必须完成 Day 0 确认登记和 `day-0-to-kickoff-transition.md` 会前转换判断 |
| 执行 Day 0 确认控制 | 是 | 按 `day-0-dispatch-control.md` 完成确认前核对、确认后回写和补齐设置 |
| 完成 Day 0 到启动会转换判断 | 是 | Day 0 确认后按 `day-0-to-kickoff-transition.md` 判断确认、补齐、裁决和启动会动作 |
| 复核确认完整性 | 是 | 形成确认结果后必须先按 `reply-completeness-review.md` 判断完整性，再进入门禁转换 |
| 执行确认回写清单 | 是 | 完整确认结果必须先按 `reply-ledger-update-checklist.md` 回写目标台账，再进入 Go / Partial Go / No-Go 判断 |
| 登记启动会行动项 | 是 | 启动会后必须更新 `kickoff-action-tracker.md` |
| 复核阶段门禁证据矩阵 | 是 | 门禁变化前后必须按 `phase-gate-evidence-matrix.md` 检查证据充分性 |
| 完成启动会到首次真实联调转换判断 | 是 | 启动会后按 `kickoff-to-first-integration-transition.md` 判断 Go / Partial Go / No-Go |
| 平台准备临时承接页 | 是 | ADR 0003 已允许 |
| 平台准备测试账号和数据 | 是 | 清单已建立 |
| 三大板块提交 Handoff | 是 | 表单和运行机制已建立，必须按 `handoff-operating-mechanism.md` 执行 |
| 启动首次真实联调 | 否 | 仍缺负责人、测试准备签核和 Handoff 质量复核 |
| 启动单板块 Partial Go 联调 | 否 | 任一核心服务均尚未满足负责人、主动作、路由、账号、数据和 Handoff 质量复核条件 |
| 完成首次联调到问题关闭转换判断 | 否 | 尚无真实联调记录；联调后必须按 `first-integration-to-issue-closure-transition.md` 判断问题关闭、延期和升级 |
| 进入验收 | 否 | 尚无联调证据 |
| 填写第一阶段验收执行记录 | 否 | 尚未进入验收；进入验收后必须填写 `phase-1-acceptance-run-record.md` |
| 升级 P0 阻塞 | 是 | 已登记第一次缺口检查和阻塞映射；事实证据仍缺时继续按 `blocker-escalation-decision-log.md` 跟踪 |

## 三、门禁解除条件

| No-Go 项 | 解除条件 | 目标文件 |
| --- | --- | --- |
| 首次联调 No-Go | 签核清单通过，负责人、主动作、路由、账号、数据均确认；FE-PLAT、FE-MOD、FE-HO 均按总控顺序提交并通过复核；Handoff 按运行机制提交并通过质量复核；并完成确认完整性复核、逐条台账回写、确认到门禁转换和启动会后转换判断 | `fact-evidence-submission-control-board.md`、`platform-fact-submission-action-pack.md`、`module-fact-submission-action-pack.md`、`handoff-completion-action-pack.md`、`fact-evidence-submission-packet.md`、`fact-evidence-intake-review.md`、`round-1-signoff-checklist.md`、`reply-completeness-review.md`、`reply-ledger-update-checklist.md`、`reply-to-gate-transition.md`、`kickoff-to-first-integration-transition.md`、`handoff-operating-mechanism.md`、`handoff-quality-review.md` |
| 问题关闭 No-Go | 首次联调记录完成，新增问题进入问题关闭跟踪表，并完成问题关闭、延期和升级转换判断 | `round-1-integration-run-record.md`、`first-integration-to-issue-closure-transition.md`、`round-1-issue-closure-tracker.md` |
| 第一阶段验收 No-Go | 主链路阻塞问题关闭或延期，FE-GATE 和 FE-ACC 已按总控顺序完成复核，验收前置证据和证据登记齐全，完成联调到验收转换，并填写验收执行记录和签核结论 | `fact-evidence-submission-control-board.md`、`fact-evidence-review-run-log.md`、`integration-to-acceptance-transition.md`、`acceptance-evidence-register.md`、`phase-1-acceptance-checklist.md`、`phase-1-acceptance-run-record.md` |

## 四、升级记录

任何门禁从 Go 退回 No-Go，或长期 No-Go 需要裁决时，必须登记到 `blocker-escalation-decision-log.md`，并在裁决后更新本文件。
