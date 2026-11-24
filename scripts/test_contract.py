import copy, hashlib, json, tempfile, unittest
from pathlib import Path
from check_contract import inspect_plan

class ContractTests(unittest.TestCase):
    def plan(self):
        return json.loads((Path(__file__).resolve().parents[1]/'examples/contract.json').read_text(encoding='utf-8'))
    def test_valid_example_is_not_modified(self):
        d=self.plan();before=copy.deepcopy(d)
        self.assertTrue(inspect_plan(d)['contract_valid'])
        self.assertEqual(d,before)
    def test_foreign_role_and_malformed_input_are_rejected(self):
        d=self.plan();d['skill']='foreign-skill'
        self.assertFalse(inspect_plan(d)['contract_valid'])
        for bad in [None,[],{},'text',{'skill':self.plan()['skill']}]:
            self.assertFalse(inspect_plan(bad)['contract_valid'])

    def test_version_conflict_and_unknown_cannot_publish_as_fact(self):
        d=self.plan();d['sources'][0]['version']='old-patch'
        self.assertFalse(inspect_plan(d)['contract_valid'])
        d=self.plan();d['claims'][0]['status']='unknown'
        self.assertFalse(inspect_plan(d)['contract_valid'])
    def test_reposts_and_generated_evidence_are_not_verified_sources(self):
        d=self.plan();s=copy.deepcopy(d['sources'][0]);s['id']='S2';d['sources'].append(s)
        d['claims'][0].update(verification_basis='independent_sources',source_ids=['S1','S2'])
        self.assertFalse(inspect_plan(d)['contract_valid'])
        d['sources'][1]['origin_id']='different-original'
        self.assertTrue(inspect_plan(d)['contract_valid'])
        d=self.plan();d['images']=[{'kind':'generated','used_as_mechanic_evidence':True,'version':'1.0'}]
        self.assertFalse(inspect_plan(d)['contract_valid'])


if __name__=='__main__': unittest.main()
