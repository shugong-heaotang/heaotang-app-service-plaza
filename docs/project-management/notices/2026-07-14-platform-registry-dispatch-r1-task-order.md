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

## R12-B lifecycle deadlock repair（2026-07-15）

项目最高负责人从已获独立技术 Go 的 test-repair exact
`73b64b03627f37cd34f5bbbad1802fa08a20dd1f` 直接授权 R12-B。R12-B
沿用 work_id `AIW-20260714-PLATFORM-REGISTRY-DISPATCH-R1`，工作树改为
`heaotang-platform-registry-dispatch-r12b`，分支改为
`codex/platform-registry-dispatch-r12b`。本次只允许 registry、现有 task-order、
现有 Handoff 及 R12-B 新 checklist/exam/IR 六类路径；不得修改 test、validator、
policy、业务或 reviewer evidence，不得推送、集成、自行验收或接触生产、真实数据、
资金。

R12-B 原子 registry 语义：

- 以真实当前时间刷新 Activity、Mall Catalog Solution、NOVA Runtime、NOVA API、
  NOVA Overlay、dispatch 与 NOVA reviewer 的监督窗口；NOVA API 只转
  `handoff-ready`，不标记 integrated。
- 对 cross-record duplicate reviewer checkpoint 记录真实迟到 first response 和
  `no-go/superseded` decision，不回填虚假及时响应，不修改主 integrated outcome。
- Telemetry R2 保持 `planned`，刷新真实监督时间和激活条件，并明确记录 delivery-flow
  v1 不报告 planned 过期的监督盲点；本候选不修改 validator，也不激活 Telemetry。
- 新增 `AIW-20260715-PLATFORM-DELIVERY-FLOW-LEGACY-MIGRATION-V2` 与
  `AIW-20260715-PLATFORM-ACTIVITY-MALL-M2-LEGACY-TRANSITION-R1`，两者只能
  `planned`。其 `base_commit` 只记录当前 authority `73b64b0`；未知的 R12-B
  双提交链 integration SHA 不得伪造，必须在未来激活前刷新。
- Legacy Migration V2 必须产出 fixed receipt，并保持 anchor、path、cutover、hash
  不漂移；它阻塞 atomic transition。
- Atomic transition 只有在 A integration、fixed receipt、Mall Catalog Solution 与
  Evidence 双 formal Go、相关 exact worktree clean 后才可激活。未来事务必须一次完成
  五行切换：Activity `active -> handoff-ready`，Catalog Solution/Evidence
  `active -> integrated`，Order/Ports `planned -> active`。transition hash 固定为
  `5dfa87a441a04eb8a24e3a4de883648780b6eaeddf2c870d831fa6ed29620939`，
  post effective-state hash 固定为
  `7f1991952dea49dff84e6378dbdc4edd22f4bf72334e0a8c08a36474fb984ec6`；
  R12-B 不执行该事务。

为避免 registry 输出使入口 checklist 自失效，R12-B 必须形成双提交链：第一提交固定
registry transaction 与入口治理证据；第二提交从第一 exact 重新全文读取并形成 final
current checklist、exam100、IR/Handoff。任一提交独立验收失败，整条链保持 No-Go。

## R12-D direct-principal registry activation（2026-07-15）

R12-B 双提交链已由独立验收 Go 并受控集成为 authority
`e7c5b61b9905e11f1be3267ea1544610a3cd064f`。后续 R12-C 候选因删除或改写已通过的
governance exam 证据而被判定 No-Go，且权威 registry 仍指向旧 `r12b` 工作树。项目最高负责人因此直接授权
R12-D 以同一 work_id 执行一次最小 registry activation transaction；该授权只修复所有权接续与并行派发，
不追认 R12-C，也不允许复用、删除或改写其通过后证据。

R12-D 必须采用严格两阶段不可变证据：

1. 先从 `e7c5b61` 生成并保留 entry record
   `IR-20260715-PLATFORM-REGISTRY-DISPATCH-R1-R12D` 的全新 checklist 和 governance exam；
   任何 failed/passed attempt 均永久保留，不得删除或改写。
2. registry transaction 与本 task-order 进入 commit-1；Legacy Migration V2 与
   Activity/Mall Legacy Transition 只保持 `planned` 并刷新 base 到 `e7c5b61`。
3. commit-1 只激活三个 clean、互不重叠工作面：existing Telemetry R2 Acceptance、
   new Network Read Provider Evidence R2、new Health R0 F2 Audit F2-1。Telemetry 必须移除 registry
   allowed path；Network 只读绑定 backend `f6ba650c`；Health 必须保持
   `synthetic_only=true`、`executable=false`。
4. 基于 commit-1 重新全文读取并生成 final record
   `IR-20260715-PLATFORM-REGISTRY-DISPATCH-R1-R12D-R2` 的全新 checklist、exam100、IR 和 Handoff，
   进入 commit-2。entry 证据不得因 final 证据出现而失效、删除或被改写。

R12-D 仅允许六类 dispatch 路径：registry、现有 task-order、现有 dispatch Handoff、R12-D checklist、
R12-D governance exam、R12-D implementation record。禁止修改 validator、policy、test、业务或 reviewer
evidence；禁止新增 Social/Club 工作项；禁止推送、自验收或自行集成。Social 与 Club 只在 Handoff
中列为下一轮 dispatch。任一提交独立验收失败，整条两提交链保持 No-Go。
