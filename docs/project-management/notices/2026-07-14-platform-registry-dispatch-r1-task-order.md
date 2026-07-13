# 平台注册表串行派发 R1 任务通知

- work_id：`AIW-20260714-PLATFORM-REGISTRY-DISPATCH-R1`
- 下达方 / approver：项目最高负责人
- owner：`Platform registry dispatch agent`
- owner_role：平台集成负责人
- developer_role：平台注册表派发授权记录人
- reviewer_role：APP 总架构独立验收负责人
- priority / risk：`P0 / high`
- flow：`governance-repair`
- exact base：`384304a87e2a6965dc6cb3cdcafd2a92eef7d101`
- branch：`codex/platform-registry-dispatch-r1`
- workspace：`C:/Users/shugo/Documents/worktrees/heaotang-platform-registry-dispatch-r1`

## 直接授权来源

项目最高负责人在当前“24 小时项目”会话中明确批准持续完成全部已授权剩余任务，并要求 `/root` 监督、安排各板块负责人自行执行。本通知记录该 direct-principal 授权交易：当 exact base `384304a` 没有任何 `active` 或 `handoff-ready` 工作项拥有 `contracts/foundation/agent-collaboration.v1.json` 时，由平台集成负责人建立唯一最小 registry-owning 工作项，恢复受控串行派发能力。

现有 `README.md`、`AGENTS.md`、ADR 0015/0016 要求平台注册表由平台集成负责人控制、高风险治理变更接受独立验收；它们未禁止由项目最高负责人事前批准的最小 bootstrap 交易。本任务严格保持 developer / reviewer / approver 分离。

## 唯一职责

1. 记录本工作项自身的 root-of-trust 授权、current checklist、随机治理考试、实施记录和 Handoff。
2. 本候选经独立验收并受控集成后，平台集成负责人才能按顺序更新或激活已经登记为 `planned` 的平台项：先 `AIW-20260713-PLATFORM-EXAM-IR-CROSS-RECORD-GATE-R1`，后 `AIW-20260713-PLATFORM-NOVA-OVERLAY-R2`。
3. 任一时刻只允许一个拥有共享路径的工作项进入 `active` 或 `handoff-ready`；cross-record 与 NOVA overlay 共享 `scripts/Test-ServicePlazaContracts.ps1`，禁止同时激活。

## 明确非目标与禁止项

- 本候选不激活 cross-record，不激活 NOVA overlay。
- 不实现业务、validator、测试逻辑或部署。
- 不修改任何已登记 planned 项的字段。
- 不自行增加 `allowed_paths`，不把 registry 权限下放给实施 Agent。
- 不接触生产、真实会员数据、真实资金或不可逆操作。
- 如果治理规则明确拒绝 direct-principal bootstrap，则立即停止并报告，不寻找绕过方式。

## Allowed paths

- `contracts/foundation/agent-collaboration.v1.json`
- `docs/project-management/notices/2026-07-14-platform-registry-dispatch-r1-task-order.md`
- `contracts/foundation/development-checklists/2026-07-14-platform-registry-dispatch-r1*.json`
- `contracts/foundation/governance-exams/2026-07-14-platform-registry-dispatch-r1*.json`
- `contracts/foundation/implementation-records/2026-07-14-platform-registry-dispatch-r1*.json`
- `contracts/foundation/invalidated-snapshots/platform-registry-dispatch-r1/`（仅保存本次 R1 checklist、attempt-1 原字节及一份原因 manifest；由 `/root` 作为项目最高负责人授权链监督人于 2026-07-14 明确批准，不构成一般自扩权）
- `docs/project-management/service-plaza/platform-registry-dispatch-r1-handoff.md`

## 验收条件

1. 相对 exact base，registry 原 123 rows 逐字段不变，仅在末尾新增本工作项。
2. 新建且逐项读取完成的 26/26 current checklist；同一 `record_id` 随机考试 100 分。
3. 新建实施记录和 Handoff，明确 direct authority、串行顺序、禁止自增范围及不激活 cross-record 的边界。
4. agent collaboration、delivery flow、implementation record、governance exam、26/26、总合同、UTF-8、scope、diff、secret 门禁全部通过。
5. 提交并推送候选后，由 APP 总架构独立验收负责人复核；实施者不自行集成。

## R5 direct-principal 一次性职责扩展（2026-07-14）

项目最高负责人基于“24 小时清零”持续授权，针对 cross-record 实现已以 source `3b4bd0c7c78c78be5b592b894e795053f169fa14` 受控集成为 authority `757de99e4dfa4a7467a0de6e1a66d6e030ba7f09`、但 formal reviewer evidence path 缺失这一具体阻塞，明确批准 dispatch 仅执行一次必要的 supporting-item 登记与激活：

- 新增并激活 `AIW-20260714-PLATFORM-EXAM-IR-CROSS-RECORD-INDEPENDENT-ACCEPTANCE`。
- owner 为 `Platform governance independent test agent`，owner_role 为 `平台治理独立测试负责人`，reviewer_role 为 `APP总架构独立验收负责人`。
- allowed scope 仅限 `docs/project-management/independent-acceptance/platform-exam-ir-cross-record-gate/` 下的 `evidence.md`、`task-order.md`、`development-checklist*.json`、`governance-exam*.json`、`implementation-record*.json`。
- 原 cross-record 工作项仅由 `active` 转为 `handoff-ready`，记录 source、integration、next owner 与 handoff 时间；不得把聊天 Go 写成 formal independent acceptance，也不得标为 integrated。
- dispatch 只登记授权；本候选不得写 reviewer namespace、不得实现 validator、不得激活 NOVA 或 Telemetry。

本扩展由项目最高负责人直接事前批准，因此在权限链上高于本任务早期“只更新已登记 planned 项”的自限描述；它只纠正当前 formal reviewer evidence 缺口，不构成一般新增业务项、一般 supporting-item 或一般 allowed-path 扩张权。dispatch 自身 `allowed_paths` 不变。

R5 验收要求：authority 原 124 rows 除 cross-record 与 dispatch freshness/授权说明外逐字段不变；仅追加一个精确 supporting item；两个关联工作树均 clean；R5 current checklist 26/26、随机考试 100、IR/Handoff、全合同、UTF-8、scope、diff、secret 门禁通过；提交推送后交由独立验收，实施者不自行集成。
