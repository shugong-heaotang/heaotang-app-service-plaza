# 服务广场当前周推进作战板

日期：2026-07-10

本文件用于服务广场第一轮推进的日常指挥。当前只有项目负责人一人参与，因此每天由 agent 按本文件检查状态、登记确认、处理阻塞和判断是否进入首次真实联调。

## 一、本周目标

本周不再讨论服务广场架构方案，目标是把第一轮真实联调的前置条件补齐。

| 目标 | 完成标准 | 当前判断 |
| --- | --- | --- |
| Day 0 两小时动作完成 | 第一批确认、确认登记、启动会准备确认、当日门禁复核、执行记录和启动会转换判断完成 | 部分完成 |
| Day 0 确认控制闭环 | 按 `day-0-dispatch-control.md` 完成确认前核对、确认后回写和补齐设置 | 部分完成 |
| OUT-001 逐条确认执行 | 按 `out-001-dispatch-runbook.md` 七项 P0 确认事项逐条确认、逐条登记 | 首轮完成 |
| OUT-001 确认证据可追溯 | 按 `out-001-dispatch-evidence-register.md` 登记证据编号、位置和可追溯性 | 首轮完成 |
| OUT-001 补齐证据可追溯 | 按 `out-001-followup-evidence-register.md` 登记 T+0.5、T+1、T+2 补齐和裁决证据 | T+0.5 缺口检查已形成，事实证据待补齐 |
| OUT-001 确认到门禁流水可追溯 | 按 `day-0-dispatch-to-gate-run-log.md` 跟踪确认、证据、回写和门禁复核 | 首轮完成 |
| Day 0 日终复盘可同步 | 按 `day-0-end-of-day-summary.md` 形成单人项目复盘摘要，供后续 agent 接续 | 首轮完成 |
| Agent 协同规则已明确 | 按 `collaboration-tool-setup.md` 采用单人决策、agent 协同和本地台账推进 | 已完成 |
| Agent 接续看板已建立 | 按 `agent-coordination-board.md` 记录当前状态、下一步队列和交接记录 | 已完成 |
| 责任边界确认 | 架构、平台、三大核心服务、验收边界均在本地台账中明确 | 未完成 |
| 第一批确认已登记 | P0 确认事项进入 `outbound-message-dispatch-log.md` 和 `external-confirmation-tracker.md` | 首轮完成 |
| 确认完整性复核闭环 | 形成确认结果后按 `reply-completeness-review.md` 判断完整、信息不完整、需裁决或无效 | 首轮完成 |
| 确认结果回写闭环 | 完整确认结果按 `reply-ledger-update-checklist.md` 逐条回写目标台账 | 未完成 |
| 事实证据提交总控 | FE-PLAT、FE-MOD、FE-HO、FE-GATE、FE-ACC 的提交顺序、依赖和复核入口统一到 `fact-evidence-submission-control-board.md` | 已建立，待事实提交 |
| 下一轮事实证据批次 | FE-BATCH-001 至 FE-BATCH-005 的执行顺序、输入字段、退回条件统一到 `fact-evidence-next-batch-runbook.md`，实际核查登记到 `fact-evidence-next-batch-run-record.md` | FE-BATCH-001 至 FE-BATCH-003 均已核查但未接收；FE-BATCH-004 和 FE-BATCH-005 已核查但不触发 |
| 前置事实就绪矩阵 | FE-GATE 前置事实统一到 `pre-gate-fact-readiness-matrix.md` | 已建立，FE-PLAT、FE-MOD、FE-HO 均未就绪 |
| FE-GATE 触发判定 | FE-GATE 是否可触发统一到 `gate-trigger-decision-record.md` | 已登记 GATE-TRG-001；当前不触发 FE-GATE，不启动 FR-GATE |
| FE-GATE 执行记录 | FE-GATE-001 的触发核查统一到 `gate-fact-evidence-run-record.md` | 已核查但不触发 FR-GATE，首次真实联调继续 No-Go |
| 验收事实执行记录 | FE-ACC-011 至 FE-ACC-013 的核查结果统一到 `acceptance-fact-evidence-run-record.md` | 已核查但无验收触发事实，不触发 FR-ACC |
| 真实事实采集动作包 | 平台、板块、Handoff、FE-GATE、FE-ACC 的下一阶段最小执行顺序统一到 `real-fact-capture-action-pack.md` | 已建立，当前仍无新真实事实 |
| 真实事实采集执行记录 | 动作包第一次执行结果统一到 `real-fact-capture-run-record.md` | 已执行；未接收新事实，不触发 FR-PLAT、FR-MOD、FR-HO |
| Day 1 接续执行记录 | 2026-07-10 跨日状态接续统一到 `day-1-continuation-run-record.md` | 已接续；无新增事实，No-Go 不变 |
| Day 1 事实缺口关闭 | P0 事实缺口关闭核查统一到 `day-1-fact-gap-closure-run-record.md` | 已核查；无可关闭 P0，先补 FE-PLAT-001 至 FE-PLAT-005 |
| 平台事实最小补齐 | FE-BATCH-001 未接收后的五项最小事实统一到 `platform-fact-minimum-evidence-checklist.md` | 已建立，下一步按环境路由、权限、账号、数据、返回路径逐项补证据 |
| 平台事实提交工作表 | FE-PLAT-001 至 FE-PLAT-005 的可填写字段统一到 `platform-fact-submission-worksheet.md` | 已建立，当前全部待补事实，不进入待复核 |
| 平台五项最小证据执行记录 | FE-PLAT-001 至 FE-PLAT-005 的本轮核查结果统一到 `platform-fact-minimum-evidence-run-record.md` | 已核查，五项均无可接收事实；继续待补 |
| 平台路由账号数据证据接收 | 路由、临时页、权限、账号、数据和返回路径统一到 `platform-route-account-data-evidence-intake.md` | 已建立接收和退回标准，当前均待提交 |
| Day 1 平台事实执行 | FE-PLAT-001 至 FE-PLAT-005 的 Day 1 核查统一到 `day-1-platform-fact-run-record.md` | 已核查；五项均待提交，FR-PLAT 不触发 |
| Day 1 平台提交控制 | 平台事实提交包控制统一到 `day-1-platform-submission-control-record.md` | 已控制；五项未齐时不得填写待复核 |
| 板块事实提交工作表 | FE-MOD-001 至 FE-MOD-003 的可填写字段统一到 `module-fact-submission-worksheet.md` | 已建立，当前全部待补事实，不进入待复核 |
| 板块事实接收与退回 | FE-MOD-001 至 FE-MOD-003 的接收标准统一到 `module-fact-evidence-intake.md` | 已建立，MOD-INTAKE-001 至 MOD-INTAKE-003 均待提交，不触发 FR-MOD |
| 板块事实执行记录 | FE-MOD-001 至 FE-MOD-003 的核查结果统一到 `module-fact-evidence-run-record.md` | 已核查但无可接收板块事实，不触发 FR-MOD |
| Handoff 事实提交工作表 | FE-HO-001 至 FE-HO-003 的可填写字段统一到 `handoff-fact-submission-worksheet.md` | 已建立，当前全部待补事实，不进入待复核 |
| Handoff 事实接收与退回 | FE-HO-001 至 FE-HO-003 的接收标准统一到 `handoff-fact-evidence-intake.md` | 已建立，HO-INTAKE-001 至 HO-INTAKE-003 均待提交，不触发 FR-HO |
| Handoff 事实执行记录 | FE-HO-001 至 FE-HO-003 的核查结果统一到 `handoff-fact-evidence-run-record.md` | 已核查但无可接收 Handoff 事实，不触发 FR-HO |
| 三大核心服务主动作确认 | 生命导航、俱乐部联盟、健康大管家均确认第一阶段主动作和最小可交付范围 | 未完成 |
| 三大核心服务板块事实提交 | FE-MOD-001 至 FE-MOD-003 按 `module-fact-submission-action-pack.md` 完成提交前核对 | 执行包已建，待事实证据 |
| 平台联调环境确认 | 路由、权限、测试账号、测试数据、临时承接页方案均按 `platform-fact-submission-action-pack.md` 完成提交前核对 | 已建字段和执行包，待事实证据 |
| 启动会到首次联调转换闭环 | 启动会后行动项进入 `kickoff-action-tracker.md`，并按 `kickoff-to-first-integration-transition.md` 复核 Go / Partial Go / No-Go | 未完成 |
| Handoff 补齐并复核 | 三大核心服务按 `handoff-completion-action-pack.md` 和 `handoff-operating-mechanism.md` 提交首轮 handoff，并通过 `handoff-quality-review.md` 复核 | 未完成 |
| 首次真实联调解锁 | `first-integration-go-checklist.md` 结论从 No-Go 变为 Go 或 Partial Go | 未完成 |
| 联调到问题关闭转换闭环 | 首次联调后失败项进入问题池，主链路问题完成关闭、延期或升级判断 | 未完成 |
| 第一阶段验收门禁明确 | 联调完成后可按 `integration-to-acceptance-transition.md` 判断是否验收 | 口径已建，待联调事实 |
| 第一阶段验收证据可追溯 | 验收证据在 `acceptance-evidence-register.md` 登记并可回溯 | 编号已建，待真实证据 |
| 第一阶段验收执行可追溯 | 验收执行记录在 `phase-1-acceptance-run-record.md` 登记并可回溯 | 字段已建，待真实验收 |
| P0 阻塞升级有记录 | 未补齐确认、Handoff 退回、证据缺失进入 `blocker-escalation-decision-log.md` | 缺口检查和阻塞映射已登记，暂不裁决 |
| 门禁证据矩阵可追溯 | 每个 Go / No-Go 结论在 `phase-gate-evidence-matrix.md` 有证据、缺口和责任人 | 已建立，待事实证据 |
| 台账一致性可审计 | 每日和门禁变化时按 `consistency-and-gate-audit.md` 复核 | 已建立，待每日复核记录 |

