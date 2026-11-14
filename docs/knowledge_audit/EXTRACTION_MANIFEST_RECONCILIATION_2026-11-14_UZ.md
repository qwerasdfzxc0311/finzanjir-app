# FINZANJIR — ZIP-1 extraction manifest va candidate korpus reconciliation

**Sana:** 2026-11-14  
**Audit branch:** `finzanjir-knowledge-audit-2026-11`  
**Maqom:** mavjud audit artefaktlari ichidagi sonlar va locator qamrovi taqqoslandi; asl ZIP-1/ZIP-2 bilan qayta tekshiruv emas.  
**Qaror:** hech qanday bilim o‘chirilmadi, birlashtirilmadi yoki APKga qo‘shilmadi.

## 1. Tekshiruv uchun mavjud dalillar

Joriy ishchi konteynerda quyidagilar mavjud edi:

- `FINZANJIR_BILIM_AUDIT_BATCH_2026-11-09.zip`
- uning 6 ichki fayli.

Audit ZIP SHA-256:

`eb6646f43d5d7e3f307bb404faeb5cdb97ec8025673e995dff867d04e9b46684`

Tekshirilgan ichki fayllar:

| Fayl | SHA-256 |
|---|---|
| `source_manifest.json` | `d1f2fe5eaa684a9738d3151df3c1efeb80337545add1c589066ead11e5fd07b7` |
| `source_records_candidate.jsonl` | `bb084b0c1388828e29a1b5ac950e8071409af6f6d95a700954be945f5a1cb288` |
| `candidate_addendum_no_v14_or_history.jsonl` | `103b08099f33481ce3dec684a5836eab4375bdd17184aea24d6c21f34284ae17` |
| `exact_duplicate_register.json` | `5d4a9c7501970728b64596bbcdbeaf1e60833fc638ae826251bfe551da37e109` |

Asl ZIP-1 va ZIP-2 joriy suhbat fayllari hamda to‘liq Library ro‘yxatida aynan shu nomlar bilan topilmadi. Shu sababli quyidagi solishtirish audit hosila fayllari va GitHub’da avval qayd etilgan manifest qiymatlari orasida bajarildi. Oldingi source-file SHA-256 qiymatlari asl arxiv mavjud bo‘lmagani uchun qayta hisoblanmadi.

## 2. 1,456 yozuvning kelib chiqish arifmetikasi

`source_manifest.json` ichida 13 ta `source_stats` yozuvi bor:

| O‘lchov | Natija |
|---|---:|
| 13 manbadagi source items yig‘indisi | 1,199 |
| 13 manbadagi `new_chunks` yig‘indisi | 1,449 |
| JSONL candidate yozuvlari | 1,456 |
| JSONL ichidagi noyob ID | 1,456 |
| Alohida `author_profile_records.json` yozuvlari | 7 |
| Addendum yozuvlari | 1,012 |

Barcha 13 manba bo‘yicha JSONL yozuvlar soni `new_chunks` qiymatiga aynan teng. Demak, 1,456 quyidagicha tarkib topadi:

- ZIP-1ning 13 ta PDF/DOCX manbasidan 1,449 ta candidate chunk;
- alohida `author_profile_records.json` manba yo‘lidan 7 ta muallif yozuvi.

1,012 addendum yozuvi 1,456 to‘plamning ichki qismi. Unga V14ning 399 bo‘lagi va tarixiy hujjatning 45 bo‘lagi kiritilmagan. Bu 1,012 yozuv yangi, mustaqil 1,012 manba degani emas.

`items` va `new_chunks` boshqa-boshqa hisoblagichlardir: PDF sahifasi bir nechta chunk berishi mumkin; DOCX paragraf/jadval birliklari esa chunklash yoki filtrlash natijasida kamroq alohida yozuvga aylangan. Ularni tenglashtirish yoki farqni avtomatik ravishda yo‘qolgan mazmun deb talqin qilish mumkin emas.

## 3. ZIP-1 inventari bilan qamrov nomuvofiqligi

Oldingi `ZIP1_SOURCE_MANIFEST_SHA256_UZ.md` ZIP-1 ichida 20 obyektni qayd etadi:

- 14 ta hujjat;
- 6 ta PNG.

Ularning 13 tasi PDF/DOCX va `source_stats` ichida bor. 14-hujjat — `FINZANJIR_TAQDIMOT.pptx` (17 slayd, oldingi manifestda 7,798 matn belgisi) — `source_stats` ro‘yxatida yo‘q va `source_records_candidate.jsonl` ichida ham shu faylga tegishli yozuv topilmadi.

