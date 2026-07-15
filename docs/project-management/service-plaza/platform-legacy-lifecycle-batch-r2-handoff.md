# Platform Legacy Lifecycle Batch R2 Handoff

- work_id: `AIW-20260715-PLATFORM-LEGACY-LIFECYCLE-BATCH-R2`
- record_id: `IR-20260715-PLATFORM-LEGACY-LIFECYCLE-BATCH-R2`
- developer: 平台Legacy批次R2实施负责人
- reviewer: 平台治理独立测试负责人
- state: `draft-not-registered; independent review required`

## Outcome

The candidate does **not** create an `authorized-not-applied` receipt. The only new JSON is a fixed non-contract transaction design with `executable=false`, `authorization=null`, `applied=false`, `post_registry_sha256=null`, `review=null` and `integration=null`. No registry status, validator, policy, old receipt or Activity/Mall transaction changed.

The downgrade is required because `legacy-lifecycle-migration.v1.schema.json` is fixed to the Activity/Mall R1 receipt id, exactly five old transitions, legacy indices at most 114 and fixed transition/state hashes. It cannot lawfully validate a batch containing row132, and this work item has no authority to change it. A total gate that ignores the new JSON is not evidence that the design is a valid contract.

## Authorized implementation-base chain

Row135 was registered at `d7d57bdb2f9b7fc90038d92a522e56393de1f22a`. R12-L candidate `8f8f2f6e90ec11610ff73562979c64c3acbaabfe` was controlled-integrated as `05bbf6465edecaa97af5d82792db868ece4f42e8`. The highest project owner then explicitly authorized an `ff-only` update of this worktree to `05bbf646...` so the implementation could read its own active registry row. After the fast-forward, branch `codex/platform-legacy-lifecycle-batch-r2` and the clean worktree were confirmed. Source/current registry provenance is therefore exact `05bbf646...`, bytes SHA `1b880e0e46c5875163798183adf6661bcaaa09a4d3e7dfe6cec66ca7d9523c04`.

## Future projection in the design

| Index | Work item | Projection | Evidence boundary |
|---:|---|---|---|
| 47 | Action Telemetry BusinessConfig backend | `active -> integrated` | source `a0b21cf`; all five authorized blobs equal backend authority `091c9be9`; fresh acceptance `5cf87e27`; APP integration `a1ac334f` |
| 88 | Network read provider backend | `active -> integrated` | source `f6ba650c`; both authorized blobs equal backend authority `091c9be9`; fresh acceptance `5c48677c`; APP integration `610ba656` |
| 89 | old Network evidence | `active -> cancelled` | old `5eb27542` is whole-candidate No-Go due to unauthorized registry diff; replacement row128 is independently accepted and integrated |
| 90 | old Social backend | `active -> cancelled` | old `70fb18b8` is not a backend-authority ancestor; cancellation is inseparable from row132 activation |
| 132 | Social backend R2 | `planned -> active` | clean reserved child from backend base `091c9be9`; same atomic group as row90 |

The shared final dispatch Handoff bytes SHA `2de166bf142061106b9ea295141901c538a8f4999d092ba0b445d0cbd513c661` are bound to evidence-finalization commit `86d68db24268592418ea94b43d2580a89f11f488`. Network APP integration remains `610ba65680123758a53badde0fa8dc0cf52e7f20`; those commits have different roles and are not interchangeable.

Rows 47 and 88 are design projections, not developer-issued Go. Their future `integrated` transitions are legal only if the generalized validator independently rechecks every named Git blob, the file-backed acceptance and controlled APP integration. Commit ancestry alone is insufficient because the source commits are not ancestors of backend authority even though their authorized path blobs are equal.

## Excluded row

Row92 (`AIW-20260712-NOVA-M2-MIGRATION-DISABLE-DRILL`) is omitted. Its current Handoff says `ready for independent review` and explicitly asks the platform to perform that review. The implementation record says implementation evidence does not replace independent acceptance. No file-backed independent Go was found, so any terminal projection would be fabricated.

