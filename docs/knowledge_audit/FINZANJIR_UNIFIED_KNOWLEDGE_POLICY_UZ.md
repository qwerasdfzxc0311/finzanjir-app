# FINZANJIR — yagona bilim va ishlash siyosati

## 1. Bitta tizim, umumiy bilim
Fuqaro interfeysi, signal, Risk Engine, Fraud Graph, Case Management, Human Review, bank adapteri, audit va AI yordamchisi alohida uzilgan mahsulotlar emas. Ular umumiy identifikatorlar, ma’lumot modeli, manba izi va holat o‘zgarishlari bilan bog‘langan bitta tizimning qismlari bo‘lishi kerak.

Muallif uchun alohida kirish oynasi yoki maxsus muallif akkaunti talab qilinmaydi. Mutaxassislar tegishli vakolat doirasida umumiy ish oynalari va loyiha bilimlarini ko‘ra oladi. Maxfiy fuqaro/bank ma’lumotlari esa rol va vazifa bo‘yicha cheklanadi. Muallifga oid shaxsiy kontekst aloqasiz fuqaro javoblariga avtomatik qo‘shilmaydi; mutaxassis tegishli savol yoki ish kontekstida uni ko‘ra oladi.

## 2. 16 qatlam — funksional/nazorat mas’uliyatlari
1. Dalil va ma’lumot kelib chiqishini kuzatish (Evidence & Data Provenance).
2. Ma’lumot sifati va ishonchliligi (Data Quality & Reliability).
3. Xavf va noaniqlikni boshqarish (Risk & Uncertainty).
4. Inson nazorati va xatoni tuzatish (Human Oversight & Correction).
5. Qoidalar va modellarni boshqarish (Rule & Model Governance).
6. Ma’lumotni oshkor qilish va almashish nazorati (Data Disclosure & Sharing Control).
7. Avtomatik jarayonlar xavfsizligi (Automation Safety & Control).
8. Tranzaksiya zanjiri va Case bog‘liqligi (Transaction Chain & Case Correlation).
9. Fuqaro shaffofligi va e’tiroz (Citizen Transparency & Appeal).
10. Maxfiylik va ma’lumotlar hayotiy sikli (Privacy & Data Lifecycle).
11. Xavfsizlik hodisasiga javob (Security Incident Response).
12. Bilimlar bazasi va AI ishonchliligi (Knowledge Governance & AI Reliability).
13. Sinov va mustaqil baholash (Testing & Independent Evaluation).
14. Bank integratsiyasiga tayyorlik (Bank Integration Readiness).
15. Samaradorlik va quvvat (Performance & Capacity Management).
16. Ta’sir va zarar kamayishini o‘lchash (Impact & Harm Reduction).

Qatlam alohida ekran yoki server bo‘lishi shart emas. Ular bitta Case oqimi va tizimning barcha tegishli modullarida nazorat vazifasini bajaradi. Har qatlam uchun maqsad, kirish/chiqish, vakolat chegarasi, xato holati, mas’ul rol va qayta bajariladigan test bo‘lishi kerak.

## 3. Yagona bank-integratsiya oqimi
Bank/PSP yoki boshqa ruxsatli manba → Secure API/Data Exchange → autentifikatsiya (masalan, TLS/mTLS) → API Gateway → schema/format/vaqt/dublikat tekshiruvi → normalizatsiya → Risk Engine → Cross-Match → Fraud Graph → izohlanadigan signal → Case Management → Human Review / bank ko‘rigi → vakolatli himoya yoki recovery jarayoni → audit/KPI → feedback.

Bu taklif etilayotgan arxitektura. Bank shartnomasi, yuridik asos, ruxsat, xavfsizlik bahosi va test muhiti bo‘lmaguncha real API ishlaydi deb ko‘rsatilmaydi. FINZANJIR bankning ichki tizimini almashtirmaydi; bank qarori bank vakolatida. FINZANJIR avtomatik bloklash, pulni qaytarish yoki firibgarlikni isbotlashni va’da qilmaydi.

## 4. Yagona AI savol-javob oqimi
Savol/kontekst → til va matnni normallashtirish → intent/maqsadni aniqlash → maxfiylik va xavfsizlik tekshiruvi → mos bilim qidiruvi → manba/versiya/maqom/ziddiyatni baholash → dalil yetarliligi → javob sintezi → yakuniy xavfsizlik nazorati → feedback va nazoratli bilim yangilash.

Bilim manbalari alohida maqomda saqlanadi:
- tasdiqlangan bilim;
- `candidate_not_authoritative` nomzod hujjatlar;
- tarixiy/arxiv material;
- suhbat konteksti;
- AI xulosasi.

Bular bir-biriga aralashtirilmaydi. Qidiruv mosligi tasdiq yoki haqiqat kafolati emas.

## 5. AI bilimini oshirish chegarasi
Bilim bazasiga hujjat qo‘shish — model vaznlarini o‘qitish (fine-tuning) emas. RAG/qidiruv korpusining kengayishi alohida, lokal LLM inference alohida, fine-tuning esa haqiqiy o‘qitish va baholash artefaktlari bilan tasdiqlanadigan boshqa jarayondir.

## 6. O‘zgarmas tamoyillar
- Shubhali ≠ firibgar/aybdor.
- Signal ≠ firibgarlik isboti.
- Risk balli ≠ huquqiy hukm.
- Fraud Graph aloqasi ≠ ayb isboti.
- Case ≠ yakuniy qaror.
- Ma’lumot yetishmasligi ≠ xavf yo‘q.
- AI yakuniy bank, huquqiy yoki tergov qarorini mustaqil qabul qilmaydi.
- CVV, OTP, PIN, parol va maxfiy kalitlar bilim bazasiga yoki demo maydonlariga kiritilmaydi.
