# FINZANJIR — 16 qatlam DOCX extraction qamrovi bo‘yicha nomuvofiqlik

**Sana:** 2026-11-13  
**Tekshirilgan artefakt:** `FINZANJIR_BILIM_AUDIT_BATCH_2026-11-09.zip`  
**Manba hujjati:** `FINZANJIR_16_QATLAM_CHUQUR_TUSHUNTIRISH_V3_TUZATILGAN.docx`  
**Audit branch:** `finzanjir-knowledge-audit-2026-11`  
**Maqom:** extraction coverage bo‘yicha ochiq nomuvofiqlik; asl DOCX bilan qayta tekshiruv talab qilinadi.  
**Qaror:** hech qanday matn tiklanmadi, o‘chirilmadi yoki birlashtirilmadi; APKga tegilmadi.

## 1. Tekshiruv doirasi va yaxlitlik

Ushbu yugurishda faqat oldingi audit paketi mavjud bo‘ldi. Asl ZIP-1 va ZIP-2 Library hamda joriy conversation ZIP ro‘yxatida topilmadi; ishchi konteynerda ham faqat audit paketi bor edi. Shu sababli asl DOCX baytlarini qayta o‘qib tekshirish imkoni bo‘lmadi.

Tekshirilgan audit arxivi:
- `FINZANJIR_BILIM_AUDIT_BATCH_2026-11-09.zip`
- SHA-256: `eb6646f43d5d7e3f307bb404faeb5cdb97ec8025673e995dff867d04e9b46684`

Ichki fayllar:
- `source_manifest.json` SHA-256: `d1f2fe5eaa684a9738d3151df3c1efeb80337545add1c589066ead11e5fd07b7`
- `source_records_candidate.jsonl` SHA-256: `bb084b0c1388828e29a1b5ac950e8071409af6f6d95a700954be945f5a1cb288`

Bu hashlar faqat audit paketi va uning hosila fayllariga tegishli; asl ZIP-1 yoki DOCX checksumlari emas.

## 2. Manba manifestidagi ko‘rsatkichlar

`source_manifest.json` dagi ushbu DOCX uchun `source_stats` qatori:

- `items = 329`
- `new_chunks = 253`
- `chars = 39020`
- `status = candidate_layer_requirements_and_tests_not_implementation_proof`

Oldingi ZIP-1 inventarizatsiyasida shu DOCX uchun 305 ta bo‘sh bo‘lmagan paragraf, 3 ta jadval va jami 24 ta jadval qatori qayd etilgan. 305 + 24 = 329. Bu manba manifestidagi `items=329` soni bilan mos keladi.

## 3. Candidate JSONL ichidagi amaldagi qamrov

`source_records_candidate.jsonl` dan faqat shu DOCXga tegishli yozuvlar ajratildi:

| O‘lchov | Natija |
|---|---:|
| Candidate yozuvlari | 253 |
| Noyob ID | 253 |
| Paragraf lokatorli yozuv | 231 |
| Jadval qatori lokatorli yozuv | 22 |
| Matn belgilarining yig‘indisi | 36 592 |
| `chunk_index` | barcha 253 yozuvda 0 |
| Bo‘sh `text` | 0 |

Jadval lokatorlari bo‘yicha:
- T1: R1–R4 — 4 qator mavjud.
- T2: R2–R4 va R6–R11 — 9 qator mavjud; R1 va R5 uchun alohida yozuv yo‘q.
- T3: R1–R9 — 9 qator mavjud.

Shunday qilib, 24 ta manba jadval qatoridan 22 tasi alohida locator bilan ifodalangan. T2R1 va T2R5 holati asl DOCX bilan tekshirilishi kerak; ular bo‘sh, sarlavha, birlashtirilgan yoki tushib qolgan qator ekanini hozircha aniqlab bo‘lmaydi.

## 4. 76 ta item farqi — mazmun yo‘qolgan deb darhol xulosa qilinmaydi

Manba manifestida 329 item, JSONLda 253 candidate yozuv bor. Farq — 76 item.

Oldingi inventarizatsiyadagi 305 paragraf bilan solishtirganda:
- 231 paragraf lokatori alohida JSONL yozuviga ega;
- 74 paragraf itemi alohida yozuv/lokator sifatida ko‘rinmaydi;
- 24 jadval qatoridan 22 tasi alohida yozuv sifatida ko‘rinadi;
- jami farq: 74 + 2 = 76.

