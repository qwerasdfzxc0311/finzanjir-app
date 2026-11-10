# ZIP1 → V317 active index: keng qamrovli dastlabki leksik crosswalk

## Audit chegarasi
ZIP1 dagi 14 ta hujjatning 1,216 ta birliklari (DOCX paragraf/jadval qatori, PDF sahifasi, PPTX slaydi) V317 active indexidagi 4,671 yozuv bilan leksik usulda solishtirildi. Bu **qidiruv dalili**, semantik to‘liqlik yoki kodda ishlash isboti emas. Yuqori/qisman moslik importni, talab bajarilganini yoki mustaqil tasdiqni anglatmaydi. Moslik topilmasligi ham mazmun loyihada umuman yo‘q degani emas.

## Natijalar
| Manba | Birlik | Yuqori leksik moslik | Qisman | Mos dalil topilmadi |
|---|---:|---:|---:|---:|
| AI va bilim tizimi (PDF) | 29 | 1 | 27 | 1 |
| 16 qatlam talab/sinov reyestri (PDF) | 4 | 0 | 4 | 0 |
| 16 qatlam chuqur tushuntirish (DOCX) | 329 | 123 | 138 | 68 |
| Tarixiy ishchi hujjat (PDF) | 22 | 4 | 18 | 0 |
| Ekspertiza/False Positive V2 (DOCX) | 52 | 23 | 20 | 9 |
| Qo‘shimcha FDP ishchi nusxa (DOCX) | 169 | 71 | 65 | 33 |
| Qo‘shimcha amaliy talablar (PDF) | 19 | 8 | 11 | 0 |
| Fuqaro xavfsizligi (DOCX) | 186 | 27 | 104 | 55 |
| Kichik signallar (DOCX) | 76 | 10 | 37 | 29 |
| Ilg‘or signallar (DOCX) | 46 | 10 | 22 | 14 |
| Signal reyestri (DOCX) | 37 | 2 | 24 | 11 |
| Bank integratsiyasi arxitekturasi (PDF) | 66 | 8 | 58 | 0 |
| FINZANJIR KONSEPSIYA V14 (PDF) | 164 | 147 | 16 | 1 |
| Taqdimot (PPTX) | 17 | 13 | 4 | 0 |
| **Jami** | **1,216** | **447** | **524** | **221** |

## Eng muhim aniqlangan bo‘shliqlar
- 16 qatlam tushuntirish hujjatida 68 birlik uchun V317 active indexda aniq leksik dalil topilmadi.
- Fuqaro xavfsizligi hujjatida 55 birlik; FDP ishchi nusxasida 33 birlik; kichik signallarda 29 birlik; ilg‘or signallarda 14 birlik; asosiy signal reyestrida 11 birlik; ekspertiza tuzatishlarida 9 birlik uchun aniq leksik dalil topilmadi.
- Bu birliklar **yo‘qolgan deb hukm qilinmaydi**: keyingi bosqichda V317 indeks, kod, boshqa manba yozuvlari, sinonimlar va sahifa/jadval konteksti bilan tekshiriladi.
- V14 bo‘yicha yuqori leksik moslik ko‘p; bu V14 sahifalaridagi barcha diagramma, jadval va tasvirlar to‘liq import qilinganini bildirmaydi.
- 16 qatlam REQ/TEST/DEC reyestri PDFda 4 sahifadan iborat; undagi IDlar soni yoki mazmunini sahifalar sonidan kelib chiqib kamaytirib bo‘lmaydi. Oldingi inventarizatsiyada REQ-001..024, TEST-001..024 va DEC-01..10 qayd etilgan; har bir IDni alohida test daliliga bog‘lash hali talab qilinadi.

## Xavfsiz qarorlar
1. Asl ZIP fayllari o‘zgartirilmaydi; ushbu crosswalk hosila audit hujjatidir.
2. Hech qanday yozuv avtomatik o‘chirilmaydi yoki merge qilinmaydi.
3. Exact duplicate, near duplicate, contradiction va supersession alohida munosabatlar sifatida saqlanadi.
4. Muallif tasdiqlashi mustaqil ekspert/bank/rasmiy manba tasdig‘idan alohida yuritiladi.
5. Tarixiy hujjatlar arxivda; ATMOS/SINBAD faol FINZANJIR KBga ko‘chirilmaydi.
6. Test savollari faol bilimdan ajratiladi. Test natijasi faqat qayta bajarilib, dalil qayd etilganda qabul qilinadi.
7. Hozirgi Android Kotlin/Compose kodiga hech qanday o‘zgartirish kiritilmadi.

