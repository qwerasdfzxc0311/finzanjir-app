# FINZANJIR — ZIP manbalari chuqur auditi (oraliq hisobot)

**Sana:** 2026-11-09  
**Branch:** `finzanjir-knowledge-audit-2026-11`  
**Maqom:** audit natijasi; bilim integratsiyasi hali bajarilmadi.

## 1. O‘zgarmas talab

Asl manbalar qisqartirilmaydi yoki almashtirilmaydi. Yangi bilim yozuvlari manbaga bog‘langan hosila yozuvlar bo‘ladi. Bir xil mazmun takror uchrasa, manba havolalari birlashtiriladi, ammo turli kontekst, versiya, tasdiq holati yoki qarama-qarshi mazmun o‘chirilmaydi. Audit tugamaguncha faol Android bilim bazasi va ilova kodi o‘zgartirilmaydi.

## 2. ZIP-1 — manbalar inventari

Arxivda 20 ta element bor: 14 ta hujjat va 6 ta rasm/brend materiali. Tekshirilgan hujjatlar:

| Manba | Hajm / tarkib | Dastlabki holat |
|---|---:|---|
| FINZANJIR KONSEPSIYA V14 | PDF, 164 sahifa | Asosiy konsepsiya; sahifa matni va vizual obyektlar alohida tekshiruvga muhtoj |
| 16 qatlam chuqur tushuntirish V3 | DOCX, 305 paragraf, 3 jadval / 24 qator | Qatlamlarning maqsadi, chegarasi, xato holati, test va ustuvorliklari |
| 16 qatlam talablar va sinovlar reyestri V1 | PDF, 4 sahifa | REQ-001…REQ-024, TEST-001…TEST-024, DEC-01…DEC-10 |
| Signal reyestri V1 | DOCX, 4 jadval / 19 qator | 15 asosiy signalga oid reyestr va eski risk qoidalari |
| Kichik signallar | DOCX, 72 paragraf, 1 jadval | 10 ta ikkilamchi signal; misollar amaldagi tasdiqlangan qoida emas |
| Ilg‘or signallar | DOCX, 46 paragraf | 6 ta ilg‘or signal; kelajak/2.0 va ruxsat talab qiluvchi imkoniyatlar |
| Qo‘shimcha amaliy talablar | PDF, 19 sahifa | Mundarijadagi 1–18 bo‘limdan tashqari 18–36 kengaytirilgan bo‘limlar ham mavjud |
| Qo‘shimcha FDP ishchi nusxasi | DOCX, 144 paragraf, 3 jadval / 25 qator | Kuzatuv, eshitilgan da’vo, gipoteza, taklif va tekshirish zarurati ajratilgan |
| Fuqaro xavfsizligi FDP | DOCX, 186 paragraf | Fuqaro ilovasi, hamkor bank kartalari, “Men bu kartani tanimayman”, vakolatlar va Case |
| False-positive ekspertiza tuzatishi V2 | DOCX, 52 paragraf | Shadow mode, canary, circuit breaker/karantin, kill switch, rollback, inson/bank nazorati |
| Bank integratsiyasi texnik arxitekturasi V1.0 | PDF, 66 sahifa | Taklif etilgan API, xabar, autentifikatsiya, idempotency, retry, audit, xavfsizlik va tiklash |
| AI va bilim tizimi — 5 hujjat | PDF, 29 sahifa | AI ichki oqimi, KB/memory, mustaqil baholash, xato tuzatish, xavfsizlik |
| FINZANJIR taqdimoti | PPTX, 17 slayd | Qisqa taqdimot; mustaqil texnik manba emas, konsepsiya chegaralarini ko‘rsatadi |
| Tarixiy ishchi hujjat | PDF, 22 sahifa | Tarixiy/arxiv qatlamida saqlanadi; faol FINZANJIR mazmuniga avtomatik qo‘shilmaydi |

### Muhim topilmalar

- 16 qatlam reyestrida 24 talab va 24 test identifikatori, shuningdek 10 ochiq qaror mavjud. Bu testlar bajarilgan degani emas.
- Qo‘shimcha amaliy talablar PDF’ida mundarija 18 bandda tugaydi, lekin hujjat 36-bandgacha davom etadi. 19 sahifani to‘liq import qilmasdan faqat mundarijadan nusxa olish katta mazmun yo‘qotishiga olib keladi.
- 16 qatlam DOCX’ida “qatlamning amalda mavjudligi hujjat bilan tasdiqlanmagan” degan ehtiyot bayonoti 16 marta takrorlangan. Bu tasodifiy dublikat emas: har bir qatlamning o‘z kontekstida takrorlangan himoya izohi; har bir qatlam bilan saqlanishi kerak.
- Signal hujjatlaridagi ball va bloklashga o‘xshash misollarni faol avtomatik qoida deb qabul qilmaslik kerak. False-positive V2 hujjati operatsion xavfsizlik bo‘yicha keyingi tuzatish sifatida alohida bog‘lanadi; eski matn arxiv/versiya sifatida qoladi.
- Taqdimotdagi “Silent Hold” ifodasi bank vakolatiga zid talqin qilinishi mumkin. Aniq huquqiy/operatsion qaror bo‘lmaguncha bloklash yoki to‘lovni ushlab qolish funksiyasi sifatida talqin qilinmaydi.
- V14 ichidagi SINBAD/ATMOS tilga olingan bo‘lim faol FINZANJIR bilimlar to‘plamiga qo‘shilmaydi; manbaning o‘zi arxivda saqlanadi.
- Muallifning shaxsiy profil/aloqa ma’lumotlari ommaviy AI qidiruviga avtomatik chiqarilmaydi. Mualliflik hissasi va shaxsiy ma’lumotga kirish alohida boshqariladi.

