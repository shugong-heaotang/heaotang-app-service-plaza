# 服务广场平台事实提交执行包

日期：2026-07-10

本文件用于把 FE-PLAT-001 至 FE-PLAT-005 从“待提交”推进到“待复核”的提交前核对动作。它不替代真实平台证据，不把原型、规范、计划或台账当成事实。

FE-BATCH-001 工作区核查未接收后，先按 `platform-fact-minimum-evidence-checklist.md` 补齐五项最小平台事实；本文件负责判断补齐后的事实能否提交、接收或退回。

## 一、执行原则

1. 平台事实必须能指向真实环境、真实路由、真实账号保管方式、真实测试数据来源或可执行模拟方式。
2. 只有 `fact-evidence-submission-packet.md` 中平台事实提交包字段完整，才允许把 `fact-evidence-intake-review.md` 中对应 FE-PLAT 改为“待复核”。
3. 工作区核查结果以 `workspace-evidence-search-log.md` 为准；当前仅发现原型、规范、决策和台账，不足以进入待复核。
4. 任一平台事实进入待复核，只触发审计复核，不自动解除首次真实联调 No-Go。
5. 账号信息只记录账号类型、环境、保管方式和可用状态，不记录真实密码、生产凭据或真实会员隐私。

## 二、平台事实提交队列

| 队列 | FE 编号 | 证据编号 | 必须补齐的事实字段 | 可接受证据位置 | 当前状态 |
| --- | --- | --- | --- | --- | --- |
| PLAT-ACT-001 | FE-PLAT-001 | EV-PLAT-001 | 联调环境名称、环境地址、服务广场入口、三大核心服务正式路由或临时承接页、第一轮采用方案 | `platform-integration-reply-template.md`、`routing-and-temporary-page-spec.md`、真实工程文件或环境地址 | 待提交 |
| PLAT-ACT-002 | FE-PLAT-002 | EV-PLAT-002 | 未登录、普通会员、无权限、管理或审核权限规则，以及每类权限预期页面状态 | `platform-integration-reply-template.md`、`test-accounts-and-data.md`、`integration-checklist.md` | 待提交 |
| PLAT-ACT-003 | FE-PLAT-003 | EV-PLAT-003 | 账号类型、获取方式、测试环境、安全保管方式、可用状态；不得记录真实密码 | `platform-integration-reply-template.md`、`test-accounts-and-data.md` | 待提交 |
| PLAT-ACT-004 | FE-PLAT-004 | EV-PLAT-004 | 生命导航、俱乐部联盟、健康大管家的正常、空状态、异常测试数据来源或模拟方式 | `platform-integration-reply-template.md`、`test-accounts-and-data.md`、板块事实提交包 | 待提交 |
| PLAT-ACT-005 | FE-PLAT-005 | EV-PLAT-005 | 三大核心服务返回服务广场路径、无权限返回规则、异常返回规则 | `platform-integration-reply-template.md`、`routing-and-temporary-page-spec.md`、`integration-checklist.md` | 待提交 |

## 三、提交前核对

| 核对项 | 通过条件 | 不通过处理 |
| --- | --- | --- |
| 是否是真实工程或环境事实 | 能提供环境地址、工程文件位置、路由实现、账号保管方式或数据来源 | 继续保持待提交 |
| 是否仅为原型、规范或台账 | 只出现 `prototype/`、`docs/` 规范或项目管理台账 | 不接收为待复核事实 |
| 是否具备回写位置 | 能回写到平台回执、路由规格、账号数据清单或接口联调清单 | 缺回写位置则退回补充 |
| 是否避免敏感信息 | 未记录真实密码、生产凭据、真实会员隐私 | 发现敏感信息则退回重写 |
| 是否可支撑联调门禁 | 路由、权限、账号、数据、返回路径全部具备可验证字段 | 只触发复核，不自动 Go |

## 四、提交后回写顺序

| 顺序 | 动作 | 回写文件 | 责任 Agent |
| --- | --- | --- | --- |
| 1 | 填写平台事实提交包 | `fact-evidence-submission-packet.md` | 平台 Agent |
| 2 | 更新平台事实接收状态 | `fact-evidence-intake-review.md` | 审计 Agent |
| 3 | 登记复核动作 | `fact-evidence-review-run-log.md` | 审计 Agent |
| 4 | 回写平台关闭运行表 | `platform-condition-evidence-runbook.md` | 平台 Agent |
| 5 | 回写 P0 执行流水 | `p0-evidence-execution-log.md` | 执行 Agent |
| 6 | 复核首次真实联调门禁 | `first-integration-go-checklist.md`、`phase-gate-evidence-matrix.md` | 审计 Agent |

## 五、退回条件

| 退回原因 | 对应 FE | 退回说明 |
| --- | --- | --- |
| 没有真实环境地址或工程文件位置 | FE-PLAT-001 | 不能证明服务广场入口或核心服务路由可用 |
| 权限规则只有原则描述 | FE-PLAT-002 | 不能验证未登录、普通会员、无权限、管理或审核状态 |
| 账号信息包含真实密码或生产凭据 | FE-PLAT-003 | 必须删除敏感信息，只保留类型和保管方式 |
| 测试数据只有计划，没有来源或模拟方式 | FE-PLAT-004 | 不能进入联调或验收 |
| 返回路径没有可验证页面或规则 | FE-PLAT-005 | 主链路闭环不成立 |

## 六、当前结论

截至 2026-07-10，平台事实提交执行包已建立，并已通过 `day-1-platform-fact-run-record.md` 完成 Day 1 平台五项核查，但 FE-PLAT-001 至 FE-PLAT-005 尚未提交真实平台事实。下一步先补环境与路由、权限、测试账号、测试数据和返回路径五项事实；首次真实联调保持 No-Go；第一阶段验收保持 No-Go。
