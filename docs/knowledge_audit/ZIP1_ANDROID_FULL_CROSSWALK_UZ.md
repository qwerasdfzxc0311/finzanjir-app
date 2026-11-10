# ZIP1 → Android bilim bazasi: keng qamrovli dastlabki crosswalk

## Audit chegarasi
ZIP1 dagi 14 ta hujjatning 1,216 ta birliklari (DOCX paragraf/jadval qatori, PDF sahifasi, PPTX slaydi) Android indeksidagi 4,671 yozuv bilan leksik usulda solishtirildi. Bu **qidiruv dalili**, semantik to‘liqlik yoki kodda ishlash isboti emas. Yuqori/qisman moslik importni, talab bajarilganini yoki mustaqil tasdiqni anglatmaydi. Moslik topilmasligi ham mazmun loyihada umuman yo‘q degani emas.

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
- 16 qatlam tushuntirish hujjatida 68 birlik uchun Android indeksda aniq leksik dalil topilmadi.
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
