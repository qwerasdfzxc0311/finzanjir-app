# FINZANJIR Android — bilimlar korpusi importi

## Joriy import
Android ilovasining hozirgi aktiv asseti lokal assets ichidan **1,121 ta strukturali yozuv** o‘qiydi. 5,580 yozuvli yangi migratsiya alohida candidate paket sifatida tekshirilmoqda; u aktiv assetga hali ko‘chirilmagan:
- V4 korpusi: 957 yozuv;
- FINZANJIR V14 original PDF: 164 sahifa yozuvi (1–164).

Har bir V14 sahifa yozuvida original sahifa raqami, source_id, source_version, source_section, source_path va candidate maqomi saqlanadi.

## Ochiq prototip ko‘rinishi
Alohida, faqat muallifga ko‘rinadigan panel mavjud emas. Barcha bo‘limlar va bilim qidiruvi prototipga kirgan mutaxassislar/ziyirchilar uchun bir xil ko‘rinadi. V14dagi muallif va loyiha tarixi sahifalari ham alohida muallif paneliga ajratilmagan; ular manbasi bilan bilim korpusida qidiriladi.

## Maqom
Barcha yozuvlar `candidate_not_authoritative`. Ular bank tomonidan tasdiqlangan qoida, ekspert xulosasi yoki amalda ishlayotgan mexanizm deb talqin qilinmaydi. Qidiruv mosligi faktik ishonchlilik yoki ekspert tasdig‘i emas.

## Manbalar va bo‘shliqlar
- V4 manbalar reyestri va 16 qatlam katalogi import qilingan.
- V14 original PDF sahifalari import qilingan. Diagramma, rasm va murakkab jadvallar vizual tekshiruv talab qiladi.
- V8 bank texnik arxitektura PDFsi alohida asl manba sifatida hali import qilinmagan. V14/V8 taqqoslash auditi bor, ammo u original V8 o‘rnini bosmaydi.
- FINZANJIR AI v0.6.0 ZIP va original `curated_notes.json`, `SOURCE_REGISTER.csv`, `FEATURE_REGISTRY.csv`, `TEST_PLAN.csv` ushbu snapshotda topilmadi. 4,671 yozuvli V317 audit ko‘rsatkichi ham ushbu 1,121 yozuvli Android korpusiga teng emas.
- To‘liq arxiv importi uchun asl fayllar, ularning versiyasi va manba registri talab qilinadi.

## Android qidiruvi
GitHub branchidagi qidiruv kodi BM25-uslubidagi term weighting, lotin/kirill normallashtirish, fuqarolik/mutaxassis ko‘rinishi, manba/maqom ko‘rsatish va yetarli dalil bo‘lmagandagi fallbackni qo‘llaydi. Aynan bir xil matnli yozuvlar korpusda saqlanadi, lekin qidiruv javobida takrorlanmaydi; tegishli manba izlari birga ko‘rsatiladi.

## 2026-11-09 migratsiya nomzodi
- Candidate asset: 5,607 yozuv; SHA-256: `f3457b372c5e7f79a0875603cb33987a7720f96061c1ac23ea038b69f2dfb250`.
- AI v2.1 dagi 4,656 yozuv ID bo‘yicha to‘liq saqlangan.
- 893 yangi hujjat bo‘lagi va 16 ta `V4-L01` ... `V4-L16` qatlam yozuvi mavjud.
- ID dublikatlari: 0; aynan bir xil matnli guruhlar: 3. Manba izini yo‘qotmaslik uchun yozuvlar o‘chirilmagan.
- 23/23 retrieval smoke-test PASS — Python BM25-ekvivalent test, Android runtime testi emas.
- 304 PDF sahifasidan matn ajratilgan. 37 PDF ichki tasvirining 26 tasida OCR urinishlari bajarildi; 22 ta tasvir va 5 mustaqil diagrammadan 27 ta OCR candidate yozuvi qo‘shildi. Barcha OCR yozuvlari vizual tekshiruv talab qiladi.
- **Muhim:** 5,580 yozuvli JSON hali aktiv Android asset emas. Asset almashtirish, manifest SHA-256 tekshiruvi, Android build va telefon sinovi bajarilgandan keyingina aktiv import deb e’lon qilinadi.
