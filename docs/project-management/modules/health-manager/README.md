# 健康大管家项目入口

项目 ID：`health-manager`  
父项目：和奥堂 APP 服务广场  
板块负责人：健康大管家负责人
平台集成负责人：服务广场平台集成负责人  
当前切片：`health-mvp90-m0`
当前状态：正式激活；只执行 MVP-90 M0 合同与合成一致性首检查点。

## 目标

把 PRD C5 已确认的 16 个产品语义对象、6 组状态机、6 类角色和 `MVP-A001`—`MVP-A015` 转换为版本化合同、Schema、显式合成 fixtures 与 conformance。

## 启动后的必读输入

除平台 README 第 0 节课程外，还必须完整阅读：

1. `docs/project-management/notices/2026-07-12-health-manager-mvp90-m0-task-order.md`
2. `docs/project-management/modules/health-manager/health-manager-mvp90-m0-requirements.md`
3. `contracts/foundation/module-dependencies/health-manager.v1.json`
4. `contracts/modules/health-manager/internal-dependencies.v1.json`

正式派发后，必须创建独立工作项、分支和工作树，并以 `ModuleId=health-manager` 完成起飞检查单和 100 分随机治理考试。

## 边界

本切片只做 M0 机器合同和合成一致性，不做前端、后端、API、数据库、环境、部署、生产、真实健康数据、收费或真实会员试运行。27 项 `Pending with owner` 只作为不可执行元数据；HM-R0 仍为 `Technical Go / Professional Freeze Pending`。

模块负责人只修改正式工作项列出的模块专属路径。共享样式、共享 API、平台合同、认证、错误信封和部署基础设施均受平台保护，必须通过接口变更申请处理。

## 阶段门禁

- development：Go
- acceptance：Pending（M0 只做合同与合成一致性）
- 派发门禁：已完成；`AIW-20260711-HEALTH-MVP90-M0-CONTRACTS` 为唯一 active 工作项
- M0：当前正式授权
- M1 及以后：No-Go，必须另行派发
- 当前检查点：M0 首检查点
- 签收回执：`health-manager-mvp90-m0-receipt.md`
- 阶段 Handoff：`health-manager-mvp90-m0-handoff.md`
- 接口变更申请：`interface-change-request-template.md`
