# Project Brain v2 M1 contract package

This package freezes the read-only fact boundary for Project Brain v2.

- G0 mappings may point to current authoritative governance artifacts.
- G1 mappings are contract-validation fixtures only until a business owner, authority, privacy threshold and independent re-identification review are separately approved.
- P1, H1, F1, C1 and S1 are rejected.
- Every source is read-only and has no write capability.
- Missing, stale, conflicting, low-quality, unauthorized or undersized evidence fails closed as `Unknown` or `No-Go`.
- No file in this package enables a scheduler, snapshot runtime, dashboard, export, deployment or production route.

Run the package validator from the repository root:

```powershell
python -X utf8 contracts/project-brain/v2/validate_contracts.py
python -X utf8 -m unittest contracts/project-brain/v2/tests/test_contracts.py -v
```
