# 平台注册表串行派发 R1 Handoff

## 当前结论

`Independent-acceptance supporting-item authorization candidate R5 / Independent acceptance Pending`。

root-of-trust 已受控集成到权威 `edf2133e171bce31a68e2e535f94eac20d04d03b`。R3 候选执行首个受控派发交易：仅将 `AIW-20260713-PLATFORM-EXAM-IR-CROSS-RECORD-GATE-R1` 从 `planned` 激活为 `active` 并绑定 edf exact clean worktree；NOVA overlay 与 Telemetry 保持 `planned`。本候选不实现业务或 validator，不授权部署、生产、真实数据或真实资金。

## 授权链与职责分离

- direct principal / approver：项目最高负责人；当前“24小时项目”会话已明确授权 `/root` 监督并安排各负责人持续推进。
- developer：平台注册表派发授权记录人。
- owner_role：平台集成负责人。
- reviewer：APP 总架构独立验收负责人。
- 串行派发：本 R3 只激活 `AIW-20260713-PLATFORM-EXAM-IR-CROSS-RECORD-GATE-R1`；`AIW-20260713-PLATFORM-NOVA-OVERLAY-R2` 必须保持 planned，直至 cross-record 退出 active/handoff-ready 且另有受控交易。

## R1 证据纠正

R1 checklist 26/26 后使用了非门禁精确 attestation，随后 attempt-1 得分 100。修正 checklist 会使已完成试卷绑定的 hash 失效，因此没有改写或删除试卷。`/root` 作为项目最高负责人授权链监督人明确批准唯一目录 `contracts/foundation/invalidated-snapshots/platform-registry-dispatch-r1/`，仅保存 R1 checklist、attempt-1 原字节与原因 manifest；这不构成一般自扩权。

当前有效证据改为：

- record：`IR-20260714-PLATFORM-REGISTRY-DISPATCH-R1-R2`
- checklist：`FC-20260714-PLATFORM-REGISTRY-DISPATCH-R1-R2`，26/26 current
- exam：`EX-20260714-PLATFORM-REGISTRY-DISPATCH-R1-R2-1`，attempt-1，100 分

## R3 首个派发证据

- authority exact：`edf2133e171bce31a68e2e535f94eac20d04d03b`
- target worktree：`C:/Users/shugo/Documents/worktrees/heaotang-platform-exam-ir-cross-record-gate-r1`
- target branch：`codex/platform-exam-ir-cross-record-gate-r1`
- target initial HEAD：`edf2133e171bce31a68e2e535f94eac20d04d03b`，clean
- 初版 R3 的非锚定补丁误命中同名字段，语义门禁在提交前拒绝；其 checklist/exam 保留为历史快照，不作为 current 授权。
- record：`IR-20260714-PLATFORM-REGISTRY-DISPATCH-R1-R3-R2`
- checklist：`FC-20260714-PLATFORM-REGISTRY-DISPATCH-R1-R3-R2`，26/26 current
- exam：`EX-20260714-PLATFORM-REGISTRY-DISPATCH-R1-R3-R2-1`，attempt-1，100 分
- registry：仅目标 row 的 status、base_commit、updated_at、next_checkpoint、status_expires_at 变化；workspace/branch 原值已与真实工作树一致；其他 rows 逐字段不变。

## R4 安全方案 B：权威基线刷新

- authority exact：`2535a6bf0b59a308dce0e73fd58071be52353ed8`
- dispatch branch：从 `eae160e` 经 `--ff-only` 到 `2535a6bf`，无 reset、无删除、无改动丢失。
- target worktree：`C:/Users/shugo/Documents/worktrees/heaotang-platform-exam-ir-cross-record-gate-r1`
- target branch：`codex/platform-exam-ir-cross-record-gate-r1`，从 `edf2133e` 经 `--ff-only` 到 `2535a6bf`，clean。
- target local registry：cross-record 为 `active`；NOVA overlay 与 Telemetry 均为 `planned`。
- registry-only refresh：cross-record 保持 active，仅 `base_commit` 从 `edf2133e` 更新为 `2535a6bf`，并更新 `updated_at`、`next_checkpoint`、`status_expires_at`；其他 123 rows 必须逐字段不变。
- record：`IR-20260714-PLATFORM-REGISTRY-DISPATCH-R1-R4`
- checklist：`FC-20260714-PLATFORM-REGISTRY-DISPATCH-R1-R4`，26/26 current
- exam：`EX-20260714-PLATFORM-REGISTRY-DISPATCH-R1-R4-1`，attempt-1，100 分
- 禁止项：未实现 validator，未激活 NOVA/Telemetry，未修改业务、部署、生产、真实数据或真实资金路径。

