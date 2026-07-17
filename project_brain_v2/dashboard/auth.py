from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import json
import time
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

from .errors import DashboardFailure
from .policy import DashboardPolicy

TOKEN_PREFIX = "pbv2s1"


def _decode(segment: str) -> bytes:
    if not segment or len(segment) > 4096:
        raise DashboardFailure("SESSION_INVALID", http_status=401)
    try:
        return base64.b64decode(segment + "=" * (-len(segment) % 4), altchars=b"-_", validate=True)
    except (ValueError, binascii.Error) as exc:
        raise DashboardFailure("SESSION_INVALID", http_status=401) from exc


class ServerSessionVerifier:
    """Verify a short-lived server session; this class never mints or persists one."""

    def __init__(self, repo_root: Path, policy: DashboardPolicy, secret: bytes,
                 nonce_validator: Callable[[str, str, int], bool],
                 clock: Callable[[], float] = time.time) -> None:
        if not isinstance(secret, bytes) or len(secret) < 32:
            raise DashboardFailure("SESSION_KEY_INVALID", "an injected 32-byte key is required")
        if not callable(nonce_validator):
            raise DashboardFailure("SESSION_NONCE_VALIDATOR_REQUIRED")
        self._policy = policy
        self._secret = secret
        self._nonce_validator = nonce_validator
        self._clock = clock
        schema_path = repo_root / "contracts/project-brain/v2/dashboard/server-session-claims.v1.schema.json"
        try:
            self._schema = json.loads(schema_path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(self._schema)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, SchemaError) as exc:
            raise DashboardFailure("SESSION_SCHEMA_INVALID") from exc

    def verify(self, token: str) -> dict[str, Any]:
        if not isinstance(token, str) or len(token) > 8192:
            raise DashboardFailure("SESSION_INVALID", http_status=401)
        parts = token.split(".")
        if len(parts) != 3 or parts[0] != TOKEN_PREFIX:
            raise DashboardFailure("SESSION_INVALID", http_status=401)
        payload_segment, signature_segment = parts[1], parts[2]
        signing_input = f"{TOKEN_PREFIX}.{payload_segment}".encode("ascii", errors="strict")
        expected = hmac.new(self._secret, signing_input, hashlib.sha256).digest()
        supplied = _decode(signature_segment)
        if not hmac.compare_digest(expected, supplied):
            raise DashboardFailure("SESSION_INVALID", http_status=401)
        try:
            claims = json.loads(_decode(payload_segment).decode("utf-8"))
            Draft202012Validator(self._schema).validate(claims)
        except (UnicodeDecodeError, json.JSONDecodeError, ValidationError) as exc:
            raise DashboardFailure("SESSION_INVALID", http_status=401) from exc
        now = int(self._clock())
        iat = claims["iat"]
        exp = claims["exp"]
        if isinstance(iat, bool) or isinstance(exp, bool):
            raise DashboardFailure("SESSION_INVALID", http_status=401)
        if claims["iss"] != self._policy.issuer or claims["aud"] != self._policy.audience:
            raise DashboardFailure("SESSION_INVALID", http_status=401)
        if iat > now + self._policy.clock_skew_seconds:
            raise DashboardFailure("SESSION_NOT_YET_VALID", http_status=401)
        if exp <= now - self._policy.clock_skew_seconds:
            raise DashboardFailure("SESSION_EXPIRED", http_status=401)
        if exp <= iat or exp - iat > self._policy.max_session_seconds:
            raise DashboardFailure("SESSION_INVALID", http_status=401)
        if not set(claims["roles"]).intersection(self._policy.allowed_roles):
            raise DashboardFailure("ROLE_FORBIDDEN", http_status=403)
        try:
            nonce_valid = self._nonce_validator(claims["sub"], claims["nonce"], exp)
        except Exception as exc:
            raise DashboardFailure("SESSION_INVALID", http_status=401) from exc
        if nonce_valid is not True:
            raise DashboardFailure("SESSION_INVALID", http_status=401)
        return claims
