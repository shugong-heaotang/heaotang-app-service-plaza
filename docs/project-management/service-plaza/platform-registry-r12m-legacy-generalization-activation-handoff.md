# Platform Registry R12-M Legacy Generalization Activation Handoff

- work_id: `AIW-20260715-PLATFORM-REGISTRY-R12M-LEGACY-GENERALIZATION-ACTIVATION`
- record_id: `IR-20260715-PLATFORM-REGISTRY-R12M-LEGACY-GENERALIZATION-ACTIVATION`
- base: `dbfec2713542c9993508be1d69b12208dcf34edd`
- developer: 平台注册表R12-M实施负责人
- reviewer: APP总架构独立验收负责人
- state: `ready for independent review`

## Atomic result

1. Row126 Legacy V2 mechanism is projected `active -> integrated`. Source `d9822e1a36f5b9c3839feb79f020941a63aa7d66` is bound to independent reviewer role `平台治理独立测试负责人`, reviewed-at `2026-07-15T19:37:22+08:00`, evidence path `docs/project-management/independent-acceptance/platform-delivery-flow-legacy-v2-r1/evidence.md`, bytes SHA `f565074b0ce0a584a13307946a7fb65a127ec3fc4d8d1330a068a853b90e185b`, and controlled APP integration `f986734ff27ec3d58ada69a16620ce4e2d5d2f7f`.
2. `LLM-20260715-ACTIVITY-MALL-M2-R1` remains byte-identical, `authorized-not-applied`, `applied=false`, with no five-row status transition. Row126 terminalization accepts the mechanism only.
3. Row135 Batch R2 is projected `active -> cancelled`, reason `superseded-by-new-R3`. Exact `df619ff41b39ccbb2a3d19db2d4a7632a4d28901` is preserved in authority but remains `draft-not-registered`, non-contract and non-executable. It is not classified Go or integrated.
4. Row131 remains honestly active over its five immutable governance paths and releases only `contracts/foundation/agent-collaboration.v1.json`. The new unique R12-M self item owns the registry and five fresh R12-M evidence paths.
5. New post-cutover `AIW-20260715-PLATFORM-LEGACY-LIFECYCLE-RECEIPT-GENERALIZATION-R3` is active from a clean `dbfec271...` worktree. It may generalize policy/schema/validator and upgrade the Batch JSON into a verifiable `authorized-not-applied` receipt, but cannot execute a registry transaction.

The current registry schema requires `allowed_paths` to contain at least one string, and the shared checklist regression requires each post-cutoff checklist to remain attributable to its historical task order and checklist pattern. Rows126 and 135 therefore release all implementation, receipt-upgrade, validator, exam, IR and Handoff paths; they retain only unique `__released_no_write__/...` tombstones plus immutable task-order/checklist provenance patterns. None overlap R3 or grant new write authority.

## Preserved states and timing

- Rows47/88/89/90/92 are byte-semantically unchanged.
- Rows132 and 133 remain `planned`; no Social write authorization exists.
- Rows112/113/114 remain unchanged; the Activity/Mall transaction is not partially or completely applied.
- Rows109/111/117/123/130 remain in their existing business states and are refreshed through `2026-07-16T08:00:00+08:00`.
- Rows131 and 134 remain active and are current through the same supervision boundary.

## Isolation

R3 owns only the new policy v3/schema v3/migration schema v2 paths, the existing Batch R2 JSON upgrade path, the minimum Delivery Flow validator/test/aggregate files and fresh R3 governance paths. Rows126 and 135 release all original overlapping paths before R3 activation. The registry validator must prove no active workspace or path overlap.

## Governance and gates

- global preflight: ready;
- initial checkpoint state before self registration: one expected `WORK_ITEM_NOT_UNIQUE`, file-backed as the authorized bootstrap boundary;
- checklist: 26/26 completed; after authorized mechanical normalization it is UTF-8 without BOM and LF-only;
- exam attempt 1: 100;
- post-edit checkpoint state: exactly one R12-M self item, correct branch/base/worktree, next gate `implement-test-and-record` before this IR/Handoff;
- registry atomic invariants, evidence-at-commit SHA, Git ancestry, no-overlap, Delivery Flow, total contracts, encoding, scope, secret and diff gates are required before exact candidate handoff.

The developer stops after committing the six authorized paths. No push, self-review, integration, receipt execution, deployment, production, real-data or funds access is authorized.