## R5 一次性 formal reviewer supporting-item 授权

- authority：`757de99e4dfa4a7467a0de6e1a66d6e030ba7f09`，受控集成 source `3b4bd0c7c78c78be5b592b894e795053f169fa14`。
- 缺口：authority 中不存在 cross-record formal reviewer evidence path，因此聊天 Go 不能作为 `independent_acceptance`，原工作项不能标为 integrated。
- direct principal：项目最高负责人明确一次性扩展 active dispatch 职责，仅允许登记并激活 `AIW-20260714-PLATFORM-EXAM-IR-CROSS-RECORD-INDEPENDENT-ACCEPTANCE`；不构成一般新增业务项或 supporting-item 权限。
- 原 cross-record：`active` → `handoff-ready`，next owner=`平台治理独立测试负责人`，记录 handoff 时间与 integration commit；不写虚假 independent acceptance。
- reviewer item：owner=`Platform governance independent test agent`，owner_role=`平台治理独立测试负责人`，base=`757de99e`，status=`active`；allowed scope 仅五个 `docs/project-management/independent-acceptance/platform-exam-ir-cross-record-gate/` 证据模式，不含 registry、contracts/foundation、scripts 或 validator。
- reviewer worktree：`C:/Users/shugo/Documents/worktrees/heaotang-platform-exam-ir-cross-record-independent-acceptance`，branch=`codex/platform-exam-ir-cross-record-independent-acceptance`，HEAD=`757de99e`，clean。
- source worktree：`C:/Users/shugo/Documents/worktrees/heaotang-platform-exam-ir-cross-record-gate-r1`，branch=`codex/platform-exam-ir-cross-record-gate-r1`，HEAD=`3b4bd0c7`，clean。
- 本候选 reviewer namespace 零写入；dispatch 只写 registry、自身 task-order、R5 checklist/exam/IR/Handoff。
- NOVA overlay 与 Telemetry 保持 `planned`；未实现 validator，未接触部署、生产、真实数据或真实资金。
- record：`IR-20260714-PLATFORM-REGISTRY-DISPATCH-R1-R5`
- checklist：`FC-20260714-PLATFORM-REGISTRY-DISPATCH-R1-R5`，26/26 current
- exam：`EX-20260714-PLATFORM-REGISTRY-DISPATCH-R1-R5-1`，attempt-1，100 分

## 修改范围

- `contracts/foundation/agent-collaboration.v1.json`
- `docs/project-management/notices/2026-07-14-platform-registry-dispatch-r1-task-order.md`
- `contracts/foundation/development-checklists/2026-07-14-platform-registry-dispatch-r1-r2.json`
- `contracts/foundation/governance-exams/2026-07-14-platform-registry-dispatch-r1-r2-attempt-1.json`
- `contracts/foundation/implementation-records/2026-07-14-platform-registry-dispatch-r1-r2.json`
- `contracts/foundation/invalidated-snapshots/platform-registry-dispatch-r1/`
- `docs/project-management/service-plaza/platform-registry-dispatch-r1-handoff.md`
- `contracts/foundation/development-checklists/2026-07-14-platform-registry-dispatch-r1-r3.json`
- `contracts/foundation/governance-exams/2026-07-14-platform-registry-dispatch-r1-r3-attempt-1.json`
- `contracts/foundation/development-checklists/2026-07-14-platform-registry-dispatch-r1-r3-r2.json`
- `contracts/foundation/governance-exams/2026-07-14-platform-registry-dispatch-r1-r3-r2-attempt-1.json`
- `contracts/foundation/implementation-records/2026-07-14-platform-registry-dispatch-r1-r3-r2.json`
- `contracts/foundation/development-checklists/2026-07-14-platform-registry-dispatch-r1-r4.json`
- `contracts/foundation/governance-exams/2026-07-14-platform-registry-dispatch-r1-r4-attempt-1.json`
- `contracts/foundation/implementation-records/2026-07-14-platform-registry-dispatch-r1-r4.json`
- `contracts/foundation/development-checklists/2026-07-14-platform-registry-dispatch-r1-r5.json`
- `contracts/foundation/governance-exams/2026-07-14-platform-registry-dispatch-r1-r5-attempt-1.json`
- `contracts/foundation/implementation-records/2026-07-14-platform-registry-dispatch-r1-r5.json`

