#!/usr/bin/env python3
"""Fail-closed current-state checks for the Health Manager project entry."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
README_PATH = ROOT / "docs/project-management/modules/health-manager/README.md"
REGISTRY_PATH = ROOT / "contracts/foundation/agent-collaboration.v1.json"

EXPECTED_R1_R5_WORK_ITEMS = {
    "AIW-20260713-HEALTH-R1-C1-ACCEPTANCE",
    "AIW-20260713-HEALTH-R1-CROSS-MODULE-FREEZE",
    "AIW-20260713-HEALTH-R2-DUAL-CHANNEL-RECORD-CONTRACTS",
    "AIW-20260713-HEALTH-R2-C1-ACCEPTANCE",
    "AIW-20260714-HEALTH-R3-LEARNING-CLUB-ENTRY-CONTRACTS",
    "AIW-20260714-HEALTH-R3-C1-ACCEPTANCE",
    "AIW-20260714-HEALTH-R4-DOCTOR-DIRECTORY-RECOMMENDATION-CONTRACTS",
    "AIW-20260714-HEALTH-R4-C1-ACCEPTANCE",
    "AIW-20260714-HEALTH-R5-CONSULTATION-SECOND-OPINION-MDT-CONTRACTS",
    "AIW-20260714-HEALTH-R5-C1-ACCEPTANCE",
}
REQUIRED_NO_GO = {
    "真实身份", "真实健康数据", "互联网诊疗", "诊断", "处方", "改药",
    "收费", "支付", "测试服部署", "生产", "不可逆操作",
}
STALE_CLAIMS = {
    "当前切片：`health-mvp90-m0`",
    "M0 是唯一 active",
    "M0：当前正式授权",
    "M1 及以后：No-Go",
    "M1及以后：No-Go",
}
PREMATURE_GO_CLAIMS = {
    "真实健康数据：Go",
    "互联网诊疗：Go",
    "诊断：Go",
    "收费：Go",
    "支付：Go",
    "测试服部署：Go",
    "生产：Go",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_current_state(readme: str, registry: dict[str, Any]) -> str | None:
    work_items = {item.get("work_id"): item for item in registry.get("work_items", [])}
    if not EXPECTED_R1_R5_WORK_ITEMS.issubset(work_items):
        return "HMREADME_R1_R5_WORK_ITEM_MISSING"
    if any(work_items[work_id].get("status") != "integrated" for work_id in EXPECTED_R1_R5_WORK_ITEMS):
        return "HMREADME_R1_R5_NOT_INTEGRATED"

    if "R1—R5" not in readme or "共 10 个" not in readme or "已受控集成" not in readme:
        return "HMREADME_INTEGRATED_SUMMARY_MISSING"
    if "`synthetic_only=true`" not in readme:
        return "HMREADME_SYNTHETIC_BOUNDARY_MISSING"
    if "`executable=false`" not in readme:
        return "HMREADME_EXECUTION_BOUNDARY_MISSING"
    if "健康 active 工作项" not in readme or "agent-collaboration.v1.json" not in readme or "本页不固定数量" not in readme:
        return "HMREADME_ACTIVE_AUTHORITY_MISSING"
    if any(claim in readme for claim in STALE_CLAIMS):
        return "HMREADME_STALE_M0_CLAIM"
    if any(claim in readme for claim in PREMATURE_GO_CLAIMS):
        return "HMREADME_PREMATURE_REAL_WORLD_GO"
    if any(label not in readme for label in REQUIRED_NO_GO):
        return "HMREADME_NO_GO_BOUNDARY_MISSING"
    if "integrated` 只证明" not in readme or "它不等于真实医疗" not in readme:
        return "HMREADME_INTEGRATION_MEANING_MISSING"
    return None


class HealthManagerReadmeCurrentStateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.readme = README_PATH.read_text(encoding="utf-8")
        cls.registry = load_json(REGISTRY_PATH)

    def test_01_current_repository_state_passes(self) -> None:
        self.assertIsNone(validate_current_state(self.readme, copy.deepcopy(self.registry)))

    def test_02_exact_r1_r5_evidence_set_is_integrated(self) -> None:
        work_items = {item["work_id"]: item for item in self.registry["work_items"]}
        self.assertEqual(10, len(EXPECTED_R1_R5_WORK_ITEMS))
        self.assertTrue(EXPECTED_R1_R5_WORK_ITEMS.issubset(work_items))
        self.assertEqual({"integrated"}, {work_items[item]["status"] for item in EXPECTED_R1_R5_WORK_ITEMS})

    def test_03_negative_registry_stage_reopened(self) -> None:
        mutated = copy.deepcopy(self.registry)
        target = next(item for item in mutated["work_items"] if item["work_id"] in EXPECTED_R1_R5_WORK_ITEMS)
        target["status"] = "active"
        self.assertEqual("HMREADME_R1_R5_NOT_INTEGRATED", validate_current_state(self.readme, mutated))

    def test_04_negative_stale_m0_unique_active_claim(self) -> None:
        mutated = self.readme + "\n当前切片：`health-mvp90-m0`\n"
        self.assertEqual("HMREADME_STALE_M0_CLAIM", validate_current_state(mutated, copy.deepcopy(self.registry)))

    def test_05_negative_synthetic_boundary_removed(self) -> None:
        mutated = self.readme.replace("`synthetic_only=true`", "`synthetic_only=false`")
        self.assertEqual("HMREADME_SYNTHETIC_BOUNDARY_MISSING", validate_current_state(mutated, copy.deepcopy(self.registry)))

    def test_06_negative_executable_boundary_removed(self) -> None:
        mutated = self.readme.replace("`executable=false`", "`executable=true`")
        self.assertEqual("HMREADME_EXECUTION_BOUNDARY_MISSING", validate_current_state(mutated, copy.deepcopy(self.registry)))

    def test_07_negative_registry_authority_removed(self) -> None:
        mutated = self.readme.replace("本页不固定数量", "本页固定一个 active 工作项")
        self.assertEqual("HMREADME_ACTIVE_AUTHORITY_MISSING", validate_current_state(mutated, copy.deepcopy(self.registry)))

    def test_08_negative_real_health_data_promoted_to_go(self) -> None:
        mutated = self.readme + "\n- 真实健康数据：Go\n"
        self.assertEqual("HMREADME_PREMATURE_REAL_WORLD_GO", validate_current_state(mutated, copy.deepcopy(self.registry)))

    def test_09_negative_no_go_boundary_removed(self) -> None:
        mutated = self.readme.replace("不可逆操作", "高风险操作")
        self.assertEqual("HMREADME_NO_GO_BOUNDARY_MISSING", validate_current_state(mutated, copy.deepcopy(self.registry)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