Shu sababli `AUDIT_BATCH_UZ.md` dagi “ZIP1 ichidagi 14 hujjat matn darajasida ajratildi” degan jumla candidate JSONL bilan tasdiqlanmaydi. To‘g‘riroq holat:

- 13 PDF/DOCX uchun candidate chunklar qayd etilgan;
- PPTX 17 slaydli manba inventarida mavjud, ammo candidate JSONL’da slayd lokatorlari yo‘q;
- 6 PNG inventarda mavjud, ammo ular uchun candidate JSONL’da vizual asset locatorlari yo‘q.

Bu PPTX matni hech qayerda ajratilmagan degan qat’iy da’vo emas. Faqat mavjud candidate paket ichida slaydma-slayd matn, vizual tekshiruv va crosswalk dalili yo‘qligini bildiradi. PNGlar matn JSONLga kiritilishi shart emas, lekin alohida asset/provenance reyestri va vizual ko‘rik talab qiladi.

## 4. DOCX source item va candidate chunk farqi

Oldingi ZIP-1 manifestida ko‘rsatilgan paragraf va jadval birliklari bilan `source_manifest.json`dagi `items` qiymatlari mos. Biroq yetti DOCX manbada `new_chunks` soni `items`dan jami 192 taga kam:

| DOCX manbasi | Source items | Candidate chunks | Farq |
|---|---:|---:|---:|
| 16 qatlam chuqur tushuntirish | 329 | 253 | 76 |
| Signal reyestri | 37 | 30 | 7 |
| Kichik signallar | 76 | 54 | 22 |
| Ilg‘or signallar | 46 | 39 | 7 |
| Qo‘shimcha FDP ishchi nusxasi | 169 | 140 | 29 |
| False-positive tuzatishi | 52 | 43 | 9 |
| Fuqaro xavfsizligi | 186 | 144 | 42 |
| **Jami** | **895** | **703** | **192** |

JSONLdagi ushbu DOCX yozuvlarining har birida bitta `source_anchor` bor, `chunk_index=0`, va har bir fayl ichida anchorlar noyob. Bitta candidate chunk bir nechta original paragraf/jadval lokatorini qamrab olganini ko‘rsatuvchi `source_anchor_start/end` yoki locatorlar ro‘yxati mavjud emas.

**Talqin:** 192 birlikning alohida chunk sifatida ko‘rinmasligi tasdiqlangan. Ular qo‘shni chunk matniga birlashtirilganmi yoki extractionda tashlab ketilganmi — mavjud artefaktlar bilan aniqlanmaydi. Shuning uchun `source_unit_to_chunk_mapping_unverified` holati qo‘yiladi; “192 item yo‘qolgan” yoki “mazmun to‘liq saqlangan” degan xulosa chiqarilmaydi.

Bu 16 qatlam hujjati bo‘yicha 2026-11-13 qayd etilgan 76 birlik farqini kengroq DOCX manbalariga yoyadi; avvalgi 76 soni ushbu 192 umumiy farq ichida qoladi.

## 5. PDF chunklash va source locator

PDF manbalarida `items` sahifa soniga mos, `new_chunks` esa ko‘p sahifalarda bir nechta chunkni qayd etadi:

| PDF manbasi | Sahifa/source items | Candidate chunks |
|---|---:|---:|
| Tarixiy ishchi hujjat | 22 | 45 |
| 16 qatlam talablar va sinovlar reyestri | 4 | 13 |
| Qo‘shimcha amaliy talablar | 19 | 54 |
| Bank integratsiyasi texnik arxitekturasi | 66 | 166 |
| AI va bilim tizimi | 29 | 69 |
| FINZANJIR KONSEPSIYA V14 | 164 | 399 |

Bu chunk sonining ko‘payishi o‘z-o‘zidan dublikat yoki mazmun ko‘paytirish xatosi emas. Bir sahifadagi bir nechta chunklar `source_anchor=PAGE<n>` va `chunk_index` orqali farqlanishi mumkin. Biroq sahifa tasviri, jadval/diagramma strukturasi va har bir chunkning matn oralig‘i alohida tekshirilishi kerak.

## 6. Matn belgilar soni bo‘yicha ikki manifest orasidagi farq

`ZIP1_SOURCE_MANIFEST_SHA256_UZ.md`dagi avval qayd etilgan belgilar soni bilan audit paketidagi `source_stats.chars` taqqoslandi. Bu qiymatlar asl manbadan qayta hisoblanmagan; oldingi manifest yozuvlari bilan audit hosila manifesti o‘rtasidagi farqdir.

