# Project Brain v2 M1 contract package

This package freezes the read-only fact boundary for Project Brain v2.

- G0 mappings may point to current authoritative governance artifacts.
- G1 mappings are contract-validation fixtures only until a business owner, authority, privacy threshold and independent re-identification review are separately approved.
- P1, H1, F1, C1 and S1 are rejected.
- Every source is read-only and has no write capability.
- Missing, stale, conflicting, low-quality, unauthorized or undersized evidence fails closed as `Unknown` or `No-Go`.
- Every result declares a privacy risk tier that must match its fact; high-risk G1 results use the high-risk threshold, never the standard fallback.
- Freshness is recomputed from the fact SLO and result timestamps; a self-declared freshness check cannot override the calculation.
- All non-null timestamps require an explicit timezone, windows must be ordered, and observed/window evidence cannot be later than evaluation time.
- Rounding applies to every numeric leaf in an aggregate object, not only scalar values.
- An undersized aggregate is a valid fail-closed `No-Go` only when its value is null, decision use is false and the threshold check/reason agree.
- Missing or unreachable sources are expressible only as value-null `Unknown`; authorization and authority-conflict failures are expressible only as value-null `No-Go`.
- No file in this package enables a scheduler, snapshot runtime, dashboard, export, deployment or production route.

Run the package validator from the repository root:

```powershell
python -X utf8 contracts/project-brain/v2/validate_contracts.py
python -X utf8 -m unittest contracts/project-brain/v2/tests/test_contracts.py -v
```
