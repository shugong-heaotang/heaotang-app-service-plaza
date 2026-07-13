# 人脉 canonical 实现裁决

- decision_id：`NETWORK-CANONICAL-20260712-001`
- 状态：`Accepted for architecture; implementation No-Go`
- decision_maker：People Network module owner
- decision_date：2026-07-12
- scope：人脉搜索、引荐请求、连接状态及 NOVA M2 对接边界

## 事实基线

1. `network-plugin` 的 `POST /api/v1/network/introductions` 和 `POST /api/v1/network/referral` 从正文读取 `from_user_id`，未以服务端登录身份覆盖。
2. `PUT /api/v1/network/introductions/:id` 按 id 更新，没有参与者或 tenant 资源归属条件。
3. `network-plugin` 的搜索/bridge/marketplace 读取 phone、city、bio 等字段；当前没有 tenant 与逐字段可见性合同。
4. `network-plugin` 与 `social-plugin` 都写 `introduction_requests`；另有独立 `introductions` 表，形成多入口、多语义和多事实源风险。
5. `social-plugin` 从服务端身份取得发起人，响应更新绑定 `to_member_id` 和 pending 状态，基础边界更安全；但仍缺 tenant、确认票据、幂等、稳定审计、RowsAffected 失败关闭和 NOVA trace。

以上只证明代码事实，不证明接口安全、测试环境可用或 NOVA M2 Go。

## 裁决

### 1. 唯一领域所有权

人脉连接领域的唯一 Owner 为 `People Network module owner`。`network-plugin` 与 `social-plugin` 不再分别拥有连接写语义；任何新写入只能经版本化 People/Connection facade 进入 canonical service。

### 2. canonical 读写边界

- 读侧：保留 `network-plugin` 作为候选发现投影，但必须先输出 opaque `candidate_ref`，由服务端上下文提供 actor/tenant，并执行目标字段可见性、opt-out、屏蔽关系和最小披露策略。未加固前为 `forbidden for NOVA`。
- 写侧：选择 `social-plugin` 的 `introduction_requests` 生命周期作为 canonical 目标模型。选择理由是发起人来自服务端身份、接收方响应受资源条件约束，并已有连接与 contact settings 语义。它仍只是迁移目标，未加固前不得由 NOVA 调用。
- `introductions` 表及 `network` introductions/referral/status 路径为 legacy；冻结新增调用方和新功能，禁止映射到 NOVA。
- NOVA 只依赖 facade 的 `member_search`、`connection_draft`、`connection_send`、`connection_status`；callback 由 canonical outbox 产生。模型参数不得成为 actor、tenant 或权限来源。

### 3. 单一真相源不变量

1. 一次连接请求只有一个 canonical request id、tenant id 和状态机。
2. 禁止 facade、network、social 之间双写。
3. actor、tenant、资源权限和披露策略只来自可信服务端上下文。
4. draft 不发送；send 必须持绑定 actor/tenant/target/version/disclosure/expiry 的确认票据和 `Idempotency-Key`。
5. 状态与 callback 只从 canonical 写侧/outbox 派生；同 event id 异载荷冲突。

## 被禁止的替代方案

- 直接包装 `network` legacy introductions/referral/status。
- 继续让 network 与 social 同时写 `introduction_requests`。
- 以正文/query 中的 user id 或 tenant id 作为权威身份。
- 把 `introductions` 和 `introduction_requests` 静默拼接成同一状态列表。
- 在 tenant 不明时自动归属历史记录。

## 可证伪前提与复审

- 前提：`social` 的请求生命周期可在不破坏已有记录的前提下扩展 tenant、幂等、确认和审计。若数据盘点证明其语义无法稳定承载连接请求，必须复审 canonical 目标。
- 前提：`network` 发现能力可被收敛为最小投影。若字段可见性无法服务端执行，应停用该投影并另建搜索索引。
- 复审触发：出现跨 tenant 数据、双写、状态分叉、身份伪造、无法回滚迁移、法规/隐私前提变化或新连接类型。
- 兼容性：facade v1 仅兼容新增；legacy 禁用按迁移窗口执行，破坏性状态通过稳定 `410` 和替代接口信息显式发布。

## 门禁结论

canonical architecture Accepted；development、acceptance、release、operations 仍 No-Go/Pending。只有工具契约独立 Go、facade 和 canonical 写侧实现验收、迁移 dry-run/restore 验证及 legacy 禁用回归全部通过，NOVA M2 才可重新评估。
