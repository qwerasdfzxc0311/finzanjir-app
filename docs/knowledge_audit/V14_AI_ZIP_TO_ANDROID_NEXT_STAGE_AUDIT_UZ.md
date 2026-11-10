# FINZANJIR V14 + AI ZIP + 5,607 migratsiya → Android keyingi bosqich auditi

Sana: 2026-11-10  
Audit branch: `ai-core-lightweight-fts4-2026-11-10`  
Asosiy konsepsiya: `FINZANJIR_KONSEPSIYA_V14.pdf` (15 bob)  
Audit turi: manba ZIPlari va joriy Android branchining statik crosswalk auditi. Bu telefon runtime, bank sandbox yoki mustaqil ekspert auditi emas.

## 1. Tekshirilgan manbalar

### ZIP-A — konsepsiya va qo‘shimcha hujjatlar
Arxivda 14 ta hujjat va 6 ta brend/rasm materiali bor. Asosiy hujjatlar:
- FINZANJIR V14 — 15 bobli asosiy konsepsiya.
- 16 qatlam chuqur tushuntirishi V3.
- 16 qatlam talablar va sinovlar reyestri V1.
- Bank integratsiyasi, xavfsizlik va avtomatlashtirish texnik arxitekturasi.
- FINZANJIR AI va bilim tizimi — 5 hujjat birlashtirilgan.
- Qo‘shimcha amaliy talablar — 36 bo‘limgacha davom etadigan PDF.
- Fuqaro xavfsizligi FDP.
- False-positive/ekspertiza tuzatishi V2.
- Signal reyestri, kichik signallar va ilg‘or signallar.
- Qo‘shimcha FDP ishchi nusxasi, tarixiy ishchi hujjat va 17 slaydli taqdimot.

### ZIP-B — AI v2.1 source package
Tekshirilgan asosiy fayllar:
- `android_app/app/src/main/assets/core/unified_core.js` — Router, intent, til, retrieval, evidence gate, answerability, safety, synthesis, ixtiyoriy local model/provider.
- `knowledge/unified_knowledge_index.json` — faylning o‘zida 4,656 JSON yozuv bor.
- `memory/five_part_memory_vault.js` — 5 asosiy xotira × 5 ichki qatlam.
- `LocalModelBridge.kt` — ixtiyoriy Qwen3-0.6B/LiteRT-LM, hujjat importi, ovoz, gateway va backup funksiyalari uchun native bridge.
- `MemoryStore.kt` — SQLite xotira, hujjat fingerprintlari va backup merge.
- `index.html` — til tanlash, sodda/ekspert javobi, qisqa/o‘rta/chuqur uzunlik, ovozli savol, fayl importi, javobni to‘xtatish, lokal model, ZIP backup/restore va ixtiyoriy HTTPS gateway UI.
- `UNIFIED_MASTER_RULES_UZ.md` va verification testlari.

**Manba paketi bo‘yicha metadata nomuvofiqligi:** `ASSET_MANIFEST.json` 3,796 yozuv deydi; `README_UZ.md` va `SOURCE_STATUS.json` 3,281 yozuv deydi; ZIP ichidagi JSON faylning real element soni esa 4,656. SHA-256 qiymatlari ham manifest/status bilan mos kelmaydi. Shu sabab eski manifestdagi 3,281 yoki 3,796 sonini haqiqiy aktiv son deb qabul qilmaslik kerak; yangi migratsiya 4,671 V317 yozuvini alohida manba sifatida olib, 5,607 candidate korpusni qayta tuzgan.

### ZIP-C — 5,607 yozuvli bilim migratsiyasi
Tarkib:
- 4,671 V317 manba yozuvi;
- 893 yangi hujjat bo‘lagi;
- V4-L01…V4-L16 bo‘yicha 16 qatlam yozuvi;
- 27 OCR candidate yozuvi;
- jami 5,607; takroriy ID yo‘q.
- 27 OCR yozuvi va yangi hujjat bo‘laklari ekspert tekshiruvisiz authoritative emas.
- Migratsiya model fine-tuning emas; bu source-preserving knowledge import.
- Candidate asset SHA-256: `f3457b372c5e7f79a0875603cb33987a7720f96061c1ac23ea038b69f2dfb250`.

