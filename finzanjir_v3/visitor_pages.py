import streamlit as st
import visitor_analytics as visitors

def render_feedback():
    st.subheader("FINZANJIR haqida fikringiz")
    st.info("Shakl ixtiyoriy. Anonim fikr qoldirishingiz mumkin; ism, telefon yoki email majburiy emas.")
    st.warning("MAXFIYLIK: javoblaringizni faqat FINZANJIR loyiha muallifi ko'ra oladi. Boshqa tashrifchilar sizning javoblaringizni ko'ra olmaydi; siz ham boshqalarning javoblarini ko'rmaysiz.")
    st.caption("Ilova sahifa ko'rishlari, taxminiy qurilma/OS/brauzer turini va oxirgi faollikni qayd etishi mumkin. Model har doim aniqlanmaydi. Kod nusxalanganini ishonchli aniqlash imkoni yo'q. IP, GPS va yashirin fingerprint yig'ilmaydi.")
    with st.form("finzanjir-visitor-feedback", clear_on_submit=True):
        data={}
        data["usefulness"]=st.text_area("1. Loyihaning qaysi jihati foydali yoki qiziq tuyuldi?")
        data["missing"]=st.text_area("2. Sizningcha, loyihada nimalar yetishmayapti?")
        data["improve"]=st.text_area("3. Uni rivojlantirish uchun nimani birinchi yaxshilagan bo'lardingiz?")
        data["feature"]=st.text_area("4. Qaysi yangi funksiya yoki imkoniyatni tavsiya qilasiz?")
        data["concerns"]=st.text_area("5. Tushunarsiz yoki xavotir uyg'otgan joylari bormi?")
        data["collaboration"]=st.text_area("6. Hamkorlik yoki batafsil muhokama taklifingiz bormi?")
        st.markdown("**Aloqa ma'lumotlari — ixtiyoriy**")
        data["name"]=st.text_input("Ism-familiya (ixtiyoriy)")
        data["contact"]=st.text_input("Telefon yoki email (ixtiyoriy)")
        data["extra"]=st.text_area("Qo'shimcha fikr (ixtiyoriy)")
        consent=st.checkbox("Javobimni faqat FINZANJIR muallifi ko'rishiga roziman.")
        submitted=st.form_submit_button("Maxfiy fikrni yuborish",type="primary")
        if submitted:
            if not consent: st.error("Yuborish uchun muallif ko'rishini tasdiqlang.")
            else:
                try:
                    visitors.save_feedback(data)
                    st.success("Fikringiz qabul qilindi. Uni faqat loyiha muallifi ko'ra oladi.")
                except ValueError as exc: st.error(str(exc))

def render_admin():
    st.subheader("Muallif uchun maxfiy tashrifchilar paneli")
    st.warning("Bu sahifa faqat muallif uchun. Streamlit Secrets ichida visitor_analytics.admin_password_hash va visitor_analytics.session_hmac_secret sozlanishi shart.")
    try:
        admin_hash=st.secrets["visitor_analytics"]["admin_password_hash"]
        analytics_secret=st.secrets["visitor_analytics"]["session_hmac_secret"]
    except Exception: admin_hash,analytics_secret="",""
    if not admin_hash or not analytics_secret:
        st.error("Muallif paneli o'chirilgan: maxfiy sozlamalar topilmadi. Standart parol yo'q.")
        return
    if not st.session_state.get("visitor_admin_authenticated",False):
        with st.form("visitor-admin-login"):
            password=st.text_input("Muallif paroli",type="password")
            login=st.form_submit_button("Kirish")
            if login:
                if visitors.verify_admin_password(password,admin_hash):
                    st.session_state["visitor_admin_authenticated"]=True
                    st.rerun()
                else: st.error("Parol noto'g'ri.")
        return
    if st.button("Chiqish",key="visitor-admin-logout"):
        st.session_state["visitor_admin_authenticated"]=False
        st.rerun()
    snap=visitors.admin_snapshot()
    a,b,c=st.columns(3)
    a.metric("Psevdonim sessiyalar",snap["visitors"])
    b.metric("Sahifa ko'rishlar",snap["page_views"])
    c.metric("Yuborilgan fikrlar",snap["feedback_count"])
    st.caption("Sessiyalar soni noyob odamlar soni emas. Chiqish vaqti aniq aniqlanmaydi; oxirgi faollik ko'rsatiladi.")
    st.subheader("Qurilma, tizim va brauzer — taxminiy")
    if snap["devices"]: st.dataframe(snap["devices"],use_container_width=True,hide_index=True)
    st.subheader("Ko'p ko'rilgan sahifalar")
    if snap["popular_pages"]: st.dataframe(snap["popular_pages"],use_container_width=True,hide_index=True)
    st.subheader("Oxirgi tashrif sessiyalari")
    if snap["recent_visits"]: st.dataframe(snap["recent_visits"],use_container_width=True,hide_index=True)
    st.subheader("Tashrifchilarning maxfiy fikrlari")
    st.caption("Javoblar ommaviy sahifaga chiqarilmaydi; faqat muallif panelida ko'rinadi.")
    for item in snap["feedback"]:
        with st.expander("Fikr #"+str(item["id"])+" · "+item["created_at"]):
            for label,key in [("Foydali jihati","usefulness"),("Yetishmayotgani","missing"),("Yaxshilash taklifi","improve"),("Yangi funksiya","feature"),("Xavotirlar","concerns"),("Hamkorlik","collaboration"),("Ism-familiya","name"),("Aloqa","contact"),("Qo'shimcha","extra")]:
                if item.get(key): st.markdown("**"+label+":** "+item[key])
