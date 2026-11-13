# FINZANJIR Android — muallif ma’lumotlari va privacy-scope auditi

**Sana:** 2026-11-13  
**Tekshirilgan asos branch:** `finzanjir-android-v1`  
**Audit branch:** `finzanjir-knowledge-audit-2026-11`  
**Audit turi:** faqat statik manifest va Kotlin/Compose kod ko‘rigi  
**Qaror:** yuqori ustuvorlikdagi maxfiylik/kirish doirasi bo‘shlig‘i qayd etildi; kod va bilim assetlari o‘zgartirilmadi.

## 1. Tekshiruv doirasi

Ushbu audit foydalanuvchi talab qilgan uchta narsani tekshiradi:

1. Muallifga tegishli ma’lumotlar umumiy FINZANJIR bilimlaridan ajratilganmi?
2. Muallif tasdiqlaganlik va mustaqil ekspert tekshiruvi ikki alohida maqom sifatida boshqariladimi?
3. Maqom va privacy holati AI oynasining yuqorisida doimiy ko‘rinadimi yoki har javobda takrorlanadimi?

Tekshiruv faqat GitHub’dagi `finzanjir-android-v1` branchining quyidagi fayllariga asoslandi:

- `app/src/main/assets/knowledge_manifest.json`
- `app/src/main/java/uz/finzanjir/mobile/FinzanjirKnowledgeBase.kt`
- `app/src/main/java/uz/finzanjir/mobile/MainActivity.kt`

Bu statik kod ko‘rigi. APK qurilmada ishga tushirilmadi; real foydalanuvchi yoki tarmoq testi bajarilmadi.

## 2. Tasdiqlangan dalillar

### 2.1. Manifestda public KB doirasi juda keng

`knowledge_manifest.json`:

- 4-qator: manifestdagi `branch` qiymati `finzanjir-v4-unified-workflow-uz`; tekshirilayotgan Android branch esa `finzanjir-android-v1`. Bu metadata nomuvofiqligi.
- 6-qator: `record_count = 1121`.
- 7-qator: barcha yozuvlar `candidate_not_authoritative` ekanligi ko‘rsatilgan.
- 103–104-qatorlar: `privacy_scope.public_kb` tavsifida 164 ta V14 sahifasidan olingan loyiha tarixi va muallif/loyiha tarixi parchalarigacha public KB tarkibida ekani, alohida author-only panel yo‘qligi va barcha bo‘limlar hamda qidiruv natijalari tashrif buyuruvchilarga ko‘rinishi yozilgan.

Bu manifestning o‘zida e’lon qilingan scope. U 164 sahifadagi har bir matn maxfiy yoki sezgir ekanini isbotlamaydi. Biroq muallifga tegishli materialni umumiy qidiruvdan ajratish talabi bilan amaldagi public scope o‘rtasida aniq nomuvofiqlik bor.

### 2.2. Kotlin Record modeli access/privacy maqomlarini o‘qimaydi

`FinzanjirKnowledgeBase.kt` 19–28-qatorlarda `Record` quyidagi maydonlardan iborat:

- id
- text
- approval
- sourceId
- sourceVersion
- sourceSection
- sourcePath
- recordType

Modelda quyidagi alohida maydonlar yo‘q:

- `author_attestation`
- `independent_review`
- `privacy_scope`
- `access_scope`
- `language`
- `content_type`

105–125-qatorlardagi loader faqat yuqoridagi sakkizta maydonni JSONdan o‘qiydi. Demak, asset ichida qo‘shimcha metadata mavjud bo‘lgan taqdirda ham, hozirgi Kotlin modeli ularni ishlatmaydi.

### 2.3. Qidiruv barcha yuklangan yozuvlar ustida ishlaydi

`FinzanjirKnowledgeBase.kt`:

- 45-qator: `load(context)` orqali barcha yozuvlar olinadi.
- 57–68-qatorlar: umumiy qidiruv `records.mapNotNull` orqali butun ro‘yxatni ballaydi.
- Ushbu qidiruv yo‘lida `privacy_scope`, `access_scope` yoki author-only ko‘rinish uchun filtr yo‘q.

Shuning uchun hozirgi kodda muallifga oid yozuvni umumiy qidiruvdan ajratadigan kod darajasidagi kirish nazorati ko‘rinmadi.

**Chegara:** bu topilma APK ichidagi matnni kimdir amalda ko‘rganini yoki muayyan maxfiy ma’lumot oshkor bo‘lganini isbotlamaydi. U faqat manifest va qidiruv kodi bo‘yicha author-only cheklovini majburiy bajaradigan mexanizm ko‘rinmaganini isbotlaydi.

### 2.4. AI oynasida maqom doimiy yuqori panel emas

`MainActivity.kt` dagi `KnowledgeAssistant()`:

- 145-qator atrofida AI oynasi boshlanadi.
- Sarlavha va qisqa tavsifdan keyin savol maydoni hamda qidiruv tugmasi keladi.
- 157–166-qatorlar atrofidagi javob kartasida `Manbalar`, `Holat: ${result.confidence}` va `result.notice` ko‘rsatiladi.
- Bilim bazasi versiyasi va yozuvlar soni oynaning pastki qismida ko‘rsatiladi.

Demak, foydalanuvchi xohlagan doimiy yuqori maqom paneli hozir mavjud emas. Aksincha, maqom va ogohlantirish javob kartasida takrorlanadi.

