# 服务广场事实证据提交总控表

日期：2026-07-10

本文件用于统一调度 FE-PLAT、FE-MOD、FE-HO、FE-GATE 和 FE-ACC 的事实证据提交顺序。它只登记提交顺序、依赖关系、回写入口和门禁影响，不替代真实事实证据。

## 一、总控原则

1. 先补平台事实，再补板块事实，再补 Handoff 事实，最后触发门禁复核。
2. 平台、板块、Handoff 各自必须先通过对应执行包的提交前核对。
3. 任一 FE 项未提交时，不得把对应 P0-RUN 改为“证据已形成”。
4. 任一 FE 项进入待复核，只表示可以审计，不表示 Go 或 Partial Go。
5. 首次真实联调必须等 P0-PLAT、P0-MOD、P0-HO 均有足够事实后再复核。

## 二、总控队列

| 顺序 | FE 范围 | 执行包 | 必须先完成 | 提交入口 | 复核入口 | 当前状态 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | FE-PLAT-001 至 FE-PLAT-005 | `platform-fact-submission-action-pack.md`、`platform-fact-submission-worksheet.md`、`day-1-platform-submission-control-record.md`、`platform-fact-backfill-review-path.md` | 工作区事实核查；环境、路由、权限、账号、数据、返回路径事实 | `fact-evidence-submission-packet.md` 平台事实提交包 | `fact-evidence-intake-review.md`、`fact-evidence-review-run-log.md` | 待提交 |
| 2 | FE-MOD-001 至 FE-MOD-003 | `module-fact-submission-action-pack.md`、`module-fact-submission-worksheet.md` | 主动作、页面方案、权限、后台处理、测试数据、验收责任事实 | `fact-evidence-submission-packet.md` 板块事实提交包 | `fact-evidence-intake-review.md`、`fact-evidence-review-run-log.md` | 待提交 |
| 3 | FE-HO-001 至 FE-HO-003 | `handoff-completion-action-pack.md`、`handoff-fact-submission-worksheet.md` | 对应 FE-MOD 事实提交；SP-H002 至 SP-H004 完整 Handoff | `fact-evidence-submission-packet.md` Handoff 事实提交包 | `handoff-quality-review.md`、`fact-evidence-intake-review.md`、`fact-evidence-review-run-log.md` | 待提交 |
| 4 | FE-GATE-001 | `pre-gate-fact-readiness-matrix.md`、`gate-trigger-decision-record.md`、`first-integration-go-checklist.md` | FE-PLAT、FE-MOD、FE-HO 完成提交并通过必要复核，且 GATE-TRG 判定允许触发 | `fact-evidence-submission-packet.md` 门禁事实提交包 | `fact-evidence-review-run-log.md`、`phase-gate-evidence-matrix.md`、`phase-gate-status.md` | 不触发，等待前置 |
| 5 | FE-ACC-011 至 FE-ACC-013 | `integration-to-acceptance-transition.md`、`phase-1-acceptance-run-record.md` | 首次真实联调、问题关闭和验收触发条件形成 | `fact-evidence-submission-packet.md` 验收事实提交包 | `fact-evidence-review-run-log.md`、`acceptance-evidence-register.md`、`phase-gate-evidence-matrix.md` | 等待前置 |

## 三、依赖关系

| 依赖 | 说明 | 未满足时处理 |
| --- | --- | --- |
| FE-HO 依赖 FE-MOD | Handoff 必须基于已确认的板块主动作、页面方案、权限、后台处理和验收责任 | FE-HO 保持待提交 |
| FE-GATE 依赖 FE-PLAT、FE-MOD、FE-HO 和触发判定 | 首次真实联调门禁必须同时看平台、板块、Handoff 和 `gate-trigger-decision-record.md` | FE-GATE 保持不触发，等待前置 |
| FE-ACC 依赖 FE-GATE 和真实联调记录 | 验收不能先于联调、问题关闭和验收触发条件 | FE-ACC 保持等待前置 |
| Partial Go 依赖单板块完整证据 | 单板块也必须同时满足平台、板块和 Handoff 条件 | 不满足则保持整体 No-Go |

## 四、退回路径

| 退回来源 | 退回到 | 处理方式 |
| --- | --- | --- |
| 平台事实字段不完整 | `platform-fact-submission-action-pack.md` | 补环境、路由、权限、账号、数据或返回路径 |
| 板块事实字段不完整 | `module-fact-submission-action-pack.md` | 补主动作、页面方案、权限、后台处理、数据和验收责任 |
| Handoff 字段不完整 | `handoff-completion-action-pack.md`、`handoff-quality-review.md` | 补提交、接收、依赖、阻塞、下一步动作和平台可接收结论 |
| 门禁证据不充分 | `phase-gate-evidence-matrix.md`、`first-integration-go-checklist.md` | 继续 No-Go，并回到对应 FE 队列 |
| 验收证据不充分 | `acceptance-evidence-register.md`、`phase-1-acceptance-run-record.md` | 第一阶段验收继续 No-Go |

## 五、当前结论

截至 2026-07-10，事实证据提交总控表已建立，并已接入 `day-1-platform-submission-control-record.md` 的平台事实提交前控制和 `platform-fact-backfill-review-path.md` 的 FE-PLAT-001 回填复核路径。FE-PLAT、FE-MOD、FE-HO 均已有提交工作表、提交执行包和复核入口，但尚未提交真实事实证据；FE-GATE 必须先按 `pre-gate-fact-readiness-matrix.md` 判断前置事实是否就绪，并在 `gate-trigger-decision-record.md` 形成允许触发判定后才能进入 FR-GATE。当前 GATE-TRG-001 判定为不触发。FE-ACC 已按 `acceptance-fact-evidence-run-record.md` 完成触发核查，但因缺少真实联调、问题关闭、FE-GATE 复核和验收执行事实，不启动 FR-ACC。首次真实联调保持 No-Go；第一阶段验收保持 No-Go。
