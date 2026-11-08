from __future__ import annotations
import sys, json
from pathlib import Path
import streamlit as st
from streamlit_autorefresh import st_autorefresh
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"finzanjir_v2"))
sys.path.insert(0,str(HERE))
import laboratory as lab
import offline_ai
import visitor_analytics as visitors
import visitor_pages

st.set_page_config(page_title="FINZANJIR v3 | Sinov muhiti",page_icon="🛡️",layout="wide",initial_sidebar_state="collapsed")
lab.init_lab()
st.markdown("""
<style>
.stApp{background:#0b1220;color:#e8edf5}
[data-testid="stSidebar"]{background:#111b2d}
div[data-testid="stMetric"]{background:#142137;border:1px solid #293b57;padding:14px;border-radius:12px}
.panel{background:#142137;border:1px solid #293b57;border-radius:14px;padding:16px;line-height:1.65}
div[data-testid="stExpander"]{border:1px solid #293b57;border-radius:12px}
.stButton>button{border-radius:10px;min-height:2.7rem;font-weight:600}
h1,h2,h3{letter-spacing:-.02em}
</style>
""",unsafe_allow_html=True)
st.title("🛡️ FINZANJIR")
st.caption("v3 · O‘zbek tilidagi sinov prototipi · haqiqiy bank tizimiga ulanmagan")
st.warning("MUHIM: bu muhit faqat sun’iy ma’lumotlar bilan ishlaydi. Haqiqiy bank yoki mijoz ma’lumotlari yo‘q. Signal aybdorlik isboti emas; karta yoki operatsiyani avtomatik bloklash funksiyasi mavjud emas.")
st.markdown('<div class="panel"><b>Bu prototip nima qiladi?</b><br>Sun’iy bank hodisalarini qabul qiladi, ma’lumot sifatini tekshiradi va zarur holatlarni inson ko‘rigiga tayyorlaydi.<br><b>Nima qilmaydi?</b><br>Haqiqiy pulga tegmaydi, bankka buyruq yubormaydi va hech kimni avtomatik aybdor deb topmaydi.</div>',unsafe_allow_html=True)
# Ochiq namoyish bo'limlari. Muallif analitikasi alohida URL va parol bilan himoyalangan.
author_view = st.query_params.get("view","") == "author"
public_pages = [
    "Boshqaruv paneli",
    "Sun'iy bank laboratoriyasi",
    "Hodisalar va Case",
    "Signal reyestri",
    "Aloqalar grafigi",
    "Audit jurnali",
    "16 qatlam holati",
    "FINZANJIR AI (o'zbekcha)",
    "AI sinovlari",
    "Arxitektura va chegaralar",
    "Banklararo tahlil (sintetik)",
    "KPI dashboard",
    "Fuqaro uchun tushuntirish (demo)",
    "Tashrifchi fikri",
]
home_page = "Bosh sahifa"
if author_view:
    page = "Muallif analitikasi"
else:
    if st.session_state.get("v3_active_page") not in [home_page, *public_pages]:
        st.session_state["v3_active_page"] = home_page
    page = st.session_state["v3_active_page"]
    if page != home_page:
        selected = st.sidebar.selectbox("Bo'limga o'tish", public_pages,
            index=public_pages.index(page), key="v3_sidebar_navigation")
        if selected != page:
            st.session_state["v3_active_page"] = selected
            st.rerun()
        if st.sidebar.button("← Bosh sahifaga qaytish", use_container_width=True):
            st.session_state["v3_active_page"] = home_page
            st.rerun()
        st.sidebar.caption("Ochiq namoyish: faqat sintetik ma'lumotlar.")
    st.caption("Ochiq namoyish: loyiha panellari va sintetik jarayonlar barcha tashrifchilar uchun ochiq. Muallif analitikasi va boshqa tashrifchilarning maxfiy fikrlari yopiq.")
# Privacy-minimal, per-app-session analytics. No IP/GPS or raw user-agent is stored.
if "visitor_session_id" not in st.session_state:
    import uuid
    st.session_state["visitor_session_id"] = uuid.uuid4().hex
try:
    visitor_secret = st.secrets["visitor_analytics"]["session_hmac_secret"]
    visitor_ua = st.context.headers.get("User-Agent", "")
    import time
    now = time.time()
    last = st.session_state.get("visitor_last_page_event", {})
    if last.get("page") != page or now - last.get("time", 0) >= 30:
        visitors.record_page_view(st.session_state["visitor_session_id"], page, visitor_ua, visitor_secret)
        st.session_state["visitor_last_page_event"] = {"page": page, "time": now}
except Exception:
    pass
