# Legacy Delivery Flow V2 Independent Acceptance R1 Evidence

## Verdict

**Go.** Source `d9822e1a36f5b9c3839feb79f020941a63aa7d66` implements a versioned, fixed-SHA and fail-closed Legacy V2 receipt mechanism. The implementation is preserved byte-for-byte in controlled integration `92ce89eab132ef5326f49de3fa3e619f1b949fb2` and activation authority `05bbf6465edecaa97af5d82792db868ece4f42e8`.

This verdict accepts the mechanism and its current `authorized-not-applied` receipt only. It does not apply the receipt, change any collaboration-registry lifecycle, authorize a partial or complete Activity/Mall five-row transaction, or make row 126 integrated.

## Exact review identity

| Item | Exact value |
|---|---|
| Work item | `AIW-20260715-PLATFORM-DELIVERY-FLOW-LEGACY-V2-INDEPENDENT-ACCEPTANCE-R1` |
| Review record | `IR-20260715-PLATFORM-DELIVERY-FLOW-LEGACY-V2-INDEPENDENT-ACCEPTANCE-R1` |
| Registered base | `d7d57bdb2f9b7fc90038d92a522e56393de1f22a` |
| Activation authority | `05bbf6465edecaa97af5d82792db868ece4f42e8` |
| Reviewed implementation base | `8776166a52249c673ecaa24b4cd6b0522f4aba59` |
| Reviewed source | `d9822e1a36f5b9c3839feb79f020941a63aa7d66` |
| Controlled integration | `92ce89eab132ef5326f49de3fa3e619f1b949fb2` |
| Authority registry SHA-256 | `1b880e0e46c5875163798183adf6661bcaaa09a4d3e7dfe6cec66ca7d9523c04` |
| Review checklist SHA-256 | `4a712e0bb6a779784009e2d23e727a5081e9881f76fd280dd9b79e7cb10efac1` |
| Review exam SHA-256 | `658a493283399368f64b3fe925bc99b917db46c9dca844051404d7f525d724ff` |

Source is an ancestor of integration, and integration is an ancestor of activation authority. Source has exactly 14 changed files relative to `8776166`; all 14 match row 126's registered implementation scope, all 14 source blobs match both integration and authority, and the collaboration registry is byte-for-byte unchanged between `8776166` and source.

## Fresh governance evidence

- Current reviewer checklist: 26/26, `completed`, `module_id=null`, all source SHA-256 values current.
- Governance exam attempt 1: 100, `passed`, same record ID and current checklist.
- Reviewer namespace contains only the five authorized files: task order, checklist, exam, this evidence and Handoff.
- J2 implementation, old J2 Handoff, registry, validators, tests, schemas, ADRs and fixed receipt were not modified.

## Receipt and provenance verification

| Check | Independent result |
|---|---|
| Policy schema | Pass, 0 errors |
| Receipt schema | Pass, 0 errors |
| Receipt state | `authorized-not-applied`; `applied=false`; post registry, review and integration all null |
| Receipt SHA-256 | `5e85735d7c70a942efca1b8a8c6d9aecee4805a40282ae8cfbac27beab3207b1`, equals policy binding |
| Source registry SHA-256 | `d961e0b3e11f00c115bdd98f6d1216e2552bd83015c6339ce1774ef9c7a222d5`, equals receipt binding |
| J2 task-order SHA-256 | `95abc227e5b35b85495b283e587cd8893ff910d92140c4b174be4f7fdb9fcbaf`, equals receipt binding |
| Canonical transition SHA-256 | `5dfa87a441a04eb8a24e3a4de883648780b6eaeddf2c870d831fa6ed29620939` |
| Post-effective-state SHA-256 | `7f1991952dea49dff84e6378dbdc4edd22f4bf72334e0a8c08a36474fb984ec6` |
| Per-row source/before/after hashes | Pass, 5/5 |
| Checklist provenance | Pass, 22/22 path, bytes, record/work identity, scope, authority object and task-order bindings |

The receipt authorizes only this future atomic projection:

| Index | Work item | Before | Authorized after |
|---:|---|---|---|
| 109 | Activity V3 M0 | `active` | `handoff-ready` |
| 111 | Mall Catalog Solution | `active` | `integrated` |
| 112 | Mall Catalog Evidence | `active` | `integrated` |
| 113 | Mall Order Fulfillment | `planned` | `active` |
| 114 | Mall Ports Simulation | `planned` | `active` |

Current authority remains in the complete before-state. No transition is represented as applied.

## Fail-closed verification

| Scenario | Result |
|---|---|
| Existing `delivery-flow-policy.v1` rows remain governed | Pass |
| Post-cutover `delivery-flow-policy.v2` row | Pass |
| Unknown `delivery-flow-policy.v999` | Rejected with new-item policy requirement |
| Partial transition with first 1, 2, 3 or 4 rows | All four rejected as `DELIVERY_LEGACY_PARTIAL_TRANSITION` |
| Receipt SHA tamper | Rejected as `DELIVERY_LEGACY_RECEIPT_HASH_MISMATCH` |
| Registry + policy + schema triple tamper | Rejected as `DELIVERY_LEGACY_EXTERNAL_SNAPSHOT_MISMATCH` |
| `applied=true` or prefilled review/integration | Rejected by receipt schema |
| Complete five-row status projection | Legacy hash obstruction clears, but handoff-owner/request, independent-acceptance and integration gates still reject it |

The complete projection result proves that V2 does not turn receipt possession into permission to bypass the normal lifecycle evidence.

## Regression and byte-level results

| Gate | Result |
|---|---|
| Delivery Flow focused | Pass, 26/26 |
| Governance reading-list + checklist provenance focused | Pass, 22/22 |
| Complete Python regression | Pass, 92/92 |
| Service Plaza aggregate regression | Pass, 41/41 |
| Text encoding | Pass, 1545 files |
| Source implementation scope | Pass, 14/14 |
| Source-to-integration and authority blob identity | Pass, 14/14 in both comparisons |
| PowerShell encoding | Worktree starts with UTF-8 BOM, has 134 CRLF line endings and 0 bare LF; source/integration/authority Git blobs match |
| Registry change by J2 | Pass, zero diff |

## Boundary and next action

The reviewer child does not push or integrate. A different APP architecture reviewer must verify the exact five-file candidate and its final scope, encoding, secret and diff gates. After the review evidence is controlled-integrated, the platform integration owner may separately update row 126 with the real file-backed verdict. Any Activity/Mall lifecycle transaction still requires a new, current, atomic work item and all handoff, independent-acceptance and integration evidence.
