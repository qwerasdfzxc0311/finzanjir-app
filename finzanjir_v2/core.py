from __future__ import annotations
import json, sqlite3, uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).with_name("finzanjir_v2.sqlite3")
RULESET_VERSION = "0.1.0-provisional"
RULES = {
 "SIG-001":("Summa odatiy diapazondan yuqori",15,"transaction"),
 "SIG-002":("Qisqa vaqtda takroriy operatsiyalar",20,"velocity"),
 "SIG-003":("Kirimdan keyin tez chiqim",25,"fund_flow"),
 "SIG-004":("Yangi qabul qiluvchi",10,"recipient"),
 "SIG-005":("O'xshash summali takroriy o'tkazmalar",15,"structuring"),
 "SIG-006":("Yangi qurilma",15,"device"),
 "SIG-007":("Tarixdan farqli joylashuv",10,"location"),
 "SIG-008":("Qurilmada bir nechta mijoz profili",15,"shared_device"),
 "SIG-010":("Mijoz odatidan tashqari vaqt",5,"behavior"),
 "SIG-011":("Juda qisqa sessiya",5,"session"),
 "SIG-012":("Parol tiklangach tez orada o'tkazma",25,"account_access"),
 "SIG-016":("Rozilik doirasi noaniq yoki mos emas",20,"consent"),
}
@dataclass
class Signal:
 signal_id:str; name:str; weight:int; family:str; explanation:str
 source_fields:list[str]; source_type:str; confidence:str="medium"
 limitation:str="Yakka signal firibgarlikni isbotlamaydi."
@dataclass
class Assessment:
 score:int; band:str; signals:list[Signal]; case_candidate:bool
 reason:str; unknowns:list[str]; rule_version:str=RULESET_VERSION

def now(): return datetime.now(timezone.utc).isoformat(timespec="seconds")
def db(path=DB_PATH):
 c=sqlite3.connect(str(path),timeout=10); c.row_factory=sqlite3.Row
 c.execute("PRAGMA foreign_keys=ON"); return c
def init_db(path=DB_PATH):
 with db(path) as c:
  c.executescript("""
  CREATE TABLE IF NOT EXISTS events(event_id TEXT PRIMARY KEY,customer_ref TEXT NOT NULL,transaction_ref TEXT NOT NULL,amount REAL NOT NULL CHECK(amount>0),currency TEXT NOT NULL,event_time TEXT NOT NULL,device_ref TEXT,location TEXT,recipient_ref TEXT,session_seconds INTEGER,password_reset_time TEXT,consent_scope TEXT NOT NULL,fraud_type TEXT NOT NULL,source_type TEXT NOT NULL,source_note TEXT NOT NULL,payload_json TEXT NOT NULL,created_at TEXT NOT NULL);
  CREATE TABLE IF NOT EXISTS cases(case_id TEXT PRIMARY KEY,event_id TEXT NOT NULL REFERENCES events(event_id),score INTEGER NOT NULL,band TEXT NOT NULL,status TEXT NOT NULL,decision TEXT NOT NULL,assessment_json TEXT NOT NULL,reviewer_note TEXT NOT NULL DEFAULT '',created_at TEXT NOT NULL,updated_at TEXT NOT NULL);
  CREATE TABLE IF NOT EXISTS audit_log(audit_id INTEGER PRIMARY KEY AUTOINCREMENT,actor TEXT NOT NULL,action TEXT NOT NULL,object_ref TEXT NOT NULL,detail TEXT NOT NULL,created_at TEXT NOT NULL);
  CREATE INDEX IF NOT EXISTS idx_ev_customer ON events(customer_ref,event_time);
  CREATE INDEX IF NOT EXISTS idx_ev_device ON events(device_ref,event_time);
  """)
def audit(actor,action,obj,detail,path=DB_PATH):
 with db(path) as c:c.execute("INSERT INTO audit_log(actor,action,object_ref,detail,created_at) VALUES(?,?,?,?,?)",(actor,action,obj,detail,now()))
