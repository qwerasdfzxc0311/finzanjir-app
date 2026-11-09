# FINZANJIR v4 — AI arxitekturasi va xavfsizlik modeli

Holat: v4 branch uchun implementatsiya tavsifi va xavfsizlik nazorati. Bu hujjat Gemini integratsiyasi production darajasida tekshirilganini bildirmaydi.

## 1. Maqsad va aniq chegara

FINZANJIR AI — loyiha bilimini topish, tushuntirish va kerak bo‘lsa tashqi manbani tekshirishga yordam beradigan alohida yordamchi qatlam. U FINZANJIRning o‘zi emas; Risk Engine, Case Management yoki Human Review vakolatini egallamaydi.

O‘zgarmas chegaralar:
- Signal yoki Case aybdorlik hukmi emas.
- FINZANJIR karta, hisob yoki tranzaksiyani avtomatik bloklamaydi.
- AI Case ochmaydi, Case holatini o‘zgartirmaydi, Human Review qarorini yozmaydi va bankka buyruq yubormaydi.
- Tashqi manba FINZANJIRning rasmiy bilimiga avtomatik qo‘shilmaydi.
- Yetarli dalil bo‘lmasa, AI taxminni fakt sifatida bermaydi.

## 2. Joriy v4 oqimi

    Savol
      -> kirish tekshiruvi (bo‘shlik, uzunlik, karta raqamiga o‘xshash ma’lumot)
      -> o‘zbek lotin/kirill normalizatsiyasi va synonym matching
      -> FINZANJIR knowledge_uz.json ichidan manbali yozuvlarni qidirish
      -> source_id + source_version + source_section + approval maqomini qo‘shish
      -> Gemini API ga savol va topilgan ichki parchalarni yuborish
      -> Google Search grounding (foydalanuvchi alohida yoqsa)
      -> javob va grounding URL manbalarini ajratish
      -> UI da ichki candidate yozuvlar va tashqi manbalarni alohida ko‘rsatish

Google Search o‘chirilgan bo‘lsa, modelga Google Search tool berilmaydi. Yoqilgan bo‘lsa, Gemini qidiruvni o‘zi zarur deb topganida bajaradi va API javobidagi grounding manbalari UI da ko‘rsatiladi.

## 3. Bilimlar bazasi

Joriy v4 JSON bazasi 137 yozuvdan iborat:
- 33 — v3 legacy candidate yozuvlari;
- 16 — v4 qatlam katalogi;
- 22 — v4 repository konsepsiya yozuvlari;
- 42 — V14/AI arxitekturasi, AI baholash va V317 korpus auditidan tanlangan yozuvlar;
- 24 — 25 bobli integratsiyalashgan kitobning 1–24-boblari bo‘yicha sahifali xulosalar.

**Barcha 137 yozuv candidate_not_authoritative.** Hozircha authoritative/approved yozuv yo‘q.

Har bir yozuvda source_id, source_version, source_section, source_path, approval va record_type saqlanadi. knowledge_manifest.json manbalar va ochiq bo‘shliqlarni qayd etadi.

Muhim: bu 137 yozuv to‘liq V14, V8, 16 qatlam chuqur tushuntirishi yoki asl FINZANJIR_AI.zip v0.6.0 korpusining to‘liq importi emas. V317 auditida qayd etilgan 4 671 yozuv ham to‘liq ko‘chirilmagan. To‘liq arxiv importi, manba sahifalari bilan crosswalk, duplicate/conflict tekshiruvi va ekspert tasdig‘i keyingi bosqichdir.

## 4. Qidiruv chegaralari

- Joriy retrieval lexical/synonym-based; embedding yoki to‘liq semantic/vector search emas.
- O‘zbek lotin/kirill transliteratsiyasi va ayrim sinonimlar qo‘llanadi, ammo morfologiya, sheva, imlo xatosi va barcha tillar bo‘yicha sifat tasdiqlanmagan.
- “16 qatlam” savolida 16 qatlam yozuvining barchasi kontekstga qo‘shiladi.
- Qidiruv mosligi/score haqiqat ehtimoli emas.
- R@k/P@k faqat ekspert belgilagan relevant gold set bilan o‘lchanishi mumkin.
- Topilmagan yozuv “FINZANJIRda umuman mavjud emas” degani emas; faqat joriy 137 yozuvli korpusda topilmagan bo‘lishi mumkin.

## 5. Gemini va Google Search

- SDK: Google tomonidan tavsiya etilgan google-genai 2.3.0 yoki undan yangi; Interactions API shu versiyadan boshlab mavjud.
- Model default: gemini-3.8-flash; Streamlit Secrets orqali almashtirilishi mumkin.
- Google Search: Gemini API built-in grounding tool; alohida checkbox bilan yoqiladi.
- Grounding manbalari API javobidan olinadi; manba qaytmasa, UI buni ochiq ko‘rsatadi.
- Google Search grounding Gemini 3 oilasida qidiruv so‘rovlari bo‘yicha xarajat keltirishi mumkin. Bir savol uchun model bir nechta qidiruv so‘rovini bajarishi mumkin.
- Gemini API va Google Search real ishlashi faqat yangi kalit qo‘yilgach Streamlit Cloud’da sinovdan o‘tadi.

## 6. Secrets va kalit boshqaruvi