## 停止线

- 禁止自行再增加 allowed paths。
- 禁止同时激活共享路径工作项。
- 本候选只允许激活 cross-record；禁止激活 NOVA 或 Telemetry。
- 独立验收失败或 exact candidate 变化即保持 No-Go。
- 生产、真实数据、真实资金与不可逆操作持续禁止。

## 验证结果

- agent collaboration、delivery-flow、implementation-record、governance-exam、development-checklist validators：通过。
- delivery-flow 永久回归：26/26 通过。
- Service Plaza 总合同：通过。
- UTF-8：1404 文件通过。
- R3-R2 registry 语义审计：authority 124、candidate 124，仅 cross-record row 变化；变化字段严格为 `base_commit`、`next_checkpoint`、`status`、`status_expires_at`、`updated_at`。
- NOVA overlay、Telemetry 与其余 123 rows：逐字段不变；NOVA 与 Telemetry 均保持 `planned`。
- target worktree：HEAD=`edf2133e171bce31a68e2e535f94eac20d04d03b`、branch=`codex/platform-exam-ir-cross-record-gate-r1`、clean。
- scope：仅 dispatch 已授权 registry、R3/R3-R2 checklist/exam/IR 与 Handoff；`git diff --check` 通过；未修改 validator、业务、部署文件。
- R4：preflight ready；agent collaboration、delivery flow、implementation record、governance exam、development checklist validators 全部通过。
- R4：delivery-flow 永久回归 26/26、Service Plaza 总合同通过、UTF-8 1407 files 通过。
- R4：authority/candidate 均为 124 rows，仅 cross-record row 的 `base_commit`、`updated_at`、`next_checkpoint`、`status_expires_at` 变化；status 持续 active，其他 123 rows 逐字段不变。
- R4 target worktree：HEAD=`2535a6bf0b59a308dce0e73fd58071be52353ed8`、branch=`codex/platform-exam-ir-cross-record-gate-r1`、clean；本地 registry 可见 cross-record active。
- R5：preflight ready；agent collaboration、delivery flow、implementation record、governance exam、development checklist validators 全部通过。
- R5：delivery-flow + governance-exam + implementation-record 永久回归共 34 项通过；Service Plaza 总合同通过；UTF-8 1416 files 通过。
- R5 registry：authority 124 rows、candidate 125 rows；仅 cross-record lifecycle/handoff 字段和 dispatch migration/freshness 字段变化，并追加一个精确 independent-acceptance supporting item。
- R5 worktrees：source `3b4bd0c7` 与 reviewer `757de99e` 均 branch 正确、clean；reviewer namespace 候选写入数 0。
- R5 边界：NOVA/Telemetry 逐字段不变且保持 planned；未设置 `independent_acceptance`，未把 cross-record 标为 integrated，未修改 validator、业务或部署。

## 下一步

运行全量门禁、提交并推送 exact R5 supporting-item authorization candidate；由 APP 总架构独立验收负责人给出 Go/No-Go。只有该候选独立 Go 且受控集成后，独立测试负责人才能在 reviewer namespace 内生成自己的 current checklist、考试、IR、task-order 与 formal evidence；dispatch 不代写 reviewer evidence，也不自行集成。
