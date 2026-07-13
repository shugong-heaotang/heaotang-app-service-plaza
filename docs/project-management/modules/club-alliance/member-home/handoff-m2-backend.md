# H2-M2 会员首页后端授权 Handoff

- 状态：**Backend checkpoint Go / M3 pending**
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
- Implementation commit：`9d87240d3b95819d3c6dedb39042193ee0622e33`。
- Backend controlled integration：`97d8bfc5d1396f7907b1e76dfcb7c333a2913436`。
- IR 状态：`verified`，明确未达到 `deployed`。

## 授权时序偏差（现场保留）

- Backend actor 在 exam 100 分后、H2 owner 本次治理提交完成前，误判业务已 Go。
- 三个已授权后端文件已形成**未提交 diff**，并已运行定向 6 项；该结果只说明现场曾执行定向检查，不构成正式实现验收。
- Actor 已停止；未提交状态原样保留供总负责人检查，没有全量 `go test ./...`、`go vet ./...`、部署、commit、registry 修改或越界修改声明。
- 该现场随后由总负责人重新派发并独立复核；本段继续保留为历史偏差，不删除、不改写为当时已 Go。
- 后续实现修复、提交和集成证据见下节；历史现场 diff 本身仍不作为验收依据。

## 独立实现复核

- 定向 MemberHome：10/10 通过。
- `go test ./...`：通过。
- `go vet ./...`：通过。
- `git diff --check`：通过。
- P1 custom role 权限缺口已修复，并具有 custom manager role 允许、非 manager role 拒绝的正反例。
- 认证本人范围、禁止 `user_id`、三文件边界与未知类型失败关闭由实现和测试复核；未发现 schema、SC registry 或其他插件越界修改。

## M3 前风险与待办

- **真实环境来源表风险仍开放**：仓库内测试不能证明测试服务器上的成员、申请、角色、活动、待办和动态来源表已经具备四类 UAT 身份及正确关系；部署后必须以真实测试数据逐项核对，不能用空集合或合成前端数据代替。
- 尚未完成测试环境部署、服务就绪关联、前后端联调和四身份浏览器 UAT。
- 当前 `verified` 只证明后端仓库实现与独立 Go 门禁通过，不代表 `deployed`。

## 当前结论

**Backend checkpoint Go / M3 pending**。后端实现已可供受控部署联调；只有 M3 测试环境与四身份 UAT 证据齐全后，H2 才能继续向最终完成推进。
