# 服务广场第一轮联调执行日程

本日程用于把第一轮联调从启动包推进到实际执行。当前项目按“项目负责人决策 + agent 协同 + 本地台账推进”执行，具体日期可根据本地确认结果调整，但执行顺序不变。

## 一、联调执行顺序

| 顺序 | 阶段 | 目标 | 推进角色 | 输出物 | 状态 |
| --- | --- | --- | --- | --- | --- |
| 1 | Agent 分工确认 | 确认执行 Agent、平台 Agent、板块 Agent、验收 Agent、审计 Agent 的推进边界 | 项目负责人裁决、审计 Agent 记录 | `owner-roster.md` | 待执行 |
| 2 | 范围确认 | 确认三大核心服务第一阶段主动作 | 板块 Agent、审计 Agent | `core-service-main-action-confirmation.md` | 已给推荐默认项，待确认 |
| 3 | Handoff 首轮提交 | 三大核心服务提交“需求给开发”handoff | 板块 Agent | `round-1-handoff-forms.md` | 表单已建，待确认 |
| 4 | 路由准备 | 确认正式页面或临时承接页路由 | 平台 Agent | `routing-and-temporary-page-spec.md` | 已给建议，待确认 |
| 5 | 权限准备 | 准备未登录、普通会员、无权限、管理或审核账号 | 平台 Agent | `test-accounts-and-data.md` | 已建清单，待准备 |
| 6 | 数据准备 | 准备正常、空状态、异常状态测试数据 | 平台 Agent、板块 Agent | `test-accounts-and-data.md` | 已建清单，待准备 |
| 7 | 门禁复核 | 按确认结果和本地台账证据判断整体 Go 或单板块 Partial Go | 审计 Agent、项目负责人裁决 | `reply-to-gate-transition.md`、`first-integration-go-checklist.md` | No-Go |
| 8 | 首次联调 | 验证服务广场到三大核心服务跳转和返回；如 Partial Go，则只联调已满足条件的板块 | 执行 Agent、平台 Agent | `round-1-integration-run-record.md` | 待执行 |
| 9 | 问题关闭 | 关闭阻塞项，无法关闭的补齐后提交裁决 | 平台 Agent、板块 Agent、审计 Agent | `round-1-issue-closure-tracker.md` | 待执行 |
| 10 | 阶段验收 | 按第一阶段验收清单判断是否进入下一阶段 | 验收 Agent、审计 Agent、项目负责人裁决 | `phase-1-acceptance-checklist.md` | 待执行 |

## 二、首次联调启动确认安排

```text
执行名称：服务广场第一轮联调启动确认
执行目标：确认第一轮联调能否启动，以及当天需要补齐的台账项
执行 Agent：
平台 Agent：
板块 Agent：
验收 Agent：
审计 Agent：
最终裁决：项目负责人
```

## 三、首次联调启动确认必须输出

| 输出项 | 说明 | 状态 |
| --- | --- | --- |
| Agent 分工确认结论 | 至少确认本轮补齐和复核 Agent | 待输出 |
| 三大核心服务主动作 | 每个板块只能先选一个第一阶段主动作 | 待输出 |
| 临时承接页使用结论 | 已由 ADR 0003 允许，但需确认每个板块是否采用 | 待输出 |
| 路由清单 | 正式路由或临时路由 | 待输出 |
| 测试账号清单 | 覆盖登录、无权限和管理状态 | 待输出 |
| 测试数据清单 | 覆盖正常、空、异常状态 | 待输出 |
| 下一次联调时间 | 明确到日期和时间 | 待输出 |

## 四、联调记录模板

```text
联调日期：
执行 Agent：
平台 Agent：
板块 Agent：
联调范围：
使用页面：正式页面 / 临时承接页
通过项：
失败项：
新增问题：
问题补齐 Agent：
是否需要项目负责人裁决：
下一步动作：
下一次联调时间：
```

## 五、分批联调安排规则

如果三大核心服务不能同时满足首次真实联调条件，采用 Partial Go：

| 场景 | 安排方式 | 记录要求 |
| --- | --- | --- |
| 三大核心服务全部满足 | 安排整体首次真实联调 | 联调记录覆盖全部三大核心服务 |
| 只有一个或两个核心服务满足 | 先联调满足条件的板块 | 联调记录必须写明未进入联调的板块和阻塞原因 |
| 没有任何核心服务满足 | 不安排真实联调，只继续补齐确认结果、Handoff 和本地台账证据 | 更新 `current-week-command-board.md` 和问题池 |

Partial Go 不代表第一阶段验收通过。只有已联调板块完成联调记录、问题关闭和验收前置证据，才可进入该板块的验收判断。

## 六、会前材料

| 材料 | 文件 |
| --- | --- |
| 第一轮联调签核清单 | `round-1-signoff-checklist.md` |
| 确认结果到门禁转换规则 | `reply-to-gate-transition.md` |
| 第一轮联调启动会通知 | `round-1-kickoff-invitation.md` |
| 第一轮联调会前材料核对清单 | `round-1-premeeting-checklist.md` |
| 第一轮联调启动会纪要 | `round-1-kickoff-meeting-minutes.md` |
| 启动会后台账更新动作表 | `post-kickoff-update-actions.md` |
| 第一轮首次联调记录 | `round-1-integration-run-record.md` |
| 第一轮问题关闭跟踪表 | `round-1-issue-closure-tracker.md` |
| 路由与临时承接页规格 | `routing-and-temporary-page-spec.md` |
| 测试账号与测试数据清单 | `test-accounts-and-data.md` |
| 三大核心服务最小可交付范围 | `core-services-mvp-scope.md` |
| 三大核心服务主动作确认表 | `core-service-main-action-confirmation.md` |
| Handoff 首轮提交清单 | `handoff-log.md` |
| 三大核心服务首轮 Handoff 表单 | `round-1-handoff-forms.md` |
