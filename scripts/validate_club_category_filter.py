#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

def validate(schema_path: Path, contract_path: Path, fixture_path: Path) -> list[str]:
    schema=json.loads(schema_path.read_text(encoding="utf-8")); contract=json.loads(contract_path.read_text(encoding="utf-8")); rows=json.loads(fixture_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    errors=[e.message for e in Draft202012Validator(schema).iter_errors(contract)]
    expected={"self-created": {1}, "public-benefit": {2}}
    for name, profile in contract.get("profiles", {}).items():
        actual={row["id"] for row in rows if row.get("entity_kind", "club")=="club" and row.get("type")==profile.get("club_type") and row.get("category")==profile.get("category")}
        if actual != expected.get(name, set()): errors.append(f"{name}: zero-cross-category fixture mismatch expected={sorted(expected.get(name,set()))} actual={sorted(actual)}")
    if contract.get("profiles",{}).get("self-created",{}).get("category")!="general": errors.append("self-created must be standard+general")
    if contract.get("profiles",{}).get("public-benefit",{}).get("category")!="charity": errors.append("public-benefit must be standard+charity")
    for required in ("CLUB_FILTER_CATEGORY_INVALID","CLUB_FILTER_COMBINATION_UNSUPPORTED"):
        if required not in contract.get("stable_errors",[]): errors.append(f"missing stable error {required}")
    return errors

def main():
    p=argparse.ArgumentParser();p.add_argument("schema",type=Path);p.add_argument("contract",type=Path);p.add_argument("fixture",type=Path);a=p.parse_args();errors=validate(a.schema,a.contract,a.fixture)
    if errors:
        [print(f"ERROR: {e}",file=sys.stderr) for e in errors];return 1
    print("Club category authority contract and mixed-data fixture are valid.");return 0
if __name__=="__main__": raise SystemExit(main())
