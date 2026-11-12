# FINZANJIR — audit paketining yaxlitligi va metadata tekshiruvi

**Sana:** 2026-11-12  
**Branch:** `finzanjir-knowledge-audit-2026-11`  
**Holat:** faqat audit paketi tekshirildi; ZIP-1/ZIP-2 manbalari bilan yakuniy crosswalk emas; integratsiya ruxsati emas.

## 1. Tekshiruv doirasi va cheklov

Ushbu yugurishda mavjud bo‘lgan fayl `FINZANJIR_BILIM_AUDIT_BATCH_2026-11-09.zip` bo‘ldi. Asl ZIP-1 (`Finzanjir konsepsiyasi va qoshimsha malumotlar hujjatlar (1).zip`) va asl ZIP-2 (`FINZANJIR_V317_SEMANTIC_GATE_PLUS_DOMAIN_EXPANSION.zip`) Library ro‘yxatida topilmadi; ishchi konteynerda ham yo‘q. Shuning uchun asl arxivlarning baytlarini, ichki fayllarini yoki avval qayd qilingan manba checksumlarini bu yugurishda qayta tasdiqlash imkoni bo‘lmadi. Boshqa nomdagi eski FINZANJIR arxivlari ularning o‘rniga ishlatilmadi.

Audit ZIP CRC tekshiruvi: `unzip -t` — barcha 6 ichki fayl `OK`, “No errors detected”. Audit ZIP SHA-256:

`eb6646f43d5d7e3f307bb404faeb5cdb97ec8025673e995dff867d04e9b46684`

## 2. Audit ZIP ichki fayllari — SHA-256

| Fayl | SHA-256 |
|---|---|
| `AUDIT_BATCH_UZ.md` | `e26edac760da6a2014c76357332013a04c8f4c8720889c042e85601d962772fa` |
| `APP_WHOLE_SYSTEM_GAP_MATRIX_UZ.md` | `2a549018c72207edc5506f97889a2aa38ca07a268ded1c8bf528f3900246c75c` |
| `source_manifest.json` | `d1f2fe5eaa684a9738d3151df3c1efeb80337545add1c589066ead11e5fd07b7` |
| `source_records_candidate.jsonl` | `bb084b0c1388828e29a1b5ac950e8071409af6f6d95a700954be945f5a1cb288` |
| `exact_duplicate_register.json` | `5d4a9c7501970728b64596bbcdbeaf1e60833fc638ae826251bfe551da37e109` |
| `candidate_addendum_no_v14_or_history.jsonl` | `103b08099f33481ce3dec684a5836eab4375bdd17184aea24d6c21f34284ae17` |

Bu checksumlar faqat audit ZIP va uning ichki hosila fayllariga tegishli; asl ZIP-1/ZIP-2 checksumlari emas.

## 3. JSONL sonlari va ID yaxlitligi

- `source_records_candidate.jsonl`: 1,456 yozuv, 1,456 noyob ID.
- `candidate_addendum_no_v14_or_history.jsonl`: 1,012 yozuv, 1,012 noyob ID.
- Addendumdagi 1,012 ID asosiy 1,456 ID to‘plamining ichki qismi.
- Farq 444 yozuv: 399 V14 bo‘lagi va 45 tarixiy hujjat bo‘lagi. Bu chiqarib tashlash manifestdagi izohga mos.
- 1,449 yozuv ZIP-1dagi 13 hujjat manba statistikasiga mos; qolgan 7 yozuv `author_profile_records.json` manba yo‘lidan kelgan muallif yozuvlari. Ular ZIP-1 hujjat yozuvlari bilan bir xil manba qatlamiga qo‘shilmasligi kerak.
- Manifestdagi 13 `source_stats` qatori `new_chunks=1,449` beradi; `items` yig‘indisi 1,199. Bu ikki hisoblagichning ma’nosi hujjatda yetarlicha ta’riflanmagan; ularni teng deb qabul qilish yoki farqni yo‘qolgan yozuv deb talqin qilish mumkin emas.

## 4. ZIP-1 inventari va extraction qamrovi

Audit ZIP ichidagi `source_manifest.json` faqat 13 ta PDF/DOCX manbasini statistik jihatdan qayd etadi. ZIP-1 inventari esa 20 obyekt: 14 hujjat va 6 PNG. Alohida GitHub fayli `ZIP1_SOURCE_MANIFEST_SHA256_UZ.md` 20 obyekt, jumladan 17 slaydli PPTX va 6 PNG uchun bayt hajmi/checksumlarni oldin qayd etgan.

Shu sababli aniq farq quyidagicha:
- PPTX va 6 PNG avvalgi checksum manifestida ro‘yxatlangan;
- ular 1,456 ta candidate JSONL yozuvi orasida alohida slayd/rasm locatorlari sifatida yo‘q;
- avval qayd qilingan checksumlar asl ZIP hozir mavjud bo‘lmagani sababli bu yugurishda mustaqil qayta hisoblanmadi.

PPTX 17 slayd va 6 PNG uchun alohida source locator, vizual tekshiruv va crosswalk hali ochiq vazifa.

## 5. Metadata qamrovi — 1,456 yozuv bo‘yicha

