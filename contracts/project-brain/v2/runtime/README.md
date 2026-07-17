# Project Brain v2 M2 runtime contract

This package authorizes offline contract-fixture verification only. It does not
activate any M1 source, network endpoint, credential, source write, external
notification, dashboard, deployment, production job, export, or production
route.

`runtime-policy.disabled.v1.json` is the shipped default and is fail-closed.
Tests may create a temporary policy with `enabled=true` only while every
production capability switch remains `false`. M1 `runtime_enabled=false` and
`production_eligible=false` values are invariants and are never overridden.
Unknown policy keys are rejected. Route, snapshot source, scheduled job, boss
dashboard, export and notification are independent explicit off-switches.

Runtime state must resolve outside the source repository and may not be an
ancestor of it. This prevents a caller from redirecting snapshots, audit, run
records or pointers into M1 contracts or any other authoritative source tree.

Runtime evidence is stored outside this contract directory. Snapshots and run
records are immutable/content-addressed; audit records form an append-only
SHA-256 chain; alerts are evidence-only and are never sent. Only the derived
`last-trusted` pointer may advance or roll back to a verified snapshot.
Audit events have their own Schema and separate `actor` and authorization
`role`; the current pointer and every run record are cross-checked against the
audit chain, including deletion and valid-old-snapshot substitution attacks.

`OfflineScheduler.tick` is deterministic scheduling logic only. It derives the
next due time from immutable run records and explicitly reports that no
production timer is present. A cron job, worker service, or deployment remains
outside M2 authority.