## 2. Manbalar o‘rtasidagi ustuvorlik va muhim ziddiyatlar

1. **V14 — asosiy konsepsiya.** U 15 bobli strategik va funksional asos bo‘lib qoladi. Qo‘shimcha FDP/texnik hujjatlar uni almashtirmaydi.
2. **16 qatlam — cross-cutting nazorat arxitekturasi.** Ular 16 ta mustaqil ekran yoki 16 ta allaqachon ishlaydigan modul emas. Har qatlamning maqsadi, kirish/chiqishi, vakolat chegarasi, xato holati, test va dalili bor.
3. **Eski signal reyestri va False Positive V2 o‘rtasida amaliy ziddiyat bor.** Eski signal reyestrida ayrim kombinatsiyalar avtomatik Case ochishi va yuqori ball berishi yozilgan. Keyingi False Positive V2 esa ommaviy noto‘g‘ri signal xavfi sabab shadow mode, blast-radius cheklovi, kill switch, karantin, rollback va bank/inson nazoratini talab qiladi. Eski qoida matni faol production qoida sifatida ko‘chirilmasin; yangi xavfsizlik talablari bilan ekspertlar tasdiqlaydigan candidate rule sifatida saqlansin.
4. **“Aqlli Jimjitlik” bloklash vakolati emas.** U bankning o‘z vakolatli himoya tekshiruviga yo‘naltirish konsepsiyasi. FINZANJIR o‘zi pulni ushlab qolmaydi, kartani bloklamaydi yoki tranzaksiyani rad etmaydi.
5. **Signal ≠ firibgarlik isboti; Risk ≠ aybdorlik; Graph aloqasi ≠ aybdorlik; Case ≠ hukm.**
6. **SINBAD/ATMOS** V14dagi maxsus tarixiy/tadqiqot yo‘nalishi sifatida alohida saqlanadi; ularni tekshirilmagan faol antifraud qoidalariga avtomatik qo‘shmaslik kerak.
7. **ReCAL** ko‘rib chiqilgan asosiy hujjatlarda mustaqil, to‘liq spetsifikatsiyalangan modul sifatida belgilanmagan. Qayta kalibrlash (risk/model recalibration) L05/L13/L16 bilan bog‘liq boshqariladigan jarayon sifatida ishlab chiqilishi mumkin; uni FIN-RECOVERY bilan aralashtirmaslik kerak.
8. **Mualliflik va ekspert tasdig‘i ikki xil.** Muallif tasdiqlashi loyiha manbasi/qarashi uchun; bank, huquqiy, xavfsizlik va mustaqil ekspert tasdig‘i esa o‘z vakolatiga tegishli.

## 3. Joriy Android branchining haqiqiy holati

Branch: `ai-core-lightweight-fts4-2026-11-10`

### Hozir kodda bor
- Jetpack Compose Android ilovasi.
- Bosh sahifa, Jarayon, Signallar, 16 qatlam, Case, Human Review, AI yordamchi, Cheklovlar bo‘limlari.
- Lokal SQLite FTS4 qidiruv indeksi; BM25, embedding, vector DB va majburiy model yuklash yo‘q.
- JSON oqimli import, asset SHA-256 va manifest yozuv soni tekshiruvi.
- O‘zbek lotin/kirill normalizatsiyasi va qoraqalpoqcha uchun dastlabki transliteratsiya, sinonim/alias va qo‘shimcha qoidalari.
- Bir nechta qidiruv passidan kelgan nomzod yozuvlarni ID bo‘yicha birlashtirish; manba, versiya, bo‘lim, fayl yo‘li va approval maqomini ko‘rsatish.
- Ehtimoliy ziddiyatlar uchun oddiy polarity/lexical heuristic.
- Fuqaro/Mutaxassis javob rejimi; bu UI filtri, autentifikatsiya yoki RBAC emas.
- Query va birinchi import Compose UI threadidan tashqarida bajariladi.