## 3. ZIP-2 — V317 arxivi va indeks auditi

Tekshirilgan arxiv tarkibi:

- 224 fayl.
- `unified_candidate_cards_full_source.json`: 7,053 yozuv.
- Android ichidagi `unified_knowledge_index.json`: 4,671 yozuv.
- Ikki JSON ro‘yxatida ham takrorlangan ID topilmadi.
- Source archive’da normalizatsiya qilingan matn bo‘yicha 2 ta aynan takror guruh (jami 4 yozuv) aniqlandi: “Risk Engine nima” va “Fraud Graph nima” juftlari.
- Active index’da 3 ta aynan takror guruh (jami 6 yozuv) aniqlandi: population, migration va cloud ifodalarining takrorlari.
- Source archive va active index o‘rtasida 2,213 ta normalizatsiya qilingan matn mosligi bor; 3,276 ta ID ikkala ro‘yxatda ham uchraydi. Bu import/hosila aloqalarini ko‘rsatadi, ammo barcha 4,671 yozuvning hammasi kerak yoki to‘g‘ri degani emas.
- Active index’dagi metadata to‘liqligi notekis: 860 yozuvda `kind/authority/approval/language` maydonlari yo‘q; 1,070 yozuv `unclassified_knowledge_record`; 540 domain `unclassified`; 1,681 til `und`.
- Active index’da 515 umumiy ensiklopediya yozuvi bor; ular FINZANJIR maxsus firibgarlik/bank qoidalari bilan aralashtirilmaydi.
- 2,000 regression savol/tarix yozuvlari test korpusi bo‘lib qoladi, faol javob bilimiga ko‘chirilmaydi.
- V317’da 188 `authoritative_project_source` turidagi yozuv borligi ularning hammasi mustaqil ekspert yoki bank tomonidan tasdiqlanganini anglatmaydi; har birining provenance va approval maydoni alohida tekshiriladi.
- 15 `verified_source_candidate` huquqiy matn yozuvi ham amaldagi huquqiy maslahat sifatida berilishidan oldin rasmiy manbada qayta tekshirilishi kerak.

## 4. ZIP-1 va ZIP-2 o‘rtasidagi dublikat siyosati

Dublikatlarni uch darajada ajratamiz:

1. **Aynan bir xil matn:** bitta canonical bilim yozuvi, barcha source ID/path/page/section havolalari saqlanadi.
2. **Mazmunan yaqin, lekin konteksti/versiyasi farqli:** yozuvlar o‘chirilmaydi; `related_to`, `supports`, `contradicts` yoki `supersedes` aloqasi bilan bog‘lanadi.
3. **Zid yoki keyin tuzatilgan mazmun:** ikkala manba ham saqlanadi; qaysi biri keyingi tuzatish, qaysi biri eski taklif ekani status va sana bilan ko‘rsatiladi. Avtomatik ravishda “eng yangi”ni haqiqat deb qabul qilinmaydi.

## 5. Android’dagi hozirgi import bilan solishtirish

Android branch manifestida 1,121 yozuv ko‘rsatilgan: 957 V4 korpus yozuvi + V14 PDF’ning 164 sahifa yozuvi. Barcha yozuvlar `candidate_not_authoritative`. ZIP-1’dagi alohida FDP, signal, 16 qatlam, texnik arxitektura va 5 AI hujjatining to‘liq manba matni alohida-alohida import qilingani tasdiqlanmadi. V317’dagi 4,671 yozuv ham Android branchga to‘liq integratsiya qilinmagan.

Manifestdagi `branch` maydoni `finzanjir-v4-unified-workflow-uz` deb turibdi, holbuki tekshirilayotgan Android branch `finzanjir-android-v1`. Bu metadata xatosi sifatida qayd etildi; hozircha tuzatilmaydi.

## 6. Keyingi bajariladigan ishlar

1. Har bir PDF sahifasidagi jadval/diagramma/rasmni vizual tekshirish va sahifa identifikatorini saqlash.
2. Har bir DOCX paragrafi va jadval qatorini source ID bilan inventarizatsiya qilish.
3. ZIP-1 manbalarini Android 1,121 yozuvi, V317 4,671 indeks va 7,053 source archive bilan item-by-item solishtirish.
4. Exact duplicate, near duplicate, contradiction va supersession reyestrlarini tayyorlash.
5. Asl hujjatlar uchun o‘zgarmas source snapshot, hosila knowledge chunks va crosswalk formatini yaratish.
6. Manba to‘liqligi va checksum nazoratidan keyingina alohida integratsiya rejasini ko‘rsatish.

**Hisobot yakuniy integratsiya emas. Bu hisobotdagi sanash va dublikat tahlili matn/JSON darajasidagi tekshiruvdir; PDF rasmlari, murakkab jadvallar va semantik dublikatlar hali alohida ko‘rik talab qiladi.**