st.sidebar.divider()
st.sidebar.caption("Tashqi AI API ishlatilmaydi. AI hozircha dalilga asoslangan lokal qidiruv; generativ LLM emas.")
if page in ("Boshqaruv paneli","Sun'iy bank laboratoriyasi","Hodisalar va Case"):
    st_autorefresh(interval=1200,key="finzanjir-live-refresh")
if page == "Muallif analitikasi":
    st.sidebar.info("Muallif paneli ommaviy menyuda ko‘rsatilmaydi. Kirish parol bilan himoyalangan.")

if page == home_page:
    st.subheader("Ochiq namoyish markazi")
    st.write("Quyidagi bo'limlardan birini tanlab, FINZANJIR prototipining turli qismlarini ko'rishingiz mumkin.")
    st.info("Bu sinov prototipi: barcha hodisalar sintetik. Haqiqiy bank tizimiga ulanmagan, pul o'tkazmaydi va karta yoki operatsiyalarni avtomatik bloklamaydi.")
    cards = [
        ("Boshqaruv paneli", "Umumiy holat, sun'iy hodisalar va jarayon ko'rsatkichlari."),
        ("Sun'iy bank laboratoriyasi", "4 ta xayoliy bank va 400 ta sintetik hodisa bilan sinov."),
        ("Hodisalar va Case", "Ma'lumot tekshiruvi, Case va Human Review jarayoni."),
        ("Signal reyestri", "Signal turlari va ularni tekshirish uchun zarur maydonlar."),
        ("Aloqalar grafigi", "Sintetik pseudonimlar orasidagi atribut mosliklari."),
        ("Audit jurnali", "Laboratoriya jarayonida qayd etilgan amallar."),
        ("16 qatlam holati", "Har bir qatlamning joriy Demo/Qisman/Yo'q holati."),
        ("FINZANJIR AI (o'zbekcha)", "Mahalliy bilim qidiruvi va ixtiyoriy internet tadqiqoti."),
        ("AI sinovlari", "O'zbekcha retrieval javoblari uchun regression sinovlari."),
        ("Arxitektura va chegaralar", "Mavjud imkoniyatlar, cheklovlar va keyingi ishlar."),
        ("Banklararo tahlil (sintetik)", "Sun'iy bank manbalari orasidagi pseudonim atribut mosliklari."),
        ("KPI dashboard", "Jarayon ko'rsatkichlari; aniqlik yoki real firibgarlik darajasi emas."),
        ("Fuqaro uchun tushuntirish (demo)", "Signal, Case va inson ko'rigi fuqaro uchun sodda tilda."),
        ("Tashrifchi fikri", "Maxfiy fikr yuborish sahifasi; qabul qilish faqat xavfsiz sozlanganda yoqiladi."),
    ]
    for start in range(0, len(cards), 3):
        columns = st.columns(3)
        for column, item in zip(columns, cards[start:start + 3]):
            label, description = item
            with column:
                with st.container(border=True):
                    st.markdown("### " + label)
                    st.caption(description)
                    if st.button("Bo'limni ochish", key="v3-home-" + label, use_container_width=True):
                        st.session_state["v3_active_page"] = label
                        st.rerun()

if page=="Boshqaruv paneli":
    snap=lab.snapshot(); meta=snap["meta"]; counts=snap["counts"]
    st.subheader("Loyiha holati")
    st.caption("Bu sahifadagi raqamlar faqat sun’iy hodisalarga tegishli.")
    with st.expander("Ko‘rsatkichlarni qanday tushunish kerak?"):
        st.write("Jami — yaratilgan sun’iy hodisalar. Qayta ishlangan — tekshiruvdan o‘tganlari. Navbatda — hali ishlanmaganlari. Jarayon holati — laboratoriyaning joriy ish rejimi.")
    a,b,c,d=st.columns(4)
    a.metric("Sintetik hodisalar",snap["total"])
    b.metric("Qayta ishlangan",counts.get("PROCESSED",0))
    c.metric("Navbatda",counts.get("QUEUED",0))
    d.metric("Jarayon holati",meta.get("run_state","IDLE"))
    st.markdown('<div class="panel"><b>Oqim:</b> Sun’iy bank → Qabul qilish → Validation → Signal tahlili → Case / qayta tekshiruv / kuzatuv → Javob paketi → Audit</div>',unsafe_allow_html=True)
    st.subheader("Bank manbalari")
    if snap["banks"]: st.dataframe(snap["banks"],use_container_width=True,hide_index=True)
    else: st.info("Laboratoriya hali ishga tushmagan.")
    st.subheader("Oxirgi hodisalar")
    if snap["recent"]:
        st.dataframe([{"ID":r["event_id"],"Bank":r["bank_id"],"Ssenariy":r["scenario"],"Holat":r["state"],"Natija":r["result"][:160]} for r in snap["recent"]],use_container_width=True,hide_index=True)
    else: st.info("Hozircha hodisa yo'q.")

