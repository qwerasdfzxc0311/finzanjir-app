# FINZANJIR v4 — Yagona ish jarayoni va AI yordamchisi

**Branch:** finzanjir-v4-unified-workflow-uz  
**Streamlit main file:** finzanjir_v4/app.py

## 1. Ochiq interfeys

v4 ommaviy interfeysi mobilga mos va ko‘rish rejimida. Bo‘lim tanlash, sintetik misol tanlash va AI savol-javobi loyiha ma’lumotlari yoki Case holatini o‘zgartirmaydi.

Asosiy bo‘limlar:
1. Bosh sahifa — maqsad, chegaralar va umumiy jarayon.
2. Boshqaruv paneli — v4 dagi to‘rtta sintetik namuna.
3. Sun’iy bank laboratoriyasi — v3 dagi alohida 4 manbali/400 ssenariyli laboratoriya haqida ma’lumot; v4 ga ulanmagan.
4. Yagona ish jarayoni — hodisadan ma’lumot sifati, signal/dalil, Case mezonlari va Human Reviewgacha.
5. Signallar reyestri — indikator, dalil, qarshi dalil va noma’lum jihatlar.
6. 16 qatlam — maqsad, savol, kirish/chiqish va cheklovlar.
7. FINZANJIR AI — ichki candidate bilimlar + Gemini; Google Search ixtiyoriy.
8. Case markazi — sintetik Case va rozilik doirasi.
9. Human Review — ko‘rib chiqish savollari va mumkin bo‘lgan natijalar; qaror kiritish yo‘q.
10. Banklararo tahlil — sintetik atribut mosligi va ehtiyot chegaralari.
11. KPI dashboard — sintetik jarayon sonlari; aniqlik yoki FP/FN natijasi emas.
12. Fuqaro uchun tushuntirish — konsepsiyani sodda tilda izohlash.
13. Audit jurnali — ko‘rgazmali vaqt chizig‘i; doimiy audit ombori emas.
14. Qatlamlararo xarita — mazmuniy jarayon xaritasi; rasmiy LINK-ID/API emas.
15. Sintetik sinovlar — tushuntiruvchi ssenariylar.
16. Atamalar va cheklovlar — oddiy va texnik izohlar.

## 2. FINZANJIR AI arxitekturasi

Savol → Uzbek Latin/Cyrillic normalizatsiyasi → ichki bilim qidiruvi → manba/versiya/maqom → Gemini javobi → ixtiyoriy Google Search grounding → manbalarni ko‘rsatish.

- Python SDK: google-genai (Google tavsiya qilgan rasmiy GenAI SDK).
- Default model: gemini-3.8-flash.
- Google Search grounding foydalanuvchi checkbox orqali alohida yoqiladi.
- Grounding URL manbalari Gemini API javobidan olinadi.
- Gemini API kaliti faqat Streamlit Secrets orqali o‘qiladi.
- AI Case, Human Review yoki bilimlar bazasini o‘zgartirmaydi.
- Savollar v4 ilova ma’lumotlar bazasiga yozilmaydi.
- AI javobi rasmiy ekspert yoki bank qarori emas.

### Google Search va xarajat

Google Search grounding qo‘shimcha xarajat keltirishi mumkin. Gemini bir so‘rov uchun bir nechta qidiruv query bajarishi ehtimoli bor. Gemini Interactions API chaqiruvida store=false ishlatiladi, shuning uchun server-side Interaction tarixi saqlash o‘chiriladi; bu Google providerning so‘rovni qayta ishlash shartlarini bekor qilmaydi. Google AI Studio/Cloud’da quota, API key restriction va billing alerts sozlang.

Brauzer sessiyasidagi 5 ta so‘rov cheklovi yumshoq UI nazorati xolos; u billing cap yoki kuchli rate limit emas. Public release oldidan server-side rate limiting va abuse protection alohida kerak.

### Streamlit Secrets

Streamlit Cloud → App settings → Secrets:

    [gemini]
    enabled = true
    api_key = "YANGI_GEMINI_API_KEY"
    model = "gemini-3.8-flash"
    max_requests_per_session = 5

**Xavfsizlik:** oldin chatga yuborilgan Gemini kaliti oshkor bo‘lgan deb hisoblanadi va bekor qilinishi kerak. Yangi kalitni faqat Streamlit Secrets ichiga kiriting. GitHub, commit, README yoki chatga hech qachon yozmang. Repository .gitignore fayli .streamlit/secrets.toml ni chiqarib tashlaydi.

