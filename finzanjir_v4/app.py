from __future__ import annotations

from datetime import datetime, timezone
import streamlit as st

st.set_page_config(
    page_title="FINZANJIR v4 | Yagona ish jarayoni",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# FINZANJIR v4 — UI foundation only.
# All displayed records are synthetic examples. This is not a bank integration.
# Human-review actions in this first UI slice live only in Streamlit session state.

NAVY = "#142B49"
BLUE = "#2878C8"
TEAL = "#178C87"
AMBER = "#C58B28"
RED = "#C74B50"
GREEN = "#23865B"
MUTED = "#65758B"

st.markdown(
    f"""
    <style>
      .stApp {{ background: #F4F7FB; }}
      [data-testid="stSidebar"] {{ background: #10243D; }}
      [data-testid="stSidebar"] * {{ color: #F4F7FB !important; }}
      .brand {{ font-size: 1.45rem; font-weight: 800; letter-spacing: .02em; color: {NAVY}; }}
      .subbrand {{ color: {MUTED}; font-size: .84rem; margin-top: -.25rem; }}
      .section-title {{ color: {NAVY}; font-weight: 750; font-size: 1.15rem; margin: .25rem 0 .6rem; }}
      .muted {{ color: {MUTED}; font-size: .86rem; }}
      .metric-card {{ background: white; border: 1px solid #E1E8F0; border-radius: 14px; padding: 16px 18px; min-height: 112px; }}
      .metric-label {{ color: {MUTED}; font-size: .82rem; }}
      .metric-value {{ color: {NAVY}; font-size: 1.8rem; font-weight: 800; margin-top: .2rem; }}
      .metric-note {{ color: {MUTED}; font-size: .76rem; margin-top: .2rem; }}
      .panel {{ background: white; border: 1px solid #E1E8F0; border-radius: 14px; padding: 16px 18px; margin-bottom: 12px; }}
      .step {{ border-left: 4px solid #CBD5E1; padding: 8px 12px; margin: 5px 0; background: white; border-radius: 0 10px 10px 0; }}
      .step-active {{ border-left-color: {BLUE}; background: #EDF5FF; }}
      .step-done {{ border-left-color: {GREEN}; }}
      .pill {{ display: inline-block; padding: 3px 9px; border-radius: 999px; font-size: .74rem; font-weight: 700; background: #EAF0F7; color: {NAVY}; }}
      .layer-id {{ color: {BLUE}; font-size: .76rem; font-weight: 800; letter-spacing: .04em; }}
      .layer-card {{ background: white; border: 1px solid #E1E8F0; border-radius: 12px; padding: 13px; min-height: 142px; }}
      .small {{ color: {MUTED}; font-size: .78rem; }}
      div[data-testid="stMetric"] {{ background: white; padding: 12px 14px; border: 1px solid #E1E8F0; border-radius: 12px; }}
      .stButton > button {{ border-radius: 9px; }}
      footer {{ visibility: hidden; }}
    </style>
    """,
    unsafe_allow_html=True,
)

LAYERS = [
    ("L01", "Evidence & Data Provenance", "Har bir muhim ma’lumotning manbasi, vaqti, olish usuli va versiyasini saqlaydi."),
    ("L02", "Data Quality & Reliability", "To‘liqsizlik, eskirish, dublikat va zid qiymatlarni ko‘rsatadi."),
    ("L03", "Risk & Uncertainty", "Xavf indikatorlari sababini, noaniqlikni va yetishmayotgan dalilni ajratadi."),
    ("L04", "Human Oversight & Correction", "Noaniq yoki yuqori ta’sirli holatni inson ko‘rigiga olib boradi; tuzatish izini saqlaydi."),
    ("L05", "Rule & Model Governance", "Qoida, model va konfiguratsiya versiyasi hamda o‘zgarish tarixini boshqaradi."),
    ("L06", "Data Disclosure & Sharing Control", "Tashqi uzatishdan oldin maqsad, ruxsat, oluvchi va minimal maydonlarni tekshiradi."),
    ("L07", "Automation Safety & Control", "Avtomatlashtirish chegarasi, xavfsiz to‘xtash va qo‘lda ko‘rik yo‘lini belgilaydi."),
    ("L08", "Transaction Chain & Case Correlation", "Hodisalar zanjiri va Case bilan bog‘lanish sababini ko‘rsatadi."),
    ("L09", "Citizen Transparency & Appeal", "Foydalanuvchiga tushunarli holat izohi va e’tiroz/tuzatish yo‘lini loyihalaydi."),
    ("L10", "Privacy & Data Lifecycle", "Maqsad, saqlash muddati, kirish, arxivlash va o‘chirish qoidalarini belgilaydi."),
    ("L11", "Security Incident Response", "Xavfsizlik hodisasini tasniflash, eskalatsiya, dalilni saqlash va tiklashni qamraydi."),
    ("L12", "Knowledge Governance & AI Reliability", "AI javobini manbaga bog‘laydi; yetarli dalil bo‘lmasa buni ochiq aytadi."),
    ("L13", "Testing & Independent Evaluation", "Talab, test, kutilgan/haqiqiy natija va dalil izchilligini tekshiradi."),
    ("L14", "Bank Integration Readiness", "Bank integratsiyasi shartlari, API/schema, autentifikatsiya va sandbox tayyorligini baholaydi."),
    ("L15", "Performance & Capacity Management", "Javob vaqti, xato ulushi, resurs va tiklanish ko‘rsatkichlarini o‘lchaydi."),
    ("L16", "Impact & Harm Reduction", "FP/FN va salbiy ta’sir metrikalarini aniq metodika bilan baholaydi."),
]

DEMO_EVENTS = {
    "SYN-ATO-001": {
        "title": "Noodatiy qurilma va yangi oluvchi",
        "source": "Sintetik bank A",
        "time": "2026-11-08 10:42",
        "status": "HUMAN_REVIEW",
        "signals": [
            ("SIG-001", "Yangi qurilma", "L03", "Kontekst bilan tekshirish kerak"),
            ("SIG-002", "Yangi qabul qiluvchi", "L03", "Oldingi operatsiyalar bilan solishtirish kerak"),
            ("SIG-003", "Rozilik doirasi noaniq", "L04", "Aniq o'tkazma bo'yicha rozilik dalili yo'q"),
        ],
        "evidence": [
            ("EVD-SYN-01", "Qurilma identifikatori avvalgi sintetik hodisalarda uchramagan", "Tasdiqlovchi indikator", "Sintetik payload"),
            ("EVD-SYN-02", "Yangi qabul qiluvchi identifikatori", "Kontekst talab qiladi", "Sintetik payload"),
        ],
        "unknowns": [
            "Mijoz aynan shu o'tkazmaga rozilik berganmi?",
            "Qurilma mijoz tomonidan qonuniy ishlatilganmi?",
            "Qo'ng'iroq yoki ijtimoiy muhandislik alomati bormi?",
        ],
        "case_id": "CASE-SYN-0001",
        "reason": "Bir nechta mustaqil sintetik indikator bor; inson ko‘rigi uchun namuna.",
    },
    "SYN-DATA-002": {
        "title": "Ma'lumot yetishmasligi",
        "source": "Sintetik bank B",
        "time": "2026-11-08 10:47",
        "status": "DATA_REVIEW",
        "signals": [
            ("SIG-004", "Qabul qiluvchi maydoni yo'q", "L02", "Ma'lumot sifati muammosi"),
        ],
        "evidence": [],
        "unknowns": ["Qabul qiluvchi identifikatori payload'da mavjud emas."],
        "case_id": "",
        "reason": "Majburiy maydon yetishmaydi; Case ochishdan oldin ma'lumotni to'ldirish kerak.",
    },
    "SYN-ONE-003": {
        "title": "Yakka noaniq indikator",
        "source": "Sintetik bank C",
        "time": "2026-11-08 10:51",
        "status": "RECHECK",
        "signals": [
            ("SIG-005", "Kontekstdan yuqori summa", "L03", "Yakka indikator yakuniy xulosa emas"),
        ],
        "evidence": [
            ("EVD-SYN-03", "Operatsiya summasi oldingi sintetik medianadan yuqori", "Kontekst talab qiladi", "Sintetik tarix"),
        ],
        "unknowns": ["Mijozning odatiy operatsiya konteksti to‘liq emas."],
        "case_id": "",
        "reason": "Bitta indikator yetarli emas; kuzatish yoki qo‘shimcha kontekst kerak.",
    },
}

PIPELINE = [
    ("01", "Manba va hodisani qabul qilish", "L01 · L14"),
    ("02", "Ma’lumot sifati tekshiruvi", "L02 · L10"),
    ("03", "16 qatlam bo‘yicha tahlil", "L01–L16"),
    ("04", "Signal, dalil va noma’lumlarni ajratish", "L03 · L08"),
    ("05", "Case ochish mezonlarini tekshirish", "L03 · L04 · L07"),
    ("06", "Case markazida boshqarish", "L08 · L10"),
    ("07", "Human Review", "L04 · L05"),
    ("08", "Yakun, audit va o‘lchash", "L01 · L11 · L13 · L16"),
]

def init_state():
    st.session_state.setdefault("review_decisions", {})
    st.session_state.setdefault("selected_event", "SYN-ATO-001")
    st.session_state.setdefault("nav", "Umumiy ko‘rinish")

init_state()

st.sidebar.markdown("## 🛡️ FINZANJIR")
st.sidebar.caption("Yagona ish jarayoni · v4 ishlab chiqish prototipi")
st.sidebar.markdown("---")
nav_items = [
    "Umumiy ko‘rinish",
    "Ish jarayoni",
    "Signallar",
    "16 qatlam",
    "Case markazi",
    "Human Review",
    "Ma’lumot sifati",
    "Aloqalar xaritasi",
    "Audit jurnali",
    "Sinov laboratoriyasi",
    "Tizim haqida",
]
page = st.sidebar.radio("ASOSIY MENYU", nav_items, key="nav")
st.sidebar.markdown("---")
st.sidebar.markdown("**Namoyish muhiti**")
st.sidebar.markdown("🟡 Faqat sintetik ma’lumot")
st.sidebar.markdown("🔒 Haqiqiy bank integratsiyasi yo‘q")
st.sidebar.markdown("⛔ Avtomatik bloklash yo‘q")
st.sidebar.caption("v4 UI foundation · session demo")

st.markdown('<div class="brand">FINZANJIR</div>', unsafe_allow_html=True)
st.markdown('<div class="subbrand">Firibgarlik xavfini aniqlashga yordam beruvchi signal, dalil va inson ko‘rigi tizimi</div>', unsafe_allow_html=True)
st.markdown("")

def metric(label: str, value: str, note: str, icon: str):
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{icon} &nbsp; {label}</div>'
        f'<div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
        unsafe_allow_html=True,
    )

