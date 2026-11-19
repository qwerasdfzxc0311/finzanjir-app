# FINZANJIR Android — faol qidiruv korpusi: scope va provenance auditi

**Sana:** 2026-11-19  
**Tekshiruv turi:** Android asos branchidagi statik asset/kod auditi; real qurilma yoki production sinovi emas.  
**Asos branch:** `finzanjir-android-v1`  
**Audit branch:** `finzanjir-knowledge-audit-2026-11`  
**Audit branch yozuvdan oldingi HEAD:** `3fbeeb4c3acd4e9e0b555ecbb74a780f9889a4b1`

## 1. Tekshiruv doirasi va dalillar

Quyidagi GitHub obyektlari to‘liq yoki tegishli qismi bilan o‘qildi:

| Obyekt | Branch / SHA | Tekshiruv |
|---|---|---|
| `app/src/main/assets/knowledge_manifest.json` | Android / `a946e6292d4b1bd65b570b414a70694107f5e2c1` | Manifest to‘liq o‘qildi |
| `app/src/main/assets/finzanjir_knowledge.json` | Android / `fc57872f98b33ecec0d182e58354f63ee9d4b7c1` | Git blob to‘liq olindi va 1,121 JSON yozuv parse qilindi |
| `app/src/main/java/uz/finzanjir/mobile/FinzanjirKnowledgeBase.kt` | Android / `1f49c0752412afdd9a075001c336dd214c0af7b0` | To‘liq statik kod ko‘rigi |
| `app/src/main/assets/IMPORT_STATUS_UZ.md` | Android / `44097524d7fb38d1e505d310900ed42c480f7ef9` | Import doirasi va cheklovlari o‘qildi |
| `docs/knowledge_audit/README_UZ.md` | Audit / `f31d2d4cb62fb8e3254952f5c31ce5fd7fd7bfd2` | 8-bo‘limdagi SINBAD/ATMOS chegarasi bilan solishtirildi |

Bu audit ZIP-1 yoki ZIP-2ning asl arxivlarini qayta tekshirish emas. U Android branchga allaqachon kiritilgan 1,121 yozuvli assetni tekshiradi.

## 2. JSON assetning real tarkibi

`finzanjir_knowledge.json` ichida **1,121 yozuv** bor. Barcha IDlar noyob; takrorlangan ID topilmadi.

| `record_type` | Soni |
|---|---:|
| `book_page_candidate` | 820 |
| `v14_page_candidate` | 164 |
| `ai_architecture_candidate` | 42 |
| `legacy_candidate` | 33 |
| `book_chapter_summary_candidate` | 24 |
| `project_concept_candidate` | 22 |
| `layer_catalog_candidate` | 16 |
| **Jami** | **1,121** |

Barcha 1,121 yozuvda:
- `approval = candidate_not_authoritative`;
- `record_status = candidate_not_authoritative`;
- `language = uz`;
- `source_id`, `source_version`, `source_section`, `source_path` va `source_package` mavjud.

`source_package` bo‘yicha taqsimot:

| Manba paketi | Yozuv |
|---|---:|
| 25 bobli Yagona Tizim Kitobi | 844 |
| V14 original PDF | 164 |
| V14 / AI V1 / V317 audit / v4 source audit aralash manbasi | 42 |
| V317 ZIP-2 legacy import | 33 |
| v4 repository hujjatlari | 22 |
| v4 arxitektura va 16 qatlam katalogi | 16 |
| **Jami** | **1,121** |

NFKC + kichik harf + ketma-ket bo‘sh joylarni birlashtirishdan keyingi aniq matn tengligi tekshiruvida 1,121 yozuv orasida exact-text duplicate guruhi topilmadi. Bu faqat shu normalizatsiyadagi aynan teng matn tekshiruvi; near-duplicate, mazmuniy takror yoki ZIP-1/ZIP-2 bilan hujjatlararo dublikat auditi emas. Hech qanday yozuv o‘chirilmagan yoki birlashtirilmagan.

## 3. Provenance va governance maydonlari

| Maydon | Mavjud yozuv | Yetishmaydi |
|---|---:|---:|
| `id` | 1,121 | 0 |
| `text` | 1,121 | 0 |
| `language` | 1,121 | 0 |
| `approval` | 1,121 | 0 |
| `source_id` | 1,121 | 0 |
| `source_version` | 1,121 | 0 |
| `source_section` | 1,121 | 0 |
| `source_path` | 1,121 | 0 |
| `source_package` | 1,121 | 0 |
| `source_page` | 164 | 957 |
| `author_attestation` | 0 | 1,121 |
| `independent_review` | 0 | 1,121 |
| `privacy_scope` | 0 | 1,121 |
| `access_scope` | 0 | 1,121 |
| `domain` | 0 | 1,121 |
| `kind` | 0 | 1,121 |
| `type` | 0 | 1,121 |
| `authority` | 0 | 1,121 |
| `content_hash` | 0 | 1,121 |