Bundan tashqari, `confidence` nomli qiymat `FinzanjirKnowledgeBase.kt` 90-qatorida oddiy moslik yorlig‘i sifatida belgilanadi: `MOS YOZUV TOPILDI` yoki `QISMAN MOSLIK`. Uni model aniqligi, faktik ishonchlilik yoki ekspert tasdig‘i foizi deb talqin qilish mumkin emas.

## 3. Xavf va ustuvorlik

**Ustuvorlik: yuqori — keyingi mutaxassislar namoyishidan oldin hal qilinishi kerak.**

| Muammo | Dalil | Xavf |
|---|---|---|
| Public KB ichida muallif/loyiha tarixi parchalarining borligi | Manifest 103–104-qatorlar | Muallifga oid material umumiy qidiruvda chiqishi mumkin |
| Author-only access filter yo‘qligi | Record modeli va search oqimi | Cheklangan yozuvlar kod darajasida ajratilmagan |
| Mustaqil tekshiruv maqomi modelda yo‘q | Record maydonlari | Muallif tasdig‘i va ekspert tekshiruvi farqi saqlanmaydi |
| Doimiy yuqori maqom paneli yo‘q | MainActivity AI UI | Foydalanuvchi bilimlar holatini oynaning boshida ko‘rmaydi |
| Har javobda takroriy notice | Javob kartasi | Foydalanuvchi xohlagan ixcham, doimiy holat ko‘rinishi bajarilmagan |
| Manifest branch metama’lumoti eskirgan | Manifest 4-qator | Korpus qaysi branch snapshotidan olingani noaniqlashadi |

## 4. Tavsiya etiladigan xavfsiz dizayn — hozircha amalga oshirilmaydi

Audit va item-by-item crosswalk tugamaguncha quyidagi takliflar kodga kiritilmaydi:

1. Har bir yozuv uchun `author_attestation` va `independent_review` alohida saqlansin. `author_confirmed` hech qachon `expert_reviewed` yoki `official_source_verified` o‘rnida ishlatilmasin.
2. `privacy_scope/access_scope` aniq bo‘lmagan yozuvlar umumiy qidiruvga ochilmasin; default holat `restricted_review` yoki deny bo‘lsin.
3. Muallif biografiyasi va shaxsiy ma’lumotlar faqat muallif haqidagi bevosita savol va ruxsat etilgan scope bo‘yicha ajratilgan qatlamda saqlansin.
4. Loyiha falsafasi haqidagi muallif tasdiqlagan ma’lumotlar alohida scope bilan saqlansin; ular umumiy loyiha talabi yoki mustaqil ekspert xulosasi sifatida ko‘rsatilmasin.
5. AI oynasining yuqorisida doimiy panel bo‘lsin: muallif tasdig‘i holati, mustaqil tekshiruv holati, demo/prototip holati va bilimlar bazasining qamrovi alohida ko‘rsatilsin.
6. Panel umumiy korpus bo‘yicha noto‘g‘ri yagona maqom bermasin. Masalan, “muallif tasdiqlagan” faqat tegishli muallif yozuvlariga taalluqli ekani aniq bo‘lsin.
7. Har bir javob oxirida uzun notice takrorlash o‘rniga, zarur manba va yozuv maqomi ixcham ko‘rsatilishi mumkin. Lekin bu yuqori paneldagi holatni almashtirmaydi.
8. `confidence` nomi faktik ishonchlilik sifatida talqin qilinmasin; oddiy retrieval mosligi ekanligi aniq ifodalansin yoki keyingi dizaynda qayta nomlansin.

## 5. O‘zgartirilmagan narsalar

- Android/V3/V4/main branchlarga yozuv kiritilmadi.
- `finzanjir-android-v1` kodi va assetlari o‘zgartirilmadi.
- `knowledge_manifest.json` yoki `finzanjir_knowledge.json` qayta yozilmadi.
- Hech qanday muallif yozuvi o‘chirilmadi yoki ommaviy/private qatlamlar o‘rtasida ko‘chirilmadi.
- APK build, install yoki runtime testi bajarilmadi.
- ZIP-1 va ZIP-2 manbalarining to‘liq nusxasi yoki crosswalk yakunlangan deb da’vo qilinmaydi.

## 6. Keyingi ochiq vazifa

Asl ZIP-1 va ZIP-2 qayta mavjud bo‘lgach, V14 va tegishli hujjatlardagi muallifga oid har bir bo‘lakni source locator bilan ro‘yxatga olish; keyin uni Androiddagi 1,121 yozuv bilan item-by-item solishtirish. Har bir bo‘lak uchun muallif tasdig‘i, mustaqil tekshiruv, public/restricted scope va saqlash qarori qayd etilsin.

Shundan keyin, to‘liq crosswalk, ziddiyat/dublikat reyestri va mazmunni saqlash ledgeri tayyor bo‘lgach, foydalanuvchiga alohida integratsiya rejasi hamda xavflar ko‘rsatiladi. Kodga o‘tish uchun foydalanuvchining aniq tasdig‘i talab qilinadi.

**Yakuniy xulosa:** joriy Android manifesti va Kotlin qidiruvi bo‘yicha muallifga oid ma’lumotlarni umumiy qidiruvdan ajratadigan majburiy privacy/access nazorati tasdiqlanmadi. Bu hal qilinishi kerak bo‘lgan audit topilmasi; hozircha hech qanday kod yoki bilim o‘zgartirilmadi.