### Local run

    pip install -r requirements.txt
    streamlit run finzanjir_v4/app.py

Local test uchun .streamlit/secrets.toml faylini faqat o‘z qurilmangizda yarating; uni GitHub’ga yubormang.

## 3. Knowledge Base holati

Joriy v4 knowledge_uz.json ichida 137 ta yozuv:
- 33 legacy v3 candidate;
- 16 qatlam katalogi;
- 22 repository konsepsiya yozuvi;
- 42 AI arxitekturasi, AI baholash va V317 auditidan tanlangan yozuv;
- 24 ta 25 bobli integratsiyalashgan kitobning 1–24-boblari bo‘yicha sahifaga bog‘langan qisqa xulosa.

Barcha yozuvlar candidate_not_authoritative. Hozircha authoritative/approved yozuv yo‘q.

Har bir yozuv source_id, source_version, source_section, source_path va approval maqomiga ega. knowledge_manifest.json manbalar va ma’lum bo‘shliqlarni ko‘rsatadi.

**Bu to‘liq FINZANJIR arxivi emas.** To‘liq V14, V8, 16 qatlam chuqur tushuntirishi va asl FINZANJIR_AI.zip v0.6.0 korpusi hali to‘liq import qilinmagan. V317 auditida qayd etilgan 4 671 yozuv ham to‘liq ko‘chirilmagan. Shuning uchun AI loyiha haqidagi barcha savollarga javob bera oladi deb va’da qilinmaydi.

Qidiruv hozir lexical/synonym-based; to‘liq embedding/vector semantic search emas. “16 qatlam” savolida barcha 16 qatlam yozuvi kontekstga beriladi. Qidiruv balli faktik ishonchlilik emas.

## 4. Tavily bilan bog‘liq qaror

Tavily v4 AI modulida ishlatilmaydi va v4 app.py undan import qilmaydi. v3 tarixiy app.py va internet_research.py fayllari eski branch/mexanizmni saqlash uchun repository ichida qolgan; ular v4 ishga tushish yo‘liga ulanmagan. Yangi v4 AI yo‘li Gemini + optional Google Search + FINZANJIR knowledge base.

## 5. Halol holat va cheklovlar

- Barcha v4 hodisalari sintetik namuna.
- 16 qatlam katalogi talab mazmuni; barcha qatlamlar implementatsiya qilingan yoki ekspert tasdiqlagan degani emas.
- Case va Human Review ko‘rgazmali; haqiqiy reviewer autentifikatsiyasi, SSO/RBAC va doimiy audit ulanmagan.
- 400 hodisali v3 laboratoriyasi v4 yagona jarayoniga integratsiya qilinmagan.
- Gemini/Google Search kod yo‘li yozilgan, ammo yangi kalit bilan Streamlit Cloud’da jonli tekshiruv hali bajarilishi kerak.
- Gemini API ishlashi internetga va Google xizmatiga bog‘liq; bu offline AI emas.
- Haqiqiy bank API, mijoz ma’lumotlari, production monitoring yoki production tayyorligi mavjud deb da’vo qilinmaydi.
- FINZANJIR karta, hisob yoki tranzaksiyani avtomatik bloklamaydi.
- Sintetik sinovlar real firibgarlik aniqligi, precision, recall, FP/FN yoki bank samaradorligini isbotlamaydi.

## 6. Testlar

GitHub Actions:
- Python compile;
- barcha public sahifalar uchun Streamlit smoke test;
- AI retrieval va source provenance testlari;
- 16 qatlamning hammasini retrieval qilish;
- Latin/Cyrillic qidiruv;
- maxfiy karta raqamiga o‘xshash inputni rad etish;
- grounding citation filtering;
- public appda persistent Case/business-data write yo‘llari yo‘qligi;
- v4 AI modulida Tavily yo‘qligi.

CI PASS — source/unit/smoke test dalili. Bu jonli Gemini API, Google Search, production xavfsizligi yoki AI javoblarining universal to‘g‘riligini tasdiqlamaydi.

Qo‘shimcha hujjat: AI_ASSISTANT_SECURITY_UZ.md.

## 7. Branch va tarixni saqlash

- Eski main, concept-aligned-v1 va finzanjir-v3-synthetic-ai-uz branchlari o‘zgartirilmaydi.
- Yangi ish finzanjir-v4-unified-workflow-uz branchida.
- Ommaviy interfeys ko‘rish va savol-javob uchun; Case/Human Review biznes yozuvlari tahrirlanmaydi.
