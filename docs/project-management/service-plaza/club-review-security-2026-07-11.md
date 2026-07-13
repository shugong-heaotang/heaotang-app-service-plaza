# 俱乐部审核资源授权、事务故障与错误矩阵

- 日期：2026-07-11
- 工作项：`AIW-20260711-CLUB-REVIEW-SECURITY-GOVERNANCE` / `AIW-20260711-CLUB-REVIEW-SECURITY-BACKEND`
- 实现记录：`IR-20260711-CLUB-REVIEW-SECURITY`
- 后端提交：`ece6d4fe`
- 当前结论：本地实现与回归 Go；测试环境未部署，俱乐部 M2 仍 No-Go

## 资源授权

- 普通登录用户审核返回 403 / `CLUB_MANAGER_REQUIRED`；
- B 俱乐部管理者读取 A 俱乐部待审列表返回同一 403；
- B 俱乐部管理者使用 B 路径审核 A 的 application，在通过 B 的管理授权后返回 404 / `CLUB_APPLICATION_NOT_FOUND`；
- 所有拒绝场景保持原申请 pending。

稳定 403 只在待审列表和审核两个本切片接口显式返回。没有把通用 `requireClubManager` 改成写响应的 nil-return helper；测试曾证明这样会使几十个调用者继续执行业务逻辑，因此恢复了原非 nil 守卫语义，避免公共权限绕过。

## 事务故障矩阵

分别以数据库触发器强制以下写入失败：

1. `club_members` 成员插入；
2. `clubs.member_count` 更新；
3. `member_points` 积分插入；
4. `club_join_applications.status` 更新；
5. 延迟外键在事务 commit 时失败。

每种故障都验证：申请仍为 pending、无新成员、成员数保持原值、无积分、幂等 reservation 不残留。commit 故障移除后使用相同 key 重试成功，证明不是以换 key 绕过失败。

## 验证

- 插件定向测试通过；
- `go test -count=1 ./...` 通过；
- `go vet ./...` 与 `git diff --check` 通过；
- 400/403/404/409 机器错误矩阵已写入首切片契约并有 handler 测试。

## 未关闭

- 测试环境 JWT 双角色、跨俱乐部、并发和重放 HTTP 验收；
- 自建俱乐部权威筛选 `GET /api/v1/clubs/search?type=standard` 的混合类型正向回归；
- 俱乐部业务前端尚未由板块负责人正式启动。

因此依赖状态只记为 `implemented`，不得写成 `verified` 或 `deployed`。
