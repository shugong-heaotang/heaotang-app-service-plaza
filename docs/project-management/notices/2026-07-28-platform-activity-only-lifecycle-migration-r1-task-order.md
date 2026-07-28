# Activity-only lifecycle migration R1 task order

- Work ID: `AIW-20260728-ACTIVITY-ONLY-LIFECYCLE-MIGRATION-R1`
- Authority base: `d428747a072ab8a21bc07667d3b65be4906fb6c2`
- Source registry SHA-256: `611c804346b2e3861118b2d7cde6c827263b16e5d9669ab8c07b62169acc702d`
- Branch: `codex/platform-activity-only-lifecycle-migration-r1`
- Workspace: `C:/Users/shugo/Documents/worktrees/heaotang-platform-activity-only-lifecycle-migration-r1`
- Writer: platform registry owner
- Reviewer: independent platform governance validator/reviewer
- Approver: project highest owner
- Expires: `2026-07-29T12:43:00+08:00`

## Outcome

Create, but do not integrate, a Stage A successor activation-base candidate that:

1. records an exact disposition for the 11 expired rows at indices 109, 111, 117, 123, 130, 131, 134, 137, 138, 139 and 140;
2. keeps Activity row 109 active until the separately reviewed Stage B transaction;
3. keeps Mall row 111 active and limits its Stage A change to governance metadata;
4. protects Mall rows 112-114 byte-for-byte;
5. preserves the registered five-row receipt byte-for-byte;
6. keeps R12-O release, P0-01 registration and all product work No-Go until an independent Go.

## Exact writer paths

The writer may modify exactly the 16 paths recorded in the registry entry. No glob is permitted. Reviewer evidence is owned by the independent reviewer and is not a writer path.

## Stop conditions

Stop on any path expansion, missing or duplicate expired disposition, Mall byte drift, unknown contract version, source/activation/candidate authority mismatch, premature R12-O release, premature P0-01 registration, self-review, production access, real funds, or real sensitive data.

## Explicit exclusions

No business code, product branch, product worktree, push, merge, deployment, production, real payment, real funds or real sensitive data.
