# 服务广场 Agent 协同配置清单

日期：2026-07-09

本项目当前按单人决策、agent 协同推进，不再要求建立多人项目群、外部协作工具或复杂工作台。唯一状态基准是本地项目台账；agent 之间通过文件、门禁和审计记录完成交接。

## 一、当前结论

| 项目 | 当前状态 | 说明 |
| --- | --- | --- |
| 项目参与方式 | 单人决策 | 当前只有项目负责人一人参与 |
| 协作方式 | Agent 协同 | 由不同 agent/工作流围绕本地台账持续推进 |
| 主入口 | 已确定 | `START-HERE.md` |
| Agent 接续看板 | 已确定 | `agent-coordination-board.md` |
| 总看板 | 已确定 | `current-week-command-board.md`、`progress-board.md` |
| 问题池 | 已确定 | `issue-pool.md` |
| Handoff 入口 | 已确定 | `handoff-log.md`、`round-1-handoff-forms.md`、`handoff-quality-review.md` |
| 门禁依据 | 已确定 | `phase-gate-status.md`、`phase-gate-evidence-matrix.md` |
| 外部工具 | 不强制 | 不需要飞书、企业微信、钉钉、Jira 或禅道 |

## 二、Agent 分工

| Agent 角色 | 职责 | 主要文件 |
| --- | --- | --- |
| 规划 Agent | 拆阶段、排优先级、维护下一步动作 | `START-HERE.md`、`current-week-command-board.md`、`phase-progress-report.md` |
| 执行 Agent | 按清单推进确认、补齐、Handoff、联调、验收 | `day-0-execution-record.md`、`day-0-dispatch-to-gate-run-log.md`、`handoff-operating-mechanism.md` |
| 文档 Agent | 更新规范、模板、记录和状态摘要 | `day-0-end-of-day-summary.md`、`daily-standup-log.md`、`project-status-one-page.md` |
| 审计 Agent | 检查台账一致性、证据充分性和门禁结论 | `consistency-and-gate-audit.md`、`phase-gate-evidence-matrix.md` |
| 决策 Agent | 识别需要项目负责人裁决的事项 | `blocker-escalation-decision-log.md`、`docs/decisions/` |

## 三、最小运行规则

| 规则 | 要求 |
| --- | --- |
| 一个主入口 | 所有 agent 先读 `START-HERE.md` |
| 一个接续看板 | 所有 agent 再读 `agent-coordination-board.md` |
| 一个当前状态 | 以 `project-status-one-page.md` 和 `phase-gate-status.md` 为准 |
| 一个看板 | 以 `current-week-command-board.md` 管理下一步 |
| 一个问题池 | 阻塞进入 `issue-pool.md` 或 `blocker-escalation-decision-log.md` |
| 一个 Handoff 机制 | 交接以 `handoff-log.md`、`round-1-handoff-forms.md` 和 `handoff-quality-review.md` 为准 |
| 一个门禁结论 | 是否联调、是否验收只看 `phase-gate-status.md` 和 `phase-gate-evidence-matrix.md` |

## 四、Agent 交接格式

每次 agent 接续推进时，只需要留下以下信息：

```text
本次处理日期：
处理 Agent：
处理范围：
已完成：
未完成：
当前阻塞：
门禁是否变化：是 / 否
新的门禁结论：
下一步建议：
已更新文件：
```

## 五、不再需要的内容

| 原方案 | 当前处理 |
| --- | --- |
| 建立项目群或频道 | 不需要 |
| 指定飞书、企业微信、钉钉、Jira 或禅道 | 不需要 |
| 多负责人每日同步 | 不需要 |
| 成员清单和群主配置 | 不需要 |
| 工具内复杂字段配置 | 不需要 |
| 群聊截图作为管理证据 | 不需要 |

## 六、保留的必要证据

虽然不需要多人协作工具，但以下证据仍必须保留：

| 证据 | 用途 |
| --- | --- |
| 执行记录 | 证明某项动作是否完成 |
| Handoff 记录 | 证明交接是否完整 |
| 联调记录 | 证明是否具备问题关闭和验收前提 |
| 验收记录 | 证明是否通过阶段验收 |
| 门禁矩阵 | 证明 Go / Partial Go / No-Go 结论 |

## 七、当前结论

截至 2026-07-09，本项目采用单人决策、agent 协同、本地台账推进方式。无需配置外部协作工具；后续只需保持本地台账、Handoff、问题池、门禁矩阵和日终摘要一致。首次真实联调和第一阶段验收仍保持 No-Go。