elif page=="Sun'iy bank laboratoriyasi":
    st.subheader("Sun’iy bank laboratoriyasi")
    st.caption("4 ta xayoliy bankdan kelgandek yaratilgan 400 ta hodisa sinovdan o‘tkaziladi. Bu haqiqiy bank integratsiyasi emas.")
    with st.expander("Tugmalar nimani anglatadi?"):
        st.write("START — boshlash. PAUSE — vaqtincha to‘xtatish. STOP — ishlovni to‘xtatib, navbatni saqlash. RESUME — davom ettirish. RESET — sinov ma’lumotlarini o‘chirib, yangi sikl boshlash. KILL SWITCH — favqulodda to‘xtatish; qayta yoqish uchun alohida tasdiq kerak.")
    st.write("4 ta sun'iy bankdan jami 400 ta oldindan belgilangan sintetik holat keladi. Start bosilganda fon jarayoni hodisalarni avtomatik qayta ishlaydi.")
    snap=lab.snapshot(); meta=snap["meta"]; counts=snap["counts"]
    a,b,c,d=st.columns(4)
    a.metric("Jami",snap["total"]); b.metric("Qayta ishlangan",counts.get("PROCESSED",0))
    c.metric("Navbat",counts.get("QUEUED",0)); d.metric("Holat",meta.get("run_state","IDLE"))
    progress=(counts.get("PROCESSED",0)/max(1,snap["total"]))
    st.progress(min(1.0,progress),text=f"{counts.get('PROCESSED',0)} / {snap['total']} hodisa")
    x,y,z=st.columns(3)
    if x.button("▶ START — boshlash",type="primary",use_container_width=True,disabled=meta.get("run_state")=="EMERGENCY_STOP"):
        lab.start_run(resume=False); st.rerun()
    if y.button("Ⅱ PAUSE — vaqtincha to'xtatish",use_container_width=True,disabled=meta.get("run_state")=="EMERGENCY_STOP"):
        lab.pause_run(); st.rerun()
    if z.button("■ STOP — to'liq to'xtatish",use_container_width=True,disabled=meta.get("run_state")=="EMERGENCY_STOP"):
        lab.stop_run(); st.rerun()
    x,y,z=st.columns(3)
    if x.button("↻ RESUME — davom ettirish",use_container_width=True,disabled=meta.get("run_state")=="EMERGENCY_STOP"):
        lab.start_run(resume=True); st.rerun()
    if y.button("Yangilash",use_container_width=True): st.rerun()
    confirm=st.checkbox("Navbat va natijalarni o'chirishga roziman")
    if z.button("RESET — yangi sikl",disabled=(not confirm or meta.get("run_state") in ("RUNNING","EMERGENCY_STOP")),use_container_width=True):
        lab.reset_run(confirmed=confirm); st.rerun()
    st.caption("PAUSE/STOP navbatda qolgan hodisalarni o'chirmaydi. RESUME ularni davom ettiradi. RESET alohida tasdiq talab qiladi.")
    st.divider()
    k1,k2=st.columns(2)
    if k1.button("⛔ KILL SWITCH — favqulodda to'xtatish",type="secondary",use_container_width=True,disabled=meta.get("run_state")=="EMERGENCY_STOP"):
        lab.emergency_stop("Operator favqulodda to'xtatishni faollashtirdi"); st.rerun()
    recovery_ok=st.checkbox("Favqulodda holat ko'rib chiqildi; navbatni saqlab tiklashga ruxsat beraman")
    if k2.button("Emergency Recovery — qulfni yechish",use_container_width=True,disabled=(not recovery_ok or meta.get("run_state")!="EMERGENCY_STOP")):
        lab.recover_emergency(confirmed=recovery_ok,note="Operator UI orqali recovery tasdiqladi"); st.rerun()
    if meta.get("last_error"): st.error("Jarayon xatosi: "+meta["last_error"])
    st.subheader("400 ta sinov holati taqsimoti")
    distribution={}
    for event_row in snap["recent"]:
        key=event_row["scenario"]
        distribution[key]=distribution.get(key,0)+1
    if distribution:
        st.dataframe([{"Ssenariy":k,"Hodisalar":v} for k,v in sorted(distribution.items())],use_container_width=True,hide_index=True)
    st.caption("Run ID: "+str(meta.get("run_id","—")))
    st.subheader("Banklar bo'yicha qabul holati")
    if snap["banks"]: st.dataframe(snap["banks"],use_container_width=True,hide_index=True)
    st.subheader("Jarayon auditi")
    if snap["audit"]: st.dataframe(snap["audit"],use_container_width=True,hide_index=True)

