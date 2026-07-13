import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[3]
CONTRACT_DIR = ROOT / "contracts" / "service-plaza" / "nova"


class NovaApiContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads((CONTRACT_DIR / "nova-api-contract.v1.schema.json").read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema)

    def test_signed_contract_is_valid(self):
        contract = json.loads((CONTRACT_DIR / "nova-api-contract.v1.json").read_text(encoding="utf-8"))
        self.validator.validate(contract)

    def test_model_scope_expansion_fixture_is_rejected(self):
        fixture = json.loads((CONTRACT_DIR / "fixtures" / "invalid-model-scope.json").read_text(encoding="utf-8"))
        errors = list(self.validator.iter_errors(fixture))
        self.assertTrue(errors)
        self.assertTrue(any("False was expected" in error.message for error in errors))


if __name__ == "__main__":
    unittest.main()
