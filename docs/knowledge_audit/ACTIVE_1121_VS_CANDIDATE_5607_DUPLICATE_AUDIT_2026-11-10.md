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
