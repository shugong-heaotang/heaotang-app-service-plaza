# M0-R3 invalidated acceptance snapshot

These files preserve the exact M0-R3 checklist, exam, and implementation record bytes.

M0-R3 passed the repository's formal governance validators, but independent acceptance found that `validate_contract()` mixed Schema errors into the invariant count. Four of five critical mutations therefore had no independent invariant rejection even though the developer mutation gate reported success. The evidence is retained for audit and must not authorize integration or M1.

M0-R4 is the only active correction evidence.
