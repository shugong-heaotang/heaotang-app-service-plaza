# H2-M2 会员首页后端授权 Handoff

- 状态：**Authorized / implementation pending**
- 提交人：Club Alliance module owner
- 接收人：Club Alliance backend agent
- 日期：2026-07-12
- Work item：`AIW-20260712-CLUB-MEMBER-HOME-BACKEND`

## 工作树与基线

- Repository：`C:/Users/shugo/Documents/heaotang-main`
- Worktree：`C:/Users/shugo/Documents/worktrees/heaotang-club-member-home-backend`
- Branch：`codex/club-member-home-backend`
- Base/HEAD at authorization：`d98f0601a45c4328ca5b14eac7fbea43c52c04a7`

## 唯一允许的业务范围

1. `backend-go/plugins/club-plugin/member_home.go`
2. `backend-go/plugins/club-plugin/member_home_test.go`
3. `backend-go/plugins/club-plugin/plugin.go`

不得修改数据库 schema、SC registry、APP collaboration registry、其他插件或前端；端点不得接受 `user_id`，必须使用认证会话中的本人身份。

## 已完成授权证据

- Backend actor checklist：completed。
- Backend actor governance exam：passed，100 分。
- 本 IR 仅为 `draft` 授权记录，不代表业务实现或验证完成。

## 授权时序偏差（现场保留）

- Backend actor 在 exam 100 分后、H2 owner 本次治理提交完成前，误判业务已 Go。
- 三个已授权后端文件已形成**未提交 diff**，并已运行定向 6 项；该结果只说明现场曾执行定向检查，不构成正式实现验收。
- Actor 已停止；未提交状态原样保留供总负责人检查，没有全量 `go test ./...`、`go vet ./...`、部署、commit、registry 修改或越界修改声明。
- 本 IR 继续为 `draft/authorized`，Handoff 继续为 `implementation pending`。
- 正式 implementation Go 必须等本治理证据集成后，由总负责人重新派发；不得凭现场 diff 自动续做。

## 实现完成前必跑门禁

- `gofmt` 覆盖全部修改的 Go 文件。
- 定向：`go test ./plugins/club-plugin -run MemberHome`（从 `backend-go` 执行，实际测试名以实现为准且不得缩小覆盖）。
- 全量：`go test ./...`。
- 静态检查：`go vet ./...`。
- Handoff 必须补充 exact commit、正反例、本人归属、未知类型失败关闭、数据库错误不降级、未改 schema/SC registry 的证据。

## 当前结论

治理门禁允许后端负责人开始三文件实现；后端业务仍为 pending。未取得代码、测试和独立验收证据前，不得标为 implemented、verified 或 H2 完成。
