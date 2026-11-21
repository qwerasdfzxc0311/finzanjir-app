# FINZANJIR Android — SINBAD/ATMOS atamalari uchraydigan 26 yozuv uchun scope crosswalk

**Sana:** 2026-11-20  
**Maqom:** item-by-item inventar va dastlabki scope tavsiyasi; to‘liq matnli ekspert ko‘rigi emas.  
**Asos branch:** finzanjir-android-v1  
**Audit branch:** finzanjir-knowledge-audit-2026-11  
**Asosiy cheklov:** hech bir original yozuv o‘chirilmaydi, birlashtirilmaydi yoki Android assetidan ko‘chirilmaydi. Ushbu hujjat faqat audit qaydidir.

## 1. Tekshiruv dalillari va cheklov

Ushbu crosswalk 2026-11-19 dagi record-level audit hujjatida qayd etilgan 26 ta original ID ro‘yxatini item-by-item ajratadi. O‘sha audit har bir yozuv matnida SINBAD va ATMOS atamalari uchrashini qayd etgan. 2026-11-20 kuni GitHub’dagi Android JSON asset uchun ayni blob SHA qayta olindi: **fc57872f98b33ecec0d182e58354f63ee9d4b7c1**. Biroq repository connector katta JSON faylining matnini bu seansda qaytarmadi (bo‘sh content). Shu sababli 26 ta yozuvning to‘liq matni, atrofidagi paragraf va semantik mazmuni bugun qayta o‘qilmadi.

Shuning uchun:
- atamalar mavjudligi — avvalgi record-level auditdan olingan, bugun qayta sanalmagan dalil;
- quyidagi locatorlar — original ID ichida kodlangan bob/sahifa/segment yoki V14 sahifa identifikatori;
- kitobning original PDF va V14 original PDFsi joriy Library PDF ro‘yxatida topilmadi; vizual sahifa tekshiruvi bajarilmadi;
- mazmuniy xulosa, faktik tasdiq yoki tashkilotlar haqida huquqiy xulosa chiqarilmadi;
- bu hujjat ZIP-1/ZIP-2 crosswalki yoki merge ledger o‘rnini bosmaydi.

## 2. Manba darajasidagi metadata

Android knowledge manifestidagi manba registri bo‘yicha:

| Guruh | Manifest source_id | Manba nomi | Versiya | Manba yo‘li |
|---|---|---|---|---|
| 25 bobli kitob | SRC-YAGONA-25B | FINZANJIR Yagona Tizim Kitobi — 25 bobli integratsiyalashgan ishchi kitob | 2026 integrated working book | FINZANJIR_YAGONA_YAXLIT_KITOB_25_BOB.pdf |
| V14 konsepsiya | SRC-V14-ORIGINAL | FINZANJIR V14 original concept PDF | V14 / 2026 | FINZANJIR_KONSEPSIYA_V14.pdf |

Bu qiymatlar manifestdagi package-level manba registridan olingan. JSON faylining to‘liq matni bu seansda qaytmagani uchun ularni har bir yozuvning individual JSON maydonlari bilan qayta solishtirish imkoni bo‘lmadi. Shuning uchun jadvaldagi source_id/version/path — manba guruhiga bog‘langan manifest qiymatlari, yangi per-record tasdiq emas.

## 3. Item-by-item inventar

Har bir qator uchun dastlabki scope tavsiyasi bir xil: **archive_only / excluded_from_active_retrieval — inson ko‘rigi kutilmoqda**. Bu tavsiya hali kod yoki assetda amalga oshirilmagan.

