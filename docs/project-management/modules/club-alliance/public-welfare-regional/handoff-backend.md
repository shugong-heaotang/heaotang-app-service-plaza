# 公益创办与区域中心后端 Handoff

- 后端仓库：`C:/Users/shugo/Documents/heaotang-main`
- 分支：`codex/club-public-welfare-regional-backend`
- 基线：`e41265905815082433e040412f3dd6b6b33dfede`
- 实现提交：`388846597131d75aafc54081070fe5fc0bf3ecd0`

## 已实现

- 公益创办申请提交、本人列表、管理员列表、撤回和审批。
- 批准后原子创建 `standard+charity+active` 俱乐部并授予发起人 owner。
- 普通创建入口拒绝直接创建公益俱乐部。
- 区域主任/副主任申请、本人列表、管理员列表和审批后精确区域授权。
- 区域管理中心/公益服务中心匿名地址搜索。
- maker-checker、自审拒绝、Idempotency-Key 重放、稳定错误和治理审计。

## 验证

- `go test ./plugins/club-plugin`：通过。
- `go test ./...`：通过。
- `go vet ./...`：通过。
- `gofmt`、`git diff --check`：通过。

未部署到测试服或生产；中心资料仍需由后续受控配置/管理能力录入。
