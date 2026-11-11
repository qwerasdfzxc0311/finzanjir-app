# 16 qatlam hujjati — birinchi manba crosswalk natijasi

**Audit obyekti:** FINZANJIR_16_QATLAM_CHUQUR_TUSHUNTIRISH_V3_TUZATILGAN.docx  
**Manba yaxlitligi:** 305 bo'sh bo'lmagan paragraf, 3 jadval, 24 jadval qatori; 38,909 ajratilgan belgi.  
**Hujjatdagi sana va maqom:** 2026-10-17; mustaqil qo'shimcha ishchi hujjat, ekspertlar muhokamasi uchun. U V14 konsepsiyasini almashtirmaydi.  
**Muhim mualliflik chegarasi:** hujjatning o'zi qatlamlar taklif/talab ekanini, sanab o'tilishi ularning APKda ishlayotganini anglatmasligini aytadi.

## 1. Tekshirilgan manba tuzilmasi
- Hujjat boshida maqsad, chegaralar, holat yorliqlari va 9 bandli yo'lko'rsatkich mavjud.
- 16 qatlamning har biri alohida bo'limda berilgan: maqsad, qamrov, vakolat chegarasi, xato holati, tekshiruv mezoni, kirish/chiqish, boshqa qatlamlar bilan aloqa va amaldagi mavjudlikni tasdiqlash talabi.
- Keyingi bo'limlarda qatlamlararo nazorat zanjiri, noto'g'ri signal/bank xabari misoli, ustuvorlik, hujjatlashtirish shabloni, KPI, 15 bobga nisbatan audit va ekspertlar bilan kelishiladigan masalalar bor.
- 16 qatlam bo'limlari paragraf oralig'i bo'yicha ajratildi; jadval qatorlari ham alohida manba birliklari sifatida saqlanishi kerak.

## 2. V317 active index bilan solishtirish (Android APK emas)
**Natija: partial / source-provenance-missing — to'liq import tasdiqlanmadi.**

Tekshiruv:
- V317 active indexida 4,671 yozuv bor. Bu Android APK indeksi emas; Android asos branchidagi `knowledge_manifest.json` alohida 1,121 yozuvni ko‘rsatadi.
- Indeks bo'yicha ushbu DOCX nomi yoki 16_QATLAM manba belgisi bilan bevosita bog'langan yozuv topilmadi.
- source maydonida aynan shu fayl ko'rsatilgan yozuv topilmadi.
- Matn o'xshashligi asosida ayrim umumiy mavzular (provenance, data quality, risk/uncertainty, human review, governance, privacy, incident response, testing, bank integration) bilan bog'liq yozuvlar bor. Lekin ular mustaqil 16 qatlam hujjatining barcha matni, cheklovlari va lokatorlari saqlanganini isbotlamaydi.
- Shuning uchun semantik yaqinlikni present deb belgilash mumkin emas; tegishli mavzular hozircha partial_candidate darajasida.

## 3. V317 source archive bilan solishtirish
**Natija: source-provenance-missing — aynan shu DOCX nomi yoki uning aniq manba identifikatori topilmadi.**

- 7,053 yozuvli V317 source archive va uning JSON/JSONL/MD/TXT/HTML fayllarida fayl nomi hamda hujjat sarlavhasining aniq qidiruvi bajarildi.
- Ushbu qidiruvda aynan shu DOCX nomiga bevosita ishora topilmadi.
- Bu hujjatdagi g'oyalar boshqa manbalarda umuman yo'q degani emas; faqat mazkur hujjatning manba sifatida izchil qayd etilgani tasdiqlanmadi.

## 4. Android ilova kodi bilan solishtirish
- Android ilovasida 16 qatlam katalogi/statik ekran borligi avvalgi kod auditi bilan qayd etilgan.
- Katalog yoki qatlam nomlarining ekranda ko'rsatilishi 16 qatlamning real ishlaydigan mustaqil modullari borligini anglatmaydi.
- Hozirgi dalillar 16 qatlam uchun to'liq runtime implementatsiya, qatlamlararo API, xato boshqaruvi yoki har bir qatlamning test dalilini ko'rsatmaydi.
- Hujjatning o'zi ham mavjud/tasdiqlangan yorlig'i uchun talab, mas'ul rol, kod/konfiguratsiya, kirish-chiqish namunasi va qayta tiklanadigan test dalilini talab qiladi.

## 5. Dastlabki crosswalk jadvali

| Manba bo'limi | Android/V317 dalili | Holat | Qaror |
|---|---|---|---|
| Hujjat maqsadi va holat yorliqlari | To'liq manba provenance yozuvi topilmadi | missing | Hujjat metadata sifatida saqlash |
| 1–3 qatlam: provenance, sifat, risk/noaniqlik | Umumiy mavzudagi yaqin yozuvlar bor, aniq manba lokatori yo'q | partial_candidate | Manba matnini alohida import qilish; mavjud yozuvlarga derived_from bilan bog'lash |
| 4–7 qatlam: human review, governance, disclosure, automation safety | Umumiy o'xshashliklar mavjud; hujjat bo'limi bilan tasdiqlangan bog'lanish yo'q | partial_candidate | Hozircha merge qilmaslik |
| 8–12 qatlam: Case, citizen transparency, privacy, incident, AI KB | Ayrim konsepsiya va xavfsizlik mavzulari boshqa yozuvlarda uchraydi | partial_candidate | Har bir qatlamni alohida talab birligi sifatida crosswalk qilish |
| 13–16 qatlam: testing, bank integration, capacity, impact | V14/V317 ichida mavzuga oid materiallar bor; aynan ushbu hujjatning to'liq nusxasi isbotlanmagan | partial_candidate | Manba lokatorlari bilan alohida moslashtirish |
| Qatlamlararo zanjir, amaliy misol, KPI, audit va ekspert savollari | Aniq to'liq nusxa yoki lokator mosligi topilmadi | missing_or_unverified | Alohida bloklar sifatida saqlash; qisqartirmaslik |

## 6. Xavfsiz integratsiya qarori
1. Hujjatning to'liq matni va jadvallari alohida immutable source snapshot sifatida saqlanadi.
2. Har bir qatlam uchun L01–L16 barqaror ID beriladi; original bo'lim sarlavhasi va paragraf lokatorlari saqlanadi.
3. Hozirgi o'xshash yozuvlar o'chirilmaydi yoki birlashtirilmaydi. Faqat related_to/candidate_match aloqasi qo'yiladi.
4. Hujjatdagi taklif, sinovdan o'tmagan, ochiq masala yorliqlari yozuvlarga ko'chiriladi; author_attestation va independent_review alohida yuritiladi.
5. Keyingi qadam — 16 qatlamning har birini talab/test/qaror IDlari va Android kod dalillari bilan alohida tekshirish.

**Audit cheklovi:** bu crosswalk statik fayl/indeks/kod tekshiruvidir. U ekspert tasdig'i, bank tasdig'i, real API sinovi yoki telefon runtime testi emas.


## 7. 2026-11-11 audit correction — indeks nomi

Oldingi matndagi “Android bilim bazasi” sarlavhasi noto‘g‘ri bo‘lgan: 4,671 yozuvli korpus V317 active indexidir. Android APK manifestidagi 1,121 yozuv boshqa korpus. Shu sababli 16 qatlam hujjati bo‘yicha bu natija faqat V317 active index bilan dastlabki solishtirish hisoblanadi; Android 1,121 yozuvi bilan item-by-item crosswalk hali bajarilmagan. Hech qanday yozuv merge qilinmadi yoki o‘chirilmadi.
