# Platform Delivery Flow Expiry Regression R1 Task Order

## Authorization

- Record: `IR-20260715-PLATFORM-DELIVERY-FLOW-EXPIRY-REGRESSION-R1`
- Branch: `codex/platform-delivery-flow-expiry-regression-r1`
- Worktree: `C:/Users/shugo/Documents/worktrees/heaotang-platform-delivery-flow-expiry-regression-r1`
- Base: `dc8a52a4bcc130c6cdb4da55d5d015cdf501ba16`
- Developer: Delivery Flow expiry regression implementation owner
- Reviewer: independent reviewer designated by the project principal
- Approver: project principal

The project principal grants one direct-principal bootstrap exception for this
single regression slice. The exception exists only because the R12 expiry fix
made the fixed-clock negative test depend on authority data naturally becoming
expired, while the same failure prevents registering a conventional repair
item. The repository registry contains no matching active work item at this
base. This exception substitutes only for that missing registration; it does
not grant ownership of the registry, validator, production, deployment, real
data, funds, or any unrelated path, and it cannot be reused by another slice.

## Goal

Make `test_rejects_status_expired_against_current_clock` construct at least one
governed item whose `status_expires_at` is explicitly earlier than the fixed
clock supplied by the test. The negative case must no longer depend on an
authority-registry item naturally becoming expired.

## Allowed paths

- `scripts/tests/test_validate_delivery_flow_policy.py` (only the named test)
- `docs/project-management/notices/2026-07-15-platform-delivery-flow-expiry-regression-r1-task-order.md` (new)
- `docs/project-management/service-plaza/platform-delivery-flow-expiry-regression-r1-handoff.md` (new)
- `contracts/foundation/development-checklists/2026-07-15-platform-delivery-flow-expiry-regression-r1*.json` (new)
- `contracts/foundation/governance-exams/2026-07-15-platform-delivery-flow-expiry-regression-r1*.json` (new)
- `contracts/foundation/implementation-records/2026-07-15-platform-delivery-flow-expiry-regression-r1*.json` (new)

## Prohibitions

- Do not modify the validator or weaken the assertion.
- Do not modify `agent-collaboration.v1.json` or expand this exception.
- Do not modify historical checklist, exam, implementation, or acceptance evidence.
- Do not self-review, self-integrate, push, deploy, or access production.

## Acceptance evidence

- A current completed governance checklist and attempt-1 exam score of 100.
- The named negative test explicitly creates an expiry before the fixed clock.
- The targeted 34-test regression and relevant aggregate gates pass.
- Preflight, contract, encoding, diff, scope, and secret checks pass.
- A same-record implementation record and Handoff identify the bootstrap
  exception, exact changed paths, results, residual risk, and independent next
  owner.
- A local commit is created; pushing and integration remain prohibited.
