import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent


def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def test_contract_matches_schema():
    schema = load("public-welfare-regional.v1.schema.json")
    contract = load("public-welfare-regional.v1.json")
    Draft202012Validator.check_schema(schema)
    assert list(Draft202012Validator(schema).iter_errors(contract)) == []


def test_approval_is_the_only_public_welfare_creation_path():
    contract = load("public-welfare-regional.v1.json")
    assert contract["classification"] == {
        "public_welfare_type": "standard",
        "public_welfare_category": "charity",
        "direct_create_allowed": False,
    }
    effect = contract["workflows"]["establishment_application"]["approval_effect"]
    assert "Atomically create" in effect
    assert "external publication" in effect


def test_role_approval_grants_real_scoped_role_and_center_search_is_public():
    contract = load("public-welfare-regional.v1.json")
    role_effect = contract["workflows"]["regional_role_application"]["approval_effect"]
    assert "Grant exactly" in role_effect
    search = next(item for item in contract["api"] if item["operation_id"] == "search-club-alliance-centers")
    assert search["auth"] == "anonymous"
    assert contract["center_search"]["kinds"] == [
        "regional_management_center",
        "public_welfare_service_center",
    ]
