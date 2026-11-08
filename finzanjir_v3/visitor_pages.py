from __future__ import annotations
import time
import streamlit as st
import visitor_analytics as visitors

def render_feedback():
    st.subheader("FINZANJIR haqida fikringiz")
    st.write("Fikringiz loyihani yaxshilashga yordam beradi. Savollarning barchasiga javob berish shart emas.")
    with st.container():
        st.markdown("**🔒 Maxfiylik qanday ishlaydi?**")
        st.write("Yuborgan javoblaringiz ommaviy sahifada ko‘rsatilmaydi. Boshqa tashrifchilar ularni ko‘ra olmaydi. Javoblarni faqat muallif himoyalangan panelga parol bilan kirgandan keyin ko‘radi.")
        st.caption("Ilova sahifa ko‘rishlari va taxminiy qurilma/brauzer turini qayd etishi mumkin. IP-manzil, GPS yoki yashirin brauzer fingerprinti yig‘ilmaydi. Qurilma aniqligi kafolatlanmaydi.")
    with st.form("finzanjir-visitor-feedback", clear_on_submit=True):
        st.markdown("#### 1. Loyiha haqidagi fikringiz")
        left, right = st.columns(2)
        with left:
            usefulness = st.text_area("Nimasi foydali yoki qiziq tuyuldi?", max_chars=visitors.MAX_TEXT,
                                      help="Masalan: qaysi funksiya yoki g‘oya sizga ma’qul bo‘ldi?")
            missing = st.text_area("Nimalar yetishmayapti?", max_chars=visitors.MAX_TEXT)
            improve = st.text_area("Birinchi navbatda nimani yaxshilash kerak?", max_chars=visitors.MAX_TEXT)
        with right:
            feature = st.text_area("Qanday yangi imkoniyat qo‘shishni tavsiya qilasiz?", max_chars=visitors.MAX_TEXT)
            concerns = st.text_area("Tushunarsiz yoki xavotirli joylari bormi?", max_chars=visitors.MAX_TEXT)
            collaboration = st.text_area("Hamkorlik yoki muhokama taklifingiz bormi?", max_chars=visitors.MAX_TEXT)
        st.divider()
        st.markdown("#### 2. Aloqa ma’lumotlari (ixtiyoriy)")
        name = st.text_input("Ism yoki tashkilot nomi", max_chars=200)
        contact = st.text_input("Email yoki telefon", max_chars=300,
                                help="Javob olishni istasangizgina kiriting. Majburiy emas.")
        extra = st.text_area("Qo‘shimcha izoh", max_chars=visitors.MAX_TEXT)
        consent = st.checkbox("Yozgan fikrlarim faqat loyiha muallifiga ko‘rinishini tushundim.")
        submitted = st.form_submit_button("Fikrni maxfiy yuborish", type="primary", use_container_width=True)
        if submitted:
            data = {"usefulness": usefulness, "missing": missing, "improve": improve,
                    "feature": feature, "concerns": concerns, "collaboration": collaboration,
                    "name": name, "contact": contact, "extra": extra}
            if not consent:
                st.error("Davom etish uchun maxfiylik shartini tasdiqlang.")
            else:
                try:
                    visitors.save_feedback(data)
                    st.success("Rahmat! Fikringiz qabul qilindi va ommaviy sahifaga chiqarilmadi.")
                except ValueError as exc:
                    st.error(str(exc))
    with st.expander("Nimalarni yozmaslik kerak?"):
        st.write("Karta raqami, PIN, CVV, OTP-kod, parol, pasport ma’lumoti yoki boshqa maxfiy moliyaviy/shaxsiy ma’lumotlarni yubormang.")

