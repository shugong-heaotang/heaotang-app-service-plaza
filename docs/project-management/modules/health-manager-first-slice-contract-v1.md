# 健康大管家首切片内部契约 v1

首切片：个人健康咨询提交与本人记录。用户登录后通过 `POST /api/v1/health/consultations` 幂等提交，通过 `GET /api/v1/health/consultations?page=<n>&size=<n>` 只读本人记录，初始状态为 `pending`。咨询正文属于敏感数据，不进入结构化日志。

## 已冻结行为

- 用户 ID 只取自登录会话；请求体不得指定归属用户。
- POST 必须携带 `Idempotency-Key`；首次创建为 201，同键同载荷重放为 200 并返回原资源和 `Idempotency-Replayed: true`，同键异载荷为 409 `IDEMPOTENCY_KEY_REUSED`。
- 本人列表按 `id DESC` 返回，空列表为 `items=[]`；当前分页安全范围为 page 最小 1、size 为 1..100，非法值回退 page=1、size=20。
- 前端必须复用共享 `BusinessApiAdapter.executeWithMeta`，不得直接调用 `fetch` 读取重放头。

## M2 前平台必须冻结并实现

1. `patient_name` 与 `symptoms` 的 trim、必填和服务端最大长度；禁止前端把空症状悄悄替换为固定句子。
2. POST/GET 可展示 DTO、稳定错误矩阵和敏感字段最小化；列表响应必须增加 `Cache-Control: no-store`。
3. 证明咨询正文不会进入结构化日志、遥测、截图和测试报告；M1/M4 只使用合成非真实健康数据。
4. 平台提供 `app/src/modules/health-manager` 的精确路由挂载工作项；模块负责人不得修改共享 `App.tsx`、认证或 SDK。

上述四项未关闭时只允许 M0/M1 事实核对和接口变更申请，M2 No-Go。

本切片不做 AI 诊断、医生预约、收费、健康报告生成或家庭共享。AI 同意、正式医疗免责声明、危急分流、供应商边界和保留规则未形成独立契约前，服务端不得把咨询正文发送给 AI，`ai_advice` 保持空值。测试环境临时提示固定为：“本服务仅接收健康咨询，不构成诊断或处方，也不替代急救；如有紧急情况，请立即呼叫 120 或前往医疗机构。”正式生产法律文本仍为独立 No-Go 门禁。
