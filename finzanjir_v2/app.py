from __future__ import annotations
from datetime import datetime, timezone
import streamlit as st
from core import (DB_PATH,RULESET_VERSION,RULES,add_event,assess,event,audit_list,cases,events,
                  init_db,review,self_checks,save_assessment,seed_demo)

st.set_page_config(page_title="FINZANJIR | Yangi prototip",page_icon="🛡️",layout="wide")
init_db()
st.markdown("""
<style>
.stApp{background:#0b1220;color:#e8edf5}
[data-testid="stSidebar"]{background:#111b2d}
div[data-testid="stMetric"]{background:#142137;border:1px solid #293b57;padding:12px;border-radius:10px}
.panel{background:#142137;border:1px solid #293b57;border-radius:12px;padding:14px}
</style>
""",unsafe_allow_html=True)
st.title("🛡️ FINZANJIR")
st.caption("Konsepsiyaga mos alohida prototip • "+RULESET_VERSION)
st.warning("SINOV MUHITI: banklarga ulanmagan, real bank dalillarini olmaydi va karta/tranzaksiyalarni bloklamaydi. Ball aybdorlik yoki firibgarlik ehtimolining kalibrlangan foizi emas.")
with st.sidebar:
 st.header("Ish panellari")
 page=st.radio("Bo'lim",["Boshqaruv paneli","Hodisa va signal tahlili","Case / inson nazorati","Aloqalar grafigi","Signal reyestri","Audit jurnali","Sinov markazi","16 qatlam holati"])
 st.divider()
 st.caption("Lokal SQLite • Pseudonim test ma'lumotlari")
 if st.button("Demo ma'lumotlarni qo'shish",use_container_width=True):
  ids=seed_demo()
  st.success(str(len(ids))+" ta sintetik hodisa qo'shildi." if ids else "Demo ma'lumotlar avval qo'shilgan.")
evs=events(); cs=cases(); opened=[c for c in cs if c["status"]=="OPEN"]
if page=="Boshqaruv paneli":
 st.subheader("Tizim ko'rsatkichlari")
 a,b,c,d=st.columns(4)
 a.metric("Hodisalar",len(evs));b.metric("Ochiq Case",len(opened));c.metric("Yopilgan Case",len(cs)-len(opened));d.metric("Signal qoidalari",len(RULES))
 st.markdown('<div class="panel"><b>Jarayon:</b> Hodisa → Ma’lumot sifati → Signallar → Dalillar va noma’lumlar → Case nomzodi → Inson ko‘rib chiqishi → Audit</div>',unsafe_allow_html=True)
 st.markdown("### So'nggi hodisalar")
 if evs:st.dataframe([{"Event":e["event_id"],"Mijoz ref":e["customer_ref"],"Tranzaksiya":e["transaction_ref"],"Summa":e["amount"],"Manba":e["source_type"],"Rozilik":e["consent_scope"]} for e in evs[:15]],use_container_width=True,hide_index=True)
 else:st.info("Hozircha hodisa yo'q. Demo qo'shing yoki yangi hodisa kiriting.")
 st.caption("FP/FN/precision/recall ko'rsatilmaydi: tasdiqlangan ground-truth dataset mavjud emas.")
elif page=="Hodisa va signal tahlili":
 st.subheader("Yangi hodisa kiritish")
 st.caption("Faqat ruxsatli, shaxsni aniqlamaydigan test ma'lumotlaridan foydalaning.")
 with st.form("event"):
  x1,x2,x3=st.columns(3)
  customer=x1.text_input("Mijoz pseudonim ID","TEST-C01");tx=x2.text_input("Tranzaksiya ID","TX-TEST-01");amount=x3.number_input("Summa UZS",min_value=1.0,value=1500000.0,step=50000.0)
  x4,x5,x6=st.columns(3)
  event_time=x4.text_input("Vaqt ISO 8601",datetime.now(timezone.utc).isoformat(timespec="seconds"));device=x5.text_input("Qurilma pseudonim ID","DEV-TEST");location=x6.text_input("Joylashuv","Tashkent")
  x7,x8,x9=st.columns(3)
  recipient=x7.text_input("Qabul qiluvchi pseudonim ID","REC-TEST");session=x8.number_input("Sessiya soniya",min_value=0,value=45);consent=x9.selectbox("Rozilik doirasi",["transfer","account_and_transfer","device_only","none","unknown"])
  x10,x11=st.columns(2)
  reset=x10.text_input("Parol tiklash vaqti ISO (ixtiyoriy)","");fraud=x11.selectbox("Sinov ssenariysi (yorliq, hukm emas)",["unknown","ATO","social_engineering","money_mule","card_fraud","other"])
  note=st.text_input("Manba izohi","Qo'lda kiritilgan sintetik test")
  submit=st.form_submit_button("Saqlash va tahlil qilish",type="primary",use_container_width=True)
 if submit:
  try:
   eid=add_event({"customer_ref":customer.strip(),"transaction_ref":tx.strip(),"amount":amount,"event_time":event_time.strip(),"device_ref":device.strip(),"location":location.strip(),"recipient_ref":recipient.strip(),"session_seconds":session,"password_reset_time":reset.strip() or None,"consent_scope":consent,"fraud_type":fraud,"source_type":"manual_synthetic","source_note":note})
   a=assess(eid);cid=save_assessment(eid,a)
   st.success("Hodisa saqlandi: "+eid);st.metric("Vaqtinchalik ball",str(a.score)+"/100",a.band);st.write(a.reason)
   if cid:st.warning("Inson ko'rib chiqishi uchun Case ochildi: "+cid)
   else:st.info("Case mezoniga yetmadi. Bu xavf yo'q degani emas.")
   st.markdown("#### Aniqlangan signallar")
   if a.signals:st.dataframe([{"ID":s.signal_id,"Signal":s.name,"Vazn":s.weight,"Oila":s.family,"Ishonch":s.confidence,"Izoh":s.explanation,"Manba maydonlari":", ".join(s.source_fields)} for s in a.signals],use_container_width=True,hide_index=True)
   else:st.info("Signal aniqlanmadi.")
   st.markdown("#### Noma'lumlar / yetishmayotgan ma'lumotlar")
   for u in a.unknowns:st.write("• "+u)
  except Exception as e:st.error("Saqlash xatosi: "+str(e))
