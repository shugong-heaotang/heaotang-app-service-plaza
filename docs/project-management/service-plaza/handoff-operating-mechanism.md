# 服务广场 Handoff 运行机制

日期：2026-07-09

本文件用于规定服务广场项目统一 Handoff 机制。当前按单人决策、agent 协同和本地台账推进，由板块 Agent、平台 Agent、审计 Agent 和项目负责人按本机制提交、接收、复核、退回、裁决和回写门禁。

## 一、机制结论

| 项目 | 当前状态 | 结论 |
| --- | --- | --- |
| Handoff 表单 | 已建立 | `round-1-handoff-forms.md` 已覆盖三大核心服务首轮表单 |
| Handoff 总表 | 已建立 | `handoff-log.md` 已记录首轮编号 |
| Handoff 质量复核 | 已建立 | `handoff-quality-review.md` 已定义复核标准 |
| Handoff 真实提交 | 未开始 | 三大核心服务均未形成完整 Handoff 事实记录 |
| 是否解除联调门禁 | 否 | Handoff 未通过质量复核，首次真实联调保持 No-Go |

## 二、统一角色分工

| 角色 | 职责 | 主要文件 |
| --- | --- | --- |
| 项目负责人 | 裁决 Handoff 是否满足架构、主动作和验收边界 | `handoff-quality-review.md`、`phase-gate-status.md` |
| 平台 Agent | 接收 Handoff，复核路由、权限、账号、数据、联调条件 | `handoff-log.md`、`integration-checklist.md` |
| 板块 Agent | 提交本板块 Handoff，补齐业务规则、主动作、验收标准 | `round-1-handoff-forms.md`、`module-intake-cards.md` |
| 验收 Agent | 接收联调给测试 Handoff，确认验收范围和证据要求 | `phase-1-acceptance-checklist.md`、`phase-1-acceptance-run-record.md` |
| 审计 Agent | 复核 Handoff 完整性并判断门禁影响 | `handoff-quality-review.md`、`first-integration-go-checklist.md` |

## 三、Handoff 阶段

| 阶段 | 触发条件 | 提交人 | 接收人 | 解除哪个门禁 |
| --- | --- | --- | --- | --- |
| 方案到执行 | 服务广场架构和推进方案定版 | 规划 Agent | 平台 Agent、板块 Agent | 启动会材料准备 |
| 需求给开发 | 板块进入第一轮准备 | 板块 Agent | 平台 Agent | 首次真实联调前置条件 |
| 开发给联调 | 路由、接口、账号、数据准备完成 | 平台 Agent、板块 Agent | 平台 Agent、审计 Agent | 首次真实联调 Go / Partial Go |
| 联调给测试 | 首次真实联调完成且问题关闭 | 执行 Agent、板块 Agent | 验收 Agent | 第一阶段验收前置条件 |
| 测试给上线准备 | 第一阶段验收通过 | 验收 Agent | 项目负责人、平台 Agent | 上线准备 |

## 四、每日 Handoff 节奏

| 时间点 | 动作 | 负责人 | 输出 |
| --- | --- | --- | --- |
| 上午 | 板块提交或补充 Handoff | 板块 Agent | `round-1-handoff-forms.md` 更新 |
| 下午 | 平台 Agent 复核联调条件 | 平台 Agent | `handoff-quality-review.md` 更新 |
| 下班前 | 审计 Agent 确认是否影响门禁 | 审计 Agent | `phase-gate-status.md`、`first-integration-go-checklist.md` 更新 |
| 次日上午 | 未补齐项进入补齐或裁决 | 执行 Agent、审计 Agent | `blocker-escalation-decision-log.md` 更新 |

## 五、提交标准

| 阶段 | 最低提交标准 |
| --- | --- |
| 需求给开发 | 负责人、主动作、页面或临时承接页、权限规则、验收标准 |
| 开发给联调 | 接口或临时数据方案、页面路由、测试账号、测试数据、已知问题、联调通过标准 |
| 联调给测试 | 测试范围、不测试范围、主要测试路径、异常场景、已知风险、验收负责人、验收通过标准 |
| 测试给上线准备 | 上线内容、影响板块、回滚方案、上线后验证项、最终确认人 |

## 六、复核结论

| 复核结论 | 含义 | 后续动作 |
| --- | --- | --- |
| 通过 | 必填字段完整，接收人可据此进入下一阶段 | 更新 `handoff-log.md` 和对应门禁 |
| 信息不完整 | 有部分信息，但缺关键字段 | 退回补充，不解除门禁 |
| 退回 | 缺主动作、责任人、路由、账号、数据、验收标准等关键项 | 登记退回原因和补齐期限 |
| 需裁决 | 涉及架构边界、主动作争议或范围变化 | 进入 `blocker-escalation-decision-log.md` |

## 七、退回和升级规则

| 场景 | 处理方式 | 升级时限 |
| --- | --- | --- |
| 缺责任边界或联系方式 | 退回板块 Agent 和规划 Agent | 当日未补齐升 L2 |
| 缺主动作或验收标准 | 退回板块 Agent，项目负责人裁决 | 当日未补齐升 L2 |
| 缺路由、账号、数据 | 退回平台 Agent | 当日未补齐升 L2 |
| Handoff 退回后未补 | 登记阻塞升级 | 次日上午升 L2 |
| 连续两次退回 | 项目负责人裁决是否 Partial Go 或 No-Go | 直接升 L3 |
| 影响架构边界 | 形成裁决记录，必要时形成 ADR | 直接升 L3 或 L4 |

## 八、通过后的回写

| 通过阶段 | 必须回写 |
| --- | --- |
| 需求给开发通过 | `handoff-log.md`、`handoff-quality-review.md`、`first-integration-go-checklist.md` |
| 开发给联调通过 | `integration-checklist.md`、`test-accounts-and-data.md`、`round-1-integration-schedule.md` |
| 联调给测试通过 | `phase-1-acceptance-checklist.md`、`acceptance-evidence-register.md`、`integration-to-acceptance-transition.md` |
| 测试给上线准备通过 | `phase-gate-status.md`、后续上线准备台账 |

## 九、当前执行要求

截至 2026-07-09，三大核心服务 Handoff 仍处于“表单已建，待确认和补齐”状态。下一步必须先补齐三大核心服务责任边界、主动作、页面方案、权限规则、账号数据和验收责任，再由平台 Agent 和审计 Agent 按 `handoff-quality-review.md` 复核。未通过复核前，首次真实联调和第一阶段验收均保持 No-Go。
