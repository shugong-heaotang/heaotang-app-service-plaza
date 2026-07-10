# 健康咨询本人历史最小展示 DTO

- 日期：2026-07-11
- 工作项：`AIW-20260711-HEALTH-HISTORY-GOVERNANCE` / `AIW-20260711-HEALTH-HISTORY-BACKEND`
- 实现记录：`IR-20260711-HEALTH-HISTORY`
- 后端提交：`a27b6f76`
- 当前结论：本地实现与回归 Go；测试环境未部署，健康 M2 仍 No-Go

## 根因

服务层本人列表和跨用户隔离已经存在，但 HTTP 直接序列化内部 `Consultation`，把 `user_id` 与尚未批准的 `ai_advice` 一并暴露；非法分页虽然查询层回退到 1/20，响应信封仍可能回显原始 0/101，造成接口自相矛盾。

## 修复

- POST/GET 固定输出 `id/patient_name/symptoms/status/created_at`；
- 排除内部 `user_id` 和 `ai_advice`；
- 请求体伪造 `user_id`、`ai_advice` 不参与持久化；
- 列表只按会话用户读取，查询参数 `user_id` 无效；
- page<1 回退 1，size 不在 1..100 回退 20，信封与实际查询一致；
- 列表内部失败稳定返回 500 / `HEALTH_CONSULTATIONS_UNAVAILABLE`；
- POST/GET 继续设置 `Cache-Control: private, no-store`。

## 验证

- 合成用户 101 只能看到本人记录，伪造 user_id=202 无效；
- POST 与 GET JSON 均不存在 user_id/ai_advice；
- 页面必需五字段完整；
- page=0、size=101 实际及信封均回退 1/20；
- 伪造建议不持久化；
- `go test -count=1 ./plugins/health-plugin`、`go test -count=1 ./...`、`go vet ./...`、`git diff --check` 通过。

## 未关闭

- 测试环境真实 JWT/HTTP 的 DTO、缓存头、本人隔离和分页回退验收；
- 咨询正文不进入日志、遥测、截图和测试报告的专项扫描；
- 健康页面由板块负责人正式派发后实现。

因此依赖状态只记为 `implemented`，不得写成 `verified` 或 `deployed`。