`source_page` faqat 164 ta V14 sahifa yozuvida strukturali maydon sifatida bor. Qolgan 957 yozuvda `source_section` ichida bob/PDF sahifa oralig‘i yoki segment matni bo‘lishi mumkin, lekin alohida `source_page` yo‘q. JSON sxemasida `paragraph`, `table_row`, `slide`, `asset` yoki umumiy `source_locator` maydonlari yo‘q.

**Talqin:** source ID/version/path mavjudligi ijobiy provenance belgisi, ammo u to‘liq paragraph/table/slide locator, per-record privacy ruxsati yoki mustaqil tasdiq o‘rnini bosmaydi. `candidate_not_authoritative` maqomi saqlangan; uni ekspert/bank tasdig‘i deb talqin qilish mumkin emas.

## 4. Kotlin qidiruv modeli metadata qismini o‘qimaydi

`FinzanjirKnowledgeBase.kt` dagi `Record` modeli quyidagi maydonlarni oladi: `id`, `text`, `approval`, `source_id`, `source_version`, `source_section`, `source_path`, `record_type`.

JSON assetda mavjud bo‘lsa-da, Kotlin modeliga olinmaydigan maydonlar:
- `language`;
- `source_package`;
- `source_page`;
- `record_status` (faqat `approval` bo‘lmasa fallback sifatida o‘qiladi);
- `author_attestation`, `independent_review`;
- `privacy_scope`, `access_scope`;
- `domain`, `kind`, `authority`.

Qidiruv `load(context)` orqali yuklangan yozuvlar ustida ishlaydi. Kodda `domain`, `privacy_scope` yoki `access_scope` bo‘yicha qidiruvdan oldingi filtr ko‘rinmadi. `record_type` faqat qatlamga oid maxsus so‘rovda ishlatiladi; odatiy so‘rovda boshqa barcha record type’lar birgalikda ballanadi.

Bu yerda muhim farq: yozuvlar authoritative emas, ammo **candidate bo‘lsa ham amaldagi lokal qidiruv korpusiga yuklanadi va topilishi mumkin**.

## 5. SINBAD / ATMOS bo‘yicha scope nomuvofiqligi

Android JSON assetida **26 ta yozuvda SINBAD va ATMOS atamalarining ikkalasi ham** uchraydi:

| Manba | Yozuv |
|---|---:|
| 25 bobli Yagona Tizim Kitobi | 17 |
| V14 original PDF | 9 |
| **Jami** | **26** |

Record type bo‘yicha:
- 1 ta `book_chapter_summary_candidate`;
- 16 ta `book_page_candidate`;
- 9 ta `v14_page_candidate`.

Original IDlar:

```text
BOOK25-CH15
BOOK25-P17-S02
BOOK25-P167-S01
BOOK25-P189-S03
BOOK25-P190-S01
BOOK25-P191-S01
BOOK25-P192-S01
BOOK25-P192-S02
BOOK25-P192-S03
BOOK25-P193-S01
BOOK25-P193-S02
BOOK25-P193-S03
BOOK25-P194-S01
BOOK25-P194-S02
BOOK25-P194-S03
BOOK25-P197-S02
BOOK25-P284-S01
V14-P002
V14-P014
V14-P092
V14-P112
V14-P113
V14-P114
V14-P115
V14-P116
V14-P128
```

V14 yozuvlaridagi strukturali sahifalar: 2, 14, 92, 112, 113, 114, 115, 116 va 128. 25 bobli kitob yozuvlarida bob/PDF sahifa/segment `source_section` matnida ko‘rsatilgan.

Audit branchdagi `README_UZ.md` 8-bo‘lim, 93-qator V14 mundarijasidagi 10-bob SINBAD/ATMOS yo‘nalishini faol FINZANJIR bilimlar bazasiga ko‘chirmaslik, manba arxivida qoldirish kerakligini aniq belgilaydi. Shu bilan birga, Android assetida V14 sahifalari 1–164 oralig‘ida import qilingan va yuqoridagi 9 sahifa, shuningdek Yagona Tizim Kitobidagi 17 yozuv qidiruv korpusida turibdi.

