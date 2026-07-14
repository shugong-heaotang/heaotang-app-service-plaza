# NOVA Phase 5 M1 治理冷启动入口

本文是平台在 NOVA 模块正式产物之外建立的不可循环 bootstrap 输入。它只解决 `-ModuleId nova` 在正式实现前必须能读取完整、稳定、已存在的模块治理边界；不代表 M1、synthetic E2E、真实工具网关或上线已经 Go。

## 身份与责任

- module id：`nova`
- 父项目：和奥堂 APP
- 当前模块工作项：`AIW-20260712-NOVA-PHASE5-M1-RUNTIME`
- 模块负责人：Nova + AI 板块负责人
- 平台接口与最终集成：平台集成负责人
- 独立验收：平台治理独立测试负责人
- 正式阶段任务入口：`docs/project-management/notices/2026-07-12-nova-m1-task-order.md`

板块负责人实现 NOVA 内部 runtime、工具调用和合成验证；平台负责人只提供治理、公共契约门禁和受控集成，不代做板块业务。

## 当前范围

Phase 5 M1 的最小目标是版本化任务运行底座：任务/步骤/事件状态、工具注册和调用、显式确认、权限与租户隔离、审计、幂等、失败恢复、模型路由和成本边界。mock 或 synthetic 证据只能证明协议可开发，不能证明真实闭环或上线。

本 overlay 修复项只建立治理阅读入口和激活前门禁，不修改 `nova_ai/**`、`contracts/modules/nova/**`、`tests/**`、公共 NOVA API 合同或任何业务实现。

## 当前缺口与失败关闭

- APP 当前权威基线存在 NOVA M1 正式任务通知书，但模块工作树中的 Phase 5 README、需求输入、平台依赖和内部依赖产物尚未受控集成到此基线。
- 该缺口不得被写成 development Go；NOVA 后续 owner 必须在自己的授权工作项内形成 current checklist、100 分考试、依赖事实、实现记录和 Handoff。
- `TaskRuntime` 是否统一通过 `ToolRuntime.call` 执行真实/合成工具仍需代码与独立 E2E 证据验证；文档存在不构成通过。

## 禁止边界

- 不访问生产凭据、真实用户、真实关系、真实活动、真实消息或真实资金。
- 不发送邀请、消息，不创建真实业务对象，不部署。
- 不以提示词代替服务端权限、租户、确认、幂等或审计。
- 不把 mock 结果冒充工具网关 E2E、真实板块闭环或 release Go。
- 不硬编码模型路由、额度、成本、超时或重试为业务事实。

## 下一检查点

平台 overlay/激活前共享门禁经独立验收并受控集成后，NOVA owner 使用 `-ModuleId nova` 生成新的 pending current checklist；逐项全文读取并考试100分后，才能在原工作项授权范围内补齐依赖与 synthetic E2E，不自动扩大业务或部署权限。
