# 三大核心服务确认记录模板

本文件用于项目负责人或板块 Agent 补齐生命导航、俱乐部联盟、健康大管家三大核心服务的第一阶段确认信息。当前项目不要求多人外发和回执，所有信息以本地台账和证据编号为准。

## 一、使用规则

1. 每个板块只登记已经确认的事实；没有证据的内容保持“待补齐”。
2. 板块信息完整后，再回写 `core-service-main-action-confirmation.md`、`round-1-handoff-forms.md`、`module-intake-cards.md`、`routing-and-temporary-page-spec.md` 和 `test-accounts-and-data.md`。
3. 三大核心服务 Handoff 未通过质量复核前，首次真实联调保持 No-Go。
4. EV-MOD-001 至 EV-MOD-003 只用于关闭板块确认缺口；不得用本模板把尚未完成的 Handoff 质量复核写成已通过。
5. 板块事实证据先提交到 `module-fact-evidence-intake.md`，再进入 `fact-evidence-intake-review.md` 的 FE-MOD-001 至 FE-MOD-003；接收状态未进入“证据已形成，待门禁复核”前，不得关闭 P0-MOD。

## 二、EV-MOD 关闭口径

| 证据编号 | 板块 | P0 队列 | 待确认字段 | 关闭条件 | 回写位置 |
| --- | --- | --- | --- | --- | --- |
| EV-MOD-001 | 生命导航 | P0-MOD-001 | 主动作、页面方案、页面或路由、登录要求、会员权限要求、后台处理方式、正常数据、空状态数据、异常数据、验收责任 | 上述字段均有确认来源和证据编号；主动作可回写；页面、权限、后台处理、数据和验收责任不再为“待补齐” | 本文件生命导航确认记录；`module-intake-cards.md` 生命导航接入卡；`core-service-main-action-confirmation.md` 生命导航行；后续由平台回写路由和测试数据文件 |
| EV-MOD-002 | 俱乐部联盟 | P0-MOD-002 | 主动作、页面方案、页面或路由、登录要求、会员权限要求、是否涉及审核、管理中心附属操作、后台处理方式、正常数据、空状态数据、异常数据、验收责任 | 上述字段均有确认来源和证据编号；主动作、审核或管理中心关系、页面、权限、后台处理、数据和验收责任明确 | 本文件俱乐部联盟确认记录；`module-intake-cards.md` 俱乐部联盟接入卡；`core-service-main-action-confirmation.md` 俱乐部联盟行；后续由平台回写路由和测试数据文件 |
| EV-MOD-003 | 健康大管家 | P0-MOD-003 | 主动作、页面方案、页面或路由、登录要求、会员权限要求、后台处理方式、正常数据、空状态数据、异常数据、验收责任 | 上述字段均有确认来源和证据编号；主动作可回写；页面、权限、后台处理、数据和验收责任不再为“待补齐” | 本文件健康大管家确认记录；`module-intake-cards.md` 健康大管家接入卡；`core-service-main-action-confirmation.md` 健康大管家行；后续由平台回写路由和测试数据文件 |

## 三、生命导航确认记录

```text
板块：生命导航
确认来源：
证据编号：EV-MOD-001 / 待补齐
P0 队列：P0-MOD-001
是否进入第一轮联调：是 / 否 / 待补齐
第一阶段主动作：提交导航申请 / 其他：
页面方案：正式页面 / 临时承接页 / 待补齐
页面或路由：
登录要求：
会员权限要求：
后台处理方式：
正常数据：
空状态数据：
异常数据：
验收责任：
Handoff 状态：已提交 / 待补齐 / 退回
关闭条件：主动作、页面方案、权限、后台处理、验收责任明确，并完成接入卡和主动作表回写；Handoff 仍需另按 EV-HO-001 复核
回写位置：module-intake-cards.md；core-service-main-action-confirmation.md；round-1-handoff-forms.md；routing-and-temporary-page-spec.md；test-accounts-and-data.md
补充说明：
```

## 四、俱乐部联盟确认记录

```text
板块：俱乐部联盟
确认来源：
证据编号：EV-MOD-002 / 待补齐
P0 队列：P0-MOD-002
是否进入第一轮联调：是 / 否 / 待补齐
第一阶段主动作：申请加入俱乐部 / 其他：
页面方案：正式页面 / 临时承接页 / 待补齐
页面或路由：
登录要求：
会员权限要求：
是否涉及审核：
管理中心附属操作：
后台处理方式：
正常数据：
空状态数据：
异常数据：
验收责任：
Handoff 状态：已提交 / 待补齐 / 退回
关闭条件：主动作、页面方案、权限、审核或管理中心关系、后台处理、验收责任明确，并完成接入卡和主动作表回写；Handoff 仍需另按 EV-HO-002 复核
回写位置：module-intake-cards.md；core-service-main-action-confirmation.md；round-1-handoff-forms.md；routing-and-temporary-page-spec.md；test-accounts-and-data.md
补充说明：
```

## 五、健康大管家确认记录

```text
板块：健康大管家
确认来源：
证据编号：EV-MOD-003 / 待补齐
P0 队列：P0-MOD-003
是否进入第一轮联调：是 / 否 / 待补齐
第一阶段主动作：提交健康咨询 / 其他：
页面方案：正式页面 / 临时承接页 / 待补齐
页面或路由：
登录要求：
会员权限要求：
后台处理方式：
正常数据：
空状态数据：
异常数据：
验收责任：
Handoff 状态：已提交 / 待补齐 / 退回
关闭条件：主动作、页面方案、权限、后台处理、验收责任明确，并完成接入卡和主动作表回写；Handoff 仍需另按 EV-HO-003 复核
回写位置：module-intake-cards.md；core-service-main-action-confirmation.md；round-1-handoff-forms.md；routing-and-temporary-page-spec.md；test-accounts-and-data.md
补充说明：
```