def status_label(status: str) -> str:
    return {
        "HUMAN_REVIEW": "Inson ko‘rigi",
        "DATA_REVIEW": "Ma’lumot tekshiruvi",
        "RECHECK": "Qayta tekshiruv",
        "MONITOR": "Kuzatuv",
    }.get(status, status)

def render_pipeline(active: int = 3):
    for i, (number, label, layers) in enumerate(PIPELINE):
        cls = "step step-done" if i < active else ("step step-active" if i == active else "step")
        st.markdown(
            f'<div class="{cls}"><b>{number}. {label}</b><br>'
            f'<span class="small">Tegishli qatlamlar: {layers}</span></div>',
            unsafe_allow_html=True,
        )

def render_event_detail(event_id: str):
    event = DEMO_EVENTS[event_id]
    st.markdown(f"### {event['title']}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Hodisa ID", event_id)
    c2.metric("Manba", event["source"])
    c3.metric("Holat", status_label(event["status"]))
    st.caption(f"Vaqt: {event['time']} · {event['reason']}")
    st.markdown("#### Aniqlangan signallar")
    if event["signals"]:
        st.dataframe(
            [{"Signal ID": s[0], "Indikator": s[1], "Qatlam": s[2], "Izoh": s[3]} for s in event["signals"]],
            use_container_width=True, hide_index=True,
        )
    else:
        st.info("Hozircha signal yo‘q.")
    left, right = st.columns(2)
    with left:
        st.markdown("#### Dalillar")
        if event["evidence"]:
            for eid, desc, kind, source in event["evidence"]:
                st.markdown(f"**{eid}** · {kind}")
                st.write(desc)
                st.caption(f"Manba: {source}")
        else:
            st.info("Tasdiqlovchi yoki inkor etuvchi dalil hali mavjud emas.")
    with right:
        st.markdown("#### Noma’lum jihatlar")
        for item in event["unknowns"]:
            st.markdown(f"- {item}")
    if event["case_id"]:
        st.success(f"Bog‘langan demo Case: {event['case_id']}")
    else:
        st.warning("Bu hodisa uchun hozircha Case ochilmagan.")

