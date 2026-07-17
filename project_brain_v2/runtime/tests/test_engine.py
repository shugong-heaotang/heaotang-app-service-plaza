from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from jsonschema import Draft202012Validator
from project_brain_v2.runtime.engine import RefreshEngine, RuntimeFailure, TransientSourceError, sha256
from project_brain_v2.runtime.scheduler import OfflineScheduler


FIXTURE = "contracts/project-brain/v2/examples/trusted-g1-synthetic.json"
FACT = "synthetic.operations.completed_services.count"
ROLE = "project_brain_reviewer"


class RuntimeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.repo = root / "repo"
        self.state = root / "state"
        source = Path(__file__).resolve().parents[3] / "contracts/project-brain/v2"
        target = self.repo / "contracts/project-brain/v2"
        target.parent.mkdir(parents=True)
        shutil.copytree(source, target)
        self.policy = root / "policy.json"
        self.write_policy()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_policy(self, **overrides) -> None:
        policy = {
            "contract_version": "project-brain-runtime-policy.v1", "enabled": True,
            "production_enabled": False, "network_enabled": False, "real_sources_enabled": False,
            "source_writes_enabled": False, "external_notifications_enabled": False,
            "max_attempts": 3, "timeout_seconds": 10, "max_source_bytes": 1048576,
            "schedule_interval_seconds": 3600,
            "allowed_fixtures": [FIXTURE],
        }
        policy.update(overrides)
        self.policy.write_text(json.dumps(policy), encoding="utf-8")

    def engine(self, **kwargs) -> RefreshEngine:
        return RefreshEngine(self.repo, self.state, self.policy, **kwargs)

    def fixture_json(self, relative: str = FIXTURE) -> dict:
        return json.loads((self.repo / relative).read_text(encoding="utf-8"))

    def write_fixture(self, value: dict, relative: str = FIXTURE) -> None:
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")

    def execute(self, run_id="run-1", **kwargs):
        return self.engine(**kwargs).run(run_id, FACT, FIXTURE, ROLE)

    def test_trusted_run_creates_content_addressed_snapshot_pointer_and_audit(self):
        record = self.execute()
        self.assertEqual("Trusted", record["status"])
        snapshot = self.state / "snapshots" / f'{record["snapshot_hash"]}.json'
        self.assertEqual(record["snapshot_hash"], sha256(snapshot.read_bytes()))
        pointer = json.loads((self.state / "last-trusted.json").read_text(encoding="utf-8"))
        self.assertEqual(record["snapshot_hash"], pointer["snapshot_hash"])
        self.assertEqual(1, self.engine().verify_audit())
        audit = json.loads((self.state / "audit.jsonl").read_text(encoding="utf-8"))
        self.assertEqual(FACT, audit["fact_id"])
        self.assertEqual("authority.synthetic.completed_services_fixture", audit["authority_id"])
        self.assertEqual("v1", audit["definition_version"])
        self.assertEqual("G1", audit["classification"])
        self.assertEqual("pass", audit["freshness"])
        self.assertEqual("pass", audit["quality"])
        self.assertEqual(record["snapshot_hash"], audit["output_hash"])

    def test_idempotent_replay_does_not_append_a_second_audit(self):
        first = self.execute()
        second = self.execute()
        self.assertEqual(first, second)
        self.assertEqual(1, self.engine().verify_audit())

    def test_same_run_id_with_changed_input_is_no_go_and_preserves_record(self):
        first = self.execute()
        fixture = self.fixture_json(); fixture["value"] = 125; self.write_fixture(fixture)
        conflict = self.execute()
        self.assertEqual("IDEMPOTENCY_CONFLICT", conflict["reason_code"])
        stored = json.loads((self.state / "runs/run-1.json").read_text(encoding="utf-8"))
        self.assertEqual(first, stored)

    def test_existing_lock_fails_closed_and_appends_alert_only(self):
        self.state.mkdir(parents=True); (self.state / "refresh.lock").write_text("owned", encoding="utf-8")
        record = self.execute()
        self.assertEqual("LOCKED", record["reason_code"])
        self.assertFalse((self.state / "audit.jsonl").exists())
        self.assertIn('"reason_code":"LOCKED"', (self.state / "alerts.jsonl").read_text(encoding="utf-8"))
        self.assertIn('"escalation_owner":"project_brain_v2_owner"', (self.state / "alerts.jsonl").read_text(encoding="utf-8"))

    def test_transient_source_retries_are_bounded_and_success_is_attempt_three(self):
        calls = []
        def reader(path, maximum):
            calls.append(1)
            if len(calls) < 3: raise TransientSourceError("try again")
            return path.read_bytes()
        record = self.execute(reader=reader)
        self.assertEqual("Trusted", record["status"])
        self.assertEqual(3, record["attempts"])
        self.assertEqual(3, len(calls))

    def test_retry_exhaustion_is_no_go_without_pointer(self):
        calls = []
        def reader(path, maximum): calls.append(1); raise TransientSourceError("down")
        record = self.execute(reader=reader)
        self.assertEqual("RETRY_EXHAUSTED", record["reason_code"])
        self.assertEqual(3, len(calls))
        self.assertFalse((self.state / "last-trusted.json").exists())

    def test_deadline_is_checked_after_source_read(self):
        ticks = [0.0]
        def clock(): return ticks[0]
        def reader(path, maximum): ticks[0] = 2.0; return path.read_bytes()
        self.write_policy(timeout_seconds=1)
        record = self.execute(reader=reader, clock=clock)
        self.assertEqual("TIMEOUT", record["reason_code"])

    def test_disabled_policy_is_no_go_and_emits_no_snapshot(self):
        self.write_policy(enabled=False)
        record = self.execute()
        self.assertEqual("RUNTIME_DISABLED", record["reason_code"])
        self.assertEqual([], list((self.state / "snapshots").glob("*.json")))

    def test_missing_allowlisted_fixture_is_unknown(self):
        missing = "contracts/project-brain/v2/examples/missing.json"
        self.write_policy(allowed_fixtures=[missing])
        record = self.engine().run("missing", FACT, missing, ROLE)
        self.assertEqual("Unknown", record["status"])
        self.assertEqual("SOURCE_MISSING", record["reason_code"])
        replay = self.engine().run("missing", FACT, missing, ROLE)
        self.assertEqual(record, replay)
        self.assertEqual(1, self.engine().verify_audit())

    def test_stale_fixture_is_unknown(self):
        stale = "contracts/project-brain/v2/examples/unknown-stale.json"
        self.write_policy(allowed_fixtures=[stale])
        record = self.engine().run("stale", "governance.work_items.status_counts", stale, ROLE)
        self.assertEqual("Unknown", record["status"])
        self.assertEqual("SOURCE_STALE", record["reason_code"])

    def test_unauthorized_role_is_no_go(self):
        record = self.engine().run("role", FACT, FIXTURE, "project_owner")
        self.assertEqual("UNAUTHORIZED", record["reason_code"])

    def test_authority_conflict_is_no_go(self):
        fixture = self.fixture_json(); fixture["authority_id"] = "authority.other"; self.write_fixture(fixture)
        self.assertEqual("AUTHORITY_CONFLICT", self.execute()["reason_code"])

    def test_high_risk_small_sample_is_no_go(self):
        fixture = self.fixture_json(); fixture["sample_size"] = 45; self.write_fixture(fixture)
        self.assertEqual("PRIVACY_THRESHOLD_FAILED", self.execute()["reason_code"])

    def test_failure_does_not_overwrite_last_trusted_pointer(self):
        trusted = self.execute("trusted")
        pointer_before = (self.state / "last-trusted.json").read_bytes()
        failure = self.engine().run("failure", FACT, FIXTURE, "project_owner")
        self.assertEqual("No-Go", failure["status"])
        self.assertEqual(pointer_before, (self.state / "last-trusted.json").read_bytes())
        self.assertEqual(trusted["snapshot_hash"], json.loads(pointer_before)["snapshot_hash"])

    def test_snapshot_tamper_is_detected_on_replay(self):
        record = self.execute()
        snapshot = self.state / "snapshots" / f'{record["snapshot_hash"]}.json'
        snapshot.write_bytes(snapshot.read_bytes() + b" ")
        replay = self.execute()
        self.assertEqual("TAMPER_DETECTED", replay["reason_code"])

    def test_run_record_tamper_is_detected_against_audit(self):
        self.execute()
        path = self.state / "runs/run-1.json"
        record = json.loads(path.read_text(encoding="utf-8")); record["status"] = "No-Go"
        path.write_text(json.dumps(record), encoding="utf-8")
        self.assertEqual("TAMPER_DETECTED", self.execute()["reason_code"])

    def test_pointer_tamper_blocks_next_refresh_without_overwrite(self):
        self.execute("first")
        pointer = self.state / "last-trusted.json"
        pointer.write_text('{"snapshot_hash":"' + ('0' * 64) + '"}', encoding="utf-8")
        before = pointer.read_bytes()
        failed = self.execute("second")
        self.assertEqual("TAMPER_DETECTED", failed["reason_code"])
        self.assertEqual(before, pointer.read_bytes())

    def test_audit_tamper_breaks_chain(self):
        self.execute()
        audit = self.state / "audit.jsonl"
        audit.write_bytes(audit.read_bytes().replace(b'"event":"refresh"', b'"event":"changed"', 1))
        with self.assertRaisesRegex(RuntimeFailure, "audit hash chain"):
            self.engine().verify_audit()

    def test_rollback_moves_only_pointer_to_verified_prior_snapshot(self):
        first = self.execute("first")
        second = self.execute("second")
        first_bytes = (self.state / "snapshots" / f'{first["snapshot_hash"]}.json').read_bytes()
        second_bytes = (self.state / "snapshots" / f'{second["snapshot_hash"]}.json').read_bytes()
        self.engine().rollback(first["snapshot_hash"], "release_owner", "drill")
        pointer = json.loads((self.state / "last-trusted.json").read_text(encoding="utf-8"))
        self.assertEqual(first["snapshot_hash"], pointer["snapshot_hash"])
        self.assertEqual(first_bytes, (self.state / "snapshots" / f'{first["snapshot_hash"]}.json').read_bytes())
        self.assertEqual(second_bytes, (self.state / "snapshots" / f'{second["snapshot_hash"]}.json').read_bytes())
        self.assertEqual(3, self.engine().verify_audit())

    def test_rollback_rejects_missing_or_tampered_snapshot(self):
        with self.assertRaises(RuntimeFailure): self.engine().rollback("0" * 64, "owner", "drill")

    def test_any_production_capability_switch_is_policy_no_go(self):
        for switch in ("production_enabled", "network_enabled", "real_sources_enabled", "source_writes_enabled", "external_notifications_enabled"):
            with self.subTest(switch=switch):
                shutil.rmtree(self.state, ignore_errors=True)
                self.write_policy(**{switch: True})
                self.assertEqual("POLICY_INVALID", self.execute()["reason_code"])

    def test_path_traversal_is_unauthorized_even_if_allowlisted(self):
        escaped = "contracts/project-brain/v2/examples/../../fact-catalog.v1.json"
        self.write_policy(allowed_fixtures=[escaped])
        record = self.engine().run("escape", FACT, escaped, ROLE)
        self.assertEqual("UNAUTHORIZED", record["reason_code"])

    def test_m1_runtime_enablement_is_rejected_not_overridden(self):
        path = self.repo / "contracts/project-brain/v2/source-map.v1.json"
        source_map = json.loads(path.read_text(encoding="utf-8"))
        source_map["sources"][2]["runtime_enabled"] = True
        path.write_text(json.dumps(source_map), encoding="utf-8")
        self.assertEqual("POLICY_INVALID", self.execute()["reason_code"])

    def test_scheduler_first_tick_is_due_and_later_tick_waits_for_interval(self):
        scheduler = OfflineScheduler(self.engine())
        now = datetime.now(timezone.utc)
        first = scheduler.tick(now, "scheduled-1", FACT, FIXTURE, ROLE)
        self.assertTrue(first["schedule"]["due"])
        self.assertEqual("Trusted", first["run"]["status"])
        last = datetime.fromisoformat(first["run"]["completed_at"].replace("Z", "+00:00"))
        waiting = scheduler.tick(last + timedelta(seconds=3599), "scheduled-2", FACT, FIXTURE, ROLE)
        self.assertFalse(waiting["schedule"]["due"])
        self.assertIsNone(waiting["run"])
        self.assertFalse(waiting["schedule"]["production_timer_present"])

    def test_scheduler_rejects_tampered_run_history(self):
        self.execute()
        path = self.state / "runs/run-1.json"
        record = json.loads(path.read_text(encoding="utf-8")); record["completed_at"] = "2099-01-01T00:00:00Z"
        path.write_text(json.dumps(record), encoding="utf-8")
        with self.assertRaises(RuntimeFailure):
            OfflineScheduler(self.engine()).decision(datetime.now(timezone.utc))

    def test_generated_runtime_artifacts_match_contract_schemas(self):
        trusted = self.execute("schema-success")
        self.engine().run("schema-alert", FACT, FIXTURE, "project_owner")
        base = self.repo / "contracts/project-brain/v2/runtime"
        def validate(name, value):
            schema = json.loads((base / name).read_text(encoding="utf-8"))
            Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER).validate(value)
        validate("run-record.v1.schema.json", trusted)
        snapshot = json.loads((self.state / "snapshots" / f'{trusted["snapshot_hash"]}.json').read_text(encoding="utf-8"))
        validate("snapshot.v1.schema.json", snapshot)
        alert = json.loads((self.state / "alerts.jsonl").read_text(encoding="utf-8").splitlines()[-1])
        validate("alert.v1.schema.json", alert)
        decision = OfflineScheduler(self.engine()).decision(datetime.now(timezone.utc))
        validate("schedule-decision.v1.schema.json", decision)


if __name__ == "__main__": unittest.main()