elif page=="Hodisalar va Case":
    st.caption("Case — inson ko‘rib chiqishi uchun ochilgan ish yozuvi. Bu aybdorlik haqida yakuniy qaror emas.")
    snap=lab.snapshot()
    st.subheader("Qayta ishlangan hodisalar")
    rows=snap["recent"]
    if rows:
        display=[]
        for r in rows:
            result={}
            try: result=json.loads(r["result"]) if r["result"] else {}
            except Exception: pass
            detail=result.get("detail",{})
            quality=("Yetishmayotgan: "+", ".join(detail.get("missing",[]))+"; xato: "+", ".join(detail.get("errors",[]))) if result.get("outcome")=="DATA_REVIEW" else "Tekshirildi"
            display.append({"Hodisa":r["event_id"],"Bank":r["bank_id"],"Ssenariy":r["scenario"],"Kutilgan":r["expected"],"Amaldagi":result.get("outcome","—"),"Ma'lumot sifati":quality,"Bank javobi":result.get("bank_response","—"),"Dublikat":result.get("duplicate_delivery_action","—"),"Holat":r["state"]})
        st.dataframe(display,use_container_width=True,hide_index=True)
    else: st.info("Hali hodisa kelmagan. Laboratoriyada START bosing.")
    evaluation=lab.evaluate()
    st.subheader("Kutilgan va amaldagi yo'nalishlar taqqoslanishi")
    st.metric("Taqqoslash uchun qayta ishlangan hodisalar",evaluation["processed"])
    if evaluation["confusion"]:
        st.dataframe([{"Kutilgan yo'nalish → Amaldagi yo'nalish":k,"Soni":v} for k,v in evaluation["confusion"].items()],use_container_width=True,hide_index=True)
    st.caption("Kutilgan yorliqlar ham sintetik taxmin. Bu jadval aniqlik/precision/recall isboti emas; mutaxassis tasdiqlagan ground-truth talab qilinadi.")
    st.subheader("Human Review uchun ochilgan sintetik Case'lar")
    if snap.get("cases"):
        st.dataframe(snap["cases"],use_container_width=True,hide_index=True)
        for case in snap["cases"]:
            with st.expander(case["case_id"]+" · "+case["status"]):
                st.write(case["reason"])
                st.caption("Bankka yuborish faqat inson ko'rigidan keyin javob paketi sifatida tayyorlanadi; haqiqiy API jo'natmasi yo'q.")
                choice=st.selectbox("Inson ko'rigi natijasi",["REFER_TO_BANK","NO_FRAUD_INDICATION","NEEDS_MORE_INFO","INCONCLUSIVE"],key="human-"+case["case_id"])
                note=st.text_area("Asos / izoh",key="note-"+case["case_id"])
                if st.button("Human Review natijasini saqlash",key="save-"+case["case_id"]):
                    lab.review_case(case["case_id"],choice,note); st.success("Natija auditga yozildi."); st.rerun()
    else:
        st.info("Hozircha Human Review Case yo'q.")
    st.subheader("Yetishmayotgan ma'lumotlar — qayta tekshiruv")
    if snap.get("data_reviews"):
        st.dataframe(snap["data_reviews"],use_container_width=True,hide_index=True)
        for ticket in snap["data_reviews"]:
            with st.expander(ticket["review_id"]+" · "+ticket["status"]):
                st.write(ticket["reason"])
                choice=st.selectbox("Data Review natijasi",["REQUEST_BANK_DATA","DATA_RECEIVED_RECHECK","RECHECK_RULES","CLOSED_INCONCLUSIVE"],key="data-"+ticket["review_id"])
                note=st.text_area("Tekshiruv izohi",key="data-note-"+ticket["review_id"])
                if st.button("Qayta tekshiruv holatini saqlash",key="data-save-"+ticket["review_id"]):
                    lab.review_data_ticket(ticket["review_id"],choice,note); st.success("Holat saqlandi."); st.rerun()
    else:
        st.info("Qayta tekshiruv navbati hozircha bo'sh.")
    st.caption("Hodisa tafsilotlari sintetik; natijalar prototip qoidalari bilan hisoblangan.")


