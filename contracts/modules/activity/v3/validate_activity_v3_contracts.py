import json
from pathlib import Path
from jsonschema import validate

ROOT = Path(__file__).resolve().parent
MODULE = ROOT.parent

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    files = list(ROOT.rglob("*.json")) + [MODULE / "internal-dependencies.v1.json"]
    docs = {str(p.relative_to(MODULE)).replace("\\", "/"): load(p) for p in files}
    req = docs["v3/requirements.v3.json"]
    schema_pairs = [
        ("v3/requirements.v3.json", "v3/requirements.v3.schema.json"),
        ("v3/domain-model.v1.json", "v3/domain-model.v1.schema.json"),
        ("v3/state-machines.v1.json", "v3/state-machines.v1.schema.json"),
        ("v3/api-contracts.v1.json", "v3/api-contracts.v1.schema.json"),
        ("v3/safety-matrix.v1.json", "v3/safety-matrix.v1.schema.json"),
    ]
    for instance, schema in schema_pairs:
        validate(docs[instance], docs[schema])
    validate(docs["internal-dependencies.v1.json"], load(MODULE / "internal-dependencies.v1.schema.json"))
    assert req["baseline"]["sha256"] == "838C54AE895D223E66FCA8BE8BB54D588DC3F83234B430B91073B8454E2975E6"
    assert [x["id"] for x in req["acceptance"]] == list(range(1, 37))
    assert all(x["capability"] and x["negative"] for x in req["acceptance"])
    assert len(req["pending_decisions"]) == 10
    deps = docs["internal-dependencies.v1.json"]
    assert len(deps["dependencies"]) == 6
    required = {"owner","version","request_schema","response_schema","errors","permission","fixture","readiness"}
    assert all(required <= set(x) and x["readiness"] == "provisional" for x in deps["dependencies"])
    for doc in docs.values():
        if "execution" in doc:
            assert doc["execution"] == {"executable": False, "mode": "mock-only", "environment": "non-production"}
    safety = docs["v3/safety-matrix.v1.json"]
    denied = {v for row in safety["boundaries"] for v in row.get("deny", [])}
    for item in ["auto-publish","auto-register","auto-invite","auto-contact","auto-cart","auto-order","auto-payment","duplicate-attribution","real-payment-in-m0"]:
        assert item in denied
    fixtures = docs["v3/fixtures/cases.v1.json"]
    assert fixtures["deterministic"] and fixtures["synthetic_only"]
    assert {x["id"] for x in fixtures["cases"]} >= {"member-direct-publish-denied","privacy-small-cohort","unilateral-introduction","duplicate-attribution","retry-idempotent"}
    print(f"PASS activity V3 M0 contracts: {len(files)} JSON files, 36 acceptance mappings, 6 provisional dependencies")

if __name__ == "__main__":
    main()
