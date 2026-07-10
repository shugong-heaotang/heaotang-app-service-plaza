# 健康大管家项目入口

项目 ID：`health-manager`  
父项目：和奥堂 APP 服务广场  
板块负责人：健康大管家负责人（正式派发时确认）  
平台集成负责人：服务广场平台集成负责人  
当前切片：`personal-consultation-inbox`  
当前状态：待启动；生命导航二完成 M4 并通过试验复盘前，不得签收或编码。

## 目标

完成“进入健康大管家—提交个人健康咨询—查看本人咨询历史和状态—返回服务广场”的测试环境闭环。

## 启动后的必读输入

除平台 README 第 0 节课程外，还必须完整阅读：

1. `docs/project-management/notices/2026-07-11-health-manager-first-phase-task-order.md`
2. `docs/project-management/modules/health-manager-first-slice-contract-v1.md`
3. `contracts/foundation/module-dependencies/health-manager.v1.json`
4. `contracts/modules/health-manager/internal-dependencies.v1.json`

正式派发后，必须创建独立工作项、分支和工作树，并以 `ModuleId=health-manager` 完成起飞检查单和 100 分随机治理考试。

## 边界

本切片只做个人咨询收件与本人历史，不做 AI 诊断、医生预约、收费、健康报告生成、家庭共享或后台医生处置闭环。咨询正文属于敏感数据，不进入结构化日志，也不得发送给 AI。

模块负责人只修改正式工作项列出的模块专属路径。共享样式、共享 API、平台合同、认证、错误信封和部署基础设施均受平台保护，必须通过接口变更申请处理。

## 阶段门禁

- development：Go
- acceptance：Partial Go
- 派发门禁：生命导航二 `LN-M4-001 Go`，且平台完成试验复盘
- 当前检查点：未启动
- 签收回执：`task-receipt.md`
- 阶段 Handoff：`checkpoint-handoff-template.md`
- 接口变更申请：`interface-change-request-template.md`
