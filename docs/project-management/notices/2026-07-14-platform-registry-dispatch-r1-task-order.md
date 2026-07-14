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

## R9 Delivery Flow handoff SLA 阻滞清除（2026-07-14）

R8 candidate `6eabd60ba1b33e6608cdc3ded7d735ac18622b47` 被 APP 总架构独立验收负责人 No-Go：其 checklist 绑定修改前 registry hash，且 authority `81f6bc8a7e1bc872f1689099a704768495deb009` 已因 `AIW-20260713-DELIVERY-FLOW-OPTIMIZATION-INDEPENDENT-ACCEPTANCE` first-response SLA 逾期而总合同转红。R8 已以 revert `76f90aaf2abd118c27d8d4264269f09096eae9b4` 完整恢复 authority tree；旧 checklist/exam/IR 保留在 Git 历史，不改写、不作为 current。

项目最高负责人要求 24 小时项目不得因单项阻塞停止其他工作，并授权平台集成负责人持续清除已授权剩余任务。该 handoff 的 `next_owner_role` 已明确为平台集成负责人，因此 R9 只执行最小、真实的 lifecycle closeout：

- business owner：平台交付流负责人；blockage/decision owner：平台集成负责人；verifier：APP 总架构独立验收负责人。
- evidence source `f1db5d43da40bfab33004776a4b903e78f86ec7c` 是 artifact `25b6cd753d2194efa2c0b4faab3dff0357805a93` 的祖先；evidence SHA-256 必须等于已登记 `21bfe6cb4dab21db4072bb5a4335c5f2ff85cd85f8a971cd0deb8265466cbd86`。
- 政策的 `one_business_outcome_one_work_item=true` 与 `supporting_evidence_is_checkpoint=true` 禁止把 evidence bootstrap 变成第二个 integrated 完成实体；否则会产生对验收证据的递归验收。
- 原 supporting item 仅从 `handoff-ready` 转为 `cancelled/superseded`，记录真实迟到的 first response 与 `no-go` decision；禁止回填虚假准时响应，禁止修改主 delivery-flow implementation/acceptance 结论或删除已集成 artifact。
- R9 只改该 supporting item、dispatch freshness、本任务通知、R9 checklist/exam/IR 与 Handoff；不得恢复 R8 的 NOVA supporting-item 变更，不得写 reviewer namespace、validator、业务、部署、生产、真实数据或真实资金路径。
- R9 必须 current checklist 26/26、随机考试 100、全量门禁通过、独立验收 Go 后才允许受控集成。R9 集成后，R8 必须从新的 authority 重新生成 checklist、重新考试和重新验收。

## R10 NOVA Overlay formal reviewer supporting-item 重新授权（2026-07-14）

R9 exact candidate `104a50cbb9e97cc3bab8250a388b0f98ee318a6c` 已由 APP 总架构独立验收负责人 Go，并以双父 no-ff integration `0c420c3448a9e6399410cb6c230b43c243b0471c` 进入 authority。项目最高负责人随后明确要求从该新 authority 重新建立 NOVA Overlay R2 formal reviewer supporting-item 授权候选；旧 R8 `6eabd60ba1b33e6608cdc3ded7d735ac18622b47` 持续 No-Go，其 checklist、exam、IR 均不得复用。

R10 只允许以下原子登记语义：

- `AIW-20260713-PLATFORM-NOVA-OVERLAY-R2` 从 `active` 转为 `handoff-ready`，记录 implementation source `59a988df0d7d1a13ac4dd9ad48da62d5c0340534`、integration `81f6bc8a7e1bc872f1689099a704768495deb009` 及当前 authority 祖先链；不得提前写 `independent_acceptance` 或标为 `integrated`。
- 追加且只追加唯一 `AIW-20260714-PLATFORM-NOVA-OVERLAY-R2-INDEPENDENT-ACCEPTANCE`，状态 `active`，base 为 `0c420c3448a9e6399410cb6c230b43c243b0471c`，owner 为平台治理独立测试负责人，allowed scope 仅 `docs/project-management/independent-acceptance/platform-nova-overlay-r2/` 下五类证据文件。
- dispatch 只刷新本次 direct-principal 授权说明、时间、next checkpoint、expiry 与 blocks；其余 123 个既有 rows 逐字段不变。
- reviewer worktree 必须为 `C:/Users/shugo/Documents/worktrees/heaotang-platform-nova-overlay-r2-independent-acceptance`，branch `codex/platform-nova-overlay-r2-independent-acceptance`，HEAD `0c420c3` 且 clean。

