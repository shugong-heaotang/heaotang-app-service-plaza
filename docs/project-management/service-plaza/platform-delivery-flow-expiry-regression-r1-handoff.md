# Platform Delivery Flow Expiry Regression R1 Handoff

## Status

- Record: `IR-20260715-PLATFORM-DELIVERY-FLOW-EXPIRY-REGRESSION-R1`
- Developer status: implemented; independent acceptance pending
- Base: `dc8a52a4bcc130c6cdb4da55d5d015cdf501ba16`
- Integration and push: prohibited for the implementation owner

## Authorization exception

The project principal explicitly granted one direct-principal bootstrap
exception for this slice because the fixed-clock expiry regression blocks the
normal registration gate that would authorize its own repair. The exception is
recorded in the task order and is limited to the named regression test plus the
new evidence paths. No registry, validator, production, deployment, real-data,
funds, or unrelated-path authority was inferred or used.

## Implementation

Only `test_rejects_status_expired_against_current_clock` changed. It now selects
an active or handoff-ready governed item and explicitly assigns:

- `updated_at = 2026-07-14T23:00:00+00:00`
- `status_expires_at = 2026-07-14T23:30:00+00:00`
- fixed validation clock `2026-07-15T00:00:00+00:00`

The validator and the assertion for `DELIVERY_STATUS_EXPIRED` are unchanged.
The test no longer relies on authority data naturally expiring.

## Governance and verification

- Current checklist: completed against current hashes.
- Governance exam: attempt 1, score 100, passed.
- Target delivery-flow test module: 26/26 passed.
- Delivery-flow, governance-exam, implementation-record regression set: 34/34 passed.
- Preflight: ready; checklist, exam, and implementation-record validators pass.
- Encoding: 1450 files passed; `git diff --check` passed.
- Scope: six changed paths, all authorized; secret scan: zero findings.
- Full Service Plaza contracts were executed and stopped at the existing
  authority registry: eight pre-existing active/handoff-ready items emit
  `DELIVERY_STATUS_EXPIRED`, and one of those also emits
  `DELIVERY_HANDOFF_RESPONSE_SLA_EXCEEDED`. This gate did not reach the new
  checklist/IR checks. The failure is outside this slice's allowed paths and is
  not bypassed, relabeled as passing, or repaired through the bootstrap
  exception.

## Changed paths

- `scripts/tests/test_validate_delivery_flow_policy.py`
- `docs/project-management/notices/2026-07-15-platform-delivery-flow-expiry-regression-r1-task-order.md`
- `docs/project-management/service-plaza/platform-delivery-flow-expiry-regression-r1-handoff.md`
- `contracts/foundation/development-checklists/2026-07-15-platform-delivery-flow-expiry-regression-r1.json`
- `contracts/foundation/governance-exams/2026-07-15-platform-delivery-flow-expiry-regression-r1-attempt-1.json`
- `contracts/foundation/implementation-records/2026-07-15-platform-delivery-flow-expiry-regression-r1.json`

## Residual risk and next owner

Residual implementation risk includes independent confirmation of the exact
commit, scope, and negative-test semantics. The platform integration owner also
owns the separate stale-registry/SLA remediation before the aggregate contract
gate can become Go. That authority-state blockage does not authorize this
implementation owner to edit the registry. The implementation owner does not
approve or integrate this result. The next code owner is the independent
reviewer designated by the project principal; only after a Go verdict and the
separate authority repair may the platform integration owner perform controlled
integration.