### Hozircha statik yoki yo‘q
- Signallar, Case, Human Review va 16 qatlam sahifalari hozir asosan statik `InfoList`; ular umumiy ma’lumotlar bazasiga ulangan real ish jarayoni emas.
- Case yaratish, tahrirlash, biriktirish, ko‘rib chiqish qarori, eskalatsiya va yopishning persistent state machine’i yo‘q.
- Timeline/History, Evidence/Counter-evidence, Cross-Match, Fraud Graph, Risk Engine, FIN-RECOVERY, Mening kartalarim, FINZANJIR ID, Anti-Phishing, App Scanner, Credit/Payment Verification, Antifraud Exchange va Demo Reportning to‘liq interaktiv implementatsiyasi yo‘q.
- 16 qatlam uchun REQ/TEST/EVIDENCE/DEFECT/CHANGE izchilligi UI va ma’lumotlar modelida yo‘q.
- 5×5 memory vault, suhbat xotirasi, hujjat xotirasi, candidate learning, archive/version/rollback, original fayl importi, PDF/DOCX/PPTX/EPUB parsing, OCR, ovoz, lokal LLM, javobni to‘xtatish va ZIP backup/restore hozirgi Compose branchga ulanmagan.
- Original `unified_core.js` Kotlin Compose branchga integratsiya qilinmagan. Hozirgi javob tuzuvchi deterministic/extractive; u generativ LLM emas.
- 5,607 yozuvli asset hali aktiv Android assetiga joylanmagan. Hozirgi aktiv Android JSON 1,121 yozuv.
- Qoraqalpoqcha til aniqlash va morfologiya birinchi bosqich; to‘liq dialekt/yozuv qamrovi yo‘q.

### Hozirgi branchdagi qidiruv yadrosi uchun aniqlangan texnik qarz
- FTS4 so‘rovlari SQL `LIMIT` bilan keladi, ammo qidiruv natijasini SQL qatlamida deterministik relevance tartibida bermaydi; keyingi Kotlin score faqat olingan nomzodlar ustida ishlaydi.
- Matni bir xil yozuvlar `distinctBy(normalize(text))` bilan bir javob tanlovida qisqarishi mumkin; turli manba provenance’larini yo‘qotmaslik uchun duplicate text va multi-source citation alohida saqlanishi kerak.
- Ziddiyat aniqlash ijobiy/inkor so‘zlari va lexical overlapga tayanadi; semantik ziddiyatni ishonchli hal qilmaydi.
- “Muallif” so‘rovi uchun kalit so‘zlar juda keng; “asoschi” yoki “author” so‘zi boshqa kontekstda kelganda noto‘g‘ri author route bo‘lishi mumkin.
- `confidence` nomli maydon hozir kalibrlangan ishonch emas, qidiruv mosligi yorlig‘ini qaytaradi. UI’da “moslik holati” deb atalishi kerak; foiz yoki ehtimollik sifatida ko‘rsatilmasin.
- Til aniqlashda qoraqalpoq/kazakh kirill belgilarining kesishishi, qisqa so‘rovlar, aralash til va imlo xatolari bo‘yicha gold testlar yo‘q.

### Build holati
- Eng so‘nggi branch commit: `21d0ffa1e67c71f82d0050a30dcc17dd71dc4d37`.
- GitHub Actions Android build: PASS; workflow run `42687825829`.
- Python prototype tests: PASS; workflow run `42687836628`.
- Android debug artifact yaratilgan. Bu Gradle build muvaffaqiyatini tasdiqlaydi, lekin APK Samsung qurilmaga o‘rnatilgani, runtime, tezlik, xotira, batareya yoki funksional oqimlar tekshirilganini anglatmaydi.
- PR #3 Draft va merge qilinmagan.

## 4. Keyingi APK uchun maqsadli yagona arxitektura

Ilova bir nechta alohida demo ekranlardan iborat bo‘lib qolmasligi kerak. Barcha ekranlar yagona local data model/repository bilan ishlasin. Har bir obyekt barqaror ID va audit/timeline yozuviga ega bo‘lsin.