## Minimum follow-up before any executable receipt

An independently authorized work item must generalize and register schema, validator and policy handling while preserving the current Activity/Mall receipt unchanged. At minimum it must:

1. bind source and current registry commit, bytes SHA, work identity, status and canonical row SHA;
2. verify Git objects and exact allowed-path blob equivalence for row47 and row88, plus fresh independent acceptance and controlled APP integration;
3. enforce row90/132 as a single atomic group and reject partial before/after states;
4. reject registry drift, evidence SHA drift, missing Git objects, reordered/duplicate transitions, projected-state hash mismatch and any unregistered state;
5. reject row92 until a file-backed independent Go path/SHA/reviewer/reviewed-at set exists;
6. require a new independent review of the exact generalized-contract candidate before authorization or execution.

## Governance and verification

- current checklist: 26/26 completed;
- governance exam attempt 1: 100;
- registry remains unchanged at source authority;
- draft JSON parses and its canonical row/state/transition/projected-state hashes are reproducible;
- existing schema incompatibility is an explicit No-Go boundary, not a hidden test omission;
- the Activity/Mall-only schema rejects the draft with 23 expected validation errors; no schema-pass claim is made;
- six negative mutations were rejected: false authorization state, partial Social atomic group, row-hash drift, transition-hash drift, evidence-hash drift and the incorrect `610ba656 + 2de166bf` commit/bytes pairing;
- focused checklist/exam/IR validators, total Service Plaza contracts with 41 regression tests, UTF-8 over 1546 files, six-file scope, high-confidence secret scan and `git diff --check` passed;
- review, authorization, integration and execution remain pending.

The developer stops at this Handoff and does not push, independently accept, register, authorize, integrate or execute the design.

## Root-cause closeout: evidence bytes bound to the wrong commit

- pattern_id: `RC-20260715-BATCH-R2-EVIDENCE-COMMIT-BYTES`
- first_seen / recurrence_count: first occurrence / 1
- affected_checkpoint: independent review of candidate `53e1b7ae2a771b79d9cc82f6eea517626dc7ad21`
- symptom and exact stop: the draft paired dispatch Handoff SHA `2de166bf...` with authority commit `610ba656...`; independent review returned No-Go.
- reproduction: `git show 610ba656:docs/project-management/service-plaza/platform-registry-dispatch-r1-handoff.md` hashes to `2ebc6a2a657ab7f9102465c0aae38ffb47e705fbdaf493043537086dfeaea67e` and blob `e33f5ff2...`, while the same path at `86d68db` hashes to `2de166bf...` and blob `f7093d3d...`.
- causal chain: because evidence was hashed from current authority but its `authority_commit` was copied from the Network integration field, therefore bytes from a later final Handoff were attributed to an earlier Git object; because the initial positive check verified only the current file SHA and commit existence, therefore it did not prove `sha256(git show authority_commit:path)` equality. The earliest controllable cause is the missing commit-scoped bytes check.
- impact: the draft provenance claim was invalid and blocked independent acceptance; registry, projected statuses, backend blobs, production, real data, funds and the Activity/Mall receipt were unaffected.
- rejected workaround: changing the SHA to the older `610ba656` bytes would discard final R12-G evidence and obscure the source used by current registry independent acceptance.
- systemic fix: retain business integration `610ba656`, bind the final evidence file to exact `86d68db`, and distinguish `app_integration_commit` from `final_evidence_commit` in each affected projection basis.
- prevention gate: every evidence entry must prove path existence and byte SHA at its declared authority commit, not merely against the current worktree; a mutation back to `610ba656 + 2de166bf` must fail.
- blocks: independent acceptance of the amended candidate.
- does_not_block: unrelated isolated work, existing registry authority, backend implementation evidence and old Activity/Mall receipt.
- verdict: fixed locally, pending independent review of the amended exact; no authorization or execution is implied.