if page == "Umumiy ko‘rinish":
    st.markdown("## Umumiy ko‘rinish")
    st.caption("Barcha bo‘limlar bir xil hodisa, signal, dalil va Case identifikatorlari bilan ishlashi uchun yagona ish maydoni.")
    a, b, c, d = st.columns(4)
    with a: metric("Sintetik hodisalar", "3", "Namoyish uchun", "📥")
    with b: metric("Human Review", "1", "Demo Case", "👤")
    with c: metric("Ma’lumot tekshiruvi", "1", "Maydon yetishmaydi", "🟡")
    with d: metric("Qayta tekshiruv", "1", "Yakka indikator", "🔎")
    st.markdown("")
    left, right = st.columns([1.15, 1])
    with left:
        st.markdown("### Asosiy ish jarayoni")
        render_pipeline(active=3)
    with right:
        st.markdown("### Oxirgi sintetik hodisalar")
        for eid, event in DEMO_EVENTS.items():
            with st.container(border=True):
                st.markdown(f"**{eid} · {event['title']}**")
                st.caption(f"{event['source']} · {status_label(event['status'])}")
                if st.button("Hodisani ochish", key=f"open-{eid}", use_container_width=True):
                    st.session_state["selected_event"] = eid
                    st.success("Hodisa tanlandi. Batafsil ko‘rish uchun chap menyudan “Signallar” bo‘limini oching.")
    st.info("Bu raqamlar faqat ushbu sahifadagi 3 ta sintetik namuna. Real bank statistikasi emas.")

