# 服务广场项目推进台账

本目录用于持续推进服务广场项目。后续所有进度、接口、阻塞、Handoff、联调和阶段验收均在这里维护。

## 当前推进口径

当前项目按“项目负责人统一决策 + agent 协同 + 本地台账推进”执行。规划 Agent、执行 Agent、文档 Agent、平台 Agent、板块 Agent、验收 Agent、审计 Agent 分工协作；不要求配置复杂外部协作工具，也不以多人外发消息、等待回执或催办作为主流程。

所有 agent 接续前先读：

1. `START-HERE.md`
2. `agent-coordination-board.md`
3. `current-week-command-board.md`
4. `phase-gate-status.md`
5. `phase-gate-evidence-matrix.md`

## 核心入口

| 文件 | 用途 | 责任边界 |
| --- | --- | --- |
| `START-HERE.md` | 项目推进第一入口 | 所有 agent |
| `agent-coordination-board.md` | Agent 接续看板 | 规划 Agent |
| `current-week-command-board.md` | 当前周推进作战板 | 执行 Agent、审计 Agent |
| `project-status-one-page.md` | 当前状态一页纸 | 文档 Agent |
| `phase-progress-report.md` | 阶段推进报告 | 文档 Agent |
| `phase-gate-status.md` | 阶段门禁状态 | 审计 Agent |
| `phase-gate-evidence-matrix.md` | 门禁证据矩阵 | 审计 Agent |
| `consistency-and-gate-audit.md` | 台账一致性审计 | 审计 Agent |

## Day 0 与 OUT-001

| 文件 | 用途 | 当前状态 |
| --- | --- | --- |
| `day-0-two-hour-execution.md` | Day 0 两小时本地确认清单 | 待同步为确认模式 |
| `day-0-execution-record.md` | Day 0 执行记录 | 首轮确认已登记 |
| `day-0-dispatch-control.md` | Day 0 确认控制表 | 已收敛为单人确认模式 |
| `out-001-dispatch-runbook.md` | OUT-001 单人确认执行包 | 已收敛为确认执行包 |
| `outbound-message-dispatch-log.md` | 确认批次执行表 | OUT-001 首轮已登记 |
| `external-confirmation-tracker.md` | 确认事项跟踪表 | 已确认 / 待补齐状态已登记 |
| `out-001-dispatch-evidence-register.md` | OUT-001 确认证据登记表 | OUT001-EV 证据已登记 |
| `out-001-followup-evidence-register.md` | OUT-001 补齐证据登记表 | 第一次缺口检查已形成，事实证据待补齐 |
| `day-0-dispatch-to-gate-run-log.md` | Day 0 确认到门禁流水 | 首轮流水已登记 |
| `day-0-end-of-day-summary.md` | Day 0 日终复盘摘要 | 已更新为接续摘要 |
| `day-0-to-kickoff-transition.md` | Day 0 到启动会转换 | 待同步为确认/补齐模式 |

## 确认结果处理

