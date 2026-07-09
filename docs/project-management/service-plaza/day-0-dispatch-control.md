# 服务广场 Day 0 确认控制表

日期：2026-07-09

本文件用于控制服务广场 Day 0 第一批 P0 确认事项的登记、证据、回写和门禁复核。当前项目为单人决策模式，不再要求外部多人发送和回执。它不替代 `communication-message-pack.md`、`outbound-message-dispatch-log.md`、`external-confirmation-tracker.md` 和 `day-0-dispatch-to-gate-run-log.md`，只负责把确认动作串成可执行闭环。

## 一、当前执行结论

| 项目 | 当前状态 | 结论 |
| --- | --- | --- |
| 确认材料 | 已具备 | 可从 `out-001-dispatch-runbook.md`、台账和模板读取 |
| 确认批次 | 已定义 | 使用 OUT-001 |
| 确认方式 | 已收敛 | 项目负责人本地确认，不要求外部工具 |
| 确认人 | 已确认 | 项目负责人或 agent |
| 处理截止时间 | 未确认 | 确认时必须写明 |
| 确认后回写 | 未执行 | 必须同步更新确认日志和确认事项跟踪表 |
| 确认到门禁流水 | 未执行 | 必须同步更新 `day-0-dispatch-to-gate-run-log.md` |
| 当前门禁 | No-Go | 仅允许确认和补齐，不允许进入首次真实联调 |

## 二、确认前 10 分钟核对

| 顺序 | 核对项 | 通过标准 | 未通过处理 |
| --- | --- | --- | --- |
| 1 | 当前口径是否一致 | `project-status-one-page.md`、`phase-gate-status.md`、`phase-gate-evidence-matrix.md` 结论一致 | 先回写一致性审计 |
| 2 | OUT-001 批次是否确认 | `outbound-message-dispatch-log.md` 已列出确认事项和编号 | 补齐批次表 |
| 3 | 消息文本是否确认 | 从 `out-001-dispatch-runbook.md`、`communication-message-pack.md` 或指定模板复制 | 不允许临场改口径 |
| 4 | 确认人是否确认 | 明确项目负责人或本轮 agent | 未确认则不得标记已确认 |
| 5 | 确认方式是否确认 | 本地台账确认、备注记录或证据编号 | 未形成记录不得标记已确认 |
| 6 | 处理截止时间是否确认 | 每条 P0 确认项都有明确处理时间 | 没有截止时间不得关闭 |

## 三、OUT-001 确认控制表

| 编号 | 确认项 | 信息来源 | 必填确认信息 | 确认后第一回写 | 第二回写 | 未完成处理 |
| --- | --- | --- | --- | --- | --- | --- |
| EXT-001 | 架构负责人职责 | `collaboration-tool-setup.md` | 确认人、确认时间、处理截止时间 | `outbound-message-dispatch-log.md` | `external-confirmation-tracker.md` | 未确认不得解除负责人阻塞 |
| EXT-002 | 第一轮范围和启动方式 | `project-status-one-page.md` | 确认人、确认时间、处理截止时间 | `outbound-message-dispatch-log.md` | `external-confirmation-tracker.md` | 未确认不得正式召开启动会 |
| EXT-003 | 生命导航主动作和 Handoff | `core-service-main-action-confirmation.md` | 确认人、确认时间、处理截止时间 | `outbound-message-dispatch-log.md` | `reply-intake-tracker.md` | 未补齐不得进入生命导航 Partial Go |
| EXT-004 | 俱乐部联盟主动作和 Handoff | `core-service-main-action-confirmation.md` | 确认人、确认时间、处理截止时间 | `outbound-message-dispatch-log.md` | `reply-intake-tracker.md` | 未补齐不得进入俱乐部联盟 Partial Go |
| EXT-005 | 健康大管家主动作和 Handoff | `core-service-main-action-confirmation.md` | 确认人、确认时间、处理截止时间 | `outbound-message-dispatch-log.md` | `reply-intake-tracker.md` | 未补齐不得进入健康大管家 Partial Go |
| EXT-007 | 平台路由、账号、数据和权限 | `integration-checklist.md` | 确认人、确认时间、处理截止时间 | `outbound-message-dispatch-log.md` | `reply-intake-tracker.md` | 未补齐不得进入首次真实联调 |
| EXT-008 | 验收责任和证据要求 | `phase-1-acceptance-checklist.md` | 确认人、确认时间、处理截止时间 | `outbound-message-dispatch-log.md` | `reply-intake-tracker.md` | 未补齐不得进入第一阶段验收 |

