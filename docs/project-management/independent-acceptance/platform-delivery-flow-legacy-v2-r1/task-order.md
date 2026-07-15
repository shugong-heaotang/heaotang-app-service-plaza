# Legacy Delivery Flow V2 Independent Acceptance R1 Task Order

- work item: `AIW-20260715-PLATFORM-DELIVERY-FLOW-LEGACY-V2-INDEPENDENT-ACCEPTANCE-R1`
- record: `IR-20260715-PLATFORM-DELIVERY-FLOW-LEGACY-V2-INDEPENDENT-ACCEPTANCE-R1`
- actor: 平台治理独立测试负责人
- registered base: `d7d57bdb2f9b7fc90038d92a522e56393de1f22a`
- activation authority: `05bbf6465edecaa97af5d82792db868ece4f42e8`
- reviewed source: `d9822e1a36f5b9c3839feb79f020941a63aa7d66`
- controlled integration: `92ce89eab132ef5326f49de3fa3e619f1b949fb2`
- branch: `codex/platform-delivery-flow-legacy-v2-independent-acceptance-r1`
- reviewer: APP 总架构独立验收负责人
- approver: 项目最高负责人

## Scope

This checkpoint creates fresh, file-backed independent-review evidence only. It may write exactly these five path classes under this directory:

- `task-order.md`
- `development-checklist*.json`
- `governance-exam*.json`
- `evidence.md`
- `handoff.md`

The collaboration registry, J2 implementation, J2 task order, old J2 Handoff, Delivery Flow validators and tests, fixed receipt, schemas, ADRs, production, real data and funds are read-only and outside scope. The reviewer cannot push or integrate this candidate and cannot execute any lifecycle transition.

## Required independent verification

1. Prove source `d9822e1` is an ancestor of integration `92ce89e`, and integration is an ancestor of activation authority `05bbf64`.
2. Prove the source has exactly 14 changed files relative to J2 base `8776166`, all 14 match row 126 implementation scope, all 14 source blobs are preserved in integration and current authority, and the collaboration registry is unchanged by J2.
3. Validate the V2 policy, policy schema, migration schema and fixed receipt. Recompute the source-registry, legacy work-id/state, canonical transition, post-effective-state and receipt-binding SHA-256 values.
4. Verify the receipt remains `authorized-not-applied`, `applied=false`, with null post-registry, review and integration evidence. It authorizes but does not perform the five-row Activity/Mall transition.
5. Verify all 22 checklist-provenance entries bind path, SHA-256, record, work item, scope, authority commit and task-order provenance, and do not expand the legacy exception set.
6. Independently reproduce V1/V2 compatibility, unknown `v999` rejection, partial one-to-four-row rejection, receipt and registry/policy/schema tamper rejection, and prefilled review/integration rejection. A complete five-row projection must still fail closed until handoff, independent acceptance and integration evidence are valid.
7. Verify `scripts/Test-ServicePlazaContracts.ps1` preserves UTF-8 BOM plus CRLF in the Windows worktree and remains byte-identical from source through integration and authority.
8. Require Delivery Flow focused `26/26`, governance reading-list plus checklist provenance `22/22`, complete Python regression `92/92`, Service Plaza regression `41/41`, text encoding, exact allowed scope, secret scan and `git diff --check` to pass.

## Verdict rule

Issue **Go** only if every required result is independently reproduced and the reviewer candidate contains only the five authorized review artifacts. Otherwise record **No-Go** with the exact failing gate. A Go confirms the J2 receipt mechanism only; it does not apply the receipt, transition registry rows, authorize the later Activity/Mall transaction, or make row 126 integrated.

## Handoff boundary

After committing the five reviewer artifacts, stop and provide the exact candidate to a different APP architecture reviewer. The implementation owner, this reviewer child and the controlled integration owner remain separate.
