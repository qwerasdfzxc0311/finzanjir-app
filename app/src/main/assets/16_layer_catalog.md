# FINZANJIR v4 — 16 qatlam katalogi (manba asosida)

Holat: manbadan ko'chirilgan boshlang'ich katalog; loyiha egasi/ekspert tasdig'i va implementatsiya dalili talab etiladi.
Manba: FINZANJIR 16 qatlam talablar va sinovlar reyestri V1 (L01–L16, REQ-001…REQ-016).
Muhim: reyestrdagi talab va testlar TAKLIF / TASDIQLANMAGAN. Quyidagi nomlar qatlam identifikatorlarini saqlash uchun kiritildi; ular amalda to'liq ishlaydi degani emas.

| Layer | Manbadagi nomi | Vazifasi (reyestrdagi talab mazmuni) | Hozirgi v4 holati |
|---|---|---|---|
| L01 | Evidence & Data Provenance | Muhim ma'lumot uchun manba, vaqt, olish usuli va versiya/identifikatorni saqlash; manbasi yo'q yozuvni tasdiqlangan dalil sifatida ko'rsatmaslik. | PLANNED |
| L02 | Data Quality & Reliability | To'liqsizlik, eskirish, dublikat va zid qiymatlarni sifat belgisi bilan ko'rsatish; ta'sirini yashirmaslik. | PLANNED |
| L03 | Risk & Uncertainty | Xavf signali/balli sabablarini, noaniqlikni va yetishmayotgan dalilni ajratish; ballni aybdorlik yoki yakuniy hukmga aylantirmaslik. | PLANNED |
| L04 | Human Oversight & Correction | Yuqori ta'sirli yoki noaniq holatni inson ko'rigiga yuborish; tuzatish va oldingi/keyingi qiymat izini audit qilish. | PLANNED |
| L05 | Rule & Model Governance | Qoida/model/config versiyasi, tasdiqlash vakolati va o'zgarish tarixini qayd etish; tasdiqlanmagan o'zgarish va rollbackni nazorat qilish. | PLANNED |
| L06 | Data Disclosure & Sharing Control | Tashqi uzatishdan oldin maqsad, ruxsat, qabul qiluvchi va minimal maydonlarni tekshirish. | PLANNED |
| L07 | Automation Safety & Control | Avtomatik amal chegarasi, sabab kodi va xavfsiz to'xtash/qo'lda ko'rik yo'lini belgilash. FINZANJIRning avtomatik bloklamaslik chegarasi saqlanadi. | PLANNED |
| L08 | Transaction Chain & Case Correlation | Case ichidagi hodisa manbasi, vaqti va bog'lanish sababini ko'rsatish; to'liq bo'lmagan zanjirni yakuniy isbotdek ko'rsatmaslik. | PLANNED |
| L09 | Citizen Transparency & Appeal | Foydalanuvchiga jarayon holati, tushunarli izoh va e'tiroz/tuzatish yo'lini loyihalash; maxfiy ichki yoki boshqa shaxs ma'lumotini oshkor qilmaslik. | PLANNED |
| L10 | Privacy & Data Lifecycle | Ma'lumot turi, maqsad, saqlash muddati, kirish va o'chirish/arxivlash qoidalarini belgilash. | PLANNED |
| L11 | Security Incident Response | Hodisa tasnifi, eskalatsiya, dalilni saqlash va tiklash bosqichlarini belgilash. | PLANNED |
| L12 | Knowledge Governance & AI Reliability | AI javobini manbaga bog'lash; manba yetarli bo'lmasa cheklov yoki bilmaslikni ochiq aytish; tasdiqlanmagan bilimni authoritative deb ko'rsatmaslik. | PLANNED / AI alohida gate |
| L13 | Testing & Independent Evaluation | Muhim talab uchun sinov, kutilgan/haqiqiy natija va dalilni qayd etish; etalon ma'lumot va qamrov cheklovini hujjatlashtirish. | PLANNED |
| L14 | Bank Integration Readiness | Integratsiyani faqat huquqiy/hamkorlik shartlari, spetsifikatsiya va xavfsizlik tasdiqlanganda baholash; tayyor bo'lmagan integratsiyani mavjud deb ko'rsatmaslik. | PLANNED |
| L15 | Performance & Capacity Management | Javob vaqti, xato ulushi, resurslar va tiklanish uchun o'lchash/qabul mezonlarini belgilash. | PLANNED |
| L16 | Impact & Harm Reduction | FP/FN va salbiy ta'sir metrikalari uchun formula, denominator, segment va taqqoslash usulini belgilash; sababiy ta'sirni dalilsiz da'vo qilmaslik. | PLANNED |

## UI'da qatlamlar qanday ko'rsatiladi

Har bir qatlam uchun umumiy karta:
- ID + aniq nom;
- oddiy tilda "nima qiladi?";
- nima uchun kerak;
- kiruvchi ma'lumotlar;
- chiqish / natija;
- qaysi qatlamlar bilan bog'liqligi;
- Case va Human Review'ga qanday ta'sir qilishi;
- cheklovlar va noma'lumlar;
- talab/test/evidence zanjiri;
- joriy implementatsiya holati.

## Bog'lanishlarni ko'rsatishdagi ehtiyot qoidasi

2026-10-30 dagi non-AI LINK matritsasi izchillik auditi v0.3 xulosasida 36 ta yo'nalish manba bilan qo'llab-quvvatlangan taklif sifatida qoldirilgan, lekin ular rasmiy LINK-ID emas va mustaqil texnik interfeysni isbotlamaydi. LINK-PROP-013 (L06 → L10) asosiy matritsadan chiqarilgan. LINK-PROP-037 (L04 → L07) manba zanjiriga tayangan mazmuniy yo'nalish, ammo texnik interfeys emas. REQ-017/TEST-017 va REQ-024/TEST-024 uchun qatlam mappingi ochiq.

Shu sabab v4 UI:
- manbada ko'rsatilgan yo'nalishlarni "manbaga asoslangan aloqa taklifi" deb belgilaydi;
- loyiha egasi tasdiqlamaguncha rasmiy LINK-ID deb atamaydi;
- kodda mustaqil servis/API mavjudligini anglatmaydi;
- har bir yo'nalish uchun manba, REQ/TEST va dalil holatini saqlaydi;
- tasdiqlanmagan teskari aloqa yoki qo'shimcha aloqani o'zi yaratmaydi.

## Dalil va holat qoidasi

Reyestrdagi test nomi yoki talab mavjudligi PASS degani emas. Qatlam holati faqat quyidagi dalillar bilan ko'tariladi: build/commit, konfiguratsiya, muhit, sana, bajaruvchi/reviewer, input, expected, actual, log/artifact va cheklov. Hozircha ushbu katalogdagi qatlamlarning hech biri v4 ichida implementatsiya qilingan deb belgilanmaydi.
