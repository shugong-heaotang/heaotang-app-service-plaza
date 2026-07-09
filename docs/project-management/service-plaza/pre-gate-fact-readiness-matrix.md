# 服务广场前置事实就绪矩阵

日期：2026-07-09

本文件汇总 FE-GATE-001 之前必须完成的三类前置事实：平台事实、板块事实和 Handoff 事实。它用于判断是否具备触发首次真实联调门禁复核的条件，不替代任何真实事实证据。每次触发或不触发结论必须同步登记到 `gate-trigger-decision-record.md`。

## 一、当前总判断

| 项目 | 当前结论 |
| --- | --- |
| FE-PLAT 是否可复核 | 否，工作表已建，真实平台事实未提交 |
| FE-MOD 是否可复核 | 否，工作表已建，真实板块事实未提交 |
| FE-HO 是否可复核 | 否，工作表已建，真实 Handoff 事实未提交 |
| FE-GATE-001 是否可触发 | 否 |
| 当前触发判定记录 | `gate-trigger-decision-record.md` 已登记 GATE-TRG-001，不触发 |
| 首次真实联调 | No-Go |
| 第一阶段验收 | No-Go |

## 二、前置事实就绪矩阵

| 前置类别 | FE 范围 | 当前工作表 | 提交包入口 | 接收复核入口 | 当前状态 | FE-GATE 影响 |
| --- | --- | --- | --- | --- | --- | --- |
| 平台事实 | FE-PLAT-001 至 FE-PLAT-005 | `platform-fact-submission-worksheet.md` | `fact-evidence-submission-packet.md` 平台事实提交包 | `fact-evidence-intake-review.md`、`fact-evidence-review-run-log.md` | 待补真实环境、路由、权限、账号、数据和返回路径 | 不允许触发 |
| 板块事实 | FE-MOD-001 至 FE-MOD-003 | `module-fact-submission-worksheet.md` | `fact-evidence-submission-packet.md` 板块事实提交包 | `fact-evidence-intake-review.md`、`fact-evidence-review-run-log.md` | 待补三大核心服务主动作、页面方案、权限、后台处理、测试数据和验收责任 | 不允许触发 |
| Handoff 事实 | FE-HO-001 至 FE-HO-003 | `handoff-fact-submission-worksheet.md` | `fact-evidence-submission-packet.md` Handoff 事实提交包 | `handoff-quality-review.md`、`fact-evidence-intake-review.md`、`fact-evidence-review-run-log.md` | 待补 SP-H002 至 SP-H004 真实提交、接收、依赖、阻塞、下一步动作和质量复核结论 | 不允许触发 |

## 三、单板块 Partial Go 前置矩阵

| 板块 | 平台事实 | 板块事实 | Handoff 事实 | 当前判断 |
| --- | --- | --- | --- | --- |
| 生命导航 | FE-PLAT 未通过 | FE-MOD-001 未提交 | FE-HO-001 未提交 | No-Go |
| 俱乐部联盟 | FE-PLAT 未通过 | FE-MOD-002 未提交 | FE-HO-002 未提交 | No-Go |
| 健康大管家 | FE-PLAT 未通过 | FE-MOD-003 未提交 | FE-HO-003 未提交 | No-Go |

## 四、触发 FE-GATE 的最小条件

| 条件 | 当前状态 | 不满足时动作 |
| --- | --- | --- |
| FE-PLAT-001 至 FE-PLAT-005 已提交并通过复核 | 未满足 | 回到 `platform-fact-submission-worksheet.md` 补事实 |
| FE-MOD-001 至 FE-MOD-003 已提交并通过复核 | 未满足 | 回到 `module-fact-submission-worksheet.md` 补事实 |
| FE-HO-001 至 FE-HO-003 已提交并通过复核 | 未满足 | 回到 `handoff-fact-submission-worksheet.md` 补事实 |
| Handoff 质量复核通过 | 未满足 | 回到 `handoff-quality-review.md` 复核或退回 |
| `first-integration-go-checklist.md` 条件完整 | 未满足 | 继续 No-Go |

## 五、回写规则

1. 任一工作表只有字段、没有真实证据位置时，不得进入待复核。
2. 任一 FE 项进入待复核，只表示可以审计，不表示 Go 或 Partial Go。
3. 只有 FE-PLAT、FE-MOD、FE-HO 全部通过必要复核后，才能填写 `fact-evidence-submission-packet.md` 的门禁事实提交包。
4. FE-GATE 触发前，必须先在 `gate-trigger-decision-record.md` 追加允许触发的 GATE-TRG 记录。
5. FE-GATE-001 复核完成后，才允许更新 `phase-gate-evidence-matrix.md`、`first-integration-go-checklist.md` 和 `phase-gate-status.md`。
6. FE-GATE 未触发前，第一阶段验收相关 FE-ACC 继续等待前置。