elif page=="Case / inson nazorati":
 st.subheader("Case boshqaruvi")
 if not cs:st.info("Hozircha Case yo'q. Demo ma'lumotlarni qo'shing.")
 for case in cs:
  with st.expander(case["case_id"]+" | "+case["band"]+" | "+str(case["score"])+"/100 | "+case["status"]):
   ev=event(case["event_id"]);st.write("Tranzaksiya: "+ev["transaction_ref"]+" • "+format(ev["amount"],",.0f")+" "+ev["currency"])
   st.write("Holat: "+case["decision"])
   st.markdown("**Signal dalillari**")
   for s in case["assessment"]["signals"]:st.write("- "+s["signal_id"]+": "+s["explanation"]+" (manba: "+", ".join(s["source_fields"])+")")
   st.markdown("**Noma'lumlar**")
   for u in case["assessment"]["unknowns"]:st.write("- "+u)
   st.info("Case aybdorlikni anglatmaydi. Avtomatik bloklash mavjud emas.")
   if case["status"]=="OPEN":
    with st.form("review-"+case["case_id"]):
     outcome=st.selectbox("Inson ko'rib chiqish natijasi",["NEEDS_MORE_INFO","NO_FRAUD_INDICATION","REFERRED_TO_BANK","CLOSED_INCONCLUSIVE"],format_func=lambda v:{"NEEDS_MORE_INFO":"Qo'shimcha ma'lumot kerak","NO_FRAUD_INDICATION":"Hozircha firibgarlik belgisi tasdiqlanmadi","REFERRED_TO_BANK":"Bank mutaxassisiga yuborildi","CLOSED_INCONCLUSIVE":"Aniq xulosa yo'q — yopildi"}[v])
     reviewer=st.text_input("Ko'rib chiquvchi ID","reviewer-demo");note=st.text_area("Izoh / asos")
     if st.form_submit_button("Natijani auditga qayd etish"):
      review(case["case_id"],outcome,note,reviewer);st.success("Natija qayd etildi.");st.rerun()
elif page=="Aloqalar grafigi":
 st.subheader("Pseudonim atributlar bo'yicha aloqa grafigi")
 st.caption("Bu banklararo graf emas. Lokal test bazasidagi bir xil atributlarni ko'rsatadi; bog'liqlik aybdorlik isboti emas.")
 if evs:
  selected=st.selectbox("Hodisani tanlang",[e["event_id"] for e in evs]);root=event(selected)
  related=[e for e in evs if e["event_id"]!=selected and ((root["device_ref"] and e["device_ref"]==root["device_ref"]) or (root["recipient_ref"] and e["recipient_ref"]==root["recipient_ref"]) or e["customer_ref"]==root["customer_ref"])]
  st.graphviz_chart('''
  graph G { graph [bgcolor="transparent"]; node [style=filled,fontname="Arial"];
   "Hodisa" [label="Hodisa\n'''+root["transaction_ref"]+'''",fillcolor="#f4b942"];
   "Mijoz" [label="Mijoz ref\n'''+root["customer_ref"]+'''",fillcolor="#9bc2e6"];
   "Qurilma" [label="Qurilma ref\n'''+(root["device_ref"] or "noma'lum")+'''",fillcolor="#9bc2e6"];
   "Qabul qiluvchi" [label="Qabul qiluvchi\n'''+(root["recipient_ref"] or "noma'lum")+'''",fillcolor="#9bc2e6"];
   "Hodisa" -- "Mijoz"; "Hodisa" -- "Qurilma"; "Hodisa" -- "Qabul qiluvchi";
  }''')
  st.write("Mos atributli boshqa hodisalar: "+str(len(related)))
  if related:st.dataframe([{"Event":e["event_id"],"Mijoz":e["customer_ref"],"Qurilma":e["device_ref"],"Qabul qiluvchi":e["recipient_ref"]} for e in related],use_container_width=True,hide_index=True)
 else:st.info("Graf uchun hodisalar yo'q.")
