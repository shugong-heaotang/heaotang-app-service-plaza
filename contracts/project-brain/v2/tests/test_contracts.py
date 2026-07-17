from __future__ import annotations

import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

from validate_contracts import ContractError, load_json, validate_package, validate_result  # noqa: E402


class ProjectBrainV2ContractsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.policy = load_json(PACKAGE_ROOT / "privacy-threshold-policy.v1.json")
        catalog = load_json(PACKAGE_ROOT / "fact-catalog.v1.json")
        source_map = load_json(PACKAGE_ROOT / "source-map.v1.json")
        cls.facts = {item["fact_id"]: item for item in catalog["facts"]}
        cls.sources = {item["fact_id"]: item for item in source_map["sources"]}

    def test_full_package(self) -> None:
        self.assertEqual(validate_package(), {"facts": 3, "sources": 3, "positive": 7, "negative": 10})

    def test_unknown_must_not_carry_value(self) -> None:
        result = load_json(PACKAGE_ROOT / "examples" / "unknown-stale.json")
        result["value"] = 1
        with self.assertRaisesRegex(ContractError, "FAIL_CLOSED_VALUE_REQUIRED_NULL"):
            validate_result(result, self.facts, self.sources, self.policy)

    def test_g1_threshold_is_versioned_and_enforced(self) -> None:
        result = load_json(PACKAGE_ROOT / "examples" / "trusted-g1-synthetic.json")
        self.assertEqual(self.facts[result["fact_id"]]["privacy_risk_tier"], "high")
        result["sample_size"] = self.policy["rules"]["high_risk_minimum_group_size"] - 1
        with self.assertRaisesRegex(ContractError, "PRIVACY_THRESHOLD_FAILED"):
            validate_result(result, self.facts, self.sources, self.policy)

    def test_high_risk_threshold_does_not_fall_back_to_standard(self) -> None:
        result = load_json(PACKAGE_ROOT / "examples" / "trusted-g1-synthetic.json")
        result["sample_size"] = self.policy["rules"]["standard_minimum_group_size"] + 5
        with self.assertRaisesRegex(ContractError, "PRIVACY_THRESHOLD_FAILED"):
            validate_result(result, self.facts, self.sources, self.policy)

    def test_fail_closed_small_sample_no_go_is_valid(self) -> None:
        result = load_json(PACKAGE_ROOT / "examples" / "no-go-small-sample.json")
        validate_result(result, self.facts, self.sources, self.policy)

    def test_freshness_is_recomputed_from_timestamps(self) -> None:
        result = load_json(PACKAGE_ROOT / "examples" / "trusted-g0-synthetic.json")
        result["observed_at"] = "2020-01-01T00:00:00Z"
        with self.assertRaisesRegex(ContractError, "FRESHNESS_ASSERTION_MISMATCH"):
            validate_result(result, self.facts, self.sources, self.policy)

    def test_timestamp_timezone_is_mandatory(self) -> None:
        result = load_json(PACKAGE_ROOT / "examples" / "trusted-g0-synthetic.json")
        result["evaluated_at"] = "2026-07-17T12:00:00"
        with self.assertRaisesRegex(ContractError, "TIMESTAMP_TIMEZONE_REQUIRED"):
            validate_result(result, self.facts, self.sources, self.policy)

    def test_window_must_not_be_reversed(self) -> None:
        result = load_json(PACKAGE_ROOT / "examples" / "trusted-g0-synthetic.json")
        result["window_start"] = "2026-07-17T01:00:00Z"
        result["window_end"] = "2026-07-17T00:00:00Z"
        with self.assertRaisesRegex(ContractError, "TIME_WINDOW_INVALID"):
            validate_result(result, self.facts, self.sources, self.policy)

    def test_missing_source_unknown_is_valid(self) -> None:
        result = load_json(PACKAGE_ROOT / "examples" / "unknown-source-missing.json")
        validate_result(result, self.facts, self.sources, self.policy)

    def test_unauthorized_no_go_is_valid(self) -> None:
        result = load_json(PACKAGE_ROOT / "examples" / "no-go-unauthorized.json")
        validate_result(result, self.facts, self.sources, self.policy)

    def test_authority_conflict_no_go_is_valid(self) -> None:
        result = load_json(PACKAGE_ROOT / "examples" / "no-go-authority-conflict.json")
        validate_result(result, self.facts, self.sources, self.policy)

    def test_g1_object_values_cannot_bypass_rounding(self) -> None:
        result = load_json(PACKAGE_ROOT / "examples" / "trusted-g1-synthetic.json")
        result["value"] = {"category_a": 25, "category_b": 21}
        with self.assertRaisesRegex(ContractError, "ROUNDING_POLICY_FAILED"):
            validate_result(result, self.facts, self.sources, self.policy)

    def test_g1_cannot_be_relabelled_real(self) -> None:
        result = load_json(PACKAGE_ROOT / "examples" / "trusted-g1-synthetic.json")
        result["synthetic"] = False
        with self.assertRaisesRegex(ContractError, "SYNTHETIC_PROVENANCE_REQUIRED"):
            validate_result(result, self.facts, self.sources, self.policy)

    def test_authority_conflict_fails_closed(self) -> None:
        result = load_json(PACKAGE_ROOT / "examples" / "trusted-g0-synthetic.json")
        result["checks"]["authority_conflict"] = True
        with self.assertRaisesRegex(ContractError, "AUTHORITY_CONFLICT"):
            validate_result(result, self.facts, self.sources, self.policy)

    def test_write_path_is_absent_from_all_contracts(self) -> None:
        for path in PACKAGE_ROOT.rglob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            text = json.dumps(data, ensure_ascii=False)
            if path.parent.name != "negative":
                self.assertNotIn('"write_capability": "update"', text)
                self.assertNotIn('"read_mode": "read_write"', text)


if __name__ == "__main__":
    unittest.main()
