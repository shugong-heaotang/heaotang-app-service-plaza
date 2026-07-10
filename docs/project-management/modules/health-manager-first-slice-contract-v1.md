# 健康大管家首切片内部契约 v1

首切片：个人健康咨询提交与本人记录。用户登录后通过 `POST /api/v1/health/consultations` 幂等提交，通过 `GET /api/v1/health/consultations?page=<n>&size=<n>` 只读本人记录，初始状态为 `pending`。咨询正文属于敏感数据，不进入结构化日志。

## 已冻结行为

- 用户 ID 只取自登录会话；请求体不得指定归属用户。
- POST 必须携带 `Idempotency-Key`；首次创建为 201，同键同载荷重放为 200 并返回原资源和 `Idempotency-Replayed: true`，同键异载荷为 409 `IDEMPOTENCY_KEY_REUSED`。
- 本人列表按 `id DESC` 返回，空列表为 `items=[]`；当前分页安全范围为 page 最小 1、size 为 1..100，非法值回退 page=1、size=20。
- 前端必须复用共享 `BusinessApiAdapter.executeWithMeta`，不得直接调用 `fetch` 读取重放头。
- `patient_name` 与 `symptoms` 均先执行 Unicode 空白 trim，再校验必填；最大长度分别为 80 和 2000 个 Unicode 字符。归一化发生在幂等载荷哈希之前，同键的等价空白输入必须重放原资源。
- 前端空白 symptoms 必须原样归一化为空字符串并由服务端返回 `HEALTH_SYMPTOMS_REQUIRED`；禁止生成默认症状、提示语或任何用户没有输入的健康内容。
- POST/GET 咨询响应统一返回 `Cache-Control: private, no-store`。请求体不是有效 JSON 返回 400 `INVALID_REQUEST_BODY`；姓名缺失/超长返回 `HEALTH_PATIENT_REQUIRED` / `HEALTH_PATIENT_TOO_LONG`；症状缺失/超长返回 `HEALTH_SYMPTOMS_REQUIRED` / `HEALTH_SYMPTOMS_TOO_LONG`。
- POST/GET 可展示 DTO 固定为 `id`、`patient_name`、`symptoms`、`status`、`created_at`；不得返回内部 `user_id` 或尚未批准的 `ai_advice`。请求体中的 `user_id`、`ai_advice` 必须忽略，归属只取会话。分页输入回退后，列表信封的 `page/size` 必须返回实际使用的 1/20，而不是原始非法值。列表内部失败返回 500 `HEALTH_CONSULTATIONS_UNAVAILABLE`。
- 在健康 AI 同意、供应商、医疗安全、危急分流和保留规则形成独立契约前，兼容路由 `POST /api/v1/health/analyze` 固定返回 503 `HEALTH_AI_CONSENT_REQUIRED`，不得读取健康档案/指标或调用 AI Provider；健康插件不得因此依赖 AI 插件。

## M2 前平台必须冻结并实现

1. `patient_name` 与 `symptoms` 的 trim、必填和服务端最大长度；禁止前端把空症状悄悄替换为固定句子。后端提交 `e361a8ac` 已实现，等待测试环境部署验证。
2. POST/GET 可展示 DTO、稳定错误矩阵和敏感字段最小化；列表响应必须增加 `Cache-Control: no-store`。输入错误矩阵和缓存头已在 `e361a8ac` 实现；最小 DTO、伪造字段忽略和分页回退信封已在 `a27b6f76` 实现。等待测试环境验证前状态为 implemented。
3. 证明咨询正文不会进入结构化日志、遥测、截图和测试报告；M1/M4 只使用合成非真实健康数据。平台生产路径扫描、动作遥测字段审计和空症状伪造回退修复已在前端提交完成；等待测试环境运行日志与 UAT 制品复核前状态为 implemented。
4. 平台提供 `app/src/modules/health-manager` 的精确路由挂载工作项；模块负责人不得修改共享 `App.tsx`、认证或 SDK。

上述四项未关闭时只允许 M0/M1 事实核对和接口变更申请，M2 No-Go。

本切片不做 AI 诊断、医生预约、收费、健康报告生成或家庭共享。AI 同意、正式医疗免责声明、危急分流、供应商边界和保留规则未形成独立契约前，服务端不得把咨询正文发送给 AI，`ai_advice` 保持空值。测试环境临时提示固定为：“本服务仅接收健康咨询，不构成诊断或处方，也不替代急救；如有紧急情况，请立即呼叫 120 或前往医疗机构。”正式生产法律文本仍为独立 No-Go 门禁。