| Original ID | Manba guruhi | Record turi | Locator | Matn ko‘rigi | Dastlabki scope |
|---|---|---|---|---|---|
| BOOK25-CH15 | SRC-YAGONA-25B | book_chapter_summary_candidate | 15-bob xulosasi; sahifa oralig‘i bu audit dalilida aniqlanmagan | Kutilmoqda | archive_only — tavsiya |
| BOOK25-P17-S02 | SRC-YAGONA-25B | book_page_candidate | PDF sahifa 17, segment 02 | Kutilmoqda | archive_only — tavsiya |
| BOOK25-P167-S01 | SRC-YAGONA-25B | book_page_candidate | PDF sahifa 167, segment 01 | Kutilmoqda | archive_only — tavsiya |
| BOOK25-P189-S03 | SRC-YAGONA-25B | book_page_candidate | PDF sahifa 189, segment 03 | Kutilmoqda | archive_only — tavsiya |
| BOOK25-P190-S01 | SRC-YAGONA-25B | book_page_candidate | PDF sahifa 190, segment 01 | Kutilmoqda | archive_only — tavsiya |
| BOOK25-P191-S01 | SRC-YAGONA-25B | book_page_candidate | PDF sahifa 191, segment 01 | Kutilmoqda | archive_only — tavsiya |
| BOOK25-P192-S01 | SRC-YAGONA-25B | book_page_candidate | PDF sahifa 192, segment 01 | Kutilmoqda | archive_only — tavsiya |
| BOOK25-P192-S02 | SRC-YAGONA-25B | book_page_candidate | PDF sahifa 192, segment 02 | Kutilmoqda | archive_only — tavsiya |
| BOOK25-P192-S03 | SRC-YAGONA-25B | book_page_candidate | PDF sahifa 192, segment 03 | Kutilmoqda | archive_only — tavsiya |
| BOOK25-P193-S01 | SRC-YAGONA-25B | book_page_candidate | PDF sahifa 193, segment 01 | Kutilmoqda | archive_only — tavsiya |
| BOOK25-P193-S02 | SRC-YAGONA-25B | book_page_candidate | PDF sahifa 193, segment 02 | Kutilmoqda | archive_only — tavsiya |
| BOOK25-P193-S03 | SRC-YAGONA-25B | book_page_candidate | PDF sahifa 193, segment 03 | Kutilmoqda | archive_only — tavsiya |
| BOOK25-P194-S01 | SRC-YAGONA-25B | book_page_candidate | PDF sahifa 194, segment 01 | Kutilmoqda | archive_only — tavsiya |
| BOOK25-P194-S02 | SRC-YAGONA-25B | book_page_candidate | PDF sahifa 194, segment 02 | Kutilmoqda | archive_only — tavsiya |
| BOOK25-P194-S03 | SRC-YAGONA-25B | book_page_candidate | PDF sahifa 194, segment 03 | Kutilmoqda | archive_only — tavsiya |
| BOOK25-P197-S02 | SRC-YAGONA-25B | book_page_candidate | PDF sahifa 197, segment 02 | Kutilmoqda | archive_only — tavsiya |
| BOOK25-P284-S01 | SRC-YAGONA-25B | book_page_candidate | PDF sahifa 284, segment 01 | Kutilmoqda | archive_only — tavsiya |
| V14-P002 | SRC-V14-ORIGINAL | v14_page_candidate | V14 PDF sahifa 2 | Kutilmoqda | archive_only — tavsiya |
| V14-P014 | SRC-V14-ORIGINAL | v14_page_candidate | V14 PDF sahifa 14 | Kutilmoqda | archive_only — tavsiya |
| V14-P092 | SRC-V14-ORIGINAL | v14_page_candidate | V14 PDF sahifa 92 | Kutilmoqda | archive_only — tavsiya |
| V14-P112 | SRC-V14-ORIGINAL | v14_page_candidate | V14 PDF sahifa 112 | Kutilmoqda | archive_only — tavsiya |
| V14-P113 | SRC-V14-ORIGINAL | v14_page_candidate | V14 PDF sahifa 113 | Kutilmoqda | archive_only — tavsiya |
| V14-P114 | SRC-V14-ORIGINAL | v14_page_candidate | V14 PDF sahifa 114 | Kutilmoqda | archive_only — tavsiya |
| V14-P115 | SRC-V14-ORIGINAL | v14_page_candidate | V14 PDF sahifa 115 | Kutilmoqda | archive_only — tavsiya |
| V14-P116 | SRC-V14-ORIGINAL | v14_page_candidate | V14 PDF sahifa 116 | Kutilmoqda | archive_only — tavsiya |
| V14-P128 | SRC-V14-ORIGINAL | v14_page_candidate | V14 PDF sahifa 128 | Kutilmoqda | archive_only — tavsiya |