elif page=="Signal reyestri":
 st.subheader("Signal reyestri")
 st.caption("Vaznlar vaqtinchalik muhandislik taxmini; mutaxassislar va bank ma'lumotlari bilan kalibrlanmagan.")
 st.dataframe([{"ID":k,"Signal":v[0],"Vazn":v[1],"Oila":v[2]} for k,v in RULES.items()],use_container_width=True,hide_index=True)
 st.write("Signal ≠ isbot. Har bir signal manba maydonlari, ishonch darajasi va cheklovi bilan ko'riladi.")
elif page=="Audit jurnali":
 st.subheader("Audit jurnali")
 rows=audit_list(200)
 if rows:st.dataframe(rows,use_container_width=True,hide_index=True)
 else:st.info("Audit yozuvlari yo'q.")
elif page=="Sinov markazi":
 st.subheader("Sinov markazi")
 results=self_checks();passed=sum(x["result"]=="PASS" for x in results)
 a,b,c=st.columns(3);a.metric("Tekshiruv",len(results));b.metric("O'tdi",passed);c.metric("Xato",len(results)-passed)
 st.dataframe(results,use_container_width=True,hide_index=True)
 st.caption("Bu lokal invariant testlari; real bank aniqligi yoki production tayyorligini isbotlamaydi.")
 if st.button("Demo hodisalarni tahlil qilib Case nomzodlarini yaratish"):
  ids=seed_demo()
  for eid in ids:
   result=assess(eid);save_assessment(eid,result)
  st.success("Demo hodisalar baholandi.");st.rerun()
elif page=="16 qatlam holati":
 st.subheader("Konsepsiya qatlamlari: amaldagi holat")
 layers=[
 ("L01","Dalil va manba","Qisman","Manba turi, izoh, vaqt, pseudonim ID; tashqi imzo yo'q."),
 ("L02","Ma'lumot sifati","Qisman","Majburiy maydon va summa tekshiruvi; to'liq schema validation yo'q."),
 ("L03","Signal / risk tahlili","Demo","Deterministik qoidalar; vaznlar kalibrlanmagan."),
 ("L04","Inson nazorati","Demo","Review natijasi; real IAM/SSO yo'q."),
 ("L05","Qoidalar boshqaruvi","Qisman","Versiya bor; tasdiqlash workflow yo'q."),
 ("L06","Maxfiylik","Qisman","Pseudonim test ID; production encryption/key management yo'q."),
 ("L07","Avtomatlashtirish","Demo","Faqat lokal tahlil va Case nomzodi; tashqi amal yo'q."),
 ("L08","Case va dalil boshqaruvi","Qisman","Signal, manba, noma'lum va review natijasi saqlanadi."),
 ("L09","Fuqaro shaffofligi","Yo'q","Fuqaro portali ishlab chiqilmagan."),
 ("L10","Hayotiy sikl","Qisman","Lokal SQLite; retention/arxiv siyosati yo'q."),
 ("L11","Hodisaga javob","Yo'q","Incident runbook va kill switch yo'q."),
 ("L12","AI ishonchliligi","Yo'q","AI qaror moduli ataylab kiritilmagan."),
 ("L13","Audit","Qisman","Asosiy amallar qayd etiladi; o'zgarmas tashqi audit yo'q."),
 ("L14","Banklararo integratsiya","Yo'q","API yoki bank ma'lumoti yo'q."),
 ("L15","Fraud Graph / cross-match","Demo","Lokal pseudonim atributlar; banklararo graf emas."),
 ("L16","KPI / sifat","Qisman","Operatsion hisoblagichlar; labelled dataset yo'q.")]
 st.dataframe([{"Qatlam":a,"Nomi":b,"Holat":c,"Cheklov":d} for a,b,c,d in layers],use_container_width=True,hide_index=True)
 st.error("16 qatlam to'liq bajarilgan deb da'vo qilinmaydi. Jadval ayni prototipdagi real holatni ehtiyotkor ko'rsatadi.")
st.divider()
st.caption("FINZANJIR • Concept-aligned prototype • Sinov muhiti; bank pilotiga yoki productionga tayyor deb e'lon qilinmaydi.")
