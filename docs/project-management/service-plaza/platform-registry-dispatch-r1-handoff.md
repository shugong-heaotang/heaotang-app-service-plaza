# 平台注册表串行派发 R1 Handoff

## 当前结论

`Implementation candidate / Independent acceptance Pending`。

exact base `384304a87e2a6965dc6cb3cdcafd2a92eef7d101` 的原 123 个 registry rows 保持逐字段不变；候选只新增 `AIW-20260714-PLATFORM-REGISTRY-DISPATCH-R1`，使平台注册表恢复一个唯一 `active` owner。该候选不激活 cross-record，不激活 NOVA overlay，不授权业务、validator、部署、生产、真实数据或真实资金。

## 授权链与职责分离

- direct principal / approver：项目最高负责人；当前“24小时项目”会话已明确授权 `/root` 监督并安排各负责人持续推进。
- developer：平台注册表派发授权记录人。
- owner_role：平台集成负责人。
- reviewer：APP 总架构独立验收负责人。
- 后续串行目标：先 `AIW-20260713-PLATFORM-EXAM-IR-CROSS-RECORD-GATE-R1`，后 `AIW-20260713-PLATFORM-NOVA-OVERLAY-R2`；本候选本身不执行激活。

## R1 证据纠正

R1 checklist 26/26 后使用了非门禁精确 attestation，随后 attempt-1 得分 100。修正 checklist 会使已完成试卷绑定的 hash 失效，因此没有改写或删除试卷。`/root` 作为项目最高负责人授权链监督人明确批准唯一目录 `contracts/foundation/invalidated-snapshots/platform-registry-dispatch-r1/`，仅保存 R1 checklist、attempt-1 原字节与原因 manifest；这不构成一般自扩权。

当前有效证据改为：

- record：`IR-20260714-PLATFORM-REGISTRY-DISPATCH-R1-R2`
- checklist：`FC-20260714-PLATFORM-REGISTRY-DISPATCH-R1-R2`，26/26 current
- exam：`EX-20260714-PLATFORM-REGISTRY-DISPATCH-R1-R2-1`，attempt-1，100 分

## 修改范围

- `contracts/foundation/agent-collaboration.v1.json`
- `docs/project-management/notices/2026-07-14-platform-registry-dispatch-r1-task-order.md`
- `contracts/foundation/development-checklists/2026-07-14-platform-registry-dispatch-r1-r2.json`
- `contracts/foundation/governance-exams/2026-07-14-platform-registry-dispatch-r1-r2-attempt-1.json`
- `contracts/foundation/implementation-records/2026-07-14-platform-registry-dispatch-r1-r2.json`
- `contracts/foundation/invalidated-snapshots/platform-registry-dispatch-r1/`
- `docs/project-management/service-plaza/platform-registry-dispatch-r1-handoff.md`

## 停止线

- 禁止自行再增加 allowed paths。
- 禁止同时激活共享路径工作项。
- 禁止本候选激活 cross-record 或 NOVA。
- 独立验收失败或 exact candidate 变化即保持 No-Go。
- 生产、真实数据、真实资金与不可逆操作持续禁止。

## 验证结果

- agent collaboration、delivery-flow、implementation-record、governance-exam、development-checklist validators：通过。
- delivery-flow 永久回归：26/26 通过。
- Service Plaza 总合同：通过。
- UTF-8：1399 文件通过。
- registry 语义审计：base 123、current 124、原 123 rows 变化数 0。
- scope：7 个授权路径组，越权 0；`git diff --check` 通过；secret suspects 0。

## 下一步

运行全量门禁、提交并推送 exact candidate；由 APP 总架构独立验收负责人给出 Go/No-Go。只有独立 Go 且受控集成后，平台集成负责人才能另建后续状态交易，先激活 cross-record。