| Maydon | Natija |
|---|---:|
| `source_file`, `source_archive_path`, `source_anchor` | 1,456/1,456 mavjud |
| `source_version` | 1,456/1,456 yo‘q |
| `language` | 1,456/1,456 yo‘q |
| `privacy_scope` | 1,456/1,456 yo‘q |
| `independent_review` | 1,456/1,456 `not_reviewed` |
| `author_attestation` | 1,449 `not_assessed`; 7 muallif yozuvi `author_confirmed_as_supplied_in_prior_author_material` |
| `approval` | 1,449 `candidate_review_required`; 5 `author_visible_on_direct_request`; 2 `author_confirmed_project_philosophy` |
| `access_scope` | 1,449 yo‘q; 7 muallif yozuvida cheklov ko‘rsatilgan |
| `source_status` | 7 muallif yozuvida yo‘q |

Yetti muallif yozuvi `author_profile_records.json`dan olingan; 5 tasi `direct_author_question_only`, 2 tasi `author_or_project_philosophy_question`. Ularning muallif tasdig‘i mustaqil ekspert tekshiruvi emas. `source_status` va `privacy_scope` maydonlari yetishmagani sababli ularni yangi sxemada restricted-review holatiga qo‘yish kerak; hozircha hech narsa o‘zgartirilmadi.

## 6. `content_hash` maydonining cheklovi

Barcha yozuvlarda 20 belgili hex `content_hash` bor, ammo algoritm yoki normalizatsiya spetsifikatsiyasi audit paketida berilmagan. Qiymatlar matnning raw UTF-8, trim, NFKC+whitespace SHA-256 shakllariga teng emas; tekshirilgan MD5/SHA-1/SHA-2/BLAKE2 variantlarining to‘liq yoki prefiks mosligi ham topilmadi.

Shuning uchun bu maydonni hozircha **checksum yoki manba yaxlitligi isboti** sifatida ishlatib bo‘lmaydi. Uni o‘chirib yoki almashtirib yuborish ham mumkin emas: mavjud IDlar shu qiymatga bog‘langan. Keyingi sxemada eski `content_hash` saqlanib, algoritmi aniqlanmaguncha opaque fingerprint deb belgilanadi; asl matn qayta mavjud bo‘lganda alohida, hujjatlashtirilgan `source_text_sha256` hisoblanishi kerak.

## 7. Exact duplicate reyestrining mustaqil tekshiruvi

`exact_duplicate_register.json`dagi ikkala guruh ham yozuvlarning haqiqiy `text` qiymatlari bo‘yicha tekshirildi:

1. 16 qatlam DOCX: 16 lokator (`P47` … `P212`) matni aynan teng. Bu 16 qatlamning har biridagi kontekstual himoya izohi; 16 uchrashuv saqlanadi yoki canonical matnga 16 source relation bilan bog‘lanadi.
2. Signal reyestri: `T1R1`, `T2R1`, `T3R1`, `T4R1` sarlavhalari aynan teng. To‘rtta jadval lokatori saqlanadi; bu alohida bilim javoblari emas.

Hech bir yozuv o‘chirilmagan, canonical merge qilinmagan va APKga o‘zgartirish kiritilmagan. Exact text tengligi tasdiqlandi; bu yaqin yoki zid yozuvlar to‘liq tekshirildi degani emas.

## 8. GitHub branch xavfsizligi va hujjat nomuvofiqligi

Yozuv yaratishdan oldingi branch holati:
- Audit branch HEAD: `402f4b1998978b27cddca153e67b9fb8ddb64f67`.
- Android asos branch HEAD: `f38e0b7253c915e50f84ffe1053a9e40aec12733`.
- Compare audit branch vs Android: `ahead_by=25`, `behind_by=0`; farqdagi 9 faylning barchasi `docs/knowledge_audit/` ichida.
- `README_UZ.md`ning 2026-11-11 bo‘limida oldingi audit HEAD sifatida `4b631bea57380fbe1b504615e1cac43261408e13` yozilgan. GitHub branch endpointida hozirgi HEAD `402f4b...`; README’dagi SHA joriy emas va tarixiy snapshot sifatida talqin qilinishi kerak.

Ushbu yugurishda asosiy Android, V3, V4 yoki main branchga yozuv kiritilmadi. APK kodi, Android assetlari va bilimlar bazasi o‘zgartirilmadi. Build/test bajarilmadi.

## 9. Keyingi ochiq vazifalar

1. Asl ZIP-1 va ZIP-2ni qayta mavjud qilish; har bir original fayl checksumini qayta tekshirish.
2. ZIP-1 PPTX 17 slayd va 6 PNGni source locatorlar bilan alohida inventarizatsiya qilish.
3. ZIP-2 188 FINZANJIR-domain yozuvini ZIP-1 source itemlari bilan item-by-item bog‘lash.
4. Android 1,121 yozuvi bilan alohida item-by-item crosswalkni yakunlash.
5. Missing `source_version`, `language`, `privacy_scope`, muallif yozuvlaridagi `source_status` va hash algoritmi uchun qarorlar reyestrini tayyorlash.
6. Exact/near duplicate, contradiction va supersession reyestrlarini inson ko‘rigi bilan yakunlash.
7. Har bir original ID/provenance canonical yozuvga qanday bog‘langanini ko‘rsatuvchi merge ledger tayyorlash.

**Qaror:** audit davom etadi. Ushbu yugurish audit paketining o‘z yaxlitligi va metadata bo‘shliqlarini tekshirdi; asl ZIP manbalarini to‘liq ko‘chirish yoki crosswalkni yakunlash emas. Bilim integratsiyasi va ishlaydigan kodga o‘tish uchun shartlar hali bajarilmagan.
