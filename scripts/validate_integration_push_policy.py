from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator


EXPECTED_ERRORS = [
    "INTEGRATION_REPOSITORY_INVALID",
    "INTEGRATION_WORKTREE_DIRTY",
    "INTEGRATION_CANDIDATE_BRANCH_INVALID",
    "INTEGRATION_EXPECTED_REMOTE_INVALID",
    "INTEGRATION_REMOTE_UNAVAILABLE",
    "INTEGRATION_REMOTE_HEAD_CHANGED",
    "INTEGRATION_CANDIDATE_INVALID",
    "INTEGRATION_REMOTE_NOT_ANCESTOR",
    "INTEGRATION_CANDIDATE_BEHIND",
    "INTEGRATION_LEASE_PUSH_FAILED",
    "INTEGRATION_POST_PUSH_MISMATCH",
]


def validate(schema_path: Path, contract_path: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    errors = [error.message for error in Draft202012Validator(schema).iter_errors(contract)]
    if contract.get("error_ids") != EXPECTED_ERRORS:
        errors.append("error_ids must preserve the stable v1 order")
    if contract.get("freshness", {}).get("require_explicit_lease") is not True:
        errors.append("explicit lease is mandatory")
    if contract.get("candidate", {}).get("max_behind_count") != 0:
        errors.append("behind candidates must fail closed")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("schema", type=Path)
    parser.add_argument("contract", type=Path)
    args = parser.parse_args()
    errors = validate(args.schema, args.contract)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Integration push policy is schema-valid and fail-closed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
