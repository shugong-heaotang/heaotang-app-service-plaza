# 服务广场事实证据下一轮批次执行单

日期：2026-07-10

本文件用于把下一轮事实证据推进压缩成可直接执行的批次。它只定义批次顺序、输入字段、提交包、接收复核和退回条件，不替代真实事实证据。

## 一、批次原则

1. 下一轮只推进 FE-PLAT、FE-MOD、FE-HO 三类前置事实，不触发 FE-GATE 和 FE-ACC。
2. FE-GATE-001 只能在 FE-PLAT、FE-MOD、FE-HO 通过必要复核后触发。
3. FE-ACC-011 至 FE-ACC-013 只能在真实联调、问题关闭和验收触发条件形成后触发。
4. 每个批次必须先填写 `fact-evidence-submission-packet.md`，再回写 `fact-evidence-intake-review.md`，最后由 `fact-evidence-review-run-log.md` 记录复核动作。
5. 原型、规范、计划、台账和口头说明不能作为可接收事实。

## 二、下一轮批次总表

| 批次 | 范围 | 目标 | 提交包 | 接收和复核 | 当前状态 |
| --- | --- | --- | --- | --- | --- |
| FE-BATCH-001 | FE-PLAT-001 至 FE-PLAT-005 | 补齐平台环境、路由、权限、账号、数据和返回路径事实 | `fact-evidence-submission-packet.md` 平台事实提交包 | `fact-evidence-intake-review.md`、`fact-evidence-review-run-log.md` | 已核查未接收，见 `fact-evidence-next-batch-run-record.md` |
| FE-BATCH-002 | FE-MOD-001 至 FE-MOD-003 | 补齐三大核心服务主动作、页面、权限、后台处理、测试数据和验收责任事实 | `fact-evidence-submission-packet.md` 板块事实提交包 | `fact-evidence-intake-review.md`、`fact-evidence-review-run-log.md` | 已核查未接收，见 `module-fact-evidence-run-record.md` 和 `fact-evidence-next-batch-run-record.md` |
| FE-BATCH-003 | FE-HO-001 至 FE-HO-003 | 基于板块事实补齐三大核心服务 Handoff、平台接收和质量复核事实 | `fact-evidence-submission-packet.md` Handoff 事实提交包 | `handoff-quality-review.md`、`fact-evidence-intake-review.md`、`fact-evidence-review-run-log.md` | 已核查未接收，见 `handoff-fact-evidence-run-record.md` 和 `fact-evidence-next-batch-run-record.md` |
| FE-BATCH-004 | FE-GATE-001 | 复核首次真实联调 Go / Partial Go / No-Go | `fact-evidence-submission-packet.md` 门禁事实提交包 | `fact-evidence-review-run-log.md`、`phase-gate-evidence-matrix.md`、`phase-gate-status.md` | 已核查但不触发，见 `gate-fact-evidence-run-record.md` 和 `fact-evidence-next-batch-run-record.md` |
| FE-BATCH-005 | FE-ACC-011 至 FE-ACC-013 | 复核第一阶段验收执行、裁决和 Go / No-Go | `fact-evidence-submission-packet.md` 验收事实提交包 | `fact-evidence-review-run-log.md`、`acceptance-evidence-register.md` | 已核查但不触发，见 `acceptance-fact-evidence-run-record.md` 和 `fact-evidence-next-batch-run-record.md` |

## 三、FE-BATCH-001 平台事实

| FE 项 | 必填事实 | 不可接收内容 | 退回路径 |
| --- | --- | --- | --- |
| FE-PLAT-001 | 环境名称、环境地址、服务广场入口、三大核心服务正式路由或临时承接页、第一轮采用方案 | 只有原型图、页面设想或待开发说明 | ESC-004 |
| FE-PLAT-002 | 未登录、普通会员、无权限、管理或审核权限规则，以及每类权限预期页面状态 | 只有“后续补权限”或原则描述 | ESC-004 |
| FE-PLAT-003 | 账号类型、获取方式、测试环境、安全保管方式、可用状态；不得记录真实密码 | 生产账号、真实密码、无法确认保管方式 | ESC-004 |
| FE-PLAT-004 | 三大核心服务正常、空状态、异常测试数据来源或模拟方式 | 只有测试计划，没有数据来源或模拟方式 | ESC-004 |
| FE-PLAT-005 | 三大核心服务返回服务广场路径、无权限返回规则、异常返回规则 | 只有“返回上一页”等不可验证描述 | ESC-004 |

