# 服务广场平台事实最小证据补齐清单

日期：2026-07-09

本文件承接 `fact-evidence-next-batch-run-record.md` 的未接收结论，用于把 FE-BATCH-001 的平台事实缺口压缩为最小可执行任务。它不是新的流程，只是平台 Agent 和后续 agent 补齐 FE-PLAT-001 至 FE-PLAT-005 时的逐项检查表。本轮实际核查结果记录在 `platform-fact-minimum-evidence-run-record.md`。

## 一、当前结论

| 项目 | 结论 |
| --- | --- |
| FE-BATCH-001 状态 | 已执行工作区核查，未接收 |
| 未接收原因 | 当前工作区只发现原型、规范、决策和项目台账，未发现真实工程入口、环境、路由、权限、账号、数据或返回路径证据 |
| 本轮执行记录 | `platform-fact-minimum-evidence-run-record.md` 已登记五项平台事实核查结果，当前均不可接收 |
| 当前门禁 | 首次真实联调 No-Go；第一阶段验收 No-Go |
| 下一步原则 | 先补平台事实，再触发 FE-PLAT 接收与复核；不得直接推进 FE-GATE 或 FE-ACC |

## 二、五项最小补齐任务

| 顺序 | FE 编号 | 必须补齐的最小事实 | 可接受证据 | 不可接受内容 | 回写文件 |
| --- | --- | --- | --- | --- | --- |
| 1 | FE-PLAT-001 | 测试或联调环境名称、环境地址、服务广场入口、三大核心服务正式路由或临时承接页路由、第一轮采用方案 | 可访问环境地址、工程文件位置、路由配置、临时承接页实现记录 | 原型截图、建议路由、待开发说明 | `platform-condition-evidence-runbook.md`、`routing-and-temporary-page-spec.md`、`integration-checklist.md` |
| 2 | FE-PLAT-002 | 未登录、普通会员、无权限、管理或审核权限规则，以及每类权限预期页面状态 | 权限规则表、账号类型与权限映射、可验证页面状态说明 | “后续补权限”、原则描述、没有账号类型的权限说明 | `platform-integration-reply-template.md`、`test-accounts-and-data.md`、`integration-checklist.md` |
| 3 | FE-PLAT-003 | 测试账号类型、获取方式、测试环境、安全保管方式、可用状态 | 账号类型清单、领取或保管方式、安全说明、可用状态记录 | 真实密码、生产凭据、真实会员隐私数据 | `platform-integration-reply-template.md`、`test-accounts-and-data.md` |
| 4 | FE-PLAT-004 | 生命导航、俱乐部联盟、健康大管家的正常、空状态、异常测试数据来源或模拟方式 | 测试数据来源、mock 或 fixture 位置、数据初始化说明、板块数据责任说明 | 只有测试计划，没有数据来源或模拟方式 | `platform-integration-reply-template.md`、`test-accounts-and-data.md`、`fact-evidence-submission-packet.md` |
| 5 | FE-PLAT-005 | 三大核心服务返回服务广场路径、无权限返回规则、异常返回规则 | 页面返回规则、路由返回实现、异常状态返回说明、可验证记录 | “返回上一页”等不可验证描述 | `routing-and-temporary-page-spec.md`、`integration-checklist.md`、`platform-condition-evidence-runbook.md` |

## 三、接收前检查

| 检查项 | 通过标准 | 未通过动作 |
| --- | --- | --- |
| 证据是否真实 | 能指向环境、工程文件、配置、账号保管方式、数据来源或可验证记录 | 继续保持待提交 |
| 字段是否完整 | FE-PLAT-001 至 FE-PLAT-005 的最小事实字段均有内容 | 缺哪项退回哪项 |
| 是否安全 | 不包含真实密码、生产凭据或真实会员隐私 | 删除敏感信息后重提 |
| 是否可复核 | 审计 Agent 可以按证据位置复查 | 证据位置不清则退回 |
| 是否影响门禁 | 五项均通过接收后，只能触发 FE-PLAT 复核 | 不直接改 Go |

## 四、回写顺序

1. 先按本文件补齐 FE-PLAT-001 至 FE-PLAT-005 的最小事实。
2. 再填写 `fact-evidence-submission-packet.md` 的平台事实提交包。
3. 然后在 `fact-evidence-intake-review.md` 中把对应 FE-PLAT 从待提交改为待复核或退回补充。
4. 审计 Agent 在 `fact-evidence-review-run-log.md` 登记 FR-PLAT 复核结果。
5. 只有 FR-PLAT 通过后，才允许继续判断 FE-BATCH-002、FE-BATCH-003 和后续 FE-GATE 是否具备触发条件。

## 五、当前执行状态

| FE 编号 | 当前状态 | 下一步 |
| --- | --- | --- |
| FE-PLAT-001 | 待补真实环境和路由事实 | 补环境地址、入口和路由实现证据 |
| FE-PLAT-002 | 待补权限事实 | 补权限矩阵和预期页面状态 |
| FE-PLAT-003 | 待补账号事实 | 补账号类型、获取方式和安全保管方式 |
| FE-PLAT-004 | 待补测试数据事实 | 补三大核心服务数据来源或模拟方式 |
| FE-PLAT-005 | 待补返回路径事实 | 补返回服务广场、无权限返回和异常返回规则 |

本轮执行记录已经确认：建议路由、ADR、原型和清单不能替代真实平台事实。后续只有补出可访问地址、工程实现位置、账号保管方式、数据来源和返回路径验证后，才能重新提交 FE-PLAT。