**Hisob nazorati:** 1 ta bob xulosasi + 16 ta kitob sahifa segmenti + 9 ta V14 sahifa yozuvi = **26 ta original ID**.

## 4. Governance va tasdiq holati

2026-11-19 dagi record-level auditda Android assetining 1,121 yozuvi uchun quyidagi umumiy holat qayd etilgan. JSON blob SHA bugun o‘zgarmagan, lekin katta fayl matni bu seansda qayta parse qilinmadi; shu sababli bu jadval avvalgi audit daliliga tayanadi.

| Maydon | Avvalgi auditdagi 1,121 yozuv holati | 26 yozuv uchun talqin |
|---|---|---|
| approval | 1,121/1,121 candidate_not_authoritative | Tasdiqlangan fakt yoki bank qoidasi emas |
| language | 1,121/1,121 uz | Til kodi mavjud deb avval qayd etilgan |
| author_attestation | Maydon yo‘q | Muallif tasdig‘i isbotlanmagan |
| independent_review | Maydon yo‘q | Mustaqil ekspert/bank ko‘rigi isbotlanmagan |
| privacy_scope | Maydon yo‘q | Har bir yozuvning maxfiylik doirasi belgilanmagan |
| access_scope | Maydon yo‘q | Kirish ruxsati yozuv darajasida belgilanmagan |
| domain | Maydon yo‘q | FINZANJIR/SINBAD/ATMOS doirasi strukturali ajratilmagan |
| source_page | 164 ta V14 yozuvda mavjud | V14 sahifa locatorlari bor; kitob segmentlarida IDdan tashqari strukturali sahifa maydoni yo‘q deb avval qayd etilgan |
| paragraph/table/slide locator | Alohida maydonlar yo‘q | Ushbu 26 yozuv uchun paragraf/jadval/rasm darajasidagi locator tasdiqlanmagan |

Bu maydonlar yo‘qligini taxmin bilan to‘ldirish mumkin emas. author_attestation=author_confirmed yoki independent_review=expert_reviewed kabi qiymatlar hujjat dalilisiz kiritilmasin.

## 5. Amaldagi qidiruv holati va xavf

Android branchdagi FinzanjirKnowledgeBase.kt fayli (blob SHA **1f49c0752412afdd9a075001c336dd214c0af7b0**) statik ko‘rildi:

- Record modelida privacy_scope, access_scope va domain maydonlari yo‘q;
- load() JSON massivini o‘qib, yaroqli yozuvlarni umumiy ro‘yxatga yuklaydi;
- search() val records = load(context) dan so‘ng odatiy qidiruvni shu ro‘yxat bo‘yicha bajaradi;
- kodda privacy_scope/access_scope/domain bo‘yicha qidiruvdan oldingi scope filtri topilmadi.

Shu sababli avvalgi auditda qayd etilgan 26 yozuv joriy qidiruv korpusidan texnik jihatdan chiqarilmagan. Bu statik kod dalili; Android qurilmada qayta runtime test bajarilmadi.

Audit README’sining 8-bo‘limida V14 10-bobidagi SINBAD/ATMOS materiallarini faol FINZANJIR KBga ko‘chirmaslik talabi bor. Hozirgi asset va qidiruv oqimi bu talabni yozuv darajasida majburiy bajarmaydi. Bu mutaxassislar namoyishida “SINBAD/ATMOS qidiruvdan ajratilgan” deb aytishga yo‘l qo‘ymaydi.

