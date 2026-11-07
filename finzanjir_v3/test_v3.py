import json
import tempfile
import unittest
from pathlib import Path
import laboratory as lab
import offline_ai

class SyntheticLabTests(unittest.TestCase):
    def setUp(self):
        self.old = lab.LAB_DB
        self.tmp = tempfile.TemporaryDirectory()
        lab.LAB_DB = Path(self.tmp.name) / "lab.sqlite3"
        lab.init_lab()

    def tearDown(self):
        lab.LAB_DB = self.old
        self.tmp.cleanup()

    def test_exactly_400_cases(self):
        self.assertEqual(lab.generate_dataset(seed=317), 400)
        snap=lab.snapshot()
        self.assertEqual(snap["total"],400)

    def test_four_synthetic_banks(self):
        lab.generate_dataset()
        self.assertEqual(len(lab.snapshot()["banks"]),4)

    def test_missing_data_routes_to_review(self):
        p=lab._make_payload(1,"missing_data",__import__("random").Random(2))
        p["scenario"]="missing_data"
        missing,errors=lab._validate(p)
        outcome,_=lab._classify(p,missing,errors)
        self.assertEqual(outcome,"DATA_REVIEW")

    def test_contradiction_routes_to_review(self):
        p=lab._make_payload(1,"contradictory",__import__("random").Random(2))
        p["scenario"]="contradictory"
        missing,errors=lab._validate(p)
        outcome,_=lab._classify(p,missing,errors)
        self.assertEqual(outcome,"DATA_REVIEW")

    def test_ato_routes_to_human(self):
        p=lab._make_payload(1,"ato",__import__("random").Random(2))
        p["scenario"]="ato"
        missing,errors=lab._validate(p)
        outcome,_=lab._classify(p,missing,errors)
        self.assertEqual(outcome,"HUMAN_REVIEW")

    def test_signal_is_not_verdict(self):
        p=lab._make_payload(1,"suspicious_combo",__import__("random").Random(2))
        p["scenario"]="suspicious_combo"
        missing,errors=lab._validate(p)
        outcome,detail=lab._classify(p,missing,errors)
        self.assertEqual(outcome,"HUMAN_REVIEW")
        self.assertIn("aybdorlik isboti emas",detail["reason"])

    def test_offline_ai_has_no_external_provider(self):
        self.assertIn("offline",offline_ai.answer("FINZANJIR nima?")["mode"])
        self.assertNotIn("http",Path(offline_ai.__file__).read_text(encoding="utf-8").lower())

    def test_ai_abstains_on_unknown_question(self):
        r=offline_ai.answer("Kvazarlarning bugungi bozor narxi qancha?")
        self.assertEqual(r["status"],"NO_SUFFICIENT_EVIDENCE")

    def test_ai_regression(self):
        self.assertTrue(all(x["passed"] for x in offline_ai.self_test()))

if __name__=="__main__":
    unittest.main()