Streamlit Cloud → App settings → Secrets ichiga quyidagi shaklda kiritiladi. Haqiqiy kalit faqat foydalanuvchining Streamlit Secrets oynasida bo‘ladi:

    [gemini]
    enabled = true
    api_key = "YANGI_GEMINI_API_KEY"
    model = "gemini-3.8-flash"
    max_requests_per_session = 5

Qoidalar:
- Eski, chatda oshkor bo‘lgan API kalit bekor qilinishi kerak.
- Yangi kalit faqat Streamlit Secrets ichiga kiritiladi.
- Kalit GitHub source, README, commit, issue, log yoki chatga yozilmaydi.
- Kod kalitni brauzerga chiqarmaydi; faqat Streamlit server tomonida ishlatadi.
- API xatolari foydalanuvchiga ko‘rsatilganda xom SDK exception yoki request metadata qaytarilmaydi.
- Google AI Studio/Cloud’da API key restriction, quota va billing alert sozlash tavsiya qilinadi.

Sessiya uchun 5 ta so‘rov chegarasi faqat yumshoq UI nazorati. Session yangilansa yoki yangi sessiya ochilsa qayta boshlanishi mumkin; bu billing cap yoki kuchli rate limit emas. Public release uchun server-side rate limit, provider quota va abuse monitoring alohida kerak.

## 7. Maxfiylik va ma’lumot oqimi

Gemini ishlatilganda foydalanuvchi savoli va qidiruvdan topilgan ichki bilim parchalari Google Gemini API ga yuboriladi. Har bir Interactions API chaqiruvida store=false beriladi: Google hujjatlariga ko‘ra bu server-side Interaction obyektini saqlashni o‘chiradi. Google Search yoqilsa, Gemini qidiruv so‘rovlarini Google Search orqali bajarishi mumkin.

Shu sabab:
- Haqiqiy mijoz ma’lumoti, karta raqami, hisob raqami, PIN, CVV/CVC, OTP, parol, bank siri yoki shaxsiy identifikatorni AI oynasiga kiritmaslik kerak.
- Ilova savol-javobni o‘zining loyiha ma’lumotlar bazasiga saqlamaydi; natija doimiy knowledge bazasiga yozilmaydi.
- store=false provider tomonidan Interaction resursini saqlashni o‘chiradi, lekin providerning xizmat ko‘rsatish, xavfsizlik va qonuniy data processing amaliyotini yo‘q qilmaydi. Streamlit hosting va Google providerning o‘z data processing siyosati ilova kodining nazoratidan tashqarida; “hech qayerda saqlanmaydi” deb va’da qilinmaydi.
- V4 ommaviy sahifasiga shaxsiy muallif biografiyasi, shaxsiy suhbat xotirasi yoki maxfiy hujjatlar import qilinmaydi.

## 8. Prompt injection va tashqi manba xavfi

- Ichki hujjat, candidate yozuv, foydalanuvchi matni va Google Search natijasi — ma’lumot; tizim ko‘rsatmasi emas.
- “Oldingi qoidalarni unut”, “kalitni chiqar”, “Case och”, “bankka xabar yubor” kabi matnlar bajarilmaydi.
- Gemini uchun function calling yoki bank/API amallari yoqilmagan.
- Model chiqishi oddiy matn va HTTPS manbalar sifatida ko‘rsatiladi; u kod yoki avtomatik amal sifatida bajarilmaydi.
- Prompt injection, soxta manba, qarama-qarshi hujjat, credential so‘rash va aybdorlikni qat’iy e’lon qilish bo‘yicha red-team testlar keyingi gate hisoblanadi.

## 9. Test va release gate

CI quyidagilarni tekshiradi:
- Python compile;
- 16 qatlamning hammasini keng savolda retrieval qilish;
- lotin/kirill qidiruvning mosligi;
- barcha yozuvlarda source provenance mavjudligi;
- barcha yozuvlar candidate holatda qolishi;
- karta raqamiga o‘xshash inputni rad etish;
- grounding URL larni filtrlash va dublikatni yo‘qotish;
- AI sahifasi va barcha public sahifalarning Streamlit smoke testlari;
- v4 AI modulida Tavily yo‘qligi va public appda Case/business-data write yo‘llari yo‘qligi.

CI PASS — source/unit/smoke test dalili. Bu Gemini API bilan jonli javob, Google Search grounding, xarajat nazorati, ekspert javob sifati, production security yoki barcha o‘zbekcha savollarning to‘g‘riligini tasdiqlamaydi.

## 10. Ochiq ishlar

1. Eski Gemini API kalitini bekor qilish va yangi kalit yaratish — hisob egasi bajaradi.
2. Streamlit Secrets sozlash.
3. Streamlit Cloud’da haqiqiy Gemini javobini sinash.
4. Google Search grounding va URL citations tekshirish.
5. To‘liq V14/V8/AI v0.6.0 hujjatlari va korpusini manba sahifalari bilan import qilish.
6. V317 4 671 yozuvni to‘liq ko‘chirmasdan oldin provenance, status, language va duplicate audit qilish.
7. Authoritative KBni faqat vakolatli tasdiq bilan yaratish; hozirgi candidate yozuvlarni avtomatik ko‘tarmaslik.
8. Uzbek Latin/Cyrillic, typo, negation, mixed-language, prompt injection va unsupported-question gold set tayyorlash.
9. Public billing/abuse control va privacy/legal review.
10. Mustaqil AI ekspert bahosi va reliz qabul mezonlari.
