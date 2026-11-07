from __future__ import annotations
import json, random, sqlite3, threading, time, uuid
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
LAB_DB = ROOT / "synthetic_lab.sqlite3"
_lock = threading.Lock()
_worker = None
_startup_checked = False
TOTAL = 400
ALLOCATIONS = [
    ("normal", 80), ("ambiguous_single_signal", 20), ("suspicious_combo", 70), ("ato", 45),
    ("social_engineering", 40), ("money_mule", 40), ("device_anomaly", 35),
    ("missing_data", 30), ("contradictory", 20), ("duplicate_or_transport", 20),
]
BANKS = ["SUNIY-BANK-A", "SUNIY-BANK-B", "SUNIY-BANK-C", "SUNIY-BANK-D"]

@contextmanager
def connect():
    c = sqlite3.connect(str(LAB_DB), timeout=20, check_same_thread=False)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA foreign_keys=ON")
    try:
        yield c
        c.commit()
    except Exception:
        c.rollback()
        raise
    finally:
        c.close()

def init_lab():
    global _startup_checked
    with connect() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS lab_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS bank_events (
          event_id TEXT PRIMARY KEY, bank_id TEXT NOT NULL, scenario TEXT NOT NULL,
          expected TEXT NOT NULL, payload TEXT NOT NULL, state TEXT NOT NULL,
          result TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL, processed_at TEXT
        );
        CREATE TABLE IF NOT EXISTS lab_cases (
          case_id TEXT PRIMARY KEY, event_id TEXT NOT NULL UNIQUE, bank_id TEXT NOT NULL,
          status TEXT NOT NULL, reason TEXT NOT NULL, created_at TEXT NOT NULL,
          review_outcome TEXT NOT NULL DEFAULT '', review_note TEXT NOT NULL DEFAULT '',
          bank_response_status TEXT NOT NULL DEFAULT 'NOT_READY', updated_at TEXT NOT NULL DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS lab_data_reviews (
          review_id TEXT PRIMARY KEY, event_id TEXT NOT NULL UNIQUE, bank_id TEXT NOT NULL,
          status TEXT NOT NULL, reason TEXT NOT NULL, created_at TEXT NOT NULL,
          review_outcome TEXT NOT NULL DEFAULT '', review_note TEXT NOT NULL DEFAULT '',
          updated_at TEXT NOT NULL DEFAULT '', review_type TEXT NOT NULL DEFAULT 'DATA_QUALITY'
        );
        CREATE TABLE IF NOT EXISTS lab_audit (
          id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT NOT NULL, detail TEXT NOT NULL,
          created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_lab_state ON bank_events(state, created_at);
        """)
        defaults = {"run_state":"IDLE", "generated":"0", "processed":"0", "last_error":"",
                    "run_id":"", "started_at":"", "finished_at":""}
        existing={r["name"] for r in c.execute("PRAGMA table_info(lab_cases)")}
        migrations={
          "review_outcome":"TEXT NOT NULL DEFAULT ''",
          "review_note":"TEXT NOT NULL DEFAULT ''",
          "bank_response_status":"TEXT NOT NULL DEFAULT 'NOT_READY'",
          "updated_at":"TEXT NOT NULL DEFAULT ''",
          "review_type":"TEXT NOT NULL DEFAULT 'DATA_QUALITY'"
        }
        for column,definition in migrations.items():
            if column not in existing:
                c.execute(f"ALTER TABLE lab_cases ADD COLUMN {column} {definition}")
        review_columns={r["name"] for r in c.execute("PRAGMA table_info(lab_data_reviews)")}
        if "review_type" not in review_columns:
            c.execute("ALTER TABLE lab_data_reviews ADD COLUMN review_type TEXT NOT NULL DEFAULT 'DATA_QUALITY'")
        for k,v in defaults.items():
            c.execute("INSERT OR IGNORE INTO lab_meta(key,value) VALUES(?,?)",(k,v))
    if not _startup_checked:
        state=get_meta().get("run_state")
        if state=="RUNNING":
            set_meta(run_state="PAUSED",last_error="Ilova qayta ishga tushgan; xavfsizlik uchun navbat PAUSE holatiga o'tkazildi.")
            audit("RECOVERY_PAUSED","Process restart detected; queued events retained for manual resume")
        _startup_checked=True

def get_meta():
    with connect() as c:
        return {r["key"]:r["value"] for r in c.execute("SELECT key,value FROM lab_meta")}

def set_meta(**values):
    with connect() as c:
        for k,v in values.items():
            c.execute("INSERT INTO lab_meta(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",(k,str(v)))

def audit(action, detail):
    with connect() as c:
        c.execute("INSERT INTO lab_audit(action,detail,created_at) VALUES(?,?,?)",
                  (action,detail,datetime.now(timezone.utc).isoformat()))

def _make_payload(i:int, scenario:str, rng:random.Random):
    bank = BANKS[i % len(BANKS)]
    base = datetime(2026, 11, 1, 8, 0, tzinfo=timezone.utc) + timedelta(minutes=i*3)
    customer = f"CUST-{i%85:03d}"
    tx = f"TX-{i+1:04d}"
    amount = rng.choice([85000,120000,245000,490000,750000,1250000])
    direction = "OUT"
    device = f"DEV-{customer}-1"
    recipient = f"REC-{i%110:03d}"
    consent = "transfer"
    session = rng.randint(35,240)
    reset = None
    location = "Tashkent"
    duplicate = False
    missing = []
    contradictions = []
    if scenario == "normal":
        amount = rng.choice([45000,80000,120000,180000,250000])
        consent = "transfer"
    elif scenario == "ambiguous_single_signal":
        amount = 2200000
        consent = "transfer"
        session = 90
    elif scenario == "suspicious_combo":
        amount = rng.choice([3500000,5200000,8700000])
        recipient = f"NEW-REC-{i}"
        device = f"NEW-DEV-{i}"
        session = rng.randint(2,12)
        consent = rng.choice(["unknown","device_only"])
        reset = (base-timedelta(minutes=3)).isoformat()
    elif scenario == "ato":
        amount = rng.choice([1800000,4300000,9100000])
        device = f"ATO-DEV-{i}"
        location = rng.choice(["Dubai","Istanbul","Unknown"])
        session = rng.randint(1,10)
        reset = (base-timedelta(minutes=2)).isoformat()
        consent = "unknown"
    elif scenario == "social_engineering":
        amount = rng.choice([900000,2100000,4800000])
        recipient = f"CALL-REC-{i}"
        consent = "unknown"
        session = rng.randint(10,40)
    elif scenario == "money_mule":
        amount = rng.choice([1500000,3000000,6000000])
        direction = "IN" if i%2 else "OUT"
        recipient = f"MULE-NODE-{i%12}"
        consent = "transfer"
    elif scenario == "device_anomaly":
        device = f"SHARED-DEVICE-{i%5}"
        location = rng.choice(["Samarkand","Bukhara","Dubai"])
        session = rng.randint(3,20)
    elif scenario == "missing_data":
        missing = rng.sample(["device_id","recipient_id","consent_scope","session_seconds"], k=2)
        for field in missing:
            if field == "device_id": device = ""
            elif field == "recipient_id": recipient = ""
            elif field == "consent_scope": consent = ""
            elif field == "session_seconds": session = None
    elif scenario == "contradictory":
        contradictions = ["consent_scope","direction"]
        consent = "none"
        direction = "IN"
    elif scenario == "duplicate_or_transport":
        duplicate = True
    return {
      "event_id": f"SB-{i+1:04d}", "bank_id": bank, "customer_id": customer,
      "transaction_id": tx, "amount": amount, "currency":"UZS",
      "event_time":base.isoformat(), "direction":direction, "device_id":device,
      "recipient_id":recipient, "consent_scope":consent, "session_seconds":session,
      "password_reset_time":reset, "location":location, "missing_fields":missing,
      "contradictions":contradictions, "duplicate_delivery":duplicate,
      "transport_status":"DELIVERED", "delivery_attempts":(2 if duplicate else 1), "scenario_index":i
    }

def generate_dataset(seed=317):
    init_lab()
    rng = random.Random(seed)
    rows=[]
    idx=0
    for scenario,count in ALLOCATIONS:
        for _ in range(count):
            p=_make_payload(idx,scenario,rng)
            p["scenario"] = scenario
            expected = "DATA_REVIEW" if scenario in ("missing_data","contradictory") else (
                "RECHECK" if scenario=="ambiguous_single_signal" else
                "HUMAN_REVIEW" if scenario in ("suspicious_combo","ato","social_engineering","money_mule","device_anomaly") else "MONITOR")
            rows.append((p["event_id"],p["bank_id"],scenario,expected,json.dumps(p,ensure_ascii=False)))
            idx += 1
    rng.shuffle(rows)
    with connect() as c:
        c.execute("DELETE FROM bank_events")
        c.execute("DELETE FROM lab_cases")
        c.execute("DELETE FROM lab_data_reviews")
        c.execute("DELETE FROM lab_audit")
        for eid,bank,scenario,expected,payload in rows:
            c.execute("INSERT INTO bank_events(event_id,bank_id,scenario,expected,payload,state,created_at) VALUES(?,?,?,?,?,'QUEUED',?)",
                      (eid,bank,scenario,expected,payload,datetime.now(timezone.utc).isoformat()))
    run_id="RUN-"+uuid.uuid4().hex[:8].upper()
    set_meta(run_state="READY",generated=len(rows),processed=0,last_error="",run_id=run_id,
             started_at="",finished_at="")
    audit("DATASET_GENERATED",f"{len(rows)} synthetic events; seed={seed}; run={run_id}")
    return len(rows)

def _validate(p):
    required=("event_id","bank_id","customer_id","transaction_id","amount","currency","event_time","direction")
    missing=[k for k in required if p.get(k) in (None,"")]
    if p.get("missing_fields"):
        missing.extend(p["missing_fields"])
    errors=[]
    if not isinstance(p.get("amount"),(int,float)) or p.get("amount",0)<=0: errors.append("Summa noto'g'ri")
    if p.get("direction") not in ("IN","OUT"): errors.append("Pul yo'nalishi noto'g'ri")
    try: datetime.fromisoformat(p["event_time"].replace("Z","+00:00"))
    except Exception: errors.append("Vaqt formati noto'g'ri")
    if p.get("contradictions"): errors.append("Bank maydonlari o'zaro zid: "+", ".join(p["contradictions"]))
    return sorted(set(missing)),errors

def _classify(p, missing, errors):
    if missing or errors:
        return "DATA_REVIEW", {"missing":missing,"errors":errors,"reason":"Ma'lumot to'liq yoki o'zaro mos emas; avtomatik xulosa berilmadi."}
    signals=[]
    if p["amount"] >= 1500000: signals.append("Yuqori summa (kontekst talab qiladi)")
    if p.get("device_id","").startswith(("ATO-","NEW-","SHARED-")): signals.append("Yangi yoki noodatiy qurilma")
    if p.get("recipient_id","").startswith(("NEW-","CALL-","MULE-")): signals.append("Yangi/noodatiy qabul qiluvchi")
    if p.get("session_seconds") is not None and p["session_seconds"]<=15: signals.append("Juda qisqa sessiya")
    if p.get("password_reset_time"): signals.append("Parol tiklangach operatsiya")
    if p.get("consent_scope") in ("unknown","none","device_only"): signals.append("Rozilik doirasi tasdiqlanmagan")
    if p.get("scenario") == "money_mule" or p["recipient_id"].startswith("MULE-"): signals.append("Pul oqimi bo'yicha qo'shimcha tekshiruv")
    # Cross-bank demo match: a repeated pseudonymous device across several synthetic customers.
    if p.get("device_id"):
        with connect() as c:
            linked=[json.loads(r["payload"]) for r in c.execute("SELECT payload FROM bank_events WHERE event_id<>?",(p["event_id"],))]
        same=[x for x in linked if x.get("device_id")==p["device_id"]]
        linked_customers={x.get("customer_id") for x in same if x.get("customer_id")}
        linked_banks={x.get("bank_id") for x in same if x.get("bank_id")}
        if len(linked_customers)>=3:
            signals.append("Bir qurilmaga bir nechta sintetik mijoz profili bog'langan")
        if len(linked_banks)>=2:
            signals.append("Qurilma bir nechta sintetik bank manbasida uchraydi")
    if len(signals)>=2 or p.get("scenario") in ("ato","social_engineering","money_mule"):
        return "HUMAN_REVIEW", {"signals":signals,"reason":"Bir nechta indikator yoki ssenariy belgisi mavjud; bu aybdorlik isboti emas."}
    if len(signals)==1:
        return "RECHECK", {"signals":signals,"reason":"Yakka indikator yetarli xulosa bermaydi; qoida va qo'shimcha kontekst qayta tekshirilsin."}
    return "MONITOR", {"signals":signals,"reason":"Hozircha signal aniqlanmadi; bu xavf yo'q degani emas."}

def _process_one(row):
    p=json.loads(row["payload"])
    missing,errors=_validate(p)
    outcome,detail=_classify(p,missing,errors)
    result={"outcome":outcome,"detail":detail,"source_bank":p["bank_id"],
            "event_id":p["event_id"],"processed_at":datetime.now(timezone.utc).isoformat(),
            "bank_response":("HUMAN_REVIEW_REQUIRED" if outcome=="HUMAN_REVIEW" else "REQUEST_MORE_DATA" if outcome=="DATA_REVIEW" else "RECHECK_REQUIRED" if outcome=="RECHECK" else "MONITORING_RESULT_READY"),
            "duplicate_delivery_detected":bool(p.get("duplicate_delivery",False)),
            "delivery_attempts_simulated":int(p.get("delivery_attempts",1)),
            "idempotency_key":p["event_id"],
            "duplicate_delivery_action":"DEDUPLICATED_BY_EVENT_ID" if p.get("duplicate_delivery") else "SINGLE_DELIVERY",
            "notice":"Sintetik sinov. Real bank ma'lumoti yoki huquqiy xulosa emas; bank APIga yuborilmadi."}
    with connect() as c:
        changed=c.execute("UPDATE bank_events SET state='PROCESSED',result=?,processed_at=? WHERE event_id=? AND state='QUEUED'",
                          (json.dumps(result,ensure_ascii=False),result["processed_at"],p["event_id"])).rowcount
        if not changed:
            return "DUPLICATE_IGNORED"
        if outcome == "HUMAN_REVIEW":
            cid="LAB-CASE-"+uuid.uuid4().hex[:10].upper()
            c.execute("INSERT OR IGNORE INTO lab_cases(case_id,event_id,bank_id,status,reason,created_at) VALUES(?,?,?,?,?,?)",
                      (cid,p["event_id"],p["bank_id"],"OPEN",detail.get("reason","Human review talab qilinadi"),result["processed_at"]))
        elif outcome == "DATA_REVIEW":
            rid="DATA-REVIEW-"+uuid.uuid4().hex[:10].upper()
            reason="Yetishmayotgan maydonlar: "+", ".join(detail.get("missing",[]))+"; tekshiruv xatolari: "+", ".join(detail.get("errors",[]))
            c.execute("INSERT OR IGNORE INTO lab_data_reviews(review_id,event_id,bank_id,status,reason,created_at,review_type) VALUES(?,?,?,?,?,?,?)",
                      (rid,p["event_id"],p["bank_id"],"OPEN",reason,result["processed_at"],"DATA_QUALITY"))
        elif outcome == "RECHECK":
            rid="RECHECK-"+uuid.uuid4().hex[:10].upper()
            c.execute("INSERT OR IGNORE INTO lab_data_reviews(review_id,event_id,bank_id,status,reason,created_at,review_type) VALUES(?,?,?,?,?,?,?)",
                      (rid,p["event_id"],p["bank_id"],"OPEN",detail.get("reason","Noaniq signal qayta tekshirilsin"),result["processed_at"],"UNRESOLVED_SIGNAL"))
    return outcome

def _worker_loop():
    while True:
        state=get_meta().get("run_state","IDLE")
        if state in ("PAUSED","STOPPED","EMERGENCY_STOP","IDLE","READY","COMPLETED","ERROR"):
            return
        if state != "RUNNING":
            time.sleep(.2); continue
        with connect() as c:
            row=c.execute("SELECT * FROM bank_events WHERE state='QUEUED' ORDER BY created_at,event_id LIMIT 1").fetchone()
        if not row:
            set_meta(run_state="COMPLETED",finished_at=datetime.now(timezone.utc).isoformat())
            audit("RUN_COMPLETED","All queued synthetic events processed")
            return
        try:
            _process_one(row)
            with connect() as c:
                count=c.execute("SELECT COUNT(*) FROM bank_events WHERE state='PROCESSED'").fetchone()[0]
            set_meta(processed=count,last_error="")
        except Exception as exc:
            set_meta(run_state="ERROR",last_error=str(exc))
            audit("PROCESSING_ERROR",str(exc))
            return
        time.sleep(.035)

def start_run(resume=False):
    global _worker
    init_lab()
    state=get_meta().get("run_state")
    if state=="EMERGENCY_STOP":
        raise RuntimeError("KILL SWITCH faol. Avval favqulodda holatni tasdiqlangan recovery orqali yeching.")
    if not resume and state in ("IDLE","READY","COMPLETED","STOPPED","ERROR"):
        with connect() as c:
            queued=c.execute("SELECT COUNT(*) FROM bank_events WHERE state='QUEUED'").fetchone()[0]
        if queued==0:
            generate_dataset()
    set_meta(run_state="RUNNING",started_at=get_meta().get("started_at") or datetime.now(timezone.utc).isoformat())
    audit("RUN_RESUMED" if resume else "RUN_STARTED","Synthetic bank event processing started")
    with _lock:
        if _worker is None or not _worker.is_alive():
            _worker=threading.Thread(target=_worker_loop,daemon=True,name="finzanjir-synthetic-bank-worker")
            _worker.start()

def pause_run():
    if get_meta().get("run_state")=="EMERGENCY_STOP":
        raise RuntimeError("KILL SWITCH faol; recovery talab qilinadi")
    set_meta(run_state="PAUSED")
    audit("RUN_PAUSED","Processing paused; unprocessed queue retained")

def stop_run():
    if get_meta().get("run_state")=="EMERGENCY_STOP":
        raise RuntimeError("KILL SWITCH faol; recovery talab qilinadi")
    set_meta(run_state="STOPPED")
    audit("RUN_STOPPED","Processing stopped; unprocessed queue retained")

def emergency_stop(reason="Operator emergency stop"):
    set_meta(run_state="EMERGENCY_STOP",last_error=reason)
    audit("KILL_SWITCH_ACTIVATED",reason)

def recover_emergency(confirmed=False, note=""):
    if not confirmed:
        raise ValueError("Recovery uchun aniq tasdiq kerak")
    if get_meta().get("run_state")!="EMERGENCY_STOP":
        raise RuntimeError("KILL SWITCH faol emas")
    set_meta(run_state="STOPPED",last_error="Emergency holat operator tomonidan ko'rib chiqildi: "+note)
    audit("EMERGENCY_RECOVERY_APPROVED",note or "Operator tasdig'i")
    
def reset_run(confirmed=False):
    if not confirmed: raise ValueError("Reset uchun tasdiq kerak")
    if get_meta().get("run_state")=="EMERGENCY_STOP":
        raise RuntimeError("KILL SWITCH faol; avval recovery talab qilinadi")
    with connect() as c:
        c.execute("DELETE FROM bank_events")
        c.execute("DELETE FROM lab_cases")
        c.execute("DELETE FROM lab_data_reviews")
    set_meta(run_state="IDLE",generated=0,processed=0,last_error="",run_id="",started_at="",finished_at="")
    audit("RUN_RESET","Dataset cleared after explicit confirmation")

def review_case(case_id, outcome, note=""):
    allowed={"REFER_TO_BANK","NO_FRAUD_INDICATION","NEEDS_MORE_INFO","INCONCLUSIVE"}
    if outcome not in allowed:
        raise ValueError("Noto'g'ri Human Review natijasi")
    status="REFERRAL_READY" if outcome=="REFER_TO_BANK" else "CLOSED" if outcome in ("NO_FRAUD_INDICATION","INCONCLUSIVE") else "OPEN"
    bank_status="READY_NOT_SENT" if outcome=="REFER_TO_BANK" else "NOT_REQUIRED"
    stamp=datetime.now(timezone.utc).isoformat()
    with connect() as c:
        changed=c.execute("UPDATE lab_cases SET status=?,review_outcome=?,review_note=?,bank_response_status=?,updated_at=? WHERE case_id=?",
                          (status,outcome,note,bank_status,stamp,case_id)).rowcount
        if not changed:
            raise KeyError("Case topilmadi")
    audit("HUMAN_REVIEW_RECORDED",f"{case_id}: {outcome}; bank_status={bank_status}")

def review_data_ticket(review_id, outcome, note=""):
    allowed={"REQUEST_BANK_DATA","DATA_RECEIVED_RECHECK","RECHECK_RULES","CLOSED_INCONCLUSIVE"}
    if outcome not in allowed:
        raise ValueError("Noto'g'ri Data Review natijasi")
    status="WAITING_BANK_DATA" if outcome=="REQUEST_BANK_DATA" else "READY_FOR_RECHECK" if outcome in ("DATA_RECEIVED_RECHECK","RECHECK_RULES") else "CLOSED"
    stamp=datetime.now(timezone.utc).isoformat()
    with connect() as c:
        changed=c.execute("UPDATE lab_data_reviews SET status=?,review_outcome=?,review_note=?,updated_at=? WHERE review_id=?",
                          (status,outcome,note,stamp,review_id)).rowcount
        if not changed:
            raise KeyError("Data Review yozuvi topilmadi")
    audit("DATA_REVIEW_RECORDED",f"{review_id}: {outcome}")

def snapshot():
    init_lab()
    meta=get_meta()
    with connect() as c:
        counts={r["state"]:r["n"] for r in c.execute("SELECT state,COUNT(*) n FROM bank_events GROUP BY state")}
        totals=c.execute("SELECT COUNT(*) FROM bank_events").fetchone()[0]
        rows=c.execute("SELECT * FROM bank_events ORDER BY processed_at DESC LIMIT 500").fetchall()
        banks=[dict(r) for r in c.execute("SELECT bank_id,COUNT(*) total,SUM(CASE WHEN state='PROCESSED' THEN 1 ELSE 0 END) processed FROM bank_events GROUP BY bank_id")]
        audit_rows=[dict(r) for r in c.execute("SELECT * FROM lab_audit ORDER BY id DESC LIMIT 30")]
        cases=[dict(r) for r in c.execute("SELECT * FROM lab_cases ORDER BY created_at DESC LIMIT 500")]
        data_reviews=[dict(r) for r in c.execute("SELECT * FROM lab_data_reviews ORDER BY created_at DESC LIMIT 100")]
    return {"meta":meta,"counts":counts,"total":totals,"recent":[dict(r) for r in rows],"banks":banks,"audit":audit_rows,"cases":cases,"data_reviews":data_reviews}

def evaluate():
    with connect() as c:
        rows=c.execute("SELECT expected,result FROM bank_events WHERE state='PROCESSED'").fetchall()
    matrix={}
    for r in rows:
        actual=json.loads(r["result"])["outcome"]
        key=f'{r["expected"]} → {actual}'
        matrix[key]=matrix.get(key,0)+1
    return {"processed":len(rows),"confusion":matrix}
