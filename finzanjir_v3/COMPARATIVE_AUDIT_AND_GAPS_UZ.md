# FINZANJIR v3 — Eski versiyalar bilan solishtirma audit

Sana: 2026-11-07
Repository: qwerasdfzxc0311/finzanjir-app
Tekshirilgan branchlar: main, concept-aligned-v1, finzanjir-v3-synthetic-ai-uz

## 1. Tarixiy versiyalarni saqlash

- main: dastlabki prototip; tasodifiy risk ballari, oddiy tranzaksiya, operator/fuqaro/KPI ko'rinishlari mavjud. Bu kod tarixiy namuna, yangi tizim uchun ishonchli risk mexanizmi emas.
- concept-aligned-v1: alohida branch; v2 core va qulay sahifalar: boshqaruv paneli, hodisa/signal tahlili, Case/Human Review, aloqa grafigi, signal reyestri, audit, sinov markazi, 16 qatlam holati. Ushbu branch o'zgartirilmaydi.
- finzanjir-v3-synthetic-ai-uz: 400 hodisali laboratoriya va V317dan ajratilgan o'zbekcha candidate bilim qidiruvi.

## 2. Eski versiyalardan saqlash kerak bo'lgan foydali UX

1. Boshqaruv panelida KPI va oxirgi hodisalar.
2. Alohida Case/Human Review paneli va natijani izoh bilan qayd etish.
3. Aloqalar grafigi (faqat sintetik/pseudonim atributlar; aybdorlik isboti emas).
4. Signal reyestri (ID, manba maydoni, qoida cheklovi).
5. Audit jurnali.
6. Sinov markazi.
7. 16 qatlam holati — har bir qatlamni "ishlaydi" deb bo'rttirmasdan, real darajasi va cheklovi bilan ko'rsatish.

v3 da Human Review va Data Review mavjud, ammo alohida signal reyestri, graf, umumiy audit sahifasi va 16 qatlam status paneli hali yo'q. Eski versiyadagi fuqaro paneli va "bloklash" oqimi konsepsiyaning hozirgi xavfsiz chegarasiga mos emas; ko'chirilmasin.

## 3. v3 da topilgan muhim texnik va metodologik bo'shliqlar

### A. Sintetik yorliqning tasnifga sizib kirishi
Oldingi _classify() ssenariy nomining o'zidan ("ato", "social_engineering", "money_mule") Human Review chiqarardi. Bu test natijasini oldindan belgilangan yorliq bilan sun'iy ravishda moslashtirishi mumkin. Tuzatish: qaror faqat payload maydonlari/signallaridan chiqishi kerak; scenario/expected faqat test auditida qoladi.

### B. Dublikat transportni ortiqcha da'vo qilish xavfi
400 qatorning har biri yagona event_id. "duplicate_or_transport" holatida delivery_attempts=2 metama'lumoti bor, ammo ikkita mustaqil transport xabari queue'ga yuborilmaydi. Ikkinchi _process_one chaqiruvi DB state orqali idempotency'ni tekshiradi, lekin bu real webhook/transport simulyatsiyasi emas. UI va hujjatlarda bu chegarani ochiq ko'rsatish kerak.

### C. UI avtomatik yangilanmasligi
Worker fon oqimida ishlaydi, ammo sahifa avtomatik refresh qilmaydi; foydalanuvchi "Yangilash"ni bosishi kerak bo'lishi mumkin. Cloud'dagi monitoring uchun davriy yangilanish zarur.

### D. Eski foydali boshqaruv ekranlari yetishmaydi
v3 navigatsiyasida alohida Signal Registry, Graph, Audit va 16 qatlam holati yo'q. Ular eski versiyadagi qulayliklarning muhim qismi.

### E. Data Review va qayta tekshiruvning chegarasi
Data Review statusi o'zgaradi, ammo bankdan yangi payload kelishini qabul qiluvchi haqiqiy transport endpoint yo'q. "DATA_RECEIVED_RECHECK" hozircha workflow statusidir, qayta kelgan bank ma'lumoti emas.

### F. Bank ACK/NACK va yetkazish holati
Haqiqiy bank API, imzolangan webhook, autentifikatsiya, ACK/NACK, retry/backoff, dead-letter queue, schema version va idempotency persistence real bank bilan tekshirilmagan.

### G. Human Review vakolati
Hozirgi UI demo reviewer ID, SSO/RBAC, ikki kishilik tasdiq, case assignment va access audit bilan himoyalanmagan. Production ruxsati sifatida talqin qilinmasin.

### H. Saqlash va audit
SQLite bitta prototip jarayoni uchun; retention, arxiv, backup/restore, shifrlash, kalit boshqaruvi, tamper-evident audit va parallel worker xavfsizligi production darajasida isbotlanmagan.

