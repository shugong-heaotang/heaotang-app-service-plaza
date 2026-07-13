# NOVA M2 Social Write Provider Handoff

- work_id: `AIW-20260712-NOVA-M2-SOCIAL-WRITE-PROVIDER-BACKEND`
- companion: `AIW-20260712-NOVA-M2-SOCIAL-WRITE-PROVIDER-EVIDENCE`
- record_id: `IR-20260712-NOVA-M2-SOCIAL-WRITE-PROVIDER-R1`
- status: `handoff-ready`
- acceptance: `pending-independent-review`
- backend source: `70fb18b82c20be1927d8b39abd530aa30d40f8a3`
- backend branch: `codex/nova-m2-social-write-provider`

## Delivered scope

Only `nova_connection_provider.go` and `nova_connection_provider_test.go` were added. The provider is not mounted to a route. It implements connection draft, confirmed/idempotent send, participant-scoped status reads, guarded status transitions, contact-policy and rejection-cooldown checks, affected-row fail-close behavior, and transactional outbox writes against temporary or synthetic SQLite only.

## Verification

- APP preflight ready; current checklist 26/26 completed; governance exam 100/passed.
- Source commit `70fb18b82c20be1927d8b39abd530aa30d40f8a3` is pushed and changes exactly the two backend allowed paths.
- `gofmt -d` and `git diff --check` are clean.
- Targeted `TestNova` package tests and targeted race tests passed.
- Full backend `go test ./...` and `go vet ./...` passed.
- Negative tests cover missing configuration, tenant/opt-out isolation, confirmation binding and expiry, idempotency payload conflict, outbox rollback, participant/resource authorization, transition conflict, cooldown, and affected-row fail-close.

## Boundary and next gate

No route, legacy social plugin modification, real member data, real message, external notification, deployment, production, payment, or irreversible write is authorized. This Handoff does not mark the source integrated or executable. Platform independent acceptance must review the exact backend source commit and this evidence commit before controlled integration or downstream M2 authorization.
