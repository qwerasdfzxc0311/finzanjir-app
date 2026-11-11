# FINZANJIR bilim manbalari auditi

**Holat:** dastlabki audit qaydi; yakuniy integratsiya ruxsati emas.  
**Ishchi branch:** `finzanjir-knowledge-audit-2026-11`  
**Asos branch:** `finzanjir-android-v1`  
**Asosiy qoida:** mavjud Android/V3/V4 branchlari o‘zgartirilmaydi. Ushbu branch audit va keyingi alohida, tekshiriladigan o‘zgarishlar uchun ajratilgan.

## 1. Maqsad

FINZANJIR konsepsiyasi va unga tegishli yordamchi hujjatlardagi bilimlarni hozirgi GitHub kod/ma’lumotlar bazasi bilan solishtirish. Maqsad — mutaxassislar oldida konsepsiyaning asosiy tamoyillarini tushuntira oladigan, manbani ko‘rsatadigan va real ishlaydigan qismini demo orqali namoyish qiladigan prototipni tayyorlash. Hujjatdagi talab yoki diagramma mavjud kod funksiyasi deb ko‘rsatilmaydi.

## 2. O‘zgarmas audit qoidalari

1. Asl manba matni qisqartirilmaydi va o‘chirib yuborilmaydi. Yangi tuzilma, bo‘laklar yoki izohlar asl manbaga bog‘langan hosila yozuvlar bo‘ladi.
2. Har bir ma’lumotning manbasi, versiyasi, sahifasi/bo‘limi va kelib chiqish izi saqlanadi.
3. Dublikat deb ko‘ringan yozuvlar mazmuni, konteksti va munosabati tekshirilmasdan o‘chirilmaydi.
4. Muallif tasdig‘i va mustaqil ekspert/bank/rasmiy manba tasdig‘i alohida maydonlarda yuritiladi.
5. Kuzatuv, eshitilgan ma’lumot, gipoteza, taklif, talab, kelajak rejasi, tarixiy ma’lumot va tekshirilgan fakt bir-biriga aralashtirilmaydi.
6. Signal firibgarlik isboti emas; risk balli aybdorlik emas; Case hukm emas; grafikdagi aloqa aybdorlik emas.
7. FINZANJIR bank o‘rniga karta yoki tranzaksiyani bloklamaydi. Bank qarori bank vakolatida qoladi.
8. Faqat hamkor banklar va kelishilgan/ruxsatli kanallar doirasidagi ma’lumot ko‘zda tutiladi; barcha banklar yoki barcha kartalarga kirish da’vo qilinmaydi.
9. Sintetik demo, manba kodi, muvaffaqiyatli build va real qurilma/bank sinovi — turli dalil darajalari.
10. BM25 ushbu ishchi yo‘nalishga ko‘chirilmaydi. V317’dan faqat tanlangan, yengil va testlanadigan savol-tahlil, dalil tanlash, javob-savol mosligi va abstention g‘oyalari baholanadi.
11. Hozirgi APK ichiga Qwen yoki boshqa tashqi/local katta model qo‘shilmaydi. Avval FINZANJIR’ning o‘z bilim bazasi va yengil lokal mantiqi mustahkamlanadi.
12. Bilim importi model vaznlarini o‘qitish degani emas. Quantization faqat keyinchalik alohida model va mos runtime tanlansa baholanadi.
13. Hech qanday integratsiya audit va crosswalk tugamasdan bajarilmaydi. Asosiy branchga bevosita commit qilinmaydi.

## 3. Dastlab ko‘rilgan manbalar

### ZIP 1 — konsepsiya va yordamchi hujjatlar

- FINZANJIR KONSEPSIYA V14 PDF — 164 sahifa.
- FINZANJIR 16 qatlam chuqur tushuntirish DOCX.
- 16 qatlam talablar va sinovlar reyestri PDF — 4 sahifa.
- Signal reyestri, kichik signallar va ilg‘or signallar DOCX.
- Qo‘shimcha amaliy talablar PDF — 19 sahifa.
- Qo‘shimcha FDP ishchi nusxasi DOCX.
- Fuqaro xavfsizligi FDP DOCX.
- False-positive bo‘yicha ekspertiza tuzatishi DOCX.
- Bank integratsiyasi, xavfsizlik va avtomatlashtirish texnik arxitekturasi PDF — 66 sahifa.
- AI va bilim tizimi bo‘yicha besh hujjat birlashtirilgan PDF — 29 sahifa.
- FINZANJIR taqdimoti PPTX — 17 slayd.
- Tarixiy ishchi hujjat va brend rasmlari.

### ZIP 2 — V317 semantik/evidence candidate arxivi