elif page=="Signal reyestri":
    st.subheader("Signal reyestri — tarixiy qoidalar")
    st.caption("Signal — tekshirishga sabab bo‘ladigan belgi. Bitta signalning o‘zi firibgarlik yoki aybdorlikni anglatmaydi.")
    st.warning("Bu v2 dan saqlangan muhandislik reyestri. Hozirgi v3 classifier barcha qoidalarni bajarmaydi; vaznlar tasdiqlangan risk ehtimoli emas.")
    rows=[
      ("SIG-001","Odatdan yuqori summa","amount, customer_ref"),
      ("SIG-002","Qisqa vaqtda takroriy operatsiya","event_time, customer_ref"),
      ("SIG-003","Kirimdan keyin tez chiqim","direction, amount, event_time"),
      ("SIG-004","Yangi qabul qiluvchi","recipient_ref, customer_ref"),
      ("SIG-005","O'xshash summali takroriy o'tkazmalar","amount, event_time"),
      ("SIG-006","Yangi qurilma","device_ref, customer_ref"),
      ("SIG-007","Tarixdan farqli joylashuv","location, event_time"),
      ("SIG-008","Bir qurilmada bir nechta mijoz","device_ref, customer_ref"),
      ("SIG-010","Odatdan tashqari vaqt","event_time, customer_ref"),
      ("SIG-011","Juda qisqa sessiya","session_seconds"),
      ("SIG-012","Parol tiklangach tez o'tkazma","password_reset_time, event_time"),
      ("SIG-016","Rozilik doirasi noaniq","consent_scope, event_scope")
    ]
    st.dataframe([{"Signal ID":a,"Signal":b,"Kerakli maydonlar":c} for a,b,c in rows],use_container_width=True,hide_index=True)

elif page=="Banklararo tahlil (sintetik)":
    st.subheader("Banklararo tahlil — sintetik atribut mosliklari")
    st.caption("Bu sahifa banklararo tranzaksiya yo'lini emas, 4 ta sun'iy bank manbasidagi psevdonim atribut mosliklarini ko'rsatadi.")
    snap = lab.snapshot()
    device_banks = {}
    for row in snap["recent"]:
        try:
            payload = json.loads(row["payload"])
        except Exception:
            continue
        device = str(payload.get("device_id") or "")
        bank = str(payload.get("bank_id") or row.get("bank_id") or "")
        if device and bank:
            device_banks.setdefault(device, set()).add(bank)
    edges = {}
    for banks in device_banks.values():
        ordered = sorted(banks)
        for i, left in enumerate(ordered):
            for right in ordered[i + 1:]:
                edges[(left, right)] = edges.get((left, right), 0) + 1
    st.markdown("**Sun'iy bank manbalari**")
    if snap["banks"]:
        st.dataframe(snap["banks"], use_container_width=True, hide_index=True)
    if edges:
        dot = ["graph Banklararo {", '  graph [overlap=false];', '  node [shape=box, style="rounded,filled", fillcolor="#dbeafe"];']
        for bank in sorted({x for pair in edges for x in pair}):
            dot.append('  "' + bank + '";')
        for (left, right), count in sorted(edges.items()):
            dot.append('  "' + left + '" -- "' + right + '" [label="' + str(count) + ' moslik"];')
        dot.append("}")
        st.graphviz_chart("\n".join(dot), use_container_width=True)
        st.dataframe([{"Bank manbasi A":k[0],"Bank manbasi B":k[1],"Sintetik qurilma mosliklari":v} for k,v in sorted(edges.items())],use_container_width=True,hide_index=True)
    else:
        st.info("Hozircha banklararo atribut mosligi ko'rsatiladigan hodisalar yo'q. Laboratoriyada START bosing.")
    st.warning("Muhim: bir xil qurilma identifikatori mosligi shaxs aybdorligini isbotlamaydi. Hozirgi sintetik payloadda qabul qiluvchi bank maydoni yo'q; shu sabab A→B→C→D pul o'tkazish zanjiri yoki haqiqiy mablag' oqimi deb ko'rsatilmaydi.")
    st.caption("Bu tahlil faqat namoyish uchun yaratilgan sintetik identifikatorlardan foydalanadi; real banklar bilan integratsiya yo'q.")

elif page=="KPI dashboard":
    st.subheader("KPI dashboard — sintetik jarayon ko'rsatkichlari")
    snap = lab.snapshot()
    evaluation = lab.evaluate()
    results = {"HUMAN_REVIEW":0,"DATA_REVIEW":0,"RECHECK":0,"MONITOR":0}
    for row in snap["recent"]:
        if row["state"] != "PROCESSED" or not row["result"]:
            continue
        try:
            outcome = json.loads(row["result"]).get("outcome")
            if outcome in results:
                results[outcome] += 1
        except Exception:
            continue
    processed = evaluation["processed"]
    total = snap["total"]
    a,b,c,d = st.columns(4)
    a.metric("Sintetik hodisalar", total)
    b.metric("Qayta ishlangan", processed)
    c.metric("Human Review Case", len(snap.get("cases",[])))
    d.metric("Data Review / qayta tekshiruv", len(snap.get("data_reviews",[])))
    st.progress(min(1.0, processed / max(1,total)), text=f"Jarayon bajarilishi: {processed} / {total}")
    st.markdown("#### Amaldagi yo'nalishlar")
    st.dataframe([{"Yo'nalish":"Human Review","Hodisalar":results["HUMAN_REVIEW"]},
                  {"Yo'nalish":"Data Review","Hodisalar":results["DATA_REVIEW"]},
                  {"Yo'nalish":"Recheck","Hodisalar":results["RECHECK"]},
                  {"Yo'nalish":"Monitor","Hodisalar":results["MONITOR"]}],
                 use_container_width=True, hide_index=True)
    st.markdown("#### Sintetik kutilgan yorliq va amaldagi yo'nalish")
    if evaluation["confusion"]:
        st.dataframe([{"Taqqoslash":k,"Soni":v} for k,v in evaluation["confusion"].items()],use_container_width=True,hide_index=True)
    st.warning("Bu KPIlar faqat sintetik laboratoriya ish hajmi va yo'nalishlarini ko'rsatadi. Kutilgan yorliqlar ekspert tasdiqlagan ground-truth emas; bu natijalardan aniqlik, precision, recall, false-positive yoki real zarar kamayishi haqida xulosa chiqarib bo'lmaydi.")
    st.caption("FINZANJIR karta yoki tranzaksiyani avtomatik bloklamaydi. Case — inson ko'rigi uchun tayyorlangan ish yozuvi.")