## 6. Tavsiya etilgan qaror — faqat audit darajasida

1. Ushbu 26 yozuvning asl matni va atrofidagi konteksti olinmaguncha ularni mazmunan “keraksiz”, “noto‘g‘ri” yoki “faqat tarixiy” deb yakuniy tasniflamaslik.
2. FINZANJIR faol qidiruvi uchun dastlabki tavsiya — ushbu 26 yozuvni archive_only / excluded_from_active_retrieval sifatida ko‘rib chiqish. Bu hozircha tavsiya; kodga qo‘llanmagan.
3. Original matn, ID, source_id, source_version, source_path, source_section va mavjud page/segment lokatorlari o‘zgarmasdan saqlansin.
4. Agar sahifada FINZANJIR uchun alohida tegishli mazmun ham bo‘lsa, asl yozuvni qisqartirish o‘rniga, faqat inson ko‘rigidan keyin originalga bog‘langan yangi hosila yozuv ko‘rib chiqilishi mumkin.
5. Near-duplicate, ziddiyat yoki mazmuniy takror bo‘yicha bu hujjat hech qanday o‘chirish/merge qarori bermaydi.
6. Test savollari bilimga qo‘shilmaydi.
7. BM25, Qwen yoki tashqi katta model APKga qo‘shilmaydi.
8. Bank karta/tranzaksiyasini avtomatik bloklash taklif qilinmaydi; har qanday amaliy qaror bank vakolatida qoladi.

## 7. Keyingi dalil talab qilinadigan bosqich

To‘liq semantik ko‘rik uchun quyidagilar zarur:
- original 25 bobli kitob PDFsi;
- original V14 PDFsi;
- Android JSON assetining record text va metadata bilan o‘qiladigan nusxasi;
- 26 yozuvning to‘liq matni, atrofidagi oldingi/keyingi paragraf yoki sahifa konteksti;
- har bir yozuvning source locator va checksum dalili.

Shundan keyin har bir ID bo‘yicha mazmuniy xulosa, tarixiy/arxiv/FINZANJIR aloqasi, ehtimoliy ziddiyat, privacy tavsiyasi va inson ko‘rigi qarori yozilishi mumkin. Hozirgi hujjat bu yakuniy qarorlarning o‘rnini bosmaydi.

## 8. Branch va o‘zgarish chegarasi

Yozuvdan oldingi GitHub compare:
- Android asos branch: **f38e0b7253c915e50f84ffe1053a9e40aec12733**;
- audit branch HEAD: **535175df9e41ffaeae3ab6bd19bd020f35e5ef76**;
- audit branch Androiddan **35 commit oldinda, 0 commit ortda**;
- compare ro‘yxatidagi 15 faylning barchasi docs/knowledge_audit/ ichida.

Ushbu commit faqat yangi audit hujjatini qo‘shish uchun mo‘ljallangan. Android, V3, V4 va main branchlariga yozuv kiritilmaydi. Android JSON, manifest, Kotlin kodi yoki APK o‘zgartirilmaydi. Build va qurilma testi bajarilmaydi.

**Qaror:** 26 original ID uchun scope inventari tuzildi. Ularning matni to‘liq qayta o‘qilmagani ochiq ko‘rsatildi. Faol qidiruvdagi scope muammosi mavjud; hech qanday avtomatik o‘chirish yoki integratsiya bajarilmadi. Merge ledger tayyor emas, integratsiya bloklangan.


## 9. 2026-11-21 — hujjat ichidagi inventarning strukturaviy qayta tekshiruvi

### 9.1. 26 qatorli jadvalning ichki yaxlitligi

Audit hujjatining 3-bo‘limidagi item-by-item jadval matni qayta o‘qilib, ID ustuni bo‘yicha strukturaviy tekshirildi:

