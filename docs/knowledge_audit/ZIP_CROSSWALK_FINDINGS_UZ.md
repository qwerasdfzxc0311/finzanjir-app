# FINZANJIR — ZIP manbalari chuqur auditi (oraliq hisobot)

**Sana:** 2026-11-09  
**Branch:** `finzanjir-knowledge-audit-2026-11`  
**Maqom:** audit natijasi; bilim integratsiyasi hali bajarilmadi.

## 1. O‘zgarmas talab

Asl manbalar qisqartirilmaydi yoki almashtirilmaydi. Yangi bilim yozuvlari manbaga bog‘langan hosila yozuvlar bo‘ladi. Bir xil mazmun takror uchrasa, manba havolalari birlashtiriladi, ammo turli kontekst, versiya, tasdiq holati yoki qarama-qarshi mazmun o‘chirilmaydi. Audit tugamaguncha faol Android bilim bazasi va ilova kodi o‘zgartirilmaydi.

## 2. ZIP-1 — manbalar inventari

Arxivda 20 ta element bor: 14 ta hujjat va 6 ta rasm/brend materiali. Tekshirilgan hujjatlar:

| Manba | Hajm / tarkib | Dastlabki holat |
|---|---:|---|
| FINZANJIR KONSEPSIYA V14 | PDF, 164 sahifa | Asosiy konsepsiya; sahifa matni va vizual obyektlar alohida tekshiruvga muhtoj |
| 16 qatlam chuqur tushuntirish V3 | DOCX, 305 paragraf, 3 jadval / 24 qator | Qatlamlarning maqsadi, chegarasi, xato holati, test va ustuvorliklari |
| 16 qatlam talablar va sinovlar reyestri V1 | PDF, 4 sahifa | REQ-001…REQ-024, TEST-001…TEST-024, DEC-01…DEC-10 |
| Signal reyestri V1 | DOCX, 4 jadval / 19 qator | 15 asosiy signalga oid reyestr va eski risk qoidalari |
| Kichik signallar | DOCX, 72 paragraf, 1 jadval | 10 ta ikkilamchi signal; misollar amaldagi tasdiqlangan qoida emas |
| Ilg‘or signallar | DOCX, 46 paragraf | 6 ta ilg‘or signal; kelajak/2.0 va ruxsat talab qiluvchi imkoniyatlar |
| Qo‘shimcha amaliy talablar | PDF, 19 sahifa | Mundarijadagi 1–18 bo‘limdan tashqari 18–36 kengaytirilgan bo‘limlar ham mavjud |
| Qo‘shimcha FDP ishchi nusxasi | DOCX, 144 paragraf, 3 jadval / 25 qator | Kuzatuv, eshitilgan da’vo, gipoteza, taklif va tekshirish zarurati ajratilgan |
| Fuqaro xavfsizligi FDP | DOCX, 186 paragraf | Fuqaro ilovasi, hamkor bank kartalari, “Men bu kartani tanimayman”, vakolatlar va Case |
| False-positive ekspertiza tuzatishi V2 | DOCX, 52 paragraf | Shadow mode, canary, circuit breaker/karantin, kill switch, rollback, inson/bank nazorati |
| Bank integratsiyasi texnik arxitekturasi V1.0 | PDF, 66 sahifa | Taklif etilgan API, xabar, autentifikatsiya, idempotency, retry, audit, xavfsizlik va tiklash |
| AI va bilim tizimi — 5 hujjat | PDF, 29 sahifa | AI ichki oqimi, KB/memory, mustaqil baholash, xato tuzatish, xavfsizlik |
| FINZANJIR taqdimoti | PPTX, 17 slayd | Qisqa taqdimot; mustaqil texnik manba emas, konsepsiya chegaralarini ko‘rsatadi |
| Tarixiy ishchi hujjat | PDF, 22 sahifa | Tarixiy/arxiv qatlamida saqlanadi; faol FINZANJIR mazmuniga avtomatik qo‘shilmaydi |

### Muhim topilmalar