| Manba | Oldingi manifest chars | Candidate manifest chars | Farq |
|---|---:|---:|---:|
| Bank integratsiyasi arxitekturasi | 177,937 | 177,821 | -116 |
| V14 konsepsiya | 426,482 | 424,929 | -1,553 |
| 16 qatlam chuqur tushuntirish | 38,909 | 39,020 | +111 |
| 16 qatlam talablar reyestri | 16,666 | 16,659 | -7 |
| AI va bilim tizimi | 78,795 | 78,766 | -29 |
| False-positive tuzatishi | 6,700 | 6,700 | 0 |
| Fuqaro xavfsizligi | 16,512 | 16,512 | 0 |
| Qo‘shimcha amaliy talablar | 62,108 | 62,079 | -29 |
| Qo‘shimcha FDP | 17,805 | 17,907 | +102 |
| Ilg‘or signallar | 4,538 | 4,538 | 0 |
| Kichik signallar | 6,413 | 6,449 | +36 |
| Signal reyestri | 2,734 | 3,019 | +285 |
| Tarixiy ishchi hujjat | 43,826 | 43,800 | -26 |
| **Jami** | **899,425** | **898,199** | **-1,226** |

Mutlaq farqlar yig‘indisi 2,294 belgi. `chars` maydonining hisoblash qoidasi (bo‘sh joy, satr oxiri, jadval kataklari, Unicode normalizatsiyasi) hujjatlashtirilmagan. Shu sababli farqlar mazmun yo‘qolganining isboti emas; ular qayta hisoblash va item-level crosswalk uchun ochiq nomuvofiqlikdir.

## 7. Alohida muallif yozuvlari

Yetti `author_profile_records.json` yozuvi ZIP-1 hujjat yozuvlariga qo‘shilmasdan alohida qatlamda yuritilishi kerak:

- `author_attestation` muallif tomonidan taqdim etilgan materialga asoslangan;
- `independent_review=not_reviewed`;
- `access_scope` muallif savoli yoki loyiha falsafasi savoli bilan cheklangan;
- `source_status`, `source_version`, `language` va `privacy_scope` maydonlari yetishmaydi.

Ushbu yetishmayotgan maydonlar taxmin bilan to‘ldirilmaydi. Yangi sxemaga o‘tkazishda cheklangan ko‘rik holatida qoladi. Muallif tasdig‘i ekspert tekshiruvi deb talqin qilinmaydi.

## 8. Keyingi majburiy tekshiruv

Asl ZIP-1 qayta mavjud bo‘lgach:

1. PPTX 17 slaydning har biriga slayd raqami, matn, rasm/diagramma lokatori va SHA-256 bog‘lash.
2. 6 PNGni fayl nomi, bayt hajmi, SHA-256, tasvir tavsifi va tegishli slayd/bo‘lim bilan bog‘lash.
3. Yetti DOCXning barcha 895 source itemini original paragraf/jadval lokatorlari bilan qayta inventarizatsiya qilish.
4. Har bir source itemni candidate chunk(lar)ga item-by-item bog‘lash; bir nechta locator bir chunkda bo‘lsa, to‘liq locator ro‘yxatini saqlash.
5. Hech qaysi chunkda aks etmagan itemlarni asl matni bilan alohida qayd etish.
6. PDF sahifalaridagi ko‘p chunkli holatlarda chunk matni va sahifa oralig‘ini tekshirish; jadval va diagramma kontekstini vizual tasdiqlash.
7. Ikki manifestdagi `chars` hisoblash algoritmini bir xil qoidaga keltirib, checksumni asl baytlardan qayta hisoblash.
8. Har bir o‘zgarish uchun source ID, original locator, candidate ID, status va reviewer qarorini merge ledgerga yozish.

**Hozircha hech qanday canonical merge, delete, KB import yoki Android kod o‘zgarishi bajarilmaydi.** Near-duplicate va contradiction ko‘riklari ham ochiq qoladi.

## 9. Xulosa

Audit batchda 13 ta PDF/DOCX manbadan 1,449 chunk va alohida author archive’dan 7 yozuv borligi qayta tasdiqlandi. ZIP-1 inventaridagi PPTX 17 slayd candidate JSONL’da ifodalanmagan. Yetti DOCX bo‘yicha 895 source item va 703 chunk o‘rtasida 192 birlik locator mapping farqi mavjud; bu mazmun yo‘qolganini isbotlamaydi, lekin to‘liq provenance crosswalk yo‘qligini ko‘rsatadi. 13 manba bo‘yicha oldingi va candidate char-countlar orasida net -1,226 farq bor, hisoblash qoidasi noma’lum.

**Integratsiya sharti bajarilmagan.** Asl manbalar bilan crosswalk, dublikat/ziddiyat ko‘rigi va mazmun saqlanganini isbotlovchi merge ledger tugamaguncha bilimlar bazasi hamda ishlaydigan APK kodi o‘zgartirilmaydi.
