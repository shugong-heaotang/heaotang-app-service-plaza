# NOVA M2 Provider 三包正式任务通知书

- notice_id：`NOVA-M2-PROVIDER-TASK-20260712-001`
- platform_work_id：`AIW-20260712-NOVA-M2-PROVIDER-DISPATCH`
- 日期：2026-07-12
- 当前总门禁：`M2 No-Go`

## 1. 已满足前置

- 人脉唯一 Owner/canonical 决策已 integrated。
- `member_search`、`connection_draft`、`connection_send`、`connection_status` 与 server callback 契约包已 integrated，全部 `executable=false`。
- legacy network unsafe write 已在合同和 Owner 决策中明确 forbidden。

上述只允许启动 provider 实现与临时数据库演练，不代表 M2 development Go、环境 Go 或真实消息授权。

## 2. 三个主业务包

### P1 Network Read Provider

- work_id：`AIW-20260712-NOVA-M2-NETWORK-READ-PROVIDER-BACKEND`
- repository：`C:/Users/shugo/Documents/heaotang-main`
- branch：`codex/nova-m2-network-read-provider`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-nova-m2-network-read-provider`
- owner：`NOVA network read provider agent`
- base：激活时的 authoritative backend integration exact HEAD
- companion evidence：`AIW-20260712-NOVA-M2-NETWORK-READ-PROVIDER-EVIDENCE`

精确代码路径：

- `backend-go/plugins/network-plugin/nova_member_search_provider.go`
- `backend-go/plugins/network-plugin/nova_member_search_provider_test.go`

首检查点只实现未挂路由的 provider 核：trusted server actor/tenant 输入、candidate opaque ref、目标字段策略/opt-out、字段白名单、分页/速率限制决定、审计记录与稳定错误。禁止 introduction/referral/status 写、禁止修改 legacy `plugin.go/service.go`、禁止真实会员数据。

### P2 Social Write Provider

- work_id：`AIW-20260712-NOVA-M2-SOCIAL-WRITE-PROVIDER-BACKEND`
- repository：`C:/Users/shugo/Documents/heaotang-main`
- branch：`codex/nova-m2-social-write-provider`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-nova-m2-social-write-provider`
- owner：`NOVA social write provider agent`
- base：激活时的 authoritative backend integration exact HEAD
- companion evidence：`AIW-20260712-NOVA-M2-SOCIAL-WRITE-PROVIDER-EVIDENCE`

精确代码路径：

- `backend-go/plugins/social-plugin/nova_connection_provider.go`
- `backend-go/plugins/social-plugin/nova_connection_provider_test.go`

首检查点只实现未挂路由的 provider 核：draft/version/disclosure hash、确认票据校验、Idempotency-Key 同键重放/异载荷冲突、参与者授权、contact settings、冷却、RowsAffected fail-close、canonical status 与 transactional outbox。仅使用临时/模拟 SQLite；禁止真实消息、外部通知和生产写入，禁止修改 legacy `plugin.go/service.go/types.go`。

### P3 Migration & Disable Drill

- work_id：`AIW-20260712-NOVA-M2-MIGRATION-DISABLE-DRILL`
- repository：`C:/Users/shugo/Documents/APP系统`
- branch：`codex/nova-m2-migration-disable-drill`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-nova-m2-migration-disable-drill`
- owner：`NOVA migration and disable drill agent`
- base：激活时的 authoritative APP integration exact HEAD

精确允许路径：

- `scripts/Manage-NovaPeopleMigrationDrill.ps1`
- `scripts/Test-NovaPeopleMigrationDrillSafety.ps1`
- `contracts/modules/network/migration/nova-introduction-migration.v1.json`
- `contracts/modules/network/migration/nova-introduction-migration.v1.schema.json`
- `contracts/modules/network/migration/fixtures/`
- `docs/project-management/modules/network/migration-drill-plan.md`
- `docs/project-management/modules/network/migration-drill-report.md`
- `docs/project-management/modules/network/migration-drill-handoff.md`
- `contracts/modules/network/development-checklists/2026-07-12-nova-m2-migration-disable*.json`
- `contracts/modules/network/governance-exams/2026-07-12-nova-m2-migration-disable*.json`
- `contracts/modules/network/implementation-records/2026-07-12-nova-m2-migration-disable*.json`

仅对临时或明确测试数据库执行 Plan/Apply/Inspect/Cleanup/RestoreVerify：`introductions -> introduction_requests` 单向迁移、unknown tenant quarantine、禁止双写、legacy Sunset/410 successor 合同和回滚验证。首检查点不得修改后端路由；410 真实激活必须等 P1/P2 provider Go 后另行授权。回滚只能恢复安全旧数据，不得重新开放 unsafe writes。

## 3. 后端伴随治理证据

后端 Git 根没有 APP 的治理目录。不得把 APP `contracts/foundation` 相对路径登记到后端工作项，也不得复制一套治理仓库。因此 P1/P2 各有一个同 owner 的 APP companion evidence item，只保存 current checklist、100 分考试、IR 和 Handoff，不拥有 Go 源码：

- `AIW-20260712-NOVA-M2-NETWORK-READ-PROVIDER-EVIDENCE`
- `AIW-20260712-NOVA-M2-SOCIAL-WRITE-PROVIDER-EVIDENCE`

companion 不是额外业务包；主后端 commit、tests、gofmt、go test、go vet 必须由 companion IR 精确引用。

## 4. 两层依赖

平台层：identity/API、authorization/idempotency、contract tooling、observability/config 与 delivery recovery 必须继续 Go。

内部层：

- Owner decision integrated；
- tools/callback contract integrated；
- provider status 初始 `planned/code-present-unverified`；
- migration 只接受 canonical target 与 tenant quarantine 规则；
- legacy write authority=forbidden。

任一包不得用另一个包未 Go 的行为作已实现前提。

## 5. 共同验收与禁止

每包必须独立 preflight、current checklist、100 分考试、IR、Handoff、精确范围、单元/契约/安全正反例和独立复核。

P1/P2：gofmt、定向与全量 Go tests、go vet；必须证明 trusted actor/tenant 不可由正文伪造、跨 tenant/跨资源拒绝、字段/消息最小化、稳定错误、无凭据输出。

P3：唯一 RunId、临时/测试 DB allowlist、Plan 默认零 mutation、Apply 前备份、Inspect 数量/冲突、Cleanup/RestoreVerify、unknown tenant quarantine、双写检测、410 successor 与 rollback 不重开 unsafe writes；禁止生产连接字符串。

三包全部 Go 后仍需组合部署和测试环境安全验收；此前 `M2 development_readiness` 不得改为 Go。禁止真实会员数据、真实搜索、真实消息、生产、资金和不可逆迁移。
