# 服务广场启动确认后台账更新动作表

本文件用于启动确认后逐项更新项目台账。当前“启动会”不代表多人会议事实，只有形成真实确认记录和证据后，才允许回写为已完成。

## 一、启动确认后更新动作

| 顺序 | 动作 | 目标文件 | 责任角色 | 状态 |
| --- | --- | --- | --- | --- |
| 1 | 回写总架构推进职责 | `owner-roster.md`、`round-1-signoff-checklist.md`、`role-action-list.md` | 文档 Agent | RPLY-001 已确认，已回写 |
| 2 | 更新签核结论 | `round-1-signoff-checklist.md` | 文档 Agent、审计 Agent | 待处理 |
| 3 | 更新启动确认纪要 | `round-1-kickoff-meeting-minutes.md` | 文档 Agent | 待真实确认 |
| 4 | 更新三大核心服务主动作确认结果 | `core-service-main-action-confirmation.md` | 板块 Agent | 待补齐 |
| 5 | 更新正式页面或临时承接页路径 | `routing-and-temporary-page-spec.md` | 平台 Agent | 待补齐 |
| 6 | 更新测试账号和测试数据准备责任 | `test-accounts-and-data.md` | 平台 Agent | 待补齐 |
| 7 | 更新首轮 Handoff 状态 | `round-1-handoff-forms.md` | 板块 Agent | 待补齐 |
| 8 | 更新问题池状态 | `issue-pool.md` | 文档 Agent | 待处理 |
| 9 | 登记启动确认后行动项 | `kickoff-action-tracker.md` | 文档 Agent | 待处理 |
| 10 | 更新阶段门禁状态 | `phase-gate-status.md` | 审计 Agent | No-Go |
| 11 | 更新准备度报告结论 | `round-1-readiness-report.md` | 审计 Agent | No-Go |

## 二、Go / No-Go 更新规则

| 条件 | 判断 |
| --- | --- |
| 责任、主动作、路由、账号、数据、Handoff 均确认且通过质量复核 | 首次真实联调可从 No-Go 改为 Go |
| 单个核心服务完整满足条件，平台条件可支持该服务 | 可评估该服务 Partial Go |
| 任一核心服务责任边界未确认 | 该板块不能进入真实联调 |
| 测试账号或数据未准备 | 只能继续准备，不能真实联调 |
| Handoff 未提交或未通过质量复核 | 对应板块不能进入真实联调 |
| 启动行动项未登记 | 启动确认不解除门禁，先补 `kickoff-action-tracker.md` |

## 三、更新汇总模板

```text
启动确认日期：
已回写责任台账：
已完成主动作确认：
已确认路由或临时承接页：
已确认测试账号和数据：
已完成首轮 Handoff：
已登记启动行动项：
是否允许启动首次真实联调：
下一步动作：
```