- 7,053 source archive record va 4,671 active index record qayd etilgan.
- 2,000 regression savol/tarix yozuvlari test materialidir; faol javob bilimiga aralashtirilmaydi.
- 515 umumiy ensiklopediya yozuvi FINZANJIR moliyaviy-firibgarlik bilimidan alohida domain qatlamida qoladi.
- Metadata bo‘shliqlari mavjud: 860 yozuvda kind yo‘q, 1,070 kind tasniflanmagan, 540 domain tasniflanmagan, 1,681 til aniqlanmagan.
- V317 manba testlari o‘tgan deb qayd etilgan, ammo Android build/runtime/JNI/Qwen va bank integratsiyasi tekshirilmagan.
- 10K gate o‘tmagan; 2,000 savol smoke testi semantik to‘g‘rilikning mutlaq isboti emas.

## 4. Dastlabki Android branch holati

- Android branch: `finzanjir-android-v1`.
- `knowledge_manifest.json` 1,121 yozuvni ko‘rsatadi: 957 V4 yozuvi va 164 V14 sahifa yozuvi.
- Manifestdagi barcha yozuvlar `candidate_not_authoritative` deb belgilangan.
- V14 sahifa matni import qilingan, biroq diagrammalar, tasvirlar va murakkab jadvallar alohida vizual tekshiruv talab qiladi.
- Hozirgi Kotlin qidiruvi oddiy token kesishmasi va sodda ballashga asoslangan; bu to‘liq semantik tushunish yoki javobning savolga mosligini kafolatlamaydi.
- Android UI’da demo signal/Case namunalari sintetik deb belgilangan; bank API va real bank ma’lumoti ulanmagan.
- Manifest ichidagi branch nomi Android branch bilan mos kelmaydi; bu metadata nomuvofiqligi keyingi audit nuqsoni sifatida qayd etildi, hozircha tuzatilmagan.

## 5. Muhim mazmuniy ziddiyat va tuzatishlar

- Ayrim eski signal misollarida yuqori ball yoki bloklashga o‘xshash ifodalar uchraydi. Ular tasdiqlangan amaliy qoida emas.
- False-positive V2 tuzatishi ommaviy noto‘g‘ri signalni asosiy xavf sifatida belgilaydi; shadow mode, canary, circuit breaker/karantin, kill switch, rollback, bank/inson nazorati va legal-only testlarni taklif qiladi.
- Shu sababli eski ball/avtomatik Case misollari manbada tarixiy taklif sifatida saqlanadi, lekin amaldagi xulq-atvor qoidasi sifatida ko‘chirilmaydi.
- Taqdimotdagi “Silent Hold” iborasi bank vakolatiga zid talqin qilinishi mumkin. U alohida ochiq qaror sifatida aniqlashtirilmaguncha bloklash yoki to‘lovni ushlab qolish funksiyasi deb ko‘rsatilmaydi.
- V14 va texnik arxitektura hujjatlari konsepsiya/taklifdir; ularning mavjudligi bank integratsiyasi yoki production tayyorligini isbotlamaydi.

## 6. Bilim yozuvi uchun tavsiya etiladigan ikki mustaqil maqom

- `author_attestation`: `author_confirmed`, `author_provided`, `not_confirmed`.
- `independent_review`: `not_reviewed`, `expert_reviewed`, `bank_confirmed`, `official_source_verified`.

Bundan alohida `content_type` va `record_status` saqlanadi. Masalan, “muallif tasdiqlagan loyiha materiali” degani “bank tasdiqlagan fakt” degani emas.

## 7. Keyingi audit bosqichlari

1. Har bir manbaning to‘liq bo‘lim/sahifa/tabel/diagramma inventarini yakunlash.
2. Har bir source item uchun Android/V4/V317’dagi mos yozuv va kodni topish.
3. `present / partial / missing / duplicate / conflict / obsolete / future / archive-only` holatlarini dalil bilan belgilash.
4. Asl matnni saqlaydigan, source-linked yangi bilim formati va fayl bo‘linishini tayyorlash.
5. Crosswalk va ziddiyatlar reyestrini tekshirish.
6. Shundan keyingina alohida integratsiya rejasini tuzish va foydalanuvchiga ko‘rsatish.

**Ushbu qayd dastlabki audit natijasidir. Yakuniy crosswalk, to‘liq manba nusxalari yoki bilim integratsiyasi bajarildi degani emas.**


## 8. V14 bo‘yicha qo‘shimcha maxfiylik va doira nazorati

- V14 mundarijasidagi 10-bob SINBAD va ATMOS yo‘nalishlarini tilga oladi. Foydalanuvchining amaldagi loyiha chegarasiga muvofiq, bu bob faol FINZANJIR bilimlar bazasiga ko‘chirilmaydi; manba arxivda o‘z holicha qoladi.
- V14’ning muallif profili va loyiha pasporti sahifalarida shaxsiy aloqa ma’lumotlari bor. Android manifesti V14’ning 164 sahifasi ommaviy candidate yozuvlari sifatida import qilinganini ko‘rsatadi. Shuning uchun ommaviy AI qidiruvi va mualliflikni ko‘rsatishdan oldin shaxsiy aloqa maydonlari bo‘yicha alohida maxfiylik auditi talab qilinadi.
- Mualliflikni ko‘rsatish mumkin, lekin muallifning shaxsiy aloqa ma’lumotlarini umumiy bilim qidiruvida chiqarish avtomatik ravishda ruxsat etilgan deb olinmaydi. Alohida muallif-only yoki ruxsat bilan ko‘rsatiladigan qatlam dizayni ko‘rib chiqiladi.


