import tempfile, unittest
from pathlib import Path
import core

class CoreTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/"t.sqlite3";core.init_db(self.path)
 def tearDown(self):self.tmp.cleanup()
 def sample(self,**kw):
  x={"customer_ref":"C1","transaction_ref":"T1","amount":1000,"event_time":"2026-11-07T10:00:00+00:00","device_ref":"D1","location":"Tashkent","recipient_ref":"R1","session_seconds":60,"consent_scope":"transfer","fraud_type":"unknown","source_type":"test","source_note":"unit test"};x.update(kw);return x
 def test_reject_nonpositive(self):
  with self.assertRaises(ValueError):core.add_event(self.sample(amount=0),self.path)
 def test_one_event_not_case(self):
  eid=core.add_event(self.sample(),self.path);a=core.assess(eid,self.path);self.assertFalse(a.case_candidate);self.assertIsNone(core.save_assessment(eid,a,self.path))
 def test_case_human_review(self):
  for i,amt in enumerate([1000,1200,900]):
   core.add_event(self.sample(transaction_ref="B"+str(i),amount=amt,event_time=f"2026-11-07T09:0{i}:00+00:00",device_ref="DOLD",recipient_ref="ROLD"),self.path)
  eid=core.add_event(self.sample(transaction_ref="NEW",amount=120000,device_ref="DNEW",recipient_ref="RNEW",session_seconds=5,consent_scope="unknown",password_reset_time="2026-11-07T09:58:00+00:00"),self.path)
  a=core.assess(eid,self.path);self.assertTrue(a.case_candidate);cid=core.save_assessment(eid,a,self.path)
  core.review(cid,"REFERRED_TO_BANK","review test","reviewer",self.path)
  self.assertEqual(core.cases(path=self.path)[0]["decision"],"REFERRED_TO_BANK")
 def test_invalid_review_rejected(self):
  with self.assertRaises(ValueError):core.review("x","BLOCK_CARD","","x",self.path)
 def test_self_checks(self):self.assertTrue(all(x["result"]=="PASS" for x in core.self_checks()))
if __name__=="__main__":unittest.main()
