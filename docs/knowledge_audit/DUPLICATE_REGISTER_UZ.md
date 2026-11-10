# FINZANJIR — dublikatlar reyestri (aniq topilmalar)

**Branch:** finzanjir-knowledge-audit-2026-11  
**Maqom:** dastlabki avtomatik matn taqqoslash; semantik ekspert ko‘rigi davom etadi.

## 1. V317 source archive — 7,053 yozuv

Takrorlangan ID: **0 ta**.

Normalizatsiya qilingan text maydoni bo‘yicha 2 ta aynan takror guruh (4 yozuv):

| Mazmun | 1-yozuv ID | 2-yozuv ID | Tavsiya |
|---|---|---|---|
| Risk Engine nima | mlq_23aef1293514a4a8 | HTML-Q-dc9797c26352cb14d8d2 | Bitta canonical ta’rifga bog‘lash mumkin; ikkala ID va source provenance saqlansin |
| Fraud Graph nima | mlq_d17d42035fdf1edb | HTML-Q-b192a16b977a7a77d0d8 | Bitta canonical ta’rifga bog‘lash mumkin; ikkala ID va source provenance saqlansin |

## 2. V317 Android active index — 4,671 yozuv

Takrorlangan ID: **0 ta**.

Normalizatsiya qilingan text maydoni bo‘yicha 3 ta aynan takror guruh (6 yozuv):

| Mazmun | 1-yozuv ID | 2-yozuv ID | Tavsiya |
|---|---|---|---|
| population | C24M-437c6a158087de | C24M-42c383cdae7fe7 | Til/domain/alias vazifasini tekshirib, faqat keyin canonical bog‘lash |
| migration | C24M-9328dfd2b4592a | C24M-a51bf4f3ba5cc0 | Til/domain/alias vazifasini tekshirib, faqat keyin canonical bog‘lash |
| cloud | C24M-d37cbf19583db9 | C24M-db8a506fd3a669 | Til/domain/alias vazifasini tekshirib, faqat keyin canonical bog‘lash |

## 3. Source archive va active index o‘rtasidagi takror/ko‘chirish aloqasi

- Normalizatsiya qilingan matn bo‘yicha **2,213** ta exact overlap.
- ID bo‘yicha **3,276** ta umumiy yozuv.
- Bu raqamlar source archive va active index orasidagi katta miqdordagi qayta ishlatilgan materialni ko‘rsatadi. Ular o‘z-o‘zidan xato dublikat degani emas: indeksda yozuv boshqa metadata, til, alias yoki retrieval vazifasiga ega bo‘lishi mumkin.
- Ko‘chirishda source_record_id, _merged_source_ids, _merged_source_files, provenance va original record ID’lar yo‘qotilmasin.

## 4. ZIP-1 DOCX ichidagi takrorlar

- 16 qatlam chuqur tushuntirish DOCX’ida bir xil “qatlamning amaldagi mavjudligi hujjat bilan tasdiqlanmagan” degan himoya jumlasi 16 qatlam kontekstida qayta ishlatilgan. Bu **mazmuniy takror, ammo funksional jihatdan qatlamga tegishli**. Har bir qatlam yozuvida saqlanishi yoki qatlamga alohida bog‘lanishi kerak; global bitta nusxaga siqib yuborilmasin.
- Signal reyestri, kichik signal va ilg‘or signal DOCX’larida muallif satri takrorlangan. Bu bilim mazmuni emas, hujjat metama’lumoti; har bir manbaning muallif metama’lumoti alohida qoladi.
- ZIP-1 hujjatlari orasidagi semantik yaqinlik/ziddiyatlar hali to‘liq tekshirilmagan. Hozircha “barcha dublikatlar topildi” degan da’vo yo‘q.

## 5. Birlashtirishdan oldingi majburiy himoya

1. Hech bir yozuv faqat o‘xshash ko‘ringani uchun o‘chirilmaydi.
2. Exact duplicate birlashtirilsa, barcha eski ID’lar canonical yozuvga alias/source relation sifatida biriktiriladi.
3. Til, domain, audience, access scope, vaqt, versiya va status farqi dublikat qaroriga ta’sir qiladi.
4. Qarama-qarshi bayonotlar duplicate emas; ular contradicts yoki supersedes munosabati bilan saqlanadi.
5. Har bir merge uchun oldingi va keyingi yozuvlar soni, ID xaritasi va checksum saqlanadi.
6. Importdan keyin source recordlar soni kamayishi mumkin bo‘lsa ham, hech qanday mazmun/manba yo‘qolmaganini merge ledger orqali tekshirish shart.