## 二、每日推进节奏

| 时间点 | 动作 | 负责人 | 记录位置 |
| --- | --- | --- | --- |
| 上午 | 执行 Day 0 两小时动作并登记记录 | 执行 Agent | `day-0-two-hour-execution.md`、`day-0-execution-record.md` |
| 上午 | 执行 Day 0 确认控制 | 执行 Agent | `day-0-dispatch-control.md` |
| 上午 | 逐条确认 OUT-001 P0 事项 | 执行 Agent | `out-001-dispatch-runbook.md` |
| 上午 | 登记 OUT-001 确认证据 | 文档 Agent | `out-001-dispatch-evidence-register.md` |
| 上午 | 更新 OUT-001 确认到门禁总流水 | 审计 Agent | `day-0-dispatch-to-gate-run-log.md` |
| 下午 | 登记 OUT-001 补齐和裁决证据 | 执行 Agent | `out-001-followup-evidence-register.md` |
| 上午 | 判断 Day 0 到启动会转换动作 | 规划 Agent | `day-0-to-kickoff-transition.md` |
| 上午 | 检查昨日未补齐确认事项 | 审计 Agent | `outbound-message-dispatch-log.md`、`external-confirmation-tracker.md` |
| 上午 | 更新今日 P0 动作 | 执行 Agent | `daily-standup-log.md` |
| 上午 | 检查 agent 协同和本地台账是否一致 | 审计 Agent | `collaboration-tool-setup.md`、`consistency-and-gate-audit.md` |
| 上午 | 检查 agent 接续看板和本轮最小动作 | 规划 Agent | `agent-coordination-board.md` |
| 下午 | 登记并复核确认结果 | 文档 Agent | `reply-intake-tracker.md`、`reply-completeness-review.md`、`reply-processing-batch-log.md` |
| 下午 | 将完整确认结果逐条回写目标台账 | 文档 Agent | `reply-ledger-update-checklist.md` |
| 下午 | 启动会后登记行动项 | 执行 Agent | `kickoff-action-tracker.md` |
| 下午 | 启动会后转换首次联调动作 | 规划 Agent | `kickoff-to-first-integration-transition.md` |
| 下午 | 更新责任边界、主动作、路由、账号、数据、handoff 台账 | 对应 Agent | 对应台账文件 |
| 下午 | 执行 Handoff 提交、复核、退回和门禁回写 | 平台 Agent、板块 Agent、审计 Agent | `handoff-completion-action-pack.md`、`handoff-operating-mechanism.md`、`handoff-quality-review.md` |
| 下午 | 登记未补齐、退回、缺证据阻塞 | 执行 Agent | `blocker-escalation-decision-log.md` |
| 下班前 | 复核首次真实联调 Go / Partial Go / No-Go | 审计 Agent | `reply-to-gate-transition.md`、`kickoff-to-first-integration-transition.md`、`handoff-quality-review.md`、`first-integration-go-checklist.md` |
| 下班前 | 联调后转换问题关闭动作 | 执行 Agent | `first-integration-to-issue-closure-transition.md`、`round-1-issue-closure-tracker.md` |
| 下班前 | 验收后记录执行结论 | 验收 Agent | `phase-1-acceptance-run-record.md` |
| 下班前 | 复核门禁证据矩阵 | 审计 Agent | `phase-gate-evidence-matrix.md` |
| 下班前 | 形成 Day 0 日终复盘摘要 | 文档 Agent | `day-0-end-of-day-summary.md` |
| 下班前 | 审计台账一致性和门禁证据 | 审计 Agent | `consistency-and-gate-audit.md` |

