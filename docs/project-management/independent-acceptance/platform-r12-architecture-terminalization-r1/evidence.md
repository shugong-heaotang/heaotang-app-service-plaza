# Platform R12 Architecture Terminalization R1 Evidence

- work_id: `AIW-20260715-PLATFORM-R12-ARCHITECTURE-TERMINALIZATION-R1`
- authority_base: `9f79d06d502bf11ad0bb7f6dc74c80c0175f01d3`
- reviewer_role: APP 总架构独立验收负责人
- reviewed_at: `2026-07-15T22:05:44+08:00`
- verdict: `Go for a fresh terminalization candidate; historical candidates are not replayable as current registry transactions`

## Task-order and entry-governance causality

| Evidence | Value |
| --- | --- |
| task order | `docs/project-management/notices/2026-07-15-platform-r12-architecture-terminalization-r1-task-order.md` |
| task-order SHA-256 | `4950ec52fcbaad9c2253a0abf181904f046195e1c1b8b66ef6d389703071c69b` |
| task order signed | `2026-07-15T13:55:47.5200151Z` |
| entry checklist created | `2026-07-15T13:56:51.4810596Z` |
| task order read | `2026-07-15T14:02:17.089Z` |
| entry checklist completed | `2026-07-15T14:02:41.356Z` |
| entry checklist SHA-256 | `c4079e6f34373dd59bd688afca8106f10102a986f6dbc6c2bd77a75047095e5f` |
| entry exam generated | `2026-07-15T14:04:01.7237157Z` |
| entry exam completed | `2026-07-15T14:04:21.5595366Z` |
| entry exam result | `100 / passed` |

The repository exam gate requires the checklist item set to equal the canonical reading
list exactly, so the task order is bound here and in the implementation record rather
than inserted as an invalid extra checklist item. The recorded order proves task-order
issuance, reading, checklist completion, and exam generation were causal rather than
backfilled.

This entry snapshot authorized the scoped registry implementation. Because the registry
is itself a governance input and changed during terminalization, it is not presented as
the final current snapshot. After this evidence and its SHA are frozen into the final
registry bytes, a distinct R2 checklist and exam must prove the final governance state.

## Legacy V2 source and architecture verdict

- implementation source: `d9822e1a36f5b9c3839feb79f020941a63aa7d66`
- file-backed independent-test candidate: `aa23dbe37b4310c081b7cfdec2459fd8df1b7c7a`
- original independent-test evidence:
  `docs/project-management/independent-acceptance/platform-delivery-flow-legacy-v2-r1/evidence.md`
- original evidence SHA-256:
  `f565074b0ce0a584a13307946a7fb65a127ec3fc4d8d1330a068a853b90e185b`
- early integration: `f986734ff27ec3d58ada69a16620ce4e2d5d2f7f`
- APP architecture verdict: `Go`, recorded at the real `reviewed_at` above.

Independent APP architecture review verified the clean and remote-identical exact
`aa23dbe` candidate, five allowed evidence paths, checklist 26/26, exam 100, causal
ordering, exact ancestry, 14/14 implementation paths and blobs, 22/22 provenance
entries, Delivery Flow 26/26, provenance 15/15, aggregate 41/41, UTF-8 1545, diff and
secret gates. The old receipt remained byte-identical and unapplied.

`f986734` contains `aa23dbe`, but it was created before this distinct APP architecture
verdict. This is an `integration-preceded-final-verdict` governance deviation.
`f986734` is preserved as historical integration evidence only; it is not substituted
for the later verdict and no `reviewed_at` value is backdated.

## R12-L exact verdict

- exact source: `8f8f2f6e90ec11610ff73562979c64c3acbaabfe`
- historical integration: `05bbf6465edecaa97af5d82792db868ece4f42e8`
- verdict: `content Go / current direct integration No-Go`

The exact six-path candidate matched its six allowed paths, preserved rows 90, 91 and
126, released only R12-K registry ownership and added isolated children. Static
collaboration, preflight, checklist 26/26, exam 100, IR, UTF-8 1540, diff, secret,
submission-clock Delivery Flow and Delivery Flow tests 26/26 passed; the candidate was
clean and remote-identical.

It is not replayable as a current registry transaction: six active rows later expired,
and the current aggregate run had 32 passing tests while nine tests were twice blocked
by the Windows Python alias environment. No 41/41 current claim is made. `05bbf646`
also preceded the final verdict and remains historical integration evidence only.

## R12-M exact verdict

- exact source: `2f4cb9d49aed6c1f082f06ef435b6f453862542a`
- verdict: `technical content Go / direct integration Exact revision`

The six-path candidate passed its technical, governance and scope checks, but it did
not contain the later distinct APP architecture verdict and did not disclose the
early-integration timing deviation. It therefore must not be replayed or labelled
integrated. The fresh transaction supersedes its registry purpose and records R12-M
as cancelled by remediation, preserving the source and review history.

## Receipt and boundary proof

- old receipt:
  `contracts/foundation/legacy-lifecycle-migrations/LLM-20260715-ACTIVITY-MALL-M2-R1.json`
- SHA-256:
  `5e85735d7c70a942efca1b8a8c6d9aecee4805a40282ae8cfbac27beab3207b1`
- state: `authorized-not-applied`
- applied: `false`
- transitions: `5`

This checkpoint does not edit or execute the receipt, change any Mall row, implement
supersession schemas, or activate Activity lifecycle decoupling. It only prepares a
fresh registry terminalization candidate for another independent review.