- 16 qatlam reyestrida 24 talab va 24 test identifikatori, shuningdek 10 ochiq qaror mavjud. Bu testlar bajarilgan degani emas.
- Qo‘shimcha amaliy talablar PDF’ida mundarija 18 bandda tugaydi, lekin hujjat 36-bandgacha davom etadi. 19 sahifani to‘liq import qilmasdan faqat mundarijadan nusxa olish katta mazmun yo‘qotishiga olib keladi.
- 16 qatlam DOCX’ida “qatlamning amalda mavjudligi hujjat bilan tasdiqlanmagan” degan ehtiyot bayonoti 16 marta takrorlangan. Bu tasodifiy dublikat emas: har bir qatlamning o‘z kontekstida takrorlangan himoya izohi; har bir qatlam bilan saqlanishi kerak.
- Signal hujjatlaridagi ball va bloklashga o‘xshash misollarni faol avtomatik qoida deb qabul qilmaslik kerak. False-positive V2 hujjati operatsion xavfsizlik bo‘yicha keyingi tuzatish sifatida alohida bog‘lanadi; eski matn arxiv/versiya sifatida qoladi.
- Taqdimotdagi “Silent Hold” ifodasi bank vakolatiga zid talqin qilinishi mumkin. Aniq huquqiy/operatsion qaror bo‘lmaguncha bloklash yoki to‘lovni ushlab qolish funksiyasi sifatida talqin qilinmaydi.
- V14 ichidagi SINBAD/ATMOS tilga olingan bo‘lim faol FINZANJIR bilimlar to‘plamiga qo‘shilmaydi; manbaning o‘zi arxivda saqlanadi.
- Muallifning shaxsiy profil/aloqa ma’lumotlari ommaviy AI qidiruviga avtomatik chiqarilmaydi. Mualliflik hissasi va shaxsiy ma’lumotga kirish alohida boshqariladi.

## 3. ZIP-2 — V317 arxivi va indeks auditi

Tekshirilgan arxiv tarkibi:

- 224 fayl.
- `unified_candidate_cards_full_source.json`: 7,053 yozuv.
- V317 ZIP-2 arxividagi eski Android paket ichidagi `unified_knowledge_index.json`: 4,671 yozuv (joriy `finzanjir-android-v1` Kotlin/Compose APK indeksi emas).
- Ikki JSON ro‘yxatida ham takrorlangan ID topilmadi.
- Source archive’da normalizatsiya qilingan matn bo‘yicha 2 ta aynan takror guruh (jami 4 yozuv) aniqlandi: “Risk Engine nima” va “Fraud Graph nima” juftlari.
- Active index’da 3 ta aynan takror guruh (jami 6 yozuv) aniqlandi: population, migration va cloud ifodalarining takrorlari.
- Source archive va active index o‘rtasida 2,213 ta normalizatsiya qilingan matn mosligi bor; 3,276 ta ID ikkala ro‘yxatda ham uchraydi. Bu import/hosila aloqalarini ko‘rsatadi, ammo barcha 4,671 yozuvning hammasi kerak yoki to‘g‘ri degani emas.
- Active index’dagi metadata to‘liqligi notekis: 860 yozuvda `kind/authority/approval/language` maydonlari yo‘q; 1,070 yozuv `unclassified_knowledge_record`; 540 domain `unclassified`; 1,681 til `und`.
- Active index’da 515 umumiy ensiklopediya yozuvi bor; ular FINZANJIR maxsus firibgarlik/bank qoidalari bilan aralashtirilmaydi.
- 2,000 regression savol/tarix yozuvlari test korpusi bo‘lib qoladi, faol javob bilimiga ko‘chirilmaydi.
- V317 active indexida `domain=finzanjir` bo‘lgan 188 yozuv qayd etilgan. Bu 188 yozuvning `kind`, `approval` va `authority` taqsimoti aralash; ularni 188 ta `authoritative_project_source` deb atash hozirgi audit dalillari bilan tasdiqlanmaydi. Field semantikasi bo‘yicha 2026-11-16 qo‘shimcha tekshiruvni ushbu hujjatning 10-bo‘limiga qarang.
- 15 `verified_source_candidate` huquqiy matn yozuvi ham amaldagi huquqiy maslahat sifatida berilishidan oldin rasmiy manbada qayta tekshirilishi kerak.

## 4. ZIP-1 va ZIP-2 o‘rtasidagi dublikat siyosati

Dublikatlarni uch darajada ajratamiz:

