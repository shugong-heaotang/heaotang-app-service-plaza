# NOVA M2 人脉 Owner 与版本化工具契约任务通知书

- notice_id：`NOVA-M2-PEOPLE-TOOLS-TASK-20260712-001`
- platform_work_id：`AIW-20260712-NOVA-M2-PEOPLE-TOOLS-DISPATCH`
- owner_decision_work_id：`AIW-20260712-NETWORK-CANONICAL-OWNER-DECISION`
- contract_work_id：`AIW-20260712-NOVA-M2-PEOPLE-TOOLS-CONTRACT`
- 日期：2026-07-12
- 当前结论：`M2 No-Go`

## 1. 平台只处理的两个最小事项

### A. 人脉唯一 Owner 与 canonical 实现裁决

由人脉板块唯一负责人形成可审计决策：

- `network-plugin` 只可作为经加固的搜索读侧投影；
- `social-plugin` 的 `introduction_requests`/连接生命周期作为暂定 canonical 写侧；
- NOVA 只面向统一 People/Connection facade 或工具网关，禁止直连 legacy 写路由；
- `network` introductions/referral/status 写路径对 NOVA 标记 `forbidden/deprecated`；
- 形成 `introductions` 与 `introduction_requests` 的盘点、tenant 隔离、单向迁移、禁止双写、Sunset/410 和回滚方案；
- 未知 tenant 的历史记录隔离，不得自动归属。

该工作项只允许决策、内部依赖、迁移/禁用计划与治理证据，不修改任何后端代码。

### B. NOVA M2 四工具与 callback 版本化契约会签

工具集精确为：

1. `member_search`；
2. `connection_draft`；
3. `connection_send`；
4. `connection_status`。

`connection_result_callback` 是 server-to-server 协议，不是模型工具。合同必须覆盖 server identity、tenant、资源权限、字段可见性、确认票据、Idempotency-Key、trace/audit、稳定错误、回流责任和兼容策略。

合同工作项只形成 JSON/Schema/error catalog/fixtures/Python tests/会签结论，不修改人脉或 NOVA 业务代码。

## 2. 已确认风险

- `network` introduction/referral 接收正文 `from_user_id`，可伪造发起人；状态 PUT 缺资源归属授权。
- `network` member search 暴露 phone/city/bio，缺 tenant、目标字段可见性和同意策略。
- `social` 发起人来自服务端身份且状态更新绑定接收方，基础边界更安全，但仍缺 tenant、确认票据、幂等、审计、contact settings 和 RowsAffected 失败关闭。
- 两插件同时拥有 `introduction_requests`，同时存在 `introductions`，形成双 Owner/双事实源。

这些 legacy 路径不得直接包装为 NOVA 工具。

## 3. 人脉 Owner 工作项 metadata

- repository：`C:/Users/shugo/Documents/APP系统`
- branch：`codex/network-canonical-owner-decision`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-network-canonical-owner-decision`
- owner：`People Network module owner`
- owner_role：`人脉板块唯一负责人`
- base：以平台派发受控集成后的 exact APP HEAD 为准

精确允许路径：

- `docs/project-management/modules/network/README.md`
- `docs/project-management/modules/network/canonical-implementation-decision.md`
- `docs/project-management/modules/network/migration-disable-plan.md`
- `docs/project-management/modules/network/task-receipt.md`
- `docs/project-management/modules/network/handoff.md`
- `contracts/modules/network/internal-dependencies.v1.json`
- `contracts/modules/network/development-checklists/2026-07-12-network-canonical-owner*.json`
- `contracts/modules/network/governance-exams/2026-07-12-network-canonical-owner*.json`
- `contracts/modules/network/implementation-records/2026-07-12-network-canonical-owner*.json`

## 4. 工具契约工作项 metadata

- repository：`C:/Users/shugo/Documents/APP系统`
- branch：`codex/nova-m2-people-tools-contract`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-nova-m2-people-tools-contract`
- owner：`NOVA tool contract signoff agent`
- owner_role：`平台集成负责人`
- base：以平台派发受控集成后的 exact APP HEAD 为准

精确允许路径：

- `contracts/service-plaza/nova/nova-people-tools.v1.json`
- `contracts/service-plaza/nova/nova-people-tools.v1.schema.json`
- `contracts/service-plaza/nova/nova-people-tool-errors.v1.json`
- `contracts/service-plaza/nova/nova-people-tool-errors.v1.schema.json`
- `contracts/service-plaza/nova/nova-connection-callback.v1.json`
- `contracts/service-plaza/nova/nova-connection-callback.v1.schema.json`
- `contracts/service-plaza/nova/fixtures/m2/`
- `contracts/service-plaza/nova/test_nova_people_tools.py`
- `docs/project-management/modules/nova/m2-people-tools-signoff.md`
- `contracts/foundation/development-checklists/2026-07-12-nova-m2-people-tools-contract*.json`
- `contracts/foundation/governance-exams/2026-07-12-nova-m2-people-tools-contract*.json`
- `contracts/foundation/implementation-records/2026-07-12-nova-m2-people-tools-contract*.json`

## 5. 契约硬边界

- actor 与 tenant 仅来自 trusted server context；模型参数、正文和 query 不得扩大。
- `member_search` 只返回 opaque candidate_ref 与字段白名单；禁止完整手机号、证件、原始健康文本和未授权自由文本。
- `connection_draft` 只生成预览、披露清单/hash/version/expiry，不产生外部消息。
- `connection_send` 只接受 draft_id、version 与绑定 actor/tenant/target/draft/disclosure/trace/expiry 的确认票据，必须要求 Idempotency-Key。
- `connection_status` 只允许参与者或授权操作人读取，不泄露对方隐藏字段。
- callback 强制服务身份、tenant、event_id 幂等、同事件异载荷冲突；人脉 Owner 产生 canonical outbox，平台负责传输/认证，NOVA 只追加消费事件，失败进入 retry/DLQ 并通过 status 对账。
- 审计只记录允许字段和敏感数据 hash/脱敏摘要，不记录完整身份、消息、凭据或健康内容。

## 6. 最小验收

- exact 四工具 + 一个 callback；Schema Draft 2020-12；additionalProperties=false。
- 每项具 owner、authn、tenant_source、resource_policy、visible/redacted fields、confirmation、idempotency、audit、errors、compatibility 和 executable 状态。
- 稳定错误覆盖 context、tenant、permission、visibility、confirmation、idempotency、draft/version、status、callback、dependency、rate limit 和 internal failure。
- 正例覆盖 search/draft/send/status/callback。
- 负例覆盖 forged actor/tenant、cross-tenant、隐藏字段、opt-out、draft/target/version 漂移、票据缺失/过期/绑定错误、同键异载荷、未授权 status、非法迁移、callback 假服务身份/跨 tenant/事件冲突、legacy unsafe route 映射和 PII 输出。
- 机器测试必须拒绝任何工具映射到 network legacy introductions/referral/status 写路径。
- 人脉 Owner canonical 决策和工具契约两项都独立 Go 前，M2 保持 No-Go。

## 7. 明确禁止

- 真实会员数据、真实消息、真实连接发送、生产或不可逆迁移。
- 修改 network/social/backend/db/cmd/server。
- 把当前危险 legacy 路径直接包装为 NOVA 工具。
- 平台 Agent 代替人脉 Owner 作业务裁决，或用聊天确认替代仓库证据。
