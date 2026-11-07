from __future__ import annotations
import sys, json
from pathlib import Path
import streamlit as st
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"finzanjir_v2"))
sys.path.insert(0,str(HERE))
import laboratory as lab
import offline_ai

st.set_page_config(page_title="FINZANJIR v3 | Laboratoriya",page_icon="🛡️",layout="wide")
lab.init_lab()
st.markdown("""
<style>
.stApp{background:#0b1220;color:#e8edf5}
[data-testid="stSidebar"]{background:#111b2d}
div[data-testid="stMetric"]{background:#142137;border:1px solid #293b57;padding:12px;border-radius:10px}
.panel{background:#142137;border:1px solid #293b57;border-radius:12px;padding:14px}
</style>
""",unsafe_allow_html=True)
st.title("🛡️ FINZANJIR")
st.caption("v3 development branch • Uzbek-first • offline knowledge retrieval • synthetic bank lab")
st.warning("Bu faqat sintetik sinov muhiti. Haqiqiy bankka ulanmagan, haqiqiy pul yoki mijoz ma'lumotini olmaydi. Signal yoki Case aybdorlik isboti emas. Avtomatik bloklash mavjud emas.")
page=st.sidebar.radio("Ish bo'limlari",["Boshqaruv paneli","Sun'iy bank laboratoriyasi","Hodisalar va Case","FINZANJIR AI (o'zbekcha)","AI sinovlari","Arxitektura va chegaralar"])
st.sidebar.divider()
st.sidebar.caption("Tashqi AI API ishlatilmaydi. AI hozircha dalilga asoslangan lokal qidiruv; generativ LLM emas.")

if page=="Boshqaruv paneli":
    snap=lab.snapshot(); meta=snap["meta"]; counts=snap["counts"]
    st.subheader("Umumiy holat")
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
    st.subheader("Avtomatik bank ma'lumotlari oqimi")
    st.write("4 ta sun'iy bankdan jami 400 ta oldindan belgilangan sintetik holat keladi. Start bosilganda fon jarayoni hodisalarni avtomatik qayta ishlaydi.")
    snap=lab.snapshot(); meta=snap["meta"]; counts=snap["counts"]
    a,b,c,d=st.columns(4)
    a.metric("Jami",snap["total"]); b.metric("Qayta ishlangan",counts.get("PROCESSED",0))
    c.metric("Navbat",counts.get("QUEUED",0)); d.metric("Holat",meta.get("run_state","IDLE"))
    progress=(counts.get("PROCESSED",0)/max(1,snap["total"]))
    st.progress(min(1.0,progress),text=f"{counts.get('PROCESSED',0)} / {snap['total']} hodisa")
    x,y,z=st.columns(3)
    if x.button("▶ START — boshlash",type="primary",use_container_width=True):
        lab.start_run(resume=False); st.rerun()
    if y.button("Ⅱ PAUSE — vaqtincha to'xtatish",use_container_width=True):
        lab.pause_run(); st.rerun()
    if z.button("■ STOP — to'liq to'xtatish",use_container_width=True):
        lab.stop_run(); st.rerun()
    x,y,z=st.columns(3)
    if x.button("↻ RESUME — davom ettirish",use_container_width=True):
        lab.start_run(resume=True); st.rerun()
    if y.button("Yangilash",use_container_width=True): st.rerun()
    confirm=st.checkbox("Navbat va natijalarni o'chirishga roziman")
    if z.button("RESET — yangi sikl",disabled=not confirm,use_container_width=True):
        lab.reset_run(confirmed=confirm); st.rerun()
    st.caption("PAUSE/STOP navbatda qolgan hodisalarni o'chirmaydi. RESUME ularni davom ettiradi. RESET alohida tasdiq talab qiladi.")
    if meta.get("last_error"): st.error("Jarayon xatosi: "+meta["last_error"])
    st.subheader("Banklar bo'yicha qabul holati")
    if snap["banks"]: st.dataframe(snap["banks"],use_container_width=True,hide_index=True)
    st.subheader("Jarayon auditi")
    if snap["audit"]: st.dataframe(snap["audit"],use_container_width=True,hide_index=True)

elif page=="Hodisalar va Case":
    snap=lab.snapshot()
    st.subheader("Qayta ishlangan hodisalar")
    rows=snap["recent"]
    if rows:
        display=[]
        for r in rows:
            result={}
            try: result=json.loads(r["result"]) if r["result"] else {}
            except Exception: pass
            display.append({"Hodisa":r["event_id"],"Bank":r["bank_id"],"Ssenariy":r["scenario"],"Kutilgan":r["expected"],"Amaldagi":result.get("outcome","—"),"Holat":r["state"]})
        st.dataframe(display,use_container_width=True,hide_index=True)
    else: st.info("Hali hodisa kelmagan. Laboratoriyada START bosing.")
    st.caption("Hodisa tafsilotlari sintetik; natijalar prototip qoidalari bilan hisoblangan.")

elif page=="FINZANJIR AI (o'zbekcha)":
    st.subheader("Lokal bilim yordamchisi")
    st.info("Internetdagi AI xizmatiga so'rov yuborilmaydi. Bu bosqichda matn generatsiyasi emas, V317 bilim kartalaridan o'zbekcha dalil qidirish va parchalarni ko'rsatish ishlaydi.")
    q=st.text_area("Savolingizni o'zbek tilida yozing",placeholder="Masalan: Shubhali signal mijozni aybdor qiladimi?")
    if st.button("Bilimdan qidirish",type="primary",disabled=not q.strip()):
        result=offline_ai.answer(q)
        if result["status"]=="NO_SUFFICIENT_EVIDENCE": st.warning(result["answer"])
        else: st.success(result["answer"])
        with st.expander("Topilgan dalillar va ularning maqomi",expanded=True):
            for item in result["evidence"]:
                st.markdown(f"**{item['id']}** · {item['approval']} · moslik {item['coverage']}")
                st.write(item["text"])
    st.caption("Bilim yozuvlari candidate maqomida. AI ularni rasmiy tasdiqlangan qoida sifatida ko'rsatmaydi va Authoritative KBni o'zgartirmaydi.")

elif page=="AI sinovlari":
    st.subheader("O'zbekcha AI regression sinovlari")
    results=offline_ai.self_test()
    passed=sum(1 for r in results if r["passed"])
    a,b=st.columns(2); a.metric("Sinovlar",len(results)); b.metric("O'tdi",passed)
    st.dataframe(results,use_container_width=True,hide_index=True)
    if passed==len(results): st.success("Barcha smoke-testlar o'tdi. Bu mazmuniy ekspert validatsiyasi emas.")
    else: st.error("Kamida bitta sinov o'tmadi. Javoblarni kengaytirishdan oldin retrieval qoidalarini tuzatish kerak.")

elif page=="Arxitektura va chegaralar":
    st.subheader("Versiya va ishlash chegaralari")
    st.markdown("""
    **Yangi branch:** finzanjir-v3-synthetic-ai-uz

    - Sun'iy bank laboratoriyasi: 400 ta deterministik sintetik hodisa, 4 manba.
    - Boshqaruv: START, PAUSE, STOP, RESUME, RESET.
    - AI: o'zbekcha offline evidence retrieval; tashqi model/API yo'q.
    - Bilimlar: V317 ZIPdan ajratilgan candidate yozuvlar; tasdiqlangan bilim bilan aralashtirilmaydi.
    - Inson ko'rigi: shubhali holatni Case nomzodiga yo'naltirish tamoyili.
    - L11: favqulodda to'xtatish, navbatni saqlash va tiklash bo'yicha laboratoriya boshqaruvlari.

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