R10 必须新建 current checklist 26/26、随机考试 100、IR/Handoff，并通过 agent collaboration、delivery flow、implementation record、governance exam、development checklist、总合同、UTF-8、scope、diff 与 secret 门禁。dispatch 不得写 reviewer evidence namespace、validator、业务、部署、生产、真实数据或真实资金；候选只提交推送，不自行集成。

## R11 六项生命周期新鲜度原子修复（2026-07-14）

authority `dc8a52a4bcc130c6cdb4da55d5d015cdf501ba16` 在当前时钟运行总合同时精确出现四个 `DELIVERY_STATUS_EXPIRED` 和一个 `DELIVERY_HANDOFF_RESPONSE_SLA_EXCEEDED`。项目最高负责人授权 dispatch 执行一次最小原子 transaction；本 R11 不改变产品、证据内容或既有 integration，只修复真实生命周期登记：

1. `AIW-20260713-ACTIVITY-V3-M0`：`active` → `handoff-ready`，绑定已推送 exact `9d474ee7f340af543bbcb06da1a6b6dd9d00a94b`，转交 APP 总架构独立验收。
2. `AIW-20260713-PROTECTION-MALL-M2-CATALOG-SOLUTION`：`active` → `handoff-ready`，绑定已推送 exact `22073cd8ddeff48a4f679ffcd41a2686d8ea3ba5`；R2 evidence 必须先在自身授权工作项中合法修复并远端固化 exact，再进行完整证据复核。
3. `AIW-20260712-NOVA-PHASE5-M1-RUNTIME`：保持 `active`；只有 NOVA Overlay formal evidence 在 R11 新 authority 下取得 fresh Go，才可执行 TaskRuntime → ToolRuntime synthetic E2E。
4. `AIW-20260712-NOVA-API-CONTRACT-SIGNOFF`：`active` → `handoff-ready`；APP 总架构复核 authority 内 artifact `f5546f25b9b023cb43b9f61c78b837b7e5cb67eb`、五个当前等价 blob 与历史自登记边界。
5. `AIW-20260714-PLATFORM-EXAM-IR-CROSS-RECORD-INDEPENDENT-ACCEPTANCE`：`handoff-ready` → `cancelled/superseded`；保留真实 request `2026-07-14T07:53:56+08:00`，记录真实迟到 response/decision `14:26/14:27` 与 `no-go`。source `efad99b` 是 artifact `dafdd09f` 的祖先，evidence SHA-256=`f8a247a68532f2d198ffea4a8acc0724849099a1832a36282537b01e798c38e9`；主 cross-record integrated item不变。
6. dispatch 只刷新 R11 授权、当前时间、next checkpoint、expiry 与 blocks。

R11 registry candidate 必须仍为 126 rows；changed IDs 精确为上述五项加 dispatch，其他 120 rows 逐字段零变化。registry 内容稳定后才生成全新 `IR-20260714-PLATFORM-REGISTRY-DISPATCH-R1-R11` 的 current checklist、attempt-1、IR 与 Handoff。必须运行 agent collaboration、delivery flow、implementation record、governance exam、development checklist 五个 validator，34 项永久回归、Service Plaza 总合同、UTF-8、diff、scope 和高置信 secret scan；总合同必须 exit 0。候选提交推送后交 APP 总架构独立验收，实施者禁止自行集成。

