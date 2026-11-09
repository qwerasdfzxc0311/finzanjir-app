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
