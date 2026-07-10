# 俱乐部联盟项目入口

项目 ID：`club-alliance`  
父项目：和奥堂 APP 服务广场  
板块负责人：俱乐部联盟负责人（正式派发时确认）  
平台集成负责人：服务广场平台集成负责人  
当前切片：`standard-club-join-review`  
当前状态：待启动；生命导航二完成 M4 并通过试验复盘前，不得签收或编码。

## 目标

完成“浏览自建俱乐部—申请加入—查看本人申请状态—俱乐部管理者审核—批准后成为成员”的测试环境闭环。

## 启动后的必读输入

除平台 README 第 0 节课程外，还必须完整阅读：

1. `docs/project-management/notices/2026-07-11-club-alliance-first-phase-task-order.md`
2. `docs/project-management/modules/club-alliance-first-slice-contract-v1.md`
3. `contracts/foundation/module-dependencies/club-alliance.v1.json`
4. `contracts/modules/club-alliance/internal-dependencies.v1.json`

正式派发后，必须创建独立工作项、分支和工作树，并以 `ModuleId=club-alliance` 完成起飞检查单和 100 分随机治理考试。

## 边界

本切片只做后端 `type=standard` 对应的自建俱乐部加入审核闭环，不做家庭俱乐部、公益俱乐部、友联体、会费、支付、提现、分账和付费套餐。

模块负责人只修改正式工作项列出的模块专属路径。共享样式、共享接口和平台合同必须通过接口变更申请。

## 阶段门禁

- development：Go
- acceptance：Partial Go
- 已知缺口：权威 `type=standard` 列表筛选和本人申请状态接口尚未验收
- 派发门禁：生命导航二 `LN-M4-001 Go`，且平台完成试验复盘
- 当前检查点：未启动
- 签收回执：`task-receipt.md`
- 阶段 Handoff：`checkpoint-handoff-template.md`
- 接口变更申请：`interface-change-request-template.md`
