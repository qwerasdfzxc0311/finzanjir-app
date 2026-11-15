# FINZANJIR — candidate record schema va exact-duplicate qayta tekshiruvi

**Sana:** 2026-11-15  
**Audit branch:** `finzanjir-knowledge-audit-2026-11`  
**Tekshiruv obyekti:** 2026-11-09 audit hosila ZIP paketi; asl ZIP-1 yoki ZIP-2 emas.  
**Qaror:** yozuvlar o‘chirilmagan, birlashtirilmagan va APKga import qilinmagan.

## 1. Dalil va yaxlitlik

Tekshiruvdagi fayl: `FINZANJIR_BILIM_AUDIT_BATCH_2026-11-09.zip`.

- ZIP SHA-256: `eb6646f43d5d7e3f307bb404faeb5cdb97ec8025673e995dff867d04e9b46684`
- ZIP CRC tekshiruvi: muvaffaqiyatli.
- Ichki fayllar: 6 ta.
- `source_records_candidate.jsonl`: 1,456 yozuv, 1,456 noyob ID.
- `candidate_addendum_no_v14_or_history.jsonl`: 1,012 yozuv; barchasining IDsi 1,456 yozuvli asosiy to‘plam ichida.
- Addendumdan chiqarilgan 444 yozuv: V14 sahifa yozuvlari 399 ta va tarixiy hujjat yozuvlari 45 ta.

Bu paket ZIP-1 yoki ZIP-2ning to‘liq nusxasi emas. Tekshiruv faqat audit hosila paketidagi yozuvlar va metadata bilan cheklangan.

## 2. Exact duplicate reyestrini qayta tekshirish

Barcha 1,456 matn quyidagi normalizatsiya bilan solishtirildi: Unicode NFKC, non-breaking space oddiy bo‘sh joyga almashtirish, ketma-ket whitespace’ni bitta bo‘sh joyga yig‘ish va case-fold.

Natija:

- Normallashtirilgan exact duplicate guruhlari: **2**.
- Guruhlardagi yozuvlar: **20**.
- Mavjud `exact_duplicate_register.json`: **2 guruh / 20 yozuv**.
- Qayta hisoblangan guruhlar mavjud reyestr bilan mos tushdi.

Guruhlar:
1. 16 qatlam hujjatidagi bir xil qatlam-mavjudligi izohi — 16 ta alohida paragraf lokatori.
2. Signal reyestridagi bir xil jadval sarlavhasi — 4 ta jadvalning alohida birinchi qatori.

Bular kontekstual takrorlardir. Hech biri o‘chirilmaydi. Keyingi canonical modelda barcha 20 original ID va locatorlar bitta matnni qayta ishlatadigan alohida relationlar sifatida saqlanishi kerak. Near-duplicate yoki ziddiyatlar bo‘yicha ushbu tekshiruvda inson ko‘rigi bajarilmadi.

## 3. Author-only qatlamining alohida ID sxemasi

1,456 yozuvning 1,449 tasi ZIP-1 manbalaridan olingan `SRC-...` yozuvlari. Qolgan 7 tasi quyidagi alohida manba yo‘lidan:

`finzanjir_global_build/reference/author_archive/author_profile_records.json`

Ular `AUTHOR-...` ID prefiksidan foydalanadi. Bu ID formati farqi o‘z-o‘zidan xato emas; muallif arxivining alohida namespace’i sifatida ko‘rilishi kerak.

Yetti yozuvning metadata holati:

- `author_attestation=author_confirmed_as_supplied_in_prior_author_material`: 7.
- `independent_review=not_reviewed`: 7.
- `approval=author_visible_on_direct_request`: 5.
- `approval=author_confirmed_project_philosophy`: 2.
- `access_scope=direct_author_question_only`: 5.
- `access_scope=author_or_project_philosophy_question`: 2.
- `source_version`, `language`, `privacy_scope`, `source_status`, `chunk_index`: mavjud emas.

Ushbu 7 yozuv muallif tasdiqlagan material hisoblanadi, lekin mustaqil ekspert tasdig‘i emas. Ular umumiy FINZANJIR domain javoblariga avtomatik qo‘shilmasligi va belgilangan savol doirasidan tashqarida ko‘rsatilmasligi kerak.

## 4. 1,449 ZIP-source yozuvining schema bo‘shliqlari

| Maydon | Yetishmaydigan yozuvlar |
|---|---:|
| `source_version` | 1,456 |
| `language` | 1,456 |
| `privacy_scope` | 1,456 |
| `access_scope` | 1,449 |
| `source_status` | 7 (faqat author archive yozuvlari) |
| `chunk_index` | 7 (faqat author archive yozuvlari) |

Barcha 1,456 yozuvda `source_archive_path`, `source_anchor`, `content_hash`, `content_type`, `author_attestation`, `independent_review` va `approval` maydonlari mavjud. `independent_review` qiymati barcha yozuvlarda `not_reviewed`.

ZIP-source 1,449 yozuvda `approval=candidate_review_required` va `author_attestation=not_assessed`. Bu yozuvlarni tasdiqlangan bilim deb talqin qilish mumkin emas.

## 5. content_hash bo‘yicha cheklov

- Barcha 1,456 `content_hash` qiymati 20 ta hex belgidan iborat.
- Raw UTF-8 text baytlari bo‘yicha SHA-256, SHA-1 yoki MD5 digestining dastlabki 20 belgisi bilan mos kelgan yozuv: **0**.
- Shuning uchun ushbu `content_hash` qiymatlarining algoritmi va hisoblash inputi mavjud artefaktlardan aniqlanmadi.

Bu mazmun buzilgan yoki hash noto‘g‘ri degan isbot emas. Ammo algoritm va normalizatsiya qoidasi hujjatlashtirilmaguncha `content_hash`ni tekshirilgan checksum, original source fingerprint yoki canonical identity sifatida ishlatish mumkin emas. Asl ZIP fayllarining SHA-256 qiymatlari alohida hisoblanishi kerak.

## 6. Keyingi majburiy harakatlar

1. Asl ZIP-1 va ZIP-2 qayta mavjud bo‘lgach, har bir original faylning SHA-256 va bayt hajmini qayta hisoblash.
2. Author archive uchun alohida versioned schema va maxfiylik scope’ni hujjatlashtirish; mavjud 7 ID’ni o‘zgartirmaslik.
3. 1,449 ZIP-source yozuviga manba versiyasi, til va privacy scope’ni faqat asl manba yoki tasdiqlangan metadata asosida to‘ldirish.
4. Exact duplicate guruhlaridagi barcha original ID/locatorlarni kelajakdagi merge ledgerda bog‘lash; hozircha merge qilmaslik.
5. Near-duplicate va contradiction nomzodlarini alohida inson ko‘rigiga yuborish.
6. ZIP-1 va ZIP-2 manbalari bilan item-by-item crosswalkni davom ettirish.

**Yakun:** audit hosila paketining exact-duplicate reyestri qayta hisob bilan tasdiqlandi. Author-only 7 yozuvning alohida namespace’i va metadata bo‘shliqlari aniqlandi. Asl ZIP-1/ZIP-2 bilan to‘liq qamrov, mazmun saqlanishi yoki merge ledger hali isbotlanmagan. Integratsiya va Android kodi o‘zgarishi taqiqlangan holatda qoladi.
