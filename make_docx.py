from docx import Document
from docx.shared import Pt

doc = Document()

doc.add_heading("FINZANJIR: SIGNAL REYESTRI VA ANIQLASH QOIDALARI (v1.0)", 0)
doc.add_paragraph("Muallif: Salamat Smaylov Tangrbergen uli")
doc.add_paragraph("Sana: 2026-yil")

doc.add_heading("1. Hujjatning maqsadi", level=1)
doc.add_paragraph("Ushbu reyestr FINZANJIR platformasining Risk Engine qismida ishlatiladigan dastlabki signallarni, ularning matematik mantiqini va qaysi firibgarlik ssenariysiga tegishli ekanligini tizimlashtirish uchun yaratildi.")

doc.add_heading("2.1. 1-Jadval: Tranzaksiya va Pul Harakati Signallari", level=2)
table1 = doc.add_table(rows=1, cols=6)
table1.style = "Table Grid"
hdr = table1.rows[0].cells
hdr[0].text = "Signal ID"
hdr[1].text = "Signal Nomi"
hdr[2].text = "Mantiq"
hdr[3].text = "Kerakli Malumot"
hdr[4].text = "Manba Darajasi"
hdr[5].text = "Ssenariy"
data1 = [
    ("SIG-001", "Noodatiy summa", "Ortachadan 5-10 baravar katta", "Summa, Tarix", "Tier 1", "ATO"),
    ("SIG-002", "Yuqori tezlik", "1 daqiqada 3+ tranzaksiya", "Vaqt, Karta ID", "Tier 1", "Karta firibgarligi"),
    ("SIG-003", "Pul otishi", "Pul tushib, 1-2 daqiqada chiqishi", "Vaqt, Qoldiq", "Tier 1", "Money Mule"),
    ("SIG-004", "Yangi qabul qiluvchi", "Ilgari ishlatilmagan hisob", "Qabul qiluvchi ID", "Tier 1/2", "ATO, Aldov"),
    ("SIG-005", "Limitdan qochish", "Bolib bolib otkazish", "Summa, Limit", "Tier 1", "Pul yuvish"),
]
for r in data1:
    row = table1.add_row().cells
    for i, item in enumerate(r):
        row[i].text = item

doc.add_heading("2.2. 2-Jadval: Qurilma va Tarmoq Signallari", level=2)
table2 = doc.add_table(rows=1, cols=6)
table2.style = "Table Grid"
hdr2 = table2.rows[0].cells
hdr2[0].text = "Signal ID"
hdr2[1].text = "Signal Nomi"
hdr2[2].text = "Mantiq"
hdr2[3].text = "Kerakli Malumot"
hdr2[4].text = "Manba Darajasi"
hdr2[5].text = "Ssenariy"
data2 = [
    ("SIG-006", "Yangi qurilma", "Noodatiy telefon/kompyuter", "Device ID, Sessiya", "Tier 2", "ATO"),
    ("SIG-007", "Geo-anomaliya", "Impossible Travel", "IP, Geo, Vaqt", "Tier 2", "Karta firibgarligi"),
    ("SIG-008", "Bir qurilmada kop kartalar", "1 ta telefondan 3+ karta", "Device ID, Karta ID", "Tier 2", "Pul yuvish"),
    ("SIG-009", "VPN/Proxy/Tor", "Anonim tarmoq", "IP, Reputatsiya", "Tier 2/3", "Karta firibgarligi"),
]
for r in data2:
    row = table2.add_row().cells
    for i, item in enumerate(r):
        row[i].text = item

doc.add_heading("2.3. 3-Jadval: Xulq-atvor va Sessiya Signallari", level=2)
table3 = doc.add_table(rows=1, cols=6)
table3.style = "Table Grid"
hdr3 = table3.rows[0].cells
hdr3[0].text = "Signal ID"
hdr3[1].text = "Signal Nomi"
hdr3[2].text = "Mantiq"
hdr3[3].text = "Kerakli Malumot"
hdr3[4].text = "Manba Darajasi"
hdr3[5].text = "Ssenariy"
data3 = [
    ("SIG-010", "Noodatiy vaqt", "Tungi soat 03:00", "Vaqt, Tarix", "Tier 1", "ATO"),
    ("SIG-011", "Shoshilinch sessiya", "10-15 soniyada pul otkazish", "Sessiya vaqti", "Tier 2", "Ijtimoiy injiniring"),
    ("SIG-012", "Parol tiklash + Pul", "Parol tiklab, darhol pul otkazish", "Auth loglari", "Tier 2", "ATO"),
]
for r in data3:
    row = table3.add_row().cells
    for i, item in enumerate(r):
        row[i].text = item

doc.add_heading("2.4. 4-Jadval: Tarmoq va Graf Signallari", level=2)
table4 = doc.add_table(rows=1, cols=6)
table4.style = "Table Grid"
hdr4 = table4.rows[0].cells
hdr4[0].text = "Signal ID"
hdr4[1].text = "Signal Nomi"
hdr4[2].text = "Mantiq"
hdr4[3].text = "Kerakli Malumot"
hdr4[4].text = "Manba Darajasi"
hdr4[5].text = "Ssenariy"
data4 = [
    ("SIG-013", "Shubhali qabul qiluvchi", "Qora royxatdagi hisob", "Receiver ID, Baza", "Tier 3", "Aldov, Pul yuvish"),
    ("SIG-014", "Umumiy atributlar", "Bir xil telefon/qurilma", "Tel, Device ID", "Tier 2/3", "Firibgarlar tarmogi"),
    ("SIG-015", "Halqa (Circular)", "A->B->C->A pul aylanishi", "Graph zanjiri", "Tier 3", "Pul yuvish"),
]
for r in data4:
    row = table4.add_row().cells
    for i, item in enumerate(r):
        row[i].text = item

doc.add_heading("3. Risk Engine Qoidalari (Rules)", level=1)
doc.add_paragraph("Tizim bitta signalga emas, balki ularning kombinatsiyasiga qarab qaror qabul qiladi.")
doc.add_paragraph("Qoida 1 (Kritik xavf): Agar SIG-006 + SIG-001 + SIG-004 bir vaqtda kelsa -> Risk Score = 85 (HIGH). Tizim avtomatik Case ochadi va Human Reviewga yuboradi.", style="List Bullet")
doc.add_paragraph("Qoida 2 (Past xavf): Agar faqat SIG-002 kelsa -> Risk Score = 30 (LOW). Faqat kuzatiladi (Shadow mode).", style="List Bullet")
doc.add_paragraph("Qoida 3 (Pul yuvish): Agar SIG-003 + SIG-008 kelsa -> Risk Score = 90 (CRITICAL). Darhol tekshiruvga yuboriladi.", style="List Bullet")

doc.add_heading("4. Keyingi qadamlar", level=1)
doc.add_paragraph("1. Banklar bilan aniqlashtirish: Qaysi signallarni API orqali bera olishini aniqlash.")
doc.add_paragraph("2. Risk Engine formulasi: Har bir signalning vaznini mutaxassislar bilan kelishish.")
doc.add_paragraph("3. Test Ssenariylari: Har bir qoida uchun sintetik malumotlar yaratib, tizimni sinovdan otkazish.")

save_path = "/sdcard/Download/FINZANJIR_Signal_Reyestri.docx"
doc.save(save_path)
print(f"MUVAFFAQIYATLI YARATILDI: {save_path}")