## 四、确认后 30 分钟回写动作

| 顺序 | 动作 | 回写文件 | 完成标准 |
| --- | --- | --- | --- |
| 1 | 登记每条确认项的确认时间、确认人、处理截止时间 | `outbound-message-dispatch-log.md` | OUT-001 每条记录不再是待定 |
| 2 | 将对应确认事项改为已确认或待补齐 | `external-confirmation-tracker.md` | EXT-001 至 EXT-008 状态和截止时间已更新 |
| 3 | 更新 Day 0 执行记录 | `day-0-execution-record.md` | 第一批确认结果有真实时间和证据编号 |
| 4 | 更新确认到门禁流水 | `day-0-dispatch-to-gate-run-log.md` | 每个 EXT 的确认、证据、回写和门禁状态有记录 |
| 5 | 设定未补齐动作 | `reply-followup-cadence.md` | 每个 P0 缺口有下一步动作 |
| 6 | 复核门禁证据 | `phase-gate-evidence-matrix.md` | EVD-GAP-001 可按真实确认情况更新 |
| 7 | 执行一致性审计 | `consistency-and-gate-audit.md` | 审计记录说明门禁是否变化 |

## 五、确认到台账的最短路径

| 确认来源 | 第一登记 | 质量判断 | 台账回写 | 门禁影响 |
| --- | --- | --- | --- | --- |
| 项目负责人确认 | `reply-intake-tracker.md` | 是否明确当前由项目负责人临时承担总架构推进职责 | `owner-roster.md`、`round-1-signoff-checklist.md` | 影响首次真实联调 |
| 启动方式确认 | `reply-intake-tracker.md` | 是否确认范围、启动会和临时承接页策略 | `round-1-kickoff-invitation.md`、`phase-gate-status.md` | 影响正式启动会 |
| 板块事项确认 | `reply-intake-tracker.md` | 是否确认主动作、页面、权限、Handoff 缺口 | `module-intake-cards.md`、`core-service-main-action-confirmation.md`、`round-1-handoff-forms.md` | 影响 Partial Go |
| 平台事项确认 | `reply-intake-tracker.md` | 是否确认路由、账号、数据、权限、环境缺口 | `integration-checklist.md`、`routing-and-temporary-page-spec.md`、`test-accounts-and-data.md` | 影响首次真实联调 |
| 验收事项确认 | `reply-intake-tracker.md` | 是否确认验收责任和验收方式 | `phase-1-acceptance-checklist.md`、`acceptance-evidence-register.md` | 影响第一阶段验收 |

## 六、当天结束判断

| 判断项 | Go 条件 | 当前结论 |
| --- | --- | --- |
| Day 0 是否完成 | OUT-001 已真实确认、已登记、已设置补齐动作、已复核门禁 | 未完成 |
| 是否可以召开启动会 | Day 0 确认登记完成，启动会准备确认完成，会前清单通过 | Conditional Go |
| 是否可以启动首次真实联调 | 负责人、主动作、路由、账号、数据、Handoff 均通过 | No-Go |
| 是否可以进入第一阶段验收 | 联调记录、问题关闭和验收证据完整 | No-Go |

## 七、当前结论

截至 2026-07-09，Day 0 确认控制表已收敛为单人确认模式，OUT-001 逐条确认执行包见 `out-001-dispatch-runbook.md`，确认到门禁流水见 `day-0-dispatch-to-gate-run-log.md`。下一步必须完成本地确认、确认登记、确认事项状态更新、流水更新和缺口补齐设置；在这些事实证据形成前，不得启动首次真实联调或第一阶段验收。
