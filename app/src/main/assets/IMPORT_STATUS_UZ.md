# FINZANJIR Android — bilimlar korpusi importi

## Joriy import
Android ilovasi lokal assets ichidan **1,121 ta strukturali yozuv** o‘qiydi:
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
Android qidiruvi V4 va V14 sahifa yozuvlarini lokal JSON assetdan o‘qiydi. Lotin/kirill normallashtirish, manba izini chiqarish va yetarli dalil topilmaganda ochiq rad etish holati mavjud.
