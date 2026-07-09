# 服务广场确认结果到门禁转换规则

本文件用于把责任边界确认、核心服务确认和平台联调环境确认转换成明确的 Go / Partial Go / No-Go 结论。形成确认结果后，agent 必须按本文件更新台账。

## 一、处理原则

1. 确认结果不是完成，只有确认结果进入对应台账并影响门禁判断，才算完成处理。
2. 所有确认结果必须先按 `reply-completeness-review.md` 完整性复核，再进入门禁转换。
3. 完整确认结果必须先按 `reply-ledger-update-checklist.md` 逐条回写目标台账，再进入 Go / Partial Go / No-Go 判断。
4. 信息不完整的确认结果不能直接解除阻塞，必须标记为“信息不完整”并继续补齐。
5. 首次真实联调可以按三大核心服务分批 Partial Go，但每个进入联调的板块必须满足本板块完整条件。
6. 任何主链路阻塞项必须进入 `issue-pool.md` 或 `round-1-issue-closure-tracker.md`。

## 二、确认类型和转换目标

| 确认类型 | 来源 | 先登记 | 必须更新 | 影响门禁 |
| --- | --- | --- | --- | --- |
| 责任边界 | 项目负责人和 agent 台账确认 | `reply-intake-tracker.md`、`reply-completeness-review.md` | `owner-roster.md`、`round-1-signoff-checklist.md`、`role-action-list.md` | 负责人确认 |
| 核心服务确认 | 生命导航、俱乐部联盟、健康大管家事项 | `reply-intake-tracker.md`、`reply-completeness-review.md` | `core-service-main-action-confirmation.md`、`module-intake-cards.md`、`round-1-handoff-forms.md`、`handoff-quality-review.md` | 主动作和 Handoff 质量复核 |
| 平台联调环境 | 平台条件 | `reply-intake-tracker.md`、`reply-completeness-review.md` | `integration-checklist.md`、`routing-and-temporary-page-spec.md`、`test-accounts-and-data.md` | 路由、账号、数据确认 |
| 启动会签核 | 启动会纪要或本地启动会准备确认 | `round-1-kickoff-meeting-minutes.md` | `round-1-signoff-checklist.md`、`phase-gate-status.md` | 启动会后门禁 |

## 三、完整性判定

### 1. 责任边界完整

| 字段 | 要求 |
| --- | --- |
| 责任边界 | 必填，必须对应唯一职责 |
| 负责范围 | 必填，不能只写“配合” |
| 确认方式 | 必填，本地台账确认或证据编号 |
| 是否有最终确认权 | 必填，是 / 否 |

缺任一字段，状态为“信息不完整”，不能解除负责人阻塞。

### 2. 核心服务确认完整

| 字段 | 要求 |
| --- | --- |
| 服务名称 | 生命导航 / 俱乐部联盟 / 健康大管家 |
| 第一阶段主动作 | 必填，只能有一个主动作 |
| 最小可交付范围 | 必填，必须能支持主动作 |
| 页面方案 | 正式页面 / 临时承接页 / 混合 |
| Handoff 信息 | 必填，至少覆盖需求给开发、开发给联调所需字段，并通过 `handoff-quality-review.md` 复核 |
| 验收责任 | 必填 |

缺主动作、页面方案或 Handoff，不能进入该板块 Partial Go。

### 3. 平台联调环境完整

| 字段 | 要求 |
| --- | --- |
| 服务广场入口路由 | 必填 |
| 三大核心服务路由 | 每个待联调板块必填 |
| 权限规则 | 必填，至少包含普通会员、无权限、管理或审核角色 |
| 测试账号 | 必填，账号必须可登录或说明创建时间；不得在仓库记录真实密码 |
| 测试数据 | 必填，至少包含正常、空状态、异常状态 |
| 临时承接页策略 | 如使用临时页，必须明确页面文案和后续替换责任边界 |

缺路由、账号或测试数据，首次真实联调保持 No-Go。

## 四、转换动作

| 步骤 | 动作 | 处理 Agent | 输出 |
| --- | --- | --- | --- |
| 1 | 在 `reply-intake-tracker.md` 登记确认结果 | 文档 Agent | 状态从待确认变更为已确认或信息不完整 |
| 2 | 按 `reply-completeness-review.md` 判断完整性 | 审计 Agent | 完整、信息不完整、需裁决、不进入第一轮或无效 |
| 3 | 按 `reply-ledger-update-checklist.md` 逐条回写目标台账 | 文档 Agent | 负责人、主动作、Handoff、平台、验收台账形成事实更新 |
| 4 | 按确认类型更新目标台账状态 | 对应 Agent | 台账状态从待确认变更为已确认、信息不完整或待补充 |
| 5 | 更新 `round-1-signoff-checklist.md` | 文档 Agent | 签核项状态更新 |
| 6 | 更新 `first-integration-go-checklist.md` | 审计 Agent | Go / Partial Go / No-Go 重新判断 |
| 7 | 如仍阻塞，登记问题 | 执行 Agent | `issue-pool.md` 或 `round-1-issue-closure-tracker.md` 更新 |
| 8 | 如达到 Go 或 Partial Go，更新联调日程 | 执行 Agent | `round-1-integration-schedule.md` 更新 |

## 五、Partial Go 判定

三大核心服务可以独立判定 Partial Go。

| 板块条件 | 满足后动作 |
| --- | --- |
| 责任边界已确认 | 更新负责人表和签核清单 |
| 主动作已确认 | 更新主动作确认表 |
| 路由已确认且可访问 | 更新路由规格和联调清单 |
| 测试账号和数据可用 | 更新测试账号与数据清单 |
| Handoff 已提交并通过质量复核 | 更新 Handoff 表单和 Handoff 质量复核清单 |

某个板块以上五项全部满足，即可进入该板块 Partial Go。未满足的板块继续 No-Go，不影响已满足板块先联调。

## 六、门禁结论模板

```text
复核日期：
本次处理确认：
已解除阻塞：
仍阻塞事项：
三大核心服务判定：
- 生命导航：Go / Partial Go / No-Go
- 俱乐部联盟：Go / Partial Go / No-Go
- 健康大管家：Go / Partial Go / No-Go
整体结论：Go / Partial Go / No-Go
下一步动作：
处理 Agent：
复核 Agent：
项目负责人确认：
```

## 七、当前结论

截至 2026-07-09，OUT-001 首轮确认结果已登记并完成初步完整性复核：RPLY-001 完整，RPLY-002 至 RPLY-010 信息不完整。由于平台路由、测试账号、测试数据、三大核心服务 Handoff 和验收责任仍未补齐，首次真实联调整体保持 No-Go，单板块 Partial Go 也暂不满足。