## 三、当前 P0 推进事项

| 编号 | 事项 | 处理 Agent | 确认对象 | 目标产出 | 状态 |
| --- | --- | --- | --- | --- | --- |
| SP-CW-000 | 执行 Day 0 两小时清单并登记记录 | 执行 Agent | 项目负责人确认 | `day-0-execution-record.md`、`outbound-message-dispatch-log.md`、`external-confirmation-tracker.md`、`phase-gate-status.md` 更新 | 部分完成 |
| SP-CW-000B | 执行 Day 0 确认控制和确认后回写 | 执行 Agent | 项目负责人确认 | `day-0-dispatch-control.md`、`outbound-message-dispatch-log.md`、`external-confirmation-tracker.md`、`reply-followup-cadence.md` 更新 | 部分完成 |
| SP-CW-000C | 逐条确认 OUT-001 P0 事项 | 执行 Agent | 项目负责人确认 | `out-001-dispatch-runbook.md`、`outbound-message-dispatch-log.md` 更新 | 首轮完成 |
| SP-CW-000D | 登记 OUT-001 确认证据 | 文档 Agent | 项目负责人确认 | `out-001-dispatch-evidence-register.md`、`phase-gate-evidence-matrix.md` 更新 | 首轮完成 |
| SP-CW-000E | 登记 OUT-001 补齐和裁决证据 | 执行 Agent | 未补齐事项 | `out-001-followup-evidence-register.md`、`reply-followup-cadence.md`、`blocker-escalation-decision-log.md` 更新 | 第一次缺口检查已形成，待事实证据 |
| SP-CW-000F | 更新 OUT-001 确认到门禁复核流水 | 审计 Agent | 项目负责人确认 | `day-0-dispatch-to-gate-run-log.md` 更新 | 首轮完成 |
| SP-CW-000G | 形成 Day 0 日终复盘摘要 | 文档 Agent | 后续 agent 接续 | `day-0-end-of-day-summary.md` 更新 | 首轮完成 |
| SP-CW-000H | 明确 agent 协同和本地台账推进规则 | 规划 Agent | 项目负责人确认 | `collaboration-tool-setup.md` 更新 | 已完成 |
| SP-CW-000I | 建立 agent 接续看板 | 规划 Agent | 项目负责人确认 | `agent-coordination-board.md` 更新 | 已完成 |
| SP-CW-000A | 完成 Day 0 到启动会转换判断 | 规划 Agent | 项目负责人确认 | `day-0-to-kickoff-transition.md`、`reply-intake-tracker.md`、`reply-followup-cadence.md` 更新 | 待执行 |
| SP-CW-001 | 登记项目统一推进口径确认 | 文档 Agent | 项目负责人确认 | `outbound-message-dispatch-log.md`、`external-confirmation-tracker.md` 更新 | 待执行 |
| SP-CW-002 | 补齐责任边界、角色和联系方式 | 文档 Agent | 项目负责人确认 | `owner-roster.md` 更新 | 待执行 |
| SP-CW-002A | 复核确认完整性并分流补齐或回写 | 审计 Agent | 已形成确认结果 | `reply-completeness-review.md`、`reply-processing-batch-log.md` 更新 | 待执行 |
| SP-CW-002B | 完整确认结果逐条回写目标台账 | 文档 Agent | 完整确认结果 | `reply-ledger-update-checklist.md` 和目标台账更新 | 待执行 |
| SP-CW-003 | 确认三大核心服务主动作 | 板块 Agent | 项目负责人确认 | `core-service-main-action-confirmation.md` 更新 | 待执行 |
| SP-CW-003A | 按板块事实提交工作表和执行包补齐 FE-MOD-001 至 FE-MOD-003 | 板块 Agent、审计 Agent | 项目负责人确认 | `module-fact-submission-worksheet.md`、`module-fact-submission-action-pack.md`、`module-fact-evidence-intake.md`、`module-fact-evidence-run-record.md`、`fact-evidence-submission-packet.md`、`fact-evidence-intake-review.md` 更新 | 提交工作表、执行包、接收表和执行记录已建；本轮核查未接收，待真实事实 |
| SP-CW-004 | 确认平台路由、权限、账号、数据 | 平台 Agent | 项目负责人确认 | `platform-fact-minimum-evidence-checklist.md`、`platform-fact-submission-worksheet.md`、`platform-fact-minimum-evidence-run-record.md`、`platform-route-account-data-evidence-intake.md`、`platform-fact-submission-action-pack.md`、`platform-condition-evidence-runbook.md`、`integration-checklist.md`、`test-accounts-and-data.md` 更新 | 最小补齐清单、提交工作表、执行记录和接收表已建；本轮五项均不可接收，待真实事实 |
| SP-CW-004A | 启动会后登记行动项 | 执行 Agent | 项目负责人确认 | `kickoff-action-tracker.md` 更新 | 待执行 |
| SP-CW-004B | 启动会后转换首次联调动作 | 规划 Agent | 项目负责人确认 | `kickoff-to-first-integration-transition.md`、`first-integration-go-checklist.md` 更新 | 待执行 |
| SP-CW-005 | 补齐并复核三大核心服务 Handoff | 板块 Agent、审计 Agent | 项目负责人确认 | `handoff-fact-submission-worksheet.md`、`handoff-fact-evidence-intake.md`、`handoff-fact-evidence-run-record.md`、`handoff-completion-action-pack.md`、`handoff-operating-mechanism.md`、`round-1-handoff-forms.md`、`handoff-quality-review.md` 更新 | 提交工作表、执行包、接收表和执行记录已建；本轮核查未接收，待真实 Handoff 事实 |
| SP-CW-005A | 按下一轮事实证据批次推进平台、板块、Handoff 和验收触发缺口 | 平台 Agent、板块 Agent、审计 Agent | 项目负责人确认 | `real-fact-capture-action-pack.md`、`real-fact-capture-run-record.md`、`fact-evidence-next-batch-runbook.md`、`fact-evidence-next-batch-run-record.md`、`pre-gate-fact-readiness-matrix.md`、`gate-trigger-decision-record.md`、`gate-fact-evidence-run-record.md`、`acceptance-fact-evidence-run-record.md`、`platform-fact-minimum-evidence-checklist.md`、`platform-fact-submission-worksheet.md`、`platform-fact-minimum-evidence-run-record.md`、`platform-route-account-data-evidence-intake.md`、`module-fact-submission-worksheet.md`、`module-fact-evidence-intake.md`、`module-fact-evidence-run-record.md`、`handoff-fact-submission-worksheet.md`、`handoff-fact-evidence-intake.md`、`handoff-fact-evidence-run-record.md`、`p0-evidence-closure-queue.md`、`p0-evidence-execution-log.md`、`fact-evidence-daily-execution.md`、`fact-evidence-submission-control-board.md`、`fact-evidence-submission-packet.md`、`fact-evidence-intake-review.md`、`fact-evidence-review-run-log.md` 逐项更新 | FE-BATCH-001 至 FE-BATCH-003 均已核查但未接收；FE-BATCH-004 和 FE-BATCH-005 已核查但不触发；真实事实采集已执行但未接收 |
| SP-CW-005B | 执行 Day 1 跨日接续 | 审计 Agent、文档 Agent | 后续 agent 接续 | `day-1-continuation-run-record.md`、`daily-standup-log.md`、`project-status-one-page.md`、`phase-progress-report.md` 更新 | 已接续；无新增事实，No-Go 不变 |
| SP-CW-005C | 执行 Day 1 事实缺口关闭核查 | 审计 Agent、文档 Agent | P0 事实缺口队列 | `day-1-fact-gap-closure-run-record.md`、`p0-evidence-closure-queue.md`、`p0-evidence-execution-log.md`、`fact-evidence-daily-execution.md` 更新 | 已核查；无可关闭 P0，先补 FE-PLAT-001 至 FE-PLAT-005 |
| SP-CW-005D | 执行 Day 1 平台五项事实核查 | 平台 Agent、审计 Agent | FE-PLAT 平台事实 | `day-1-platform-fact-run-record.md`、`platform-fact-submission-worksheet.md`、`platform-route-account-data-evidence-intake.md`、`fact-evidence-intake-review.md` 更新 | 已核查；五项均待提交，不触发 FR-PLAT |
| SP-CW-005E | 执行 Day 1 平台事实提交前控制 | 平台 Agent、审计 Agent | 平台事实提交包 | `day-1-platform-submission-control-record.md`、`fact-evidence-submission-packet.md`、`fact-evidence-submission-control-board.md` 更新 | 已控制；五项未齐时不得填写待复核 |
| SP-CW-005F | 执行 Day 1 环境与路由事实核查 | 平台 Agent、审计 Agent | FE-PLAT-001 | `day-1-environment-route-run-record.md`、`routing-and-temporary-page-spec.md`、`integration-checklist.md`、`platform-fact-submission-worksheet.md` 更新 | 已核查；仅有建议路由和原型，不触发 FR-PLAT-001 |
| SP-CW-005G | 建立 FE-PLAT-001 回填与复核路径 | 平台 Agent、审计 Agent | FE-PLAT-001 至 FR-PLAT-001 | `platform-fact-backfill-review-path.md`、`fact-evidence-submission-packet.md`、`fact-evidence-intake-review.md`、`fact-evidence-review-run-log.md` 更新 | 已建立路径；未满足八项事实前不得待复核 |
| SP-CW-006 | 按总控表、确认转换和启动会后转换规则复核首次真实联调门禁 | 审计 Agent | 项目负责人确认 | `fact-evidence-submission-control-board.md`、`reply-to-gate-transition.md`、`kickoff-to-first-integration-transition.md`、`first-integration-go-checklist.md` 更新 | No-Go |
| SP-CW-006A | 首次联调后转换问题关闭动作 | 执行 Agent | 项目负责人确认 | `first-integration-to-issue-closure-transition.md`、`issue-pool.md`、`round-1-issue-closure-tracker.md` 更新 | 待执行 |
| SP-CW-006B | 第一阶段验收执行记录 | 验收 Agent | 项目负责人确认 | `integration-to-acceptance-transition.md`、`phase-1-acceptance-run-record.md`、`acceptance-evidence-register.md` 更新 | 验收口径已建，待真实验收 |
| SP-CW-007 | 登记和裁决 P0 阻塞 | 执行 Agent | 项目负责人确认 | `blocker-escalation-decision-log.md` 更新 | 阻塞映射已登记，暂不裁决 |