| 文件 | 用途 | 当前状态 |
| --- | --- | --- |
| `communication-message-pack.md` | 第一轮确认口径包 | 已改为本地确认口径 |
| `reply-intake-tracker.md` | 确认结果登记表 | RPLY 首轮状态已登记 |
| `reply-completeness-review.md` | 确认完整性复核表 | RPLY-001 完整，其余信息不完整 |
| `reply-processing-batch-log.md` | 确认结果处理批次 | BATCH-001 已登记 |
| `reply-ledger-update-checklist.md` | 确认结果回写清单 | RPLY-001 已回写，RPLY-002 至 RPLY-010 待补齐 |
| `reply-to-gate-transition.md` | 确认结果到门禁转换规则 | 首次真实联调保持 No-Go |
| `p0-evidence-closure-queue.md` | P0 证据补齐与关闭队列 | 平台条件已建字段，板块确认、Handoff、门禁复核待补齐 |
| `p0-evidence-execution-log.md` | P0 证据补齐执行流水 | P0-RUN-001 至 P0-RUN-012 已登记，补齐证据和阻塞映射已建立 |
| `fact-evidence-intake-review.md` | 事实证据接收与复核清单 | FE-PLAT、FE-MOD、FE-HO、FE-GATE、FE-ACC 接收入口已建，待事实提交 |
| `fact-evidence-submission-packet.md` | 事实证据提交包 | 平台、板块、Handoff、门禁、验收提交模板已建，待填写 |
| `fact-evidence-submission-control-board.md` | 事实证据提交总控表 | 已把 FE-PLAT、FE-MOD、FE-HO、FE-GATE、FE-ACC 的提交顺序、依赖和复核入口统一到一张表 |
| `fact-evidence-next-batch-runbook.md` | 下一轮事实证据批次执行单 | FE-BATCH-001 至 FE-BATCH-005 已定义；FE-GATE 和 FE-ACC 已完成不触发核查，后续只在前置事实满足后再触发 |
| `fact-evidence-next-batch-run-record.md` | 下一轮事实证据批次执行记录 | FE-BATCH-001 至 FE-BATCH-003 已核查但未接收；FE-BATCH-004 和 FE-BATCH-005 已核查但不触发；首次真实联调和第一阶段验收继续 No-Go |
| `pre-gate-fact-readiness-matrix.md` | 前置事实就绪矩阵 | 已汇总 FE-PLAT、FE-MOD、FE-HO 是否具备触发 FE-GATE 的前置条件；当前全部未就绪 |
| `gate-trigger-decision-record.md` | FE-GATE 触发判定记录 | 已登记 GATE-TRG-001；当前不触发 FE-GATE，不启动 FR-GATE，不解除首次真实联调 No-Go |
| `gate-fact-evidence-run-record.md` | FE-GATE 事实证据执行记录 | 已核查 FE-GATE-001 触发条件；前置事实未通过，不启动 FR-GATE |
| `acceptance-fact-evidence-run-record.md` | 验收事实证据执行记录 | 已核查 FE-ACC-011 至 FE-ACC-013；尚无验收触发事实，不启动 FR-ACC |
| `real-fact-capture-action-pack.md` | 真实事实采集动作包 | 已统一 FE-PLAT、FE-MOD、FE-HO、FE-GATE、FE-ACC 的下一阶段最小执行顺序 |
| `real-fact-capture-run-record.md` | 真实事实采集执行记录 | 已执行一次采集核查；未发现可接收平台、板块或 Handoff 事实，不启动 FR-PLAT、FR-MOD、FR-HO |
| `day-1-continuation-run-record.md` | Day 1 接续执行记录 | 2026-07-10 已接续；无新增事实，不触发 FR-PLAT、FR-MOD、FR-HO、FR-GATE、FR-ACC |
| `day-1-fact-gap-closure-run-record.md` | Day 1 事实缺口关闭执行记录 | 已核查 P0 缺口；无可关闭 P0，下一步先补 FE-PLAT-001 至 FE-PLAT-005 |
| `day-1-platform-submission-control-record.md` | Day 1 平台事实提交控制记录 | 已控制平台事实提交包；五项未齐时不得写为待复核 |
| `fact-evidence-review-run-log.md` | 事实证据复核执行记录 | FR-PLAT、FR-MOD、FR-HO、FR-GATE、FR-ACC 复核记录已建，尚未触发 |
| `fact-evidence-daily-execution.md` | 事实证据日执行清单 | FE 提交优先级已建立，待事实提交 |
| `workspace-evidence-search-log.md` | 工作区事实证据核查记录 | 已核查原型、规范、台账和工程入口；未发现可作为 FE-PLAT 待复核的真实工程证据 |
| `platform-fact-minimum-evidence-checklist.md` | 平台事实最小证据补齐清单 | 已把 FE-BATCH-001 未接收后的缺口压缩为环境路由、权限、账号、数据、返回路径五项最小补齐任务 |
| `platform-fact-submission-worksheet.md` | 平台事实提交工作表 | 已把 FE-PLAT-001 至 FE-PLAT-005 转成可填写字段；当前全部待补事实，不允许提交复核 |
| `platform-fact-minimum-evidence-run-record.md` | 平台五项最小证据执行记录 | 已完成本轮核查；五项均无可接收事实，不触发 FE-PLAT 复核 |
| `platform-route-account-data-evidence-intake.md` | 平台路由账号数据证据接收表 | 已建立路由、临时页、权限、账号、数据和返回路径的接收与退回标准；当前均待提交 |
| `day-1-platform-fact-run-record.md` | Day 1 平台事实执行记录 | 已核查 FE-PLAT-001 至 FE-PLAT-005；五项均待提交，不触发 FR-PLAT |
| `day-1-environment-route-run-record.md` | Day 1 环境与路由事实执行记录 | 已核查 FE-PLAT-001；仅有建议路由和原型，不触发 FR-PLAT-001 |
| `platform-fact-backfill-review-path.md` | 平台事实回填与复核路径控制记录 | 已定义 FE-PLAT-001 从真实证据回填到 FR-PLAT-001 复核的路径；当前仍不得触发 |
| `reply-followup-cadence.md` | 确认补齐节奏表 | 待补齐事项已登记 |
| `reply-update-guide.md` | 确认结果更新指南 | 待后续收敛 |