elif page == "Ish jarayoni":
    st.markdown("## Hodisadan inson ko‘rigigacha")
    st.caption("Bir hodisa bo‘yicha barcha bosqichlar ketma-ket ko‘rsatiladi. Har bosqichda manba va natija izini saqlash ko‘zda tutilgan.")
    selected = st.selectbox("Sintetik hodisani tanlang", list(DEMO_EVENTS), key="workflow-event")
    event = DEMO_EVENTS[selected]
    active = {"HUMAN_REVIEW": 6, "DATA_REVIEW": 1, "RECHECK": 3, "MONITOR": 7}.get(event["status"], 3)
    left, right = st.columns([1.05, 1])
    with left:
        render_pipeline(active=active)
    with right:
        st.markdown("### Joriy holat")
        st.markdown(f"**{selected}**")
        st.markdown(f'<span class="pill">{status_label(event["status"])}</span>', unsafe_allow_html=True)
        st.write(event["reason"])
        if event["case_id"]:
            st.success(f"Case ID: {event['case_id']}")
        else:
            st.warning("Case ochilmagan. Bu xato emas: ma’lumot yoki mezon yetarli bo‘lmasligi mumkin.")
    render_event_detail(selected)

elif page == "Signallar":
    st.markdown("## Signal reyestri")
    st.caption("Signal — indikator. U yakuniy xulosa, aybdorlik yoki avtomatik bloklash buyrug‘i emas.")
    selected = st.selectbox("Hodisani tanlang", list(DEMO_EVENTS), key="signal-event")
    st.session_state["selected_event"] = selected
    render_event_detail(selected)

