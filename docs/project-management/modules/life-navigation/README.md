# 生命导航项目入口

项目 ID：`life-navigation`
父项目：和奥堂 APP 服务广场
板块负责人：生命导航二负责人
平台集成负责人：服务广场平台集成负责人
当前切片：`application-history`

## 目标

完成“进入生命导航—提交导航申请—查看本人申请历史—展示状态—返回服务广场”的测试环境闭环。

## 权威输入

按平台 README 第 0 节完成核心课程，再读取：

1. `docs/project-management/notices/2026-07-10-life-navigation-first-phase-task-order.md`
2. `docs/project-management/modules/life-navigation-first-slice-contract-v1.md`
3. `contracts/foundation/module-dependencies/life-navigation.v1.json`
4. `contracts/modules/life-navigation/internal-dependencies.v1.json`

开始编码前必须完成带 `ModuleId=life-navigation` 的起飞检查单和随机治理考试，成绩必须为 100。

## 边界

本切片只做申请记录及本人历史，不实现题库、评分权重、命运预测、AI 建议、收费套餐、下游服务交易、医疗/心理/法律/金融结论。公共服务广场契约和基础设施路径属于平台受保护范围。

## 当前门禁

- development：Go
- acceptance：Partial Go
- 通知状态：已于 2026-07-11 正式下达
- 当前检查点：M0 起飞认证；未取得 `LN-M0-001 Go` 不得编辑业务代码
- 签收回执：`task-receipt.md`
- 阶段 Handoff：`checkpoint-handoff-template.md`
- 接口变更申请：`interface-change-request-template.md`