- Jadvaldagi data qatorlari: **26**.
- Noyob original ID: **26**.
- Shu jadval ichida takrorlangan ID: **0**.
- `BOOK25-` prefiksli yozuvlar: **17**.
- `V14-P` prefiksli yozuvlar: **9**.

Bu natija faqat ushbu audit hujjatidagi jadvalning ichki arifmetikasi va ID takrorlanmasligini tasdiqlaydi. Android JSON assetidagi 1,121 yozuvni xom matn bilan qayta ochib, ushbu IDlar mavjudligini yoki har bir record textida SINBAD/ATMOS atamalari borligini bugun qayta tasdiqlash **emas**. Avvalgi record-level audit dalili o‘zining avvalgi tekshiruv sanasi bilan qoladi.

### 9.2. Asl manbalar mavjudligi — 2026-11-21 Library inventari

Library ro‘yxatining barcha 3 sahifasi ko‘rib chiqildi; jami **276 ta Library elementi** qayd etildi. Quyidagi aniq nomlar topilmadi:

- `Finzanjir konsepsiyasi va qoshimcha malumotlar hujjatlar (1).zip` — ZIP-1;
- `FINZANJIR_V317_SEMANTIC_GATE_PLUS_DOMAIN_EXPANSION.zip` — ZIP-2;
- `FINZANJIR_KONSEPSIYA_V14.pdf` — crosswalk uchun ko‘rsatilgan original V14 PDF;
- `FINZANJIR_YAGONA_YAXLIT_KITOB_25_BOB.pdf` — crosswalk uchun ko‘rsatilgan original 25 bobli kitob PDF;
- `FINZANJIR_BILIM_AUDIT_BATCH_2026-11-09.zip` — oldingi audit hosila arxivi.

Boshqa FINZANJIR nomli ZIP/DOCX/HTML/APK fayllari mavjud. Ularning nomi, hajmi yoki loyiha bilan bog‘liqligi ularni ZIP-1/ZIP-2 yoki ko‘rsatilgan original PDFlar bilan aynan bir xil deb qabul qilishga yetarli emas; ular o‘rniga ishlatilmadi. Joriy suhbat fayllari ro‘yxatida ham yuklangan manba yo‘q.

### 9.3. Branch snapshot va o‘zgarish chegarasi

Ushbu qo‘shimcha yozilishidan oldingi GitHub holati:

- Audit branch tipidagi commit: `f0229c395b076b9420dfc51bb2b6421b4ffdbbc9`.
- Android asos branch commit: `f38e0b7253c915e50f84ffe1053a9e40aec12733`.
- Compare: **36 commit ahead / 0 behind**.
- Android bilan diffdagi **16 faylning barchasi** `docs/knowledge_audit/` ichida edi.

Bu snapshot ushbu bo‘lim qo‘shilishidan oldingi holatdir. Keyingi audit commitlari ahead sonini oshirishi mumkin. Ushbu qo‘shimcha faqat audit hujjatiga tegishli; Android assetlari, Kotlin kodi, manifest, V3, V4 va `main` branchlariga yozuv kiritilmaydi.

### 9.4. Qaror

26 qatorli inventarning ichki soni va ID noyobligi tasdiqlandi, lekin bu manba matni bilan semantik tekshiruv o‘rnini bosmaydi. Asl ZIP-1/ZIP-2 va ikkita original PDF mavjud bo‘lmagani sababli 26 yozuvning to‘liq matni, oldingi-keyingi paragraf, sahifa tasviri va source checksum bo‘yicha ko‘rik bloklangan. Scope tavsiyasi hali tavsiya bo‘lib qoladi; hech qanday yozuv o‘chirilmaydi, birlashtirilmaydi yoki faol qidiruvdan kod orqali chiqarilmaydi.

**Integratsiya sharti bajarilmagan.** Merge ledger tayyor emas; Android bilimlari va ishlaydigan kodga tegilmaydi.
