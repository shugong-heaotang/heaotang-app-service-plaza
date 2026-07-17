from __future__ import annotations

import hashlib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

from .errors import DashboardFailure
from .policy import DashboardPolicy

HASH = re.compile(r"^[a-f0-9]{64}$")
SAFE_BUCKET = re.compile(r"^[A-Za-z0-9_. -]{1,64}$")
REASON_STATUS = {
    "SOURCE_MISSING": "Unknown",
    "SOURCE_NOT_REFRESHED": "Unknown",
    "SOURCE_STALE": "Unknown",
    "RUNTIME_DISABLED": "No-Go",
    "UNAUTHORIZED": "No-Go",
    "AUTHORITY_CONFLICT": "No-Go",
    "QUALITY_FAILED": "No-Go",
    "PRIVACY_THRESHOLD_FAILED": "No-Go",
    "TIMEOUT": "No-Go",
    "RETRY_EXHAUSTED": "No-Go",
    "LOCKED": "No-Go",
    "IDEMPOTENCY_CONFLICT": "No-Go",
    "TAMPER_DETECTED": "No-Go",
    "POLICY_INVALID": "No-Go",
}
EXPLANATIONS = {
    "SYNTHETIC_CONTRACT_FIXTURE": "Synthetic contract evidence passed, but it is not usable for a production decision.",
    "SOURCE_MISSING": "The latest source evidence is missing; the last trusted aggregate, if shown, is stale.",
    "SOURCE_NOT_REFRESHED": "No refresh evidence exists for this fact yet.",
    "SOURCE_STALE": "The latest source evidence exceeded its freshness rule; any displayed prior aggregate is stale.",
    "RUNTIME_DISABLED": "The refresh runtime was disabled by policy.",
    "UNAUTHORIZED": "The attempted refresh or source access was not authorized.",
    "AUTHORITY_CONFLICT": "More than one authority, or an authority mismatch, prevents a trusted conclusion.",
    "QUALITY_FAILED": "The latest evidence failed its quality contract.",
    "PRIVACY_THRESHOLD_FAILED": "The aggregate did not meet the minimum privacy threshold.",
    "TIMEOUT": "The bounded read did not finish before its deadline.",
    "RETRY_EXHAUSTED": "The bounded retry budget was exhausted.",
    "LOCKED": "Another refresh owned the single-instance lock.",
    "IDEMPOTENCY_CONFLICT": "The run identifier was reused with different input.",
    "TAMPER_DETECTED": "The immutable evidence chain did not verify.",
    "POLICY_INVALID": "A required fail-closed policy invariant was invalid.",
}


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class DashboardReader:
    """Read and verify M1/M2 evidence without creating, changing or deleting files."""

    def __init__(self, repo_root: Path, state_root: Path, policy: DashboardPolicy) -> None:
        self.repo_root = repo_root.resolve()
        self.state_root = state_root.resolve()
        self.policy = policy
        if not state_root.exists() or not state_root.is_dir() or state_root.is_symlink():
            raise DashboardFailure("STATE_INVALID", "state root must be an existing non-symlink directory")
        if self._overlaps(self.repo_root, self.state_root):
            raise DashboardFailure("STATE_INVALID", "state root must be isolated outside the repository")
        self.contract_root = self.repo_root / "contracts/project-brain/v2"
        self.dashboard_contract_root = self.contract_root / "dashboard"

    @staticmethod
    def _overlaps(left: Path, right: Path) -> bool:
        try:
            left.relative_to(right)
            return True
        except ValueError:
            try:
                right.relative_to(left)
                return True
            except ValueError:
                return False

    def _state_path(self, relative: str) -> Path:
        path = self.state_root / relative
        resolved = path.resolve()
        try:
            resolved.relative_to(self.state_root)
        except ValueError as exc:
            raise DashboardFailure("TAMPER_DETECTED", "state path escaped its root") from exc
        if path.is_symlink():
            raise DashboardFailure("TAMPER_DETECTED", "state symlinks are forbidden")
        return path

    def _read_state(self, path: Path, maximum: int | None = None) -> bytes:
        limit = self.policy.max_state_file_bytes if maximum is None else maximum
        try:
            with path.open("rb") as handle:
                data = handle.read(limit + 1)
        except OSError as exc:
            raise DashboardFailure("TAMPER_DETECTED", "state evidence is unreadable") from exc
        if len(data) > limit:
            raise DashboardFailure("TAMPER_DETECTED", "state evidence exceeds the bounded read limit")
        return data

    @staticmethod
    def _json_bytes(data: bytes, code: str = "TAMPER_DETECTED") -> dict[str, Any]:
        try:
            value = json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise DashboardFailure(code, "invalid UTF-8 JSON evidence") from exc
        if not isinstance(value, dict):
            raise DashboardFailure(code, "JSON object required")
        return value

    def _contract(self, relative: str) -> tuple[dict[str, Any], bytes]:
        path = self.contract_root / relative
        try:
            raw = path.read_bytes()
        except OSError as exc:
            raise DashboardFailure("CONTRACT_INVALID", "required contract is unreadable") from exc
        return self._json_bytes(raw, "CONTRACT_INVALID"), raw

    def _validator(self, relative: str) -> Draft202012Validator:
        schema, _ = self._contract(relative)
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            raise DashboardFailure("CONTRACT_INVALID", "invalid fixed schema") from exc
        return Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)

    @staticmethod
    def _validate(validator: Draft202012Validator, value: Any, code: str = "TAMPER_DETECTED") -> None:
        try:
            validator.validate(value)
        except ValidationError as exc:
            raise DashboardFailure(code, "evidence failed its fixed schema") from exc

    def _contracts(self) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, Any], dict[str, str]]:
        catalog, catalog_raw = self._contract("fact-catalog.v1.json")
        source_map, source_raw = self._contract("source-map.v1.json")
        privacy, privacy_raw = self._contract("privacy-threshold-policy.v1.json")
        self._validate(self._validator("fact-catalog.v1.schema.json"), catalog, "CONTRACT_INVALID")
        self._validate(self._validator("source-map.v1.schema.json"), source_map, "CONTRACT_INVALID")
        self._validate(self._validator("privacy-threshold-policy.v1.schema.json"), privacy, "CONTRACT_INVALID")
        facts = catalog.get("facts", [])
        sources = source_map.get("sources", [])
        fact_by_id = {item.get("fact_id"): item for item in facts}
        source_by_id = {item.get("fact_id"): item for item in sources}
        if len(fact_by_id) != len(facts) or len(source_by_id) != len(sources) or set(fact_by_id) != set(source_by_id):
            raise DashboardFailure("AUTHORITY_CONFLICT", "facts and sources must be one-to-one")
        for fact_id, fact in fact_by_id.items():
            source = source_by_id[fact_id]
            if fact.get("authority_id") != source.get("authority_id"):
                raise DashboardFailure("AUTHORITY_CONFLICT")
            if fact.get("read_mode") != "read_only" or fact.get("write_capability") != "none" or fact.get("production_eligible") is not False:
                raise DashboardFailure("CONTRACT_INVALID", "fact is not read-only and production-off")
            if source.get("read_mode") != "read_only" or source.get("write_capability") != "none" or source.get("runtime_enabled") is not False:
                raise DashboardFailure("CONTRACT_INVALID", "source is not read-only and runtime-off")
        if privacy.get("production_enabled") is not False or privacy.get("rules", {}).get("drill_down") is not False:
            raise DashboardFailure("CONTRACT_INVALID", "privacy policy must disable production and drill-down")
        hashes = {"catalog": sha256(catalog_raw), "source_map": sha256(source_raw), "privacy": sha256(privacy_raw)}
        return fact_by_id, source_by_id, privacy, hashes

    def _audit(self) -> list[dict[str, Any]]:
        path = self._state_path("audit.jsonl")
        if not path.exists():
            return []
        raw = self._read_state(path, self.policy.max_audit_bytes)
        lines = raw.splitlines()
        if len(lines) > self.policy.max_audit_entries:
            raise DashboardFailure("TAMPER_DETECTED", "audit entry limit exceeded")
        validator = self._validator("runtime/audit-event.v1.schema.json")
        entries: list[dict[str, Any]] = []
        previous = "0" * 64
        for line in lines:
            entry = self._json_bytes(line)
            self._validate(validator, entry)
            recorded = entry.get("entry_hash")
            unsigned = {key: value for key, value in entry.items() if key != "entry_hash"}
            if entry.get("previous_hash") != previous or recorded != sha256(canonical(unsigned)):
                raise DashboardFailure("TAMPER_DETECTED", "audit hash chain is broken")
            previous = recorded
            entries.append(entry)
        return entries

    def _directory_files(self, relative: str) -> list[Path]:
        directory = self._state_path(relative)
        if not directory.exists() or not directory.is_dir() or directory.is_symlink():
            raise DashboardFailure("TAMPER_DETECTED", f"{relative} must be a non-symlink directory")
        files: list[Path] = []
        for child in directory.iterdir():
            if child.is_symlink() or not child.is_file() or child.suffix != ".json":
                raise DashboardFailure("TAMPER_DETECTED", f"unexpected entry in {relative}")
            files.append(child)
        return sorted(files)

    def _runs(self, entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
        validator = self._validator("runtime/run-record.v1.schema.json")
        audit_records: dict[str, list[dict[str, Any]]] = {}
        for entry in entries:
            if entry.get("event") in ("refresh", "refresh_failed"):
                record = entry["run_record"]
                audit_records.setdefault(record["run_id"], []).append(record)
        records: dict[str, dict[str, Any]] = {}
        for path in self._directory_files("runs"):
            raw = self._read_state(path)
            record = self._json_bytes(raw)
            self._validate(validator, record)
            if raw != canonical(record) or path.stem != record["run_id"]:
                raise DashboardFailure("TAMPER_DETECTED", "run record is non-canonical or misnamed")
            if not any(record == candidate for candidate in audit_records.get(record["run_id"], [])):
                raise DashboardFailure("TAMPER_DETECTED", "run record is not bound to the audit chain")
            records[record["run_id"]] = record
        for run_id, candidates in audit_records.items():
            if all(item.get("reason_code") != "IDEMPOTENCY_CONFLICT" for item in candidates) and run_id not in records:
                raise DashboardFailure("TAMPER_DETECTED", "audit references a missing run record")
        return records

    def _safe_value(self, fact: dict[str, Any], result: dict[str, Any], privacy: dict[str, Any]) -> Any:
        if result.get("synthetic") is not True or result.get("decision_usable") is not False:
            raise DashboardFailure("UNAUTHORIZED", "M3 accepts synthetic non-decision evidence only")
        dimensions = fact.get("aggregation", {}).get("dimensions", [])
        forbidden = {str(item).casefold() for item in privacy.get("forbidden_dimensions", [])}
        if len(dimensions) > privacy.get("rules", {}).get("maximum_dimensions", 0):
            raise DashboardFailure("PRIVACY_THRESHOLD_FAILED")
        if any(str(item).casefold() in forbidden for item in dimensions):
            raise DashboardFailure("PRIVACY_THRESHOLD_FAILED")
        rounding_base: int | None = None
        if fact.get("classification") == "G1":
            candidate = privacy.get("rules", {}).get("rounding_base")
            if isinstance(candidate, bool) or not isinstance(candidate, int) or candidate < 1:
                raise DashboardFailure("ROUNDING_POLICY_FAILED", "G1 rounding policy is invalid")
            rounding_base = candidate

        def validate_amount(amount: Any) -> int | float:
            if isinstance(amount, bool) or not isinstance(amount, (int, float)):
                raise DashboardFailure("PRIVACY_THRESHOLD_FAILED")
            if not math.isfinite(amount) or amount < 0:
                raise DashboardFailure("PRIVACY_THRESHOLD_FAILED")
            if rounding_base is not None and amount % rounding_base != 0:
                raise DashboardFailure("ROUNDING_POLICY_FAILED", "G1 aggregate is not rounded")
            return amount

        value = result.get("value")
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return validate_amount(value)
        if not isinstance(value, dict) or len(value) > 50:
            raise DashboardFailure("PRIVACY_THRESHOLD_FAILED")
        clean: dict[str, int | float] = {}
        for key, amount in value.items():
            if not isinstance(key, str) or not SAFE_BUCKET.fullmatch(key):
                raise DashboardFailure("PRIVACY_THRESHOLD_FAILED")
            lowered = key.casefold()
            if lowered in forbidden or any(term in lowered for term in ("member", "phone", "email", "address", "payment", "order")):
                raise DashboardFailure("PRIVACY_THRESHOLD_FAILED")
            clean[key] = validate_amount(amount)
        return clean

    def _snapshots(self, entries: list[dict[str, Any]], facts: dict[str, dict[str, Any]],
                   sources: dict[str, dict[str, Any]], privacy: dict[str, Any],
                   hashes: dict[str, str]) -> dict[str, dict[str, Any]]:
        snapshot_validator = self._validator("runtime/snapshot.v1.schema.json")
        result_validator = self._validator("fact-result.v1.schema.json")
        referenced: dict[str, list[dict[str, Any]]] = {}
        for entry in entries:
            if entry.get("event") == "refresh" and entry.get("output_hash"):
                referenced.setdefault(entry["output_hash"], []).append(entry)
            elif entry.get("event") == "rollback":
                referenced.setdefault(entry["snapshot_hash"], [])
        snapshots: dict[str, dict[str, Any]] = {}
        for path in self._directory_files("snapshots"):
            raw = self._read_state(path)
            digest = sha256(raw)
            snapshot = self._json_bytes(raw)
            self._validate(snapshot_validator, snapshot)
            self._validate(result_validator, snapshot.get("result"))
            if raw != canonical(snapshot) or path.stem != digest or digest not in referenced:
                raise DashboardFailure("TAMPER_DETECTED", "snapshot is altered, misnamed or orphaned")
            fact_id = snapshot["fact_id"]
            if fact_id not in facts:
                raise DashboardFailure("TAMPER_DETECTED", "snapshot fact is not registered")
            fact = facts[fact_id]
            source = sources[fact_id]
            result = snapshot["result"]
            if snapshot["contract_hashes"] != hashes:
                raise DashboardFailure("TAMPER_DETECTED", "snapshot contract hashes are stale")
            if snapshot["authority_id"] != fact["authority_id"] or result["authority_id"] != source["authority_id"]:
                raise DashboardFailure("AUTHORITY_CONFLICT")
            if snapshot["classification"] != fact["classification"] or result["classification"] != fact["classification"]:
                raise DashboardFailure("TAMPER_DETECTED", "snapshot classification mismatch")
            if snapshot["definition"] != fact["business_definition"] or snapshot["permitted_use"] != fact["permitted_use"]:
                raise DashboardFailure("TAMPER_DETECTED", "snapshot definition or permitted use drifted")
            if result["fact_id"] != fact_id or result["definition_version"] != fact["aggregation"]["definition_version"]:
                raise DashboardFailure("TAMPER_DETECTED", "snapshot definition mismatch")
            if result["source_owner"] != fact["source_owner"] or result["privacy_risk_tier"] != fact["privacy_risk_tier"]:
                raise DashboardFailure("TAMPER_DETECTED", "snapshot owner or privacy tier mismatch")
            result["value"] = self._safe_value(fact, result, privacy)
            if result["status"] == "Trusted":
                checks = result["checks"]
                required = ("freshness", "quality", "authorization")
                if not all(checks.get(name) == "pass" for name in required):
                    raise DashboardFailure("TAMPER_DETECTED", "Trusted checks did not pass")
                if fact["classification"] == "G1":
                    minimum = privacy["rules"]["high_risk_minimum_group_size"] if fact["privacy_risk_tier"] == "high" else privacy["rules"]["standard_minimum_group_size"]
                    if not isinstance(result.get("sample_size"), int) or result["sample_size"] < minimum or checks.get("privacy_threshold") != "pass":
                        raise DashboardFailure("PRIVACY_THRESHOLD_FAILED")
            matches = referenced[digest]
            if matches and not any(
                item["fact_id"] == fact_id
                and item["source_hash"] == snapshot["source_hash"]
                and item["run_record"]["run_id"] == snapshot["run_id"]
                and item["run_record"]["snapshot_hash"] == digest
                for item in matches
            ):
                raise DashboardFailure("TAMPER_DETECTED", "snapshot is not bound to its audit event")
            snapshots[digest] = snapshot
        for digest in referenced:
            if digest not in snapshots:
                raise DashboardFailure("TAMPER_DETECTED", "audit references a missing snapshot")
        return snapshots

    def _pointer(self, entries: list[dict[str, Any]], snapshots: dict[str, dict[str, Any]]) -> None:
        path = self._state_path("last-trusted.json")
        if not path.exists():
            return
        pointer = self._json_bytes(self._read_state(path))
        if set(pointer) != {"snapshot_hash", "run_id", "updated_at", "action"}:
            raise DashboardFailure("TAMPER_DETECTED", "pointer fields are invalid")
        digest = pointer.get("snapshot_hash")
        if not isinstance(digest, str) or not HASH.fullmatch(digest) or digest not in snapshots:
            raise DashboardFailure("TAMPER_DETECTED", "pointer snapshot is invalid")
        events = [entry for entry in entries if
                  (entry.get("event") == "refresh" and entry["run_record"]["status"] == "Trusted")
                  or entry.get("event") == "rollback"]
        if not events:
            raise DashboardFailure("TAMPER_DETECTED", "pointer has no audit authority")
        latest = events[-1]
        expected_action = "rollback" if latest["event"] == "rollback" else "advance"
        expected_run = "rollback" if latest["event"] == "rollback" else latest["run_record"]["run_id"]
        expected_hash = latest.get("snapshot_hash") if latest["event"] == "rollback" else latest["run_record"]["snapshot_hash"]
        if pointer["action"] != expected_action or pointer["run_id"] != expected_run or digest != expected_hash:
            raise DashboardFailure("TAMPER_DETECTED", "pointer is not bound to the latest pointer event")

    @staticmethod
    def _last_trusted(fact_id: str, entries: Iterable[dict[str, Any]], snapshots: dict[str, dict[str, Any]]) -> tuple[str | None, dict[str, Any] | None]:
        for entry in reversed(list(entries)):
            if entry.get("event") == "refresh" and entry.get("fact_id") == fact_id and entry["run_record"]["status"] == "Trusted":
                digest = entry["run_record"]["snapshot_hash"]
                return digest, snapshots[digest]
        return None, None

    def overview(self, viewer_roles: Iterable[str]) -> dict[str, Any]:
        if not self.policy.enabled or self.policy.environment != "offline_synthetic_test":
            raise DashboardFailure("DASHBOARD_DISABLED", http_status=404)
        roles = set(viewer_roles)
        if not roles.intersection(self.policy.allowed_roles):
            raise DashboardFailure("ROLE_FORBIDDEN", http_status=403)
        facts, sources, privacy, hashes = self._contracts()
        entries = self._audit()
        self._runs(entries)
        snapshots = self._snapshots(entries, facts, sources, privacy, hashes)
        self._pointer(entries, snapshots)
        latest: dict[str, dict[str, Any]] = {}
        for entry in entries:
            if entry.get("event") in ("refresh", "refresh_failed"):
                if entry.get("fact_id") not in facts:
                    raise DashboardFailure("TAMPER_DETECTED", "audit fact is not registered")
                latest[entry["fact_id"]] = entry
        cards: list[dict[str, Any]] = []
        for fact_id in sorted(facts):
            fact = facts[fact_id]
            if not roles.intersection(fact.get("allowed_roles", [])):
                continue
            source = sources[fact_id]
            event = latest.get(fact_id)
            status = "Unknown"
            reason = "SOURCE_NOT_REFRESHED"
            cutoff = None
            value = None
            observed = None
            sample_size = None
            latest_snapshot_hash = None
            prior_snapshot_hash = None
            last_trusted = False
            stale = False
            audit_hash = None
            run_id = None
            if event:
                record = event["run_record"]
                status = record["status"]
                reason = record["reason_code"]
                cutoff = record["completed_at"]
                audit_hash = event["entry_hash"]
                run_id = record["run_id"]
                latest_snapshot_hash = record.get("snapshot_hash")
                snapshot = snapshots.get(latest_snapshot_hash) if latest_snapshot_hash else None
                if snapshot:
                    result = snapshot["result"]
                    value = result["value"]
                    observed = result["observed_at"]
                    sample_size = result["sample_size"]
                elif status != "Trusted":
                    prior_snapshot_hash, prior = self._last_trusted(fact_id, entries, snapshots)
                    if prior:
                        result = prior["result"]
                        value = result["value"]
                        observed = result["observed_at"]
                        sample_size = result["sample_size"]
                        last_trusted = True
                        stale = True
            if status == "Trusted" and reason not in EXPLANATIONS:
                explanation = "The immutable synthetic evidence chain verified; production decisions remain disabled."
            else:
                explanation = EXPLANATIONS.get(reason, "The latest evidence is not trusted; escalation is required.")
            if REASON_STATUS.get(reason) and REASON_STATUS[reason] != status:
                raise DashboardFailure("TAMPER_DETECTED", "reason and status disagree")
            cards.append({
                "fact_id": fact_id,
                "title": fact["title"],
                "status": status,
                "reason_code": reason,
                "explanation": explanation,
                "stale": stale,
                "last_trusted": last_trusted,
                "cutoff_at": cutoff,
                "observed_at": observed,
                "source_owner": source["source_owner"],
                "authority_id": source["authority_id"],
                "classification": fact["classification"],
                "definition": fact["business_definition"],
                "definition_version": fact["aggregation"]["definition_version"],
                "permitted_use": fact["permitted_use"],
                "value": value,
                "sample_size": sample_size,
                "synthetic": True,
                "decision_usable": False,
                "evidence": {
                    "audit_entry_hash": audit_hash,
                    "run_id": run_id,
                    "snapshot_hash": latest_snapshot_hash,
                    "last_trusted_snapshot_hash": prior_snapshot_hash,
                },
            })
        counts = {status: sum(card["status"] == status for card in cards) for status in ("Trusted", "Unknown", "No-Go")}
        cutoffs = [card["cutoff_at"] for card in cards if card["cutoff_at"]]
        overview = {
            "contract_version": "project-brain-dashboard-overview.v1",
            "generated_at": utc_now(),
            "environment": "offline_synthetic_test",
            "data_mode": "synthetic_only",
            "production_enabled": False,
            "network_route_enabled": False,
            "decision_usable": False,
            "as_of": max(cutoffs, key=lambda value: datetime.fromisoformat(value.replace("Z", "+00:00"))) if cutoffs else None,
            "status_counts": counts,
            "facts": cards,
        }
        schema = json.loads((self.dashboard_contract_root / "dashboard-overview.v1.schema.json").read_text(encoding="utf-8"))
        try:
            Draft202012Validator.check_schema(schema)
            Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER).validate(overview)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, SchemaError, ValidationError) as exc:
            raise DashboardFailure("CONTRACT_INVALID", "overview failed its fixed schema") from exc
        return overview
