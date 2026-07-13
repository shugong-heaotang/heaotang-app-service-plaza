import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).parent


def load(relative_path: str):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def main() -> int:
    contract = load("catalog.v1.json")
    schema = load("catalog.v1.schema.json")
    fixtures = load("fixtures/cases.v1.json")
    errors = [error.message for error in Draft202012Validator(schema).iter_errors(contract)]
    fixture_ids = [case["id"] for case in fixtures.get("cases", [])]
    if fixtures.get("contract_version") != "protection-mall.catalog-cases.v1":
        errors.append("fixture contract_version mismatch")
    if len(fixture_ids) < 10 or len(fixture_ids) != len(set(fixture_ids)):
        errors.append("fixtures must contain at least 10 unique cases")
    if not {"accept", "race_free"}.issubset({case.get("expected") for case in fixtures.get("cases", [])}):
        errors.append("fixtures must cover positive and concurrency outcomes")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Protection Mall M2 catalog contracts valid: 1 contract, {len(fixture_ids)} synthetic cases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
