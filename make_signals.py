from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Asosiy sarlavha
title = doc.add_heading("FINZANJIR: KICHIK SIGNALLAR VA ULARNING AHAMIYATI", 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph("Muallif: Salamat Smaylov Tangrbergen uli")
doc.add_paragraph("Sana: 2026-yil")
doc.add_paragraph("Hujjat turi: Texnik qo'llanma (barcha uchun tushunarli tilda)")

doc.add_heading("1. Kirish: Kichik signal nima?", level=1)
doc.add_paragraph("Kichik signal (yoki 'zaif signal' / 'secondary signal') — bu yakka o'zi hech narsani isbotlamaydigan, lekin boshqa signallar bilan birikganda firibgarlikni ochib beradigan mayda belgidir.")
doc.add_paragraph("FINZANJIR tamoyilida aytilishicha: 'Signal isbot emas'. Bitta katta signal (masalan, 50 million so'm o'tkazma) hamma e'tiborini tortadi. Lekin 'kichik signallar' (masalan, o'sha o'tkazmadan 5 daqiqa oldin parolning o'zgargani) soyada qoladi.")

doc.add_heading("2. Nega kichik signallar muhim?", level=1)
doc.add_paragraph("Firibgarlar 'birinchi' katta signalni yashirishga harakat qiladi, lekin ular 'ikkinchi' va 'uchinchi' kichik signallarni nazorat qila olmaydi. FINZANJIRning Fraud Graph va Cross-Match qatlamlari aynan shu kichik signallarni birlashtirib, butun tarmoqni ko'rsatadi.")

doc.add_heading("3. Kichik signallarning 10 ta amaliy misoli", level=1)

signals = [
    {
        "title": "1. Mikro-tranzaksiya (Kartani sinash)",
        "signal": "Firibgar o'g'irlangan kartadan 1000 so'm yoki 5000 so'm o'tkazadi.",
        "why_small": "Bu summa hech kimni xavotirga solmaydi.",
        "why_matters": "Firibgar kartani 'tirik' ekanini tekshiryapti. Agar o'tsa, 5 daqiqadan keyin 10 million so'm o'tkazadi.",
        "how": "SIG-001 (noodatiy summa) ishlamaydi, lekin Cross-Match orqali 'bu karta 5 daqiqada 2 marta ishlatildi' — bu naqsh (pattern) bo'ladi."
    },
    {
        "title": "2. Sessiya davomiyligi juda qisqa (Shoshilinchlik)",
        "signal": "Mijoz tizimga kirgandan so'ng 12 soniya ichida pul o'tkazdi.",
        "why_small": "Odam shunchaki tez ishlayotgan bo'lishi mumkin.",
        "why_matters": "Haqiqiy mijoz odatda summani o'ylaydi, hisob raqamini tekshiradi. Firibgar esa telefon qo'ng'irog'i paytida shoshilinch ravishda o'tkazadi.",
        "how": "SIG-011 (Rushed Session) + SIG-004 (Yangi qabul qiluvchi) = 80 ball."
    },
    {
        "title": "3. Parolni tiklashdan keyingi birinchi o'tkazma",
        "signal": "Mijoz SMS orqali parolni tiklab, 2 daqiqa ichida yirik pul o'tkazdi.",
        "why_small": "Parolni unutish — oddiy holat.",
        "why_matters": "Akkaunt egallash (ATO) ning klassik belgisi. Firibgar telefon raqamini nazoratga olib, parolni tiklaydi va darhol pulni olib qochadi.",
        "how": "SIG-012 (Parol tiklash + Pul) yakka o'zi 60 ball, lekin SIG-006 (Yangi qurilma) bilan biriksa 95 ball."
    },
    {
        "title": "4. Hisob raqamining 'yoshligi' (Account Age)",
        "signal": "Qabul qiluvchi hisob 3 kundan beri mavjud.",
        "why_small": "Yangi hisob ochish — qonuniy huquq.",
        "why_matters": "Firibgarlar pul yuvish uchun 'bir martalik' hisoblardan foydalanadi. Pul tushgach, hisobni tashlab ketadi.",
        "how": "SIG-013 (Shubhali qabul qiluvchi) — yangi hisob + yirik summa = Qizil bayroq."
    },
    {
        "title": "5. Limitdan past summalar (Structuring)",
        "signal": "Mijoz 3 marta 9,900,000 so'mdan o'tkazadi (10 million limitdan past).",
        "why_small": "Har bir tranzaksiya limitga mos.",
        "why_matters": "Bu 'Smurfing' — firibgarlar nazoratdan qochish uchun katta summani bo'lib-bo'lib o'tkazadi. Har bir o'tkazma alohida qonuniy ko'rinadi, lekin jami 30 million.",
        "how": "SIG-005 (Limitdan qochish) — vaqt oynasi (1 soat) ichida bir xil summadagi takrorlanish."
    },
    {
        "title": "6. Noodatiy qurilma tili (Language Change)",
        "signal": "Mijoz har doim o'zbek tilida ishlatadi, lekin bugun ilova rus yoki ingliz tilida ochilgan.",
        "why_small": "Tilni o'zgartirish — oddiy sozlama.",
        "why_matters": "Firibgar o'z telefonida ilovani o'z tiliga o'girib, keyin pul o'tkazadi. Yoki akkauntni boshqa davlatdan boshqarayotgan bo'lishi mumkin.",
        "how": "SIG-006 (Yangi qurilma) bilan birga kelganda kuchayadi."
    },
    {
        "title": "7. Bir xil IP manzildan ko'p kartalar",
        "signal": "Bitta Wi-Fi tarmog'idan (IP) 4 ta turli xil mijozlar pul o'tkazmoqda.",
        "why_small": "Oilaviy Wi-Fi bo'lishi mumkin.",
        "why_matters": "Firibgarlar 'call-center'larda ishlaydi — bir xonada 10-20 kishi turli kartalardan pul o'tkazadi.",
        "how": "SIG-008 (Bir qurilmada ko'p kartalar) — Fraud Graphdagi eng kuchli tugunlardan biri."
    },
    {
        "title": "8. Copy-Paste orqali kiritilgan karta raqami",
        "signal": "Mijoz karta raqamini qo'lda yozmay, nusxalab qo'ydi (agar ilova buni aniqlay olsa).",
        "why_small": "Ko'pchilik nusxalab qo'yadi.",
        "why_matters": "Firibgar Telegram'dan olingan karta raqamini nusxalab qo'yadi. Haqiqiy mijoz esa odatda o'z kartasini yod biladi.",
        "how": "SIG-011 (Shoshilinch sessiya) bilan biriksa — naqsh paydo bo'ladi."
    },
    {
        "title": "9. Tranzaksiya vaqti va mijozning odatiy faolligi",
        "signal": "Mijoz 6 oy davomida faqat kunduzi 09:00-18:00 orasida ishlagan. Bugun soat 03:14 da pul o'tkazdi.",
        "why_small": "Tungi o'tkazma taqiqlanmagan.",
        "why_matters": "Firibgar boshqa vaqt zonasida yoki mijoz uxlayotganda ishlaydi.",
        "how": "SIG-010 (Noodatiy vaqt) — Behavioral Analytics qatlami."
    },
    {
        "title": "10. Telefon raqamining o'zgarishi (SIM Swap belgisi)",
        "signal": "Mijozning profildagi telefon raqami 1 soat oldin o'zgartirilgan.",
        "why_small": "Raqam o'zgartirish — qonuniy amal.",
        "why_matters": "SIM-Swap firibgarligida firibgar operatorga borib, 'telefonimni yo'qotdim' deb yangi SIM oladi. Keyin barcha SMS-kodlar unga keladi.",
        "how": "SIG-012 (Parol tiklash) + telefon o'zgarishi + yangi qurilma = 100 ball (CRITICAL)."
    },
]

for s in signals:
    doc.add_heading(s["title"], level=2)
    doc.add_paragraph("Kichik signal: " + s["signal"], style="List Bullet")
    doc.add_paragraph("Nega kichik? " + s["why_small"], style="List Bullet")
    doc.add_paragraph("Nega muhim? " + s["why_matters"], style="List Bullet")
    doc.add_paragraph("FINZANJIR qanday ko'radi? " + s["how"], style="List Bullet")

doc.add_heading("4. Signallar kombinatsiyasi: Qanday qilib ular 'katta' bo'ladi?", level=1)
doc.add_paragraph("Bitta signal hech qachon firibgarlikni isbotlamaydi. Lekin 3 ta signal birga kelganda, Risk Engine ularni birlashtirib, yuqori ball beradi.")

doc.add_heading("4.1. Jadval: Signal kombinatsiyalari", level=2)
table = doc.add_table(rows=1, cols=4)
table.style = "Table Grid"
hdr = table.rows[0].cells
hdr[0].text = "Bitta signal (past xavf)"
hdr[1].text = "Ball"
hdr[2].text = "3 ta signal birga"
hdr[3].text = "Natija"

data = [
    ("Yangi qurilma", "20 ball", "Yangi qurilma + Parol tiklash + Tungi vaqt", "85 ball (Case ochiladi)"),
    ("Kichik o'tkazma", "10 ball", "Kichik o'tkazma + 2 daqiqadan keyin katta + Yangi qabul qiluvchi", "90 ball (Bloklash)"),
    ("Yangi qabul qiluvchi", "15 ball", "Yangi qabul qiluvchi + Bir xil IP + 3 ta karta", "95 ball (Fraud Graph)"),
]
for r in data:
    row = table.add_row().cells
    for i, item in enumerate(r):
        row[i].text = item

doc.add_heading("5. Xulosa", level=1)
doc.add_paragraph("Firibgarlar 'birinchi' katta signalni yashirishga harakat qiladi, lekin 'ikkinchi' va 'uchinchi' kichik signallarni nazorat qila olmaydi.")
doc.add_paragraph("Sizning Fraud Graph va Cross-Match qatlamlaringiz aynan shu kichik signallarni birlashtirib, 'birinchi astronom' ortidagi butun tarmoqni ko'rsatadi.")
doc.add_paragraph("Asosiy qoida: Kichik signallar — bu firibgarlikning barmoq izlari. Ularni birma-bir emas, birgalikda o'qish kerak.")

doc.add_heading("6. Keyingi qadamlar", level=1)
doc.add_paragraph("1. Ushbu 10 ta signalni Signal Reyestriga (FINZANJIR_Signal_Reyestri.docx) qo'shish.")
doc.add_paragraph("2. Har bir signal uchun bankdan qanday ma'lumot olish mumkinligini aniqlashtirish.")
doc.add_paragraph("3. Risk Engine formulasida bu signallarning vaznini (ballini) belgilash.")
doc.add_paragraph("4. Prototipda bu signallarni 'Shadow Mode' (kuzatish rejimi) da sinab ko'rish.")

save_path = "/sdcard/Download/FINZANJIR_Kichik_Signallar.docx"
doc.save(save_path)
print("MUVAFFAQIYATLI YARATILDI: " + save_path)
