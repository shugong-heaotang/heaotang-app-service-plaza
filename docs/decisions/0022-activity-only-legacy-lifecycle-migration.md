# ADR 0022: Activity-only two-stage lifecycle migration

Status: Proposed for independent review  
Date: 2026-07-28

## Decision

Replace the ambiguous five-row Activity/Mall transaction with two content-addressed stages:

- Stage A creates a successor activation base and disposes the exact 11 expired rows without executing the Activity transition.
- Stage B may later change only Activity row 109 from `active` to `handoff-ready`.

Mall rows 111-114 are protected between the Stage A activation base and Stage B candidate by raw UTF-8 row-byte hashes. Row 111 may receive only explicitly listed governance-metadata changes while Stage A is formed and must remain `active`. Rows 112-114 do not change in Stage A. The old five-row receipt remains immutable historical evidence and is never rewritten.

R12-O remains No-Write in the central authority until this candidate has machine validation, independent P0/P1 clearance and separate activation authorization. P0-01 cannot be registered by this work item.

## Consequences

- Source, activation base and migration candidate are three distinct authorities.
- The validator fails closed on incomplete dispositions, hash drift, extra transitions, multiple writers or premature release.
- This ADR authorizes no product code or deployment.
