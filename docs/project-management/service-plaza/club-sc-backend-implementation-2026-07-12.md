# CA-SC 自建俱乐部后端实现检查点

## Outcome

后端实现与自动化完成，状态为 **Handoff Ready / Integration No-Go pending APP contract correction**。

- backend work item：`AIW-20260712-CLUB-SC-FIRST-CLOSURE-BACKEND`
- backend branch：`codex/club-sc-first-closure-backend`
- backend implementation commit：`b0ca6b7735287b22c90f84565cadbad67f710102`
- backend route-isolation fix：`d98f0601a45c4328ca5b14eac7fbea43c52c04a7`
- evidence work item：`AIW-20260712-CLUB-SC-FIRST-CLOSURE-BACKEND-EVIDENCE`
- checklist：`FC-20260712-CLUB-SC-FIRST-CLOSURE-BACKEND`（28/28，current SHA mismatch 0）
- exam：`EX-20260712-CLUB-SC-FIRST-CLOSURE-BACKEND-1`（100）

## Implemented

1. 共享 `GET /api/v1/clubs/:id` 恢复通用 Club 详情，继续支持 family/charity；新增且优先注册 `GET /api/v1/clubs/self-created/:id`，两者均保持 `Auth:true` shared-session 门禁。
2. SC 专用详情仅允许 `active+standard+general`；不存在、非 active、非 standard 或非 general 一律 404 `CLUB_NOT_FOUND`，隐藏资源存在性；内部读取异常才 500 `CLUB_DETAIL_UNAVAILABLE`。
3. 详情投影只返回 `id/name/intro/city/type/category/status/member_count/created_at`；拒绝 `description` 与内部字段。
4. join 新增稳定 `CLUB_JOIN_MESSAGE_TOO_LONG`；非已知内部错误统一 500 `CLUB_JOIN_UNAVAILABLE`。既有首次 201、同键同规范化载荷 200 + `Idempotency-Replayed:true`、异载荷 409 保持。
5. 本人申请投影移除 `user_id/user_name/reviewed_by/owner_id/internal_code`，身份继续只取认证会话。
6. standard SC 的 join/approval 继续绕过 family capacity 解析；family 缺配置继续失败关闭。
7. category 查询错误沿用权威 `CLUB_FILTER_CATEGORY_INVALID`，未新增第二套错误。

## Verification

- 定向 7 tests：Pass，包含通用 family/charity 成功、SC 专用路由优先级与不串类。
- `go test ./plugins/club-plugin -count=1`：Pass。
- `go vet ./plugins/club-plugin`：Pass。
- `go test ./...`：Pass。
- `go vet ./...`：Pass。
- `gofmt`、`git diff --check`：Pass。
- changed paths：3/3，全部位于后端 exact allowed paths。

## Contract correction prerequisite

平台 T0 独立审计发现 APP P0/P1 合同需先做受控修正，后端不得自行跨根修改：

1. 明确 list/detail 为 shared session，保持路由 `Auth:true`，不开放匿名。
2. 非 SC 或非 active 详情对外使用 404 `CLUB_NOT_FOUND`；`CLUB_DETAIL_UNAVAILABLE` 仅内部异常 500。
3. `CLUB_JOIN_UNAVAILABLE` 为内部失败 500。
4. category invalid 沿用 `CLUB_FILTER_CATEGORY_INVALID`。
5. SC 前端与机器合同必须改用 `GET /api/v1/clubs/self-created/:id`；共享 `/clubs/:id` 不能被单一子项目收窄。

在 APP 合同/错误目录/Schema/conformance和前端 detail adapter 修正并受控集成前，本后端提交不得被宣称 Contract Go 或激活 T0。

## Root-cause closeout

初版把共享 `/clubs/:id` 直接改成 SC 边界，造成 family/charity 通用详情回归风险。根因是把子项目语义施加到共享资源路由。修复采用专用、优先注册的 `/clubs/self-created/:id`，共享 route 恢复原语义；自动化同时证明专用路由不会被 `:id` 吞并且非 SC 仍 404 隐藏。

## Explicit exclusions

未修改创建、创建审核、管理者审核、成员管理、支付、部署、环境或生产；未复制 APP contracts 到后端 Git 根。
