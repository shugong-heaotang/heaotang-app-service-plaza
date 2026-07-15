# 平台注册表 R12-M Legacy Generalization Activation Task Order

- work_id: `AIW-20260715-PLATFORM-REGISTRY-R12M-LEGACY-GENERALIZATION-ACTIVATION`
- record_id: `IR-20260715-PLATFORM-REGISTRY-R12M-LEGACY-GENERALIZATION-ACTIVATION`
- platform identity: `platform scope; module_id=null`
- authority/base: `dbfec2713542c9993508be1d69b12208dcf34edd`
- branch: `codex/platform-registry-r12m-legacy-generalization-activation`
- worktree: `C:/Users/shugo/Documents/worktrees/heaotang-platform-registry-r12m-legacy-generalization-activation`
- developer_role: `平台注册表R12-M实施负责人`
- reviewer: APP总架构独立验收负责人
- approver: 项目最高负责人

## Bootstrap ownership boundary

The authority does not yet contain the R12-M self item; the checkpoint-state command therefore returns `WORK_ITEM_NOT_UNIQUE` before the transaction. The highest project owner explicitly authorizes this one bootstrap transaction to create the unique self item and transfer the registry path from active row131. The self item owns only:

- `contracts/foundation/agent-collaboration.v1.json`
- this task order
- `contracts/foundation/development-checklists/2026-07-15-platform-registry-r12m-legacy-generalization-activation*.json`
- `contracts/foundation/governance-exams/2026-07-15-platform-registry-r12m-legacy-generalization-activation*.json`
- `contracts/foundation/implementation-records/2026-07-15-platform-registry-r12m-legacy-generalization-activation*.json`
- `docs/project-management/service-plaza/platform-registry-r12m-legacy-generalization-activation-handoff.md`

After the registry edit, the checkpoint-state command must resolve exactly one matching self item. A second failure stops the task.

## Atomic registry transaction

1. Row126 `AIW-20260715-PLATFORM-DELIVERY-FLOW-LEGACY-MIGRATION-V2`: `active -> integrated`; bind implementation source `d9822e1a36f5b9c3839feb79f020941a63aa7d66`, file-backed independent Go at `docs/project-management/independent-acceptance/platform-delivery-flow-legacy-v2-r1/evidence.md`, exact evidence bytes SHA, reviewer/reviewed-at, and controlled APP integration `f986734ff27ec3d58ada69a16620ce4e2d5d2f7f`. Release its implementation paths. The Activity/Mall receipt remains `authorized-not-applied` and is not executed.
2. Row135 Batch R2 design: `active -> cancelled`, explicitly superseded by R3 because the design is integrated into authority but remains `draft-not-registered`, non-contract and non-executable. It must not be marked Go or integrated. Release its Batch JSON, exam, implementation-record and Handoff paths; if the shared historical checklist gate requires immutable task-order/checklist provenance, retain only those non-overlapping provenance patterns plus a non-write release tombstone.
3. Add post-cutover active `AIW-20260715-PLATFORM-LEGACY-LIFECYCLE-RECEIPT-GENERALIZATION-R3` from clean base `dbfec271...`. It may generalize schema/validator/policy and upgrade the Batch JSON into a verifiable `authorized-not-applied` receipt, but cannot execute any registry transaction.
4. Keep row131 honestly `active` and remove only `contracts/foundation/agent-collaboration.v1.json` from its paths. Add the unique active R12-M self item owning the registry and fresh R12-M governance paths.
5. Refresh still non-terminal rows 109/111/117/123/130, row134 and any other necessary current-clock row to `2026-07-16T08:00:00+08:00` without changing their business status. Rows132/133 remain `planned`. Legacy rows47/88/89/90/92 retain their current statuses byte-semantically except no authorized field change.

## R3 exact path boundary

R3 may own only:

- `contracts/foundation/delivery-flow-policy.v3.json`
- `contracts/foundation/delivery-flow-policy.v3.schema.json`
- `contracts/foundation/legacy-lifecycle-migration.v2.schema.json`
- `contracts/foundation/legacy-lifecycle-migrations/LLM-20260715-TECHNICAL-SOCIAL-BATCH-R2.json`
- `scripts/validate_delivery_flow_policy.py`
- `scripts/tests/test_validate_delivery_flow_policy.py`
- `scripts/Test-ServicePlazaContracts.ps1`
- `docs/project-management/notices/2026-07-15-platform-legacy-lifecycle-receipt-generalization-r3-task-order.md`
- `contracts/foundation/development-checklists/2026-07-15-platform-legacy-lifecycle-receipt-generalization-r3*.json`
- `contracts/foundation/governance-exams/2026-07-15-platform-legacy-lifecycle-receipt-generalization-r3*.json`
- `contracts/foundation/implementation-records/2026-07-15-platform-legacy-lifecycle-receipt-generalization-r3*.json`
- `docs/project-management/service-plaza/platform-legacy-lifecycle-receipt-generalization-r3-handoff.md`

Rows126 and 135 release their paths before R3 becomes active, so no active path overlap is permitted.

## Non-goals and stop conditions

- Do not modify or apply the Activity/Mall receipt.
- Do not modify business implementation, production, real data or funds.
- Do not activate Social rows132/133 or change statuses 47/88/89/90/92.
- Do not mark the Batch R2 design integrated or authorized.
- Do not push, self-review or integrate the candidate.
- Stop on path overlap, evidence bytes/commit mismatch, identity mismatch, repeated gate failure or any partial registry transaction.
