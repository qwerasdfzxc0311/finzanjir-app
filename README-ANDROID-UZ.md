# FINZANJIR Android — ochiq mutaxassislar prototipi

Ishchi branch: `finzanjir-android-v1`. Asosiy FINZANJIR V3/V4 branchlari o‘zgartirilmaydi.

## Android foundation
- Kotlin + Jetpack Compose.
- Cloud build: GitHub Actions, JDK 17, Gradle 8.9.
- Ekranlar: Bosh sahifa, Jarayon, Signallar, 16 qatlam, Case, Human Review, AI yordamchi, Cheklovlar. Barcha ekranlar umumiy navigatsiyadan ochiladi.
- Alohida muallif-only panel yo‘q; barcha bo‘limlar va bilim qidiruvi tashrif buyuruvchilar uchun ochiq.
- Barcha ekranlar yuqori bo‘lim navigatsiyasidan ochiladi; pastki navigatsiya asosiy to‘rtta bo‘limni ham beradi.
- API kalitlari APK yoki repository ichiga joylanmaydi.


## Yagona bog‘langan jarayon — integratsiya bosqichi 1
- Fuqaro murojaati, avtomatik demo-signal, Case reyestri, Human Review, tuzatish so‘rovi, mock bank so‘rovi/javobi va audit tarixi bitta Case ID atrofida bog‘landi.
- Case holati va voqealar tarixi ilova qurilmasidagi SharedPreferences ichida saqlanadi; ilova qayta ochilganda demo Case'lar saqlanib qoladi.
- “Jarayon”, “Signallar”, “Case”, “Human Review” va “Yagona tizim” navigatsiyalari bir xil workflow ma’lumotlariga olib boradi.
- Signal yaratish hozircha sodda, izohlanadigan demo qoidalariga asoslangan; u real firibgarlikni aniqlash modeli yoki kalibrlangan Risk Score emas.
- Bank adapteri hozircha faqat lokal mock so‘rov/javobni qayd etadi. Hech qanday bankka tarmoq so‘rovi yuborilmaydi.
- Hozircha production autentifikatsiya, server RBAC, shifrlangan server audit jurnali, real bank API, push-xabarnoma va ko‘p qurilmali sinxronlash mavjud emas. Maxfiy yoki to‘lov ma’lumotlarini demo maydonlariga kiritmang.
- Bu bosqich modullarni umumiy Case holatiga ulaydi; keyingi bosqichlarda rolga mos ish maydonlari, dalil/qarshi dalil obyektlari, signal reyestri, server API kontrakti va avtomatlashtirilgan testlar qo‘shilishi kerak.

## Bilimlar bazasi
- Android assets ichida 1,121 ta strukturali yozuv mavjud: V4 korpusidagi 957 yozuv + V14 original PDFning 164 sahifa yozuvi.
- Har bir V14 sahifa yozuvida original PDF sahifasi, source_id, source_version, source_section, source_path va candidate maqomi saqlanadi.
- Qidiruv o‘zbek lotin/kirill yozuvlarini normallashtiradi va topilgan yozuvlarning manba izini ko‘rsatadi.
- Barcha yozuvlar `candidate_not_authoritative`; qidiruv mosligi faktik to‘g‘rilik yoki ekspert tasdig‘i emas.
- 16 qatlam bo‘yicha umumiy so‘rov barcha 16 qatlam yozuvini qaytaradi; alohida L01–L16 so‘rovi qatlam ID bo‘yicha izlaydi.

## Hali mavjud bo‘lmagan manbalar va cheklovlar
- Asl V8 bank texnik arxitektura PDFsi ushbu branchdagi manba fayllari orasida topilmadi. V14/V8 taqqoslash auditi mavjud, lekin u original V8 o‘rnini bosmaydi.
- FINZANJIR AI v0.6.0 ZIP va uning original registry fayllari ushbu repository/library snapshotida topilmadi. V4 korpusi to‘liq AI ZIP deb ko‘rsatilmaydi.
- V14 matn sahifalar bo‘yicha import qilindi; diagrammalar, rasm va murakkab jadvallar alohida vizual tekshiruv talab qiladi.
- Bank API, real mijoz ma’lumotlari, production autentifikatsiya/RBAC va bank muhitidagi sinovlar ulanmagan.
- FINZANJIR karta, hisob yoki tranzaksiyani avtomatik bloklamaydi. Signal yoki Case aybdorlik hukmi emas. Human Review vakolati saqlanadi.

## Build maqomi
GitHub Actions build muvaffaqiyati faqat shu commitning APK kompilyatsiyasi va artifact chiqarilishini tasdiqlaydi. U real qurilmada o‘rnatish, barcha ekranlarning UX sinovi, bank integratsiyasi yoki production tayyorligini isbotlamaydi.
