# H2-M3 测试环境验收记录

- work item：`AIW-20260712-CLUB-MEMBER-HOME-M3-ACCEPTANCE`
- 时间：2026-07-12 11:43–11:53 Asia/Shanghai
- verdict：`No-Go / environment API and recovery passed; browser and lifecycle coverage Unverified`
- base URL：`https://heaotang.cn`
- APP source：`37c6c3aa65b9a1332732d552063d6e06a2d7643a`，包含 frontend integration `4a9b42ee9be3655deda13603c5a2bf55a8eeb121`
- backend source：`e41265905815082433e040412f3dd6b6b33dfede`
- secrets：`none-recorded`

## 1. 治理与本地门禁

- preflight：`ready`。
- current checklist：`28/28 completed`。
- governance exam：attempt 1，`100 / passed`。
- 前端：22 files、`225/225`；test-server build 通过。
- 后端：club-plugin 定向、`go test ./... -count=1`、`go vet ./...` 通过。
- fixture safety：passed；静态阶段 server mutations=0、OTP requests=0、secrets persisted=false。

## 2. 环境冻结、备份与部署

部署前：`/health?json=1=ok`，`/ready=ready`、`db=true`、plugins=24，PM2 online，SQLite WAL、integrity=ok。原二进制 SHA-256 为 `fec7bcbb58d6186d9c384b1b837479f592d978c145ce09c46e002763d9c565f1`；原入口资产为 `assets/index-6r_HRkaO.js`，SHA-256 为 `bfe4d9848d52ce4fac6d92edc3668bd78a20c7ca853301976fc6013d52038e99`。

部署证据：

- 后端备份：`/root/heaotang-backups/20260712-114720.tar.gz`；本地副本 `D:/Backup/heaotang-test-server/20260712-114720/test-server-state.tar.gz`。
- 前端备份：`/root/heaotang-backups/20260712-114825.tar.gz`；本地副本 `D:/Backup/heaotang-test-server/20260712-114825/test-server-state.tar.gz`。
- 后端部署二进制 SHA-256：`f5abea4d24230625c271ac0721ccd2837c291dfe5ad9fcc477465945354c30ec`；未轮换 secrets。
- 前端部署资产：`assets/index-DCYGiKy4.js`，SHA-256 `ce2a254c66d46505260ef89f52c9acda0c0707a24a96d0f392cdfe42adaa3de7`。
- 前端 rollback target：`/var/www/heaotang/app/service-plaza.rollback-20260712-114823`。
- 部署后 health/ready、9 services、20 actions、24 plugins 和公共资产验证均通过。

## 3. OTP 容量与凭据边界

四个批准合成身份在发送前均执行 UTC 日容量门禁，均为 `capacity_ready=true`。后续 family 与 manager 独立错误场景会话也在每次发送前重新核对容量。OTP、JWT、Cookie、Authorization、完整手机号和完整用户标识均未写入输出或证据；未重复执行任何加入申请。

## 4. Baseline 场景

RunId：`club-member-home-m3-20260712-115100-b4e9c201`。

- Plan → Apply → Inspect 通过：clubs=5、memberships=4、tasks=1、activities=2、registrations=2、announcements=3、notifications=3。
- 未登录真实 API：`GET /api/v1/clubs/member-home` 返回 401。
- 带 `user_id` 查询：返回 400，证明服务端拒绝跨用户查询参数。
- new-member：200，joined=0、tasks=0、activities=0、feed=0、can_manage=false。
- family-member：200，joined=1、tasks=1、activities=1、feed=1、can_manage=false。
- multi-club-member：200，joined=2、activities=1、feed=2、can_manage=false。
- manager：200，joined=1、can_manage=true。
- 所有返回的当前俱乐部状态对均为 `club_status=active / membership_status=active`；禁止响应字段命中 0。
- Cleanup 内置残留检查全为 0；users_deleted=0。

## 5. PartialError 场景

RunId：`club-member-home-m3-20260712-115200-5d7a8f32`。

- Plan → Apply → Inspect 通过：clubs=5、memberships=4、tasks=2，其余计数与 baseline 一致。
- family-member 真实 API 返回 200；关键 club 数据仍可用，`section_errors.tasks=CMH_TASKS_UNAVAILABLE`，状态对仍为 active/active。
- Cleanup 内置残留检查全为 0；users_deleted=0。

## 6. CriticalError 场景

RunId：`club-member-home-m3-20260712-115300-9ac043de`。

- Plan → Apply → Inspect 通过：clubs=5、memberships=5；run-owned `standard/health` 关系已挂到 manager。
- manager 真实 API 权威结果：HTTP 422，机器码 `CMH_CLUB_CLASSIFICATION_INVALID`。
- Cleanup 内置残留检查全为 0；users_deleted=0。

## 7. 恢复和最终状态

- 部署前隔离 RestoreVerify：RunId `club-member-home-m3-20260712-115000-7bce219f`，integrity=ok、schema objects=400、dump SHA match、live DB unchanged、临时文件清理完成。
- 关窗隔离 RestoreVerify：RunId `club-member-home-m3-20260712-115400-c62e1a04`，同样全部通过。
- 全局只读残留复核：本轮 fixture club=0、fixture notification=0。
- 最终 `/health?json=1=ok`、`/ready=ready`、`db=true`。

## 8. 未验证项与判定

浏览器运行时没有可用实例，发现结果为空。因此 direct/reload/back/return、DOM marker、五档 viewport、真实 Tab/Shift+Tab/Enter、离线态和浏览器网络分类均为 control-channel `Unverified`；未使用静态页面或组件测试替代。

环境没有获批的 maintenance 自然条件，按任务要求保持 `Unverified`，没有制造开关。pending/rejected 申请历史、left/suspended 会员历史和 dissolved 俱乐部生命周期也没有由本次已批准 fixture 提供安全构造机制；禁止直接 DB 业务捷径，因此环境覆盖保持 `Unverified`。API 已真实覆盖 ready、empty、partial-error、critical error 和 unauthorized；offline 因浏览器不可用为 `Unverified`。

最终结论为 No-Go，而不是 Full Go。已关闭部署、真实 API、局部错误、权威 422、清理和恢复风险；剩余阻塞是可见浏览器控制通道，以及缺少已批准的 lifecycle/history fixture。重测必须复用当前已部署 hash（若未漂移则禁止重复部署），恢复浏览器后只补浏览器矩阵；状态历史需另行批准最小 fixture 扩展，不能直接改库。
