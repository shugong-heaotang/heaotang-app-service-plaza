# 服务广场首次联调到问题关闭转换表

日期：2026-07-09

本文件用于把首次真实联调结果转换为问题关闭动作。首次联调结束后，由执行 Agent 整理记录，平台 Agent 判断平台类问题，板块 Agent 补齐板块问题，审计 Agent 复核证据完整性，最终由项目负责人裁决：哪些失败项进入问题池，哪些问题阻塞主链路，哪些可以延期，哪些必须补齐或裁决，以及是否可以进入第一阶段验收准备。

## 一、转换结论

| 项目 | 当前状态 | 结论 |
| --- | --- | --- |
| 首次真实联调 | 未开始 | 尚无真实联调记录 |
| 新增联调问题 | 未产生 | 尚无新增问题编号 |
| 主链路问题关闭 | 未开始 | 现有 P0 阻塞仍未关闭 |
| 问题关闭阶段 | No-Go | 必须先完成真实联调记录和问题登记 |
| 第一阶段验收准备 | No-Go | 无问题关闭结论和验收证据 |

## 二、输入文件

| 输入 | 用途 |
| --- | --- |
| `round-1-integration-run-record.md` | 提取通过项、失败项、新增问题和下一步动作 |
| `issue-pool.md` | 登记影响主链路、接口、权限、路由、账号、数据的问题 |
| `round-1-issue-closure-tracker.md` | 跟踪问题关闭、延期和关闭证据 |
| `blocker-escalation-decision-log.md` | 登记超时、无人负责、架构裁决类问题 |
| `handoff-quality-review.md` | 判断问题是否源于 Handoff 不完整 |
| `integration-to-acceptance-transition.md` | 判断问题关闭后是否可以进入验收转换 |

## 三、联调后 2 小时内必须完成

| 顺序 | 动作 | 推进角色 | 目标文件 | 未完成后果 |
| --- | --- | --- | --- | --- |
| 1 | 填写联调实际记录 | 执行 Agent | `round-1-integration-run-record.md` | 不能进入问题关闭阶段 |
| 2 | 为失败项生成问题编号 | 执行 Agent | `issue-pool.md` | 失败项不可追踪 |
| 3 | 判断是否阻塞主链路 | 平台 Agent、审计 Agent | `round-1-issue-closure-tracker.md` | 不能判断验收门禁 |
| 4 | 指定补齐 Agent 和关闭时间 | 执行 Agent、板块 Agent | `round-1-issue-closure-tracker.md` | 问题不得关闭 |
| 5 | 登记需补齐或裁决事项 | 审计 Agent、项目负责人 | `blocker-escalation-decision-log.md` | P0 阻塞无裁决路径 |
| 6 | 判断 Handoff 是否需要退回 | 审计 Agent | `handoff-quality-review.md` | 问题根因不能闭环 |
| 7 | 复核是否进入验收转换 | 审计 Agent、项目负责人 | `integration-to-acceptance-transition.md` | 第一阶段验收保持 No-Go |

## 四、问题分流规则

| 联调结果 | 判断条件 | 转换动作 | 目标文件 |
| --- | --- | --- | --- |
| 路径通过 | 实际结果符合预期且有本地台账证据 | 登记通过项和证据位置 | `round-1-integration-run-record.md`、`acceptance-evidence-register.md` |
| 路径失败且阻塞主链路 | 入口不可达、主动作不可执行、账号不可用、权限错误、核心数据缺失 | 登记 P0 问题，必须关闭后才能验收 | `issue-pool.md`、`round-1-issue-closure-tracker.md` |
| 路径失败但不阻塞主链路 | 文案、展示、非关键状态等不影响主动作 | 可延期，但必须写明原因、补齐 Agent 和后续阶段 | `round-1-issue-closure-tracker.md` |
| 缺少证据 | 未提供截图、日志、路由、账号数据或操作结果 | 回退补齐本地台账证据，不允许进入验收 | `acceptance-evidence-register.md` |
| Handoff 信息导致失败 | 需求、接口、权限、验收标准不完整 | 退回 Handoff 补充并复核 | `handoff-quality-review.md`、`handoff-log.md` |
| 架构或范围争议 | 影响服务广场结构、核心服务边界或主动作 | 项目负责人裁决，必要时形成 ADR | `blocker-escalation-decision-log.md` |

## 五、问题关闭判定

| 问题状态 | 允许动作 | 是否允许进入验收 |
| --- | --- | --- |
| 已关闭且有证据 | 进入验收证据登记 | 是 |
| 已关闭但无证据 | 补关闭证据 | 否 |
| 已延期且不阻塞主链路 | 登记延期原因和后续阶段 | 可按板块判断 |
| 已延期但阻塞主链路 | 不允许验收，必须升级裁决 | 否 |
| 待处理或处理中 | 继续跟踪 | 否 |
| 无补齐 Agent 或无关闭时间 | 升级项目负责人裁决 | 否 |

## 六、单板块问题关闭判定

Partial Go 情况下，只对已完成联调的板块做问题关闭判断。

| 板块 | 是否完成联调 | 主链路问题 | 非阻塞问题 | Handoff 状态 | 当前判定 |
| --- | --- | --- | --- | --- | --- |
| 生命导航 | 否 | 待判断 | 待判断 | 待复核 | No-Go |
| 俱乐部联盟 | 否 | 待判断 | 待判断 | 待复核 | No-Go |
| 健康大管家 | 否 | 待判断 | 待判断 | 待复核 | No-Go |

## 七、输出文件更新顺序

| 顺序 | 动作 | 文件 |
| --- | --- | --- |
| 1 | 填写首次联调记录 | `round-1-integration-run-record.md` |
| 2 | 把失败项登记为问题 | `issue-pool.md` |
| 3 | 同步问题关闭跟踪 | `round-1-issue-closure-tracker.md` |
| 4 | 对超时、无补齐 Agent、需裁决问题升级 | `blocker-escalation-decision-log.md` |
| 5 | 如需退回 Handoff，更新复核结论 | `handoff-quality-review.md`、`handoff-log.md` |
| 6 | 更新问题关闭阶段门禁 | `phase-gate-status.md` |
| 7 | 问题关闭后进入验收转换 | `integration-to-acceptance-transition.md` |
| 8 | 登记验收证据或缺证据回退动作 | `acceptance-evidence-register.md` |

## 八、当前结论

截至 2026-07-09，首次真实联调尚未开始，联调到问题关闭转换尚未开始。当前不能进入问题关闭阶段或第一阶段验收，只能继续推进首次真实联调门禁解除和本地台账证据补齐。
