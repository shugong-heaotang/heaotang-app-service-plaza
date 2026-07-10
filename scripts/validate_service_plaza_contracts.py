import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: validate_service_plaza_contracts.py SCHEMA BASELINE")

    schema_path = Path(sys.argv[1])
    baseline_path = Path(sys.argv[2])
    schema = load_json(schema_path)
    baseline = load_json(baseline_path)

    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(baseline), key=lambda error: list(error.path))
    if errors:
        for error in errors:
            location = "/".join(str(part) for part in error.absolute_path) or "<root>"
            print(f"{location}: {error.message}", file=sys.stderr)
        return 1

    print("Service Plaza action baseline satisfies the Draft 2020-12 schema.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