## 四、Agent 协同规则

本项目当前只有项目负责人一人参与，不需要配置飞书、企业微信、钉钉、Jira、禅道等外部工具。后续由 agent 围绕本地台账协同，必须满足以下规则：

| 规则 | 要求 |
| --- | --- |
| 一个主入口 | 所有 agent 先读 `START-HERE.md` |
| 一个接续看板 | 所有 agent 再读 `agent-coordination-board.md` |
| 一个总看板 | 所有状态以 `current-week-command-board.md` 和 `progress-board.md` 为准 |
| 一个问题池 | 所有阻塞进入 `issue-pool.md`，不能停留在临时说明里 |
| 一个 Handoff 记录 | 阶段交接以 `handoff-completion-action-pack.md`、`handoff-fact-evidence-intake.md`、`handoff-log.md` 和 `round-1-handoff-forms.md` 为准 |
| 一个门禁结论 | 是否联调、是否验收以 Go / No-Go 清单为准 |

## 五、沟通升级规则

| 场景 | 处理人 | 升级时限 | 升级对象 |
| --- | --- | --- | --- |
| 板块资料缺失 | 板块 Agent | 当日未补齐 | 项目负责人裁决 |
| 接口、路由、权限不清 | 平台 Agent | 当日未解决 | 项目负责人裁决 |
| 测试账号或测试数据缺失 | 平台 Agent | 当日未补齐 | 项目负责人裁决 |
| 主动作或最小范围争议 | 规划 Agent | 直接提出裁决项 | 项目负责人裁决 |
| 影响服务广场架构边界 | 规划 Agent | 直接形成 ADR 草案 | 项目负责人裁决 |
| 超过一个工作日未解决的主链路阻塞 | 执行 Agent、审计 Agent | 次日进入阻塞台账 | 项目负责人裁决 |

