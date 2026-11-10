# Aktiv 1,121 yozuv va 5,607 migratsiya nomzodini solishtirish

Sana: 2026-11-10
Branch: `integrated-workflow-foundation-2026-11-10`

## Tekshiruv natijalari

GitHub branchidagi hozirgi Android asset va Library'dagi SHA-256 bilan tasdiqlangan 5,607 yozuvli migratsiya fayli to'g'ridan-to'g'ri solishtirildi.

| Ko'rsatkich | Natija |
|---|---:|
| Hozirgi Android asset | 1,121 |
| Migratsiya nomzodi | 5,607 |
| Har ikki fayldagi bir xil ID | 49 |
| Bir xil ID va bir xil matn | 31 |
| Bir xil ID, lekin matni farqli | 18 |
| Faqat eski aktiv assetda bor yozuv | 1,072 |
| Turli ID bilan aynan bir xil matnli cross-file yozuv | 0 |
| Birlashtirilgan korpusdagi noyob ID (versiya tarixisiz) | 6,679 |

Migratsiya faylining SHA-256:
`f3457b372c5e7f79a0875603cb33987a7720f96061c1ac23ea038b69f2dfb250`

## Xavfsiz birlashtirish qarori

1. 1,072 ta eski aktiv yozuvni yo'qotmasdan yangi korpusga qo'shish kerak.
2. 31 ta bir xil ID va bir xil matnli yozuvni ikkinchi marta qo'shmaslik kerak; eski manba metama'lumotlari provenance sifatida saqlanadi.
3. 18 ta bir xil ID, ammo matni farqli yozuvni jim almashtirish mumkin emas. Yangi nomzod matni canonical ko'rinishda qoladi, eski matn esa `legacy_versions` ichida tarixiy variant sifatida saqlanishi va `search_aliases` orqali qidiruvda topilishi mumkin.
4. Migratsiya korpusidagi 3 ta exact-text duplicate guruhi (6 yozuv) hozircha o'chirilmaydi: ID va manba izlari saqlanadi. Bu guruhlar alias/til vazifasi bo'yicha alohida ko'rib chiqiladi.
5. Yakuniy aktiv asset kutiladigan soni — 6,679 noyob ID. 18 ta tarixiy matn versiyasi shu yozuvlarning ichida metadata sifatida saqlanadi; alohida dublikat ID sifatida qo'shilmaydi.

## Hozirgi holat

5,607 yozuvli fayl hali Android aktiv asseti bilan almashtirilmadi. Sababi: eski 1,121 yozuvdan 1,072 tasi migratsiya nomzodida yo'q, shuningdek 18 ta ID bo'yicha matn versiyasi farqi bor. To'g'ridan-to'g'ri overwrite ma'lumot yo'qotishiga olib kelishi mumkin.

BM25 qo'shilmaydi. Android retrieval indeksi SQLite FTS4 bo'lib qoladi. Korpus birlashtirish alohida, SHA/count/ID tekshiruvlaridan o'tgandan keyin bajariladi.


## 2026-11-10 — 6,679 yozuvli birlashtirilgan candidate tayyorlandi

Mavjud aktiv 1,121 yozuvli Android asset va Library'dagi SHA-256 bilan tasdiqlangan 5,607 yozuvli candidate qayta birlashtirildi. Yakuniy invariantlar:

- Candidate: 5,607; aktiv oldingi asset: 1,121.
- Bir xil ID va bir xil matn: 31; eski provenance birlashtirildi.
- Bir xil ID, matni o'zgargan: 18; eski matn `legacy_versions` va `search_aliases` ichida saqlandi.
- Faqat eski aktiv assetda bo'lgan yozuv: 1,072; saqlandi.
- Yakuniy noyob ID: 6,679; takror ID: 0.
- Tarixiy versiya: 18; oldingi provenance yozuvi: 49.
- Ichki exact-text duplicate guruhlari: 3; avtomatik o'chirilmadi.

Birlashtirilgan candidate GitHub'da 12 ta JSON bo'lagida saqlandi:
`source-import/candidates/finzanjir_knowledge_merged_6679_part_01.json` ... `part_12.json`.

Birlashtirilgan JSONni qayta yig'ish uchun SHA-256:
`301a1889ef4245eb72a4c68b7e678d842e5e5bf1a68c1507066e4801bc0051af`

Muhim: bo'laklar `app/src/main/assets` tashqarisida. APKning aktiv 1,121 yozuvli asseti va uning manifesti o'zgartirilmadi. 6,679 yozuvli candidate hali APKga kiritilmagan. SQLite FTS4 regression tekshiruvi CI orqali bajarilishi kerak; bu natija Samsung qurilmadagi runtime sinovi o'rnini bosmaydi.