1. **Aynan bir xil matn:** bitta canonical bilim yozuvi, barcha source ID/path/page/section havolalari saqlanadi.
2. **Mazmunan yaqin, lekin konteksti/versiyasi farqli:** yozuvlar o‘chirilmaydi; `related_to`, `supports`, `contradicts` yoki `supersedes` aloqasi bilan bog‘lanadi.
3. **Zid yoki keyin tuzatilgan mazmun:** ikkala manba ham saqlanadi; qaysi biri keyingi tuzatish, qaysi biri eski taklif ekani status va sana bilan ko‘rsatiladi. Avtomatik ravishda “eng yangi”ni haqiqat deb qabul qilinmaydi.

## 5. Android’dagi hozirgi import bilan solishtirish

Android branch manifestida 1,121 yozuv ko‘rsatilgan: 957 V4 korpus yozuvi + V14 PDF’ning 164 sahifa yozuvi. Barcha yozuvlar `candidate_not_authoritative`. ZIP-1’dagi alohida FDP, signal, 16 qatlam, texnik arxitektura va 5 AI hujjatining to‘liq manba matni alohida-alohida import qilingani tasdiqlanmadi. V317’dagi 4,671 yozuv ham Android branchga to‘liq integratsiya qilinmagan.

Manifestdagi `branch` maydoni `finzanjir-v4-unified-workflow-uz` deb turibdi, holbuki tekshirilayotgan Android branch `finzanjir-android-v1`. Bu metadata xatosi sifatida qayd etildi; hozircha tuzatilmaydi.

## 6. Keyingi bajariladigan ishlar

1. Har bir PDF sahifasidagi jadval/diagramma/rasmni vizual tekshirish va sahifa identifikatorini saqlash.
2. Har bir DOCX paragrafi va jadval qatorini source ID bilan inventarizatsiya qilish.
3. ZIP-1 manbalarini Android 1,121 yozuvi, V317 4,671 indeks va 7,053 source archive bilan item-by-item solishtirish.
4. Exact duplicate, near duplicate, contradiction va supersession reyestrlarini tayyorlash.
5. Asl hujjatlar uchun o‘zgarmas source snapshot, hosila knowledge chunks va crosswalk formatini yaratish.
6. Manba to‘liqligi va checksum nazoratidan keyingina alohida integratsiya rejasini ko‘rsatish.

**Hisobot yakuniy integratsiya emas. Bu hisobotdagi sanash va dublikat tahlili matn/JSON darajasidagi tekshiruvdir; PDF rasmlari, murakkab jadvallar va semantik dublikatlar hali alohida ko‘rik talab qiladi.**


## 7. V14 vizual sahifalarini tanlab ko‘rish

PDF ichidagi sahifa rasmlari alohida ko‘rildi; oddiy matn ekstraksiyasi bilan cheklanilmadi.

- 20–23-sahifalarda eski Android prototip ekranlari tasvirlangan: Dashboard, “Mening kartalarim”, xavf tahlili, History, ilova xavfsizligi skaneri, ogohlantirishlar, AI yordamchi va Demo Report. 23-sahifadagi izoh bu ekranlardagi ma’lumotlar demo/sintetik ekanini va real bank API/Production integratsiyasi ishlayotganini anglatmasligini ochiq aytadi. Ular konsepsiya va UX namunalari sifatida saqlanadi, joriy APK funksiyasi deb qabul qilinmaydi.
- 24-sahifa Android prototipining o‘rni va chegarasini tushuntiradi; Identity Risk/Identity Assurance kabi yo‘nalishlar ham mavjud APK’da to‘liq implementatsiya qilingan deb da’vo qilinmaydi.
- 78–79-sahifalarda API data contract jadvali va Prototype → MVP → Pilot → Production farqlari bor. Bu jadvalni alohida strukturali bilimga aylantirish kerak; har bir bosqichning dalil va qabul sharti saqlanishi lozim.
- 95–96-sahifalarda KPI manbalari va namunaviy Risk Score arifmetikasi ko‘rsatilgan. 96-sahifadagi 70/100 misoli Production modeli emasligi, real og‘irliklar pilot ma’lumotlari va ekspert validatsiyasidan keyin belgilanishi matnda qayd etilgan. Shuning uchun bu misol faqat tushuntiruvchi namuna sifatida indekslanadi.
- 141-sahifada vizual chizma/drawing obyektlari mavjud; ushbu va boshqa diagrammali sahifalar alohida sahifa tasviri bilan qayd qilinishi kerak.

