# NOVA Overlay R2 fresh independent acceptance task order

- Work item: `AIW-20260714-PLATFORM-NOVA-OVERLAY-R2-INDEPENDENT-ACCEPTANCE`
- Record: `IR-20260715-PLATFORM-NOVA-OVERLAY-R2-INDEPENDENT-ACCEPTANCE-R2`
- Actor: Platform governance independent test agent
- Registered branch: `codex/platform-nova-overlay-r2-independent-acceptance`
- Registered base: `9090fb5338a10d838cdea7ac75d0c61cdc0285a9`
- Re-anchor history: `b609b375b2a8eacfaef7ccb1aee88cc989bb781b` -> `86f7fdc218252cb6333f39850112f7e03d35128c`
- Current authority: `640738097102820f2e53ac8a2a0e465fa7acea58`
- Current registry SHA-256: `cdacf712f9065514914887e48706fda8580ba60d40d30aa25acb0eceb347defd`
- Reviewed source: `59a988df0d7d1a13ac4dd9ad48da62d5c0340534`
- Controlled integration: `81f6bc8a7e1bc872f1689099a704768495deb009`

## Scope

This checkpoint creates fresh R2 independent-acceptance evidence only. It may write exactly these new files:

- `evidence-r2.md`
- `task-order-r2.md`
- `development-checklist-r2.json`
- `governance-exam-r2-attempt-1.json`
- `implementation-record-r2.json`

The existing R1 files are immutable. The registry, shared scripts, contracts, source implementation, deployment, production, real data and funds are outside scope.

## Required verification

1. Prove source `59a988d` is an ancestor of integration `81f6bc8`, and integration is an ancestor of current authority `6407380`.
2. Prove the 19 source changes remain within the registered implementation scope and the implementation did not alter the collaboration registry.
3. Run the focused governance regressions, requiring 22/22.
4. Run the complete Python regression, requiring 92/92.
5. Run the Service Plaza total contract, text-encoding and diff gates on the current authority/reviewer candidate.
6. Bind the fresh checklist, passed exam and implementation record to this same R2 record and current registry hash.
7. Do not cite an R1 pass or R1 artifact hash as evidence for the R2 verdict.

## Handoff boundary

The candidate remains local and unintegrated. A different APP architecture acceptance agent must review the exact candidate before any push, lifecycle transition or controlled integration.