### Qidiruv oqimiga ta’siri

Kotlin qidiruv kodidagi ayni normalizatsiya/token-overlap ballash qoidasi bo‘yicha `“SINBAD nima?”` so‘rovi uchun statik algoritm simulyatsiyasi quyidagi besh yozuvni yuqori natija sifatida qaytardi:

1. `BOOK25-CH15`
2. `BOOK25-P17-S02`
3. `BOOK25-P167-S01`
4. `BOOK25-P189-S03`
5. `BOOK25-P190-S01`

Bu Android qurilmada bajarilgan runtime testi emas; repository kodi va asset tartibiga asoslangan qayta hisoblangan statik simulyatsiya. Lekin u 26 yozuv qidiruvdan scope bo‘yicha chiqarilmaganini ko‘rsatadi.

**Xulosa:** bu 26 yozuvning hammasi bir xil mazmundagi yoki bir xil maqomdagi material emas. Ayrimlari ogohlantirish, tarixiy kontekst yoki muallif kuzatuvi sifatida yozilgan. Ushbu audit ularning mazmunini tasdiqlamaydi va tegishli tashkilotlar haqida huquqiy xulosa bermaydi. Muammo — foydalanuvchining “SINBAD/ATMOS faol FINZANJIR KBga aralashmasin” chegarasi bilan amaldagi qidiruv korpusi o‘rtasidagi texnik nomuvofiqlik.

Hech biri o‘chirilmasin. Keyingi inson ko‘rigi ularni original matn, ID va provenance saqlangan holda `archive_only / excluded_from_active_retrieval` kabi alohida scope’da yuritish kerakmi, shuni hal qilishi lozim.

## 6. BM25 / Qwen bo‘yicha aniq farqlash

- Android JSON assetida BM25 tilga olingan bitta yozuv bor: `BOOK25-P104-S01`. Unda BM25, semantik qidiruv, RRF va reranking mumkin bo‘lgan usullar sifatida tasvirlangan; bu ularning APKda implementatsiya qilinganini bildirmaydi.
- JSON assetida Qwen atamasi topilmadi.
- Ko‘rilgan Kotlin qidiruv kodi token overlap va sodda ballashdan foydalanadi; BM25 implementatsiyasi ko‘rinmadi.
- Ushbu auditda BM25, Qwen yoki boshqa model qo‘shilmadi.

## 7. Xavfsiz keyingi qadamlar — hozircha faqat audit talabi

1. Yuqoridagi 26 original ID uchun inson ko‘rigiga mo‘ljallangan scope crosswalk tayyorlash: manba, sahifa/segment, record type, matn maqomi, muallif tasdig‘i, mustaqil ko‘rik va qidiruv doirasi.
2. Muallif-only/private, historical/archive, general encyclopedia va FINZANJIR-domain qatlamlari uchun per-record metadata sxemasini belgilash. Hozirgi JSONda bu maydonlar yo‘q; ularni taxmin bilan to‘ldirmaslik.
3. `source_page` kabi mavjud locatorlarni Kotlin javobining manba ko‘rsatish qismida yo‘qotmaslik; paragraph/table/slide locatorlar faqat asl manbadan tekshirilgandan keyin kiritilishi kerak.
4. Scope filtri va provenance maydonlari bo‘yicha har qanday kod/asset o‘zgarishini faqat ZIP-1/ZIP-2 item-by-item crosswalk, dublikat/ziddiyat ko‘rigi va merge ledger tugagach, alohida reja hamda foydalanuvchi tasdig‘i bilan ko‘rib chiqish.

## 8. Branch va o‘zgarish chegarasi

Yozuvdan oldin GitHub compare:
- audit branch Android asos branchidan 34 commit oldinda;
- 0 commit ortda;
- farqdagi 14 faylning barchasi `docs/knowledge_audit/` ichida.

Ushbu tekshiruvda Android, V3, V4 va `main` branchlariga yozuv kiritilmadi. `finzanjir-android-v1` dagi JSON, manifest va Kotlin fayllari o‘zgartirilmadi. Hech qanday yozuv o‘chirilmadi, birlashtirilmadi yoki APKga import qilinmadi. Build va real qurilma testi bajarilmadi.

**Qaror:** Android assetning to‘liq record-level sxemasi tekshirildi va SINBAD/ATMOS bo‘yicha faol qidiruv scope nomuvofiqligi aniqlandi. ZIP-1/ZIP-2 crosswalk va merge ledger hali yakunlanmagan; bilim integratsiyasi bloklangan.
