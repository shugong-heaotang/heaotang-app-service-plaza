# 自建俱乐部 type=standard 权威筛选

- 日期：2026-07-11
- 工作项：`AIW-20260711-CLUB-STANDARD-FILTER-GOVERNANCE` / `AIW-20260711-CLUB-STANDARD-FILTER-BACKEND`
- 实现记录：`IR-20260711-CLUB-STANDARD-FILTER`
- 后端提交：`d0154ad9`
- 当前结论：本地实现与回归 Go；测试环境未部署，俱乐部 M2 仍 No-Go

## 事实与修复

服务层原有 SQL 已正确使用 `WHERE status='active' AND type=?`，缺口不是重新实现查询，而是没有证明混合类型和非 active 数据不会进入自建俱乐部列表，HTTP 错误也只有通用码。

本切片增加：

- standard/direct/family 混合数据正向测试；
- pending standard 排除测试；
- HTTP `type=standard` 只返回 standard 的测试；
- 非法 type：400 / `INVALID_CLUB_TYPE`；
- query 超过 80 字符：400 / `SEARCH_QUERY_TOO_LONG`；
- city 超过 60 字符：400 / `CITY_FILTER_TOO_LONG`；
- 内部查询失败：500 / `CLUB_SEARCH_UNAVAILABLE`。

前端不得请求无 type 的 `/api/v1/clubs` 后再按标签筛选。

## 验证

- `go test -count=1 ./plugins/club-plugin` 通过；
- `go test -count=1 ./...` 通过；
- `go vet ./...` 与 `git diff --check` 通过。

## 未关闭

- 测试环境需准备合成的 standard/direct/family 和非 active 数据执行真实 JWT/HTTP 验收；
- 俱乐部业务前端尚未由板块负责人正式启动。

因此依赖状态只记为 `implemented`，不得写成 `verified` 或 `deployed`。
