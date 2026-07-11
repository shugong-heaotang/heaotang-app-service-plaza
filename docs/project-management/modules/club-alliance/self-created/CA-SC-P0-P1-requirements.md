# CA-SC P0/P1 需求与合同边界

## 目标

冻结自建俱乐部首个会员侧闭环：列表、详情、加入申请、本人申请状态。提交成功只代表申请可持久、可幂等重放、可由本人重新读取；不代表已批准或已成为成员。

## 权威规则

1. 列表仅允许 `GET /api/v1/clubs/search?type=standard&category=general`，分页默认 1/20、`size<=100`。
2. 列表与详情继承服务广场 `shared_session`，必须登录；本切片不新增匿名读取能力。
3. SC 详情使用专用 `GET /api/v1/clubs/self-created/:id`；共享 `GET /api/v1/clubs/:id` 保持类型无关的通用详情兼容性。专用详情仅返回 `status=active AND type=standard AND category=general`；不存在、非 active 或非 SC 资源统一返回 `CLUB_NOT_FOUND` 404，内部读取故障返回 `CLUB_DETAIL_UNAVAILABLE` 500。
4. 加入必须认证并提供 `Idempotency-Key`。首次 201；同键同规范化载荷重放 200 且 `Idempotency-Replayed:true`；同键异载荷 409；已有 pending 不重复创建；内部故障返回 `CLUB_JOIN_UNAVAILABLE` 500。
5. 本人列表身份只来自认证会话，伪造 `user_id` 无效；按 ID 倒序并严格跨用户隔离。
6. Club 文本字段统一使用后端权威 `intro`，禁止发明 `description`；DTO 禁止暴露 `owner_id/user_id/user_name/reviewed_by/internal_code`。
7. 页面路径 `clubId` 只接受不带符号和前导零的正十进制安全整数；科学计数、十六进制、`+`、前导零、0、负数和超大值必须在请求前返回 `CLUB_ID_INVALID`，网络请求为零。

## 角色

- guest：由父首页 ActionControl 承接登录要求；未登录不得调用 SC 列表、详情、加入或本人状态接口。
- candidate A：可提交一次加入并读取自己的 pending/approved/rejected。
- isolated B：只能读取 B 自己的申请，不能观察 A。
- existing member C：重复加入失败关闭。

## 非目标

创建、创建审核、管理者审核、成员/角色管理、退出、解散、公益/家庭/友联体、管理中心激活、会费/支付/退款/提现/订阅、生产和真实数据。

## 完成门禁

JSON/Schema、固定 seed fixtures、稳定错误、正负例 conformance、两层依赖、current R2 检查单、100 分考试、IR 与 Handoff 全部通过。本门禁不授权 API 或页面实现。
