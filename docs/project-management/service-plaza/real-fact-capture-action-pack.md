# 服务广场真实事实采集动作包

日期：2026-07-09

本文件用于把当前“待补真实事实”推进到可提交、可接收、可复核的最小动作。当前项目按单人决策和 Agent 协同推进，不要求外部多人会议、聊天工具或回执机制。

## 一、执行原则

1. 只采集真实事实，不用计划、建议、默认假设、空模板或原型说明替代事实。
2. 每条事实必须同时具备事实内容、证据位置、回写文件和接收判断。
3. 先补 FE-PLAT，再补 FE-MOD，再补 FE-HO；三类前置事实未接收前，不触发 FE-GATE。
4. 未完成真实联调、问题关闭和 FE-GATE 复核前，不触发 FE-ACC。
5. 任何一项缺证据时，保持待提交，并回到对应工作表补齐。

## 二、最小执行顺序

| 顺序 | 动作 | 主 Agent | 输入文件 | 输出文件 | 通过条件 |
| --- | --- | --- | --- | --- | --- |
| 1 | 采集平台路由、权限、账号、数据和返回路径事实 | 平台 Agent | `platform-fact-submission-worksheet.md`、`routing-and-temporary-page-spec.md`、`integration-checklist.md`、`test-accounts-and-data.md` | `fact-evidence-submission-packet.md` 平台事实提交包 | FE-PLAT-001 至 FE-PLAT-005 字段完整，且证据位置可追溯 |
| 2 | 接收平台事实 | 审计 Agent | `fact-evidence-submission-packet.md`、`platform-route-account-data-evidence-intake.md` | `fact-evidence-intake-review.md`、`fact-evidence-review-run-log.md` | FR-PLAT 可启动或明确退回字段 |
| 3 | 采集三大核心服务板块事实 | 板块 Agent | `module-fact-submission-worksheet.md`、`core-service-main-action-confirmation.md`、`module-intake-cards.md` | `fact-evidence-submission-packet.md` 板块事实提交包 | FE-MOD-001 至 FE-MOD-003 字段完整，且证据位置可追溯 |
| 4 | 接收板块事实 | 审计 Agent | `fact-evidence-submission-packet.md`、`module-fact-evidence-intake.md` | `fact-evidence-intake-review.md`、`fact-evidence-review-run-log.md` | FR-MOD 可启动或明确退回字段 |
| 5 | 采集 Handoff 事实 | 板块 Agent | `handoff-fact-submission-worksheet.md`、`round-1-handoff-forms.md`、`handoff-log.md`、`handoff-quality-review.md` | `fact-evidence-submission-packet.md` Handoff 事实提交包 | FE-HO-001 至 FE-HO-003 字段完整，且平台可接收结论明确 |
| 6 | 接收 Handoff 事实 | 审计 Agent | `fact-evidence-submission-packet.md`、`handoff-fact-evidence-intake.md` | `fact-evidence-intake-review.md`、`fact-evidence-review-run-log.md` | FR-HO 可启动或明确退回字段 |
| 7 | 判断 FE-GATE | 审计 Agent | `pre-gate-fact-readiness-matrix.md`、`gate-trigger-decision-record.md`、`gate-fact-evidence-run-record.md` | `fact-evidence-review-run-log.md`、`first-integration-go-checklist.md` | FE-PLAT、FE-MOD、FE-HO 均复核通过后才允许启动 FR-GATE |
| 8 | 判断 FE-ACC | 验收 Agent | `acceptance-fact-evidence-run-record.md`、`integration-to-acceptance-transition.md`、`phase-1-acceptance-run-record.md` | `fact-evidence-review-run-log.md`、`phase-1-acceptance-checklist.md` | 真实联调、问题关闭、FE-GATE 复核和验收执行事实齐全后才允许启动 FR-ACC |

## 三、本轮可执行采集字段

| 队列 | 必须采集的最小事实 | 当前状态 | 不满足时动作 |
| --- | --- | --- | --- |
| FE-PLAT-001 | 环境名称、环境地址、服务广场入口、三大核心服务路由或临时承接页 | 待提交 | 回填 `platform-fact-submission-worksheet.md` |
| FE-PLAT-002 | 未登录、普通会员、无权限、管理或审核权限状态 | 待提交 | 回填 `platform-fact-submission-worksheet.md` |
| FE-PLAT-003 | 测试账号类型、获取方式、保管方式、可用状态 | 待提交 | 回填 `platform-fact-submission-worksheet.md`，不得记录真实密码 |
| FE-PLAT-004 | 三大核心服务正常、空状态、异常数据来源或模拟方式 | 待提交 | 回填 `platform-fact-submission-worksheet.md` |
| FE-PLAT-005 | 返回服务广场路径、无权限返回规则、异常返回规则 | 待提交 | 回填 `platform-fact-submission-worksheet.md` |
| FE-MOD-001 | 生命导航主动作、页面方案、权限、后台处理、测试数据、验收责任 | 待提交 | 回填 `module-fact-submission-worksheet.md` |
| FE-MOD-002 | 俱乐部联盟主动作、页面方案、审核规则、管理中心边界、测试数据、验收责任 | 待提交 | 回填 `module-fact-submission-worksheet.md` |
| FE-MOD-003 | 健康大管家主动作、页面方案、后台处理路径、测试数据、验收责任 | 待提交 | 回填 `module-fact-submission-worksheet.md` |
| FE-HO-001 | 生命导航 Handoff 提交、接收、依赖、阻塞、下一步、平台可接收结论 | 待提交 | 回填 `handoff-fact-submission-worksheet.md` |
| FE-HO-002 | 俱乐部联盟 Handoff 提交、接收、审核依赖、管理中心边界、平台可接收结论 | 待提交 | 回填 `handoff-fact-submission-worksheet.md` |
| FE-HO-003 | 健康大管家 Handoff 提交、接收、后台处理依赖、平台可接收结论 | 待提交 | 回填 `handoff-fact-submission-worksheet.md` |

## 四、提交门槛

| 提交对象 | 允许提交条件 | 禁止提交条件 |
| --- | --- | --- |
| 平台事实包 | FE-PLAT-001 至 FE-PLAT-005 均有事实内容和证据位置 | 只有路由建议、账号计划、数据计划或空模板 |
| 板块事实包 | FE-MOD-001 至 FE-MOD-003 均有确认来源、页面方案、权限、后台处理、测试数据和验收责任 | 只有推荐主动作或宣传描述 |
| Handoff 事实包 | FE-HO-001 至 FE-HO-003 均有提交接收记录、依赖、阻塞、下一步和平台可接收结论 | 只有 Handoff 模板或未接收记录 |
| FE-GATE | FE-PLAT、FE-MOD、FE-HO 均提交并通过复核 | 任一前置事实仍待提交或未复核 |
| FE-ACC | 真实联调、问题关闭、FE-GATE 复核、验收执行和负责人裁决均有事实 | 未完成联调或问题关闭 |

## 五、当前结论

截至 2026-07-10，本动作包已建立，并已通过 `day-1-fact-gap-closure-run-record.md` 收敛 Day 1 下一步。当前尚未采集到新的真实事实。FE-PLAT、FE-MOD、FE-HO 继续保持待提交；FR-PLAT、FR-MOD、FR-HO、FR-GATE 和 FR-ACC 均不触发；下一步先补 FE-PLAT-001 至 FE-PLAT-005；首次真实联调和第一阶段验收继续 No-Go。
