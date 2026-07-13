# APP 公共 `/api/nova` v1 契约会签

- 工作项：`AIW-20260712-NOVA-API-CONTRACT-SIGNOFF`
- 会签角色：平台集成负责人
- 结论：`Go for NOVA M1 contract implementation`
- 范围：仅确认 APP 公共边界；不代写 NOVA 运行时，不授权 M2 真实人脉闭环。

## 会签边界

平台确认 `nova-api-contract.v1` 为 M1 实现边界：身份和租户来自可信服务端上下文，权限由服务端执行；模型不得扩大 scope。外部影响、隐私披露、发布、商业承诺和权益变化必须进入统一确认。写操作遵循 `Idempotency-Key` 重放与冲突语义，恢复和重试不得重复副作用。

任务、步骤、事件、确认和工具结果必须保留 trace、主体、租户、契约版本及脱敏审计。稳定错误至少包含 `code`、`message`、`trace_id`、`retryable` 和安全 `details`；`waiting_confirmation` 是任务状态，不是失败。

NOVA 板块负责人实现运行时和兼容适配；平台集成负责人维护公共边界、执行抽查和最终集成。`/api/nova/ask`、`/api/chat` 与既有业务 API 保持兼容，不得削弱上述安全边界。新增兼容字段走次版本；破坏性变化必须新主版本并重新会签。

## 证据

- Schema：`contracts/service-plaza/nova/nova-api-contract.v1.schema.json`
- 已签契约：`contracts/service-plaza/nova/nova-api-contract.v1.json`
- 拒绝夹具：`contracts/service-plaza/nova/fixtures/invalid-model-scope.json`
- 自动测试：`tests/contracts/nova/test_nova_api_contract.py`

本会签满足 `NOVA-M0-001 Conditional Go` 的条件 2，但是否最终激活 M1 仍由项目最高负责人结合条件 1 证据裁决。

## 治理闭环

- 当前检查单：`FC-20260712-NOVA-API-CONTRACT-SIGNOFF`，26 项 completed。
- 随机考试：`EX-20260712-NOVA-API-CONTRACT-SIGNOFF-1`，第一次 8/8、100 分。
- 实现记录：`IR-20260712-NOVA-API-CONTRACT-SIGNOFF`。
- `blocks`：无；两项 Conditional Go 激活条件均已有权威证据。
- `does_not_block`：M2 人脉真实闭环仍按后续独立检查点推进，不属于本次 M1 授权。

平台会签最终结论：`Go`。NOVA 板块可在已登记允许路径内启动 M1；不得修改 APP 受保护契约，不得提前实现 M2。
