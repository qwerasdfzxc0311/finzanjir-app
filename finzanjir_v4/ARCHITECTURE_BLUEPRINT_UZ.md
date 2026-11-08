# FINZANJIR v4 — Yagona ish jarayoni va interfeys arxitekturasi

Holat: loyiha qarori va ishlab chiqish spetsifikatsiyasi (kodning ishlashi hali tasdiqlanmagan).
Branch: `finzanjir-v4-unified-workflow-uz`
Asos branch: `finzanjir-v3-synthetic-ai-uz`
Sana: 2026-11-08

## 1. Maqsad

FINZANJIRning barcha asosiy mexanizmlarini bitta izchil prototipda ko'rsatish: ma'lumot/signallarni qabul qilish, 16 qatlam orqali tahlil, dalillar va noma'lumliklarni ajratish, Case ochish mezonlari, Case boshqaruvi, Human Review va audit izi.

Bu versiya eski prototiplarning ko'rinishini shunchaki yangilash emas. Ularning foydali, tekshirilgan qismlarini saqlab, foydalanuvchiga tushunarli yagona ish jarayoniga qayta joylashtirishdir.

## 2. O'zgarmas loyiha chegaralari

1. FINZANJIR karta, hisob yoki tranzaksiyani bloklamaydi.
2. Signal yoki Case shaxsning aybdorligini anglatmaydi.
3. Bitta qurilma, telefon raqami, IP yoki boshqa umumiy atribut mosligi aybdorlik isboti emas.
4. Tizim firibgarlik turini, rozilik doirasini, dalillarni, zid dalillarni, noma'lum jihatlarni va ishonchlilik cheklovlarini alohida ko'rsatadi.
5. Yakka indikator avtomatik ravishda Case yoki ayblovga aylanmaydi; kontekst va belgilangan mezonlar kerak.
6. Yetarli ma'lumot bo'lmasa tizim taxmin qilmaydi: ma'lumot yetishmasligi yoki qayta tekshiruv holatini ko'rsatadi.
7. Human Review inson qarorini qayd etadi; avtomatik tizim inson vakolatini almashtirmaydi.
8. Sintetik sinov natijasi real bank aniqligi, firibgarlik ehtimoli yoki production tayyorligini isbotlamaydi.
9. Haqiqiy bank integratsiyasi, bankka yuborish, SSO/RBAC, production saqlash va huquqiy muvofiqlik mavjud deb ko'rsatilmaydi, toki alohida sinov va tasdiq bo'lmaguncha.
10. Oldingi `main`, `concept-aligned-v1` va `finzanjir-v3-synthetic-ai-uz` branchlari o'zgartirilmaydi.

## 3. Bitta bosh ish jarayoni

`Manba / Bank adapteri (hozircha sintetik)`
→ `Qabul qilingan hodisa`
→ `Ma'lumot sifati tekshiruvi`
→ `16 qatlam tahlili`
→ `Signal va dalillarni birlashtirish`
→ `Case ochish mezonlari`
→ `Case (faqat mezonlar bajarilsa)`
→ `Human Review`
→ `Inson qarori va asoslari`
→ `Audit izi / yakun`

Muqobil yo'nalishlar ham ko'rinadigan bo'lishi shart:
- Yetishmayotgan yoki o'zaro zid ma'lumot → DATA_REVIEW.
- Bitta noaniq indikator yoki dalil yetarli emas → RECHECK / MONITORING.
- Case ochish mezonlari bajarilmagan → NO_CASE, sabablar va kuzatuv holati bilan.
- Bir nechta mustaqil, tekshiriladigan indikator va mezonlar bajarilgan → CASE_CANDIDATE; vakolatli ish jarayoni bo'yicha Case ochiladi.
- Human Review natijasi: tasdiqlash, rad etish, qo'shimcha ma'lumot so'rash, qayta tekshiruv yoki yopish. Bu natijalar faqat demo workflow; haqiqiy huquqiy hukm emas.

## 4. Yagona ma'lumot modeli

Barcha sahifalar alohida nusxalangan ma'lumotlardan emas, bir xil markaziy modeldan foydalanishi kerak.

### 4.1 Entitylar

- Event: event_id, source_id, source_type, event_time, received_at, schema_version, payload, provenance, validation_status.
- Signal: signal_id, event_id, layer_id, rule_id, observed_value, interpretation, status, created_at.
- Evidence: evidence_id, case_id (ixtiyoriy), signal_id (ixtiyoriy), evidence_type, source, observed_at, supports_or_refutes, reliability_notes, limitations.
- Unknown: unknown_id, event_id/case_id, missing_or_unverified_fact, why_it_matters, requested_source, status.
- ConsentScope: consent_id, subject_reference (pseudonymous), device_use_scope, account_use_scope, transfer_scope, evidence_source, status, unknowns. Rozilik "bor/yo'q" degan bitta maydonga qisqartirilmaydi.
- Case: case_id, status, linked_event_ids, linked_signal_ids, linked_evidence_ids, fraud_type_hypothesis, consent_summary, open_reason, assigned_reviewer, created_at, updated_at.
- Review: review_id, case_id, reviewer_reference, action, rationale, evidence_considered, unresolved_questions, created_at.
- AuditEvent: audit_id, actor_type, actor_reference, action, object_type, object_id, before/after reference, timestamp.