Tavsiya etiladigan asosiy obyektlar:
- `Event` — hodisa va uning manbasi;
- `Evidence` / `CounterEvidence` / `Unknown` — dalil, qarshi dalil va noma’lum jihat;
- `Signal` — indikator, qoida versiyasi, vaqt, manba va holat;
- `RiskAssessment` — izohlanadigan omillar, noaniqlik va model/rule versiyasi;
- `Entity` / `Relation` — fuqaro, karta tokeni, hisob tokeni, telefon, qurilma, IP, qabul qiluvchi, merchant, gateway va ular orasidagi manbali aloqa;
- `Case` — signal va dalillar bilan bog‘langan tekshiruv ishi;
- `ReviewDecision` — reviewer, vaqt, qaror, sabab va dalil havolalari;
- `RecoveryAction` — FIN-RECOVERY bo‘yicha murojaat/checklist/status; pulni o‘zi qaytarmaydi;
- `TimelineEntry` / `AuditEvent` — barcha o‘zgarishlar va foydalanuvchi/rol harakati;
- `RuleVersion` / `ModelVersion` — boshqariladigan qoidalar, tasdiq va rollback;
- `KnowledgeRecord` / `SourceDocument` — bilim yozuvi, original fayl, hash, sahifa/bo‘lim va approval.

### Bitta umumiy jarayon
`Event → Data Validation → Signal → Evidence/Counter-evidence/Unknown → Risk Explanation → Cross-Match → Fraud Graph → Case Candidate → Human Review → Authorized Outcome → FIN-RECOVERY coordination → Audit/Feedback → Candidate recalibration → test/approval`.

Biror bosqichda yetarli dalil bo‘lmasa, jarayon to‘xtaydi yoki qo‘shimcha ma’lumot kutadi; tizim uydirma dalil bilan keyingi bosqichga o‘tmaydi.

## 5. APKga qo‘shilishi kerak bo‘lgan funksiyalar

### A. Fuqaro ko‘rinishi
- Bosh sahifa: xavfsizlik holati, ogohlantirishlar, so‘nggi faoliyat va aniq demo/real status.
- FINZANJIR ID: faqat prototip identifikatori; real KYC/identity assurance deb ko‘rsatilmaydi.
- “Mening kartalarim”: `O‘zimniki / Tanimayman / Yo‘qotilgan`; faqat sintetik/masked karta. Real egalik faqat hamkor-bankning qonuniy tasdig‘i bilan.
- Karta bo‘yicha xavfsiz murojaat va rasmiy bank kanaliga yo‘naltirish; “bloklandi” faqat bank tasdig‘i bo‘lsa.
- Yagona ogohlantirish markazi: phishing, SMS, qo‘ng‘iroq, havola va ijtimoiy muhandislik bo‘yicha tushuntirish.
- App Scanner: ruxsatlar/konfiguratsiya xavfini ko‘rsatish; to‘liq antivirus deb ko‘rsatmaslik.
- History/Timeline, murojaat holati, FIN-RECOVERY yo‘riqnomasi va shikoyat/tuzatish yo‘li.
- AI fuqaro rejimi: sodda izoh, amaliy qadamlar, xavfsiz fallback.

### B. Mutaxassis ko‘rinishi
- Yagona Operations Dashboard va hodisalar navbati.
- Data Quality: schema, to‘liqlik, eskirish, dublikat, manba ishonchliligi.
- Signal Registry: signal qoidasi, versiya, source, test holati va false-positive xavfi.
- Explainable Risk Engine: indikatorlar, sabablar, qarshi dalillar, noma’lumlar va noaniqlik; demo ball ehtimollik emas.
- Cross-Match va Fraud Graph: faqat manbali aloqa; grafdagi bog‘lanish aybdorlik emas.
- Timeline: hodisa, signal, bank xabari, review va natija bir vaqt chizig‘ida.
- Case detail: dalillar, qarshi dalillar, unknown, consent scope, owner, status, SLA, bog‘liq signal/entity.
- Human Review: `tasdiqlash / rad etish / qo‘shimcha ma’lumot / qayta tekshiruv / eskalatsiya`; har qaror sabab va reviewer bilan auditga yoziladi.
- FIN-RECOVERY: hodisadan keyingi checklist, murojaat, bank javobi/ACK, status va hujjatlar; pul qaytarish kafolati yo‘q.
- 16 qatlam: har qatlamning maqsadi, input/output, vakolat chegarasi, xato holati, bog‘lanishi, REQ/TEST/EVIDENCE/DEFECT statusi.
- ReCAL/recalibration workbench: faqat candidate qoida/model o‘zgarishi, offline/synthetic test, shadow/canary natijasi va rollback; mustaqil tasdiqsiz faol qoida o‘zgarmaydi.
- Audit log, KPI/report, Test Lab, incident response va ma’lumotlar boshqaruvi.
- Mutaxassis ko‘rinishi muallifga maxsus bog‘lanmasin; lekin bu demo rejim production RBAC o‘rnini bosmaydi.