## 9. 2026-11-11 audit verification — Android manifest, privacy scope va branch ajratilishi

### 9.1. Branch holati

GitHub branch endpoint va compare natijasi qayta tekshirildi:

- Audit branch HEAD: `4b631bea57380fbe1b504615e1cac43261408e13`.
- Android asos branch HEAD: `f38e0b7253c915e50f84ffe1053a9e40aec12733`.
- Compare: audit branch Android branchdan 18 commit oldinda, 0 commit ortda.
- Compare ro‘yxatidagi 9 ta o‘zgargan faylning barchasi `docs/knowledge_audit/` ichida. `app/` kodi yoki Android assetlari o‘zgarmagan.

### 9.2. Android manifest bo‘yicha qayta tasdiqlangan faktlar

Android asos branchidagi `app/src/main/assets/knowledge_manifest.json`:

- Git blob SHA: `a946e6292d4b1bd65b570b414a70694107f5e2c1`.
- `record_count = 1121`.
- `records_by_type` yig‘indisi ham 1,121: 33 + 16 + 22 + 42 + 24 + 820 + 164.
- Manifestdagi `branch` qiymati `finzanjir-v4-unified-workflow-uz`, holbuki real Android asos branch `finzanjir-android-v1`. Bu metadata nomuvofiqligi; Android branchda tuzatilmadi.
- 1,121 yozuvning barchasi `candidate_not_authoritative` siyosati ostida. Bu muallif tasdig‘i yoki mustaqil ekspert tasdig‘i emas.

### 9.3. Maxfiylik va yozuv maqomi bo‘yicha tasdiqlangan xavf

Manifestning umumiy `privacy_scope.public_kb` bayonoti V14ning 164 sahifasidan olingan muallif/loyiha tarixi parchalarini ham ommaviy KB ichida saqlashini, muallif-only panel yo‘qligini va barcha qidiruv natijalari tashrif buyuruvchilarga ko‘rinishini aytadi.

Android `FinzanjirKnowledgeBase.kt` fayli bo‘yicha kod ko‘rigi:

- `Record` modeli faqat ID, text, approval, source ID/version/section/path va record type maydonlarini o‘qiydi.
- `author_attestation`, `independent_review`, `language`, `privacy_scope/access_scope` maydonlari ushbu modelda yo‘q.
- Qidiruv `load(context)` orqali yuklangan barcha yozuvlarni token mosligi bilan saralaydi; privacy/access scope bo‘yicha filtr ko‘rinmadi.
- Javob manba satrlarida approval ko‘rsatiladi, ammo muallif tasdig‘i va mustaqil tekshiruv alohida aks ettirilmaydi.

Bu **tasdiqlangan privacy/governance xavfi**: V14 sahifalaridagi muallifga oid yoki shaxsiy ma’lumotlar umumiy qidiruvda chiqishi ehtimoli bor. Hozircha hech qanday ma’lumot o‘chirilmadi yoki APK kodi o‘zgartirilmadi. Keyingi crosswalkda bunday yozuvlar `restricted_review` sifatida belgilanib, muallifga oid savollarga cheklangan ko‘rsatish siyosati alohida ishlab chiqilishi kerak. Faqat umumiy manifest bayonoti asosida har bir yozuvning aniq maxfiylik maqomi aniqlangan deb bo‘lmaydi.

### 9.4. Hali ochiq qolgan ishlar

1. Asl ZIP-1 va ZIP-2 fayllari ushbu seansda Library ZIP ro‘yxatida topilmadi; shu sababli asl baytlar, checksumlar va PPTX/PNG vizual lokatorlari qayta tekshirilmadi.
2. ZIP-1dagi 17 PPTX slaydi va 6 PNG uchun alohida source locator/crosswalk hali yo‘q.
3. V317 188 FINZANJIR-domain yozuvlari bilan ZIP-1 source birliklari item-by-item bog‘lanmagan.
4. Android 1,121 yozuvi bilan item-by-item crosswalk hali bajarilmagan.
5. Katta `finzanjir_knowledge.json` aktivining to‘liq yozuv darajasidagi tekshiruvi ushbu seansda bajarilmadi; kod modeli faqat ayrim governance maydonlarini o‘qimasligi tasdiqlandi.
6. Merge ledger tayyor emas; bilim integratsiyasi va ishlaydigan kod o‘zgarishi taqiqlangan holatda qoladi.

**Qaror:** audit davom etadi. Muallif/private ma’lumotlarning public qidiruvga chiqish xavfi va manifest branch nomuvofiqligi qayd etildi. Asosiy Android/V3/V4/main branchlarga tegilmadi.