## 四、FE-BATCH-002 板块事实

| FE 项 | 板块 | 必填事实 | 不可接收内容 | 退回路径 |
| --- | --- | --- | --- | --- |
| FE-MOD-001 | 生命导航 | 主动作、页面方案、权限、后台处理、测试数据、验收责任 | 只有板块名称或宣传描述 | ESC-002 / ESC-003 |
| FE-MOD-002 | 俱乐部联盟 | 主动作、页面方案、权限、审核规则、管理中心边界、测试数据、验收责任 | 没有审核和管理中心边界 | ESC-002 / ESC-003 |
| FE-MOD-003 | 健康大管家 | 主动作、页面方案、权限、后台处理路径、测试数据、验收责任 | 没有后台处理路径或责任边界 | ESC-002 / ESC-003 |

## 五、FE-BATCH-003 Handoff 事实

| FE 项 | Handoff | 必填事实 | 不可接收内容 | 退回路径 |
| --- | --- | --- | --- | --- |
| FE-HO-001 | SP-H002 | 生命导航 Handoff 完整提交、平台接收、依赖、阻塞、下一步动作和质量复核结论 | Handoff 字段缺失或未经过平台接收 | ESC-003 / ESC-005 |
| FE-HO-002 | SP-H003 | 俱乐部联盟 Handoff 完整提交、平台接收、依赖、阻塞、下一步动作和质量复核结论 | 未说明审核或管理中心依赖 | ESC-003 / ESC-005 |
| FE-HO-003 | SP-H004 | 健康大管家 Handoff 完整提交、平台接收、依赖、阻塞、下一步动作和质量复核结论 | 未说明后台处理路径依赖 | ESC-003 / ESC-005 |

## 六、执行后回写

| 执行动作 | 必须回写 | 不允许 |
| --- | --- | --- |
| 提交包字段完整 | `fact-evidence-submission-packet.md`、`fact-evidence-intake-review.md` | 直接改成 Go 或 Partial Go |
| 审计复核通过 | `fact-evidence-review-run-log.md`、`phase-gate-evidence-matrix.md` | 跳过接收清单 |
| 退回补充 | `fact-evidence-intake-review.md`、`blocker-escalation-decision-log.md`、对应 action pack | 只在备注里写缺口 |
| 批次无事实提交 | 保持待提交，并更新下一步动作 | 把计划、规范或原型当成事实 |

## 七、当前结论

截至 2026-07-10，下一轮事实证据批次执行单已建立，并已接入 `day-1-fact-gap-closure-run-record.md` 的 Day 1 缺口关闭结论。FE-BATCH-001 已完成工作区核查，但未发现可接收平台事实，执行结论见 `fact-evidence-next-batch-run-record.md`。FE-BATCH-002 已完成板块事实核查，但未发现可接收板块事实，执行结论见 `module-fact-evidence-run-record.md` 和 `fact-evidence-next-batch-run-record.md`。FE-BATCH-003 已完成 Handoff 事实核查，但未发现可接收 Handoff 事实，执行结论见 `handoff-fact-evidence-run-record.md` 和 `fact-evidence-next-batch-run-record.md`。FE-BATCH-004 已完成 FE-GATE 触发核查，但前置事实不满足，执行结论见 `gate-fact-evidence-run-record.md` 和 `fact-evidence-next-batch-run-record.md`。FE-BATCH-005 已完成 FE-ACC 触发核查，但尚无真实联调、问题关闭、FE-GATE 复核和验收执行事实，执行结论见 `acceptance-fact-evidence-run-record.md` 和 `fact-evidence-next-batch-run-record.md`。下一步先补 FE-PLAT-001 至 FE-PLAT-005 的真实事实字段，再补 FE-MOD-001 至 FE-MOD-003 的真实板块事实，最后补 FE-HO-001 至 FE-HO-003 的真实 Handoff 事实；不启动 FR-GATE 或 FR-ACC。当前尚未提交真实事实证据，首次真实联调保持 No-Go，第一阶段验收保持 No-Go。