elif page == "16 qatlam":
    st.markdown("## 16 qatlam — yagona arxitektura")
    st.caption("Qatlamlar mustaqil menyular to‘plami emas. Ular bitta hodisa va Case kontekstida o‘zaro bog‘lanadigan funksional/nazorat chegaralaridir.")
    st.warning("Qatlam nomlari talablar reyestridan olingan. Bu v4 ekranida qatlamlar hali to‘liq implementatsiya qilingan yoki ekspertlar tomonidan tasdiqlangan degani emas.")
    search = st.text_input("Qatlamdan qidirish", placeholder="Masalan: provenance, privacy, Human Oversight")
    filtered = [x for x in LAYERS if search.casefold() in (x[0] + " " + x[1] + " " + x[2]).casefold()]
    cols = st.columns(2)
    for i, (layer_id, name, description) in enumerate(filtered):
        with cols[i % 2]:
            st.markdown(
                f'<div class="layer-card"><div class="layer-id">{layer_id} · HOZIRCHA REJA</div>'
                f'<b>{name}</b><p class="small">{description}</p>'
                f'<span class="pill">Ekspert tasdig‘i kutilmoqda</span></div>',
                unsafe_allow_html=True,
            )
    with st.expander("Qatlamlararo bog‘liqlik qanday boshqariladi?"):
        st.write("Har bir qatlamning kirish/chiqish kontrakti, manbasi, vaqt belgisi, versiyasi va cheklovi saqlanadi. Bog‘lanishlar manba reyestridan olinadi; loyiha egasi tasdiqlamaguncha LINK-PROP nomzodlari rasmiy LINK-ID deb ko‘rsatilmaydi.")
        st.write("Hozirgi sahifada qatlamlar katalogi ko‘rsatilgan. To‘liq manba asosidagi aloqa xaritasi keyingi ishlab chiqish bosqichida qo‘shiladi.")

elif page == "Case markazi":
    st.markdown("## Case markazi")
    st.caption("Case — tekshiruv uchun jamlangan kontekst. Bu aybdorlik hukmi emas.")
    cases = [(k, v) for k, v in DEMO_EVENTS.items() if v["case_id"]]
    if not cases:
        st.info("Hozircha ochiq demo Case yo‘q.")
    else:
        case_id, event = cases[0][1]["case_id"], cases[0][1]
        st.markdown(f"### {case_id}")
        st.markdown(f'<span class="pill">OPEN · SINTETIK</span>', unsafe_allow_html=True)
        st.write(event["reason"])
        c1, c2, c3 = st.columns(3)
        c1.metric("Bog‘langan hodisalar", "1")
        c2.metric("Bog‘langan signallar", str(len(event["signals"])))
        c3.metric("Noma’lum jihatlar", str(len(event["unknowns"])))
        tab1, tab2, tab3, tab4 = st.tabs(["Umumiy", "Signallar va dalillar", "Rozilik doirasi", "Tarix"])
        with tab1:
            st.write("**Gipoteza:** hisob yoki qurilmadan ruxsatsiz foydalanish ehtimolini tekshirish.")
            st.write("**Holat:** inson ko‘rigini kutmoqda.")
            st.write("**Chegara:** sintetik namuna; haqiqiy mijoz yoki bank ma’lumoti emas.")
        with tab2:
            render_event_detail("SYN-ATO-001")
        with tab3:
            st.write("Qurilmadan foydalanishga ruxsat, hisobdan foydalanishga ruxsat va aynan shu pul o‘tkazmasiga rozilik alohida tekshirilishi kerak.")
            st.warning("Ushbu sintetik namuna rozilikni tasdiqlamaydi. Aniq o‘tkazmaga rozilik dalili noma’lum.")
        with tab4:
            st.write("10:42 · Sintetik hodisa qabul qilindi")
            st.write("10:42 · Sintetik indikatorlar qayd etildi")
            st.write("10:42 · Case demo sifatida ochildi")
            st.caption("Bu tarix UI namunasi; real audit jurnali emas.")

