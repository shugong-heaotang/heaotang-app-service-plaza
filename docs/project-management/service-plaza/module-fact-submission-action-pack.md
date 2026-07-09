# 服务广场板块事实提交执行包

日期：2026-07-09

本文件用于把 FE-MOD-001 至 FE-MOD-003 从“待提交”推进到“待复核”的提交前核对动作。它只接收三大核心服务的可验证板块事实，不把推荐主动作、计划项、原型或空模板当成事实。

板块事实提交前，先用 `module-fact-submission-worksheet.md` 整理三大核心服务的主动作、页面方案、权限、后台处理、测试数据和验收责任字段，再按 `module-fact-evidence-intake.md` 判断是否可接收；工作表未补齐或接收表未通过时不得提交为待复核。

## 一、执行原则

1. 板块事实必须先明确主动作、页面方案、权限、后台处理、测试数据和验收责任。
2. 推荐主动作可以作为默认准备口径，但没有确认来源时不能关闭 FE-MOD。
3. 板块事实通过后只关闭 P0-MOD，不自动关闭 Handoff，也不自动解除首次真实联调 No-Go。
4. Handoff 事实另按 `handoff-completion-action-pack.md` 和 FE-HO-001 至 FE-HO-003 提交。
5. 平台路由、账号、数据和返回路径仍按 `platform-fact-submission-action-pack.md` 提交；板块事实不能替代平台事实。

## 二、板块事实提交队列

| 队列 | FE 编号 | 证据编号 | 板块 | 必须补齐的事实字段 | 回写文件 | 当前状态 |
| --- | --- | --- | --- | --- | --- | --- |
| MOD-ACT-001 | FE-MOD-001 | EV-MOD-001 | 生命导航 | 是否采用“提交导航申请”、正式页面或临时承接页、页面或路由、登录要求、会员权限、后台处理方式、正常数据、空状态数据、异常数据、验收责任 | `core-service-confirmation-reply-template.md`、`module-intake-cards.md`、`core-service-main-action-confirmation.md` | 待提交 |
| MOD-ACT-002 | FE-MOD-002 | EV-MOD-002 | 俱乐部联盟 | 是否采用“申请加入俱乐部”、正式页面或临时承接页、页面或路由、登录要求、会员权限、审核规则、管理中心附属操作边界、后台处理方式、正常数据、空状态数据、异常数据、验收责任 | `core-service-confirmation-reply-template.md`、`module-intake-cards.md`、`core-service-main-action-confirmation.md` | 待提交 |
| MOD-ACT-003 | FE-MOD-003 | EV-MOD-003 | 健康大管家 | 是否采用“提交健康咨询”、正式页面或临时承接页、页面或路由、登录要求、会员权限、后台处理方式、正常数据、空状态数据、异常数据、验收责任 | `core-service-confirmation-reply-template.md`、`module-intake-cards.md`、`core-service-main-action-confirmation.md` | 待提交 |

## 三、提交前核对

| 核对项 | 通过条件 | 不通过处理 |
| --- | --- | --- |
| 主动作是否明确 | 采用推荐主动作或明确替换主动作，并记录确认来源 | 保持待提交 |
| 页面方案是否明确 | 正式页面、临时承接页或其他方案只能选一种，并说明页面或路由 | 保持待提交 |
| 权限和登录要求是否明确 | 登录要求、会员权限和无权限状态有具体规则 | 退回补充 |
| 后台处理是否明确 | 提交后由谁处理、是否审核、状态如何反馈有具体说明 | 退回补充 |
| 测试数据是否明确 | 正常、空状态、异常数据来源或模拟方式可说明 | 缺数据则不能进入联调 |
| 验收责任是否明确 | 验收责任 Agent、通过标准和不通过回退动作明确 | 退回补充 |
| 是否同步 Handoff | 板块事实准备好后，说明是否同步 SP-H002 至 SP-H004 | 未同步时不得关闭 Handoff |

## 四、提交后回写顺序

| 顺序 | 动作 | 回写文件 | 责任 Agent |
| --- | --- | --- | --- |
| 1 | 填写板块事实提交包 | `fact-evidence-submission-packet.md` | 板块 Agent |
| 2 | 更新核心服务确认记录 | `core-service-confirmation-reply-template.md` | 板块 Agent |
| 3 | 更新板块接入卡 | `module-intake-cards.md` | 板块 Agent |
| 4 | 更新主动作确认表 | `core-service-main-action-confirmation.md` | 板块 Agent |
| 5 | 更新事实接收状态 | `fact-evidence-intake-review.md` | 审计 Agent |
| 6 | 登记复核动作 | `fact-evidence-review-run-log.md` | 审计 Agent |
| 7 | 回写 P0 执行流水 | `p0-evidence-execution-log.md` | 执行 Agent |
| 8 | 复核首次真实联调门禁 | `first-integration-go-checklist.md`、`phase-gate-evidence-matrix.md` | 审计 Agent |

## 五、退回条件

| 退回原因 | 对应 FE | 退回说明 |
| --- | --- | --- |
| 只写推荐主动作，没有确认来源 | FE-MOD-001 至 FE-MOD-003 | 推荐项不能直接当成事实 |
| 页面方案仍是多选或待补齐 | FE-MOD-001 至 FE-MOD-003 | 无法判断正式页或临时承接页 |
| 权限、后台处理或验收责任缺失 | FE-MOD-001 至 FE-MOD-003 | 无法进入 Handoff 或联调 |
| 俱乐部联盟管理中心边界不清 | FE-MOD-002 | 可能影响入口层级和审核责任 |
| 测试数据只有计划，没有来源或模拟方式 | FE-MOD-001 至 FE-MOD-003 | 无法支撑联调和验收 |

## 六、当前结论

截至 2026-07-09，板块事实提交执行包已建立，但 FE-MOD-001 至 FE-MOD-003 尚未提交真实板块事实。首次真实联调保持 No-Go；第一阶段验收保持 No-Go。