## 板块事实

| 文件 | 用途 | 当前状态 |
| --- | --- | --- |
| `module-fact-submission-action-pack.md` | 板块事实提交执行包 | 已把 FE-MOD-001 至 FE-MOD-003 的提交前核对、回写顺序和退回条件收敛为可执行动作 |
| `module-fact-submission-worksheet.md` | 板块事实提交工作表 | 已把 FE-MOD-001 至 FE-MOD-003 转成可填写字段；当前全部待补事实，不允许提交复核 |
| `module-fact-evidence-intake.md` | 板块事实接收与退回表 | 已建立 MOD-INTAKE-001 至 MOD-INTAKE-003 接收标准；当前均待提交，不触发 FR-MOD |
| `module-fact-evidence-run-record.md` | 板块事实证据执行记录 | 已核查 FE-MOD-001 至 FE-MOD-003；未发现可接收板块事实，不触发 FR-MOD |

## Handoff

| 文件 | 用途 | 当前状态 |
| --- | --- | --- |
| `handoff-operating-mechanism.md` | Handoff 运行机制 | 已改为 agent 协同机制 |
| `handoff-log.md` | Handoff 交接记录 | 表单已建，事实 Handoff 待补齐 |
| `handoff-completion-action-pack.md` | Handoff 补齐执行包 | 已把 SP-H002 至 SP-H004 的补齐字段、回写文件、退回条件和门禁影响收敛为可执行动作 |
| `handoff-fact-submission-worksheet.md` | Handoff 事实提交工作表 | 已把 FE-HO-001 至 FE-HO-003 转成可填写字段；当前全部待补事实，不允许提交复核 |
| `handoff-fact-evidence-intake.md` | Handoff 事实接收与退回表 | 已建立 HO-INTAKE-001 至 HO-INTAKE-003 接收标准；当前均待提交，不触发 FR-HO |
| `handoff-fact-evidence-run-record.md` | Handoff 事实证据执行记录 | 已核查 FE-HO-001 至 FE-HO-003；未发现可接收 Handoff 事实，不触发 FR-HO |
| `round-1-handoff-forms.md` | 三大核心服务首轮 Handoff 表单 | 待板块 Agent 补齐 |
| `handoff-quality-review.md` | Handoff 质量复核清单 | 未通过，首次真实联调 No-Go |
| `module-intake-cards.md` | 板块接入卡 | 待补齐 |

## 启动会与联调

