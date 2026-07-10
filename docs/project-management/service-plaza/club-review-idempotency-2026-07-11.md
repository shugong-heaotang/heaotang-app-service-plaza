# 俱乐部加入申请审核幂等与并发一致性

- 日期：2026-07-11
- 工作项：`AIW-20260711-CLUB-REVIEW-IDEMPOTENCY-GOVERNANCE` / `AIW-20260711-CLUB-REVIEW-IDEMPOTENCY-BACKEND`
- 实现记录：`IR-20260711-CLUB-REVIEW-IDEMPOTENCY`
- 后端提交：`e46c5e02`
- 当前结论：本地实现与回归 Go；测试环境未部署，俱乐部 M2 仍 No-Go

## 根因

原审核接口没有强制 `Idempotency-Key`，服务方法发现申请已非 pending 时直接返回现状。这会让网络重试无法与新请求区分，也会让不同键的相反决定看起来都“成功”，客户端无法知道自己的决定并未生效。

## 冻结语义

- 审核强制合法 `Idempotency-Key`；
- 哈希载荷包含 club、application、approved 和 trim 后 note；
- 同键同载荷返回原申请并设置 `Idempotency-Replayed: true`；
- 同键异载荷返回 409 / `IDEMPOTENCY_KEY_REUSED`；
- 不同键的相反决定并发时一个成功，另一个返回 409 / `CLUB_APPLICATION_ALREADY_REVIEWED`；
- application 不存在或与路径 club 不匹配统一返回 404 / `CLUB_APPLICATION_NOT_FOUND`，不泄露跨俱乐部资源存在性。

审核业务写入与幂等完成记录共用同一个数据库事务。批准路径的成员、成员数、积分和申请状态任一失败时全部回滚；失败 reservation 被释放，可使用相同请求安全重试。

## 验证

- 首次成功、规范化 note 重放和原资源返回通过；
- 同键相反决定得到 `ErrKeyReused`；
- 新键不能覆盖既有最终决定；
- 两个数据库连接并发批准/拒绝，严格一个成功、一个冲突；
- 最终申请只有一个状态，成员关系与最终状态一致；
- HTTP handler 缺键 400、首次 200、重放头、异载荷 409 通过；
- `go test -count=1 ./plugins/club-plugin` 通过；
- `go test -count=1 ./...`、`go vet ./...`、`git diff --check` 通过。

## 未关闭

- 测试环境 JWT/HTTP 并发、重放与错误信封验收；
- 普通用户审核 403、A 管理者不可读写 B 俱乐部的完整 HTTP 证据；
- member_count、member_points、application update 和 commit 各故障点矩阵；
- 全部 400/403/404/409 机器错误矩阵。

因此依赖状态只记为 `implemented`，不得写成 `verified` 或 `deployed`。