elif page=="Fuqaro uchun tushuntirish (demo)":
    st.subheader("Fuqaro uchun tushuntirish — demo")
    st.write("FINZANJIR konsepsiyasida signal yoki Case fuqaroning aybdorligini anglatmaydi. Maqsad — noaniq holatni dalillar bilan tekshirish va vakolatli inson ko'rigiga tayyorlash.")
    with st.expander("Signal nima?"):
        st.write("Signal — operatsiya, qurilma, rozilik doirasi yoki boshqa kontekstda qo'shimcha tekshiruvga sabab bo'ladigan belgi. Bitta signalning o'zi firibgarlik isboti emas.")
    with st.expander("Case nima?"):
        st.write("Case — tekshirish uchun yig'ilgan hodisa, dalillar, noma'lum jihatlar va ko'rik qaydlari jamlanmasi. Bu yakuniy huquqiy qaror emas.")
    with st.expander("Human Review nima?"):
        st.write("Vakolatli mutaxassis mavjud dalillarni ko'rib chiqadi, yetishmayotgan ma'lumotni so'rashi yoki noaniqlikni saqlashi mumkin. Prototip hozir bankka haqiqiy buyruq yubormaydi.")
    with st.expander("Karta yoki pul avtomatik bloklanadimi?"):
        st.write("Yo'q. Ushbu FINZANJIR prototipida karta yoki tranzaksiyani avtomatik bloklash funksiyasi yo'q.")
    st.info("Bu fuqarolar uchun axborot sahifasi xolos. Hozircha haqiqiy mijoz Case'larini qidirish, shaxsiy ma'lumotlarni ko'rish yoki shikoyat yuborish portali mavjud emas.")

elif page=="Aloqalar grafigi":
    st.subheader("Sintetik pseudonim aloqalar grafigi")
    st.caption("Atribut mosligi faqat tekshirishga yordam beradi; shaxsning aybdorligi yoki firibgarligini isbotlamaydi.")
    snap=lab.snapshot()
    rows=snap["recent"]
    if rows:
        chosen=st.selectbox("Asosiy hodisa",[r["event_id"] for r in rows],key="graph-event")
        root=next(r for r in rows if r["event_id"]==chosen)
        rp=json.loads(root["payload"])
        related=[]
        for r in rows:
            if r["event_id"]==chosen: continue
            p=json.loads(r["payload"])
            matches=[label for key,label in (("customer_id","Mijoz"),("device_id","Qurilma"),("recipient_id","Qabul qiluvchi")) if rp.get(key) and rp.get(key)==p.get(key)]
            if matches: related.append((r,p,matches))
        dot=['graph G { node [style=filled];','"ROOT" [label="Hodisa '+chosen+'",fillcolor="gold"];']
        for i,(r,p,matches) in enumerate(related[:30]):
            node="R"+str(i)
            dot.append('"'+node+'" [label="'+r["event_id"]+' / '+p.get("bank_id","")+'",fillcolor="lightblue"];')
            dot.append('"ROOT" -- "'+node+'" [label="'+", ".join(matches)+'"];')
        dot.append("}")
        st.graphviz_chart("\n".join(dot),use_container_width=True)
        st.metric("Mos atributli hodisalar",len(related))
        if related:
            st.dataframe([{"Hodisa":r["event_id"],"Bank":p.get("bank_id"),"Moslik":", ".join(m),"Mijoz":p.get("customer_id"),"Qurilma":p.get("device_id"),"Qabul qiluvchi":p.get("recipient_id")} for r,p,m in related],use_container_width=True,hide_index=True)
    else:
        st.info("Avval laboratoriyada sintetik hodisalarni yarating.")

