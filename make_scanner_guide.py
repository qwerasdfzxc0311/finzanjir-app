from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Sarlavha
title = doc.add_heading("FINZANJIR: APP SCANNER — FIRIBGARLIKDAN HIMOYA QILUVCHI QALQON", 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph("Versiya: 1.0 | Sana: 2026-yil")
doc.add_paragraph("Muallif: Salamat Smaylov Tangrbergen uli")
doc.add_paragraph("Til: Oddiy va tushunarli (hayotiy misollar bilan)")

doc.add_heading("1. App Scanner nima va nega kerak? (Oddiy tilda)", level=1)
doc.add_paragraph("Tasavvur qiling, sizning telefoningiz — bu sizning uyingiz. Ichida pulingiz (bank ilovasi), shaxsiy hujjatlaringiz (rasmlar, kontaktlar) va qimmatbaho narsalaringiz bor. Siz uyingizga faqat o'zingiz va ishonchli odamlarnigina kiritasiz.")
doc.add_paragraph("Ammo ba'zi 'mehmonlar' (zararli ilovalar) uyingizga kirib, kalitingizni nusxalab olishi, seyfingizni ochishi yoki sizni kuzatishi mumkin.")
doc.add_paragraph("App Scanner — bu sizning uyingiz eshigida turgan qo'riqchi. U har bir 'mehmon'ni (ilovani) tekshiradi: 'Sen kimsan? Nima uchun kirding? Nima qilmoqchisan?' Agar mehmon shubhali bo'lsa, App Scanner sizni ogohlantiradi yoki uni ichkariga kiritmaydi.")

doc.add_heading("2. Ruxsatlar nima va nega ular muhim? (Kalit misoli)", level=1)
doc.add_paragraph("Telefoningizdagi har bir ilova sizdan 'ruxsat' so'raydi. Bu xuddi shunday: mehmon sizdan 'uyingizning qaysi xonalariga kirishim mumkin?' deb so'raydi.")
doc.add_paragraph("Misol:")
doc.add_paragraph("• Fonar ilovasi 'Kamera' ruxsatini so'rasa — bu mantiqan to'g'ri, chunki fonar chiroqni yoqish uchun kamerani ishlatadi.", style='List Bullet')
doc.add_paragraph("• Fonar ilovasi 'SMS o'qish' ruxsatini so'rasa — bu juda g'alati! Nega fonar sizning SMS'laringizni o'qishi kerak?", style='List Bullet')
doc.add_paragraph("Mana shunday g'alati kombinatsiyalarni App Scanner aniqlaydi va sizni ogohlantiradi.")

doc.add_heading("3. App Scanner qanday ruxsatlarni tekshiradi? (Har biri misol bilan)", level=1)

doc.add_heading("3.1. SMS va OTP o'g'irlash (READ_SMS / RECEIVE_SMS)", level=2)
doc.add_paragraph("Bu ruxsat nima? Ilovaga sizning SMS xabarlaringizni o'qish imkonini beradi.", style='List Bullet')
doc.add_paragraph("Hayotiy misol: Tasavvur qiling, siz bankdan 'Kartangizga 100,000 so'm kirdi' degan SMS kutyapsiz. Lekin firibgarning ilovasi bu SMS'ni birinchi bo'lib o'qib, o'chirib tashlaydi. Siz pul kelganini bilmaysiz, firibgar esa buni bilib, pulni o'z hisobiga o'tkazadi.", style='List Bullet')
doc.add_paragraph("Qanday aniqlanadi: App Scanner fonar, kalkulyator yoki o'yin kabi ilovalarning SMS ruxsatini so'rayotganini ko'rsa, darhol 'Qizil bayroq' beradi. Haqiqiy bank ilovasi SMS o'qishi shart emas (chunki OTP kod faqat bank ilovasiga keladi).", style='List Bullet')

doc.add_heading("3.2. Soxta oyna (SYSTEM_ALERT_WINDOW / Overlay Attack)", level=2)
doc.add_paragraph("Bu ruxsat nima? Ilovaga boshqa ilovalar ustidan o'z oynasini chizish imkonini beradi.", style='List Bullet')
doc.add_paragraph("Hayotiy misol: Siz bank ilovasini ochdingiz. Ekranda 'Karta raqamingizni kiriting' degan oyna chiqdi. Siz ishonib, raqamni kiritdingiz. Aslida, bu bank ilovasi emas — bu firibgarning soxta oynasi! U sizning ustingizda turib, bank ilovasi kabi ko'rinadi.", style='List Bullet')
doc.add_paragraph("Qanday aniqlanadi: App Scanner telefonda 'Overlay' ruxsatini olgan ilovalarni tekshiradi. Agar bu ruxsatni fonar, o'yin yoki notanish ilova so'ragan bo'lsa, u sizni ogohlantiradi.", style='List Bullet')

doc.add_heading("3.3. Ekran va sensorlarni boshqarish (BIND_ACCESSIBILITY_SERVICE)", level=2)
doc.add_paragraph("Bu ruxsat nima? Ilovaga sizning ekrandagi harakatlaringizni (bosishlar, yozishlar) 'o'qish' va hatto sizning nomingizdan tugmalarni bosish imkonini beradi.", style='List Bullet')
doc.add_paragraph("Hayotiy misol: Firibgar sizga 'Bu ilova sizga yordam beradi' deb yuklatadi. Aslida, bu ilova bank ilovangizni ochib, 'Pul o'tkazish' tugmasini sizning nomingizdan bosadi. Siz hech narsa qilmaysiz, lekin pulingiz yo'qoladi.", style='List Bullet')
doc.add_paragraph("Qanday aniqlanadi: App Scanner 'Accessibility' ruxsatini so'ragan ilovalarni tekshiradi. Bank ilovasi bu ruxsatni hech qachon so'ramaydi. Agar notanish ilova buni so'rasa — bu juda katta xavf.", style='List Bullet')

doc.add_heading("3.4. Ekran yozib olish (MediaProjection / Screen Capture)", level=2)
doc.add_paragraph("Bu ruxsat nima? Ilovaga sizning ekraningizda nima bo'layotganini videoga yozib olish imkonini beradi.", style='List Bullet')
doc.add_paragraph("Hayotiy misol: Siz Telegram orqali 'Mijozlarga xizmat' degan odam bilan gaplashyapsiz. U 'Ekraningizni ko'rsating, yordam beraman' deydi. Siz rozi bo'lasiz. Aslida, u sizning ekraningizni yozib olib, bank parolingizni va OTP kodlaringizni o'g'irlaydi.", style='List Bullet')
doc.add_paragraph("Qanday aniqlanadi: App Scanner ekran yozib olish xizmati faol bo'lsa, sizni ogohlantiradi: 'Hozir ekran yozib olinmoqda. Bu xavfli bo'lishi mumkin.'", style='List Bullet')

doc.add_heading("3.5. Qurilmaning 'buzilganligi' (Root / Jailbreak)", level=2)
doc.add_paragraph("Bu nima? 'Root' — bu Android telefonning xavfsizlik tizimini buzib, unga to'liq kirish huquqini olish. 'Jailbreak' — iPhone'da xuddi shunday.", style='List Bullet')
doc.add_paragraph("Hayotiy misol: Uyingizning asosiy eshigini ochib, hech qanday qulf qoldirmaslik. Kim xohlasa kiradi, kim xohlasa chiqadi. Root qilingan telefonda bank ilovasi ham himoyasiz qoladi.", style='List Bullet')
doc.add_paragraph("Qanday aniqlanadi: App Scanner telefonning 'SU' (SuperUser) faylini tekshiradi. Agar topilsa, sizga aytadi: 'Telefoningiz xavfsiz emas. Iltimos, bank ilovasini ishlatmang.'", style='List Bullet')

doc.add_heading("3.6. Noma'lum manbalardan o'rnatish (REQUEST_INSTALL_PACKAGES)", level=2)
doc.add_paragraph("Bu ruxsat nima? Ilovaga Play Store'dan tashqari boshqa joylardan ilova o'rnatish imkonini beradi.", style='List Bullet')
doc.add_paragraph("Hayotiy misol: Sizga Telegram orqali 'Yangi bank ilovasi chiqdi, yangilang' degan havola keladi. Siz yuklab olasiz. Aslida, bu soxta ilova. U sizning barcha ma'lumotlaringizni firibgarga yuboradi.", style='List Bullet')
doc.add_paragraph("Qanday aniqlanadi: App Scanner 'Noma'lum manba' ruxsatini so'ragan ilovalarni tekshiradi. Agar bank nomidan kelgan ilova bu ruxsatni so'rasa — bu soxta.", style='List Bullet')

doc.add_heading("4. App Scanner yana qanday firibgarliklarni aniqlay oladi?", level=1)

doc.add_heading("4.1. SIM-Swap (Telefon raqamini o'g'irlash)", level=2)
doc.add_paragraph("Hayotiy misol: Firibgar sizning ismingizdan operatorga borib, 'Telefonimni yo'qotdim, yangi SIM bering' deydi. Operator yangi SIM beradi. Endi barcha SMS'lar (jumladan bank OTP kodlari) firibgarga keladi.", style='List Bullet')
doc.add_paragraph("App Scanner: SIM-karta o'zgarganini aniqlaydi va bankka signal yuboradi: 'Bu telefon raqami yaqinda o'zgargan, ehtiyot bo'ling.'", style='List Bullet')

doc.add_heading("4.2. Fishing (Aldov havolalari)", level=2)
doc.add_paragraph("Hayotiy misol: Sizga 'Sovg'a yutdingiz! Shu havolani bosing' degan SMS keladi. Havolani bossangiz, soxta bank sahifasi ochiladi. Siz parolni kiritasiz — firibgar uni o'g'irlaydi.", style='List Bullet')
doc.add_paragraph("App Scanner: Havolani tekshiradi va 'Bu havola xavfli, bu bankning rasmiy sayti emas' deb ogohlantiradi.", style='List Bullet')

doc.add_heading("4.3. Qo'ng'iroq orqali aldash (Vishing)", level=2)
doc.add_paragraph("Hayotiy misol: Sizga qo'ng'iroq qilib, 'Men bankdanman, kartangizda shubhali operatsiya bor. Tasdiqlash uchun SMS kodni ayting' deyishadi. Siz kodni aytasiz — pul o'g'irlanadi.", style='List Bullet')
doc.add_paragraph("App Scanner: Qo'ng'iroq paytida sizga ogohlantirish chiqaradi: 'Bank xodimi hech qachon SMS kod so'ramaydi. Hech kimga bermang.'", style='List Bullet')

doc.add_heading("4.4. Zararli Wi-Fi (Public Wi-Fi Attack)", level=2)
doc.add_paragraph("Hayotiy misol: Siz kafeda bepul Wi-Fi'ga ulanasiz. Aslida, bu firibgarning Wi-Fi'si. U sizning barcha ma'lumotlaringizni (parollar, karta raqamlari) ko'rib turadi.", style='List Bullet')
doc.add_paragraph("App Scanner: Wi-Fi tarmog'ining xavfsizligini tekshiradi va 'Bu tarmoq shifrlanmagan, bank ilovasini ishlatmang' deb ogohlantiradi.", style='List Bullet')

doc.add_heading("4.5. Skrinshot orqali ma'lumot o'g'irlash", level=2)
doc.add_paragraph("Hayotiy misol: Siz karta raqamingizni skrinshot qilib, saqlab qo'yasiz. Keyin telefonni boshqa ilovaga ruxsat berasiz. U ilova skrinshotlaringizni o'qib, karta raqamingizni o'g'irlaydi.", style='List Bullet')
doc.add_paragraph("App Scanner: Galereya ruxsatini so'ragan ilovalarni tekshiradi va 'Bu ilova rasmlaringizni o'qishi mumkin. Ishonchingiz komilmi?' deb so'raydi.", style='List Bullet')

doc.add_heading("5. App Scanner qanday ruxsatlarni o'zi so'raydi? (Va nega?)", level=1)
doc.add_paragraph("App Scanner o'zi ham ba'zi ruxsatlarni so'raydi, lekin ular faqat xavfsizlikni tekshirish uchun kerak:")
table = doc.add_table(rows=1, cols=2)
table.style = "Table Grid"
hdr = table.rows[0].cells
hdr[0].text = "Ruxsat"
hdr[1].text = "Nega kerak? (Oddiy tilda)"

data = [
    ("QUERY_ALL_PACKAGES", "Telefonda qanday ilovalar o'rnatilganini ko'rish uchun. Bu — qo'riqchining 'mehmonlar ro'yxati'ni tekshirishi."),
    ("HIDE_OVERLAY_WINDOWS", "Bank ilovasi ustidan soxta oyna ochilishining oldini olish uchun. Bu — qo'riqchining 'derazalarni qulflash' harakati."),
    ("READ_PHONE_STATE", "Telefonning asosiy holatini (qo'ng'iroq, SIM) bilish uchun. Bu — qo'riqchining 'eshikni kim taqillatayotganini eshitishi'."),
    ("RECORD_AUDIO (ixtiyoriy)", "Mikrofon boshqa ilova tomonidan tinglanayotganini aniqlash uchun. Faqat siz ruxsat bersangiz ishlaydi."),
    ("READ_SMS (ixtiyoriy)", "SMS orqali kelgan shubhali havolalarni aniqlash uchun. Faqat siz ruxsat bersangiz ishlaydi."),
]
for r in data:
    row = table.add_row().cells
    for i, item in enumerate(r):
        row[i].text = item

doc.add_paragraph("Muhim: App Scanner hech qachon sizning SMS'laringizni firibgarga yubormaydi. U faqat 'Bu SMS xavfli yoki yo'q' deb aytadi.")

doc.add_heading("6. Xulosa: App Scanner — sizning shaxsiy qo'riqchingiz", level=1)
doc.add_paragraph("Tasavvur qiling, sizda bankda 50 million so'm bor. Har kuni sizga 10-20 ta notanish odam qo'ng'iroq qiladi, SMS yuboradi, ilova yuklatishni so'raydi. Kimga ishonasiz?")
doc.add_paragraph("App Scanner — bu sizning ishonchli qo'riqchingiz. U:")
doc.add_paragraph("• Har bir ilovani tekshiradi: 'Sen kimsan, nima uchun bu ruxsatlarni so'rayapsan?'", style='List Bullet')
doc.add_paragraph("• Har bir havolani tekshiradi: 'Bu bankning rasmiy saytimi yoki soxtami?'", style='List Bullet')
doc.add_paragraph("• Telefoningiz xavfsizligini tekshiradi: 'Root qilinganmi? Ekran yozib olinyaptimi?'", style='List Bullet')
doc.add_paragraph("• Sizni ogohlantiradi: 'Bu xavfli, ehtiyot bo'ling!'", style='List Bullet')
doc.add_paragraph("Asosiy qoida: Bank xodimi hech qachon SMS kod, parol yoki karta raqamini so'ramaydi. Agar so'rasa — bu 100% firibgar.")

doc.add_heading("7. Keyingi qadam (FINZANJIR uchun)", level=1)
doc.add_paragraph("Ushbu App Scanner talablari FINZANJIR 2.0 versiyasida joriy etiladi. Hozirgi prototipda u oddiy ruxsatlar ro'yxatini ko'rsatadi, xolos. To'liq ishlashi uchun:")
doc.add_paragraph("1. Banklar bilan huquqiy kelishuv (foydalanuvchi ruxsatlari uchun).", style='List Bullet')
doc.add_paragraph("2. Real qurilmalarda sinov (Root, Overlay, Accessibility aniqlash).", style='List Bullet')
doc.add_paragraph("3. Foydalanuvchilar uchun tushunarli ogohlantirish matnlari.", style='List Bullet')

doc.add_paragraph("Yakuniy fikr: Firibgarlar har kuni yangi usul o'ylab topadi, lekin App Scanner — sizning eng kuchli himoyangiz. Ular qanchalik aqlli bo'lishmasin, qo'riqchi doim hushyor!")

save_path = "/sdcard/Download/FINZANJIR_App_Scanner_Qollanma.docx"
doc.save(save_path)
print("MUVAFFAQIYATLI YARATILDI: " + save_path)