**Vizual tekshiruv cheklovi:** V14 va texnik arxitektura PDF’larida sahifa resurslarida takrorlanuvchi rasmlar mavjud; sahifadagi image-resource soni mustaqil diagrammalar soni emas. Diagramma va jadvallarni sahifa renderi, matn va kontekst bilan birga tekshirish kerak. Hozirgi ko‘rik tanlangan sahifalar bilan cheklangan; barcha 164 sahifa vizual tasdiqdan o‘tdi deb aytilmaydi.

## 8. Dublikat bo‘yicha aniq saqlash qoidasi

- 16 qatlam hujjatidagi bir xil himoya jumlasi 16 qatlamning har birida kontekstli takrorlangan; bu mazmuniy dublikat bo‘lsa ham, qatlamdan uzib tashlanmaydi.
- Signal hujjatlaridagi muallif satrining takrorlanishi metadata, bilim mazmuni emas.
- V317 source archive’dagi “Risk Engine nima” va “Fraud Graph nima” ikki juft yozuvi aynan takrorlangan. Canonical javob yozuvi yaratilsa, ikkala original ID/source relation saqlanadi.
- Active index’dagi population, migration va cloud ifodalarining uch juft takrori til/domain alias yozuvlari bo‘lishi mumkin; ularni faqat mazmun, til va routing vazifasi tekshirilgandan keyin birlashtirish mumkin.
- ZIP-1’dagi hujjatlar orasidagi o‘xshash matnlar hali to‘liq semantik taqqoslanmagan. Shu sababli bu bosqichda ZIP-1 hujjatlararo “dublikat yo‘q” degan xulosa berilmaydi.

## 9. Integratsiyadan oldingi qabul mezonlari

1. Har bir manba fayli uchun checksum, hajm, sahifa/bo‘lim soni va manba ID bo‘lishi.
2. Har bir hosila yozuv kamida bitta aniq source locator (PDF sahifa, DOCX paragraf/jadval qatori, PPTX slayd yoki V317 record ID) bilan bog‘lanishi.
3. Exact duplicate merge qilinganda barcha original IDs va source locators saqlanishi.
4. Near duplicate yoki ziddiyatli yozuvlar inson ko‘rigisiz o‘chirilmasligi.
5. General encyclopedia, test dataset, author-only/private, historical/archive va FINZANJIR domain qatlamlari ajratilishi.
6. Author attestation, independent review, content type, record status va privacy/access scope mustaqil maydonlarda bo‘lishi.
7. Bilim soni kamaygan ko‘rinsa, merge ledger orqali oldingi yozuvlarning har biri qaysi canonical IDga bog‘langanini ko‘rsatish; manbasiz yo‘qolgan yozuv bo‘lmasligi.
8. Asl matn va hosila yozuvlar uchun hash/checksum hamda import hisoboti qayta tiklanadigan bo‘lishi.


**Aniqlik (2026-11-11):** ZIP-2 ichidagi 4,671 yozuvli `unified_knowledge_index.json` V317 paketining ichki indeksi. Uni joriy Kotlin/Compose Android APKning 1,121 yozuvli `knowledge_manifest.json` bilan bir xil korpus deb qabul qilmaslik kerak.


## 10. 2026-11-16 — V317 dagi 188 yozuv soni va authority field semantikasi

### Tekshiruv doirasi

Ushbu qo‘shimcha faqat audit branchidagi mavjud ikki hujjatni o‘zaro solishtiradi:

- `V317_FINZANJIR_DOMAIN_AUDIT_UZ.md` (Git blob SHA: `b1b129a9e816547f4bda24de2af07c330be4a004`);
- ushbu `ZIP_CROSSWALK_FINDINGS_UZ.md` faylining oldingi 3-bo‘limi.

Asl ZIP-2 va uning xom JSON fayllari ushbu yugurishda mavjud emas. Shu sababli bu field-level raw-data audit emas, mavjud audit artefaktlari o‘rtasidagi son va atama reconciliation hisoblanadi.

