import json
import copy
from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError, validate

ROOT = Path(__file__).resolve().parent
MODULE = ROOT.parent

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def decision_oracle(synthetic_input):
    if synthetic_input["violated_rules"] or not synthetic_input["authorized"] or not synthetic_input["confirmed"]:
        return "deny"
    return "allow"

def cross_domain_oracle(synthetic_input):
    if synthetic_input["club_id"] != synthetic_input["authorized_club_id"]:
        return "deny", 1
    if not synthetic_input["human_confirmed"]:
        return "deny", 1
    if synthetic_input["requested_action"] != "reference_product":
        return "deny", 2
    if not synthetic_input["saleable"]:
        return "deny", 2
    return "allow", 3

def validate_trace_semantics(req, trace_doc, fixture_doc):
    cases = {x["id"]: x for x in fixture_doc["cases"]}
    traces = trace_doc["traces"]
    assert [x["acceptance_id"] for x in traces] == list(range(1, 37))
    assert len(cases) == 72
    for trace in traces:
        positive, negative = cases[trace["positive_fixture"]], cases[trace["negative_fixture"]]
        assert positive["acceptance_id"] == negative["acceptance_id"] == trace["acceptance_id"]
        assert positive["capability"] == negative["capability"] == trace["capability"]
        assert trace["capability"] == req["acceptance"][trace["acceptance_id"] - 1]["capability"]
        assert trace["assertions"] == ["capability_matches_requirement", "positive_oracle_allows", "negative_oracle_denies", "negative_rule_matches_requirement"]
        assert positive["polarity"] == "positive" and decision_oracle(positive["synthetic_input"]) == positive["expected_decision"] == "allow"
        assert negative["polarity"] == "negative" and decision_oracle(negative["synthetic_input"]) == negative["expected_decision"] == "deny"
        assert negative["rule"] == req["acceptance"][trace["acceptance_id"] - 1]["negative"]

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
        ("v3/trace-matrix.v3.json", "v3/trace-matrix.v3.schema.json"),
        ("v3/fixtures/cases.v1.json", "v3/fixtures/cases.v1.schema.json"),
        ("v3/cross-domain-events.v1.json", "v3/cross-domain-events.v1.schema.json"),
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
    for dependency in deps["dependencies"]:
        for embedded in (dependency["request_schema"], dependency["response_schema"]):
            Draft202012Validator.check_schema(embedded)
            valid_instance = {field: "synthetic" for field in embedded["required"]}
            validate(valid_instance, embedded)
            try:
                validate({**valid_instance, "unexpected": "denied"}, embedded)
            except ValidationError:
                pass
            else:
                raise AssertionError(f"dependency schema accepted unexpected property: {dependency['id']}")
    for doc in docs.values():
        if "execution" in doc:
            assert doc["execution"] == {"executable": False, "mode": "mock-only", "environment": "non-production"}
    safety = docs["v3/safety-matrix.v1.json"]
    denied = {v for row in safety["boundaries"] for v in row.get("deny", [])}
    for item in ["auto-publish","auto-register","auto-invite","auto-contact","auto-cart","auto-order","auto-payment","duplicate-attribution","real-payment-in-m0"]:
        assert item in denied
    fixtures = docs["v3/fixtures/cases.v1.json"]
    assert fixtures["deterministic"] and fixtures["synthetic_only"]
    trace_doc = docs["v3/trace-matrix.v3.json"]
    validate_trace_semantics(req, trace_doc, fixtures)
    # Mutation guards: semantic weakening must fail, not merely remain non-empty.
    mutated = copy.deepcopy(trace_doc)
    mutated["traces"][0]["positive_fixture"] = mutated["traces"][1]["positive_fixture"]
    try:
        validate_trace_semantics(req, mutated, fixtures)
    except AssertionError:
        pass
    else:
        raise AssertionError("trace fixture mutation accepted")
    mutated_negative = copy.deepcopy(fixtures)
    mutated_negative["cases"][1]["synthetic_input"] = {"authorized": True, "confirmed": True, "violated_rules": []}
    try:
        validate_trace_semantics(req, trace_doc, mutated_negative)
    except AssertionError:
        pass
    else:
        raise AssertionError("synthetic-input mutation accepted")
    api_operations = {item["operation"] for item in docs["v3/api-contracts.v1.json"]["endpoints"]}
    assert all(trace["api_operation"] in api_operations for trace in trace_doc["traces"])
    cross_domain = docs["v3/cross-domain-events.v1.json"]
    assert [event["sequence"] for event in cross_domain["chain"]] == [1, 2, 3]
    assert [(event["producer"], event["consumer"]) for event in cross_domain["chain"]] == [
        ("activity", "club-alliance"), ("club-alliance", "mall"), ("mall", "activity")
    ]
    money_fields = {"amount", "currency", "price", "payment_id", "order_id", "refund_id", "settlement_id"}
    assert all(money_fields <= set(event["forbidden_payload"]) for event in cross_domain["chain"])
    for scenario in cross_domain["synthetic_scenarios"]:
        decision, emitted_events = cross_domain_oracle(scenario["input"])
        assert decision == scenario["expected"]["decision"]
        assert emitted_events == scenario["expected"]["emitted_events"]
        assert scenario["expected"]["money_movement"] is False
    mutated_cross_domain = copy.deepcopy(cross_domain)
    mutated_cross_domain["synthetic_scenarios"][2]["input"]["requested_action"] = "reference_product"
    decision, emitted_events = cross_domain_oracle(mutated_cross_domain["synthetic_scenarios"][2]["input"])
    assert (decision, emitted_events) != (
        mutated_cross_domain["synthetic_scenarios"][2]["expected"]["decision"],
        mutated_cross_domain["synthetic_scenarios"][2]["expected"]["emitted_events"],
    )
    print(f"PASS activity V3 M0: {len(files)} JSON files, 72 acceptance cases, 3 cross-domain event cases, 6 usable dependency schemas, semantic APIs and mutation guards")

if __name__ == "__main__":
    main()
