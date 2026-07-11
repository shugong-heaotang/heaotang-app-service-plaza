import json, tempfile, unittest
from pathlib import Path
from scripts.validate_club_category_filter import validate

ROOT=Path(__file__).resolve().parents[2]
SCHEMA=ROOT/'contracts/service-plaza/club-category-filter.v1.schema.json'; CONTRACT=ROOT/'contracts/service-plaza/club-category-filter.v1.json'; FIXTURE=ROOT/'scripts/tests/fixtures/club-category-filter/mixed-dataset.v1.json'
class ClubCategoryFilterTests(unittest.TestCase):
    def test_valid_contract_has_zero_cross_category(self): self.assertEqual(validate(SCHEMA,CONTRACT,FIXTURE),[])
    def test_frontend_style_type_only_contract_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            data=json.loads(CONTRACT.read_text(encoding='utf-8'));data['profiles']['self-created'].pop('category');p=Path(d)/'bad.json';p.write_text(json.dumps(data),encoding='utf-8')
            self.assertTrue(validate(SCHEMA,p,FIXTURE))
if __name__=='__main__': unittest.main()