| 文件 | 用途 | 当前状态 |
| --- | --- | --- |
| `round-1-readiness-report.md` | 第一轮准备度报告 | 待同步为 agent 模式 |
| remaining-8-percent-action-pack.md | 剩余 8% 人类可执行行动包 | 已把平台事实、板块确认、Handoff 和门禁压缩为四大动作 |
| `round-1-signoff-checklist.md` | 第一轮签核清单 | 待同步为项目负责人签核 + agent 证据复核 |
| `round-1-kickoff-invitation.md` | 启动会确认包 | 待同步为本地确认包 |
| `round-1-premeeting-checklist.md` | 会前材料核对清单 | 待同步为 agent 模式 |
| `round-1-kickoff-meeting-minutes.md` | 启动会纪要 | 待同步为项目负责人裁决和 agent 行动项 |
| `kickoff-action-tracker.md` | 启动会行动项跟踪 | 待同步为 agent 行动项 |
| `kickoff-to-first-integration-transition.md` | 启动会到首次联调转换 | 待同步为确认/补齐/门禁复核 |
| `first-integration-go-checklist.md` | 首次真实联调 Go 判定清单 | No-Go |
| `round-1-integration-schedule.md` | 首次联调日程 | 不得启动真实联调 |
| `round-1-integration-run-record.md` | 首次联调记录 | 尚无真实记录 |
| `first-integration-to-issue-closure-transition.md` | 首次联调到问题关闭转换 | 尚未触发 |
| `round-1-issue-closure-tracker.md` | 问题关闭跟踪 | 尚未触发 |

## 平台与验收

| 文件 | 用途 | 当前状态 |
| --- | --- | --- |
| `integration-checklist.md` | 接口与联调清单 | 平台条件已建字段，待事实证据 |
| `platform-condition-evidence-runbook.md` | 平台条件证据关闭运行表 | EV-PLAT-001 至 EV-PLAT-005 已建字段，待事实证据 |
| `platform-fact-submission-action-pack.md` | 平台事实提交执行包 | 已把 FE-PLAT-001 至 FE-PLAT-005 的提交前核对、回写顺序和退回条件收敛为可执行动作 |
| `platform-fact-minimum-evidence-checklist.md` | 平台事实最小证据补齐清单 | FE-PLAT-001 至 FE-PLAT-005 的最小事实字段、可接受证据、不可接受内容和回写文件已明确 |
| `platform-fact-submission-worksheet.md` | 平台事实提交工作表 | FE-PLAT-001 至 FE-PLAT-005 的提交字段已建，当前保持待补事实 |
| `routing-and-temporary-page-spec.md` | 路由与临时承接页规格 | 临时页策略已允许，路径待补齐；接收入口已接到 `platform-route-account-data-evidence-intake.md` |
| `test-accounts-and-data.md` | 测试账号与测试数据清单 | 待平台 Agent 补齐；接收入口已接到 `platform-route-account-data-evidence-intake.md` |
| `acceptance-evidence-register.md` | 验收证据登记 | EV-001 至 EV-013 已建编号，待真实证据 |
| `phase-1-acceptance-checklist.md` | 第一阶段验收清单 | 触发条件和 Go/No-Go 口径已建，仍 No-Go |
| `phase-1-acceptance-run-record.md` | 第一阶段验收执行记录 | 执行字段已建，待真实验收 |
| `integration-to-acceptance-transition.md` | 联调到验收转换 | 触发条件已建，尚未触发 |

## 当前第一阶段阻塞

| 编号 | 阻塞 | 当前处理文件 | 处理 Agent |
| --- | --- | --- | --- |
| SP-I001 | 总架构推进职责已回写，平台和板块责任边界待补齐 | `owner-roster.md`、`round-1-signoff-checklist.md`、`integration-checklist.md`、`module-intake-cards.md` | 文档 Agent / 平台 Agent / 板块 Agent |
| SP-I002 | 平台集成范围、路由、账号、数据未补齐 | `integration-checklist.md`、`test-accounts-and-data.md` | 平台 Agent |
| SP-I003 | 三个核心服务 Handoff 未补齐 | `round-1-handoff-forms.md`、`handoff-quality-review.md` | 板块 Agent、审计 Agent |
| SP-I005 | 第一轮联调测试账号和测试数据尚未准备 | `test-accounts-and-data.md` | 平台 Agent |
| SP-I006 | 三大核心服务第一阶段主动作仅有推荐项，未完成完整回写 | `core-service-main-action-confirmation.md` | 板块 Agent |

