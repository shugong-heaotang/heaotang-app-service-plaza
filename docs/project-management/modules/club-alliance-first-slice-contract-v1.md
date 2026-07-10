# 俱乐部联盟首切片内部契约 v1

首切片：自建俱乐部加入审核闭环。前台“自建俱乐部”固定使用现有 `GET /api/v1/clubs/search?type=standard`，筛选由后端权威执行，不使用 `/api/v1/clubs` 做前端标签伪筛选。用户通过 `POST /api/v1/clubs/:id/join` 幂等提交申请；管理者读取本俱乐部 pending 申请并批准或拒绝。批准时成员写入和申请状态必须在同一事务中成功，任何失败保持 pending。

## M2 前平台必须冻结并实现

1. 本人申请状态接口：精确路径、分页/过滤、状态枚举、v1 信封、本人归属、跨用户不可见和稳定错误码。
2. 审核写入幂等：`Idempotency-Key`、首次/重放/同键异载荷、并发相反决定及最终唯一结果；若豁免必须先有正式 ADR。
3. 修复标准俱乐部错误依赖家庭容量配置：只有 `type=family` 解析容量；家庭配置不可用时 standard 申请/批准仍成功，family 失败关闭。
4. HTTP 级越权和事务证据：普通用户审核 403、A 管理者不可读写 B 俱乐部、路径 club ID 与 application ID 错配拒绝、成员/积分/状态/commit 任一失败均保持 pending。
5. 冻结 400/403/404/409 机器错误矩阵，前端不得依赖错误文案。

上述五项未关闭时只允许 M0/M1 事实核对和接口变更申请，M2 No-Go。`club-manage` 动作仍为 preview；模块可以直测管理视图，但不得自行改为 active。

本人申请状态接口冻结为：

- `GET /api/v1/clubs/join-applications/my?page=<1..>&size=<1..100>&status=pending|approved|rejected`；
- `page` 默认 1，`size` 默认 20；状态可省略；按 application ID 倒序；
- 用户身份只取认证会话，忽略客户端传入的 `user_id`；仅返回本人记录；
- 成功使用统一列表信封 `data.items/total/page/size`，空结果 `items=[]`；
- 非法分页返回 HTTP 400 / `INVALID_PAGINATION`；非法状态返回 HTTP 400 / `INVALID_CLUB_APPLICATION_STATUS`；内部查询失败返回 HTTP 500 / `CLUB_APPLICATIONS_UNAVAILABLE`。

当前实现进度：第 3 项已在后端提交 `b8996793` 完成本地实现与全量 Go 回归；第 1 项已在后端提交 `7659c183` 完成本地实现、本人隔离/分页/过滤/空数组/稳定错误码测试及全量 Go 回归。测试环境 HTTP 验收前两项状态均为 implemented，不视为已关闭。第 2、4、5 项仍保持 No-Go。


家庭俱乐部、公益俱乐部、俱乐部友联体、会费、支付、提现和分账不属于本切片。页面、适配器和测试禁止调用 fee、account、paid-service、payment、withdraw 路由。付费家庭套餐、请求体价格和旧收入记账在资金专项根因修复、版本化定价、双人审批与资金安全门禁完成前不可激活。
