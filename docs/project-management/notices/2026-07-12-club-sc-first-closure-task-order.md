# CA-SC 自建俱乐部首个会员侧闭环任务通知书

- notice_id：`CA-SC-TASK-20260712-001`
- parent：`club-alliance`
- child project：`CA-SC`
- platform handoff：`SP-H034`
- date：2026-07-12
- status：正式下达

## 目标

完成会员侧最小可执行纵切：从俱乐部联盟标准首页进入自建俱乐部，服务端权威返回 `type=standard AND category=general AND status=active`；用户在共享登录会话中浏览列表与详情、幂等提交加入申请，并在本人申请列表中读取 `pending/approved/rejected` 状态。本切片不新增匿名业务读取能力。

本通知不包含管理者审核。首闭环的完成定义是“用户提交后可持久、可重放、可在本人状态中重新读取且跨用户隔离”，不是“申请已批准成为成员”。

## 权威事实与 supersedes

1. `D-CA-003` 已 Accepted；唯一 SC selector 是 `type=standard + category=general`。
2. 列表唯一权威接口是 `GET /api/v1/clubs/search?type=standard&category=general`；禁止 `/api/v1/clubs` 全量读取和前端本地伪筛选。
3. 本通知取代旧 `CA-TASK-20260711-001` 和 `club-alliance-first-slice-contract-v1.md` 中仅按 `type=standard` 的 selector 口径；旧文档只保留已验证的 join、本人申请、幂等与安全事实。
4. H0 Full Go 与 CA-H1 M4 Go 以 `SP-H025`、`SP-H029` 为准；模块 README 和历史 Handoff 中的旧 Pending/M3 描述不得作为当前门禁。
5. 父首页 `/services/club-alliance?category=自建俱乐部` 只负责 focused/导航，点击前仍只读 catalog/actions；业务进入独立子路由。

## 路由与接口

- 列表及状态入口：`/services/club-alliance/self-created`
- 本人申请：`/services/club-alliance/self-created/applications`，必须在 `:clubId` 前匹配
- 详情与加入：`/services/club-alliance/self-created/:clubId`
- 列表：`GET /api/v1/clubs/search?type=standard&category=general&page=&size=&q=&city=`
- SC 详情：`GET /api/v1/clubs/self-created/:id`，服务端必须拒绝非 active、非 standard 或非 general；共享 `GET /api/v1/clubs/:id` 保持类型无关的通用详情语义，不得被本切片收窄
- 加入：`POST /api/v1/clubs/:id/join`，强制 `Idempotency-Key`
- 本人状态：`GET /api/v1/clubs/join-applications/my?page=&size=&status=`，身份只来自认证会话

## 阶段与顺序

1. `CA-SC-P0/P1`：需求、决策边界、合同、Schema、错误目录、固定 seed fixtures、conformance、两层依赖与 Handoff。
2. `CA-SC-B0`：只关闭详情 `active+standard+general` 边界、稳定详情/join 错误和本人状态投影所需后端缺口；复用已有 search/join/my 能力。
3. `CA-SC-F0`：专用 adapter、列表/详情/加入/本人状态页面及自动化；不得复用旧 `CoreServicePage`/`submissionRepository`。
4. `CA-SC-T0`：测试环境备份、部署、真实 HTTP、双合成用户浏览器 UAT、网络/数据库脱敏证据与回滚验证。

每阶段必须独立 current checklist、考试100、实现记录、测试、Handoff、提交推送和平台 Go；父门禁 No-Go 只阻塞依赖它的下游。

## 合同硬边界

- 列表、详情和本人状态 DTO 不向页面暴露 `owner_id`、`user_id`、`user_name`、`reviewed_by` 或内部代码。
- 列表、详情、加入和本人状态全部继承 `shared_session`；guest 由父首页承接登录要求，不得先发 SC 业务请求。
- 详情稳定错误至少含 `CLUB_ID_INVALID`、`CLUB_NOT_FOUND`、`CLUB_DETAIL_UNAVAILABLE`。
- 加入稳定错误至少含 `INVALID_IDEMPOTENCY_KEY`、`CLUB_ID_INVALID`、`CLUB_NOT_FOUND`、`CLUB_JOIN_MESSAGE_TOO_LONG`、`IDEMPOTENCY_KEY_REUSED`、`IDEMPOTENCY_IN_PROGRESS`、`CLUB_NOT_ACTIVE`、`CLUB_ALREADY_MEMBER`、`CLUB_JOIN_UNAVAILABLE`。
- 首次加入 201；同键同规范化载荷重放 200 且 `Idempotency-Replayed:true`；同键异载荷 409；已有 pending 不得重复创建。
- 本人列表使用 v1 list envelope，分页默认 1/20、size<=100、ID 倒序；伪造 `user_id` 无效，跨用户零泄漏。
- family 容量规则不得进入 SC；任何 fee/payment/withdraw/refund/subscription 路由为 denylist。

## 合成数据

固定 seed：`HEAOTANG-CA-SC-20260712-V1`。只允许虚构标识，不得使用真实姓名、手机号、身份证、俱乐部申请、凭据或生产数据。

最小 fixture：5 个 active standard+general 跨两页；standard+charity、standard+health/trade、family、direct；pending/rejected/dissolved；guest、候选 A、隔离 B、既有成员 C。必须覆盖列表零串类、详情失败关闭、首次/重放/异载荷/并发、已有 pending、本人三状态和跨用户隔离。

## 明确禁止

创建俱乐部、创建审核、管理者待审/审核页面、成员管理、角色、退出、解散、公益/家庭/友联体业务、管理中心激活、会费/支付/退款/提现/订阅、生产、真实数据，以及免审/时限/撤回/冷却期等未决政策。

## 最终 Go

合同/Schema/conformance、后端相关测试与 vet、前端定向/全量/双 build、总合同与安全门禁全部通过；测试环境 `/health`、`/ready`、真实认证、搜索→详情→申请→本人状态→刷新持久与 B 用户隔离通过；320/360/768/desktop、键盘、直达/刷新/后退/返回、网络 denylist 和脱敏证据通过；无 Blocker 或未接受 Major。
