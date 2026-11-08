import json
import tempfile
import unittest
from pathlib import Path
import laboratory as lab
import offline_ai
import visitor_analytics as visitors

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
        evaluation=lab.evaluate()
        self.assertEqual(evaluation["processed"],400)
        self.assertTrue(all(left.strip()==right.strip() for left,right in (key.split("→") for key in evaluation["confusion"])))

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

    def test_scenario_label_does_not_change_classification(self):
        p=lab._make_payload(17,"ato",__import__("random").Random(9))
        p["scenario"]="ato"
        missing,errors=lab._validate(p)
        first=lab._classify(p,missing,errors)[0]
        p["scenario"]="normal"
        second=lab._classify(p,missing,errors)[0]
        self.assertEqual(first,second)

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
        self.assertEqual(result["duplicate_delivery_action"],"SIMULATED_TWO_ATTEMPTS_IDEMPOTENCY_NOT_TRANSPORT_TESTED")

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

    def test_private_feedback_storage(self):
        old = visitors.VISITOR_DB
        visitors.VISITOR_DB = Path(self.tmp.name) / "visitors.sqlite3"
        try:
            visitors.save_feedback({"missing": "Test taklif"})
            snap = visitors.admin_snapshot()
            self.assertEqual(snap["feedback_count"], 1)
            self.assertEqual(snap["feedback"][0]["missing"], "Test taklif")
            self.assertEqual(snap["feedback"][0]["name"], "")
        finally:
            visitors.VISITOR_DB = old

    def test_admin_password_hash(self):
        encoded = visitors.make_password_hash("Strong-Test-Password")
        self.assertTrue(visitors.verify_admin_password("Strong-Test-Password", encoded))
        self.assertFalse(visitors.verify_admin_password("wrong-password", encoded))
        with self.assertRaises(ValueError):
            visitors.make_password_hash("short")

    def test_admin_login_rate_limit_and_reset(self):
        old = visitors.VISITOR_DB
        visitors.VISITOR_DB = Path(self.tmp.name) / "visitors.sqlite3"
        try:
            sid, secret = "author-session", "x" * 40
            self.assertTrue(visitors.admin_login_status(sid, secret, now=1000)["allowed"])
            for i in range(5):
                visitors.record_admin_login_attempt(sid, secret, False, now=1000+i)
            status = visitors.admin_login_status(sid, secret, now=1006)
            self.assertFalse(status["allowed"])
            self.assertGreater(status["retry_after"], 0)
            visitors.record_admin_login_attempt(sid, secret, True, now=2000)
            self.assertTrue(visitors.admin_login_status(sid, secret, now=2001)["allowed"])
        finally:
            visitors.VISITOR_DB = old

    def test_visitor_session_is_pseudonymous_and_device_detection_approximate(self):
        old = visitors.VISITOR_DB
        visitors.VISITOR_DB = Path(self.tmp.name) / "visitors.sqlite3"
        try:
            visitors.record_page_view("random-session-id", "Bosh sahifa",
                "Mozilla/5.0 (Linux; Android 14; SAMSUNG SM-S918B) Chrome/120.0", "test-secret")
            snap = visitors.admin_snapshot()
            self.assertEqual(snap["visitors"], 1)
            self.assertIn("Samsung", snap["devices"][0]["device_family"])
            with visitors._connect() as c:
                stored = c.execute("SELECT session_key FROM visits").fetchone()[0]
            self.assertNotEqual(stored, "random-session-id")
        finally:
            visitors.VISITOR_DB = old

    def test_offline_ai_has_no_external_provider(self):
        self.assertIn("offline",offline_ai.answer("FINZANJIR nima?")["mode"])
        self.assertNotIn("http",Path(offline_ai.__file__).read_text(encoding="utf-8").lower())

    def test_ai_abstains_on_unknown_question(self):
        r=offline_ai.answer("Kvazarlarning bugungi bozor narxi qancha?")
        self.assertEqual(r["status"],"NO_SUFFICIENT_EVIDENCE")

    def test_ai_regression(self):
        self.assertTrue(all(x["passed"] for x in offline_ai.self_test()))

    def test_public_route_is_feedback_only(self):
        source = (Path(__file__).with_name("app.py")).read_text(encoding="utf-8")
        self.assertIn('page = "Tashrifchi fikri"', source)
        self.assertIn('page = "Muallif analitikasi"', source)
        self.assertNotIn('page=st.sidebar.radio("Bo‘limni tanlang"', source)

    def test_feedback_rejects_empty_submission(self):
        old = visitors.VISITOR_DB
        visitors.VISITOR_DB = Path(self.tmp.name) / "empty-feedback.sqlite3"
        try:
            with self.assertRaises(ValueError):
                visitors.save_feedback({})
            self.assertEqual(visitors.admin_snapshot()["feedback_count"], 0)
        finally:
            visitors.VISITOR_DB = old

    def test_feedback_text_is_bounded(self):
        old = visitors.VISITOR_DB
        visitors.VISITOR_DB = Path(self.tmp.name) / "bounded-feedback.sqlite3"
        try:
            visitors.save_feedback({"improve": "x" * (visitors.MAX_TEXT + 500)})
            item = visitors.admin_snapshot()["feedback"][0]
            self.assertEqual(len(item["improve"]), visitors.MAX_TEXT)
        finally:
            visitors.VISITOR_DB = old

if __name__=="__main__":
    unittest.main()
