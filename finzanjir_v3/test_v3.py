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

    def test_full_400_event_pipeline(self):
        lab.generate_dataset(seed=317)
        with lab.connect() as c:
            rows=c.execute("SELECT * FROM bank_events WHERE state='QUEUED' ORDER BY event_id").fetchall()
        self.assertEqual(len(rows),400)
        for row in rows:
            lab._process_one(row)
        snap=lab.snapshot()
        self.assertEqual(snap["counts"].get("PROCESSED",0),400)
        self.assertGreater(len(snap["cases"]),0)
        self.assertGreater(len(snap["data_reviews"]),0)
        self.assertEqual(lab.evaluate()["processed"],400)

    def test_four_synthetic_banks(self):
        lab.generate_dataset()
        self.assertEqual(len(lab.snapshot()["banks"]),4)

    def test_single_signal_routes_to_recheck(self):
        lab.generate_dataset()
        with lab.connect() as c:
            row=c.execute("SELECT * FROM bank_events WHERE scenario='ambiguous_single_signal' LIMIT 1").fetchone()
        lab._process_one(row)
        ticket=lab.snapshot()["data_reviews"][0]
        self.assertEqual(ticket["review_type"],"UNRESOLVED_SIGNAL")
        lab.review_data_ticket(ticket["review_id"],"RECHECK_RULES","Re-run rule with added context")
        self.assertEqual(lab.snapshot()["data_reviews"][0]["status"],"READY_FOR_RECHECK")

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

    def test_kill_switch_requires_explicit_recovery(self):
        lab.generate_dataset()
        lab.emergency_stop("test incident")
        with self.assertRaises(RuntimeError):
            lab.start_run(resume=True)
        with self.assertRaises(ValueError):
            lab.recover_emergency(confirmed=False)
        lab.recover_emergency(confirmed=True,note="reviewed")
        self.assertEqual(lab.get_meta()["run_state"],"STOPPED")
        self.assertEqual(lab.snapshot()["counts"].get("QUEUED",0),400)

    def test_pause_stop_keep_queued_data(self):
        lab.generate_dataset()
        before=lab.snapshot()["counts"].get("QUEUED",0)
        lab.pause_run()
        self.assertEqual(lab.snapshot()["counts"].get("QUEUED",0),before)
        lab.stop_run()
        self.assertEqual(lab.snapshot()["counts"].get("QUEUED",0),before)

    def test_duplicate_delivery_is_marked_for_deduplication(self):
        lab.generate_dataset()
        with lab.connect() as c:
            row=c.execute("SELECT * FROM bank_events WHERE scenario='duplicate_or_transport' LIMIT 1").fetchone()
        lab._process_one(row)
        duplicate_result=lab._process_one(row)
        self.assertEqual(duplicate_result,"DUPLICATE_IGNORED")
        with lab.connect() as c:
            result=json.loads(c.execute("SELECT result FROM bank_events WHERE event_id=?",(row["event_id"],)).fetchone()["result"])
        self.assertTrue(result["duplicate_delivery_detected"])
        self.assertEqual(result["idempotency_key"],row["event_id"])
        self.assertEqual(result["duplicate_delivery_action"],"DEDUPLICATED_BY_EVENT_ID")

    def test_human_review_prepares_but_does_not_send_bank_response(self):
        lab.generate_dataset()
        with lab.connect() as c:
            row=c.execute("SELECT * FROM bank_events WHERE scenario='ato' LIMIT 1").fetchone()
        lab._process_one(row)
        case=lab.snapshot()["cases"][0]
        lab.review_case(case["case_id"],"REFER_TO_BANK","Test reviewer confirms referral is appropriate")
        updated=lab.snapshot()["cases"][0]
        self.assertEqual(updated["status"],"REFERRAL_READY")
        self.assertEqual(updated["bank_response_status"],"READY_NOT_SENT")

    def test_data_quality_queue_can_request_missing_bank_data(self):
        lab.generate_dataset()
        with lab.connect() as c:
            row=c.execute("SELECT * FROM bank_events WHERE scenario='missing_data' LIMIT 1").fetchone()
        lab._process_one(row)
        ticket=lab.snapshot()["data_reviews"][0]
        lab.review_data_ticket(ticket["review_id"],"REQUEST_BANK_DATA","Please resend missing authorized fields")
        updated=lab.snapshot()["data_reviews"][0]
        self.assertEqual(updated["status"],"WAITING_BANK_DATA")

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
