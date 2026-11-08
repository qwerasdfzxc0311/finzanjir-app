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

st.set_page_config(page_title="FINZANJIR v3 | Sinov muhiti",page_icon="🛡️",layout="wide",initial_sidebar_state="expanded")
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
# Ochiq namoyish bo'limlari: tashrifchilar loyihaning ishlashini ko'rishi mumkin.
# Muallif analitikasi esa alohida URL va parol bilan himoyalangan.
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
    "Tashrifchi fikri",
]
if author_view:
    page = "Muallif analitikasi"
else:
    page = st.sidebar.radio("FINZANJIR bo'limlari", public_pages, index=0)
    st.sidebar.caption("Ochiq namoyish: faqat sintetik ma'lumotlar. Muallifning shaxsiy analitikasi bu menyuda yo'q.")
    st.caption("Ochiq namoyish rejimi: tashrifchilar loyiha panellari va sintetik ishlash jarayonini ko'rishi mumkin. Boshqa tashrifchilarning maxfiy fikrlari ko'rsatilmaydi.")
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
        st.caption("Internet qidiruvi Streamlit serveri orqali ishlaydi. Buning uchun Streamlit Secrets ichida internet_research.api_key nomi bilan Tavily API kaliti sozlanishi kerak. Kalitni chatga yoki kodga yozmang.")
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
                key=st.secrets["internet_research"]["api_key"]
            except Exception:
                key=""
            if not key:
                st.warning("Internet qidiruvi hali sozlanmagan. Streamlit Cloud → App settings → Secrets bo‘limiga internet_research.api_key qo‘shing.")
            else:
                try:
                    with st.spinner("Internet manbalari qidirilmoqda..."):
                        web_result=internet_research.search_web(q,str(key))
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
