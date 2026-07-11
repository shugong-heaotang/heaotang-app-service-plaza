#!/usr/bin/env python3
"""Generate deterministic, obviously synthetic MVP-90 fixtures."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
MODULE = HERE.parents[1]
SCENARIOS_PATH = MODULE / "synthetic-scenarios.v1.json"
OUTPUT_PATH = HERE / "mvp90-synthetic-fixtures.v1.json"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def token(seed: str, scenario_id: str, purpose: str) -> str:
    return hashlib.sha256(f"{seed}|{scenario_id}|{purpose}".encode("utf-8")).hexdigest()[:16]


def trigger_code(scenario_id: str) -> str:
    return "SYNTHETIC_" + scenario_id.replace("MVP-", "").replace("-", "_")


def build_bundle() -> dict[str, Any]:
    scenarios = json.loads(SCENARIOS_PATH.read_text(encoding="utf-8"))
    generator = scenarios["generator"]
    seed = generator["seed"]
    fixtures = []
    for scenario in scenarios["scenarios"]:
        scenario_id = scenario["scenario_id"]
        fixture = {
            "scenario_id": scenario_id,
            "fixture_id": scenario["fixture_id"],
            "synthetic": True,
            "environment": "non-production",
            "generator_version": "heaotang-deterministic-fixture-v1",
            "seed": seed,
            "destruction_policy": generator["destruction_policy"],
            "inputs": {
                "synthetic_member_ref": f"SYN-MEMBER-{token(seed, scenario_id, 'member')}",
                "synthetic_object_ref": f"SYN-OBJECT-{token(seed, scenario_id, 'object')}",
                "synthetic_correlation_id": f"SYN-CORR-{token(seed, scenario_id, 'correlation')}",
                "trigger_code": trigger_code(scenario_id),
                "display_marker": "合成验收数据",
            },
            "expected_outcomes": scenario["expected_outcomes"],
            "forbidden_outcomes": scenario["forbidden_outcomes"],
        }
        fixture["canonical_sha256"] = hashlib.sha256(canonical_bytes(fixture)).hexdigest()
        fixtures.append(fixture)
    return {
        "contract_version": "health-manager.mvp90.synthetic-fixtures.v1",
        "generator": {
            "generator_id": generator["generator_id"],
            "version": generator["version"],
            "algorithm": generator["algorithm"],
            "seed": seed,
        },
        "fixtures": fixtures,
    }


def main() -> int:
    content = json.dumps(build_bundle(), ensure_ascii=False, indent=2) + "\n"
    OUTPUT_PATH.write_text(content, encoding="utf-8", newline="\n")
    print(f"generated {OUTPUT_PATH} with 15 deterministic synthetic fixtures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