### C. AI va Knowledge Vault
- Asl `unified_core.js`dagi intent, context, Topic Router, author direct-request policy, safety, answerability, synthesis va optional local model yo‘llarini FTS4 retrieval bilan bog‘lash.
- BM25 chaqiruvlarini olib tashlash; FTS4 candidate retrieval ustidan yengil, deterministik, o‘lchanadigan ranker.
- Claim-level evidence: har bir javob da’vosi qaysi yozuv/manba/sahifa/versiyaga tayanganini ko‘rsatish.
- Multi-document synthesis: 2+ manba dalilini bitta javobga birlashtirish; qarama-qarshi manbalarni alohida ko‘rsatish.
- Source precedence: authoritative → verified official/current → candidate → historical/archive; maqom va sana ko‘rsatiladi, candidate hech qachon rasmiy faktga aylanmaydi.
- Safe answerability: savol noaniq, dalil kam, manba eskirgan yoki zid bo‘lsa, javobni cheklash.
- 5 til: o‘zbek, qoraqalpoq, qozoq, rus, ingliz; til/yozuv/sheva/typo/mixed-language/negation testlari alohida.
- Fuqaro va mutaxassis javob chuqurligi; qisqa/o‘rta/chuqur format.
- 5×5 memory vault: approved (AI uchun read-only), conversations, documents, learned candidates, archive; active/staging/index/versions/archive_handoff.
- Hujjat importi: original faylni o‘zgartirmasdan saqlash, SHA-256, parser/OCR, bob-bo‘lim-jadval-sahifa lokatorlari, candidate staging, duplicate/conflict/supersedes munosabatlari.
- Ovozli savol/javob, javobni to‘xtatish, optional local model va ixtiyoriy HTTPS gateway — faqat privacy/security reviewdan keyin. API kalit APKga joylanmaydi; gateway default o‘chiq.
- AI javobi, suhbat yoki user correction authoritative KBga avtomatik yozilmaydi.

### D. Fuqaro va mutaxassis oynalarini bog‘lash
- Bir xil event/signal/case IDlar ikkala ko‘rinishda ham ishlatiladi.
- Fuqaro faqat o‘ziga tegishli va ruxsatli ma’lumotni ko‘radi; ekspert faqat o‘z vakolati doirasidagi Case’ni ko‘radi.
- Prototipda bu sintetik data va demo role switch; real auth/SSO/MFA/RBAC server-side keyingi bosqich.
- Muallif uchun alohida yashirin panel shart emas; loyiha mutaxassislari kerakli ekspert oynalarini ko‘ra olishi mumkin, lekin shaxsiy ma’lumotlar va operatsion vakolatlar baribir role/access nazoratiga bog‘liq.

## 6. Xavfsizlik va adolat uchun majburiy release shartlari

- OTP, PIN, CVV/CVC, parol, API secret va to‘liq karta raqami yig‘ilmaydi yoki saqlanmaydi.
- Shaxsiy/bank ma’lumoti faqat qonuniy asos, maqsad, minimal maydon va ruxsat bilan.
- Demo dataset faqat sintetik; real mijoz ma’lumotlari yo‘q.
- Signal hech qachon bank qarori yoki avtomatik bloklash buyrug‘i emas.
- Risk/Rule o‘zgarishi: offline test → shadow → canary → cheklangan inson ko‘rigi → bank yozma qabulidan keyin kengaytirish.
- Ommaviy false-positive oshsa: signal oqimini pauza/karantin, kill switch, oldingi tasdiqlangan versiyaga rollback, ta’sir tahlili va audit.
- Xabar statuslari: CREATED/QUEUED/SENT/TECH_ACK/BUSINESS_ACK/UNDER_BANK_REVIEW/ACTION_REPORTED/FAILED/EXPIRED; texnik ACK bank chorasini anglatmaydi.
- WebView ishlatilsa, eski `addJavascriptInterface` va file-access sozlamalarini tekshirmasdan ko‘chirmaslik; native bridge faqat qat’iy origin-scope bilan yoki imkon qadar Compose-native arxitektura bilan.
- Offline ishlash, import, backup/restore, DB migration va crash recovery real qurilmada tekshiriladi.

