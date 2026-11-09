# FINZANJIR Android — bilimlar korpusi importi

## Joriy import
Android ilovasi lokal assets ichidan **1,121 ta strukturali yozuv** o‘qiydi:
- V4 korpusi: 957 yozuv;
- FINZANJIR V14 original PDF: 164 sahifa yozuvi.

Har bir yozuvda mavjud bo‘lgan joylarda ID, matn, approval maqomi, source_id, source_version, source_section, source_path va record_type saqlanadi. V14 yozuvlari original PDF sahifa raqami bilan bog‘langan.

## Maqom
Barcha yozuvlar `candidate_not_authoritative`. Ular bank tomonidan tasdiqlangan qoida, ekspert xulosasi yoki amalda ishlayotgan mexanizm deb talqin qilinmaydi. Qidiruv balli faktik ishonchlilik ko‘rsatkichi emas.

## Manbalar va bo‘shliqlar
- V4 manbalar reyestri va 16 qatlam katalogi import qilingan.
- V14 original PDF sahifalari import qilingan. Diagramma, rasm va murakkab jadvallar vizual tekshiruv talab qiladi.
- V8 bank texnik arxitektura PDFsi alohida asl manba sifatida hali import qilinmagan. V14/V8 taqqoslash auditi bor, ammo u original V8 o‘rnini bosmaydi.
- FINZANJIR AI v0.6.0 ZIP va original `curated_notes.json`, `SOURCE_REGISTER.csv`, `FEATURE_REGISTRY.csv`, `TEST_PLAN.csv` ushbu snapshotda topilmadi. 4,671 yozuvli V317 audit ko‘rsatkichi ham ushbu 1,121 yozuvli Android korpusiga teng emas.
- To‘liq arxiv importi uchun asl fayllar, ularning versiyasi va manba registri talab qilinadi.

## Android qidiruvi
Android qidiruvi V4 va V14 sahifa yozuvlarini lokal JSON assetdan o‘qiydi. Lotin/kirill normallashtirish, manba izini chiqarish va yetarli dalil topilmaganda ochiq rad etish holati mavjud.