JSONL yozuvlarida `source_anchor` bitta `P<number>` yoki `T<number>R<number>` ko‘rinishida. `source_anchor_start/end`, bir yozuvga bog‘langan locatorlar ro‘yxati yoki item-to-chunk mapping maydoni yo‘q. Barcha 253 yozuvning `chunk_index=0`. Shuning uchun 76 item boshqa yozuvlarga ataylab birlashtirilganmi yoki extraction jarayonida alohida ifodalanmay qolganmi — mavjud paketning o‘zi bilan isbotlab bo‘lmaydi.

Candidate `text` maydonlarining jami 36 592 belgi, manifest esa 39 020 belgi ko‘rsatadi. Farq 2 428 belgi. `chars` hisoblash algoritmi va item-to-chunk birlashtirish qoidasi hujjatlashtirilmagan. Bu farq o‘z-o‘zidan mazmun yo‘qolganini isbotlamaydi, lekin to‘liq saqlanganlikni ham isbotlashga imkon bermaydi.

**To‘g‘ri tasnif:** `coverage_unverified / locator_mapping_incomplete`. “74 paragraf yo‘qolgan” yoki “to‘liq ko‘chirilgan” degan qat’iy xulosa chiqarilmaydi.

## 5. Dublikatlar bilan bog‘liqligi

Oldin aniqlangan 16 marta takrorlangan qatlam holati izohi candidate JSONLda 16 alohida paragraf lokatorida mavjud: P47, P58, P69, P80, P91, P102, P113, P124, P135, P146, P157, P168, P179, P190, P201, P212.

Bu takrorlar qatlam kontekstini saqlaydi. Ular 76 item farqini izohlash uchun avtomatik ravishda chiqarib tashlanmaydi. Hech qanday duplicate merge bajarilmadi.

## 6. Xavfsiz keyingi tekshiruv

Asl ZIP-1 va DOCX qayta mavjud bo‘lgach:

1. DOCXni asl baytlari bilan qayta ochib, SHA-256, bayt hajmi va versiyasini tasdiqlash.
2. 305 bo‘sh bo‘lmagan paragrafning har birini original `P<n>` lokatori bilan inventarizatsiya qilish.
3. Uch jadvalning 24 qatorini har bir katak mazmuni va `T<n>R<n>` lokatori bilan inventarizatsiya qilish.
4. 329 source itemni 253 candidate yozuv bilan exact text, normalized text va locator mapping orqali solishtirish.
5. Har bir candidate yozuv bitta manba itemiga tegishlimi yoki bir nechta itemni qamrab oladimi — aniq ko‘rsatish.
6. Birlashtirilgan item bo‘lsa, barcha original paragraph/table locatorlarini saqlaydigan mapping yaratish.
7. JSONLda ifodalanmagan item bo‘lsa, asl matnni qisqartirmasdan yangi audit hosila yozuviga kiritish.
8. Har bir yozuv uchun original ID, source path, version, language, approval, author_attestation, independent_review va privacy scope maydonlarini saqlash yoki yetishmovchilikni ochiq belgilash.
9. Natijani item-by-item crosswalk va keyinchalik merge ledgerga bog‘lash.

## 7. O‘zgartirilmagan narsalar

- Asl ZIP-1/ZIP-2ga o‘zgartirish kiritilmadi.
- Candidate JSONL qayta yozilmadi.
- 76 item bo‘yicha taxminiy tiklash yoki merge bajarilmadi.
- Dublikatlar o‘chirilmagan.
- Android manifest, knowledge asset, Kotlin/Compose kodi o‘zgartirilmadi.
- V3, V4, main yoki Android branchga commit qilinmadi.
- APK build yoki runtime testi bajarilmadi.

**Yakuniy xulosa:** 16 qatlam DOCX uchun manba manifestidagi 329 item va candidate JSONLdagi 253 yozuv o‘rtasida 76 itemlik locator/representation farqi hamda 2 428 belgilik hisob tafovuti aniqlandi. Bu hozircha mazmun yo‘qolganining yakuniy isboti emas; ammo asl DOCX bilan item-by-item tekshiruvsiz to‘liq extraction deb qabul qilish mumkin emas. Integratsiya bloklangan holda qoladi.
