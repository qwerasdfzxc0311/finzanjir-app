from __future__ import annotations

from datetime import datetime
import streamlit as st
import ai_assistant

st.set_page_config(
    page_title="FINZANJIR | Ochiq namoyish",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# FINZANJIR v4 — read-only public demonstration.
# All records are synthetic. No bank connection, real customer data, or transaction control.
# Navigation and filters only change what is displayed; no public write actions are exposed.

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
      :root {{ color-scheme: light; }}
      .stApp {{ background: #F3F6FA; color: #1D2D42; }}
      [data-testid="stHeader"] {{ background: rgba(243,246,250,.92); }}
      [data-testid="stSidebar"] {{ background: #10243D; }}
      [data-testid="stSidebar"] * {{ color: #F4F7FB !important; }}
      .block-container {{ padding-top: 1.35rem; padding-bottom: 2.2rem; max-width: 1440px; }}
      .brand {{ font-size: 1.85rem; font-weight: 850; letter-spacing: .035em; color: {NAVY}; line-height: 1.15; }}
      .subbrand {{ color: {MUTED}; font-size: .98rem; margin-top: .22rem; }}
      .eyebrow {{ color: {BLUE}; font-size: .72rem; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; }}
      .hero {{ background: linear-gradient(120deg,#10243D 0%,#183B61 62%,#1B6470 100%); color: white; border-radius: 18px; padding: 26px 28px; margin: .7rem 0 1rem; }}
      .hero h2 {{ color: white; font-size: 1.65rem; margin: .25rem 0 .55rem; }}
      .hero p {{ color: #E2ECF7; margin: 0; font-size: .98rem; line-height: 1.6; }}
      .hero-tag {{ display: inline-block; border: 1px solid rgba(255,255,255,.28); border-radius: 999px; padding: 4px 10px; font-size: .75rem; color: #EAF3FC; margin: 0 6px 8px 0; }}
      .panel {{ background: white; border: 1px solid #E1E8F0; border-radius: 15px; padding: 17px 18px; margin-bottom: 12px; }}
      .metric-card {{ background: white; border: 1px solid #E1E8F0; border-radius: 14px; padding: 15px 16px; min-height: 112px; }}
      .metric-label {{ color: {MUTED}; font-size: .82rem; }}
      .metric-value {{ color: {NAVY}; font-size: 1.75rem; font-weight: 850; margin-top: .18rem; }}
      .metric-note {{ color: {MUTED}; font-size: .76rem; margin-top: .16rem; }}
      .layer-card {{ background: white; border: 1px solid #E1E8F0; border-radius: 13px; padding: 14px 15px; min-height: 148px; }}
      .layer-id {{ color: {BLUE}; font-size: .75rem; font-weight: 850; letter-spacing: .06em; }}
      .layer-name {{ color: {NAVY}; font-size: .97rem; font-weight: 780; margin: .3rem 0; }}
      .small {{ color: {MUTED}; font-size: .81rem; line-height: 1.5; }}
      .status {{ display: inline-block; border-radius: 999px; padding: 4px 9px; background: #FFF4D8; color: #805A0C; font-size: .72rem; font-weight: 750; }}
      .step {{ background: white; border: 1px solid #E1E8F0; border-left: 4px solid #B7C5D5; border-radius: 0 12px 12px 0; padding: 12px 14px; margin: 7px 0; }}
      .step-focus {{ border-left-color: {BLUE}; background: #EDF5FF; }}
      .step-title {{ color: {NAVY}; font-weight: 780; }}
      .step-meta {{ color: {MUTED}; font-size: .78rem; margin-top: 3px; }}
      .callout {{ background: #EDF5FF; border: 1px solid #D6E7FA; border-radius: 12px; padding: 13px 15px; color: #244665; }}
      .warning-note {{ background: #FFF7E5; border: 1px solid #F0DFB8; border-radius: 12px; padding: 13px 15px; color: #765515; }}
      .footer {{ color: {MUTED}; font-size: .78rem; border-top: 1px solid #DFE6EE; padding-top: 14px; margin-top: 26px; }}
      div[data-testid="stMetric"] {{ background: white; padding: 12px 14px; border: 1px solid #E1E8F0; border-radius: 12px; }}
      div[data-testid="stExpander"] {{ background: white; border: 1px solid #E1E8F0; border-radius: 12px; }}
      .stButton > button {{ border-radius: 9px; }}
      @media (max-width: 700px) {{
        .block-container {{ padding-left: 1rem; padding-right: 1rem; }}
        .brand {{ font-size: 1.55rem; }}
        .hero {{ padding: 20px 18px; }}
        .hero h2 {{ font-size: 1.3rem; }}
      }}
      footer {{ visibility: hidden; }}
    </style>
    """,
    unsafe_allow_html=True,
)

LAYERS = [
    {
        "id": "L01", "name": "Evidence & Data Provenance",
        "simple": "Har bir ma’lumot qayerdan kelganini va qachon olinganini ko‘rsatadi.",
        "purpose": "Dalilning kelib chiqishini tekshirish mumkin bo‘lishi uchun manba, vaqt, olish usuli va versiya/identifikatorni saqlash.",
        "question": "Bu ma’lumot qayerdan, qachon va qanday usulda olingan?",
        "inputs": "Manba identifikatori, hodisa vaqti, qabul qilingan vaqt, olish usuli, yozuv versiyasi.",
        "outputs": "Manbaga bog‘langan yozuv va uning kelib chiqish izohi.",
        "checks": "Manbasi noma’lum yozuv tasdiqlangan dalil sifatida ko‘rsatilmasligi kerak.",
        "limit": "Hozirgi namoyishda manba yozuvlari sintetik. Bank manbalari bilan haqiqiy provenance zanjiri ulanmagan.",
    },
    {
        "id": "L02", "name": "Data Quality & Reliability",
        "simple": "Ma’lumot to‘liqmi, eskirganmi yoki boshqa ma’lumotga zidmi — shuni tekshiradi.",
        "purpose": "To‘liqsizlik, eskirish, dublikat va zid qiymatlarni aniqlab, ularning keyingi tahlilga ta’sirini ochiq ko‘rsatish.",
        "question": "Tahlil qilish uchun zarur ma’lumot yetarlimi va o‘zaro mosmi?",
        "inputs": "Majburiy maydonlar, formatlar, vaqt belgilari, takrorlanish belgilari va o‘zaro tekshiriladigan qiymatlar.",
        "outputs": "Sifat holati, yetishmayotgan maydonlar, ziddiyatlar va qayta tekshiruv sababi.",
        "checks": "Ma’lumot yetishmasa tizim taxminiy xulosa bermasdan DATA_REVIEW holatini ko‘rsatadi.",
        "limit": "Hozirgi to‘liq sifat tekshiruvi barcha bank sxemalari bo‘yicha joriy etilgan emas.",
    },
    {
        "id": "L03", "name": "Risk & Uncertainty",
        "simple": "Xavotir uyg‘otgan belgilarni, noaniqliklarni va yetishmayotgan dalillarni ajratadi.",
        "purpose": "Signal sabablarini va noaniqlikni ko‘rsatish; ball yoki indikatorni aybdorlik hukmiga aylantirmaslik.",
        "question": "Qaysi kuzatilgan holat qo‘shimcha tekshiruvni talab qiladi va nimasi hali noma’lum?",
        "inputs": "Tekshirilgan hodisa maydonlari, tarixiy kontekst, signal qoidalari va ma’lumot sifati natijalari.",
        "outputs": "Izohlangan indikatorlar, noaniqliklar va qo‘shimcha tekshiruv ehtiyoji.",
        "checks": "Yakka indikator avtomatik ravishda Case yoki ayblovga aylanmaydi.",
        "limit": "Sintetik natijalar kalibrlangan firibgarlik ehtimoli yoki real aniqlik ko‘rsatkichi emas.",
    },
    {
        "id": "L04", "name": "Human Oversight & Correction",
        "simple": "Muhim yoki noaniq holatni inson mutaxassisiga ko‘rib chiqish uchun beradi.",
        "purpose": "Inson ko‘rigi, tuzatish va qaror sabablarini qayd etish; avtomatik tizim inson vakolatini almashtirmasligi.",
        "question": "Qaysi holatda inson ko‘rigi shart va uning xulosasi qanday asoslanadi?",
        "inputs": "Case konteksti, signallar, dalillar, qarshi dalillar, noma’lumlar va oldingi ko‘rik izlari.",
        "outputs": "Ko‘rib chiqish holati, asoslangan harakat, izoh va tuzatish tarixi.",
        "checks": "Har bir qaror dalil va sabab bilan bog‘lanishi kerak.",
        "limit": "Ushbu ommaviy ekran faqat Human Review jarayonini namoyish qiladi; haqiqiy reviewer vakolati va doimiy audit ulanmagan.",
    },
    {
        "id": "L05", "name": "Rule & Model Governance",
        "simple": "Qoidalar va modellar qaysi versiyada ekanini, kim tasdiqlaganini va nima o‘zgarganini nazorat qiladi.",
        "purpose": "Qoida/model/config versiyasi, tasdiqlash vakolati, o‘zgarish tarixi va rollback nazoratini belgilash.",
        "question": "Qaysi qoida yoki model ishladi va bu versiya tasdiqlanganmi?",
        "inputs": "Qoida identifikatori, model/config versiyasi, tasdiqlash qaydi va o‘zgarish so‘rovi.",
        "outputs": "Versiya izi, tasdiqlash holati va o‘zgarishlar jurnali.",
        "checks": "Tasdiqlanmagan o‘zgarish amaldagi qoida sifatida yashirin qo‘llanmasligi kerak.",
        "limit": "To‘liq model registry, tasdiqlash oqimi va rollback mexanizmi hozircha joriy etilmagan.",
    },
    {
        "id": "L06", "name": "Data Disclosure & Sharing Control",
        "simple": "Ma’lumot boshqa tashkilotga yuborilishidan oldin bunga ruxsat va zarurat borligini tekshiradi.",
        "purpose": "Tashqi uzatishdan oldin maqsad, huquqiy/ruxsat asosi, qabul qiluvchi va minimal kerakli maydonlarni tekshirish.",
        "question": "Kimga, nima maqsadda va aynan qaysi eng kam ma’lumot uzatilishi mumkin?",
        "inputs": "Uzatish maqsadi, oluvchi, ruxsat asosi, ma’lumot toifasi va maydonlar ro‘yxati.",
        "outputs": "Uzatishga ruxsat/taqiq holati va minimal maydonlar to‘plami.",
        "checks": "Keraksiz yoki ruxsatsiz maydonlar tashqi uzatishga kiritilmasligi kerak.",
        "limit": "Haqiqiy banklararo ma’lumot almashinuvi, huquqiy ruxsat va API integratsiyasi mavjud emas.",
    },
    {
        "id": "L07", "name": "Automation Safety & Control",
        "simple": "Avtomatik jarayon qayergacha borishi mumkinligini va qachon to‘xtashi kerakligini belgilaydi.",
        "purpose": "Avtomatik amallar chegarasi, sabab kodi, xavfsiz to‘xtash va qo‘lda ko‘rik yo‘lini belgilash.",
        "question": "Qaysi ish avtomatlashtiriladi, qaysi ish inson tasdig‘ini talab qiladi?",
        "inputs": "Jarayon holati, amal turi, ruxsat darajasi, xato/istisno signallari va xavfsizlik qoidalari.",
        "outputs": "Davom ettirish, xavfsiz to‘xtatish yoki inson ko‘rigiga yo‘naltirish holati.",
        "checks": "FINZANJIR karta, hisob yoki tranzaksiyani avtomatik bloklamaydi.",
        "limit": "Ishlab chiqarish darajasidagi xavfsiz boshqaruv va favqulodda tiklash hali ekspert sinovidan o‘tmagan.",
    },
    {
        "id": "L08", "name": "Transaction Chain & Case Correlation",
        "simple": "Bir-biriga aloqador hodisalarni nima sababdan bitta Case doirasida ko‘rayotganini tushuntiradi.",
        "purpose": "Case ichidagi hodisa manbasi, vaqti va bog‘lanish sababini ko‘rsatish; to‘liq bo‘lmagan zanjirni isbot deb ko‘rsatmaslik.",
        "question": "Bu hodisalar nima sababdan o‘zaro bog‘landi va qaysi qismi hali tasdiqlanmagan?",
        "inputs": "Hodisa identifikatorlari, vaqt, ruxsat etilgan bog‘lovchi atributlar va ularning manbalari.",
        "outputs": "Case bilan bog‘langan hodisalar va har bir bog‘lanishning izohi.",
        "checks": "Bitta umumiy atribut mosligi shaxs aybdorligini isbotlamaydi.",
        "limit": "Hozirgi v4 namunasi bitta sintetik Case ko‘rsatadi; banklararo real tranzaksiya zanjiri yo‘q.",
    },
    {
        "id": "L09", "name": "Citizen Transparency & Appeal",
        "simple": "Fuqaro jarayon holatini tushunishi va xatoga e’tiroz bildirish yo‘lini bilishi uchun xizmat qiladi.",
        "purpose": "Jarayon holati, tushunarli izoh va e’tiroz/tuzatish yo‘lini loyihalash; boshqa shaxslarning maxfiy ma’lumotini oshkor qilmaslik.",
        "question": "Fuqaro o‘ziga tegishli jarayon haqida nimani bilishi va qayerga murojaat qilishi mumkin?",
        "inputs": "Fuqaro ko‘rishi mumkin bo‘lgan holat, izoh, murojaat kanali va oshkor etish cheklovlari.",
        "outputs": "Oddiy tildagi holat izohi va e’tiroz/tuzatish yo‘li.",
        "checks": "Ichki tekshiruv tafsilotlari yoki boshqa shaxsga oid maxfiy ma’lumot ko‘rsatilmaydi.",
        "limit": "Hozirgi prototipda haqiqiy fuqaro kabineti yoki Case qidiruvi yo‘q.",
    },
    {
        "id": "L10", "name": "Privacy & Data Lifecycle",
        "simple": "Ma’lumot nima uchun yig‘ilishi, kim ko‘rishi, qancha saqlanishi va qachon o‘chirilishini belgilaydi.",
        "purpose": "Ma’lumot turi, maqsad, saqlash muddati, kirish, arxivlash va o‘chirish qoidalarini belgilash.",
        "question": "Bu ma’lumotni saqlashga nima asos bor, kim ko‘ra oladi va qachon o‘chiriladi?",
        "inputs": "Ma’lumot toifasi, maqsad, kirish roli, saqlash muddati va o‘chirish talabi.",
        "outputs": "Saqlash/kirish qoidalari va ma’lumot hayotiy sikli bo‘yicha nazorat.",
        "checks": "Faqat vazifa uchun zarur ma’lumotga ruxsat berish va saqlash muddatini cheklash.",
        "limit": "Production ma’lumot ombori, retention siyosati va huquqiy tasdiq mavjud deb ko‘rsatilmaydi.",
    },
    {
        "id": "L11", "name": "Security Incident Response",
        "simple": "Xavfsizlik muammosi yuz bersa, uni qayd etish, cheklash va tiklash tartibini belgilaydi.",
        "purpose": "Hodisa tasnifi, eskalatsiya, dalilni saqlash va tiklash bosqichlarini belgilash.",
        "question": "Xavfsizlik hodisasi yuz bersa, kim nima qiladi va tizim qanday xavfsiz holatga qaytadi?",
        "inputs": "Xato/ogohlantirish signallari, vaqt, ta’sir doirasi, tizim holati va hodisa dalillari.",
        "outputs": "Hodisa qaydi, eskalatsiya yo‘li, saqlangan dalil va tiklash rejasi.",
        "checks": "Tiklash alohida tasdiq va audit izini talab qiladi.",
        "limit": "To‘liq SOC/SIEM integratsiyasi va production incident response sinovlari mavjud emas.",
    },
    {
        "id": "L12", "name": "Knowledge Governance & AI Reliability",
        "simple": "AI yoki bilim yordamchisi javobini manbaga bog‘laydi; dalil yetmasa buni ochiq aytadi.",
        "purpose": "AI javobining manbasini ko‘rsatish, tasdiqlanmagan bilimni rasmiy bilimga aylantirmaslik va yetarli dalil bo‘lmaganda to‘xtash.",
        "question": "Javob qaysi manbaga tayangan va manba yetarlimi?",
        "inputs": "Bilim yozuvi, manba, versiya, tasdiqlash holati, foydalanuvchi savoli va qidiruv natijalari.",
        "outputs": "Manbali javob, noaniqlik izohi yoki dalil yetarli emas degan javob.",
        "checks": "Tashqi internet matni avtomatik ravishda FINZANJIRning tasdiqlangan qoidasi bo‘lib qolmaydi.",
        "limit": "Ushbu v4 UI ichida AI yordamchisi ulanmagan; AI alohida tekshiruv bosqichi.",
    },
    {
        "id": "L13", "name": "Testing & Independent Evaluation",
        "simple": "Har bir talab sinovdan o‘tganmi va natija dalil bilan tasdiqlanganmi — shuni tekshiradi.",
        "purpose": "Talab, test, kutilgan/haqiqiy natija va dalil izchilligini qayd etish; qamrov cheklovlarini hujjatlashtirish.",
        "question": "Nimani sinadik, qanday natija kutdik va amalda nima kuzatildi?",
        "inputs": "Talab ID, test ID, test ma’lumoti, muhit, kutilgan natija va bajarilgan natija.",
        "outputs": "Test natijasi, log/dalil, qamrov va ochiq muammolar.",
        "checks": "Test nomi yoki test rejasi PASS degani emas; natija va dalil kerak.",
        "limit": "Sintetik testlar real bank sharoiti yoki ekspert tasdig‘ini almashtirmaydi.",
    },
    {
        "id": "L14", "name": "Bank Integration Readiness",
        "simple": "Bank bilan ulanishdan oldin texnik, xavfsizlik va huquqiy shartlar tayyormi — shuni baholaydi.",
        "purpose": "Integratsiyani faqat hamkorlik shartlari, spetsifikatsiya va xavfsizlik tasdiqlanganda baholash.",
        "question": "Bank bilan xavfsiz va qonuniy ulanish uchun nimalar tayyor bo‘lishi kerak?",
        "inputs": "API/schema hujjati, autentifikatsiya, ruxsat, sandbox, SLA va hamkorlik kelishuvi.",
        "outputs": "Integratsiyaga tayyorlik bo‘yicha ochiq kamchiliklar va tekshiruv ro‘yxati.",
        "checks": "Tayyor bo‘lmagan integratsiya mavjud deb ko‘rsatilmaydi.",
        "limit": "Hozirgi prototipda haqiqiy bank API, webhook yoki bank ma’lumotlari yo‘q.",
    },
    {
        "id": "L15", "name": "Performance & Capacity Management",
        "simple": "Tizim qancha tez ishlashi, yuklamani ko‘tarishi va xatodan tiklanishini o‘lchashni belgilaydi.",
        "purpose": "Javob vaqti, xato ulushi, resurslar va tiklanish uchun o‘lchash/qabul mezonlarini belgilash.",
        "question": "Tizim kerakli yuklamada barqaror va yetarlicha tez ishlay oladimi?",
        "inputs": "Yuklama profili, javob vaqti, xato, CPU/RAM, navbat va tiklanish o‘lchovlari.",
        "outputs": "Ishlash ko‘rsatkichlari, chegaralar va sig‘im bo‘yicha tavsiyalar.",
        "checks": "O‘lchov muhiti va metodikasi ko‘rsatilmasdan tezlik da’vo qilinmaydi.",
        "limit": "Production yuklama sinovi va qabul mezonlari bajarilmagan.",
    },
    {
        "id": "L16", "name": "Impact & Harm Reduction",
        "simple": "Tizim xato qilsa kimga va qanday zarar yetishi mumkinligini o‘lchashga yordam beradi.",
        "purpose": "False Positive/False Negative va salbiy ta’sir metrikalari uchun formula, denominator, segment va taqqoslash usulini belgilash.",
        "question": "Tizim xato signal bersa yoki muhim holatni o‘tkazib yuborsa, ta’siri qanday o‘lchanadi?",
        "inputs": "Mutaxassis tasdiqlagan etalon, qarorlar, segmentlar, xato turlari va zarar ko‘rsatkichlari.",
        "outputs": "FP/FN va zarar ko‘rsatkichlari, metodika hamda cheklovlar.",
        "checks": "Sababiy ta’sir yoki aniqlik dalilsiz da’vo qilinmaydi.",
        "limit": "Ishonchli ground-truth va real operatsion natijalar mavjud emas; hozircha metrika rejasi.",
    },
]

EVENTS = {
    "SYN-ATO-001": {
        "title": "Yangi qurilma va yangi qabul qiluvchi",
        "source": "Sintetik bank A",
        "time": "2026-11-08 10:42",
        "status": "HUMAN_REVIEW",
        "status_uz": "Inson ko‘rigi uchun namuna",
        "summary": "Bir hodisada bir nechta tekshirilishi kerak bo‘lgan indikator bor. Bu firibgarlik tasdiqlandi degani emas.",
        "signals": [
            ("SIG-001", "Yangi qurilma", "L03", "Kontekst bilan solishtirish kerak"),
            ("SIG-002", "Yangi qabul qiluvchi", "L03", "Oldingi operatsiyalar bilan solishtirish kerak"),
            ("SIG-003", "Rozilik doirasi noaniq", "L04", "Aynan shu o‘tkazma bo‘yicha rozilik dalili ko‘rsatilmagan"),
        ],
        "evidence": [
            ("EVD-SYN-01", "Qurilma identifikatori avvalgi sintetik hodisalarda uchramagan.", "Kontekst indikatori", "Sintetik hodisa yozuvi"),
            ("EVD-SYN-02", "Qabul qiluvchi identifikatori oldingi sintetik tarixda yangi.", "Kontekst indikatori", "Sintetik hodisa yozuvi"),
        ],
        "counter": [],
        "unknowns": [
            "Mijoz aynan shu pul o‘tkazmasiga rozilik berganmi?",
            "Qurilmadan mijozning o‘zi foydalanganmi yoki boshqa shaxsmi?",
            "Mijozga qo‘ng‘iroq yoki ijtimoiy muhandislik orqali ta’sir o‘tkazilganmi?",
        ],
        "case_id": "CASE-SYN-0001",
        "case_reason": "Bir nechta mustaqil sintetik indikator inson ko‘rigiga namuna sifatida jamlangan.",
        "consent": [
            ("Qurilmadan foydalanish", "Noma’lum", "Qurilma egasi va foydalanuvchi tasdig‘i yo‘q."),
            ("Hisobdan foydalanish", "Noma’lum", "Hisob egasining ayni vaqtdagi rozilik dalili yo‘q."),
            ("Aynan shu o‘tkazma", "Noma’lum", "O‘tkazma bo‘yicha aniq rozilik dalili ko‘rsatilmagan."),
        ],
    },
    "SYN-DATA-002": {
        "title": "Majburiy ma’lumot maydoni yetishmaydi",
        "source": "Sintetik bank B",
        "time": "2026-11-08 10:47",
        "status": "DATA_REVIEW",
        "status_uz": "Ma’lumotni to‘ldirish kerak",
        "summary": "Qabul qiluvchi identifikatori yo‘q. Shu sababli keyingi bog‘lash va baholash to‘liq bajarilmaydi.",
        "signals": [("SIG-004", "Qabul qiluvchi maydoni yo‘q", "L02", "Ma’lumot sifati muammosi")],
        "evidence": [],
        "counter": [],
        "unknowns": ["Qabul qiluvchi identifikatori kelgan ma’lumotda mavjud emas."],
        "case_id": "",
        "case_reason": "Majburiy maydon yetishmaydi; Case ochish uchun yetarli kontekst yo‘q.",
        "consent": [
            ("Qurilmadan foydalanish", "Tekshirilmagan", "Kerakli kontekst to‘liq emas."),
            ("Hisobdan foydalanish", "Tekshirilmagan", "Kerakli kontekst to‘liq emas."),
            ("Aynan shu o‘tkazma", "Tekshirilmagan", "Kerakli kontekst to‘liq emas."),
        ],
    },
    "SYN-ONE-003": {
        "title": "Bitta noaniq indikator",
        "source": "Sintetik bank C",
        "time": "2026-11-08 10:51",
        "status": "RECHECK",
        "status_uz": "Qo‘shimcha kontekst kerak",
        "summary": "Operatsiya summasi odatiy sintetik ko‘rsatkichdan yuqori. Yakka indikator yakuniy xulosa uchun yetarli emas.",
        "signals": [("SIG-005", "Kontekstdan yuqori summa", "L03", "Yakka indikator, qo‘shimcha kontekst kerak")],
        "evidence": [("EVD-SYN-03", "Operatsiya summasi oldingi sintetik medianadan yuqori.", "Kontekst indikatori", "Sintetik tarix")],
        "counter": [],
        "unknowns": ["Mijozning odatiy operatsiya konteksti to‘liq emas."],
        "case_id": "",
        "case_reason": "Bitta indikator Case ochish uchun yetarli emas; kuzatuv yoki qayta tekshiruv kerak.",
        "consent": [
            ("Qurilmadan foydalanish", "Noma’lum", "Ushbu misolda rozilik dalili keltirilmagan."),
            ("Hisobdan foydalanish", "Noma’lum", "Ushbu misolda rozilik dalili keltirilmagan."),
            ("Aynan shu o‘tkazma", "Noma’lum", "Ushbu misolda rozilik dalili keltirilmagan."),
        ],
    },
    "SYN-CLEAR-004": {
        "title": "Yetarli shubhali indikator kuzatilmadi",
        "source": "Sintetik bank D",
        "time": "2026-11-08 11:02",
        "status": "MONITOR",
        "status_uz": "Kuzatuv namunasida",
        "summary": "Ushbu sintetik namuna bo‘yicha ko‘rsatilgan qoidalarda qo‘shimcha tekshiruvga sabab bo‘ladigan indikator aniqlanmagan.",
        "signals": [],
        "evidence": [],
        "counter": [],
        "unknowns": ["Bu namuna barcha ehtimoliy xavflar yo‘qligini isbotlamaydi."],
        "case_id": "",
        "case_reason": "Ko‘rsatilgan namuna bo‘yicha Case ochish mezoniga yetilmadi.",
        "consent": [
            ("Qurilmadan foydalanish", "Baholanmagan", "Bu namuna rozilikni alohida tasdiqlamaydi."),
            ("Hisobdan foydalanish", "Baholanmagan", "Bu namuna rozilikni alohida tasdiqlamaydi."),
            ("Aynan shu o‘tkazma", "Baholanmagan", "Bu namuna rozilikni alohida tasdiqlamaydi."),
        ],
    },
}

PIPELINE = [
    ("01", "Manba va hodisani qabul qilish", "L01 · L14", "Hodisa qayerdan kelgani va qaysi formatda olingani qayd etiladi."),
    ("02", "Ma’lumot sifatini tekshirish", "L02 · L10", "Majburiy maydonlar, eskirgan qiymatlar va ziddiyatlar tekshiriladi."),
    ("03", "16 qatlam talablari bo‘yicha ko‘rib chiqish", "L01–L16", "Har bir qatlam o‘z vazifasi bo‘yicha ma’lumotni tekshirishga hissa qo‘shadi; hammasi hozir to‘liq ishlaydi degani emas."),
    ("04", "Signal, dalil va noma’lumlarni ajratish", "L03 · L08 · L12", "Kuzatilgan indikator, dalil manbasi va hali noma’lum faktlar alohida ko‘rsatiladi."),
    ("05", "Case ochish mezonlarini baholash", "L03 · L04 · L07", "Yakka indikator bilan Case ochilmaydi; yetarli asos va vakolatli jarayon talab qilinadi."),
    ("06", "Case kontekstini jamlash", "L08 · L10", "Tegishli hodisalar, signallar, rozilik doirasi va noma’lumlar bitta ish yozuvida jamlanadi."),
    ("07", "Human Review", "L04 · L05", "Mutaxassis dalillarni ko‘rib, qaror va sababni qayd etadi."),
    ("08", "Audit, sinov va ta’sirni baholash", "L01 · L11 · L13 · L16", "Jarayon izi, test dalili va xatolarning ehtimoliy ta’siri ko‘rib chiqiladi."),
]

def metric(label: str, value: str, note: str, icon: str) -> None:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{icon} &nbsp; {label}</div>'
        f'<div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
        unsafe_allow_html=True,
    )

def status_text(code: str) -> str:
    return {
        "HUMAN_REVIEW": "Inson ko‘rigi",
        "DATA_REVIEW": "Ma’lumot tekshiruvi",
        "RECHECK": "Qayta tekshiruv",
        "MONITOR": "Kuzatuv",
    }.get(code, code)

def render_readonly_notice() -> None:
    st.markdown(
        '<div class="callout"><b>Ochiq ko‘rish rejimi.</b> Bu sahifadagi menyu va qidiruv faqat ma’lumotni ko‘rish uchun. '
        'Tashrifchilar hodisa, Case, qatlam, qoida yoki tizim sozlamalarini o‘zgartira olmaydi.</div>',
        unsafe_allow_html=True,
    )

def render_pipeline(active: int | None = None) -> None:
    for index, (number, title, layers, description) in enumerate(PIPELINE):
        cls = "step step-focus" if active == index else "step"
        st.markdown(
            f'<div class="{cls}"><div class="step-title">{number}. {title}</div>'
            f'<div class="step-meta">Tegishli qatlamlar: {layers}</div><div class="small">{description}</div></div>',
            unsafe_allow_html=True,
        )

def render_event_detail(event_id: str) -> None:
    event = EVENTS[event_id]
    st.markdown(f"### {event['title']}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Hodisa ID", event_id)
    c2.metric("Manba", event["source"])
    c3.metric("Holat", status_text(event["status"]))
    st.caption(f"Namuna vaqti: {event['time']} · Bu yozuv to‘liq sintetik.")
    st.write(event["summary"])

    st.markdown("#### Aniqlangan signallar")
    if event["signals"]:
        st.dataframe(
            [{"Signal ID": x[0], "Indikator": x[1], "Qatlam": x[2], "Izoh": x[3]} for x in event["signals"]],
            use_container_width=True, hide_index=True,
        )
    else:
        st.info("Ushbu sintetik namuna uchun signal qayd etilmagan.")

    left, right = st.columns(2)
    with left:
        st.markdown("#### Dalillar va kuzatuvlar")
        if event["evidence"]:
            for evidence_id, description, kind, source in event["evidence"]:
                st.markdown(f"**{evidence_id} · {kind}**")
                st.write(description)
                st.caption(f"Manba: {source}")
        else:
            st.info("Ushbu namunada dalil yozuvi keltirilmagan.")
    with right:
        st.markdown("#### Qarshi dalillar")
        if event["counter"]:
            for item in event["counter"]:
                st.write("• " + item)
        else:
            st.info("Ushbu namuna uchun qarshi dalil keltirilmagan. Bu qarshi dalil yo‘q degan isbot emas.")

    st.markdown("#### Hali noma’lum yoki tekshirilmagan jihatlar")
    for item in event["unknowns"]:
        st.markdown("- " + item)

    if event["case_id"]:
        st.success(f"Bog‘langan sintetik Case: {event['case_id']}")
    else:
        st.warning("Ushbu hodisa bo‘yicha sintetik Case ochilmagan.")

# Top-level navigation stays visible on desktop and mobile.
# It changes the displayed page only; no public data or settings can be edited.
pages = [
    "Bosh sahifa",
    "Boshqaruv paneli",
    "Sun’iy bank laboratoriyasi",
    "Yagona ish jarayoni",
    "Signallar reyestri",
    "16 qatlam",
    "FINZANJIR AI",
    "Case markazi",
    "Human Review",
    "Banklararo tahlil (sintetik)",
    "KPI dashboard",
    "Fuqaro uchun tushuntirish",
    "Audit jurnali",
    "Qatlamlararo xarita",
    "Sintetik sinovlar",
    "Atamalar va cheklovlar",
]

st.markdown('<div class="brand">FINZANJIR</div>', unsafe_allow_html=True)
st.markdown('<div class="subbrand">Firibgarlik xavfini tekshirish uchun signal, dalil va inson ko‘rigini bir jarayonga bog‘lovchi konsepsiya</div>', unsafe_allow_html=True)
st.markdown("")
nav_col, mode_col = st.columns([1.25, 1])
with nav_col:
    page = st.selectbox("BO‘LIMNI TANLANG", pages, key="public_navigation")
with mode_col:
    st.markdown(
        '<div class="callout"><b>Ochiq ko‘rish rejimi</b><br><span class="small">Faqat sintetik ma’lumot · tahrirlash yo‘q · avtomatik bloklash yo‘q</span></div>',
        unsafe_allow_html=True,
    )
render_readonly_notice()

if page == "Bosh sahifa":
    st.markdown(
        '<div class="hero"><span class="hero-tag">OCHIQ NAMOYISH</span><span class="hero-tag">SINTETIK MA’LUMOT</span>'
        '<h2>Moliyaviy firibgarlik xavfini dalillar asosida tekshirish</h2>'
        '<p>FINZANJIR turli manbalardan keladigan ruxsat etilgan signallarni tartibga solish, noaniqliklarni ko‘rsatish, '
        'tekshiruv uchun Case tayyorlash va inson ko‘rigini qo‘llab-quvvatlash konsepsiyasidir.</p></div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Bir qarashda")
    a, b, c, d = st.columns(4)
    with a: metric("Namoyish hodisalari", str(len(EVENTS)), "Barchasi sintetik", "📥")
    with b: metric("Case namunasi", str(sum(1 for x in EVENTS.values() if x["case_id"])), "Haqiqiy ish emas", "📁")
    with c: metric("Qatlamlar katalogi", "16", "Talablar darajasida", "🧩")
    with d: metric("Ommaviy tahrirlash", "Yo‘q", "Faqat ko‘rish", "🔒")

    left, right = st.columns([1.15, 1])
    with left:
        st.markdown("### FINZANJIR qanday ishlashi ko‘zda tutilgan?")
        render_pipeline()
    with right:
        st.markdown("### Muhim farqlar")
        st.markdown(
            '<div class="panel"><b>Signal</b><br><span class="small">Tekshirishga sabab bo‘ladigan indikator. Aybdorlik isboti emas.</span><hr>'
            '<b>Dalil</b><br><span class="small">Manbasi va cheklovi ko‘rsatilgan material.</span><hr>'
            '<b>Case</b><br><span class="small">Tekshiruv uchun jamlangan ish yozuvi. Hukm emas.</span><hr>'
            '<b>Human Review</b><br><span class="small">Vakolatli insonning dalillarga tayangan ko‘rigi.</span></div>',
            unsafe_allow_html=True,
        )
    st.markdown("### Bu prototip nimalarni ko‘rsatadi?")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="panel"><b>Oddiy tushuntirish</b><p class="small">Har bir bo‘limda “bu nima?” va “nima uchun kerak?” savollariga sodda javob bor.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="panel"><b>Mutaxassis ko‘rigi</b><p class="small">Qatlam vazifasi, ma’lumot talabi, dalil, noma’lum jihat va cheklovlar ochiq ko‘rsatiladi.</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="panel"><b>Halol prototip holati</b><p class="small">Rejalashtirilgan, sintetik namoyish qilingan va hali tasdiqlanmagan ishlar bir-biridan ajratiladi.</p></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="warning-note"><b>Muhim:</b> bu ishlab chiqish prototipi. Haqiqiy bank API, mijoz ma’lumotlari, '
        'production vakolati yoki real firibgarlik aniqligi mavjud deb da’vo qilinmaydi. FINZANJIR karta, hisob yoki tranzaksiyani avtomatik bloklamaydi.</div>',
        unsafe_allow_html=True,
    )

elif page == "Boshqaruv paneli":
    st.markdown("## Boshqaruv paneli — namoyish holati")
    st.caption("Bu ko‘rsatkichlar faqat quyidagi to‘rtta v4 sintetik namunasidan hisoblanadi. Ular real bank statistikasi emas.")
    counts = {code: sum(1 for event in EVENTS.values() if event["status"] == code) for code in ("HUMAN_REVIEW", "DATA_REVIEW", "RECHECK", "MONITOR")}
    a, b, c, d = st.columns(4)
    with a: metric("Sintetik hodisalar", str(len(EVENTS)), "v4 namuna to‘plami", "📥")
    with b: metric("Inson ko‘rigi", str(counts["HUMAN_REVIEW"]), "Case namunasi", "👤")
    with c: metric("Ma’lumot tekshiruvi", str(counts["DATA_REVIEW"]), "Majburiy maydon", "🧾")
    with d: metric("Qayta tekshiruv / kuzatuv", str(counts["RECHECK"] + counts["MONITOR"]), "Yakka indikator yoki kuzatuv", "🔎")
    st.markdown("### Holatlar taqsimoti")
    st.dataframe(
        [{"Holat": status_text(code), "Soni": number, "Izoh": {
            "HUMAN_REVIEW": "Bir nechta sintetik indikator — inson ko‘rigi namunasi",
            "DATA_REVIEW": "Ma’lumot maydoni yetishmaydi",
            "RECHECK": "Yakka indikator — qo‘shimcha kontekst kerak",
            "MONITOR": "Ko‘rsatilgan qoidalarda signal aniqlanmadi",
        }[code]} for code, number in counts.items()],
        use_container_width=True, hide_index=True,
    )
    st.markdown("### Barcha namuna hodisalari")
    st.dataframe(
        [{"Hodisa ID": event_id, "Manba": event["source"], "Holat": event["status_uz"],
          "Signal soni": len(event["signals"]), "Case": event["case_id"] or "Ochilmagan"}
         for event_id, event in EVENTS.items()],
        use_container_width=True, hide_index=True,
    )
    st.info("Bu panel v4 ning to‘rtta ko‘rgazmali yozuvini jamlaydi. U v3 dagi 400 hodisali laboratoriya statistikasi bilan aralashtirilmaydi.")

elif page == "Sun’iy bank laboratoriyasi":
    st.markdown("## Sun’iy bank laboratoriyasi")
    st.caption("Bu bo‘lim oldingi v3 sinov yo‘nalishining holatini tushuntiradi; v4 ichida laboratoriya ishga tushirilmaydi.")
    a, b, c = st.columns(3)
    with a: metric("Sintetik manbalar", "4", "v3 laboratoriya dizayni", "🏦")
    with b: metric("Sintetik ssenariylar", "400", "v3 deterministik to‘plami", "🧪")
    with c: metric("v4 bilan integratsiya", "Yo‘q", "Alohida ishlab chiqish bosqichi", "🔗")
    st.markdown("### Laboratoriya qanday ishlashi ko‘zda tutilgan?")
    render_pipeline()
    st.markdown("### Boshqaruv amallari haqida")
    st.write("v3 laboratoriyasida START, PAUSE, STOP, RESUME, RESET va favqulodda KILL SWITCH boshqaruvlari mavjud bo‘lgan. Ommaviy v4 ko‘rinishida bu amallar ataylab chiqarilmagan: tashrifchi sinov navbatini yoki natijalarni o‘zgartira olmaydi.")
    st.warning("400 ta sintetik hodisa v3 branchdagi alohida modulga tegishli. Ular v4 dagi to‘rtta namuna bilan bir xil ma’lumotlar to‘plami emas va hozir v4 jarayoniga ulanmagan.")

elif page == "Yagona ish jarayoni":
    st.markdown("## Hodisadan inson ko‘rigigacha")
    st.caption("Bitta hodisa butun jarayon bo‘ylab bir xil identifikator bilan kuzatilishi kerak. Quyidagi oqim — maqsadli jarayon modeli.")
    chosen = st.selectbox("Ko‘rish uchun sintetik hodisani tanlang", list(EVENTS.keys()), format_func=lambda x: f"{x} · {EVENTS[x]['title']}")
    event = EVENTS[chosen]
    active = {"HUMAN_REVIEW": 6, "DATA_REVIEW": 1, "RECHECK": 3, "MONITOR": 7}[event["status"]]
    left, right = st.columns([1.05, 1])
    with left:
        render_pipeline(active=active)
    with right:
        st.markdown("### Tanlangan hodisaning holati")
        st.markdown(f"**{chosen}**")
        st.markdown(f'<span class="status">{event["status_uz"]}</span>', unsafe_allow_html=True)
        st.write(event["summary"])
        if event["case_id"]:
            st.success(f"Case: {event['case_id']}")
        else:
            st.info("Case ochilmagan. Bu xato emas: ma’lumot yoki mezon yetarli bo‘lmasligi mumkin.")
    st.divider()
    render_event_detail(chosen)
    st.markdown("### Boshqa yo‘nalishlar ham muhim")
    st.markdown("- Yetishmayotgan yoki zid ma’lumot → **DATA_REVIEW**.")
    st.markdown("- Yakka noaniq indikator → **RECHECK / MONITORING**.")
    st.markdown("- Case mezonlari bajarilmagan → **NO_CASE**, sabab bilan.")
    st.markdown("- Yetarli mustaqil indikatorlar va belgilangan mezonlar → **CASE_CANDIDATE**, keyin vakolatli jarayon.")
    st.markdown("- Case ochilishi aybdorlikni anglatmaydi; keyingi bosqich — **Human Review**.")

elif page == "16 qatlam":
    st.markdown("## 16 qatlam — yagona arxitektura")
    st.caption("Qatlamlar alohida-alohida mahsulot emas. Ular bitta hodisa va Case kontekstida turli savollarni tekshiradigan funksional va nazorat yo‘nalishlaridir.")
    st.markdown(
        '<div class="warning-note"><b>Holatni to‘g‘ri tushunish:</b> quyidagi nom va vazifalar 16 qatlam katalogidagi talab mazmunini tushuntiradi. '
        'Ularning barchasi hozir kodda to‘liq ishlayapti yoki ekspertlar tomonidan tasdiqlangan degani emas. '
        'Hozirgi v4 da bu — manba asosidagi talablar katalogi va ko‘rish interfeysi.</div>',
        unsafe_allow_html=True,
    )
    query = st.text_input("Qatlamlarni qidirish", placeholder="Masalan: dalil, rozilik, maxfiylik, AI, bank integratsiyasi")
    matches = [layer for layer in LAYERS if query.casefold() in " ".join(str(v) for v in layer.values()).casefold()]
    st.caption(f"{len(matches)} / 16 qatlam ko‘rsatilmoqda")
    cols = st.columns(2)
    for index, layer in enumerate(matches):
        with cols[index % 2]:
            st.markdown(
                f'<div class="layer-card"><div class="layer-id">{layer["id"]} · TALAB KATALOGI</div>'
                f'<div class="layer-name">{layer["name"]}</div><div class="small">{layer["simple"]}</div>'
                f'<div style="margin-top:10px"><span class="status">Ekspert tasdig‘i kutilmoqda</span></div></div>',
                unsafe_allow_html=True,
            )
            with st.expander(f"{layer['id']} tafsilotlari"):
                st.markdown("**Maqsadi**")
                st.write(layer["purpose"])
                st.markdown("**Qatlam javob beradigan savol**")
                st.write(layer["question"])
                st.markdown("**Kirish ma’lumotlari — talab darajasida**")
                st.write(layer["inputs"])
                st.markdown("**Kutiladigan chiqish — talab darajasida**")
                st.write(layer["outputs"])
                st.markdown("**Muhim nazorat**")
                st.write(layer["checks"])
                st.markdown("**Hozirgi cheklov**")
                st.warning(layer["limit"])
                st.caption("Holat: PLANNED / EXPERT_VALIDATION_PENDING. Bu karta implementatsiya dalili emas.")
    if not matches:
        st.info("Bu so‘z bo‘yicha qatlam topilmadi. Boshqa atama bilan qidirib ko‘ring.")
    st.markdown("### Qatlamlar haqida uchta muhim qoida")
    st.markdown("1. Har bir qatlamning o‘z vazifasi, kirish/chiqish talabi va cheklovi bor.")
    st.markdown("2. Bir qatlamdan boshqasiga o‘tadigan ma’lumot manba, vaqt va versiya izini yo‘qotmasligi kerak.")
    st.markdown("3. Qatlamlararo aloqa takliflari rasmiy LINK-ID yoki tayyor texnik API degani emas.")

elif page == "Signallar reyestri":
    st.markdown("## Signal reyestri va dalil tafsilotlari")
    st.caption("Signal — indikator. U yakuniy xulosa, aybdorlik yoki avtomatik bloklash buyrug‘i emas.")
    chosen = st.selectbox("Hodisani tanlang", list(EVENTS.keys()), format_func=lambda x: f"{x} · {EVENTS[x]['title']}")
    render_event_detail(chosen)
    st.markdown("### Signal va dalilni farqlash")
    left, right = st.columns(2)
    with left:
        st.markdown('<div class="panel"><b>Signal / indikator</b><p class="small">Kuzatilgan belgi yoki qoida natijasi. Tekshiruvni boshlashga yordam beradi, lekin o‘zi bilan ayblov yoki yakuniy xulosa bermaydi.</p></div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><b>Dalil</b><p class="small">Manbasi, vaqti, mazmuni va ishonchlilik cheklovi ko‘rsatilgan material. Dalil tasdiqlashi ham, inkor etishi ham mumkin.</p></div>', unsafe_allow_html=True)

elif page == "FINZANJIR AI":
    st.markdown("## FINZANJIR AI — bilim va tushuntirish yordamchisi")
    st.caption("Ichki loyiha bilimlari + Gemini. Google Search alohida yoqiladi; javoblar loyiha qarori yoki ekspert xulosasini almashtirmaydi.")
    st.markdown(
        '<div class="callout"><b>Bu yordamchi nimalarni qiladi?</b><br>'
        '<span class="small">FINZANJIR konsepsiyasi, 16 qatlam, signal, dalil, Case va Human Review haqida hujjatlarga tayangan holda tushuntiradi. '
        'Joriy yoki tashqi ma’lumot kerak bo‘lsa Google Search grounding orqali manba qidirishi mumkin.</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown("")
    try:
        gemini_config = st.secrets.get("gemini", {})
        gemini_enabled = gemini_config.get("enabled", False) is True
        gemini_key = str(gemini_config.get("api_key", "") or "").strip()
        gemini_model = str(gemini_config.get("model", ai_assistant.DEFAULT_MODEL) or ai_assistant.DEFAULT_MODEL)
        request_cap = max(1, min(int(gemini_config.get("max_requests_per_session", 5)), 20))
    except Exception:
        gemini_enabled, gemini_key = False, ""
        gemini_model, request_cap = ai_assistant.DEFAULT_MODEL, 5

    st.info(
        "Maxfiylik: savolingiz va unga mos ichki bilim parchalari Gemini xizmatiga yuboriladi. "
        "Google Search yoqilsa, Gemini qidiruvdan ham foydalanishi mumkin. Haqiqiy mijoz ma’lumoti, "
        "karta raqami, PIN, CVV, OTP yoki parol kiritmang. Gemini so‘rovlari store=false bilan yuboriladi; ilova savollarni o‘zining doimiy bilimlar bazasiga yozmaydi."
    )
    response_mode = st.radio(
        "Javob uslubi",
        ["Sodda tushuntirish", "Ekspert tahlili"],
        horizontal=True,
        key="finzanjir_ai_response_mode",
    )
    use_google_search = st.checkbox(
        "Google Search orqali yangilangan internet manbalarini ham tekshirish",
        value=False,
        help="Qonunchilik, xalqaro tajriba yoki joriy ma’lumot kerak bo‘lganda yoqing. Google Search grounding qo‘shimcha xarajat keltirishi mumkin.",
    )
    question = st.text_area(
        "Savolingizni yozing",
        placeholder="Masalan: FINZANJIRning 16 qatlami qanday qilib Case va Human Review jarayoniga bog‘lanadi?",
        max_chars=ai_assistant.MAX_QUESTION_CHARS,
        height=115,
        key="finzanjir_ai_question",
    )
    if not gemini_enabled:
        st.warning("AI hozircha o‘chirilgan. Muallif Streamlit Secrets ichida [gemini] enabled = true qilib, yangi API kalitini xavfsiz kiritishi kerak.")
    elif not gemini_key:
        st.warning("Gemini API kaliti topilmadi. Streamlit Cloud → App settings → Secrets bo‘limida [gemini] api_key sozlang. Kalitni GitHub yoki chatga joylashtirmang.")
    else:
        used_requests = int(st.session_state.get("finzanjir_ai_requests_used", 0))
        st.caption(f"Ushbu brauzer sessiyasidagi so‘rovlar: {used_requests}/{request_cap}. Bu yumshoq sessiya cheklovi, Google billing limiti emas.")
        if st.button("Savolga javob olish", type="primary", disabled=not question.strip(), key="finzanjir_ai_submit"):
            if used_requests >= request_cap:
                st.error("Ushbu sessiya uchun ajratilgan AI so‘rovlari tugadi.")
            else:
                st.session_state.finzanjir_ai_requests_used = used_requests + 1
                try:
                    with st.spinner("Ichki bilimlar tekshirilmoqda va javob tayyorlanmoqda..."):
                        result = ai_assistant.answer_question(
                            question,
                            gemini_key,
                            use_google_search=use_google_search,
                            model=gemini_model,
                            response_mode=response_mode,
                        )
                    st.markdown("### Javob")
                    st.markdown(result["answer"])
                    if use_google_search:
                        if result["google_sources"]:
                            st.markdown("### Google Search manbalari")
                            for source in result["google_sources"]:
                                st.markdown(f"- [{source['title']}]({source['url']})")
                        else:
                            st.warning("Gemini javobida tekshiriladigan Google Search manbalari qaytmadi. Tashqi faktlarni mustaqil tekshiring.")
                        if result["google_queries"]:
                            st.caption("Qidiruv so‘rovlari: " + " · ".join(result["google_queries"]))
                    with st.expander("Javobda ishlatilgan FINZANJIR ichki bilimlari", expanded=False):
                        st.caption(f"Bilimlar bazasidagi yozuvlar: {result['knowledge_records_total']}")
                        for item in result["internal_evidence"]:
                            st.markdown(
                                f"**{item['id']}** · {item['approval']} · "
                                f"{item['source_id']} / {item['source_version']}"
                            )
                            st.caption(item["source_section"] + " · " + item["source_path"])
                            st.write(item["text"])
                    st.caption("Model: " + result["model"] + " · Ichki bilimlar candidate_not_authoritative bo‘lsa, rasmiy tasdiq deb talqin qilinmaydi.")
                except ai_assistant.AssistantError as exc:
                    st.error(str(exc))
    st.markdown("### Muhim chegaralar")
    st.markdown("- AI bilimlar bazasini, Case yoki Human Review holatini o‘zgartira olmaydi.")
    st.markdown("- Tashqi qidiruv natijalari FINZANJIRning rasmiy qoidasi sifatida qabul qilinmaydi.")
    st.markdown("- Ichki hujjatlarda topilmagan loyiha fakti tasdiqlangan deb aytilmaydi.")
    st.markdown("- AI javobi xato bo‘lishi mumkin; muhim qarorlar asl hujjat va vakolatli ekspert bilan tekshiriladi.")
    st.warning("Sessiya bo‘yicha so‘rov soni faqat oddiy xarajat nazorati. U kuchli abuse-protection yoki Google billing limitining o‘rnini bosmaydi. Ommaviy ishga tushirishdan oldin Google AI Studio/Cloud kvota va billing ogohlantirishlarini sozlash kerak.")

elif page == "Case markazi":
    st.markdown("## Case markazi — sintetik namuna")
    st.caption("Case — tekshiruv uchun jamlangan kontekst. Bu aybdorlik hukmi emas.")
    cases = [(event_id, event) for event_id, event in EVENTS.items() if event["case_id"]]
    if not cases:
        st.info("Hozircha sintetik Case yo‘q.")
    else:
        event_id, event = cases[0]
        st.markdown(f"### {event['case_id']}")
        st.markdown('<span class="status">OPEN · SINTETIK NAMUNA</span>', unsafe_allow_html=True)
        st.write(event["case_reason"])
        a, b, c = st.columns(3)
        a.metric("Bog‘langan hodisa", "1")
        b.metric("Bog‘langan signal", str(len(event["signals"])))
        c.metric("Noma’lum savol", str(len(event["unknowns"])))
        tab1, tab2, tab3, tab4 = st.tabs(["Umumiy", "Signal va dalillar", "Rozilik doirasi", "Jarayon tarixi"])
        with tab1:
            st.markdown("**Tekshirilayotgan gipoteza**")
            st.write("Hisob yoki qurilmadan ruxsatsiz foydalanish ehtimoli tekshirilmoqda. Bu tasdiqlangan firibgarlik degani emas.")
            st.markdown("**Case ochish sababi**")
            st.write(event["case_reason"])
            st.markdown("**Hozirgi holat**")
            st.write("Inson ko‘rigi uchun sintetik namuna.")
            st.markdown("**Chegara**")
            st.write("Haqiqiy mijoz, bank yoki tranzaksiya ma’lumoti mavjud emas.")
        with tab2:
            render_event_detail(event_id)
        with tab3:
            st.write("Rozilik bitta umumiy “bor/yo‘q” belgisi emas. Kamida quyidagi uch doira alohida tekshirilishi kerak.")
            st.dataframe(
                [{"Rozilik doirasi": x[0], "Namuna holati": x[1], "Izoh": x[2]} for x in event["consent"]],
                use_container_width=True, hide_index=True,
            )
            st.warning("Ushbu namuna uchala doira bo‘yicha ham rozilikni tasdiqlamaydi. Noma’lum holatni “rozilik yo‘q” yoki “rozilik bor” deb talqin qilib bo‘lmaydi.")
        with tab4:
            st.markdown("1. 10:42 · Sintetik hodisa qabul qilindi.")
            st.markdown("2. 10:42 · Sintetik indikatorlar qayd etildi.")
            st.markdown("3. 10:42 · Case namuna sifatida shakllantirildi.")
            st.caption("Bu ko‘rgazmali vaqt chizig‘i. Doimiy va o‘zgartirib bo‘lmaydigan audit jurnali emas.")
    st.markdown("### Case ochilmasligi ham to‘g‘ri natija bo‘lishi mumkin")
    st.write("Ma’lumot yetishmasa DATA_REVIEW, yakka noaniq indikator bo‘lsa RECHECK, mezonlar bajarilmasa NO_CASE holati saqlanadi. Tizim har bir hodisadan majburan Case yasamasligi kerak.")

elif page == "Banklararo tahlil (sintetik)":
    st.markdown("## Banklararo tahlil — sintetik konsepsiya")
    st.caption("Maqsad — qonuniy ruxsat etilgan va zarur bo‘lgan atributlarni turli bank manbalari kesimida ehtiyotkorlik bilan solishtirish.")
    st.markdown('<div class="panel"><b>Misol:</b> bir xil psevdonim qurilma belgisi ikki sintetik bank yozuvida uchrashi mumkin. Bu tekshiruv uchun moslik indikatori, lekin shaxs bir xil yoki aybdor degan isbot emas.</div>', unsafe_allow_html=True)
    st.markdown("### Chegaralar")
    st.markdown("- Hozirgi v4 da banklararo haqiqiy API yoki ma’lumot almashinuvi yo‘q.")
    st.markdown("- v3 da alohida sintetik atribut mosligi ko‘rinishi ishlab chiqilgan, lekin v4 ga integratsiya qilinmagan.")
    st.markdown("- Qabul qiluvchi bank maydoni bo‘lmasa, A → B → C pul o‘tkazma zanjiri deb xulosa qilinmaydi.")
    st.markdown("- Umumiy qurilma, IP yoki boshqa atribut mosligi aybdorlik isboti emas.")
    st.info("Bu sahifa banklararo tahlilning maqsadi va ehtiyot chegaralarini ko‘rsatadi; real banklararo grafik yoki mablag‘ oqimini ko‘rsatmaydi.")

elif page == "KPI dashboard":
    st.markdown("## KPI dashboard — sintetik jarayon ko‘rsatkichlari")
    st.caption("Bu ko‘rsatkichlar faqat v4 dagi to‘rtta sintetik namuna bo‘yicha jarayon holatlarini sanaydi.")
    counts = {code: sum(1 for event in EVENTS.values() if event["status"] == code) for code in ("HUMAN_REVIEW", "DATA_REVIEW", "RECHECK", "MONITOR")}
    a, b, c, d = st.columns(4)
    with a: metric("Jami namunalar", str(len(EVENTS)), "Sintetik", "📥")
    with b: metric("Case namunasi", str(sum(1 for event in EVENTS.values() if event["case_id"])), "Haqiqiy Case emas", "📁")
    with c: metric("Signal yozuvlari", str(sum(len(event["signals"]) for event in EVENTS.values())), "Sintetik indikatorlar", "📡")
    with d: metric("Case ochilmagan", str(sum(1 for event in EVENTS.values() if not event["case_id"])), "Bu xato bo‘lishi shart emas", "🧭")
    st.dataframe(
        [{"Holat": status_text(code), "Namunalar soni": number} for code, number in counts.items()],
        use_container_width=True, hide_index=True,
    )
    st.warning("Bu aniqlik, precision, recall, FP/FN yoki real firibgarlik darajasi emas. Bunday KPI uchun ekspert tasdiqlagan etalon ma’lumot va aniq metodika kerak.")

elif page == "Fuqaro uchun tushuntirish":
    st.markdown("## Fuqaro uchun sodda tushuntirish")
    st.caption("FINZANJIR konsepsiyasi oddiy tilda qanday ishlashi mumkin?")
    st.markdown("### Agar operatsiyada noodatiy holat ko‘rinsa nima bo‘ladi?")
    steps = [
        ("1. Belgi kuzatiladi", "Masalan, yangi qurilma yoki odatdagidan farqli operatsiya. Bu hali firibgarlik degani emas."),
        ("2. Ma’lumot tekshiriladi", "Tizim kerakli ma’lumot to‘liqmi, manbasi ma’lummi va boshqa ma’lumotga zid emasmi — shuni tekshiradi."),
        ("3. Rozilik alohida ko‘riladi", "Qurilmadan foydalanish, hisobdan foydalanish va aynan pul o‘tkazmasiga rozilik bir xil narsa emas."),
        ("4. Zarur bo‘lsa Case tayyorlanadi", "Case — tekshiruv uchun jamlangan ma’lumotlar. Bu ayblov yoki hukm emas."),
        ("5. Inson mutaxassis ko‘radi", "Mutaxassis dalillarni, qarshi dalillarni va noma’lum savollarni ko‘rib chiqadi."),
    ]
    for title, description in steps:
        st.markdown(f'<div class="step"><div class="step-title">{title}</div><div class="small">{description}</div></div>', unsafe_allow_html=True)
    st.markdown("### Fuqaro uchun muhim tamoyillar")
    st.markdown("- Noodatiy signal avtomatik aybdorlik degani emas.")
    st.markdown("- FINZANJIR karta, hisob yoki tranzaksiyani o‘zi bloklamaydi.")
    st.markdown("- Ma’lumot yetarli bo‘lmasa, buni yashirmasdan ko‘rsatishi kerak.")
    st.markdown("- Haqiqiy murojaat, e’tiroz va ma’lumot olish tartibi tegishli vakolatli tashkilotlar bilan kelishilishi kerak.")
    st.warning("Bu tushuntirish konsepsiya namunasidir. Hozircha fuqaro uchun haqiqiy shaxsiy kabinet yoki Case qidiruvi mavjud emas.")

elif page == "Audit jurnali":
    st.markdown("## Audit jurnali — ko‘rgazmali namuna")
    st.caption("Audit izi kim, qachon, qaysi obyekt bilan nima qilganini tekshirish imkonini berishi kerak.")
    st.dataframe(
        [
            {"Vaqt": "10:42:00", "Amal": "SYNTHETIC_EVENT_RECEIVED", "Obyekt": "SYN-ATO-001", "Holat": "NAMUNA"},
            {"Vaqt": "10:42:01", "Amal": "SIGNALS_RECORDED", "Obyekt": "SIG-001…003", "Holat": "NAMUNA"},
            {"Vaqt": "10:42:02", "Amal": "EVIDENCE_AND_UNKNOWNS_LINKED", "Obyekt": "CASE-SYN-0001", "Holat": "NAMUNA"},
            {"Vaqt": "10:42:03", "Amal": "CASE_CANDIDATE_FOR_HUMAN_REVIEW", "Obyekt": "CASE-SYN-0001", "Holat": "NAMUNA"},
        ],
        use_container_width=True, hide_index=True,
    )
    st.warning("Bu ko‘rgazmali jadval. U doimiy, o‘zgartirib bo‘lmaydigan yoki haqiqiy foydalanuvchi amallarini yozadigan audit ombori emas.")

elif page == "Human Review":
    st.markdown("## Human Review — inson ko‘rigi")
    st.caption("Bu bo‘lim mutaxassis qanday savollarni ko‘rib chiqishini ko‘rsatadi. Ommaviy versiyada qaror kiritish yoki Case holatini o‘zgartirish funksiyasi yo‘q.")
    event_id = "SYN-ATO-001"
    event = EVENTS[event_id]
    st.markdown(f"### {event['case_id']} · ko‘rib chiqish namunasi")
    st.markdown('<span class="status">FAQAT KO‘RISH · SINTETIK</span>', unsafe_allow_html=True)
    st.markdown("#### Mutaxassis tekshirishi kerak bo‘lgan savollar")
    checklist = [
        "Har bir signalning manbasi va vaqti tekshirilganmi?",
        "Signalni tasdiqlovchi va inkor etuvchi dalillar ajratilganmi?",
        "Qurilma, hisob va aynan shu o‘tkazma bo‘yicha rozilik alohida tekshirilganmi?",
        "Yetishmayotgan ma’lumot va qarama-qarshiliklar ochiq ko‘rsatilganmi?",
        "Boshqa begunoh izohlar ham ko‘rib chiqilganmi?",
        "Qaror sababi va qolgan noma’lum savollar qayd etilganmi?",
    ]
    for item in checklist:
        st.markdown("• " + item)
    st.markdown("#### Ko‘rib chiqish mumkin bo‘lgan natijalar")
    st.dataframe(
        [
            {"Natija": "Qo‘shimcha ma’lumot so‘rash", "Mazmuni": "Muhim fakt yetishmaydi; tegishli manbadan ruxsatli ma’lumot kerak."},
            {"Natija": "Qayta tekshiruv", "Mazmuni": "Yangi ma’lumot kelgach qoidalar va kontekst qayta ko‘riladi."},
            {"Natija": "Ko‘rib chiqishni davom ettirish", "Mazmuni": "Dalillar yoki qarshi dalillar hali yetarli emas."},
            {"Natija": "Case'ni asos bilan yopish", "Mazmuni": "Tekshiruv yakunlangan; sabab va dalillar auditda qayd etilishi kerak."},
        ],
        use_container_width=True, hide_index=True,
    )
    st.warning("Bu yerda hech qanday haqiqiy qaror qabul qilinmaydi. Reviewer autentifikatsiyasi, vakolat nazorati va doimiy audit ushbu ommaviy namoyishga ulanmagan.")

elif page == "Qatlamlararo xarita":
    st.markdown("## Qatlamlararo bog‘liqlik va jarayon xaritasi")
    st.caption("Qatlamlar bir xil hodisa va Case kontekstida ishlashi ko‘zda tutilgan. Quyidagi ko‘rinish jarayon bosqichlari bilan qatlamlarning mazmuniy aloqasini ko‘rsatadi.")
    st.markdown('<div class="warning-note"><b>Metodik ehtiyot:</b> bu jadval texnik API yoki tasdiqlangan LINK-ID ro‘yxati emas. 16 qatlamlararo aloqa matritsasidagi takliflar alohida manba tekshiruvi va loyiha egasi/ekspert tasdig‘ini talab qiladi.</div>', unsafe_allow_html=True)
    st.dataframe(
        [{"Jarayon bosqichi": x[1], "Mazmuniy qatlam qamrovi": x[2], "Izoh": x[3]} for x in PIPELINE],
        use_container_width=True, hide_index=True,
    )
    st.markdown("### Aloqa rasmiylashtirilishidan oldin nimalar kerak?")
    st.markdown("- Manba qatlam → maqsad qatlam yo‘nalishi.")
    st.markdown("- Uzatiladigan obyekt va nima uchun kerakligi.")
    st.markdown("- Manba bandi, REQ-ID va TEST-ID.")
    st.markdown("- Kutilgan va amaldagi natija hamda dalil.")
    st.markdown("- Tasdiqlash holati va texnik kontrakt.")
    st.info("Manba bilan qo‘llab-quvvatlangan aloqa taklifi ham mustaqil servis, API yoki ishlab turgan integratsiya mavjudligini isbotlamaydi.")

elif page == "Sintetik sinovlar":
    st.markdown("## Sintetik sinov ssenariylari")
    st.caption("Bu namunalar jarayon mantiqini tushuntirish uchun. Ular real bankdagi aniqlik yoki samaradorlik ko‘rsatkichi emas.")
    chosen = st.selectbox("Ssenariyni tanlang", list(EVENTS.keys()), format_func=lambda x: f"{x} · {EVENTS[x]['title']}")
    event = EVENTS[chosen]
    render_event_detail(chosen)
    st.markdown("### Ushbu sinovda tekshiriladigan savollar")
    test_questions = [
        "Ssenariy nomi tasniflash natijasiga yashirin ta’sir qilyaptimi?",
        "Majburiy maydon yetishmasa tizim DATA_REVIEW holatini ko‘rsatyaptimi?",
        "Yakka indikator Case ochmasdan qayta tekshiruvga yo‘naltirilyaptimi?",
        "Rozilik doiralari alohida ko‘rsatilayaptimi?",
        "Signal aybdorlik hukmi yoki avtomatik bloklash buyrug‘i sifatida talqin qilinmayaptimi?",
        "Human Review uchun dalil, qarshi dalil va noma’lum savollar ko‘rsatilayaptimi?",
    ]
    for question in test_questions:
        st.markdown("• " + question)
    st.warning("Ushbu sahifa interaktiv test bajaruvchi laboratoriya emas. 400 hodisali v3 laboratoriyasi v4 yagona jarayoniga hali integratsiya qilinmagan.")

elif page == "Atamalar va cheklovlar":
    st.markdown("## Atamalar — sodda va texnik ma’nosi")
    glossary = [
        ("Hodisa / Event", "Tahlilga kelgan bitta operatsiya yoki tizim hodisasi haqidagi yozuv."),
        ("Signal", "Tekshirishga sabab bo‘ladigan indikator; aybdorlik isboti emas."),
        ("Dalil / Evidence", "Manbasi, vaqti va cheklovi ko‘rsatilgan tasdiqlovchi yoki inkor etuvchi material."),
        ("Qarshi dalil", "Dastlabki taxminni zaiflashtirishi yoki boshqa izohni ko‘rsatishi mumkin bo‘lgan ma’lumot."),
        ("Noma’lum / Unknown", "Hali tasdiqlanmagan yoki yetishmayotgan muhim fakt."),
        ("Ziddiyat / Contradiction", "Ikki manba yoki maydondagi qiymatlar bir-biriga mos kelmasligi."),
        ("Case", "Tekshiruv uchun bog‘langan hodisa, signal, dalil va savollar jamlanmasi."),
        ("Human Review", "Vakolatli insonning dalillarni ko‘rib chiqishi va asoslangan harakatni qayd etishi."),
        ("Consent scope", "Qurilma, hisob va aynan shu o‘tkazma bo‘yicha rozilik chegaralarini alohida ko‘rish."),
        ("False Positive (FP)", "Aslida muammo bo‘lmagan holatni shubhali deb belgilash."),
        ("False Negative (FN)", "Muhim xavfli holatni aniqlamay o‘tkazib yuborish."),
        ("Provenance", "Ma’lumotning kelib chiqish tarixi: manba, vaqt va olish usuli."),
        ("Read-only", "Ko‘rish mumkin, lekin ommaviy foydalanuvchi ma’lumot yoki sozlamani o‘zgartira olmaydi."),
    ]
    st.dataframe([{"Atama": a, "Sodda izoh": b} for a, b in glossary], use_container_width=True, hide_index=True)
    st.markdown("### Prototip nimalarni qilmaydi?")
    st.markdown("- Karta, hisob yoki tranzaksiyani avtomatik bloklamaydi.")
    st.markdown("- Signalni aybdorlik isboti deb ko‘rsatmaydi.")
    st.markdown("- Banklarning barcha mijoz ma’lumotlariga erkin kira olmaydi.")
    st.markdown("- Haqiqiy bank API, production SSO/RBAC yoki doimiy audit mavjud deb da’vo qilmaydi.")
    st.markdown("- Sintetik sinov natijasini real firibgarlik aniqligi deb ko‘rsatmaydi.")
    st.markdown("### Hozirgi holatning qisqa reyestri")
    st.dataframe(
        [
            {"Qism": "Ochiq interfeys", "Holat": "Ushbu branchda ko‘rish uchun ishlab chiqilmoqda"},
            {"Qism": "16 qatlam", "Holat": "Manba asosidagi talablar katalogi; ekspert tasdig‘i kutilmoqda"},
            {"Qism": "Case va Human Review", "Holat": "Sintetik namoyish; haqiqiy vakolat va doimiy saqlash yo‘q"},
            {"Qism": "Qatlamlararo aloqa", "Holat": "Jarayon darajasidagi ko‘rinish; rasmiy LINK-ID emas"},
            {"Qism": "Bank integratsiyasi", "Holat": "Mavjud emas"},
            {"Qism": "AI moduli", "Holat": "Gemini + ichki candidate bilimlar; Google Search ixtiyoriy; yangi kalit/Secrets talab qilinadi"},
            {"Qism": "Production tayyorligi", "Holat": "Tasdiqlanmagan"},
        ],
        use_container_width=True, hide_index=True,
    )

st.markdown(
    '<div class="footer">FINZANJIR · v4 yagona ish jarayoni prototipi · faqat sintetik namoyish · '
    'ommaviy ko‘rish rejimi · real bank integratsiyasi emas</div>',
    unsafe_allow_html=True,
)
