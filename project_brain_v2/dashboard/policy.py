from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

from .errors import DashboardFailure

OFF_SWITCHES = (
    "production_enabled",
    "network_route_enabled",
    "real_sources_enabled",
    "export_enabled",
    "source_writes_enabled",
    "external_auth_enabled",
)


@dataclass(frozen=True)
class DashboardPolicy:
    environment: str
    enabled: bool
    production_enabled: bool
    network_route_enabled: bool
    real_sources_enabled: bool
    export_enabled: bool
    source_writes_enabled: bool
    external_auth_enabled: bool
    audience: str
    issuer: str
    allowed_roles: tuple[str, ...]
    max_session_seconds: int
    clock_skew_seconds: int
    max_state_file_bytes: int
    max_audit_bytes: int
    max_audit_entries: int

    @classmethod
    def load(cls, repo_root: Path, policy_path: Path) -> "DashboardPolicy":
        try:
            value = json.loads(policy_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise DashboardFailure("POLICY_INVALID", "dashboard policy is unreadable") from exc
        return cls.from_mapping(repo_root, value)

    @classmethod
    def from_mapping(cls, repo_root: Path, value: Mapping[str, Any]) -> "DashboardPolicy":
        schema_path = repo_root / "contracts/project-brain/v2/dashboard/dashboard-policy.v1.schema.json"
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            Draft202012Validator(schema).validate(dict(value))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, SchemaError, ValidationError) as exc:
            raise DashboardFailure("POLICY_INVALID", "dashboard policy failed its fixed schema") from exc
        if any(value.get(name) is not False for name in OFF_SWITCHES):
            raise DashboardFailure("POLICY_INVALID", "M3 capability switches must remain false")
        if value.get("enabled") is True and value.get("environment") != "offline_synthetic_test":
            raise DashboardFailure("POLICY_INVALID", "only offline synthetic preview may be enabled")
        return cls(
            environment=str(value["environment"]),
            enabled=value["enabled"] is True,
            production_enabled=False,
            network_route_enabled=False,
            real_sources_enabled=False,
            export_enabled=False,
            source_writes_enabled=False,
            external_auth_enabled=False,
            audience=str(value["audience"]),
            issuer=str(value["issuer"]),
            allowed_roles=tuple(value["allowed_roles"]),
            max_session_seconds=int(value["max_session_seconds"]),
            clock_skew_seconds=int(value["clock_skew_seconds"]),
            max_state_file_bytes=int(value["max_state_file_bytes"]),
            max_audit_bytes=int(value["max_audit_bytes"]),
            max_audit_entries=int(value["max_audit_entries"]),
        )