### Mavjud audit dalillaridagi 188 sonining ma’nosi

V317 domen auditi 188 yozuvni **active index ichida `domain=finzanjir` bo‘lgan yozuvlar** sifatida ta’riflaydi. Shu hujjatdagi taqsimotlar:

- `kind`: 14 ta kategoriya; yig‘indisi 188;
- `approval`: candidate 134, unclassified 40, author_confirmed_project_philosophy 10, author_visible_on_direct_request 4; yig‘indisi 188;
- `authority`: candidate_learning 75, source_unclassified 40, source_derived_candidate 33, author_provided 14, model_generated_candidate 10, index_metadata 8, project_source_synthesis 5, source_derived_or_architecture_candidate 3; yig‘indisi 188.

Demak, V317 domen auditidagi 188 yozuv bir xil maqomdagi authoritative bilimlar emas. Masalan, 134 ta approval candidate, 40 ta unclassified; authority bo‘yicha esa faqat 14 ta yozuv author_provided deb qayd etilgan. Muallif taqdim etganlik ham mustaqil ekspert yoki bank tasdig‘i degani emas.

### Nomuvofiqlik va ehtiyotkor talqin

Ushbu faylning avvalgi 3-bo‘limida 188 yozuv `authoritative_project_source` turidagi yozuvlar deb atalgan. Biroq V317 domen auditining ko‘rsatilgan `kind` ro‘yxatida bunday kategoriya yo‘q; 188 soni esa `domain=finzanjir` filtri bo‘yicha berilgan. Bu ikki atama bir xil field yoki bir xil selection predicate ekanini mavjud hujjatlar isbotlamaydi.

**Hozirgi xavfsiz talqin:** 188 — V317 active indexidagi FINZANJIR-domain yozuvlari soni (avvalgi audit hujjatida qayd etilgan). Uni 188 ta `authoritative_project_source`, 188 ta ekspert tasdiqlagan bilim yoki 188 ta ZIP-1 manbasiga bog‘langan yozuv deb ishlatmaslik kerak. Field nomi yoki count scope xatosi bo‘lishi mumkin; asl ZIP-2 JSON tekshirilmaguncha bu nomuvofiqlik `unresolved_count_field_semantics` holatida qoladi.

### Xom ZIP-2 qayta mavjud bo‘lgach bajariladigan tekshiruv

1. `unified_knowledge_index.json` va `unified_candidate_cards_full_source.json` ichidagi barcha yozuvlarni raw JSON bo‘yicha qayta o‘qish.
2. `domain=finzanjir`, `kind`, `type`, `authority`, `approval`, `source_status` maydonlarini alohida sanash; null/missing qiymatlarni alohida ko‘rsatish.
3. 188 count qaysi field/predicate bilan hosil bo‘lishini qayta bajariladigan skript va input checksum bilan tasdiqlash.
4. 188 domain yozuvini original ID bo‘yicha ZIP-1 source units va Android 1,121 manifest yozuvlari bilan alohida crosswalk qilish.
5. Muallif-only, test-only, model-generated, general-encyclopedia va historical yozuvlarni FINZANJIR active knowledge qatlamidan ajratilgan holda saqlash.

### Qaror

Hech qanday V317 yozuvi o‘zgartirilmadi, o‘chirilmadi yoki birlashtirilmadi. ZIP-1/ZIP-2 source ma’lumotlari va Android APKga import qilinmadi. 2,000 regression savol/test yozuvlari test-only bo‘lib qoladi. Integratsiya bloklangan holatda.


## 11. 2026-11-17 — asl ZIP manbalari mavjudligi va branch ancestry tekshiruvi

### Manba mavjudligi tekshiruvi

Ushbu yugurishda Library ichidagi ZIP turidagi fayllar ro‘yxati to‘liq sahifalandi: **95 ta ZIP** qaytdi, keyingi sahifa cursor’i qolmadi. Quyidagi ikki aniq nom ro‘yxatda topilmadi:

- `Finzanjir konsepsiyasi va qoshimsha malumotlar hujjatlar (1).zip` — ZIP-1 sifatida avval qayd etilgan;
- `FINZANJIR_V317_SEMANTIC_GATE_PLUS_DOMAIN_EXPANSION.zip` — ZIP-2 sifatida avval qayd etilgan.

