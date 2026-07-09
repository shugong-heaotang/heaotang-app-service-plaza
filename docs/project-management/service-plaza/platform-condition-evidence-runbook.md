# 平台条件证据关闭运行表

日期：2026-07-10

本文件用于把平台 Agent 的待补齐事项转成可执行、可回写、可复核的证据关闭动作。平台事实提交前先按 `platform-fact-submission-action-pack.md` 核对字段、证据位置和退回条件。当前只建立运行机制，不虚构平台事实；未形成证据前，首次真实联调保持 No-Go。

## 一、运行原则

1. 每个 EV-PLAT 证据只接受事实字段，不接受口头判断或建议项。
2. 账号和数据只登记获取方式、环境、类型和安全说明，不记录真实密码、真实会员隐私或生产凭据。
3. 正式页面未完成时，可以登记临时承接页，但必须说明替换路径和返回服务广场方式。
4. 任一 EV-PLAT 证据缺失时，不允许把首次真实联调改为 Go。
5. 单板块 Partial Go 也必须具备该板块所需的路由、权限、账号、数据和返回路径。

## 二、证据关闭队列

| P0 编号 | 证据编号 | 当前任务 | 最小事实字段 | 回写文件 | 当前状态 |
| --- | --- | --- | --- | --- | --- |
| P0-PLAT-001 | EV-PLAT-001 | 补齐服务广场总入口和三大核心服务路由 | 环境地址、总入口、正式路由或临时承接页路由、第一轮采用方案 | `platform-integration-reply-template.md`、`routing-and-temporary-page-spec.md`、`integration-checklist.md` | 已建字段，待事实证据 |
| P0-PLAT-002 | EV-PLAT-002 | 补齐权限基线 | 未登录、普通会员、无权限、管理或审核权限规则及预期状态 | `platform-integration-reply-template.md`、`test-accounts-and-data.md`、`integration-checklist.md` | 已建字段，待事实证据 |
| P0-PLAT-003 | EV-PLAT-003 | 补齐测试账号准备方式 | 账号类型、获取方式、测试环境、安全说明、不可记录真实密码 | `platform-integration-reply-template.md`、`test-accounts-and-data.md` | 已建字段，待事实证据 |
| P0-PLAT-004 | EV-PLAT-004 | 补齐三大核心服务测试数据 | 每个核心服务的正常、空状态、异常数据来源或模拟方式 | `platform-integration-reply-template.md`、`test-accounts-and-data.md` | 已建字段，待事实证据 |
| P0-PLAT-005 | EV-PLAT-005 | 补齐返回服务广场路径 | 三个核心服务返回方式、无权限返回规则、异常返回规则 | `platform-integration-reply-template.md`、`routing-and-temporary-page-spec.md`、`integration-checklist.md` | 已建字段，待事实证据 |

平台事实证据统一先按 `platform-fact-submission-action-pack.md` 核对，再提交到 `fact-evidence-intake-review.md` 的 FE-PLAT-001 至 FE-PLAT-005。只有接收状态从“待提交”变为“证据已形成，待门禁复核”后，才允许回写 P0 队列并请求门禁复核；不得直接解除首次真实联调 No-Go。

## 三、每日关闭动作

| 顺序 | 动作 | 产出 | 责任 Agent | 门禁影响 |
| --- | --- | --- | --- | --- |
| 1 | 按平台事实提交执行包核对 FE-PLAT-001 至 FE-PLAT-005 | 平台事实提交前核对结论 | 平台 Agent、审计 Agent | 缺失则保持待提交 |
| 2 | 核对环境和服务广场入口是否有事实地址 | EV-PLAT-001 草稿或缺口说明 | 平台 Agent | 缺失则首次真实联调 No-Go |
| 2A | 执行 Day 1 环境与路由事实核查 | FE-PLAT-001 可提交或不可提交结论 | 平台 Agent、审计 Agent | 无事实则保持待提交 |
| 3 | 核对三大核心服务路由是否可用正式页或临时承接页 | 路由表和临时承接页方案 | 平台 Agent | 单板块 Partial Go 必备 |
| 4 | 核对权限基线和账号类型 | 权限基线、账号获取方式 | 平台 Agent | 缺失则无法验证登录和无权限状态 |
| 5 | 核对测试数据来源或模拟方式 | 三类数据登记 | 平台 Agent、板块 Agent | 缺失则无法进入验收 |
| 6 | 核对返回服务广场和异常返回路径 | 返回路径验收项 | 平台 Agent | 缺失则联调闭环不成立 |
| 7 | 回写 P0 队列并请求审计复核 | P0 状态从“待补齐”变为“证据已形成，待门禁复核” | 平台 Agent、审计 Agent | 只触发复核，不自动 Go |

## 四、状态转换规则

| 状态 | 含义 | 是否解除门禁 |
| --- | --- | --- |
| 待补齐 | 尚未建立字段或缺口不清 | 否 |
| 已建字段，待事实证据 | 已明确要填什么，但没有事实证据 | 否 |
| 证据已形成，待门禁复核 | 事实字段完整，等待审计 Agent 复核 | 否 |
| 复核通过 | 审计 Agent 确认证据覆盖门禁要求 | 可进入 Go / Partial Go 判断 |
| 退回补充 | 字段不完整、证据不可验证或影响范围不清 | 否 |

## 五、当前结论

截至 2026-07-10，平台侧证据已建立关闭运行表和平台事实提交执行包，并已按 `day-1-environment-route-run-record.md` 完成 FE-PLAT-001 环境与路由核查，但 EV-PLAT-001 至 EV-PLAT-005 仍缺事实证据。首次真实联调和第一阶段验收继续保持 No-Go。