elif page=="Audit jurnali":
    st.subheader("Audit jurnali")
    snap=lab.snapshot()
    st.caption("Oxirgi 30 ta laboratoriya yozuvi. Hozircha o'zgarmas yoki imzolangan audit emas.")
    if snap["audit"]: st.dataframe(snap["audit"],use_container_width=True,hide_index=True)
    else: st.info("Audit yozuvlari hali yo'q.")
elif page=="16 qatlam holati":
    st.subheader("16 qatlam — amaldagi prototip holati")
    st.caption("Holat belgisi har bir qatlam kodda qanchalik amalga oshirilganini bildiradi; bu hali to‘liq tayyor tizim degani.")
    st.warning("Statuslar faqat ushbu branchdagi mavjud kodni bildiradi; 16 qatlam to'liq bajarilgan degani emas.")
    layers=[
      ("L01","Dalil va manba","Qisman","Event ID, sintetik manba va payload; imzo tekshiruvi yo'q."),
      ("L02","Ma'lumot sifati","Demo","Majburiy maydon, summa, vaqt, yo'nalish va zidlik tekshiruvi."),
      ("L03","Signal tahlili","Demo","Oddiy indikatorlar; v2 reyestrining hammasi ko'chmagan."),
      ("L04","Inson nazorati","Demo","Human Review qaydi; IAM/SSO/RBAC yo'q."),
      ("L05","Qoidalar boshqaruvi","Yo'q","Tasdiqlash va versiya rollout yo'q."),
      ("L06","Maxfiylik","Qisman","Sintetik pseudonim ma'lumot; production encryption yo'q."),
      ("L07","Avtomatlashtirish","Demo","400 hodisali worker; retry/backoff yo'q."),
      ("L08","Case va dalil","Qisman","Case va review qaydi; to'liq provenance yo'q."),
      ("L09","Fuqaro shaffofligi","Yo'q","Fuqaro portali yo'q; bloklash oqimi qaytarilmaydi."),
      ("L10","Hayotiy sikl","Qisman","SQLite; retention va backup siyosati yo'q."),
      ("L11","Hodisaga javob","Demo","PAUSE/STOP/RESUME/RESET/KILL SWITCH."),
      ("L12","AI ishonchliligi","Qisman","Offline extractive retrieval; generativ model emas."),
      ("L13","Audit","Qisman","SQLite audit; o'zgarmas audit emas."),
      ("L14","Banklararo integratsiya","Yo'q","Faqat 4 sun'iy bank; API/webhook yo'q."),
      ("L15","Aloqalar grafigi","Demo","Sintetik atribut mosligi."),
      ("L16","KPI va sifat","Qisman","Hisoblagichlar; mustaqil ground-truth yo'q.")
    ]
    st.dataframe([{"Qatlam":a,"Nomi":b,"Holat":c,"Cheklov":d} for a,b,c,d in layers],use_container_width=True,hide_index=True)

