# CA-SC F0 前端实现报告

- 日期：2026-07-12
- work item：`AIW-20260712-CLUB-SC-FIRST-CLOSURE-FRONTEND`
- branch：`codex/club-sc-first-closure-frontend`
- base：`6149504959ea779102022d6b6e172fe0999dcaec`
- activation HEAD：`73b21bb15fcefa5aad4140619e9661216aca54c7`
- 当前结论：本地实现与自动化已验证；测试环境 T0 尚未执行

## 实现边界

1. H1 focused 页面只在 `selected_action_id=self-created-club` 时显示“进入自建俱乐部”CTA；点击 CTA 前仍不调用俱乐部业务 API。
2. 新增独立路由：
   - `/services/club-alliance/self-created`
   - `/services/club-alliance/self-created/applications`
   - `/services/club-alliance/self-created/:clubId`
3. `applications` 静态路由在 `:clubId` 前注册，避免被解释为详情 ID。
4. 新适配器只调用：
   - `GET /api/v1/clubs/search?type=standard&category=general...`
   - `GET /api/v1/clubs/:id`
   - `POST /api/v1/clubs/:id/join`
   - `GET /api/v1/clubs/join-applications/my`
5. 未复用或修改 `CoreServicePage`、`submissionRepository`、`ServicePlazaPage`、父 action adapter/contract、`ActionControl`。

## 安全与一致性

- 平台 action 与现有后端路由均为 `shared_session/Auth:true`。未登录访问 list/detail/applications 时只显示认证要求，三个页面均不会发业务请求。
- 搜索固定携带 `type=standard&category=general`；分页、total 和 items 以服务端结果为准，不调用 `/api/v1/clubs`，不做前端本地伪筛选。
- 列表和详情收到非 active、非 standard 或非 general 数据时返回 `CLUB_CATEGORY_CROSSOVER_DETECTED`，不丢弃异常项后继续展示。
- DTO 只投影允许字段，Club 文本使用 `intro`；不向页面传播 `owner_id/user_id/user_name/reviewed_by/internal_code/description`。
- join 由共享业务适配器生成/携带 `Idempotency-Key`；提交中和成功后按钮禁用，同一内容失败重试复用原键，服务端 replay header 映射为明确重放状态。
- 本人申请只发送 page/size/status，不发送 `user_id`，展示 pending/approved/rejected。
- create/review/member/payment/withdraw/refund/subscription/charity/family/federation 均不在网络面。

## 页面状态与可用性

- guest/authentication-required、loading、empty、ready、error、submitting、created、replayed 均有实现与测试。
- 401 会清理失效会话并回到认证页面。
- 支持关键词/城市服务端搜索、分页、直达、刷新、浏览器后退、返回俱乐部联盟和返回服务广场。
- CSS 包含 320px、360px/移动端和 900px 桌面有界布局，所有输入、按钮和链接具备 `:focus-visible`。
- loading/status 使用 `role=status`，错误使用 `role=alert`，列表、表单、分页和返回路径具有可访问名称。

## 自动化证据

- 定向：4 files / 60 tests。
- 前端全量：20 files / 179 tests。
- production build：通过。
- test-server build：通过。
- `Test-ServicePlazaContracts.ps1`：通过。
- CA-SC P0/P1 conformance：13/13 通过。
- governance checklist：28/28 completed，current SHA 一致。
- governance exam：100 分。

## 已发现合同漂移及关闭要求

### F0-CORR-001 guest access 漂移

- P0/P1 需求文档仍写 guest 可浏览 list/detail。
- 现行服务广场 action 使用 `shared_session`，后端 search/detail 路由均 `Auth:true`。
- 本实现采用运行时权威边界：未登录不得发 list/detail 请求。
- 平台在 T0 前必须受控修正 P0/P1 人类/机器合同和合成案例，使 access 与部署事实一致；不得为了旧文档把后端或前端降为匿名。

### F0-CORR-002 category error ID 漂移

- P0/P1 error catalog 写 `CLUB_CATEGORY_FILTER_INVALID`。
- 平台 `club-category-filter.v1` 和后端真实错误为 `CLUB_FILTER_CATEGORY_INVALID`。
- 前端采用后者；平台在 T0 前必须修正错误目录和 conformance，禁止同时长期保留两个含义相同的机器码。

上述漂移不否定本地 F0 实现，但在受控合同修正进入权威基线前，T0 保持 No-Go。

### F0-CORR-003 边界故障 HTTP 状态漂移

- P0/P1 error catalog 把 `CLUB_DETAIL_UNAVAILABLE` 记为 404、把 `CLUB_JOIN_UNAVAILABLE` 记为 409。
- 当前后端实现对这两个非业务性内部故障均返回 500；非 SC/非 active 详情另行隐藏为 404 `CLUB_NOT_FOUND`。
- 前端只依赖稳定 error ID，不根据错误文案或错误的 404/409 推断业务状态。平台必须在 T0 前裁定并统一 error catalog 与后端 HTTP 语义。

## 未完成和禁止推断

- 尚未部署测试环境，未执行真实登录、搜索、详情、申请、刷新持久、B 用户隔离和浏览器 UAT。
- 本报告不是首闭环最终 Go，不授权管理者审核、创建、成员、其他三类业务、资金、生产或真实数据。
