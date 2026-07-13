# 俱乐部本人加入申请状态接口

- 日期：2026-07-11
- 工作项：`AIW-20260711-CLUB-MY-APPLICATIONS-GOVERNANCE` / `AIW-20260711-CLUB-MY-APPLICATIONS-BACKEND`
- 实现记录：`IR-20260711-CLUB-MY-APPLICATIONS`
- 后端提交：`7659c183`
- 当前结论：本地实现与回归 Go；测试环境未部署，俱乐部 M2 仍 No-Go

## 冻结接口

`GET /api/v1/clubs/join-applications/my?page=<1..>&size=<1..100>&status=pending|approved|rejected`

- 默认 `page=1`、`size=20`，状态可省略；
- 登录用户 ID 只取认证会话，客户端 `user_id` 不参与查询；
- 只返回本人申请，按 application ID 倒序；
- 使用统一 v1 列表信封，空结果明确返回 `items=[]`；
- 非法分页：400 / `INVALID_PAGINATION`；
- 非法状态：400 / `INVALID_CLUB_APPLICATION_STATUS`；
- 内部查询失败：500 / `CLUB_APPLICATIONS_UNAVAILABLE`。

静态路由注册在 `/api/v1/clubs/:id` 动态路由之前，避免 `join-applications` 被误解释为俱乐部 ID。

## 本地验证

- 本人隔离：查询参数伪造 `user_id=1` 不能改变会话用户 2 的结果；
- 状态过滤、倒序、分页总数和页大小通过；
- 空列表序列化为 `[]`；
- 分页和状态错误码稳定；
- `go test -count=1 ./plugins/club-plugin` 通过；
- `go test -count=1 ./...` 通过；
- `go vet ./...` 与 `git diff --check` 通过。

## 未关闭

- 测试环境 JWT/HTTP 级本人隔离、分页过滤和统一信封验收；
- 审核写入 Idempotency-Key 与并发相反决定；
- 跨俱乐部越权、错配 application ID 和全部事务故障证据；
- 完整 400/403/404/409 机器错误矩阵。

因此本接口依赖状态只记为 `implemented`，不得写成 `verified` 或 `deployed`。