## 7. Sinov va qabul rejalari

- 16 qatlam reyestridagi REQ-001…REQ-024, TEST-001…TEST-024 va DEC-01…DEC-10 identifikatorlarini Android artefaktlariga bog‘lash.
- 5 til bo‘yicha alohida gold set; o‘zbek lotin/kirill, qoraqalpoq lotin/kirill, qozoq, rus, ingliz; imlo xato, sheva, aralash til, inkor va follow-up.
- AI: intent accuracy, retrieval Recall@10/precision@k, claim-evidence coverage, contradiction recall/precision, abstention quality, sensitive-data leakage, prompt injection.
- Platforma: Event→Signal→Case→Review→Outcome→Recovery→Audit to‘liq integratsiya testi.
- Xavfsizlik: unauthorized view/edit/export, audit tampering, duplicate/replay, backup path traversal, secrets, stale data.
- Risk: legal-only synthetic, false-positive spike, false-negative, common-mode rule error, kill switch, canary/rollback.
- Qurilma: install/upgrade, DB migration, first import time, RAM, p50/p95 latency, battery, storage, airplane/offline mode, low memory.
- KPI faqat ground truth va pilot data bilan; hozir precision/recall/FP/FN natijasi da’vo qilinmaydi.
- “10,000 test” konsepsiyadagi kelajakdagi test ko‘lami bo‘lishi mumkin; hozir bajarilgan test soni sifatida ko‘rsatilmasin.

## 8. Keyingi ishlab chiqish ketma-ketligi

1. **Foundation gate:** 5,607 JSONni branchga aktivatsiya qilish; SHA/count/unique ID/16 layer/OCR checks; source manifestni to‘g‘rilash.
2. **Data model:** Room/SQLite schema, repository, event/signal/evidence/risk/entity/case/review/timeline/recovery/audit; migration va synthetic scenario seed.
3. **Yagona ish oqimi:** Event→Signal→Risk→Cross-Match/Graph→Case→Human Review→Recovery→Audit; barcha oynalar bir xil state bilan.
4. **Citizen UI:** FINZANJIR ID, Mening kartalarim, alert, phishing, scanner, history, complaint/recovery.
5. **Expert UI:** operations, data quality, signal registry, graph, case detail, human review, timeline, 16 layer, rule/recalibration, audit, KPI, test lab.
6. **AI integration:** FTS4 retrieval + original-core orchestration; 5×5 memory; multilingual tests; document import; optional model/voice.
7. **Hardening:** false-positive controls, privacy, security review, performance, device tests, backup/restore.
8. **Release gate:** APK artifact + Samsung Android runtime evidence + all critical regression/security tests. Shundan keyingina keyingi bosqich “tayyor” deb belgilanadi.

## 9. Hozirgi yakuniy xulosa

V14 va ZIP manbalari FINZANJIRni oddiy chatbot yoki statik risk dashboard emas, balki fuqaro, signal, dalil, risk, Cross-Match, Fraud Graph, Case, Human Review, FIN-RECOVERY, bank bilan kelishilgan almashinuv va 16 qatlamli boshqaruvni bog‘laydigan platforma konsepsiyasi sifatida belgilaydi.

Joriy Android branch esa hozircha **AI knowledge search foundation + statik operatsion ekranlar** darajasida. Build muvaffaqiyatli, ammo platforma ish jarayoni hali persistent va interaktiv emas. Eng katta keyingi vazifa — hamma oynani bitta ma’lumot modeli va yagona Event→Signal→Case→Review→Recovery→Audit zanjiriga ulash; so‘ng AI core, 5×5 memory va fuqarolik/ekspert funksiyalarini shu model bilan integratsiya qilish.

Bu audit asosida tuziladigan keyingi APK hali ham prototype bo‘ladi. Real bank integratsiyasi, production RBAC, mustaqil ekspert tasdig‘i va pilot natijalari alohida Gate talab qiladi.
