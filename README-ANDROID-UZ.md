# FINZANJIR Android — ochiq mutaxassislar prototipi

Ishchi branch: `finzanjir-android-v1`. Asosiy FINZANJIR V3/V4 branchlari o‘zgartirilmaydi.

## Android foundation
- Kotlin + Jetpack Compose.
- Cloud build: GitHub Actions, JDK 17, Gradle 8.9.
- Ekranlar: Bosh sahifa, Jarayon, Signallar, 16 qatlam, Case, Human Review, AI yordamchi, Cheklovlar. Barcha ekranlar umumiy navigatsiyadan ochiladi.
- Alohida muallif-only panel yo‘q; barcha bo‘limlar va bilim qidiruvi tashrif buyuruvchilar uchun ochiq.
- Barcha ekranlar yuqori bo‘lim navigatsiyasidan ochiladi; pastki navigatsiya asosiy to‘rtta bo‘limni ham beradi.
- API kalitlari APK yoki repository ichiga joylanmaydi.

## Bilimlar bazasi
- Android assets ichida 1,121 ta strukturali yozuv mavjud: V4 korpusidagi 957 yozuv + V14 original PDFning 164 sahifa yozuvi.
- Har bir V14 sahifa yozuvida original PDF sahifasi, source_id, source_version, source_section, source_path va candidate maqomi saqlanadi.
- Qidiruv BM25-uslubidagi term weighting, o‘zbek lotin/kirill normallashtirish, fuqaro/mutaxassis ko‘rinishi, manba izlari va aynan takror matnni javobda bir marta ko‘rsatishni qo‘llaydi. Korpusdagi asl yozuvlar va ularning provenance izlari o‘chirilmaydi.
- Barcha yozuvlar `candidate_not_authoritative`; qidiruv mosligi faktik to‘g‘rilik yoki ekspert tasdig‘i emas.
- 16 qatlam bo‘yicha umumiy so‘rov barcha 16 qatlam yozuvini qaytaradi; alohida L01–L16 so‘rovi qatlam ID bo‘yicha izlaydi.

## Hali mavjud bo‘lmagan manbalar va cheklovlar
- Asl V8 bank texnik arxitektura PDFsi ushbu branchdagi manba fayllari orasida topilmadi. V14/V8 taqqoslash auditi mavjud, lekin u original V8 o‘rnini bosmaydi.
- FINZANJIR AI v0.6.0 ZIP va uning original registry fayllari ushbu repository/library snapshotida topilmadi. V4 korpusi to‘liq AI ZIP deb ko‘rsatilmaydi.
- V14 matn sahifalar bo‘yicha import qilindi. 5,607 yozuvli candidate ichida 27 ta vizual OCR yozuvi ham bor; ular candidate maqomida va vizual ekspert tekshiruvini kutadi.
- Bank API, real mijoz ma’lumotlari, production autentifikatsiya/RBAC va bank muhitidagi sinovlar ulanmagan.
- FINZANJIR karta, hisob yoki tranzaksiyani avtomatik bloklamaydi. Signal yoki Case aybdorlik hukmi emas. Human Review vakolati saqlanadi.

## Build maqomi
GitHub Actions build muvaffaqiyati faqat shu commitning APK kompilyatsiyasi va artifact chiqarilishini tasdiqlaydi. U real qurilmada o‘rnatish, barcha ekranlarning UX sinovi, bank integratsiyasi yoki production tayyorligini isbotlamaydi.

## 2026-11-09 bilim migratsiyasi branchi
- Branch: `ai-knowledge-foundation-2026-11-09`.
- Candidate korpus: 5,607 yozuv; AI v2.1 dagi 4,656 ID to‘liq saqlangan.
- SHA-256: `f3457b372c5e7f79a0875603cb33987a7720f96061c1ac23ea038b69f2dfb250`.
- GitHub Actions Android debug APK build muvaffaqiyatli; bu 1,121 yozuvli aktiv asset bilan build, 5,607 yozuvli candidate qurilmada hali sinovdan o‘tmagan.
- To‘liq assetni branchga ko‘chirish va hash/record count tekshiruvi uchun issue: https://github.com/qwerasdfzxc0311/finzanjir-app/issues/2.
