from __future__ import annotations
import json, re, unicodedata
from pathlib import Path
from collections import Counter

KB_PATH = Path(__file__).with_name("knowledge_uz.json")
STOP = set("va yoki bu shu u uchun bilan ham nima qanday qaysi haqida kerak mumkin orqali uning ular bir bor yoq yo'q emas deb".split())
ALIASES = {
 "firibgarlik":"firibgar", "firibgarlikka":"firibgar", "firibgarlikni":"firibgar",
 "shubhali":"shubha", "shubhalilik":"shubha", "tranzaksiya":"operatsiya",
 "operatsiyasi":"operatsiya", "banklar":"bank", "bankning":"bank",
 "ma'lumotlar":"malumot", "ma’lumotlar":"malumot", "ma'lumot":"malumot", "ma’lumot":"malumot",
 "inson":"human", "odam":"human", "ko'rib":"review", "korib":"review",
 "aybdor":"ayb", "aybdorlik":"ayb", "xavflar":"xavf", "signallar":"signal",
 "dalillar":"dalil", "qatlamlar":"qatlam", "tizimi":"tizim", "tizimni":"tizim",
}

def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", str(text)).lower().replace("’","'").replace("ʻ","'")
    text = re.sub(r"[^a-z0-9'\s-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def tokens(text: str):
    out=[]
    for token in normalize(text).split():
        token=ALIASES.get(token,token)
        if len(token)>2 and token not in STOP:
            out.append(token)
    return out

def load_knowledge():
    with KB_PATH.open("r",encoding="utf-8") as f:
        rows=json.load(f)
    if not isinstance(rows,list) or not rows:
        raise ValueError("O'zbek bilimlar bazasi bo'sh yoki noto'g'ri.")
    return rows

def retrieve(question: str, limit: int=4):
    q=tokens(question)
    if not q:
        return []
    qset=set(q)
    scored=[]
    for row in load_knowledge():
        body=tokens(row.get("text",""))
        if not body:
            continue
        counts=Counter(body)
        overlap=qset.intersection(counts)
        if not overlap:
            continue
        # Rare terms weigh more; short cards do not win merely by repeating a word.
        score=sum(1.0 + min(counts[t],3)*0.12 for t in overlap)
        coverage=len(overlap)/max(1,len(qset))
        score=score*(0.65+coverage)
        if len(overlap)>=2 or (len(qset)==1 and len(body)<45 and overlap):
            scored.append((score,coverage,row,sorted(overlap)))
    scored.sort(key=lambda x:(x[0],x[1]),reverse=True)
    return [{"score":round(s,3),"coverage":round(c,3),"id":r["id"],
             "text":r["text"],"approval":r.get("approval","unknown"),
             "source_package":r.get("source_package","V317"),"matched_terms":terms}
            for s,c,r,terms in scored[:limit]]

def answer(question: str):
    hits=retrieve(question)
    if not hits or hits[0]["coverage"] < 0.20 or hits[0]["score"] < 1.5:
        return {"status":"NO_SUFFICIENT_EVIDENCE",
                "answer":"Ichki o‘zbek bilimlar bazasida bu savolga yetarli dalil topilmadi. Faktni taxmin qilib aytmayman. Savolni aniqlashtiring yoki tegishli hujjatni qo‘shing.",
                "evidence":[],"mode":"offline_retrieval_no_external_model"}
    # Extractive answer only: no generated facts are added.
    evidence=hits[:3]
    answer_text="Topilgan loyiha bilimlari:\n" + "\n".join("• "+x["text"] for x in evidence)
    answer_text += "\n\nEslatma: bu yozuvlar V317 paketidan olingan candidate bilimlardir; ular avtomatik ravishda rasmiy tasdiqlangan qoida hisoblanmaydi."
    return {"status":"EVIDENCE_FOUND","answer":answer_text,"evidence":evidence,
            "mode":"offline_extractive_retrieval_no_external_model"}

def self_test():
    checks=[
      ("purpose","FINZANJIR nima va maqsadi nima?","FZ24-61bb2e79bc62e1"),
      ("human","Case inson ko'rigiga yuboriladimi?","FZ24-4afa53ae99c992"),
      ("no_verdict","Shubhali signal odamni aybdor qiladimi?","FZ24-a1bf2d05a3589f"),
      ("privacy","OTP PIN CVV so'rash mumkinmi?","FZ24-6e61f0fcde2fc1"),
      ("no_guess","Marsdagi noma'lum mineralning narxi qancha?","NO_SUFFICIENT_EVIDENCE"),
    ]
    results=[]
    for name,q,expected in checks:
        res=answer(q)
        ids=[x["id"] for x in res["evidence"]]
        passed=(res["status"]=="NO_SUFFICIENT_EVIDENCE") if expected=="NO_SUFFICIENT_EVIDENCE" else expected in ids
        results.append({"test":name,"passed":passed,"status":res["status"],"top_ids":ids[:3]})
    return results