elif page == "Human Review":
    st.markdown("## Human Review — inson ko‘rigi")
    st.caption("Mutaxassis dalillarni, qarama-qarshiliklarni va noma’lum jihatlarni ko‘rib chiqib, asoslangan harakatni qayd etadi.")
    case_options = [v["case_id"] for v in DEMO_EVENTS.values() if v["case_id"]]
    if not case_options:
        st.info("Human Review uchun demo Case mavjud emas.")
    else:
        case_id = st.selectbox("Case tanlang", case_options)
        event = DEMO_EVENTS["SYN-ATO-001"]
        render_event_detail("SYN-ATO-001")
        st.markdown("### Ko‘rib chiqish natijasi")
        decision = st.radio(
            "Mutaxassisning demo harakati",
            ["Qo‘shimcha ma’lumot so‘rash", "Qayta tekshiruvga yuborish", "Case'ni yopish — asos bilan", "Ko‘rib chiqish davom etadi"],
            horizontal=False,
        )
        rationale = st.text_area("Qaror sababi", placeholder="Qaysi dalilga tayandingiz? Qaysi noma’lum jihat qoldi?")
        if st.button("Demo qarorini sessiyada qayd etish", type="primary"):
            if not rationale.strip():
                st.error("Qaror sababini yozing. Asossiz qaror qayd etilmaydi.")
            else:
                st.session_state["review_decisions"][case_id] = {
                    "decision": decision,
                    "rationale": rationale.strip(),
                    "at": datetime.now(timezone.utc).isoformat(),
                }
                st.success("Demo qarori joriy sessiyada qayd etildi. Bu hali doimiy DB/audit saqlovi emas.")
        saved = st.session_state["review_decisions"].get(case_id)
        if saved:
            st.markdown("#### Joriy sessiyadagi oxirgi qayd")
            st.write(saved["decision"])
            st.write(saved["rationale"])
            st.caption(saved["at"])
        st.warning("Bu ekran hozircha demo. Haqiqiy reviewer autentifikatsiyasi, rol/vakolat nazorati va doimiy audit hali ulanmagan.")

elif page == "Ma’lumot sifati":
    st.markdown("## Ma’lumot sifati va qayta tekshiruv")
    st.caption("Ma’lumot yetishmasligi yoki qarama-qarshilikni xavf xulosasiga aylantirmaymiz.")
    for eid, event in DEMO_EVENTS.items():
        if event["status"] in ("DATA_REVIEW", "RECHECK"):
            with st.container(border=True):
                st.markdown(f"**{eid} · {event['title']}**")
                st.markdown(f'<span class="pill">{status_label(event["status"])}</span>', unsafe_allow_html=True)
                st.write(event["reason"])
                for unknown in event["unknowns"]:
                    st.markdown(f"- {unknown}")

elif page == "Aloqalar xaritasi":
    st.markdown("## Qatlamlararo aloqalar xaritasi")
    st.caption("Bog‘liqliklar bitta tizimda ko‘rinishi kerak, lekin manbada bo‘lmagan yo‘nalishni taxmin bilan chizmaymiz.")
    st.info("36 ta manba bilan qo‘llab-quvvatlangan LINK-PROP yo‘nalishi bo‘yicha alohida v0.3 audit xulosasi mavjud. Ular rasmiy LINK-ID ham, real texnik interfeys ham emas. v4 xaritasiga faqat manba va maqomi bilan kiritiladi.")
    st.markdown("**Bog‘lanish kartasining majburiy tarkibi:**")
    st.markdown("- Manba qatlam → maqsad qatlam")
    st.markdown("- Uzatiladigan obyekt va nima uchun kerakligi")
    st.markdown("- REQ-ID / TEST-ID")
    st.markdown("- Manba bandi va cheklovi")
    st.markdown("- Tasdiq holati va dalil")
    st.warning("Hozirgi build'da to‘liq 36 yo‘nalishli interaktiv graf hali qurilmagan. Bu sahifa uning noto‘g‘ri taxmin bilan chizilishining oldini oluvchi vaqtinchalik ko‘rinish.")