Aniq nom bo‘yicha Library qidiruvi ham mos asl arxivni qaytarmadi. Library’da boshqa ko‘plab FINZANJIR ZIP arxivlari bor, jumladan `Finzanjir vlar joylangan.zip`; lekin ularning hech biri ZIP-1 yoki ZIP-2 o‘rniga qabul qilinmadi. Fayl nomi o‘xshashligi yoki FINZANJIR mavzusi bir xil manba ekanini isbotlamaydi.

Suhbat fayllari ro‘yxatida `FINZANJIR_BILIM_AUDIT_BATCH_2026-11-09.zip` nomli audit hosila paketi ikki marta ko‘rinadi. Ikkala file reference uchun ham `files.materialize` xizmati “downloadable backing file yetarli emas” deb qaytardi. Joriy ishchi konteynerda ham asl ZIP yoki audit ZIP baytlari mavjud emas. Shuning uchun ushbu yugurishda oldingi audit paketining ZIP CRC, SHA-256, JSONL sonlari va matn hajmlari xom baytlar asosida qayta hisoblanmadi. Oldingi hisobotlardagi sonlar tarixiy audit natijalari bo‘lib qoladi; ular bugungi yangi checksum tekshiruvi sifatida ko‘rsatilmaydi.

### GitHub branch ancestry va chegaralar

- Audit branch HEAD ushbu tekshiruvda `74cc04aa672205142909445f19e88e174757dba3` commitiga **identical** deb tasdiqlandi.
- `finzanjir-android-v1` bilan compare: audit branch **31 commit oldinda, 0 commit ortda**; 14 ta branchlararo faylning barchasi `docs/knowledge_audit/` ichida.
- `finzanjir-v3-synthetic-ai-uz` va `finzanjir-v4-unified-workflow-uz` bilan compare natijalarida Android app fayllari ham ko‘rinadi. Bu u branchlar bilan tarixiy base/ancestry farqidir; audit branchning Android’dan keyingi delta ro‘yxatiga app fayllari kirmaydi. Bu yugurishda V3/V4 branchlariga yozuv kiritilmadi.
- `main` bilan compare branchlar tarixining ajralganini ko‘rsatadi: audit branch common base’dan keyin o‘z yo‘nalishida, `main` esa audit branchga kirmagan ikki commitga ega. `main` dagi `948827beb0cac8a7910d7ccd8b2cfcfe5a8cec50` commit eski “5,607 yozuvli migratsiya auditi” faylini qo‘shgan, `7023a858746ce1b0d1c17df9288fdc25d09d3f4f` esa uni main’dan olib tashlagan. Bu tarixiy audit nusxasi joriy tasdiqlangan ZIP-1/ZIP-2 manbasi yoki faol integratsiya dalili emas. Undagi BM25 va 5,607 yozuv haqidagi da’volar ushbu auditda qayta tasdiqlanmadi va APKga ko‘chirilmaydi.

### Qaror va keyingi ish

1. ZIP-1/ZIP-2 o‘rniga boshqa arxiv tanlanmaydi.
2. Asl ikki arxiv qayta mavjud bo‘lmaguncha ularning checksumlari, ichki fayl ro‘yxati, sahifa/paragraf/jadval/slayd lokatorlari va item-by-item crosswalk tekshirilgan deb aytilmaydi.
3. Audit hosila ZIP ham raw bytes bilan qayta olinmaguncha uning avvalgi hash/count qiymatlari faqat oldingi hisobotga tegishli deb belgilanadi.
4. Main branchdagi tarixiy migratsiya auditi alohida tarixiy artefakt bo‘lib qoladi; undan kod, BM25, yozuvlar yoki approval holatlari ko‘chirilmadi.
5. Hech qanday bilim birlashtirilmadi/o‘chirilmadi; APK, Android assetlari, V3, V4 va main o‘zgartirilmadi.

**Natija:** bugungi tekshiruv manba mavjudligi va Git branch ancestry auditidir. U ZIP-1/ZIP-2 mazmunini qayta tekshirgan hisoblanmaydi; merge ledger hali tayyor emas, integratsiya bloklangan.
