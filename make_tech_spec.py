from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# ================= SARLAVHA =================
title = doc.add_heading("FINZANJIR: TEXNIK TOPSHIRIQ (TECH SPEC)", 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph("Versiya: 1.0 | Sana: 2026-yil")
doc.add_paragraph("Muallif: Salamat Smaylov Tangrbergen uli")
doc.add_paragraph("Hujjat maqomi: Amaliy texnik topshiriq (WIP). Ushbu hujjat banklar, investorlar va dasturchilar uchun mo'ljallangan.")

doc.add_heading("Mundarija", level=1)
doc.add_paragraph("1. Loyiha haqida umumiy ma'lumot")
doc.add_paragraph("2. Asosiy tamoyillar")
doc.add_paragraph("3. Signal Reyestri (Asosiy va Kichik signallar)")
doc.add_paragraph("4. Risk Engine Qoidalari (Ball qo'yish tizimi)")
doc.add_paragraph("5. Fuqaro va Xodimlar Xavfsizligi (Asosiy talablar)")
doc.add_paragraph("6. Sinov Ssenariylari")
doc.add_paragraph("7. Keyingi qadamlar va Ochiq masalalar")

# ================= 1-QISM =================
doc.add_heading("1. Loyiha haqida umumiy ma'lumot", level=1)
doc.add_paragraph("FINZANJIR — fuqarolar, banklar va to'lov infratuzilmasi uchun raqamli moliyaviy xavfsizlik platformasi. Uning asosiy maqsadi — firibgarlikni erta aniqlash, xavfni tahlil qilish, ogohlantirish va qonuniy javob choralarini ko'rish.")
doc.add_paragraph("Muhim: FINZANJIR bank o'rniga qaror chiqarmaydi va kartani o'zi bloklamaydi. 'Bloklandi' holati faqat tekshirilgan bank tasdig'i bilan ko'rsatiladi.")

doc.add_heading("2. Asosiy tamoyillar", level=1)
principles = [
    "Signal ≠ firibgarlik isboti.",
    "Risk balli ≠ aybdorlik.",
    "Case ≠ hukm.",
    "Fraud grafigi ≠ aybdorlik isboti.",
    "AI yakuniy qaror qabul qiluvchi emas.",
    "Har bir muhim ma'lumotning manbasi, vaqti va o'zgarish tarixi kuzatilishi kerak.",
    "Fuqaroda noto'g'ri ma'lumotni tuzatish va shikoyat qilish yo'li bo'lishi kerak.",
    "'100% firibgarlikni to'xtatadi' kabi kafolatlar berilmaydi."
]
for p in principles:
    doc.add_paragraph(p, style='List Bullet')

# ================= 3-QISM =================
doc.add_heading("3. Signal Reyestri", level=1)

doc.add_heading("3.1. Asosiy Signallar (15 ta)", level=2)
table1 = doc.add_table(rows=1, cols=5)
table1.style = "Table Grid"
hdr = table1.rows[0].cells
hdr[0].text = "Signal ID"
hdr[1].text = "Signal Nomi"
hdr[2].text = "Mantiq"
hdr[3].text = "Manba Darajasi"
hdr[4].text = "Ssenariy"

data1 = [
    ("SIG-001", "Noodatiy summa", "O'rtachadan 5-10 baravar katta", "Tier 1", "ATO"),
    ("SIG-002", "Yuqori tezlik", "1 daqiqada 3+ tranzaksiya", "Tier 1", "Karta firibgarligi"),
    ("SIG-003", "Pul o'tishi (In-Out)", "Pul tushib, 1-2 daqiqada chiqishi", "Tier 1", "Money Mule"),
    ("SIG-004", "Yangi qabul qiluvchi", "Ilgari ishlatilmagan hisob", "Tier 1/2", "ATO, Aldov"),
    ("SIG-005", "Limitdan qochish", "Bo'lib-bo'lib o'tkazish", "Tier 1", "Pul yuvish"),
    ("SIG-006", "Yangi qurilma", "Noodatiy telefon/kompyuter", "Tier 2", "ATO"),
    ("SIG-007", "Geo-anomaliya", "Impossible Travel", "Tier 2", "Karta firibgarligi"),
    ("SIG-008", "Bir qurilmada ko'p kartalar", "1 ta telefondan 3+ karta", "Tier 2", "Pul yuvish"),
    ("SIG-009", "VPN/Proxy/Tor", "Anonim tarmoq", "Tier 2/3", "Karta firibgarligi"),
    ("SIG-010", "Noodatiy vaqt", "Tungi soat 03:00", "Tier 1", "ATO"),
    ("SIG-011", "Shoshilinch sessiya", "10-15 soniyada pul o'tkazish", "Tier 2", "Ijtimoiy injiniring"),
    ("SIG-012", "Parol tiklash + Pul", "Parol tiklab, darhol pul o'tkazish", "Tier 2", "ATO"),
    ("SIG-013", "Shubhali qabul qiluvchi", "Qora ro'yxatdagi hisob", "Tier 3", "Aldov, Pul yuvish"),
    ("SIG-014", "Umumiy atributlar", "Bir xil telefon/qurilma", "Tier 2/3", "Firibgarlar tarmog'i"),
    ("SIG-015", "Halqa (Circular)", "A->B->C->A pul aylanishi", "Tier 3", "Pul yuvish"),
]
for r in data1:
    row = table1.add_row().cells
    for i, item in enumerate(r):
        row[i].text = item

doc.add_heading("3.2. Kichik Signallar (10 ta)", level=2)
table2 = doc.add_table(rows=1, cols=4)
table2.style = "Table Grid"
hdr2 = table2.rows[0].cells
hdr2[0].text = "Signal Nomi"
hdr2[1].text = "Kichik Signal"
hdr2[2].text = "Nega Muhim?"
hdr2[3].text = "FINZANJIR Qanday Ko'radi?"

data2 = [
    ("Mikro-tranzaksiya", "1000 so'm o'tkazma", "Kartani sinash", "Cross-Match: 5 daqiqada 2 marta"),
    ("Qisqa sessiya", "12 soniyada pul o'tkazish", "Shoshilinchlik (aldov)", "SIG-011 + SIG-004 = 80 ball"),
    ("Parol tiklash + Pul", "Parol tiklab, 2 daqiqada pul", "ATO klassik belgisi", "SIG-012 + SIG-006 = 95 ball"),
    ("Yangi hisob", "3 kunlik hisob", "Pul yuvish uchun", "SIG-013 + katta summa"),
    ("Limitdan past summalar", "3 marta 9,9 mln", "Smurfing", "SIG-005: 1 soatda takrorlanish"),
    ("Noodatiy til", "Rus/ingliz tili", "Firibgar o'z tiliga o'zgartirgan", "SIG-006 bilan birga"),
    ("Bir xil IP", "4 ta karta bitta Wi-Fi", "Call-center", "SIG-008: Fraud Graph"),
    ("Copy-Paste", "Karta raqami nusxalangan", "Telegram'dan olingan", "SIG-011 bilan birga"),
    ("Noodatiy vaqt", "03:14 da pul", "Mijoz uxlayotganda", "SIG-010: Behavioral Analytics"),
    ("Telefon o'zgarishi", "1 soat oldin raqam o'zgargan", "SIM-Swap", "SIG-012 + yangi qurilma = 100 ball"),
]
for r in data2:
    row = table2.add_row().cells
    for i, item in enumerate(r):
        row[i].text = item

# ================= 4-QISM =================
doc.add_heading("4. Risk Engine Qoidalari (Ball qo'yish tizimi)", level=1)
doc.add_paragraph("Tizim bitta signalga emas, balki ularning kombinatsiyasiga qarab qaror qabul qiladi.")
doc.add_paragraph("Qoida 1 (Kritik xavf): Agar SIG-006 + SIG-001 + SIG-004 bir vaqtda kelsa -> Risk Score = 85 (HIGH). Tizim avtomatik Case ochadi va Human Review'ga yuboradi.", style='List Bullet')
doc.add_paragraph("Qoida 2 (Past xavf): Agar faqat SIG-002 kelsa -> Risk Score = 30 (LOW). Faqat kuzatiladi (Shadow mode).", style='List Bullet')
doc.add_paragraph("Qoida 3 (Pul yuvish): Agar SIG-003 + SIG-008 kelsa -> Risk Score = 90 (CRITICAL). Darhol tekshiruvga yuboriladi.", style='List Bullet')

# ================= 5-QISM =================
doc.add_heading("5. Fuqaro va Xodimlar Xavfsizligi", level=1)
doc.add_paragraph("Ushbu bo'lim FDP-01 hujjatidan qisqartirilgan asosiy talablarni o'z ichiga oladi.")

doc.add_heading("5.1. Fuqaro Ilovasi", level=2)
doc.add_paragraph("• Fuqaro faqat o'ziga tegishli va hamkor bank bilan qonuniy bog'langan kartalarni ko'rishi mumkin.", style='List Bullet')
doc.add_paragraph("• Karta ekranida bank nomi va oxirgi 4 raqam ko'rsatiladi; to'liq karta raqami ochilmaydi.", style='List Bullet')
doc.add_paragraph("• 'Men bu kartani tanimayman' signali avtomatik bloklamaydi, faqat tekshiruvni boshlaydi.", style='List Bullet')

doc.add_heading("5.2. Xodimlar Muhiti", level=2)
doc.add_paragraph("• Xodimlar uchun alohida kirish muhiti, kuchli autentifikatsiya va vazifaga asoslangan ruxsatlar talab etiladi.", style='List Bullet')
doc.add_paragraph("• Xodim vakolati foydalanuvchi yuborgan 'role=admin' kabi maydon bilan berilmaydi.", style='List Bullet')
doc.add_paragraph("• Har bir xodim faqat o'z vazifasi uchun zarur ma'lumotni ko'radi.", style='List Bullet')

doc.add_heading("5.3. Case Hayotiy Sikli", level=2)
doc.add_paragraph("Holatlar: Qoralama -> Yuborish kutilmoqda -> Texnik qabul tasdig'i olindi -> Bank ko'rib chiqmoqda -> Qo'shimcha ma'lumot kerak -> Bank qarori qayd etildi -> Yopildi / Texnik xato.")
doc.add_paragraph("Muhim: Texnik qabul tasdig'i bank mazmunan ma'qulladi degani emas. 'Bloklandi' holati faqat bankning tekshiriladigan aniq tasdig'i kelganida ko'rsatiladi.")

# ================= 6-QISM =================
doc.add_heading("6. Sinov Ssenariylari", level=1)
doc.add_paragraph("Sinovlar real integratsiya, server tomonidagi tekshiruv va audit yozuvlari bilan bajariladi. Ekran tasviri yoki demo natijasi o'zi yetarli dalil emas.")
tests = [
    "Fuqaro o'ziga ruxsat etilmagan kartani ko'ra olmasligi.",
    "Hamkor bo'lmagan bank kartasi bor deb taxmin qilinmasligi.",
    "Karta ekranida faqat bank nomi va oxirgi 4 raqam ko'rsatilishi.",
    "Fuqaro o'z hisobiga xodim/admin rolini tayinlay olmasligi.",
    "So'rovdagi rol maydoni server vakolatini oshirmasligi.",
    "Boshqa tashkilot xodimi vakolatsiz Case'ni ko'ra olmasligi.",
    "'Men bu kartani tanimayman' signali avtomatik bloklamasligi.",
    "Yuborilmagan xabar 'yuborildi' deb ko'rsatilmasligi.",
    "Texnik qabul tasdig'i bank qarori bilan adashtirilmasligi.",
    "Bank tasdig'isiz 'bloklandi' statusi chiqmasligi."
]
for i, t in enumerate(tests, 1):
    doc.add_paragraph(f"{i}. {t}")

doc.add_paragraph("Qabul mezoni: kritik xavfsizlik sinovi muvaffaqiyatsiz bo'lsa, tegishli funksiya pilotga chiqarilmaydi. 'O'tdi' natijasi qayta bajariladigan dalil va tasdiqlovchi shaxsga ega bo'lishi kerak.")

# ================= 7-QISM =================
doc.add_heading("7. Keyingi qadamlar va Ochiq masalalar", level=1)
doc.add_paragraph("Tasdiqlanishi kerak:")
open_q = [
    "Qaysi banklar hamkor bo'ladi va qaysi kanal ishlatiladi?",
    "Fuqaro identifikatsiyasi va kartaga bog'lash qanday tekshiriladi?",
    "Bank statuslari uchun rasmiy sxema va manba qaysi?",
    "Bank javob bermasa SLA va eskalatsiya muddati qanday?",
    "Case'ni kim ochadi, ko'radi, yopadi va qayta ochadi?",
    "Saqlash/o'chirish muddatlari va qonuniy asoslar qanday?",
    "Favqulodda kirish va o'rinbosarlikni kim tasdiqlaydi?",
    "RPO/RTO va tiklash mashqlari qanday belgilanadi?",
    "Qaysi KPI pilotni davom ettirish yoki to'xtatishni belgilaydi?"
]
for i, q in enumerate(open_q, 1):
    doc.add_paragraph(f"{i}. {q}")

doc.add_paragraph("Yakuniy qoida: ushbu Texnik Topshiriq talablar va sinov mezonlarini belgilaydi; u implementatsiya mavjudligini, bank integratsiyasi ishlashini yoki productionga tayyorlikni o'zi bilan isbotlamaydi. FINZANJIR V14 asosiy konsepsiyasi o'zgartirilmaydi.")

save_path = "/sdcard/Download/FINZANJIR_Texnik_Topshiriq.docx"
doc.save(save_path)
print("MUVAFFAQIYATLI YARATILDI: " + save_path)
