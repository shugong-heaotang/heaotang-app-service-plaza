# ADR 0002: Service Plaza Content Governance

## Status

Accepted

## Date

2026-07-09

## Context

The Service Plaza layout is finalized. The next stage is to fill real content into each module and connect each service area to its own pages and data.

If each module team directly changes the Service Plaza, the APP core entry will become inconsistent and hard to maintain.

## Decision

Use a three-layer responsibility model:

1. APP architecture owner
   - Owns Service Plaza structure, module order, navigation boundaries, and cross-module rules.
   - Approves any change to entry names, entry order, and core service scope.

2. Module owner
   - Owns the content, business rules, pages, and acceptance criteria of one module.
   - Submits module entry requirements through a standard module access card.
   - Does not directly change the Service Plaza structure.

3. Platform integration owner
   - Integrates module entries into the Service Plaza.
   - Owns frontend routing, interface contracts, permissions, analytics, and release checks.
   - Detects naming, permission, and interaction conflicts across modules.

People are not assigned automatically by whoever edits first. The project owner must formally appoint:

- APP architecture owner
- Platform integration owner
- Module owners for each service entry

Until formal appointment, all owner fields remain "to be assigned"; the project owner keeps final decision authority.

## Premises

- Service Plaza is the APP's core entry page.
- The Service Plaza layout is final and should not be changed casually.
- Each module needs freedom to build its own internal pages.
- The core entry page needs one architecture owner to prevent fragmentation.

## Consequences

- Module teams can move independently inside their own boundaries.
- Service Plaza remains stable and unified.
- Cross-module combinations must be reviewed by the APP architecture owner.
- A module cannot join the Service Plaza until its entry name, route, permission, owner, and acceptance rules are clear.
