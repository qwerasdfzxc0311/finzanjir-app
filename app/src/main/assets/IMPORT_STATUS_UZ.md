# FINZANJIR Android — bilimlar korpusi importi

Bu papkadagi korpus FINZANJIR V4 branchida mavjud bo‘lgan 957 ta strukturali yozuvdan olindi.

- `finzanjir_knowledge.json`: 957 ta yozuv; har bir yozuvda ID, matn, maqom, source_id, source_version, source_section, source_path va record_type maydonlari mavjud.
- `knowledge_manifest.json`: korpus tarkibi, manbalar, ma’lum bo‘shliqlar va maxfiylik doirasi.
- `16_layer_catalog.md`: 16 qatlamning manbaga asoslangan nomlari va talab tavsifi.

## Muhim maqom

Barcha 957 yozuv `candidate_not_authoritative`. Ular bank tomonidan tasdiqlangan qoida yoki amalda ishlayotgan mexanizm deb talqin qilinmaydi.

## Import chegaralari

Bu import asl V14 PDF, V8 texnik arxitektura PDF va FINZANJIR AI v0.6.0 ZIP arxivlarining to‘liq importi emas. V4 manifestida qayd etilganidek, asl V14/V8 alohida sahifa-paragraf crosswalk bilan to‘liq import qilinmagan, AI v0.6.0 ZIP esa ushbu repository snapshotida mavjud emas. To‘liq asl arxivlar olinib, tekshirilgach, manba xaritasi bilan qo‘shimcha import qilinishi kerak.

Shaxsiy muallif biografiyasi va shaxsiy tarix ommaviy bilim korpusiga kiritilmaydi.

## Android qidiruvi

Android ilovasi ushbu JSON faylni lokal assets ichidan o‘qiydi. Qidiruv o‘zbek lotin/kirill yozuvlarini soddalashtirib normallashtiradi, mos yozuvlarni topadi va manba/versiya/bo‘lim/maqomni ko‘rsatadi. Qidiruv reytingi faktik ishonchlilik yoki ekspert tasdig‘i emas.
