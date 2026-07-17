# Project Brain v2 M3 dashboard contracts

This directory defines the offline, server-authorized, read-only boss-dashboard candidate.

- `dashboard-policy.disabled.v1.json` is the only shipped default and keeps production, network routing, real sources, export, source writes and external authentication disabled.
- `dashboard-policy.v1.schema.json` permits an enabled dashboard only in `offline_synthetic_test`; production is structurally forced disabled.
- `server-session-claims.v1.schema.json` binds short-lived HMAC server sessions to one issuer and audience. It is not an external identity integration.
- `dashboard-overview.v1.schema.json` permits only synthetic, de-identified aggregates and permanently marks the M3 output non-decision-usable.

M3 contains no network listener, APP route, credential, real source, export endpoint, notification, deployment or production enablement. Those boundaries remain separate M4/production decisions.