### 4.2 Muhim farqlar

- Signal — kuzatilgan indikator; dalil bilan bir xil emas.
- Evidence — manbasi va cheklovi ko'rsatilgan tasdiqlovchi yoki inkor etuvchi material.
- Unknown — hali tasdiqlanmagan yoki yetishmayotgan fakt.
- Contradiction — ikki manba yoki maydon o'rtasidagi zidlik.
- Confidence — xulosa qanchalik asoslanganini ifodalovchi izohli daraja; kalibrlangan ehtimol deb ko'rsatilmaydi.
- Fraud type — tekshirilayotgan gipoteza; yakuniy ayblov emas.
- Consent scope — qurilma, hisob va aniq o'tkazma bo'yicha ruxsat chegaralarini alohida tekshiradi.

## 5. 16 qatlamni ko'rsatish qoidalari

16 qatlam nomlari, vazifalari va ketma-ketligi faqat foydalanuvchi tasdiqlagan konsepsiya manbasidan olinadi. Manba tekshirilmaguncha qatlam nomlari yoki vazifalari taxmin bilan yaratilmaydi.

Har bir qatlam uchun bir xil karta va tafsilot sahifasi bo'ladi:
- Qatlam ID va manbadagi aniq nomi.
- Maqsadi va aniqlaydigan savoli.
- Kiruvchi ma'lumotlar va talab qilinadigan bank maydonlari.
- Qaysi boshqa qatlamlar bilan bog'liqligi (LAYER → LAYER).
- Chiqaradigan signal/ma'lumot.
- Tasdiqlovchi va inkor etuvchi munosabatlar.
- Yetishmayotgan ma'lumot va cheklovlar.
- Case ochish qaroriga ta'siri (bevosita qaror emas, mezonlarga kiritiladigan hissa).
- Implementatsiya holati: NOT_IMPLEMENTED, PARTIAL, SYNTHETIC_DEMO, TESTED_WITH_SYNTHETIC_DATA, EXPERT_VALIDATION_PENDING, BANK_VALIDATION_PENDING.
- Testlar va dalillar havolasi.

Bitta qatlamning natijasi boshqa qatlamga yuborilganda source ID, timestamp, schema/version va izoh saqlanadi. Qatlamlar bir-biriga noto'g'ri ko'rsatkich yoki asossiz xulosa uzatmasligi uchun tiplangan ma'lumot kontraktlari va tekshiruvlar qo'llanadi.

16 qatlam bir ekranda umumiy bog'liqlik xaritasi sifatida, shuningdek Case ichida tegishli qatlamlar kesimida ko'rsatiladi. Ular 16 ta aloqasiz menyu sifatida tarqatilmaydi.

## 6. Operator interfeysi

Asosiy operator interfeysi bitta ilova va bitta doimiy navigatsiyaga ega bo'ladi.

1. Umumiy ko'rinish — tizim holati, ish navbati, so'nggi hodisalar, ochiq Case va DATA_REVIEW soni.
2. Ish jarayoni — qabuldan Human Reviewgacha bo'lgan vizual ketma-ketlik va har bir hodisaning joriy bosqichi.
3. Signallar — signal reyestri, manba, qoida, qatlam, dalil va holat.
4. 16 qatlam — qatlamlar xaritasi, tafsilotlari, bog'liqliklar va implementatsiya darajasi.
5. Case markazi — Case ro'yxati, filtrlash, tafsilotlar, bog'langan signallar/dalillar/unknowns.
6. Human Review — faqat Case kontekstida ko'rib chiqish, dalillarni tekshirish, qaror va sababni qayd etish.
7. Ma'lumot sifati / qayta tekshiruv — missing, contradiction, recheck navbati.
8. Aloqalar grafigi — faqat sintetik/psevdonim bog'lanishlar; atribut mosligi aybdorlik isboti emas.
9. Audit jurnali — kim/nima/qachon/qaysi obyektni o'zgartirgan.
10. Sinov laboratoriyasi — sintetik ssenariylar, qayta ishga tushirish, pauza/to'xtatish, test natijalari.
11. Hujjatlar va cheklovlar — konsepsiya manbasi, atamalar, tizim nimalarni qila olmasligi.
12. Muallif sozlamalari — faqat himoyalangan muallif ko'rinishi; tashrifchilar Case va maxfiy fikrlarni ko'ra olmaydi.

