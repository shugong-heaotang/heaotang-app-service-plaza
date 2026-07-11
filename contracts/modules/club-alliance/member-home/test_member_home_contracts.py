#!/usr/bin/env python3
import copy,json,re,unittest
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parent
def load(name):
 raw=(ROOT/name).read_bytes(); assert not raw.startswith(b'\xef\xbb\xbf'); assert b'\r\n' not in raw; return json.loads(raw.decode())
def semantic(c,e,f):
 if c['layout_order']!=['member-summary','my-clubs','today-tasks','recent-activities','alliance-feed','explore-more']: return 'CMH_ORDER_INVALID'
 if c['sections']['explore-more'].get('action_ids')!=['public-benefit-club','self-created-club','family-club','club-federation']: return 'CMH_EXPLORE_INVALID'
 if c['sections']['my-clubs']['source']!='GET /api/v1/clubs/my' or c['sections']['my-clubs']['privacy']!='self-only': return 'CMH_MY_CLUBS_INVALID'
 if c['degradation'].get('forbid_empty_array_fallback') is not True or c['degradation'].get('forbid_runtime_mock') is not True: return 'CMH_FALLBACK_INVALID'
 if c['management']!={'action_id':'club-manage','placement':'secondary','required_scope':'club:manage','hidden_for_ordinary_member':True}: return 'CMH_MANAGEMENT_INVALID'
 if not {'phone','id_card','health_detail','family_private_record','payment_account','raw_token'}.issubset(c['forbidden_response_fields']): return 'CMH_PRIVACY_INVALID'
 ids=[x['error_id'] for x in e['errors']]
 if len(ids)!=len(set(ids)) or len(ids)<8:return 'CMH_ERRORS_INVALID'
 if f.get('seed')!='HEAOTANG-CMH-20260712-V1' or f.get('synthetic_only') is not True or len(f.get('cases',[]))<6:return 'CMH_FIXTURES_INVALID'
 if any(re.search(p,json.dumps(f)) for p in [r'(?<!\d)1[3-9]\d{9}(?!\d)',r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.']):return 'CMH_FIXTURE_SENSITIVE'
 return None
class Test(unittest.TestCase):
 @classmethod
 def setUpClass(cls): cls.c=load('member-home.v1.json');cls.e=load('error-catalog.v1.json');cls.f=load('fixtures/cases.v1.json')
 def test_schema(self):
  Draft202012Validator(load('member-home.v1.schema.json')).validate(self.c);Draft202012Validator(load('error-catalog.v1.schema.json')).validate(self.e)
 def test_baseline(self):self.assertIsNone(semantic(self.c,self.e,self.f))
 def test_order(self):
  x=copy.deepcopy(self.c);x['layout_order'].reverse();self.assertEqual('CMH_ORDER_INVALID',semantic(x,self.e,self.f))
 def test_explore(self):
  x=copy.deepcopy(self.c);x['sections']['explore-more']['action_ids'].remove('club-federation');self.assertEqual('CMH_EXPLORE_INVALID',semantic(x,self.e,self.f))
 def test_no_runtime_fallback(self):
  x=copy.deepcopy(self.c);x['degradation']['forbid_runtime_mock']=False;self.assertEqual('CMH_FALLBACK_INVALID',semantic(x,self.e,self.f))
 def test_privacy(self):
  x=copy.deepcopy(self.c);x['forbidden_response_fields'].remove('phone');self.assertEqual('CMH_PRIVACY_INVALID',semantic(x,self.e,self.f))
 def test_errors_unique(self):
  x=copy.deepcopy(self.e);x['errors'].append(x['errors'][0]);self.assertEqual('CMH_ERRORS_INVALID',semantic(self.c,x,self.f))
 def test_identities(self):self.assertEqual({'new-member','family-member','multi-club-member','manager','partial-failure','unauthorized'},{x['case_id'] for x in self.f['cases']})
if __name__=='__main__':unittest.main(verbosity=2)