### I. AI qidiruvi
offline_ai.py extractive lexical retrieval; generativ model emas. O'zbek lotin/kirill, imlo xatolari, morfologiya, negatsiya, adversarial savollar va retrieval precision/recall keng test qilinmagan. 33 candidate yozuv authoritative emas.

### J. 16 qatlam
v3 da L11 boshqaruvlari va L01/L02/L04/L07/L08/L13ning ayrim demo qismlari bor; qolgan qatlamlarning ko'p qismi to'liq amalga oshmagan. "16 qatlam ishlaydi" degan da'vo mumkin emas.

## 4. Tuzatish va rivojlantirish navbati

P0 — ishonchlilik:
- scenario label leakage yo'qotish;
- UI avtomatik yangilanishi;
- dublikat transport demo va haqiqiy transport farqini ko'rsatish;
- regression testlarda sintetik ssenariylar kutilgan oqim bilan tekshirilishi.

P1 — eski UXni qaytarish:
- Signal Registry;
- pseudonim aloqa grafigi;
- Audit jurnali;
- 16 qatlam holati (honest status);
- boshqaruv paneli va alohida Human/Data Review.

P2 — test chuqurligi:
- 400 hodisa bo'yicha barcha payload maydonlari va har bir yo'nalish uchun testlar;
- missing/contradictory/duplicate/retry/restart/stop race;
- false positive/false negative faqat mustaqil ekspert ground-truth bo'lganda.

P3 — integratsiya:
- bank adapter contract, signed webhook, ACK/NACK, retry/backoff, dead-letter;
- schema/version mapping va data provenance;
- access control, encryption, key management, retention, backup;
- local AI model va Android runtime alohida release gate.

## 5. O'zgarmas FINZANJIR chegaralari

- FINZANJIR karta yoki tranzaksiyani avtomatik bloklamaydi.
- Signal yoki Case aybdorlik hukmi emas.
- Bir qurilma/atribut mosligi shaxsning aybdorligini isbotlamaydi.
- Yetarli dalil bo'lmasa qayta tekshiruv yoki noaniqlik holati saqlanadi.
- Bankka yuborish faqat vakolatli inson ko'rigidan keyingi tayyor paket; hozir haqiqiy jo'natma yo'q.
- Sintetik test natijasi real bank aniqligi yoki production tayyorligini isbotlamaydi.
- V317 materiallari candidate maqomida qoladi; Authoritative KBga avtomatik o'tkazilmaydi.

## 6. Qabul mezonlari

- Eski branchlar o'zgarmagan holda qoladi.
- v3 da eski UXning xavfsiz qismlari qayta paydo bo'ladi.
- Scenario label tasniflash kodiga ta'sir qilmaydi.
- UI ish jarayonini o'zi yangilab ko'rsatadi.
- Har bir qatlamning statusi aniq va isbotlangan darajada ko'rsatiladi.
- CI testlar o'tadi; Cloud runtime va real Android/AI hali alohida tekshiriladi.

## 7. Ushbu audit davomida bajarilgan o'zgarishlar

- Eski branchlar o'zgartirilmadi; ish faqat finzanjir-v3-synthetic-ai-uz branchida davom etdi.
- v2 dan Signal reyestri, pseudonim aloqalar grafigi, Audit jurnali va 16 qatlam holati sahifalari xavfsiz cheklovlari bilan qaytarildi.
- Dashboard, laboratoriya va hodisalar sahifalariga avtomatik yangilanish qo'shildi.
- Classifier ichidan scenario nomiga qarab Human Review berish olib tashlandi; tasnif payload maydonlari/signallari asosida qoladi.
- Buni tekshiruvchi regression test qo'shildi.
- Dublikat ssenariy izohi aniqlandi: ikki delivery attempt faqat sintetik metama'lumot; haqiqiy transport/webhook retry hali yo'q.
- CI endi v3 requirements.txt ni o'rnatadi, shunda Cloud UI refresh dependency ham test/build muhitida mavjud bo'ladi.

## 8. Auditdan keyingi tekshiruv natijasi

GitHub Actions run: 42355931242
- Python compile: PASS
- Unit/regression: 17 test PASS
- 400 event pipeline: PASS
- Scenario-label independence: PASS
- Emergency stop/recovery: PASS
- Human review / bank response not-sent boundary: PASS

Bu CI natijasi source-level testdir. Streamlit Cloud'da brauzer orqali real ishga tushirish, uzoq muddatli worker barqarorligi, Android offline runtime va bank integratsiyasi hali alohida tekshirilishi kerak.