Tashrifchi uchun alohida ommaviy tanishtiruv sahifasi bo'lishi mumkin, lekin u operator Case ma'lumotlarini ko'rsatmaydi va haqiqiy fuqaro Case qidiruvi sifatida taqdim etilmaydi.

## 7. Vizual va foydalanish qulayligi

- Bir xil dizayn tizimi, sarlavha iyerarxiyasi, ikonka lug'ati va rang ma'nolari.
- Asosiy ranglar: sokin to'q ko'k/navy va och ishchi fon; ko'k — axborot/aktiv jarayon; sariq — tekshiruv kerak; qizil — jiddiy xato yoki qarama-qarshilik; yashil — tekshirilgan ijobiy holat; kulrang — noma'lum/faol emas.
- Rang hech qachon yagona ma'no tashuvchisi bo'lmaydi: matnli status va ikonka ham bo'ladi.
- Har bir sahifada "Bu nima?", "Nima uchun kerak?", "Keyingi qadam nima?" degan savollarga qisqa javob bo'ladi.
- Jadval va kartalar bir xil Case ID/Signal ID orqali o'zaro bog'lanadi.
- Mobil ekranlarda ham navigatsiya, matn va jadvallar o'qiladigan bo'ladi.
- Bir sahifada haddan tashqari ko'p KPI, bezak yoki mustaqil panel to'planmaydi.

## 8. Ma'lumotlar va xavfsizlik

- Dastlab barcha demo ma'lumotlar sintetik va aniq belgilangan bo'ladi.
- Haqiqiy bank ma'lumotlarini kiritish yoqilmaydi.
- Public visitor va operator/author ko'rinishlari ajratiladi.
- Case tafsilotlari public sahifada ko'rsatilmaydi.
- API kalitlari, parollar va maxfiy sozlamalar repozitoriyga yozilmaydi.
- SQLite faqat prototip cheklovlari bilan ishlatiladi; hosted diskning doimiyligi tasdiqlanmagan bo'lsa, doimiy saqlash deb va'da qilinmaydi.
- Har bir kritik amal auditga yoziladi.
- Demo vakolatlari production SSO/RBAC deb ko'rsatilmaydi.

## 9. Ishlab chiqish bosqichlari

A. Konsepsiya manbasidan 16 qatlam nomlari/vazifalarini tekshirish va qatlamlararo xaritani tuzish.
B. Eski v2/v3 kodlarining foydali va xavfli qismlarini inventarizatsiya qilish.
C. Yagona ma'lumot modelini va status/state machine ni yozish.
D. Yagona operator interfeysi va navigatsiya.
E. Synthetic pipeline va barcha yo'nalishlar.
F. Case detail + Human Review + audit.
G. 16 qatlam kartalari, xarita va Case ichidagi bog'lanishlar.
H. Signal registry, data review, graph, KPI va test lab.
I. Unit/integration/regression testlar va 400 sintetik hodisa tekshiruvi.
J. Streamlit Cloud brauzer tekshiruvi va mobil UX.
K. Deployment va xavfsizlik cheklovlari bo'yicha alohida gate.

## 10. Qabul mezonlari

- Barcha asosiy jarayonlar bitta navigatsiya va bir xil ma'lumot modeli orqali ishlaydi.
- Event → Signal → Evidence/Unknown → Case criteria → Case → Human Review → Audit izini bir hodisa bo'yicha boshidan oxirigacha kuzatish mumkin.
- Case ochilmagan yo'nalishlar ham sabab bilan ko'rsatiladi.
- 16 qatlamning har biri aniq manba, vazifa, input/output, bog'lanish va halol implementatsiya statusiga ega.
- Bir qatlam natijasi boshqa sahifada eskirgan yoki zid ko'rinishda qolmaydi.
- Scenario/expected label classifier qaroriga ta'sir qilmaydi.
- Sintetik ma'lumotlar real bank ma'lumoti sifatida ko'rsatilmaydi.
- Hech qanday avtomatik bloklash yo'q.
- Human Review qarorlari sabab va audit izi bilan saqlanadi.
- Barcha muhim sahifalar mobil brauzerda tekshiriladi.
- Test o'tmagan yoki hali ulanmagan funksiya UI da "ishlaydi" deb ko'rsatilmaydi.

## 11. Qarorlar reyestri

- DR-001: Yangi ish alohida `finzanjir-v4-unified-workflow-uz` branchida olib boriladi.
- DR-002: Eski branchlar va versiyalar o'zgartirilmaydi.
- DR-003: Yangi prototip bitta operator ish jarayoniga birlashtiriladi.
- DR-004: 16 qatlamning nomi/vazifasi manbasiz taxmin qilinmaydi.
- DR-005: Case va Human Review asosiy ketma-ketlikda, qatlamlar va dalillar bilan bog'langan holda ko'rsatiladi.
- DR-006: FINZANJIR avtomatik bloklamaydi; inson ko'rigi va dalil izini qo'llab-quvvatlaydi.