本 R11 不修改 reviewer evidence namespace、validator、实现、部署、生产、真实数据、真实资金或不可逆路径；任何独立验收失败保持 No-Go，不得绕过或倒填生命周期。

## R11-R2 direct-principal 裁决：保留 legacy 状态并规划显式迁移（2026-07-14）

R11 初稿按原要求把 Activity 与 Mall 两个 candidate 由 `active` 转为 `handoff-ready`；首轮 agent/delivery validator 正确返回 `DELIVERY_LEGACY_EXTERNAL_SNAPSHOT_MISMATCH` 与 `DELIVERY_LEGACY_STATE_CHANGED_WITHOUT_MIGRATION`。只读根因确认：两项分别位于 external snapshot/cutover prefix 的 index 109 与 111，现有 policy 固定前 115 行 `(work_id,status)` 及 `legacy_work_states_sha256`，dispatch 不拥有 policy/validator/snapshot/hash，不能合法迁移。初稿未生成 checklist/exam/IR、未提交、未推送，也未执行第二次盲重试。

项目最高负责人据此直接裁决并授权 R11-R2：

- Activity 与 Mall 完全撤销初稿 status/handoff/next-owner 变化，保持 `active`；仅以真实 transaction 时间刷新 migration note、next checkpoint、blocks、does-not-block、updated/expiry（两小时内），明确 exact candidate ready 但 legacy migration 阻断。
- NOVA Runtime 保持 active freshness refresh；NOVA API 仍转 handoff-ready；cross-record reviewer supporting item仍真实取消/superseded；dispatch freshness按R11-R2刷新。
- registry 末尾只新增一个 `planned / P0` 工作项 `AIW-20260714-PLATFORM-LEGACY-STATE-MIGRATION-R1`。它只规划显式 legacy state migration contract、受控 anchor/hash 演进和永久回归，不在 R11-R2 中激活或实施；禁止直接改 immutable snapshot、豁免 validator 或删除历史。
- 新工作项由 `Platform delivery-flow legacy migration agent` / 平台集成负责人拥有，base=`dc8a52a4bcc130c6cdb4da55d5d015cdf501ba16`，branch=`codex/platform-legacy-state-migration-r1`，workspace=`C:/Users/shugo/Documents/worktrees/heaotang-platform-legacy-state-migration-r1`。仅授权 registry、delivery-flow policy、validator及其测试、总合同入口、ADR0021 和精确 task-order/checklist/exam/IR/Handoff 路径。

R11-R2 registry 稳定后必须生成全新 record `IR-20260714-PLATFORM-REGISTRY-DISPATCH-R1-R11-R2` 的 current checklist、attempt-1、IR 与 Handoff；不复用任何未生成的 R11 证据。五个 validator、34项永久回归、Service Plaza 总合同、UTF-8、diff、scope、secret 与语义审计必须全绿；新增 planned item 若仍被 current policy 拒绝则立即 No-Go。候选只提交推送，实施者禁止自行集成。

### R11-R2-R2 关闭门禁证据重建

R11-R2 first candidate `a8b2563` 在提交后远端回读确认其 checklist 末尾多一个空白行；`git diff --check dc8a52a..a8b2563` 因 `new blank line at EOF` 失败。该提交因此保持 **No-Go**，不得集成。passed exam 绑定原 checklist SHA，禁止直接修改二者；原字节和成绩由不可变 Git commit `a8b2563` 保留，current candidate 从tip移除该三份证据，不改写为通过。

R11-R2-R2 不改变 registry、task scope或业务语义，只重新使用 record `IR-20260714-PLATFORM-REGISTRY-DISPATCH-R1-R11-R2-R2` 完成26/26 current checklist、全新attempt-1=100、IR与Handoff。关闭门禁必须使用相对authority的全范围 `git diff --check dc8a52a..candidate`，不得只检查未提交diff；五validators、34项回归、总合同、UTF-8、scope、secret与remote exact仍必须全绿。候选只提交推送，不自行集成。