## 六、每日结束前必须更新

每天结束前只检查以下事项：

1. `outbound-message-dispatch-log.md` 是否登记当天确认批次。
2. `day-0-execution-record.md` 是否记录 Day 0 实际完成情况。
3. `day-0-dispatch-control.md` 是否完成确认前核对、确认后回写和补齐设置。
4. `out-001-dispatch-runbook.md` 是否逐条记录 OUT-001 确认事项、确认方式、确认时间和处理截止时间。
5. `out-001-dispatch-evidence-register.md` 是否登记证据编号、证据位置和可追溯性。
6. `day-0-dispatch-to-gate-run-log.md` 是否记录确认、证据、回写和门禁复核流水。
7. `out-001-followup-evidence-register.md` 是否登记补齐、裁决证据和下一步动作。
8. `day-0-to-kickoff-transition.md` 是否完成确认、补齐、裁决和启动会动作判断。
9. `external-confirmation-tracker.md` 是否更新确认状态。
10. `reply-intake-tracker.md` 是否登记新确认结果。
11. `reply-completeness-review.md` 是否判断新确认结果完整性、缺失字段、回写文件和门禁影响。
12. `reply-ledger-update-checklist.md` 是否将完整确认结果逐条回写目标台账。
13. `owner-roster.md` 是否补齐新增负责人。
14. `core-service-main-action-confirmation.md` 是否更新三大核心服务主动作。
15. `kickoff-action-tracker.md` 是否登记启动会行动项。
16. `kickoff-to-first-integration-transition.md` 是否完成启动会到首次联调转换判断。
17. `module-fact-submission-action-pack.md` 是否完成 FE-MOD-001 至 FE-MOD-003 的提交前核对、回写顺序和退回条件维护。
18. `platform-fact-submission-action-pack.md` 是否完成 FE-PLAT-001 至 FE-PLAT-005 的提交前核对、回写顺序和退回条件维护。
19. `platform-condition-evidence-runbook.md`、`integration-checklist.md` 和 `test-accounts-and-data.md` 是否更新平台条件。
20. `p0-evidence-execution-log.md` 是否登记 P0 证据执行流水、缺失事实和下一步动作。
21. `fact-evidence-daily-execution.md` 是否按优先级登记今日 FE 提交动作。
22. `fact-evidence-submission-control-board.md` 是否同步 FE 提交顺序、依赖、退回路径和门禁影响。
23. `fact-evidence-next-batch-runbook.md` 是否确认 FE-BATCH-001 至 FE-BATCH-005 的执行、退回和不触发条件。
23A. `fact-evidence-next-batch-run-record.md` 是否登记本轮实际核查结果、未接收原因和门禁影响。
23B. `pre-gate-fact-readiness-matrix.md` 是否汇总 FE-PLAT、FE-MOD、FE-HO 是否具备触发 FE-GATE 的前置条件。
23C. `platform-fact-minimum-evidence-checklist.md` 是否把 FE-BATCH-001 未接收后的五项平台事实压缩为最小补齐任务。
23D. `platform-fact-submission-worksheet.md` 是否把 FE-PLAT-001 至 FE-PLAT-005 转成可填写提交字段，且未补事实时仍保持待提交。
23D1. `platform-fact-minimum-evidence-run-record.md` 是否登记 FE-PLAT 五项最小证据的本轮核查结果，且未发现真实事实时不进入待复核。
23D2. `day-1-environment-route-run-record.md` 是否登记 FE-PLAT-001 环境与路由事实核查结果，且只有建议路由、原型或 ADR 时不触发 FR-PLAT-001。
23D3. `platform-fact-backfill-review-path.md` 是否明确 FE-PLAT-001 从真实证据回填到 FR-PLAT-001 复核的触发条件和退回条件。
23D2. `platform-route-account-data-evidence-intake.md` 是否登记路由、临时页、权限、账号、数据和返回路径的接收标准，且未提交真实事实时保持待提交。
23E. `module-fact-submission-worksheet.md` 是否把 FE-MOD-001 至 FE-MOD-003 转成可填写提交字段，且未补事实时仍保持待提交。
23E1. `module-fact-evidence-intake.md` 是否登记 MOD-INTAKE-001 至 MOD-INTAKE-003 的接收与退回标准，且未提交真实板块事实时保持待提交。
23E2. `module-fact-evidence-run-record.md` 是否登记 FE-MOD-001 至 FE-MOD-003 的核查结果，且未发现真实事实时不触发 FR-MOD。
23F. `handoff-fact-submission-worksheet.md` 是否把 FE-HO-001 至 FE-HO-003 转成可填写提交字段，且未补事实时仍保持待提交。
23F1. `handoff-fact-evidence-intake.md` 是否登记 HO-INTAKE-001 至 HO-INTAKE-003 的接收与退回标准，且未提交真实 Handoff 时保持待提交。
23F2. `handoff-fact-evidence-run-record.md` 是否登记 FE-HO-001 至 FE-HO-003 的核查结果，且未发现真实事实时不触发 FR-HO。
23G. `gate-trigger-decision-record.md` 是否登记 FE-GATE 触发或不触发判定，且未满足前置事实时保持不触发。
23H. `gate-fact-evidence-run-record.md` 是否登记 FE-GATE-001 的触发核查结果，且未满足前置事实时不启动 FR-GATE。
23I. `acceptance-fact-evidence-run-record.md` 是否登记 FE-ACC-011 至 FE-ACC-013 的触发核查结果，且未满足联调、问题关闭和 FE-GATE 前置时不启动 FR-ACC。
23J. `real-fact-capture-action-pack.md` 是否把下一阶段真实事实采集动作、输入、输出和通过条件统一到一个入口。
23K. `real-fact-capture-run-record.md` 是否登记真实事实采集执行结果，且无可接收事实时不启动 FR-PLAT、FR-MOD、FR-HO。
24. `fact-evidence-submission-packet.md` 是否填写事实证据提交包。
25. `fact-evidence-intake-review.md` 是否登记事实证据接收状态、复核结论和退回动作。
26. `fact-evidence-review-run-log.md` 是否登记事实证据复核动作。
27. `handoff-completion-action-pack.md` 是否把三大核心服务 Handoff 待补齐字段、回写文件和退回条件同步为可执行动作。
28. `handoff-operating-mechanism.md` 是否完成 Handoff 提交、复核、退回、升级和门禁回写判断。
29. `handoff-quality-review.md` 是否复核 Handoff 是否通过或退回。
30. `blocker-escalation-decision-log.md` 是否登记未补齐、退回、缺证据阻塞。
31. `reply-to-gate-transition.md` 和 `first-integration-go-checklist.md` 是否重新判断 Go / Partial Go / No-Go。
32. 如果已完成联调，`first-integration-to-issue-closure-transition.md` 是否完成问题关闭、延期和升级判断。
33. 如果已完成问题关闭，`integration-to-acceptance-transition.md` 是否复核验收门禁。
34. 如果进入验收准备，`acceptance-evidence-register.md` 是否登记证据编号和缺证据回退动作。
35. 如果执行验收，`phase-1-acceptance-run-record.md` 是否登记真实执行、证据编号、未通过项和签核结论。
36. `phase-gate-evidence-matrix.md` 是否更新门禁证据、缺口、责任人和回写文件。
37. `day-0-end-of-day-summary.md` 是否形成可同步的日终复盘摘要。
38. `collaboration-tool-setup.md` 是否保持单人决策、agent 协同和本地台账推进规则。
39. `agent-coordination-board.md` 是否更新当前状态、下一步队列和接续记录。
40. `consistency-and-gate-audit.md` 是否完成当日一致性审计。

## 七、本周出口

本周结束时只能形成三种结论之一：

| 结论 | 含义 | 下一步 |
| --- | --- | --- |
| Go | 三大核心服务均具备首次真实联调条件，FE-PLAT、FE-MOD、FE-HO 已通过复核，FE-GATE-001 已在 `fact-evidence-review-run-log.md` 复核完成 | 平台 Agent 登记联调安排，项目负责人确认 |
| Partial Go | 至少一个核心服务具备真实联调条件，且该板块对应 FE 前置事实和 FE-GATE 复核完成，其余服务阻塞明确 | 先联调已满足条件的板块 |
| No-Go | 责任边界、主动作、平台条件、Handoff 或 FE-GATE 复核未满足 | 继续按下一轮批次补 FE-PLAT、FE-MOD、FE-HO 事实证据、登记复核流水，并补齐未完成确认事项 |

本地项目台账始终作为唯一状态基准；任何 agent 接续推进都不得绕过本地门禁文件。
第一阶段验收不得仅凭本周出口表进入；必须先完成真实联调、问题关闭、FE-GATE 复核和 FE-ACC-011 至 FE-ACC-013 复核。
