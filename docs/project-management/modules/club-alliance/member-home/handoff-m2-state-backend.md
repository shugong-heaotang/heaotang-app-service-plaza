# H2 会员首页状态分层后端 Handoff

- 状态：**Backend state checkpoint Go / integration and M3 pending**
- 提交人：H2 backend state agent
- 接收人：平台集成负责人
- 日期：2026-07-12
- Backend work item：`AIW-20260712-CLUB-MEMBER-HOME-STATE-BACKEND`
- Evidence work item：`AIW-20260712-CLUB-MEMBER-HOME-STATE-BACKEND-EVIDENCE`

## 工作树与提交

- Backend repository：`C:/Users/shugo/Documents/heaotang-main`
- Backend worktree：`C:/Users/shugo/Documents/worktrees/heaotang-club-member-home-state-backend`
- Backend branch：`codex/club-member-home-state-backend`
- Backend base：`98426ff83a1218080019faa377c152a81ecca437`
- Backend commit：`49227de982d0dc417542652823449a454d380ac2`
- Push：`origin/codex/club-member-home-state-backend` 成功
- Evidence repository：`C:/Users/shugo/Documents/APP系统`
- Evidence worktree：`C:/Users/shugo/Documents/worktrees/heaotang-club-member-home-state-backend-evidence`
- Evidence branch：`codex/club-member-home-state-backend-evidence`
- Evidence base：`3fc48afbbe934d9ec31d4a9c958c0dab01290031`

## 治理证据

- Preflight：`ready`。
- Current checklist：`FC-20260712-CLUB-MEMBER-HOME-STATE-BACKEND`，28/28，当前 SHA 全部匹配。
- Governance exam：`EX-20260712-CLUB-MEMBER-HOME-STATE-BACKEND-1`，attempt 1，100 分。
- Implementation record：`IR-20260712-CLUB-MEMBER-HOME-STATE-BACKEND`，`verified`。

## 实现结论

- `memberHomeClub` 删除含义不明的 JSON 字段 `status`，精确新增 `club_status` 与 `membership_status`。
- `club_status` 来自俱乐部表并统一小写、去除首尾空白；`dissolved` 保持俱乐部生命周期含义。
- 当前 schema 的 `club_members` 没有状态列；存在行代表当前 active，退出会删除行。因此本检查点只发 `membership_status=active`，不伪造 `left` 或 `suspended`。
- pending/rejected 加入申请来自 `club_join_applications`，查询不读取该实体；负例证明不会被提升为当前俱乐部。
- left 历史没有当前 `club_members` 行；负例证明缺少当前行时不会进入列表。
- handler 正例核对响应中两个精确状态字段；DTO 负例核对旧 `status` 不再出现。

## 验证证据

- `gofmt -w plugins/club-plugin/member_home.go plugins/club-plugin/member_home_test.go`：通过。
- `go test ./plugins/club-plugin -run 'TestMemberHome' -count=1`：通过。
- `go test ./...`：通过。
- `go vet ./...`：通过。
- Backend `git diff --check`：通过。
- Backend 允许路径审计：仅 `member_home.go`、`member_home_test.go`。
- Changed-file sensitive-pattern scan：0 matches。

## 未完成与边界

- 未部署、未做数据库迁移、未修改路由、其他插件、SC remediation 或 collaboration registry。
- 未实现 `suspended`；只有未来建立权威服务端状态列、迁移与独立验收后才可发出。
- 未完成受控集成、测试环境部署、原始实体关联和 M3 浏览器 UAT。
- 当前 `verified` 不等于 `deployed`，也不构成 H2 Full Go。

## 当前结论

**Backend state checkpoint Go / integration and M3 pending**。允许平台集成负责人独立复核并受控集成这一个后端提交；不授权部署或扩展其他范围。
