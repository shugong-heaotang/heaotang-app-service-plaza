from __future__ import annotations

import json
import unittest

from project_brain_v2.dashboard.errors import DashboardFailure
from project_brain_v2.dashboard.policy import DashboardPolicy
from project_brain_v2.dashboard.reader import DashboardReader, canonical, sha256
from project_brain_v2.dashboard.tests._support import DashboardTestCase, G0_FACT, G1_FACT, G1_FIXTURE


class DashboardReaderTests(DashboardTestCase):
    def state_bytes(self):
        return {str(path.relative_to(self.state)): path.read_bytes() for path in self.state.rglob("*") if path.is_file()}

    def rewrite_single_trusted_chain(self, mutate):
        record = self.run_g1()
        old_hash = record["snapshot_hash"]
        old_path = self.state / "snapshots" / f"{old_hash}.json"
        snapshot = json.loads(old_path.read_text(encoding="utf-8"))
        mutate(snapshot)
        new_raw = canonical(snapshot)
        new_hash = sha256(new_raw)
        old_path.unlink()
        (self.state / "snapshots" / f"{new_hash}.json").write_bytes(new_raw)
        record["snapshot_hash"] = new_hash
        (self.state / "runs/g1.json").write_bytes(canonical(record))
        event = json.loads((self.state / "audit.jsonl").read_text(encoding="utf-8"))
        event["output_hash"] = new_hash
        event["run_record"] = record
        unsigned = {key: value for key, value in event.items() if key != "entry_hash"}
        event["entry_hash"] = sha256(canonical(unsigned))
        (self.state / "audit.jsonl").write_bytes(canonical(event))
        pointer = json.loads((self.state / "last-trusted.json").read_text(encoding="utf-8"))
        pointer["snapshot_hash"] = new_hash
        (self.state / "last-trusted.json").write_bytes(canonical(pointer))

    def test_unobserved_authorized_facts_are_explicit_unknown(self):
        overview = self.reader().overview(["project_owner"])
        self.assertEqual(2, len(overview["facts"]))
        self.assertEqual({"Trusted": 0, "Unknown": 2, "No-Go": 0}, overview["status_counts"])
        self.assertTrue(all(card["reason_code"] == "SOURCE_NOT_REFRESHED" for card in overview["facts"]))
        self.assertIsNone(overview["as_of"])

    def test_integrated_m2_g0_remediation_is_visible_as_trusted(self):
        record = self.run_g0("g0-remediation-proof")
        self.assertEqual("Trusted", record["status"])
        self.assertEqual("SYNTHETIC_CONTRACT_FIXTURE", record["reason_code"])
        self.assertIsNotNone(record["snapshot_hash"])
        overview = self.reader().overview(["project_brain_reviewer"])
        card = next(item for item in overview["facts"] if item["fact_id"] == G0_FACT)
        self.assertEqual("Trusted", card["status"])
        self.assertEqual(record["snapshot_hash"], card["evidence"]["snapshot_hash"])

    def test_trusted_g1_snapshot_is_verified_and_explained(self):
        record = self.run_g1()
        overview = self.reader().overview(["project_brain_reviewer"])
        card = next(item for item in overview["facts"] if item["fact_id"] == G1_FACT)
        self.assertEqual("Trusted", card["status"])
        self.assertEqual(120, card["value"])
        self.assertEqual(record["snapshot_hash"], card["evidence"]["snapshot_hash"])
        self.assertFalse(card["decision_usable"])
        self.assertTrue(card["synthetic"])

    def test_reviewer_sees_g1_but_project_owner_does_not(self):
        self.run_g1()
        reviewer_ids = {item["fact_id"] for item in self.reader().overview(["project_brain_reviewer"])["facts"]}
        owner_ids = {item["fact_id"] for item in self.reader().overview(["project_owner"])["facts"]}
        self.assertEqual(3, len(reviewer_ids))
        self.assertNotIn("synthetic.operations.completed_services.count", owner_ids)

    def test_latest_no_go_preserves_but_marks_last_trusted_stale(self):
        trusted = self.run_g1("trusted")
        failed = self.engine.run("denied", G1_FACT, G1_FIXTURE, "ordinary_member", actor="m3-test-runtime")
        self.assertEqual("No-Go", failed["status"])
        card = next(item for item in self.reader().overview(["project_brain_reviewer"])["facts"] if item["fact_id"] == G1_FACT)
        self.assertEqual("No-Go", card["status"])
        self.assertEqual("UNAUTHORIZED", card["reason_code"])
        self.assertTrue(card["stale"])
        self.assertTrue(card["last_trusted"])
        self.assertEqual(trusted["snapshot_hash"], card["evidence"]["last_trusted_snapshot_hash"])
        self.assertIsNone(card["evidence"]["snapshot_hash"])

    def test_latest_unknown_preserves_but_marks_last_trusted_stale(self):
        self.run_g1("trusted")
        missing_fixture = "contracts/project-brain/v2/examples/missing-for-m3-test.json"
        failed = self.engine.run("missing", G1_FACT, missing_fixture, "project_brain_reviewer", actor="m3-test-runtime")
        self.assertEqual("Unknown", failed["status"])
        card = next(item for item in self.reader().overview(["project_brain_reviewer"])["facts"] if item["fact_id"] == G1_FACT)
        self.assertEqual("Unknown", card["status"])
        self.assertEqual("SOURCE_MISSING", card["reason_code"])
        self.assertTrue(card["stale"])

    def test_reader_does_not_change_state(self):
        self.run_g1()
        before = self.state_bytes()
        self.reader().overview(["project_brain_reviewer"])
        self.assertEqual(before, self.state_bytes())

    def test_audit_tamper_is_rejected(self):
        self.run_g1()
        audit = self.state / "audit.jsonl"
        audit.write_bytes(audit.read_bytes().replace(b'"event":"refresh"', b'"event":"changed"'))
        with self.assertRaisesRegex(DashboardFailure, "TAMPER_DETECTED"):
            self.reader().overview(["project_brain_reviewer"])

    def test_snapshot_tamper_is_rejected(self):
        record = self.run_g1()
        snapshot = self.state / "snapshots" / f'{record["snapshot_hash"]}.json'
        snapshot.write_bytes(snapshot.read_bytes() + b" ")
        with self.assertRaisesRegex(DashboardFailure, "TAMPER_DETECTED"):
            self.reader().overview(["project_brain_reviewer"])

    def test_run_record_tamper_is_rejected(self):
        self.run_g1()
        run = self.state / "runs/g1.json"
        value = json.loads(run.read_text(encoding="utf-8"))
        value["status"] = "No-Go"
        run.write_bytes(canonical(value))
        with self.assertRaisesRegex(DashboardFailure, "TAMPER_DETECTED"):
            self.reader().overview(["project_brain_reviewer"])

    def test_pointer_cannot_be_silently_moved_to_older_snapshot(self):
        first = self.run_g1("first")
        self.run_g1("second")
        pointer = {"snapshot_hash": first["snapshot_hash"], "run_id": "first", "updated_at": "2026-07-17T00:00:00Z", "action": "advance"}
        (self.state / "last-trusted.json").write_bytes(canonical(pointer))
        with self.assertRaisesRegex(DashboardFailure, "TAMPER_DETECTED"):
            self.reader().overview(["project_brain_reviewer"])

    def test_unexpected_state_file_is_rejected(self):
        self.run_g1()
        (self.state / "runs/extra.txt").write_text("x", encoding="utf-8")
        with self.assertRaisesRegex(DashboardFailure, "TAMPER_DETECTED"):
            self.reader().overview(["project_brain_reviewer"])

    def test_unsafe_aggregate_bucket_is_rejected(self):
        facts, _, privacy, _ = self.reader()._contracts()
        result = {"synthetic": True, "decision_usable": False, "value": {"member_id": 1}}
        with self.assertRaisesRegex(DashboardFailure, "PRIVACY_THRESHOLD_FAILED"):
            self.reader()._safe_value(facts[G0_FACT], result, privacy)

    def test_rehashed_definition_drift_is_rejected(self):
        self.rewrite_single_trusted_chain(lambda snapshot: snapshot.__setitem__("definition", "changed definition"))
        with self.assertRaisesRegex(DashboardFailure, "TAMPER_DETECTED"):
            self.reader().overview(["project_brain_reviewer"])

    def test_rehashed_g1_small_sample_is_rejected(self):
        self.rewrite_single_trusted_chain(lambda snapshot: snapshot["result"].__setitem__("sample_size", 25))
        with self.assertRaisesRegex(DashboardFailure, "PRIVACY_THRESHOLD_FAILED"):
            self.reader().overview(["project_brain_reviewer"])

    def assert_rehashed_g1_unrounded_value_is_rejected(self, value):
        self.rewrite_single_trusted_chain(
            lambda snapshot: snapshot["result"].__setitem__("value", value)
        )
        with self.assertRaisesRegex(DashboardFailure, "ROUNDING_POLICY_FAILED"):
            self.reader().overview(["project_brain_reviewer"])

    def test_rehashed_g1_value_121_is_rejected(self):
        self.assert_rehashed_g1_unrounded_value_is_rejected(121)

    def test_rehashed_g1_value_119_is_rejected(self):
        self.assert_rehashed_g1_unrounded_value_is_rejected(119)

    def test_rehashed_g1_value_120_point_5_is_rejected(self):
        self.assert_rehashed_g1_unrounded_value_is_rejected(120.5)

    def test_g1_unrounded_bucket_value_is_rejected(self):
        facts, _, privacy, _ = self.reader()._contracts()
        result = {"synthetic": True, "decision_usable": False, "value": {"safe_bucket": 121}}
        with self.assertRaisesRegex(DashboardFailure, "ROUNDING_POLICY_FAILED"):
            self.reader()._safe_value(facts[G1_FACT], result, privacy)

    def test_rehashed_forbidden_dimension_value_is_rejected(self):
        self.rewrite_single_trusted_chain(lambda snapshot: snapshot["result"].__setitem__("value", {"member_id": 1}))
        with self.assertRaisesRegex(DashboardFailure, "PRIVACY_THRESHOLD_FAILED"):
            self.reader().overview(["project_brain_reviewer"])

    def test_rehashed_row_level_structure_is_rejected(self):
        self.rewrite_single_trusted_chain(lambda snapshot: snapshot["result"].__setitem__("value", [{"member_id": "m1"}]))
        with self.assertRaisesRegex(DashboardFailure, "TAMPER_DETECTED"):
            self.reader().overview(["project_brain_reviewer"])

    def test_non_synthetic_or_decision_usable_value_is_rejected(self):
        facts, _, privacy, _ = self.reader()._contracts()
        for result in (
            {"synthetic": False, "decision_usable": False, "value": 1},
            {"synthetic": True, "decision_usable": True, "value": 1},
        ):
            with self.subTest(result=result):
                with self.assertRaisesRegex(DashboardFailure, "UNAUTHORIZED"):
                    self.reader()._safe_value(facts[G0_FACT], result, privacy)

    def test_default_disabled_policy_is_not_queryable(self):
        raw = json.loads((self.repo / "contracts/project-brain/v2/dashboard/dashboard-policy.disabled.v1.json").read_text(encoding="utf-8"))
        disabled = DashboardPolicy.from_mapping(self.repo, raw)
        with self.assertRaisesRegex(DashboardFailure, "DASHBOARD_DISABLED"):
            self.reader(disabled).overview(["project_owner"])

    def test_state_root_may_not_overlap_repository(self):
        with self.assertRaisesRegex(DashboardFailure, "STATE_INVALID"):
            DashboardReader(self.repo, self.repo, self.policy)


if __name__ == "__main__":
    unittest.main()
