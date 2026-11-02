from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Sarlavha
title = doc.add_heading("FINZANJIR: ILG'OR MIKRO-SIGNALLAR VA APP SCANNER'NING VAZIFASI", 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph("Versiya: 1.0 | Sana: 2026-yil")
doc.add_paragraph("Muallif: Salamat Smaylov Tangrbergen uli")
doc.add_paragraph("Hujjat turi: Qo'shimcha texnik reyestr (Kelajak rejasi / Version 2.0 uchun)")

doc.add_heading("1. Kirish: Nega bu signallar 'Ilg'or' hisoblanadi?", level=1)
doc.add_paragraph("Hozirgi 25 ta asosiy va kichik signallar (Tranzaksiya, Qurilma, Xulq-atvor) firibgarlikning 80% holatini qamrab oladi. Lekin professional firibgarlar doim yangi usullarni o'ylab topadi. Quyidagi 6 ta signal 'ilg'or' (advanced) hisoblanadi, chunki ularni aniqlash uchun telefonda maxsus ruxsatlar (Sensorlar, Ekran holati, Qurilma xavfsizligi) talab qilinadi.")
doc.add_paragraph("Muhim: Ushbu signallar hozirgi APK prototipida to'liq ishlamaydi. Ular FINZANJIR 2.0 versiyasida, banklar bilan huquqiy kelishuvdan so'ng joriy etiladi.")

doc.add_heading("2. 6 ta Ilg'or Mikro-Signal", level=1)

doc.add_heading("2.1. Xulq-atvor biometriyasi (Behavioral Biometrics)", level=2)
doc.add_paragraph("Kichik signal: Mijozning telefonda yozish tezligi, ekranga bosish kuchi yoki barmoq harakati odatdagidan keskin farq qiladi.", style='List Bullet')
doc.add_paragraph("Nega muhim? Firibgar telefonni qo'lga olgan bo'lsa ham, uning barmoq harakati va yozish uslubi boshqacha bo'ladi.", style='List Bullet')
doc.add_paragraph("Qanday aniqlanadi: Ilova sensorlari orqali (Foydalanuvchi ruxsati bilan).", style='List Bullet')

doc.add_heading("2.2. Soxta oyna (Overlay Attack)", level=2)
doc.add_paragraph("Kichik signal: Bank ilovasining ustidan boshqa soxta ilova oynasi ochilib qolishi.", style='List Bullet')
doc.add_paragraph("Nega muhim? Firibgarlar 'Sovg'a yutdingiz' deb soxta oyna chiqarib, mijozning karta ma'lumotlarini o'g'irlaydi.", style='List Bullet')
doc.add_paragraph("Qanday aniqlanadi: App Scanner orqali (Boshqa ilovalarning ekranga chizish ruxsatini tekshirish).", style='List Bullet')

doc.add_heading("2.3. Qabul qiluvchining 'qizib ketishi' (Receiver Velocity)", level=2)
doc.add_paragraph("Kichik signal: Pul yuborilayotgan hisobga oxirgi 5 daqiqada 10 ta turli odamdan pul tushmoqda.", style='List Bullet')
doc.add_paragraph("Nega muhim? Bu 'Money Mule' (pul yuvish uchun ishlatiladigan vositachi hisob) ning aniq belgisi.", style='List Bullet')
doc.add_paragraph("Qanday aniqlanadi: Banklararo Cross-Match va Fraud Graph orqali.", style='List Bullet')

doc.add_heading("2.4. Doimiy muvaffaqiyatsiz urinishlar (Brute Force)", level=2)
doc.add_paragraph("Kichik signal: 5 marta noto'g'ri parol, keyin 6-urinishda to'g'ri parol va darhol pul o'tkazish.", style='List Bullet')
doc.add_paragraph("Nega muhim? Akkauntni buzishga urinish yoki firibgar 'haqiqiy mijoz' bo'lib ko'rinishga harakat qilmoqda.", style='List Bullet')
doc.add_paragraph("Qanday aniqlanadi: Autentifikatsiya loglari orqali (SIG-012 bilan birga).", style='List Bullet')

doc.add_heading("2.5. Ekran yozib olish (Screen Recording / Mirroring)", level=2)
doc.add_paragraph("Kichik signal: Tranzaksiya paytida telefonda ekran yozib olish yoki ekranni boshqa qurilmaga uzatish yoqilgan.", style='List Bullet')
doc.add_paragraph("Nega muhim? Firibgarlar 'Telegram orqali video qo'ng'iroq qilib, ekranni ko'rsating' deb aldab, OTP va parollarni o'g'irlaydi.", style='List Bullet')
doc.add_paragraph("Qanday aniqlanadi: App Scanner orqali (Ekran yozib olish API sini tekshirish).", style='List Bullet')

doc.add_heading("2.6. Qurilmaning 'buzilganligi' (Root / Jailbreak)", level=2)
doc.add_paragraph("Kichik signal: Tranzaksiya amalga oshirilayotgan telefon Root (Android) yoki Jailbreak (iOS) qilingan.", style='List Bullet')
doc.add_paragraph("Nega muhim? Root qilingan telefonlarda zararli dasturlar bank ilovasidagi ma'lumotlarni yashirincha o'qib olishi mumkin.", style='List Bullet')
doc.add_paragraph("Qanday aniqlanadi: App Scanner orqali (Tizim fayllarini tekshirish).", style='List Bullet')

doc.add_heading("3. App Scanner nima uchun kerak? (Sizning savolingizga javob)", level=1)
doc.add_paragraph("Sizning prototipingizda 'App Scanner' (Ilova xavfsizlik skaneri) bor. Ko'pchilik buni oddiy antivirus deb o'ylaydi. Aslida, u quyidagi 4 ta ilg'or signalni aniqlash uchun maxsus yaratilgan xavfsizlik qalqonidir:")

doc.add_paragraph("1. Overlay Attack (Soxta oyna): Skaner qaysi ilova ekranga ruxsatsiz chizish (Draw over other apps) ruxsatini olganini tekshiradi.", style='List Bullet')
doc.add_paragraph("2. Screen Recording (Ekran yozish): Skaner qurilmada ekran yozib olish xizmati ishlayotganini aniqlaydi.", style='List Bullet')
doc.add_paragraph("3. Root / Jailbreak: Skaner telefonning xavfsizlik tizimi buzilganini (SU binary fayllari orqali) aniqlaydi.", style='List Bullet')
doc.add_paragraph("4. Ruxsatlar tahlili: Skaner bank ilovasiga aloqasi yo'q (masalan, mikrofon yoki kontaktlar) ruxsatlarni so'rayotgan shubhali ilovalarni aniqlaydi.", style='List Bullet')

doc.add_paragraph("Xulosa: App Scanner — bu FINZANJIRning 'ko'zi va qulog'i'. U tranzaksiya sodir bo'lishidan oldin qurilmaning xavfsizligini tekshiradi va ilg'or signallarni Risk Engine'ga uzatadi.")

doc.add_heading("4. Qachon joriy etiladi?", level=1)
doc.add_paragraph("Ushbu signallar hozirgi Android prototipida to'liq ishlamaydi. Ular FINZANJIR 2.0 (MVP va Pilot bosqichi) da joriy etiladi, chunki:")
doc.add_paragraph("• Maxfiylik: Xulq-atvor biometriyasi va ekran yozishni aniqlash uchun foydalanuvchidan aniq ruxsat olish kerak (Qonuniy jihatdan murakkab).", style='List Bullet')
doc.add_paragraph("• Texnik: Root aniqlash va Overlay tekshirish faqat real qurilmalarda ishlaydi, brauzerda emas.", style='List Bullet')
doc.add_paragraph("• Hamkorlik: Receiver Velocity faqat banklararo ma'lumot almashish (API) mavjud bo'lganda ishlaydi.", style='List Bullet')

doc.add_heading("5. Xulosa", level=1)
doc.add_paragraph("Hozirgi 25 ta signal banklar va investorlar uchun yetarli. Bu 6 ta ilg'or signal esa sizning tizimingizni raqobatchilardan ajratib turadigan 'premium' xususiyatdir. Ularni hujjatda 'Kelajak rejasi (v2.0)' deb belgilab qo'yish, sizning qanchalik chuqur o'ylashingizni ko'rsatadi.")

save_path = "/sdcard/Download/FINZANJIR_Ilgor_Signallar.docx"
doc.save(save_path)
print("MUVAFFAQIYATLI YARATILDI: " + save_path)