## 当前 Go / No-Go

| 阶段 | 判断 | 依据 |
| --- | --- | --- |
| 第一轮联调启动会 | Go | `round-1-readiness-report.md`、`phase-gate-status.md` |
| 首次真实联调 | No-Go | OUT-001 首轮确认已登记，但平台条件、Handoff、测试账号数据和质量复核仍未完成 |
| 第一阶段验收 | No-Go | 验收证据编号和执行字段已建，但尚无联调记录、问题关闭结论和真实验收证据 |

## 下一次推进动作

| 优先级 | 动作 | 处理 Agent | 目标文件 |
| --- | --- | --- | --- |
| P0 | 按下一轮批次补齐平台条件、板块确认和 Handoff | 平台 Agent / 板块 Agent / 审计 Agent | `real-fact-capture-action-pack.md`、`real-fact-capture-run-record.md`、`fact-evidence-next-batch-runbook.md`、`fact-evidence-next-batch-run-record.md`、`pre-gate-fact-readiness-matrix.md`、`gate-trigger-decision-record.md`、`gate-fact-evidence-run-record.md`、`acceptance-fact-evidence-run-record.md`、`platform-fact-minimum-evidence-checklist.md`、`platform-fact-submission-worksheet.md`、`platform-fact-minimum-evidence-run-record.md`、`platform-route-account-data-evidence-intake.md`、`module-fact-submission-worksheet.md`、`module-fact-evidence-intake.md`、`module-fact-evidence-run-record.md`、`handoff-fact-submission-worksheet.md`、`handoff-fact-evidence-intake.md`、`handoff-fact-evidence-run-record.md`、`p0-evidence-closure-queue.md`、`p0-evidence-execution-log.md`、`fact-evidence-daily-execution.md`、`fact-evidence-submission-control-board.md`、`fact-evidence-submission-packet.md`、`fact-evidence-intake-review.md`、`fact-evidence-review-run-log.md`、`workspace-evidence-search-log.md`、`platform-fact-submission-action-pack.md`、`module-fact-submission-action-pack.md`、`platform-condition-evidence-runbook.md`、`integration-checklist.md`、`test-accounts-and-data.md`、`round-1-handoff-forms.md` |
| P0 | 补齐 EXT-003、EXT-004、EXT-005 Handoff 缺口 | 板块 Agent | `handoff-completion-action-pack.md`、`handoff-fact-submission-worksheet.md`、`handoff-fact-evidence-intake.md`、`handoff-fact-evidence-run-record.md`、`round-1-handoff-forms.md`、`handoff-quality-review.md` |
| P0 | 补齐 EXT-007 平台条件 | 平台 Agent | `platform-fact-submission-action-pack.md`、`platform-condition-evidence-runbook.md`、`integration-checklist.md`、`test-accounts-and-data.md`、`routing-and-temporary-page-spec.md` |
| P0 | 补齐 EXT-008 验收责任和证据要求 | 验收 Agent | `integration-to-acceptance-transition.md`、`phase-1-acceptance-checklist.md`、`acceptance-evidence-register.md`、`phase-1-acceptance-run-record.md` |
| P0 | 形成 OUT001-FU 补齐证据 | 执行 Agent | `out-001-followup-evidence-register.md`、`reply-followup-cadence.md`、`blocker-escalation-decision-log.md` |
| P0 | 复核首次真实联调是否仍 No-Go | 审计 Agent | `first-integration-go-checklist.md`、`phase-gate-status.md` |
| P0 | 审计台账一致性和门禁证据 | 审计 Agent | `consistency-and-gate-audit.md` |

## 关联决策

| 决策 | 作用 |
| --- | --- |
| `docs/decisions/0003-allow-temporary-landing-pages-for-round-1-integration.md` | 允许第一轮联调使用临时承接页，解除正式页面未完成造成的联调阻塞 |