def render_admin():
    st.subheader("Muallif uchun yopiq boshqaruv paneli")
    st.caption("Bu bo‘lim ommaviy menyuda ko‘rsatilmaydi. Faqat muallif paroli bilan ochiladi.")
    try:
        config = st.secrets["visitor_analytics"]
        admin_hash = config["admin_password_hash"]
        analytics_secret = config["session_hmac_secret"]
    except Exception:
        admin_hash, analytics_secret = "", ""
    if not admin_hash or not analytics_secret or len(str(analytics_secret)) < 32:
        st.error("Panel hozircha yopiq: Streamlit Secrets ichida to‘g‘ri maxfiy sozlamalar yo‘q. Standart parol mavjud emas.")
        return

    session_id = st.session_state.get("visitor_session_id", "")
    auth_time = st.session_state.get("visitor_admin_authenticated_at")
    now = time.time()
    if auth_time and now - float(auth_time) > visitors.ADMIN_SESSION_TTL_SECONDS:
        st.session_state.pop("visitor_admin_authenticated_at", None)
        st.session_state.pop("visitor_admin_authenticated", None)
        st.warning("Xavfsizlik uchun sessiya muddati tugadi. Qayta kiring.")
    authenticated = bool(st.session_state.get("visitor_admin_authenticated")) and bool(st.session_state.get("visitor_admin_authenticated_at"))
    if authenticated:
        st.session_state["visitor_admin_authenticated_at"] = now
        if st.button("Xavfsiz chiqish", key="visitor-admin-logout"):
            st.session_state.pop("visitor_admin_authenticated", None)
            st.session_state.pop("visitor_admin_authenticated_at", None)
            st.rerun()
    else:
        status = visitors.admin_login_status(session_id, analytics_secret)
        if not status["allowed"]:
            st.error("Urinishlar vaqtincha cheklangan. " + str(status["retry_after"]) + " soniyadan keyin qayta urinib ko‘ring.")
            return
        st.info("Kirish faqat muallif uchun. Parolni hech kimga yubormang.")
        with st.form("visitor-admin-login"):
            password = st.text_input("Muallif paroli", type="password", max_chars=1024)
            login = st.form_submit_button("Himoyalangan panelga kirish", type="primary")
            if login:
                if visitors.verify_admin_password(password, admin_hash):
                    visitors.record_admin_login_attempt(session_id, analytics_secret, True)
                    st.session_state["visitor_admin_authenticated"] = True
                    st.session_state["visitor_admin_authenticated_at"] = time.time()
                    st.rerun()
                else:
                    visitors.record_admin_login_attempt(session_id, analytics_secret, False)
                    remaining = visitors.admin_login_status(session_id, analytics_secret)
                    if not remaining["allowed"]:
                        st.error("5 ta noto‘g‘ri urinishdan so‘ng kirish 15 daqiqaga cheklab qo‘yildi.")
                    else:
                        st.error("Parol noto‘g‘ri. Qolgan urinishlar: " + str(remaining["attempts_left"]))
        return

    snap = visitors.admin_snapshot()
    st.markdown("### Umumiy ko‘rsatkichlar")
    a, b, c = st.columns(3)
    a.metric("Psevdonim sessiyalar", snap["visitors"], help="Bu noyob odamlar soni emas; brauzer sessiyalari taxminiy hisoblanadi.")
    b.metric("Sahifa ko‘rishlar", snap["page_views"])
    c.metric("Yuborilgan fikrlar", snap["feedback_count"])
    st.caption("IP yoki GPS saqlanmaydi. Chiqish vaqti aniq aniqlanmaydi; oxirgi faollik ko‘rsatiladi.")
    tab_overview, tab_feedback = st.tabs(["Tashrif statistikasi", "Maxfiy fikrlar"])
    with tab_overview:
        st.markdown("#### Qurilma va brauzerlar")
        if snap["devices"]:
            st.dataframe(snap["devices"], use_container_width=True, hide_index=True)
        else:
            st.info("Hozircha statistika yig‘ilmagan.")
        st.markdown("#### Ko‘p ko‘rilgan bo‘limlar")
        if snap["popular_pages"]:
            st.dataframe(snap["popular_pages"], use_container_width=True, hide_index=True)
        st.markdown("#### Oxirgi sessiyalar")
        if snap["recent_visits"]:
            st.dataframe(snap["recent_visits"], use_container_width=True, hide_index=True)
    with tab_feedback:
        st.write("Bu fikrlar faqat muallif panelida ko‘rinadi. Ular ommaviy sahifaga chiqarilmaydi.")
        search = st.text_input("Fikrlar ichidan qidirish", placeholder="Masalan: maxfiylik, taklif, xato…")
        items = snap["feedback"]
        if search.strip():
            needle = search.casefold()
            items = [item for item in items if needle in " ".join(str(item.get(k, "")) for k in
                     ("usefulness","missing","improve","feature","concerns","collaboration","name","contact","extra")).casefold()]
        if not items:
            st.info("Mos fikr topilmadi yoki hali fikr kelmagan.")
        for item in items:
            with st.expander("Fikr #" + str(item["id"]) + " · " + item["created_at"]):
                for label, key in [("Foydali jihati","usefulness"),("Yetishmayotgani","missing"),
                                   ("Yaxshilash taklifi","improve"),("Yangi imkoniyat","feature"),
                                   ("Xavotirlar","concerns"),("Hamkorlik","collaboration"),
                                   ("Ism / tashkilot","name"),("Aloqa","contact"),("Qo‘shimcha","extra")]:
                    value = item.get(key, "")
                    if value:
                        st.markdown("**" + label + "**")
                        st.text(value)
