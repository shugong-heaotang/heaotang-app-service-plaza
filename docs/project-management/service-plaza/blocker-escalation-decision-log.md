# 服务广场阻塞补齐与裁决记录

本文件用于记录 P0 阻塞事项的补齐、裁决和回落动作。凡是影响首次真实联调、问题关闭或第一阶段验收的阻塞，超过约定时限未解决时，必须进入本文件。

## 一、适用范围

以下情况必须登记：

1. P0 确认事项超过补齐时限，且已在 `out-001-followup-evidence-register.md` 形成补齐证据。
2. 责任边界、主动作、路由、账号、数据任一关键项长期未确认。
3. Handoff 被质量复核退回后未按时补齐。
4. 首次真实联调失败项影响主链路。
5. 问题关闭缺少责任人、关闭标准或关闭证据。
6. 第一阶段验收缺少证据编号或证据不能证明验收项。
7. 涉及架构边界、公共规则、上线取舍，需要项目负责人裁决。

## 二、处理等级

| 等级 | 触发条件 | 处理人 | 输出 |
| --- | --- | --- | --- |
| L1 补齐 | 确认信息不完整或目标台账缺字段 | 执行 Agent | 补齐记录更新 |
| L2 复核 | 超过 1 个工作日仍未解决 | 审计 Agent | 明确缺口和补齐时间 |
| L3 裁决 | 超过 2 个工作日仍影响主链路 | 项目负责人 | 裁决继续、替代方案、Partial Go 或 No-Go |
| L4 决策记录 | 影响架构边界、上线节奏或责任无人承接 | 项目负责人 / 规划 Agent | ADR、范围调整或延期结论 |

## 三、阻塞总表

| 编号 | 阻塞事项 | 来源文件 | 当前等级 | 处理 Agent | 裁决人 | 当前状态 | 裁决结论 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ESC-001 | 架构和平台责任边界未确认 | `external-confirmation-tracker.md` EXT-001 / EXT-002 | L1 | 规划 Agent | 项目负责人 | 待触发 | 待补充 |
| ESC-002 | 三大核心服务责任边界未确认 | `external-confirmation-tracker.md` EXT-003 至 EXT-005 | L1 | 板块 Agent | 项目负责人 | 已触发缺口检查 | 事实证据待补齐，暂不裁决 |
| ESC-003 | 三大核心服务主动作和 Handoff 未确认 | `core-service-main-action-confirmation.md`、`round-1-handoff-forms.md` | L1 | 板块 Agent | 项目负责人 | 已触发缺口检查 | 事实证据待补齐，暂不裁决 |
| ESC-004 | 平台路由、账号、数据、权限未确认 | `external-confirmation-tracker.md` EXT-007 | L1 | 平台 Agent | 项目负责人 | 已触发缺口检查 | 事实证据待补齐，暂不裁决 |
| ESC-005 | Handoff 质量复核未通过 | `handoff-quality-review.md` | L2 | 审计 Agent | 项目负责人 | 已触发缺口检查 | Handoff 待提交并复核，暂不裁决 |
| ESC-006 | 验收证据缺失或无法证明验收项 | `acceptance-evidence-register.md` | L2 | 验收 Agent | 项目负责人 | 已触发缺口检查 | 验收证据待补齐，暂不裁决 |

## 四、P0 执行流水阻塞映射

| 阻塞编号 | 关联 P0-RUN | 关联补齐证据 | 当前处理 | 是否进入裁决 |
| --- | --- | --- | --- | --- |
| ESC-002 | P0-RUN-006、P0-RUN-007、P0-RUN-008 | OUT001-FU-EXT003-1、OUT001-FU-EXT004-1、OUT001-FU-EXT005-1 | 三大核心服务确认字段已建，事实证据待补齐 | 否 |
| ESC-003 | P0-RUN-006 至 P0-RUN-011 | OUT001-FU-EXT003-1、OUT001-FU-EXT004-1、OUT001-FU-EXT005-1 | 主动作、页面方案和 Handoff 待事实提交 | 否 |
| ESC-004 | P0-RUN-001 至 P0-RUN-005 | OUT001-FU-EXT007-1 | 平台条件字段已建，事实证据待补齐 | 否 |
| ESC-005 | P0-RUN-009、P0-RUN-010、P0-RUN-011 | OUT001-FU-EXT003-1、OUT001-FU-EXT004-1、OUT001-FU-EXT005-1 | Handoff 未通过质量复核，继续 No-Go | 否 |
| ESC-006 | P0-RUN-012 | OUT001-FU-EXT008-1 | EV-011 至 EV-013 已建编号，真实验收证据待补齐 | 否 |

## 五、裁决选项

| 裁决 | 适用场景 | 后续动作 |
| --- | --- | --- |
| 继续补齐 | 缺口明确，只是尚未补齐 | 更新补齐节奏和截止时间 |
| 指定临时责任边界 | 原责任边界无法及时确认 | 更新负责人表和签核清单 |
| Partial Go | 至少一个核心服务满足联调条件 | 更新 Go 判定清单和联调日程 |
| 保持 No-Go | 关键条件缺失，无法联调或验收 | 更新阶段门禁和状态页 |
| 范围降级 | 某板块短期无法完成完整能力 | 更新 MVP 范围和 Handoff |
| 形成 ADR | 涉及架构边界或公共规则 | 新增或更新架构决策记录 |
| 延期处理 | 不阻塞主链路的问题 | 登记延期原因、责任边界和后续阶段 |

## 六、裁决记录模板

```text
裁决编号：
触发日期：
阻塞事项：
来源文件：
当前等级：L1 / L2 / L3 / L4
影响门禁：首次真实联调 / 问题关闭 / 第一阶段验收 / 上线准备
处理 Agent：
裁决人：
已采取动作：
裁决结论：
需要更新的文件：
下一次复核时间：
```

## 七、更新要求

每次补齐或裁决后，必须同步更新：

| 场景 | 必须更新 |
| --- | --- |
| 责任边界变化 | `owner-roster.md`、`round-1-signoff-checklist.md` |
| 确认结果补齐 | `reply-intake-tracker.md`、`reply-to-gate-transition.md` |
| 补齐或裁决证据形成 | `out-001-followup-evidence-register.md`、`reply-followup-cadence.md` |
| Handoff 退回或通过 | `handoff-quality-review.md`、`handoff-log.md` |
| 门禁变化 | `phase-gate-status.md`、`first-integration-go-checklist.md` |
| 联调安排变化 | `round-1-integration-schedule.md` |
| 问题关闭或延期 | `round-1-issue-closure-tracker.md` |
| 验收证据变化 | `acceptance-evidence-register.md`、`phase-1-acceptance-checklist.md` |

## 八、当前结论

截至 2026-07-09，P0 阻塞已形成第一次缺口检查和执行流水映射，但尚未进入真实裁决处理，因为平台、板块、Handoff 和验收事实证据仍未形成。首次真实联调保持 No-Go；第一阶段验收保持 No-Go。
