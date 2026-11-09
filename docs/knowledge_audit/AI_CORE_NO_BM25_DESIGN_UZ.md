# FINZANJIR AI — BM25siz yengil lokal bilim yadrosi

Sana: 2026-11-10  
Branch: `ai-core-lightweight-fts4-2026-11-10`

## Maqsad
5 607 ta FINZANJIR bilim yozuvini telefon RAMiga katta obyektlar yoki vektor indekslari sifatida yuklamasdan, mahalliy manba sifatida ishlatish. Javob manba, versiya va approval maqomi bilan beriladi.

## BM25 o‘rniga
Yangi `FinzanjirKnowledgeBase.kt` BM25, embedding modeli, vector database yoki majburiy generativ model ishlatmaydi. U:
1. Asset SHA-256 va manifestdagi yozuvlar sonini tekshiradi.
2. JSONni Android `JsonReader` bilan oqim tarzida o‘qiydi.
3. Bir martalik importni app-private SQLite tranzaksiyasida bajaradi.
4. SQLite FTS4 `unicode61` indeksidan foydalanadi.
5. Har bir savolda kichik candidate to‘plamini oladi.
6. Eng ko‘pi bilan 4 ta dalil yozuvini sodda ibora/qamrov mosligi bilan tanlaydi.
7. Lokal javob yadrosi mos gaplarni birlashtiradi, manba va maqomni ko‘rsatadi.

FTS4 qidiruv mexanizmi, generativ AI modeli emas. Hozirgi javob sintezi deterministik/extractive lokal yadrodir; bu model fine-tuning yoki mustaqil katta til modeli degani emas.

## Telefon resurslari
- 5.4 MB JSON bir marta cache faylga oqim tarzida ko‘chiriladi va tekshiriladi.
- Butun korpus Kotlin obyektlari yoki token xaritalari sifatida RAMda ushlanmaydi.
- Savol bo‘yicha faqat cheklangan candidate qatorlar olinadi.
- Birinchi import va qidiruv `Dispatchers.IO` da, UI bosh threadidan tashqarida bajariladi.
- Asset hash jarayon davomida cache qilinadi.
- Manba matni SQLite `body` ustunida, FTS uchun normallashtirilgan nusxa alohida saqlanadi.
- Import soni yoki SHA mos kelmasa tranzaksiya rollback qilinadi.

## Bilim maqomi va chegaralar
- `candidate_not_authoritative`, `candidate`, `not_auto_promoted`, `unclassified` va `index_only` maqomlari ajratiladi.
- Alias/query-pattern yozuvlari javob dalili sifatida chiqarilmaydi.
- Muallif biografiyasi faqat bevosita muallif/asoschi savolida ochiladi.
- OCR yozuvi topilsa, vizual ekspert tekshiruvi kerakligi aytiladi.
- Takroriy matn javobda bir marta chiqishi mumkin; manba/provenance yo‘qolmaydi.
- “Shubhali ≠ firibgar/aybdor”. AI yakuniy bank, huquqiy yoki tergov qarorini bermaydi.
- Risk Engine, Fraud Graph, Timeline, Case Management, FIN-RECOVERY, ReCAL/recalibration va bank API haqidagi matnlar ularning hozir amalda ishlayotganini anglatmaydi. Ular konsepsiya, prototip yoki keyingi bosqich rejasidir; mutaxassislar tekshiruvi ko‘zda tutiladi.
- CVV, PIN, OTP, parol va maxfiy kalitlar bilim bazasiga kiritilmaydi.

## ReCAL va FIN-RECOVERY
Candidate korpusda “ReCAL” qisqartmasining mustaqil ta’rifi topilmadi. Risk modelini qayta kalibrlash (`recalibration`) haqida materiallar bor. `FIN-RECOVERY` esa hodisadan keyingi qonuniy recovery yo‘nalishi. Ularni tenglashtirmaslik kerak.

## Tekshiruv
2026-11-10 kuni candidate 5 607 yozuvli JSON ustida Python SQLite FTS5 simulyatsiyasi:
- 17/17 asosiy FINZANJIR savollarida mos yozuv topildi;
- 16 qatlam IDlari va umumiy katalog tekshirildi;
- muallif savoli alohida author-source yozuvlariga yo‘naltirildi;
- Risk Engine, Explainable Risk Score, Fraud Graph, Timeline, Case Management, FIN-RECOVERY, Human Review, bank integratsiyasi, OTP/CVV va prototip chegaralari sinovdan o‘tdi.
- Bu FTS5 simulyatsiyasi, Android qurilmadagi FTS4 runtime testi emas.
- Simulyatsiya SQLite bazasi taxminan 11.6 MB bo‘ldi; bu Android RAM o‘lchovi yoki kafolatlangan APK hajmi emas.

## Hozirgi GitHub holati
Branchda BM25siz SQLite FTS4 import/qidiruv va lokal javob sintezi kodi bor. Lekin aktiv `app/src/main/assets/finzanjir_knowledge.json` hali 1 121 yozuvli eski asset. 5 607 yozuvli candidate JSON SHA-256:

`f3457b372c5e7f79a0875603cb33987a7720f96061c1ac23ea038b69f2dfb250`

Asset GitHubga qo‘yilib, manifest hash/count moslashtirilmaguncha 5 607 aktiv deb e’lon qilinmaydi. Android runtime va real qurilma testi ham hali bajarilishi kerak.

## Tashqi manbalar
- Android SQLite performance: https://developer.android.com/topic/performance/sqlite-performance-best-practices
- Android Room FTS3/FTS4/FTS5: https://developer.android.com/training/data-storage/room/defining-data
- SQLite FTS3/FTS4: https://www.sqlite.org/fts3.html
- MobileRAG (2025): https://arxiv.org/abs/2507.01079
- Lightweight Chunk Selection for Mobile RAG (2026): https://arxiv.org/abs/2608.03148
- RAG context-size evaluation: https://aclanthology.org/2025.findings-naacl.375/
- Android WebView bridge security: https://developer.android.com/privacy-and-security/risks/insecure-webview-native-bridges