elif page == "Audit jurnali":
    st.markdown("## Audit jurnali")
    st.caption("Haqiqiy audit izi har bir amal, vaqt, obyekt, oldingi/keyingi qiymat va actor bilan yozilishi kerak.")
    st.info("Ushbu birinchi UI bosqichida tarix faqat ko‘rgazmali. Doimiy va o‘zgartirib bo‘lmaydigan audit saqlovi hali ulanmagan.")
    st.dataframe(
        [
            {"Vaqt": "10:42:00", "Amal": "SYNTHETIC_EVENT_RECEIVED", "Obyekt": "SYN-ATO-001", "Holat": "DEMO"},
            {"Vaqt": "10:42:01", "Amal": "SIGNALS_CREATED", "Obyekt": "SIG-001…003", "Holat": "DEMO"},
            {"Vaqt": "10:42:02", "Amal": "CASE_OPENED", "Obyekt": "CASE-SYN-0001", "Holat": "DEMO"},
        ],
        use_container_width=True, hide_index=True,
    )

elif page == "Sinov laboratoriyasi":
    st.markdown("## Sintetik sinov laboratoriyasi")
    st.caption("Haqiqiy bank ma’lumotlari emas. Bu sahifa ssenariylarni tushunish va keyinchalik qayta bajariladigan testlarga aylantirish uchun.")
    selected = st.selectbox("Sinov ssenariysi", list(DEMO_EVENTS), key="lab-event")
    render_event_detail(selected)
    st.markdown("### Sinov savollari")
    st.markdown("- Scenario nomi tasniflash algoritmiga ta’sir qilyaptimi?")
    st.markdown("- Yetishmayotgan ma’lumot xavf xulosasini to‘xtatyaptimi?")
    st.markdown("- Yakka indikator Case ochmasdan qayta tekshiruvga tushyaptimi?")
    st.markdown("- Human Review qarori dalil va sabab bilan qayd etilyaptimi?")
    st.warning("Bu UI slice 400 hodisali v3 laboratoriyasini hali v4 ga ulamagan. Avtomatik bank oqimi, pause/resume va L11 kill-switch integratsiyasi alohida bosqichda ulanadi.")

elif page == "Tizim haqida":
    st.markdown("## FINZANJIR nima?")
    st.write("FINZANJIR — banklar va vakolatli tomonlar o‘rtasida qonuniy ruxsat etilgan signallarni bog‘lash, firibgarlik xavfini tekshirish, dalillarni tartiblash va inson ko‘rigini qo‘llab-quvvatlash konsepsiyasi.")
    st.markdown("### Nima qilmaydi?")
    st.markdown("- Kartani, hisobni yoki tranzaksiyani avtomatik bloklamaydi.")
    st.markdown("- Signalni aybdorlik isboti deb ko‘rsatmaydi.")
    st.markdown("- Banklarning barcha mijoz ma’lumotlarini erkin ko‘rmaydi.")
    st.markdown("- Hozirgi prototipda real bank API yoki production vakolati yo‘q.")
    st.markdown("### Hozirgi prototip holati")
    st.warning("v4 — yangi UI va arxitektura poydevori. Ko‘rsatilgan yozuvlar sintetik namuna. Qatlamlar, LINK yo‘nalishlari va Human Review workflow'i to‘liq implementatsiya qilinishi hamda ekspertlar bilan tekshirilishi kerak.")

st.markdown("---")
st.caption("FINZANJIR v4 · yagona ish jarayoni prototipi · faqat sintetik namoyish · real bank integratsiyasi emas")