## Keyingi bitta jamlangan bosqich
V317 indeksidagi 188 FINZANJIR-domain yozuvlari bilan 1,216 manba birliklarini bog‘lash; keyin 24 REQ, 24 TEST, 10 DEC va signal IDlarini alohida reyestrga tushirish; so‘ng Android kodida har bir talab uchun real kod yo‘li/test dalilini qayd etish. Faqat shundan keyin source-preserving merge rejasi tuziladi.

**Xulosa:** bugungi tezkor keng qamrovli solishtirish bajarildi, ammo bu yakuniy semantik audit emas. 1,216 birlikning barchasi inventarizatsiya qilindi; 221 birlikda indeks ichida aniq leksik dalil topilmadi va ular alohida tekshiruvga qoldirildi.


## 10. 2026-11-10 audit correction — crosswalk nishoni va extraction yaxlitligi

### 10.1. 4,671 yozuv Android APK indeksi emas

Ushbu hujjatdagi 1,216 manba birligi, 447 yuqori leksik moslik, 524 qisman moslik va 221 mos dalil topilmagan natijalari **V317 active index (4,671 yozuv)** bilan solishtirishga tegishli. Ularni Android APKning import darajasi deb talqin qilish noto‘g‘ri.

Dalil:
- Android asos branchi `finzanjir-android-v1` dagi `app/src/main/assets/knowledge_manifest.json` `record_count: 1121` deb ko‘rsatadi.
- Shu manifestdagi turlar yig‘indisi ham 1,121: 33 legacy + 16 layer catalog + 22 project concept + 42 AI architecture + 24 chapter summary + 820 book page + 164 V14 page.
- V317 active index uchun 4,671 soni ZIP-2 auditida qayd etilgan. Bu alohida korpus.
- Audit branch Android asos branchidan ortda emas; branchlararo diffda faqat 9 ta `docs/knowledge_audit/` hujjati bor. Android kodi va assetlari o‘zgarmagan.

Shu sababli ushbu faylning nomi va 4,671 haqidagi jumlalar V317 active indexga moslab tuzatildi. Bu jadval **ZIP-1 → V317 aggregate lexical crosswalk** hisoblanadi. **ZIP-1 → Android APKning 1,121 yozuvi bo‘yicha item-by-item crosswalk hali bajarilmagan.** 447/524/221 sonlarini Android import isboti sifatida ishlatmaslik kerak.

### 10.2. Oldingi extraction paketining qayta yaxlitlik tekshiruvi

Tekshirilgan audit paketi: `FINZANJIR_BILIM_AUDIT_BATCH_2026-11-09.zip`.

- ZIP arxivi tekshiruvi: `unzip -t` — barcha 6 ichki fayl `OK`.
- Audit ZIP SHA-256: `eb6646f43d5d7e3f307bb404faeb5cdb97ec8025673e995dff867d04e9b46684`.
- `source_records_candidate.jsonl`: 1,456 yozuv; manifestdagi 1,456 bilan mos. Fayl SHA-256: `bb084b0c1388828e29a1b5ac950e8071409af6f6d95a700954be945f5a1cb288`.
- `candidate_addendum_no_v14_or_history.jsonl`: 1,012 yozuv; manifest bilan mos. Fayl SHA-256: `103b08099f33481ce3dec684a5836eab4375bdd17184aea24d6c21f34284ae17`.
- 1,456 ID o‘zaro unikal. 1,012 addendum IDning barchasi asosiy 1,456 yozuv ichida mavjud. Addendumdan chiqarilgan 444 yozuv aynan V14 sahifalaridagi 399 yozuv va tarixiy hujjatdagi 45 yozuv.
- Asosiy 1,456 yozuvning 1,449 tasi ZIP-1dagi 13 ta PDF/DOCX manbasidan olingan chunklar; qolgan 7 tasi V317 arxividagi `finzanjir_global_build/reference/author_archive/author_profile_records.json` dan olingan alohida muallif yozuvlari. Ularni ZIP-1 yozuvlari deb hisoblamaslik kerak.
- 1,456 yozuvning barchasida `source_archive_path` va `source_anchor` bor. 1,449 yozuvda `chunk_index` va `source_status` bor; 7 muallif yozuvida bu ikki maydon yo‘q.
- 1,456 yozuvning hech birida strukturali `source_version/version`, `language` yoki `privacy_scope` maydoni yo‘q. `access_scope` faqat 7 muallif yozuvida bor. 1,449 ZIP-1 yozuvida kirish doirasi belgilanmagan; bu ommaviy ko‘rsatishga ruxsat degani emas.
- `independent_review` barcha 1,456 yozuvda `not_reviewed`. `author_attestation`: 1,449 `not_assessed`, 7 muallif yozuvi `author_confirmed_as_supplied_in_prior_author_material`. Muallif tasdig‘i mustaqil ekspert tasdig‘i emas.
- 7 muallif yozuvining 5 tasi `author_visible_on_direct_request` / `direct_author_question_only`, 2 tasi `author_confirmed_project_philosophy` / `author_or_project_philosophy_question`. Ular umumiy qidiruvga avtomatik ochilmasligi kerak.
- `content_hash` maydoni 1,456 yozuvning hech birida matnning raw UTF-8 SHA-256 birinchi 20 belgisi bilan mos kelmadi. Bu ma’lumot buzilganini o‘z-o‘zidan isbotlamaydi, chunki hash algoritmi boshqacha bo‘lishi mumkin; ammo algoritm hujjatlashtirilmaguncha `content_hash` ni tekshirilgan integrity checksum deb qabul qilib bo‘lmaydi.
- Duplicate register qayta tekshirildi: 2 guruh, 20 yozuv. Barcha original IDlar topildi va har bir guruh ichidagi matn normallashtirilganda aynan teng. 16 qatlamga tegishli himoya izohi va 4 jadval sarlavhasi kontekst bilan saqlanadi; merge yoki o‘chirish bajarilmadi.

