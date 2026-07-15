# 平台注册表 R12-N-R2 Legacy Application Activation Task Order

- work_id: `AIW-20260715-PLATFORM-REGISTRY-R12N-R2-APPLICATION-ACTIVATION`
- record_id: `IR-20260715-PLATFORM-REGISTRY-R12N-R2-APPLICATION-ACTIVATION`
- platform identity: `platform scope; module_id=null`
- authority/base: `9f79d06d502bf11ad0bb7f6dc74c80c0175f01d3`
- branch: `codex/platform-registry-r12n-r2-application-activation`
- worktree: `C:/Users/shugo/Documents/worktrees/heaotang-platform-registry-r12n-r2-application-activation`
- developer_role: `平台注册表R12-N-R2实施负责人`
- reviewer: APP总架构独立验收负责人
- approver: 项目最高负责人

## Bootstrap ownership and R3.1 prerequisite

Authority-state row137 owns `contracts/foundation/agent-collaboration.v1.json` and the highest project owner authorizes this one R12-N-R2 candidate. The authority does not yet contain the R12-N-R2 self item. After the transaction, R12-N-R2 owns only its five fresh governance paths and R12-O becomes the unique registry owner; R12-N-R2 does not retain the registry after controlled integration.

The frozen first R12-N diagnostic worktree proved that v3 rejected the same governance-only registry evolution with `DELIVERY_LEGACY_CURRENT_REGISTRY_DRIFT`. Authority `9f79d06d502bf11ad0bb7f6dc74c80c0175f01d3` contains the independently accepted and controlled-integrated R3.1 validator. R12-N-R2 must reproduce the old v3 failure against the frozen semantic diff, prove the same semantic diff passes under R3.1, and prove complete canonical equality for audit rows47/88/89/90/92/132 before candidate handoff.

## Atomic activation transaction

1. Row136 R3 changes `active -> cancelled` as `superseded-by-R4`. Exact R3 implementation `381039fe4d971fc97c2aa85cef3cf4b2aa0bb5ee` is preserved in authority. This row is not marked `integrated`; all twelve implementation paths are released, while only a non-write tombstone and immutable task-order/checklist provenance remain.
2. Row137 R12-M remains `active`, preserves its five immutable governance paths, releases only the registry and records the truthful R12-N-R2 handoff.
3. Add active `AIW-20260715-PLATFORM-LEGACY-LIFECYCLE-APPLICATION-R4` from clean authority `9f79d06...`, with exactly twelve paths: policy v4/schema, application-record schema/new JSON, validator/focused tests/aggregate PowerShell, and five fresh R4 governance paths. R4 may create an independent content-addressed application/review/post-state mechanism, but cannot modify a registered receipt or execute a registry transaction.
4. Add active R12-N-R2 self owning only its five fresh governance paths.
5. Add active `AIW-20260715-PLATFORM-LEGACY-LIFECYCLE-REGISTRY-TRANSACTION-R12O` from clean authority `9f79d06...`. R12-O owns the registry plus five fresh governance paths and remains explicit No-Write until R4 content-addressed intent and policy are independently accepted and controlled-integrated, followed by separate authorization.
6. Every other existing row is byte-semantically unchanged. In particular audit rows47/88/89/90/92/132, row133 and Activity/Mall rows109/111/112/113/114 do not change. Both registered receipt files remain byte-identical and unapplied.

## R4 exact twelve-path boundary

- `contracts/foundation/delivery-flow-policy.v4.json`
- `contracts/foundation/delivery-flow-policy.v4.schema.json`
- `contracts/foundation/legacy-lifecycle-application.v1.schema.json`
- `contracts/foundation/legacy-lifecycle-applications/LLA-20260715-TECHNICAL-SOCIAL-BATCH-R2.json`
- `scripts/validate_delivery_flow_policy.py`
- `scripts/tests/test_validate_delivery_flow_policy.py`
- `scripts/Test-ServicePlazaContracts.ps1`
- `docs/project-management/notices/2026-07-15-platform-legacy-lifecycle-application-r4-task-order.md`
- `contracts/foundation/development-checklists/2026-07-15-platform-legacy-lifecycle-application-r4*.json`
- `contracts/foundation/governance-exams/2026-07-15-platform-legacy-lifecycle-application-r4*.json`
- `contracts/foundation/implementation-records/2026-07-15-platform-legacy-lifecycle-application-r4*.json`
- `docs/project-management/service-plaza/platform-legacy-lifecycle-application-r4-handoff.md`

## Stop boundary

- Do not modify either registered receipt or any audit row.
- Do not execute a receipt, application, registry status projection or Social activation.
- Do not begin R12-O writes before R4 content-addressed intent and policy controlled integration plus separate authorization.
- Do not modify business implementation, deploy, access production, real data or funds.
- Do not push, self-review or self-integrate.
- Stop after a second same-gate failure, identity mismatch, path overlap, protected-byte drift or partial registry transaction.
