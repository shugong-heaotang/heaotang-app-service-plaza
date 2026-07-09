# 服务广场第一轮确认口径包

本文件用于给项目负责人和后续 agent 提供统一确认口径。当前项目按单人决策、agent 协同和本地台账推进，不要求把以下内容发送给多人，也不要求配置外部协作工具。

## 一、当前总口径

| 项目 | 口径 |
| --- | --- |
| 第一轮联调启动会 | 材料已具备，可继续做启动会准备确认 |
| 首次真实联调 | 暂不启动，需先补齐负责人、主动作、路由、账号、数据和 Handoff 质量复核 |
| 第一阶段验收 | 暂不进入，需等待真实联调记录、问题关闭结论和验收证据 |
| 协同方式 | 项目负责人确认，agent 按本地台账接续推进 |
| 外部工具 | 不强制使用飞书、企业微信、钉钉、Jira 或禅道 |

## 二、项目负责人确认项

| 确认项 | 推荐结论 | 回写文件 |
| --- | --- | --- |
| 是否由项目负责人临时承担总架构推进职责 | 是，当前按单人决策模式推进 | `owner-roster.md`、`round-1-signoff-checklist.md` |
| 是否继续推进第一轮启动会准备 | 是，但不解除真实联调 No-Go | `phase-gate-status.md`、`day-0-to-kickoff-transition.md` |
| 是否允许 agent 按板块责任边界推进台账 | 是 | `collaboration-tool-setup.md`、`agent-coordination-board.md` |
| 是否允许临时承接页作为第一轮默认方案 | 是，按 ADR 0003 执行 | `routing-and-temporary-page-spec.md` |

## 三、三大核心服务确认项

第一轮只做主链路，不要求完整业务闭环。推荐主动作如下：

| 板块 | 推荐主动作 | 当前确认要求 | 回写文件 |
| --- | --- | --- | --- |
| 生命导航 | 提交导航申请 | 确认主动作、页面或路由、权限、测试数据、Handoff 缺口 | `core-service-main-action-confirmation.md`、`round-1-handoff-forms.md` |
| 俱乐部联盟 | 申请加入俱乐部 | 确认主动作、页面或路由、权限、测试数据、Handoff 缺口 | `core-service-main-action-confirmation.md`、`round-1-handoff-forms.md` |
| 健康大管家 | 提交健康咨询 | 确认主动作、页面或路由、权限、测试数据、Handoff 缺口 | `core-service-main-action-confirmation.md`、`round-1-handoff-forms.md` |

## 四、平台确认项

| 确认项 | 当前要求 | 回写文件 |
| --- | --- | --- |
| 服务广场入口路由 | 需要形成可访问路径或临时承接页路径 | `routing-and-temporary-page-spec.md` |
| 三大核心服务路由 | 正式页面或临时承接页路径必须明确 | `routing-and-temporary-page-spec.md` |
| 权限处理 | 未登录、无权限、普通会员、管理或审核状态必须可测 | `test-accounts-and-data.md` |
| 测试账号 | 不在仓库写真实密码，只登记账号状态和保管方式 | `test-accounts-and-data.md` |
| 测试数据 | 正常、空状态、异常状态至少有可验证方案 | `test-accounts-and-data.md` |
| 返回路径 | 核心服务返回服务广场方式必须明确 | `integration-checklist.md` |

## 五、确认后处理

每完成一项确认，按以下顺序处理：

1. 在 `outbound-message-dispatch-log.md` 登记确认批次。
2. 在 `external-confirmation-tracker.md` 更新确认状态。
3. 在 `reply-intake-tracker.md` 登记确认结果。
4. 在 `reply-processing-batch-log.md` 记录处理批次。
5. 按 `reply-completeness-review.md` 判断字段是否完整。
6. 按 `reply-ledger-update-checklist.md` 回写目标台账。
7. 用 `reply-to-gate-transition.md` 和 `first-integration-go-checklist.md` 判断是否仍为 No-Go。
8. 未补齐时按 `reply-followup-cadence.md` 进入补齐节奏，必要时登记 `blocker-escalation-decision-log.md`。
