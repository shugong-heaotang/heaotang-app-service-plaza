# Platform Legacy Lifecycle Receipt Generalization R3 Handoff

- work_id: `AIW-20260715-PLATFORM-LEGACY-LIFECYCLE-RECEIPT-GENERALIZATION-R3`
- record_id: `IR-20260715-PLATFORM-LEGACY-LIFECYCLE-RECEIPT-GENERALIZATION-R3`
- registered base: `dbfec2713542c9993508be1d69b12208dcf34edd`
- implementation authority: `d079e98ee1a4954bceb6c01eedce71371c187bd8`
- developer: 平台 Legacy 收据通用化 R3 实施负责人
- reviewer: 平台治理独立测试负责人
- state: `ready for independent review`

## Implemented result

Delivery Flow policy v3 now registers multiple lifecycle receipts by exact id, version, schema path, receipt path and receipt SHA256. The existing Activity/Mall v1 registration remains bound to its unchanged v1 schema and bytes. Batch R2 is registered through the new v2 schema and is explicitly `authorized-not-applied`; it remains `execution_enabled=false`, `applied=false`, `post_registry_sha256=null`, `review=null` and `integration=null`.

The validator dispatches by registered receipt version and rejects unknown versions, duplicate registrations, arbitrary receipt substitution, path escape, hash or schema mismatch and cross-receipt row overlap. The v1 handler remains compatible with policy v2. The v2 handler independently recomputes source/current `commit:path` bytes, current registry drift, canonical row and state hashes, audit partition, omitted rows, atomic groups, evidence bytes, acceptance/integration ancestry and cross-repository blob equality.

## Evidence interpretation correction

The earlier Batch design named `5cf87e...` and `5c48677...` as accepted evidence commits, but each implementation Handoff explicitly stopped before final independent Go. R3 does not promote those implementer-authored files into acceptance. It binds them only as `acceptance_subject_commit` and proves formal Go through current registry acceptance rows121/128, reviewer role, reviewed-at, exact subject commit, evidence path/SHA, integration commit and the final evidence bytes at `86d68db24268592418ea94b43d2580a89f11f488`.

## Atomic and omitted scope

The declared audit scope contains exactly indices 47, 88, 89, 90, 92 and 132. Transitions contain 47, 88, 89, 90 and 132; omitted rows contain only 92. The validator requires these sets to form an exact partition. Indices90 and132 are declared as the same `social-owner-switch-90-132` group and must be present together in canonical order. Row92 has no file-backed independent Go and cannot authorize a transition.

## Verification

- fresh governance checklist: 26/26 completed;
- governance exam attempt 1: 100;
- Delivery Flow focused suite: 35/35 passed;
- direct policy v3 validation: passed;
- Service Plaza aggregate gate: passed, including 50 tests;
- policy and receipt schemas: Draft 2020-12 valid; both instances pass;
- policy v2, schema v2, v1 schema and Activity receipt: byte-identical to `d079e98...`;
- `Test-ServicePlazaContracts.ps1`: UTF-8 BOM, CRLF-only and parse-valid;
- JSON/Markdown: UTF-8 without BOM, LF-only and one terminal LF;
- diff check: passed.

The first focused run had one controlled test failure: arbitrary v1-to-v2 receipt substitution raised a `TypeError` after schema/registration rejection because non-v2 indices were still sorted. The validator now fail-closes immediately on non-integer indices. The exact test passed, followed by the full 35/35 run; no same-gate second failure occurred.

## No-transaction boundary

No registry status is changed. No receipt is applied, partially projected or marked reviewed/integrated. Social rows132/133 remain planned. The developer will commit only the 12 authorized paths and stop. Push, self-review, self-integration, deployment, production, real-data and funds access remain prohibited.

## R3.1 live-registry compatibility addendum

R3 exact `381039fe4d971fc97c2aa85cef3cf4b2aa0bb5ee` was controlled-integrated as authority `06047119c12384498af78f5feab2425c6136ea52`. The existing row136 owner fast-forwarded from its clean exact candidate only to that authority before starting R3.1. The immutable task order, original R3 checklist and exam, policy v3, both policy schemas, both lifecycle schemas, both receipts and the collaboration registry remain unchanged.

R3.1 removes one structural deadlock in the v2 receipt handler. `current_registry_precondition` still means exact historical Git evidence: the validator reads `git show <commit>:<path>`, verifies its SHA256 and parses those bytes. It no longer requires the entire evolving live registry file to be byte-identical to that historical object.

The replacement live-registry gate is deliberately narrow:

- the live registry must contain at least the complete historical prefix;
- every historical index must retain the same non-empty `work_id`, so insertion, deletion, reorder or replacement fails closed;
- every live `work_id`, including appended rows, must remain unique;
- audit indices 47, 88, 89, 90, 92 and 132 must retain complete canonical row hashes from the receipt precondition;
- all existing transition, partial/mixed, audit partition, omitted row92, 90/132 atomic, evidence, review and blob-equivalence gates remain active;
- fields outside those six audit rows and unique tail appends are not frozen here; existing agent-collaboration and Delivery Flow contracts continue to govern them.

The positive regression explicitly changes row136 status and released paths, changes row137 Handoff state and appends three unique governance rows. The receipt handler accepts that shape. Negative cases reject any field drift on each audit row, historical insertion/deletion/reorder/work-id replacement, duplicate append and precondition commit/path/SHA substitution. Focused Delivery Flow regression is 39/39, including all original 35 R3 tests. R3.1 does not apply the Batch receipt or mutate any real registry or business state.