elif page=="FINZANJIR AI (o'zbekcha)":
    import internet_research
    st.subheader("FINZANJIR bilim va internet tadqiqot yordamchisi")
    st.caption("Mahalliy bilimlar bazasidan qidirish yoki internetdan yangi manbalarni topish mumkin.")
    mode=st.radio("Qidiruv manbasi",["Mahalliy bilimlar","Internetdan qidirish","Ikkalasini solishtirish"],horizontal=True)
    q=st.text_area("Savolingizni o'zbek tilida yozing",placeholder="Masalan: Banklararo firibgarlik signallarini tekshirish bo‘yicha xalqaro amaliyot qanday?")
    st.info("Maxfiylik: internet qidiruvida faqat siz yozgan so‘rov tashqi qidiruv xizmatiga yuboriladi. Karta raqami, mijoz ma’lumoti, parol, OTP yoki maxfiy bank ma’lumotlarini yozmang.")
    if mode in ("Internetdan qidirish","Ikkalasini solishtirish"):
        st.caption("Internet qidiruvi faqat muallif Streamlit Secrets ichida internet_research.enabled = true qilib yoqqanidan keyin ishlaydi. Kunlik umumiy limit sukut bo'yicha 25 ta so'rov. API kalitini chatga yoki kodga yozmang.")
    if st.button("Qidirishni boshlash",type="primary",disabled=not q.strip()):
        if mode in ("Mahalliy bilimlar","Ikkalasini solishtirish"):
            st.markdown("### Mahalliy bilimlar bazasi")
            local=offline_ai.answer(q)
            if local["status"]=="NO_SUFFICIENT_EVIDENCE": st.warning(local["answer"])
            else: st.success(local["answer"])
            with st.expander("Mahalliy topilgan dalillar va maqomi",expanded=True):
                for item in local["evidence"]:
                    st.markdown(f"**{item['id']}** · {item['approval']} · moslik {item['coverage']}")
                    st.write(item["text"])
        if mode in ("Internetdan qidirish","Ikkalasini solishtirish"):
            st.markdown("### Internet manbalari")
            try:
                internet_config = st.secrets["internet_research"]
                key = internet_config.get("api_key", "")
                internet_enabled = internet_config.get("enabled", False) is True
                daily_limit = int(internet_config.get("max_daily_requests", 25))
            except Exception:
                key, internet_enabled, daily_limit = "", False, 25
            if not internet_enabled:
                st.warning("Internet qidiruvi hozircha o'chirilgan. Muallif uni Secrets ichida enabled = true qilib, Tavily kalitini xavfsiz kiritgandan keyin yoqishi mumkin.")
            elif not key:
                st.warning("Tavily API kaliti sozlanmagan. Streamlit Cloud → App settings → Secrets bo'limiga internet_research.api_key qo'shing.")
            else:
                try:
                    with st.spinner("Internet manbalari qidirilmoqda..."):
                        web_result=internet_research.search_web(q,str(key),max_daily_requests=daily_limit)
                    if not web_result:
                        st.warning("Mos manba topilmadi. So‘rovni aniqroq yozib ko‘ring.")
                    for i,item in enumerate(web_result,1):
                        with st.container(border=True):
                            st.markdown(f"**{i}. [{item['title']}]({item['url']})**")
                            st.write(item["content"])
                            st.caption("Qidiruv mosligi: "+str(item.get("score","—"))+" · Bu parcha manbaning mustaqil tasdig‘i emas.")
                except internet_research.InternetSearchError as exc:
                    st.error("Internet qidiruvi bajarilmadi: "+str(exc))
    st.caption("Mahalliy bilim kartalari candidate maqomida; ular rasmiy tasdiqlangan qoida emas. Internet natijalari tashqi manbalardan olingan va alohida tekshirilishi kerak. Qidiruv natijasi FINZANJIR qoidalarini avtomatik o‘zgartirmaydi.")

elif page=="AI sinovlari":
    st.subheader("O'zbekcha AI regression sinovlari")
    results=offline_ai.self_test()
    passed=sum(1 for r in results if r["passed"])
    a,b=st.columns(2); a.metric("Sinovlar",len(results)); b.metric("O'tdi",passed)
    st.dataframe(results,use_container_width=True,hide_index=True)
    if passed==len(results): st.success("Barcha smoke-testlar o'tdi. Bu mazmuniy ekspert validatsiyasi emas.")
    else: st.error("Kamida bitta sinov o'tmadi. Javoblarni kengaytirishdan oldin retrieval qoidalarini tuzatish kerak.")

elif page=="Arxitektura va chegaralar":
    st.subheader("Loyiha haqida va cheklovlar")
    st.caption("Bu bo‘lim prototipning nimalari ishlashi va nimalari hali ishlab chiqilmaganini tushuntiradi.")
    st.markdown("""
    **Yangi branch:** finzanjir-v3-synthetic-ai-uz

    - Sun'iy bank laboratoriyasi: 400 ta deterministik sintetik hodisa, 4 manba.
    - Boshqaruv: START, PAUSE, STOP, RESUME, RESET.
    - AI: o'zbekcha offline evidence retrieval; tashqi model/API yo'q.
    - Bilimlar: V317 ZIPdan ajratilgan candidate yozuvlar; tasdiqlangan bilim bilan aralashtirilmaydi.
    - Inson ko'rigi: shubhali holatni Case nomzodiga yo'naltirish tamoyili.
    - L11: KILL SWITCH, PAUSE/STOP, navbatni saqlash va tasdiqlangan recovery boshqaruvlari.

    **Hali bajarilmagan / tasdiqlanmagan:**
    - Haqiqiy bank API, imzolangan webhook, autentifikatsiya va bank ACK/NACK.
    - To'liq 16 qatlamni bank mutaxassislari bilan validatsiya qilish.
    - Generativ lokal LLM va Qwen JNI/Android runtime.
    - 400 holat bo'yicha ekspert tasdiqlagan expected labels va statistik aniqlik.
    - APK build, Android qurilmadagi tezlik/RAM va offline runtime.

    Sintetik laboratoriya natijasi production aniqligi yoki bank integratsiyasi isboti emas.
    """)
st.divider()
st.caption("FINZANJIR v3 development • Uzbek-first • no external AI provider • synthetic-only testing")


# Separate public feedback page and author-only analytics panel.
if page == "Tashrifchi fikri":
    visitor_pages.render_feedback()
elif page == "Muallif analitikasi":
    visitor_pages.render_admin()