def add_event(x,path=DB_PATH):
 if float(x["amount"])<=0: raise ValueError("Summa noldan katta bo'lishi kerak.")
 eid=x.get("event_id") or "EVT-"+uuid.uuid4().hex[:10].upper()
 with db(path) as c:
  c.execute("""INSERT INTO events VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(
   eid,str(x["customer_ref"]),str(x["transaction_ref"]),float(x["amount"]),x.get("currency","UZS"),str(x["event_time"]),
   x.get("device_ref") or None,x.get("location") or None,x.get("recipient_ref") or None,
   int(x["session_seconds"]) if x.get("session_seconds") not in (None,"") else None,
   x.get("password_reset_time") or None,str(x.get("consent_scope","unknown")),str(x.get("fraud_type","unknown")),
   str(x.get("source_type","manual_synthetic")),str(x.get("source_note","")),json.dumps(x,ensure_ascii=False),now()))
 audit("system","EVENT_RECORDED",eid,"source="+str(x.get("source_type","manual_synthetic")),path)
 return eid
def event(eid,path=DB_PATH):
 with db(path) as c:r=c.execute("SELECT * FROM events WHERE event_id=?",(eid,)).fetchone()
 return dict(r) if r else None
def events(path=DB_PATH):
 with db(path) as c:return [dict(r) for r in c.execute("SELECT * FROM events ORDER BY event_time DESC")]
def dt(s):
 try:
  d=datetime.fromisoformat(str(s).replace("Z","+00:00"))
  return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
 except (ValueError,TypeError):return None
def assess(eid,path=DB_PATH):
 x=event(eid,path)
 if not x:raise KeyError("Hodisa topilmadi")
 hist=[e for e in events(path) if e["customer_ref"]==x["customer_ref"] and e["event_id"]!=eid]
 same_device=[e for e in events(path) if x["device_ref"] and e["device_ref"]==x["device_ref"] and e["event_id"]!=eid]
 found=[]; unknown=[]
 def add(sid,why,fields,conf="medium"):
  n,w,f=RULES[sid];found.append(Signal(sid,n,w,f,why,fields,x["source_type"],conf))
 t=dt(x["event_time"])
 if len(hist)>=3:
  avg=sum(float(e["amount"]) for e in hist)/len(hist)
  if float(x["amount"])>=avg*5:add("SIG-001",f"Joriy summa {x['amount']:.0f}; tarixiy o'rtacha {avg:.0f}.",["amount","customer_ref"])
 else:unknown.append("Odatiy summa uchun kamida 3 ta tarixiy hodisa yo'q.")
 if t:
  recent=[e for e in hist if dt(e["event_time"]) and abs((t-dt(e["event_time"])).total_seconds())<=300]
  if len(recent)>=2:add("SIG-002",f"5 daqiqada jami {len(recent)+1} ta hodisa.",["event_time","customer_ref"],"high")
  # Direction is not part of the current event schema, so do not infer an incoming/outgoing flow.
  unknown.append("Kirim/chiqim yo'nalishi maydoni yo'q; SIG-003 hozircha hisoblanmaydi.")
 else:unknown.append("Vaqt formati noto'g'ri; vaqt qoidalari cheklangan.")
 recipients={e["recipient_ref"] for e in hist if e["recipient_ref"]}
 if x["recipient_ref"] and recipients and x["recipient_ref"] not in recipients:add("SIG-004","Qabul qiluvchi mijoz tarixida uchramagan.",["recipient_ref","customer_ref"])
 elif not recipients:unknown.append("Qabul qiluvchilar tarixi yo'q.")
 if t:
  window=[e for e in hist if dt(e["event_time"]) and 0<=(t-dt(e["event_time"])).total_seconds()<=3600]
  similar=[e for e in window if abs(float(e["amount"])-float(x["amount"]))<=max(1,float(x["amount"])*.02)]
  if len(similar)>=2:add("SIG-005","Bir soatda o'xshash summali kamida 3 ta o'tkazma.",["amount","event_time"])
 known={e["device_ref"] for e in hist if e["device_ref"]}
 if x["device_ref"] and known and x["device_ref"] not in known:add("SIG-006","Qurilma mijoz tarixida uchramagan.",["device_ref","customer_ref"])
 elif not known:unknown.append("Qurilma tarixi yetarli emas.")
 profiles={e["customer_ref"] for e in same_device}
 if len(profiles)>=2:add("SIG-008",f"Qurilma {len(profiles)} boshqa mijoz profili bilan bog'langan.",["device_ref"],"low")
 places={e["location"] for e in hist if e["location"]}
 if x["location"] and places and x["location"] not in places:add("SIG-007","Joylashuv tarixdagi joylardan farq qiladi; aniqlik tasdiqlanmagan.",["location"],"low")
 elif not x["location"]:unknown.append("Joylashuv ma'lumoti yo'q.")
 if t and hist and t.hour<5 and sum(1 for e in hist if (dt(e["event_time"]) and 7<=dt(e["event_time"]).hour<=22))>=3:add("SIG-010","Operatsiya 00:00–04:59 oralig'ida; tarixda kunduzgi faollik bor.",["event_time"],"low")
 elif not hist:unknown.append("Shaxsiy vaqt odati haqida tarix yo'q.")
 if x["session_seconds"] is not None and int(x["session_seconds"])<=15:add("SIG-011","Sessiya 15 soniya yoki undan qisqa.",["session_seconds"],"low")
 else:unknown.append("Sessiya davomiyligi berilmagan.")
 reset=dt(x["password_reset_time"])
 if reset and t and 0<=(t-reset).total_seconds()<=600:add("SIG-012","Parol tiklangach 10 daqiqa ichida o'tkazma.",["password_reset_time","event_time"])
 elif not reset:unknown.append("Parol tiklash jurnali berilmagan.")
 if x["consent_scope"] in ("none","unknown","device_only"):
  add("SIG-016","Rozilik doirasi aynan shu o'tkazmani qamrab olishi tasdiqlanmagan.",["consent_scope"],"low")
  if x["consent_scope"]=="unknown":unknown.append("Aynan shu o'tkazmaga mijoz roziligi noma'lum.")
 # Keep strongest signal per family to avoid simple duplicate weight stacking.
 families={}
 for s in found:
  if s.family not in families or s.weight>families[s.family].weight:families[s.family]=s
 selected=list(families.values()); score=min(100,sum(s.weight for s in selected))
 band="LOW" if score<25 else "GUARDED" if score<50 else "ELEVATED" if score<75 else "HIGH"
 candidate=score>=40 and len(families)>=2
 reason="Bir nechta signal oilasi: inson ko'rib chiqishi uchun nomzod." if candidate else "Case mezoniga yetmadi; bu xavf yo'q degani emas."
 return Assessment(score,band,selected,candidate,reason,unknown)
def save_assessment(eid,a,path=DB_PATH):
 if not a.case_candidate:
  audit("system","ASSESSMENT_NO_CASE",eid,a.reason,path);return None
 cid="CASE-"+uuid.uuid4().hex[:10].upper(); stamp=now()
 data={"signals":[asdict(s) for s in a.signals],"unknowns":a.unknowns,"reason":a.reason,"rule_version":a.rule_version,"notice":"Provisional review heuristic; not proof or blocking instruction."}
 with db(path) as c:c.execute("INSERT INTO cases VALUES(?,?,?,?,?,?,?,?,?,?)",(cid,eid,a.score,a.band,"OPEN","PENDING_HUMAN_REVIEW",json.dumps(data,ensure_ascii=False),"",stamp,stamp))
 audit("system","CASE_OPENED_FOR_REVIEW",cid,"event="+eid+"; score="+str(a.score),path);return cid
def cases(status=None,path=DB_PATH):
 with db(path) as c:
  rows=c.execute("SELECT * FROM cases WHERE status=? ORDER BY created_at DESC",(status,)).fetchall() if status else c.execute("SELECT * FROM cases ORDER BY created_at DESC").fetchall()
 out=[]
 for r in rows:
  d=dict(r);d["assessment"]=json.loads(d.pop("assessment_json"));out.append(d)
 return out
def review(cid,outcome,note,reviewer,path=DB_PATH):
 allowed={"NEEDS_MORE_INFO","NO_FRAUD_INDICATION","REFERRED_TO_BANK","CLOSED_INCONCLUSIVE"}
 if outcome not in allowed:raise ValueError("Noto'g'ri review natijasi.")
 status="OPEN" if outcome=="NEEDS_MORE_INFO" else "CLOSED"
 with db(path) as c:
  if not c.execute("SELECT 1 FROM cases WHERE case_id=?",(cid,)).fetchone():raise KeyError("Case topilmadi.")
  c.execute("UPDATE cases SET status=?,decision=?,reviewer_note=?,updated_at=? WHERE case_id=?",(status,outcome,note,now(),cid))
 audit(reviewer,"HUMAN_REVIEW_RECORDED",cid,"outcome="+outcome+"; "+note,path)
def audit_list(limit=100,path=DB_PATH):
 with db(path) as c:return [dict(r) for r in c.execute("SELECT * FROM audit_log ORDER BY audit_id DESC LIMIT ?",(limit,))]
def seed_demo(path=DB_PATH):
 with db(path) as c:
  if c.execute("SELECT COUNT(*) FROM events WHERE source_type='synthetic_demo'").fetchone()[0]:return []
 base=datetime(2026,11,6,10,0,tzinfo=timezone.utc); ids=[]
 samples=[
 ("DEMO-C1","BASE1",100000,"D-OLD","Tashkent","R-OLD",300,None,"transfer"),
 ("DEMO-C1","BASE2",120000,"D-OLD","Tashkent","R-OLD",240,None,"transfer"),
 ("DEMO-C1","BASE3",90000,"D-OLD","Tashkent","R-OLD",180,None,"transfer"),
 ("DEMO-C1","DEMO-ATO",12000000,"D-NEW","Dubai","R-NEW",8,"2026-11-06T09:58:00+00:00","unknown"),
 ("DEMO-C2","DEMO-NORMAL",250000,"D-B","Samarqand","R-X",240,None,"transfer")]
 for i,(cust,tx,amt,dev,loc,rec,secs,reset,consent) in enumerate(samples):
  d=base.replace(minute=base.minute+i)
  ids.append(add_event({"customer_ref":cust,"transaction_ref":tx,"amount":amt,"event_time":d.isoformat(),"device_ref":dev,"location":loc,"recipient_ref":rec,"session_seconds":secs,"password_reset_time":reset,"consent_scope":consent,"fraud_type":"unknown","source_type":"synthetic_demo","source_note":"Demo; real bank ma'lumoti emas."},path))
 return ids
def self_checks():
 return [{"test":"Rule weights 0..30","result":"PASS" if all(0<=v[1]<=30 for v in RULES.values()) else "FAIL"},{"test":"Each rule has a family","result":"PASS" if all(v[2] for v in RULES.values()) else "FAIL"},{"test":"No blocking review outcome","result":"PASS" if not any("BLOCK" in x for x in ("NEEDS_MORE_INFO","NO_FRAUD_INDICATION","REFERRED_TO_BANK","CLOSED_INCONCLUSIVE")) else "FAIL"},{"test":"Rule version is provisional","result":"PASS" if "provisional" in RULESET_VERSION else "FAIL"}]
