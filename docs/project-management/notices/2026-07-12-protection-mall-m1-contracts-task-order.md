# 保障商城 M1 合同与合成一致性首切片任务书

日期：2026-07-12

- work_id：`AIW-20260712-PROTECTION-MALL-M1-CONTRACTS`
- owner：Protection Mall module lead agent
- owner_role：商城板块唯一负责人
- reviewer_role：平台集成负责人
- approver_role：APP 总架构独立验收 Agent
- base：`1ee2fed8157884b12615e2ef5a4aee0235b7780b`
- branch：`codex/protection-mall-m1-contracts`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-protection-mall-m1-contracts`

## 唯一检查点 M1-CP1

只冻结商城 1.0 领域合同和合成一致性案例，不编写业务运行时代码：

1. 冻结商品的商城类型、销售责任主体、履约责任主体、售后责任和保障权益边界。
2. 冻结库存、订单、履约、售后和保障权益回滚状态机，覆盖合法转换、越权、重复、乱序、失败关闭和补偿案例。
3. 冻结 `mall.api.v1` 统一成功/错误信封、request/correlation ID、服务端真实 scope 来源、`Idempotency-Key`、脱敏审计和兼容演进规则。
4. 建立可离线执行的合成正向/负向一致性验证；不连接数据库、支付、网络或真实环境。

## 硬边界

- 服务广场入口继续保持 `protection-mall`、`/services/protection-mall`、`/services`、`shared_session`、`service_plaza.protection_mall.open` 和 `planned`。
- 禁止真实支付、资金状态变更、支付回调、退款、对账、部署、Schema迁移、真实会员或商家数据。
- 禁止前后端业务代码、路由挂载、数据库实现和第三方接口。
- 不引入Nova个性化推荐、跨模块组合订单或GraphRAG。
- 旧`6bce98f`及旧脏工作树继续封存，不得读取为可执行代码来源、cherry-pick或整体复制。

## 完成定义

1. 当前模块 checklist 全部逐项读取且 SHA 匹配，治理考试100分。
2. 责任边界、五类状态机、API公共规范均有版本化Schema/合同及正负合成案例。
3. 验证器证明非法状态转换、越权scope、缺幂等键、ID缺失、敏感审计和破坏性兼容变更全部失败关闭。
4. 模块依赖、合同验证、UTF-8、diff、scope和secret scan通过。
5. 同一record_id的IR与Handoff完成，平台会签和独立验收Go。

本检查点Go只表示M1合同首切片完成，不授权业务实现、支付、环境或上线。后续实现必须另立精确工作项。
