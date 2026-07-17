from __future__ import annotations

import hashlib
import json
import os
import queue
import re
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
ALLOWED_FIXTURE_DIR = Path("contracts/project-brain/v2/examples")
REQUIRED_OFF_SWITCHES = (
    "production_enabled",
    "production_route_enabled",
    "production_snapshot_source_enabled",
    "scheduled_production_job_enabled",
    "boss_dashboard_enabled",
    "export_enabled",
    "notification_enabled",
    "network_enabled",
    "real_sources_enabled",
    "source_writes_enabled",
    "external_notifications_enabled",
)
POLICY_KEYS = {
    "contract_version", "enabled", *REQUIRED_OFF_SWITCHES, "max_attempts", "timeout_seconds",
    "max_source_bytes", "schedule_interval_seconds", "allowed_fixtures",
}
REASON_STATUS = {
    "SOURCE_MISSING": "Unknown",
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

def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

class RuntimeFailure(Exception):
    def __init__(self, reason: str, message: str = "", attempts: int = 0) -> None:
        super().__init__(message or reason)
        self.reason = reason
        self.status = REASON_STATUS.get(reason, "No-Go")
        self.attempts = attempts


class TransientSourceError(Exception):
    pass


@dataclass(frozen=True)
class RuntimePaths:
    root: Path

    @property
    def snapshots(self) -> Path: return self.root / "snapshots"
    @property
    def runs(self) -> Path: return self.root / "runs"
    @property
    def alerts(self) -> Path: return self.root / "alerts.jsonl"
    @property
    def audit(self) -> Path: return self.root / "audit.jsonl"
    @property
    def pointer(self) -> Path: return self.root / "last-trusted.json"
    @property
    def lock(self) -> Path: return self.root / "refresh.lock"


class RefreshEngine:
    """Offline-only, fail-closed refresh engine for M1 synthetic fixtures.

    M1 source-map entries remain runtime_disabled. M2 does not override that
    fact: it evaluates only allowlisted contract fixtures for offline proof.
    """

    def __init__(self, repo_root: Path, state_root: Path, policy_path: Path,
                 reader: Callable[[Path, int], bytes] | None = None,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self.repo_root = repo_root.resolve()
        self.paths = RuntimePaths(state_root.resolve())
        self.policy_path = policy_path.resolve()
        self.reader = reader or self._bounded_read
        self.clock = clock
        try:
            self.paths.root.relative_to(self.repo_root)
            overlaps = True
        except ValueError:
            try:
                self.repo_root.relative_to(self.paths.root)
                overlaps = True
            except ValueError:
                overlaps = False
        if overlaps:
            raise RuntimeFailure("POLICY_INVALID", "state_root must be isolated outside the source repository")
        self.paths.root.mkdir(parents=True, exist_ok=True)
        self.paths.snapshots.mkdir(exist_ok=True)
        self.paths.runs.mkdir(exist_ok=True)

    def _bounded_read(self, path: Path, maximum: int) -> bytes:
        with path.open("rb") as handle:
            data = handle.read(maximum + 1)
        if len(data) > maximum:
            raise RuntimeFailure("QUALITY_FAILED", "source exceeds max_source_bytes")
        return data

    def _json(self, path: Path) -> tuple[dict[str, Any], bytes]:
        data = path.read_bytes()
        try:
            value = json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RuntimeFailure("QUALITY_FAILED", f"invalid JSON: {path}") from exc
        if not isinstance(value, dict):
            raise RuntimeFailure("QUALITY_FAILED", f"object required: {path}")
        return value, data

    def _policy(self) -> tuple[dict[str, Any], bytes]:
        policy, raw = self._json(self.policy_path)
        schema_path = self.repo_root / "contracts/project-brain/v2/runtime/runtime-policy.v1.schema.json"
        schema, _ = self._json(schema_path)
        try:
            Draft202012Validator.check_schema(schema)
            Draft202012Validator(schema).validate(policy)
        except (SchemaError, ValidationError) as exc:
            raise RuntimeFailure("POLICY_INVALID", "runtime policy failed its fixed-version schema") from exc
        if policy.get("contract_version") != "project-brain-runtime-policy.v1":
            raise RuntimeFailure("POLICY_INVALID", "unknown runtime policy")
        if set(policy) != POLICY_KEYS:
            raise RuntimeFailure("POLICY_INVALID", "runtime policy keys must exactly match the M2 schema")
        if any(policy.get(name) is not False for name in REQUIRED_OFF_SWITCHES):
            raise RuntimeFailure("POLICY_INVALID", "all production capability switches must be false")
        for key in ("max_attempts", "timeout_seconds", "max_source_bytes", "schedule_interval_seconds"):
            if not isinstance(policy.get(key), int) or policy[key] < 1:
                raise RuntimeFailure("POLICY_INVALID", f"invalid {key}")
        if policy["max_attempts"] > 3 or policy["timeout_seconds"] > 60 or policy["max_source_bytes"] > 1048576:
            raise RuntimeFailure("POLICY_INVALID", "runtime resource bound exceeds M2 maximum")
        if not 60 <= policy["schedule_interval_seconds"] <= 86400:
            raise RuntimeFailure("POLICY_INVALID", "schedule interval outside M2 bounds")
        allowed = policy.get("allowed_fixtures")
        if not isinstance(allowed, list) or not allowed or not all(isinstance(x, str) for x in allowed):
            raise RuntimeFailure("POLICY_INVALID", "allowed_fixtures must be non-empty strings")
        return policy, raw

    @contextmanager
    def _lock(self, run_id: str):
        try:
            fd = os.open(self.paths.lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError as exc:
            raise RuntimeFailure("LOCKED", "another refresh owns the single-instance lock") from exc
        try:
            os.write(fd, canonical({"run_id": run_id, "acquired_at": utc_now()}))
            os.close(fd)
            yield
        finally:
            try: self.paths.lock.unlink()
            except FileNotFoundError: pass

    def _fixture_path(self, relative: str, allowed: list[str]) -> Path:
        normalized = Path(relative).as_posix()
        if normalized not in allowed:
            raise RuntimeFailure("UNAUTHORIZED", "fixture is not policy-allowlisted")
        path = (self.repo_root / normalized).resolve()
        fixture_root = (self.repo_root / ALLOWED_FIXTURE_DIR).resolve()
        try: path.relative_to(fixture_root)
        except ValueError as exc:
            raise RuntimeFailure("UNAUTHORIZED", "fixture escaped the contract fixture directory") from exc
        return path

    def _contracts(self, fact_id: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
        base = self.repo_root / "contracts/project-brain/v2"
        catalog, cat_raw = self._json(base / "fact-catalog.v1.json")
        source_map, src_raw = self._json(base / "source-map.v1.json")
        privacy, privacy_raw = self._json(base / "privacy-threshold-policy.v1.json")
        all_facts = catalog.get("facts", [])
        all_sources = source_map.get("sources", [])
        if any(item.get("production_eligible") is not False or item.get("read_mode") != "read_only"
               or item.get("write_capability") != "none" for item in all_facts):
            raise RuntimeFailure("POLICY_INVALID", "every M1 fact must remain read-only and production-ineligible")
        if any(item.get("runtime_enabled") is not False or item.get("read_mode") != "read_only"
               or item.get("write_capability") != "none" for item in all_sources):
            raise RuntimeFailure("POLICY_INVALID", "every M1 source must remain read-only and runtime-off")
        facts = [x for x in all_facts if x.get("fact_id") == fact_id]
        sources = [x for x in all_sources if x.get("fact_id") == fact_id]
        if len(facts) != 1 or len(sources) != 1:
            raise RuntimeFailure("AUTHORITY_CONFLICT", "fact requires exactly one catalog and source entry")
        fact, source = facts[0], sources[0]
        if fact.get("authority_id") != source.get("authority_id"):
            raise RuntimeFailure("AUTHORITY_CONFLICT")
        if fact.get("read_mode") != "read_only" or fact.get("write_capability") != "none":
            raise RuntimeFailure("UNAUTHORIZED", "fact is not read-only")
        if source.get("read_mode") != "read_only" or source.get("write_capability") != "none":
            raise RuntimeFailure("UNAUTHORIZED", "source is not read-only")
        if source.get("runtime_enabled") is not False or fact.get("production_eligible") is not False:
            raise RuntimeFailure("POLICY_INVALID", "M1 must remain runtime-off and production-ineligible")
        return fact, source, {"catalog": sha256(cat_raw), "source_map": sha256(src_raw), "privacy": sha256(privacy_raw), "privacy_policy": privacy}

    def _evaluate(self, fact: dict[str, Any], source: dict[str, Any], fixture: dict[str, Any], role: str,
                  privacy: dict[str, Any]) -> dict[str, Any]:
        if role not in fact.get("allowed_roles", []):
            raise RuntimeFailure("UNAUTHORIZED")
        if fixture.get("fact_id") != fact.get("fact_id"):
            raise RuntimeFailure("QUALITY_FAILED", "fixture fact mismatch")
        if fixture.get("classification") != fact.get("classification"):
            raise RuntimeFailure("QUALITY_FAILED", "fixture classification mismatch")
        if fixture.get("privacy_risk_tier") != fact.get("privacy_risk_tier"):
            raise RuntimeFailure("QUALITY_FAILED", "fixture privacy risk tier mismatch")
        if fixture.get("authority_id") != source.get("authority_id"):
            raise RuntimeFailure("AUTHORITY_CONFLICT")
        if fixture.get("synthetic") is not True:
            raise RuntimeFailure("UNAUTHORIZED", "M2 accepts synthetic contract fixtures only")
        if fixture.get("decision_usable") is not False:
            raise RuntimeFailure("UNAUTHORIZED", "offline fixture can never be decision-usable")
        status = fixture.get("status")
        if status not in ("Trusted", "Unknown", "No-Go"):
            raise RuntimeFailure("QUALITY_FAILED", "unknown result status")
        checks = fixture.get("checks") or {}
        if checks.get("authority_conflict") is True:
            raise RuntimeFailure("AUTHORITY_CONFLICT")
        if checks.get("authorization") == "fail":
            raise RuntimeFailure("UNAUTHORIZED")
        if checks.get("privacy_threshold") == "fail":
            raise RuntimeFailure("PRIVACY_THRESHOLD_FAILED")
        if checks.get("quality") == "fail":
            raise RuntimeFailure("QUALITY_FAILED")
        if checks.get("source_available") is False:
            raise RuntimeFailure("SOURCE_MISSING")
        if checks.get("freshness") == "fail":
            raise RuntimeFailure("SOURCE_STALE")
        if status == "Trusted":
            if not all(checks.get(k) == "pass" for k in ("freshness", "quality", "authorization")):
                raise RuntimeFailure("QUALITY_FAILED", "Trusted requires freshness, quality and authorization checks to pass")
            classification = fact.get("classification")
            sample_size = fixture.get("sample_size")
            if classification == "G0":
                if sample_size is not None or checks.get("privacy_threshold") != "not_applicable":
                    raise RuntimeFailure("PRIVACY_THRESHOLD_FAILED", "G0 requires no sample threshold")
            elif classification == "G1":
                minimum = privacy["rules"]["high_risk_minimum_group_size"] if fact.get("privacy_risk_tier") == "high" else privacy["rules"]["standard_minimum_group_size"]
                if isinstance(sample_size, bool) or not isinstance(sample_size, int) or sample_size < minimum:
                    raise RuntimeFailure("PRIVACY_THRESHOLD_FAILED")
                if checks.get("privacy_threshold") != "pass":
                    raise RuntimeFailure("PRIVACY_THRESHOLD_FAILED", "G1 requires a passed sample threshold")
            else:
                raise RuntimeFailure("QUALITY_FAILED", "unsupported fact classification")
        return fixture

    def _read_with_retry(self, path: Path, policy: dict[str, Any], deadline: float) -> tuple[bytes, int]:
        last: Exception | None = None
        for attempt in range(1, policy["max_attempts"] + 1):
            remaining = deadline - self.clock()
            if remaining <= 0: raise RuntimeFailure("TIMEOUT", attempts=attempt - 1)
            outcome: queue.Queue[tuple[bool, Any]] = queue.Queue(maxsize=1)
            def read_once() -> None:
                try: outcome.put((True, self.reader(path, policy["max_source_bytes"])))
                except BaseException as exc: outcome.put((False, exc))
            worker = threading.Thread(target=read_once, name="project-brain-read", daemon=True)
            worker.start()
            worker.join(remaining)
            if worker.is_alive():
                raise RuntimeFailure("TIMEOUT", "read isolated after deadline", attempts=attempt)
            succeeded, value = outcome.get_nowait()
            try:
                if not succeeded: raise value
                data = value
                if self.clock() >= deadline: raise RuntimeFailure("TIMEOUT", attempts=attempt)
                return data, attempt
            except FileNotFoundError as exc:
                raise RuntimeFailure("SOURCE_MISSING", attempts=attempt) from exc
            except TransientSourceError as exc:
                last = exc
        raise RuntimeFailure("RETRY_EXHAUSTED", str(last or "transient source failure"), policy["max_attempts"])

    def _immutable(self, path: Path, payload: dict[str, Any]) -> str:
        data = canonical(payload)
        digest = sha256(data)
        target = path / f"{digest}.json" if path.is_dir() else path
        try:
            with target.open("xb") as handle: handle.write(data)
        except FileExistsError:
            if target.read_bytes() != data:
                raise RuntimeFailure("TAMPER_DETECTED", f"immutable collision: {target}")
        return digest

    def _audit_entries(self) -> list[dict[str, Any]]:
        if not self.paths.audit.exists(): return []
        entries: list[dict[str, Any]] = []
        previous = "0" * 64
        for line in self.paths.audit.read_bytes().splitlines():
            try: entry = json.loads(line.decode("utf-8"))
            except Exception as exc: raise RuntimeFailure("TAMPER_DETECTED", "audit is not valid JSONL") from exc
            recorded = entry.pop("entry_hash", None)
            if entry.get("previous_hash") != previous or recorded != sha256(canonical(entry)):
                raise RuntimeFailure("TAMPER_DETECTED", "audit hash chain is broken")
            self._validate_audit_payload({key: value for key, value in entry.items() if key != "previous_hash"})
            entry["entry_hash"] = recorded
            previous = recorded
            entries.append(entry)
        return entries

    def _validate_audit_payload(self, payload: dict[str, Any]) -> None:
        if payload.get("contract_version") != "project-brain-audit-event.v1":
            raise RuntimeFailure("QUALITY_FAILED", "audit contract version is missing")
        if not isinstance(payload.get("actor"), str) or not payload["actor"]:
            raise RuntimeFailure("QUALITY_FAILED", "audit actor is required")
        if not isinstance(payload.get("role"), str) or not payload["role"]:
            raise RuntimeFailure("QUALITY_FAILED", "audit role is required")
        if payload.get("event") in ("refresh", "refresh_failed"):
            required = {"contract_version", "event", "actor", "role", "fact_id", "authority_id", "source_owner",
                        "source_hash", "definition_version", "classification", "freshness", "quality", "output_hash",
                        "run_record"}
            if set(payload) != required or not isinstance(payload.get("run_record"), dict):
                raise RuntimeFailure("QUALITY_FAILED", "refresh audit fields do not match the contract")
            if payload["run_record"].get("contract_version") != "project-brain-run-record.v1":
                raise RuntimeFailure("QUALITY_FAILED", "audit run record is invalid")
        elif payload.get("event") == "rollback":
            if set(payload) != {"contract_version", "event", "actor", "role", "snapshot_hash", "reason", "at"}:
                raise RuntimeFailure("QUALITY_FAILED", "rollback audit fields do not match the contract")
        else:
            raise RuntimeFailure("QUALITY_FAILED", "unknown audit event")

    def _append(self, path: Path, payload: dict[str, Any], chained: bool = False) -> str:
        if chained:
            self._validate_audit_payload(payload)
            entries = self._audit_entries()
            payload = {**payload, "previous_hash": entries[-1]["entry_hash"] if entries else "0" * 64}
            payload["entry_hash"] = sha256(canonical(payload))
        data = canonical(payload)
        fd = os.open(path, os.O_APPEND | os.O_CREAT | os.O_WRONLY)
        try: os.write(fd, data)
        finally: os.close(fd)
        return payload.get("entry_hash", sha256(data))

    def verify_audit(self) -> int:
        return len(self._audit_entries())

    def verify_run_record(self, record: dict[str, Any]) -> None:
        keys = ("contract_version", "run_id", "input_hash", "status", "reason_code", "started_at",
                "completed_at", "attempts", "snapshot_hash")
        matches = [entry for entry in self._audit_entries()
                   if entry.get("event") in ("refresh", "refresh_failed")
                   and entry.get("run_record", {}).get("run_id") == record.get("run_id")]
        if not any(all(entry["run_record"].get(key) == record.get(key) for key in keys) for entry in matches):
            raise RuntimeFailure("TAMPER_DETECTED", "run record is not bound to the audit chain")

    def verify_run_history(self) -> list[dict[str, Any]]:
        entries = self._audit_entries()
        required = {entry["run_record"]["run_id"] for entry in entries
                    if entry.get("event") in ("refresh", "refresh_failed")
                    and entry.get("run_record", {}).get("reason_code") != "IDEMPOTENCY_CONFLICT"}
        records: list[dict[str, Any]] = []
        for run_id in sorted(required):
            path = self.paths.runs / f"{run_id}.json"
            if not path.exists():
                raise RuntimeFailure("TAMPER_DETECTED", "audit references a missing immutable run record")
        for path in self.paths.runs.glob("*.json"):
            try: record = json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc: raise RuntimeFailure("TAMPER_DETECTED", "run history contains invalid JSON") from exc
            self.verify_run_record(record)
            records.append(record)
        return records

    def verified_pointer(self) -> dict[str, Any] | None:
        if not self.paths.pointer.exists():
            return None
        try:
            pointer = json.loads(self.paths.pointer.read_text(encoding="utf-8"))
            snapshot_hash = pointer["snapshot_hash"]
        except Exception as exc:
            raise RuntimeFailure("TAMPER_DETECTED", "last-trusted pointer is malformed") from exc
        if not isinstance(snapshot_hash, str) or not re.fullmatch(r"[a-f0-9]{64}", snapshot_hash):
            raise RuntimeFailure("TAMPER_DETECTED", "last-trusted pointer hash is invalid")
        snapshot = self.paths.snapshots / f"{snapshot_hash}.json"
        if not snapshot.exists() or sha256(snapshot.read_bytes()) != snapshot_hash:
            raise RuntimeFailure("TAMPER_DETECTED", "last-trusted pointer references an altered snapshot")
        pointer_events = [entry for entry in self._audit_entries()
                          if (entry.get("event") == "refresh" and entry.get("run_record", {}).get("status") == "Trusted")
                          or entry.get("event") == "rollback"]
        if not pointer_events:
            raise RuntimeFailure("TAMPER_DETECTED", "last-trusted pointer has no audit authority")
        authority = pointer_events[-1]
        expected_action = "rollback" if authority["event"] == "rollback" else "advance"
        expected_run = "rollback" if authority["event"] == "rollback" else authority["run_record"]["run_id"]
        expected_snapshot = authority.get("snapshot_hash") if authority["event"] == "rollback" else authority["run_record"]["snapshot_hash"]
        if pointer.get("snapshot_hash") != expected_snapshot or pointer.get("action") != expected_action or pointer.get("run_id") != expected_run:
            raise RuntimeFailure("TAMPER_DETECTED", "last-trusted pointer is not bound to the latest pointer audit event")
        return pointer

    def _pointer(self, snapshot_hash: str, run_id: str, action: str = "advance") -> None:
        target = self.paths.snapshots / f"{snapshot_hash}.json"
        if not target.exists() or sha256(target.read_bytes()) != snapshot_hash:
            raise RuntimeFailure("TAMPER_DETECTED", "snapshot does not match content address")
        temp = self.paths.pointer.with_suffix(".tmp")
        temp.write_bytes(canonical({"snapshot_hash": snapshot_hash, "run_id": run_id, "updated_at": utc_now(), "action": action}))
        os.replace(temp, self.paths.pointer)

    def _replay(self, existing_path: Path, input_hash: str) -> dict[str, Any] | None:
        if not existing_path.exists():
            return None
        try: existing = json.loads(existing_path.read_text(encoding="utf-8"))
        except Exception as exc: raise RuntimeFailure("TAMPER_DETECTED", "run record is malformed") from exc
        self.verify_run_record(existing)
        if existing.get("input_hash") != input_hash:
            raise RuntimeFailure("IDEMPOTENCY_CONFLICT")
        snapshot_hash = existing.get("snapshot_hash")
        if snapshot_hash:
            snapshot_path = self.paths.snapshots / f"{snapshot_hash}.json"
            if not snapshot_path.exists() or sha256(snapshot_path.read_bytes()) != snapshot_hash:
                raise RuntimeFailure("TAMPER_DETECTED", "idempotent replay snapshot was altered")
        return existing

    def _run(self, run_id: str, fact_id: str, fixture_path: str, role: str,
             actor: str = "project_brain_v2_runtime") -> dict[str, Any]:
        if not RUN_ID.fullmatch(run_id): raise RuntimeFailure("QUALITY_FAILED", "unsafe run_id")
        started = utc_now()
        policy, policy_raw = self._policy()
        input_seed = {"fact_id": fact_id, "fixture_path": fixture_path, "actor": actor,
                      "role": role, "policy_sha256": sha256(policy_raw)}
        existing_path = self.paths.runs / f"{run_id}.json"
        with self._lock(run_id):
            try:
                if policy.get("enabled") is not True:
                    input_hash = sha256(canonical({**input_seed, "source_state": "RUNTIME_DISABLED"}))
                    replay = self._replay(existing_path, input_hash)
                    if replay: return replay
                    raise RuntimeFailure("RUNTIME_DISABLED")
                self.verified_pointer()
                fixture_file = self._fixture_path(fixture_path, policy["allowed_fixtures"])
                fact, source, hashes = self._contracts(fact_id)
                deadline = self.clock() + policy["timeout_seconds"]
                contract_hashes = {k: v for k, v in hashes.items() if k != "privacy_policy"}
                try:
                    raw, attempts = self._read_with_retry(fixture_file, policy, deadline)
                    source_state = {"fixture_sha256": sha256(raw)}
                    source_failure = None
                except RuntimeFailure as failure:
                    if failure.reason not in ("SOURCE_MISSING", "TIMEOUT", "RETRY_EXHAUSTED"):
                        raise
                    raw, attempts, source_failure = b"", failure.attempts, failure
                    source_state = {"source_failure": failure.reason}
                input_hash = sha256(canonical({**input_seed, **source_state, "contract_hashes": contract_hashes}))
                replay = self._replay(existing_path, input_hash)
                if replay: return replay
                if source_failure: raise source_failure
                try: fixture = json.loads(raw.decode("utf-8"))
                except Exception as exc: raise RuntimeFailure("QUALITY_FAILED", "fixture is invalid JSON") from exc
                result = self._evaluate(fact, source, fixture, role, hashes["privacy_policy"])
                snapshot = {"contract_version": "project-brain-snapshot.v1", "run_id": run_id, "fact_id": fact_id,
                            "authority_id": fact["authority_id"], "classification": fact["classification"],
                            "permitted_use": fact["permitted_use"], "definition": fact["business_definition"],
                            "captured_at": utc_now(), "input_hash": input_hash, "source_hash": sha256(raw),
                            "contract_hashes": contract_hashes, "result": result}
                snapshot_hash = self._immutable(self.paths.snapshots, snapshot)
                record = {"contract_version": "project-brain-run-record.v1", "run_id": run_id, "input_hash": input_hash,
                          "status": result["status"], "reason_code": result["reason_code"], "started_at": started,
                          "completed_at": utc_now(), "attempts": attempts, "snapshot_hash": snapshot_hash}
                self._immutable(existing_path, record)
                self._append(self.paths.audit, {"contract_version": "project-brain-audit-event.v1",
                             "event": "refresh", "actor": actor, "role": role, "fact_id": fact_id,
                             "authority_id": fact["authority_id"], "source_owner": fact["source_owner"],
                             "source_hash": sha256(raw), "definition_version": result["definition_version"],
                             "classification": fact["classification"], "freshness": result["checks"]["freshness"],
                             "quality": result["checks"]["quality"], "output_hash": snapshot_hash,
                             "run_record": record}, chained=True)
                if result["status"] == "Trusted": self._pointer(snapshot_hash, run_id)
                return record
            except RuntimeFailure as failure:
                raw = locals().get("raw", b"")
                input_hash = locals().get("input_hash", sha256(canonical({**input_seed, "fixture_sha256": sha256(raw)})))
                record = {"contract_version": "project-brain-run-record.v1", "run_id": run_id, "input_hash": input_hash,
                          "status": failure.status, "reason_code": failure.reason, "started_at": started,
                          "completed_at": utc_now(), "attempts": failure.attempts or locals().get("attempts", 0), "snapshot_hash": None}
                if failure.reason != "IDEMPOTENCY_CONFLICT" and not existing_path.exists(): self._immutable(existing_path, record)
                fact_context = locals().get("fact", {})
                fixture_context = locals().get("fixture", {})
                checks = fixture_context.get("checks", {}) if isinstance(fixture_context, dict) else {}
                escalation_owner = fact_context.get("source_owner", "project_brain_v2_owner")
                self._append(self.paths.audit, {"contract_version": "project-brain-audit-event.v1",
                             "event": "refresh_failed", "actor": actor, "role": role, "fact_id": fact_id,
                             "authority_id": fact_context.get("authority_id"), "source_owner": escalation_owner,
                             "source_hash": sha256(locals().get("raw", b"")) if locals().get("raw") else None,
                             "definition_version": fixture_context.get("definition_version"),
                             "classification": fact_context.get("classification"), "freshness": checks.get("freshness", "unknown"),
                             "quality": checks.get("quality", "unknown"), "output_hash": None,
                             "run_record": record}, chained=True)
                self._append(self.paths.alerts, {"contract_version": "project-brain-alert.v1", "run_id": run_id,
                             "severity": "critical" if failure.status == "No-Go" else "warning", "status": failure.status,
                             "reason_code": failure.reason, "escalation_owner": escalation_owner,
                             "created_at": utc_now(), "delivery": "evidence_only_not_sent"})
                return record

    def run(self, run_id: str, fact_id: str, fixture_path: str, role: str,
            actor: str = "project_brain_v2_runtime") -> dict[str, Any]:
        try:
            return self._run(run_id, fact_id, fixture_path, role, actor)
        except RuntimeFailure as failure:
            # A lock failure cannot safely extend the hash-chained audit because
            # another process owns it. Preserve an append-only alert instead.
            record = {"contract_version": "project-brain-run-record.v1", "run_id": run_id,
                      "input_hash": sha256(canonical({"fact_id": fact_id, "fixture_path": fixture_path,
                                                       "actor": actor, "role": role})),
                      "status": failure.status, "reason_code": failure.reason, "started_at": utc_now(),
                      "completed_at": utc_now(), "attempts": 0, "snapshot_hash": None}
            self._append(self.paths.alerts, {"contract_version": "project-brain-alert.v1", "run_id": run_id,
                         "severity": "critical", "status": failure.status, "reason_code": failure.reason,
                         "escalation_owner": "project_brain_v2_owner", "created_at": utc_now(),
                         "delivery": "evidence_only_not_sent"})
            return record

    def rollback(self, snapshot_hash: str, actor: str, reason: str, role: str = "release_owner") -> dict[str, Any]:
        with self._lock("rollback"):
            self.verify_run_history()
            self.verified_pointer()
            target = self.paths.snapshots / f"{snapshot_hash}.json"
            if not target.exists() or sha256(target.read_bytes()) != snapshot_hash:
                raise RuntimeFailure("TAMPER_DETECTED", "rollback target is missing or altered")
            event = {"contract_version": "project-brain-audit-event.v1", "event": "rollback", "actor": actor,
                     "role": role, "snapshot_hash": snapshot_hash, "reason": reason, "at": utc_now()}
            self._append(self.paths.audit, event, chained=True)
            self._pointer(snapshot_hash, "rollback", action="rollback")
            return event