### 10.3. ZIP-1 extraction qamrovidagi yetishmayotgan obyektlar

ZIP-1 manba manifestida 20 obyekt qayd etilgan: 14 hujjat va 6 PNG. Candidate JSONL ichida ZIP-1dan 13 PDF/DOCX hujjatining chunklari bor, lekin:
- `FINZANJIR_TAQDIMOT.pptx` ning 17 slaydiga oid alohida source-recordlar yo‘q. 1,216 birlikli agregat crosswalkda 17 slayd sanalgan bo‘lsa-da, ular 1,449 ta ZIP-1 chunk reyestrida yo‘q.
- 6 PNG rasmning hech biri candidate JSONL ichida alohida vizual/source locator yozuvi sifatida yo‘q.

Demak, 1,456 yozuvli paket ZIP-1ning barcha 20 obyektini to‘liq saqlagan nusxa emas. ZIP1 per-file SHA-256 ro‘yxati alohida audit hujjatida mavjud, lekin asl ZIP-1 fayli ushbu ish seansida mavjud bo‘lmagani uchun bu hashlar qayta hisoblanmadi.

### 10.4. Manba fayllari va keyingi ochiq vazifa

Ushbu ish seansida asl ZIP-1 va ZIP-2 arxivlari joriy conversation fayllari yoki topilgan Library ro‘yxatida mavjud emas; faqat 2026-11-09 audit paketi va GitHub audit hujjatlari mavjud. Shu sababli:
1. Asl ZIP-1 fayllarining 20 obyektini, jumladan PPTX va 6 PNGni qayta ochib, hash va vizual lokatorlarni tekshirish hozircha bloklangan.
2. ZIP-2 ichidagi 7,053 source archive / 4,671 active index va 188 FINZANJIR-domain yozuvlarini item-by-item qayta o‘qish hozircha bloklangan. `V317_FINZANJIR_DOMAIN_AUDIT_UZ.md` dagi agregat sonlar 188 yozuvning o‘zi yoki ularning to‘liq provenance o‘rnini bosmaydi.
3. Keyingi crosswalk uchta maqsadni alohida yuritishi shart: ZIP-1 source units (1,216), V317 active index (4,671) va Android APK manifesti (1,121). Ularni bitta indeks deb aralashtirmaslik kerak.
4. `source-import/README_UZ.md` dagi ZIPlarni `finzanjir-android-v1` branchiga yuklash bo‘yicha eski ko‘rsatma ushbu topshiriqdagi branch himoyasiga zid; unga amal qilinmadi.
5. Hech qanday bilim integratsiyasi, dublikat merge, APK asset yoki ishlaydigan kod o‘zgarishi bajarilmadi.

**Keyingi zarur qadam:** asl ZIP-1 va ZIP-2 arxivlarini qayta taqdim etish; shundan so‘ng PPTX/PNG lokatorlarini to‘ldirish, V317ning 188 domen yozuvini ZIP-1 source unitlari bilan bog‘lash va Android 1,121 yozuvi uchun alohida item-by-item crosswalk tuzish. Merge ledger va to‘liq crosswalk tayyor bo‘lmaguncha integratsiya boshlanmaydi.
