from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Sarlavha
title = doc.add_heading("FINZANJIR — Fuqaro va xodimlar xavfsizligi: bank vakolatlari, karta holatlari, murojaatlar va kirish nazoratining amaliy FDP hujjati", 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph("Versiya: FDP-01 | Sana: 2026-10-22")
doc.add_paragraph("Holat: Amaliy talablar hujjati; implementatsiya dalili o'rnini bosmaydi.")
doc.add_paragraph("Muhim: FINZANJIR bank o'rniga qaror chiqarmaydi va kartani o'zi bloklamaydi. 'Bloklandi' holati faqat tekshirilgan bank tasdig'i bilan ko'rsatiladi. Asosiy konsepsiya o'zgartirilmaydi.")

doc.add_heading("1. Maqsad va qo'llanish doirasi", level=1)
doc.add_paragraph("Ushbu FDP asosiy FINZANJIR konsepsiyasini qayta yozmaydi va uning o'rnini bosmaydi. U fuqaro ilovasi, hamkor-bank kartalari, shubhali holat haqida signal berish, Case yuritish, bank bilan vakolatli aloqa, xodimlar muhiti, kirish nazorati, audit va sinovlar uchun amaliy talablarni jamlaydi.")
doc.add_paragraph("Vakolat chegarasi: FINZANJIR bank o'rniga qaror chiqarmaydi, kartani o'zi bloklamaydi va bank qarorini almashtirmaydi. U xavfsiz aloqa, murojaatni kuzatish, dalil kelib chiqishini saqlash va vakolatli tekshiruvni qo'llab-quvvatlash uchun mo'ljallanadi.")

doc.add_paragraph("Asosiy tamoyillar:", style='List Bullet')
principles = [
    "Signal ≠ firibqarlik isboti.",
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

doc.add_heading("2. Holat belgilari va dalil intizomi", level=1)
doc.add_paragraph("• Mavjudligi tasdiqlangan: ishlayotgan kod, sinov natijasi yoki tekshiriladigan dalil bilan tasdiqlangan.")
doc.add_paragraph("• Hujjatda ko'rsatilgan: talab hujjatda yozilgan, ammo ishlashi alohida tasdiqlanmagan.")
doc.add_paragraph("• Mavjud emas: tekshiruvda yo'qligi aniqlangan.")
doc.add_paragraph("• Taklif: ko'rib chiqish va tasdiqlash uchun taklif etilgan.")
doc.add_paragraph("• Kelajakdagi imkoniyat: keyingi bosqichga mo'ljallangan.")
doc.add_paragraph("• Gipoteza: sinov va dalil talab qiladigan taxmin.")
doc.add_paragraph("• Pilot: cheklangan muhitda sinovdan o'tayotgan.")
doc.add_paragraph("• Production: haqiqiy operatsion muhitga vakolatli ruxsat bilan joriy qilingan.")
doc.add_paragraph("Talab hujjatda yozilgani uning dasturda amalga oshirilganini anglatmaydi. Har bir muhim talab uchun dalil turi, tekshiruv usuli, mas'ul va natija qayd etilishi kerak. Qarama-qarshi manbalar topilsa, farq yashirincha birlashtirilmaydi; mas'ul ekspert ko'rib chiqishi uchun qayd etiladi.")

doc.add_heading("3. Asosiy konsepsiya va qo'shimcha FDP munosabati", level=1)
doc.add_paragraph("FINZANJIR V14 asosiy konsepsiyasi alohida hujjat bo'lib qoladi. Ushbu FDP undagi boblarni takrorlamasdan, fuqarolar va xodimlar xavfsizligi bilan bog'liq amaliy jarayonlar, qabul mezonlari va sinov ssenariylarini aniqlashtiradi.")
doc.add_paragraph("FDP manba hujjatlarda ko'rsatilgan talablarni amaliy tekshiruvga aylantiradi; hujjatda ko'rsatilmagan funksiyalarni mavjud deb e'lon qilmaydi. Prototipdagi ayrim ekranlar namoyish yoki simulyatsiya bo'lishi mumkin. Masalan, tugma bosilgandan keyin 'bloklandi' yoki 'himoyalandi' yozuvi paydo bo'lishi bank bilan haqiqiy integratsiya yoki real bloklash dalili emas.")

doc.add_heading("4. Fuqaro ilovasi va hamkor-bank kartalari", level=1)
doc.add_paragraph("Fuqaro ilovasi foydalanuvchining shaxsiy muhitidir. Fuqaro xodim rolini o'zi tanlab yoki oddiy so'rov yuborib faollashtira olmasligi kerak.")
doc.add_paragraph("Karta ma'lumotlari faqat FINZANJIR bilan hamkorlik qiladigan, tegishli kelishuvi va vakolatli ma'lumot almashish kanali mavjud banklardan olinishi mumkin. FINZANJIR barcha banklar yoki barcha kartalarni ko'ra oladi, deb aytilmaydi.")
doc.add_paragraph("Fuqaro ekranida minimal karta identifikatsiyasi ko'rsatiladi:")
doc.add_paragraph("• bank nomi;", style='List Bullet')
doc.add_paragraph("• karta raqamining faqat oxirgi 4 raqami;", style='List Bullet')
doc.add_paragraph("• zarur bo'lsa ma'lumot manbasi va oxirgi yangilanish vaqti;", style='List Bullet')
doc.add_paragraph("• ma'lumot eskirgan yoki sinxronlashda xato bo'lsa ogohlantirish.", style='List Bullet')
doc.add_paragraph("Karta ro'yxatda yo'qligi uning albatta boshqa bankka tegishli ekanini isbotlamaydi. Sabab hamkorlik doirasidan tashqarida qolish, ruxsat, identifikatsiya, sinxronlash yoki texnik uzilish bo'lishi mumkin. Taxmin fakt sifatida ko'rsatilmaydi.")

doc.add_heading("5. 'Men bu kartani tanimagman' signali", level=1)
doc.add_paragraph("Bu amal fuqaroning karta bilan tanish emasligi yoki shubhasini bildiradi. U firibgarlik aniqlanganini anglatmaydi va kartani avtomatik bloklamaydi.")
doc.add_paragraph("Tavsiya etiladigan oqim:")
doc.add_paragraph("1. Fuqaro o'ziga ko'rsatilgan karta yozuvini tanlaydi.")
doc.add_paragraph("2. Ilova bank nomi va oxirgi 4 raqamni qayta ko'rsatib, tasdiqlashni so'raydi.")
doc.add_paragraph("3. Fuqaro sababni ixtiyoriy tanlaydi yoki qisqa izoh beradi; ortiqcha shaxsiy ma'lumot talab qilinmaydi.")
doc.add_paragraph("4. Tizim murojaat identifikatorini yaratadi yoki dublikatni aniqlaydi.")
doc.add_paragraph("5. Murojaat faqat tegishli bank bilan kelishilgan vakolatli kanal mavjud bo'lsa yuboriladi.")
doc.add_paragraph("6. Fuqaroga yuborish holati va keyingi qadam tushuntiriladi.")
doc.add_paragraph("7. Bank qarori tekshirilgan manbadan kelgandagina ko'rsatiladi.")
doc.add_paragraph("Agar xabar yuborilmasa, ilova uni muvaffaqiyatli yuborilgan deb ko'rsatmaydi. Signalni yuborishning o'zi aybdorlik yoki firibgarlik isboti emas.")

doc.add_heading("6. Murojaat va Case hayotiy sikli", level=1)
doc.add_paragraph("Signal – boshlang'ich xabar. Case – vakolatli jarayonda kuzatiladigan ish yozuvi. Har bir signal alohida Case bo'lishi shart emas; dublikatlar bog'lanishi mumkin, ammo dastlabki yozuvlar va kelib chiqish izi saqlanadi.")
doc.add_paragraph("Tavsiya etiladigan holatlar:")
statuses = [
    "Qoralama – foydalanuvchi hali yubormagan.",
    "Yuborish kutilmoqda – ilova yuborishga urinmoqda.",
    "Texnik qabul tasdig'i olindi – kanal xabarni texnik jihatdan qabul qilgan.",
    "Bank ko'rib chiqmoqda – bankning tasdiqlangan holat ma'lumoti mavjud.",
    "Qo'shimcha ma'lumot kerak – vakolatli tomon ma'lumot so'ragan.",
    "Bank qarori qayd etildi – qaror manbasi va vaqti qayd etilgan.",
    "Yopildi – belgilangan tartibda yopilgan va sabab qayd etilgan.",
    "Texnik xato / javob kutilmoqda – aloqa yoki sinxronlash muammosi bor."
]
for s in statuses:
    doc.add_paragraph(s, style='List Bullet')
doc.add_paragraph("Texnik qabul tasdig'i bank mazmunan ma'qulladi degani emas. Bank qarori qayd etilgani ham 'karta bloklandi' degani emas. 'Bloklandi' holati faqat bankning tekshiriladigan aniq tasdig'i kelganida ko'rsatiladi.")
doc.add_paragraph("Har bir o'zgarish uchun oldingi holat, yangi holat, vaqt, manba, bajaruvchi yoki integratsiya identifikatori, sabab va dalil havolasi qayd etiladi. Kechikkan yoki ziddiyatli javoblar yashirilmaydi.")

doc.add_heading("7. FINZANJIR AI va bilim tizimi chegaralari", level=1)
doc.add_paragraph("Hozirgi FINZANJIR AI — rivojlantirilayotgan mahalliy bilim va mantiq asosining dastlabki bosqichi; uni tayyor yoki mukammal tizim sifatida taqdim etmaslik kerak. Hozirgi yo'nalishda APK ichiga Qwen yoki boshqa tashqi/mahalliy umumiy AI modelini qo'shish rejalashtirilmagan; bu masala keyinchalik dalil va ekspert bahosi asosida qayta ko'rib chiqilishi mumkin.")
doc.add_paragraph("AI tasdiqlangan ma'lumot bo'lsa, jarayonni tushuntirishi, Case holatini izohlashi, yetishmayotgan ma'lumotni ko'rsatishi va keyingi rasmiy qadamni tushuntirishi mumkin.")
doc.add_paragraph("AI:")
doc.add_paragraph("• bank javobini uydirmaydi;", style='List Bullet')
doc.add_paragraph("• bank tasdig'isiz kartani bloklangan demaydi;", style='List Bullet')
doc.add_paragraph("• Case holatini dalilsiz o'zgartirmaydi;", style='List Bullet')
doc.add_paragraph("• signalni firibgarlikning yakuniy isboti yoki aybdorlik deb ko'rsatmaydi;", style='List Bullet')
doc.add_paragraph("• bank yoki vakolatli xodim o'rniga yakuniy qaror chiqarmaydi;", style='List Bullet')
doc.add_paragraph("• tasdiqlanmagan bilimni AUTHORITATIVE bilim bazasiga avtomatik qo'shmaydi.", style='List Bullet')
doc.add_paragraph("Ma'lumot yetarli bo'lmasa, 'Ma'lumot yetarli emas' yoki 'Buni tasdiqlay olmayman' deyishi kerak. Authoritative bilim, tekshiruvga nomzod bilim, suhbat/shaxsiy kontekst va tarixiy ma'lumotlar ajratiladi. Offline-first tamoyili saqlanadi; tashqi provider faqat aniq sozlangan bo'lsa ishlatiladi. API kalitlari ilova ichiga joylashtirilmaydi.")

doc.add_heading("8. Xodimlar muhiti, identifikatsiya va rollar", level=1)
doc.add_paragraph("Xodimlar muhiti fuqaro ilovasidan alohida xavfsizlik chegarasiga ega bo'lishi kerak. Xodim vakolati foydalanuvchi yuborgan role=admin kabi maydon, oddiy sozlama yoki o'zini xodim deb e'lon qilish bilan berilmaydi.")
doc.add_paragraph("Minimal talablar:")
doc.add_paragraph("• noyob xodim identifikatsiyasi va tashkilot tasdiqlagan hisob;", style='List Bullet')
doc.add_paragraph("• kuchli autentifikatsiya, zarur bo'lsa ko'p omilli tasdiqlash;", style='List Bullet')
doc.add_paragraph("• vazifaga mos eng kam vakolat (least privilege);", style='List Bullet')
doc.add_paragraph("• banklar va tashkilotlar o'rtasida ma'lumotlarni ajratish;", style='List Bullet')
doc.add_paragraph("• Case'ga faqat xizmat vazifasi doirasida kirish;", style='List Bullet')
doc.add_paragraph("• vakolat berish, o'zgartirish va bekor qilishni qayd etish;", style='List Bullet')
doc.add_paragraph("• xodim ishdan ketganda yoki roli o'zgarganda kirishni bekor qilish;", style='List Bullet')
doc.add_paragraph("• xodim rolini fuqaro hisobidan mustaqil va tekshiriladigan jarayon orqali berish.", style='List Bullet')
doc.add_paragraph("Aniq rollar va ruxsatlar tashkilotlar bilan kelishilgan matritsada tasdiqlanadi. Hujjatda rol matritsasi bo'lishi uning amalda ishlayotganini isbotlamaydi; server tomonidagi ruxsat tekshiruvlari sinovdan o'tishi shart.")

doc.add_heading("9. Sessiya, o'rinbosarlik va favqulodda kirish", level=1)
doc.add_paragraph("Xodim sessiyasida ekran qulfi, harakatsizlikdan so'ng qayta autentifikatsiya, xavfsiz chiqish va hisob buzilishi holatida sessiyani bekor qilish mexanizmlari ko'zda tutiladi.")
doc.add_paragraph("O'rinbosarlik faqat vakolatli jarayon bilan, aniq vazifa va amal qilish muddati ko'rsatilgan holda beriladi. Muddati tugaganda avtomatik bekor qilinadi; asosiy xodimning barcha huquqlari avtomatik ko'chirilmaydi. Berish, foydalanish va tugash hodisalari auditga yoziladi.")
doc.add_paragraph("Favqulodda kirish faqat belgilangan zaruratlarda, sabab va ish raqami bilan, minimal muddat va vakolat doirasida ishlatiladi. Imkon qadar mustaqil nazorat yoki keyingi majburiy tekshiruv bo'lishi kerak. Favqulodda yo'l doimiy nazoratni chetlab o'tish vositasiga aylanmasligi lozim.")

doc.add_heading("10. Case boshqaruvi va eskalatsiya", level=1)
doc.add_paragraph("Har bir Case uchun egasi, mas'ul tashkilot, navbatdagi harakat va ko'rib chiqish muddati aniq bo'lishi kerak. Bir tashkilot xodimi boshqa bankning ichki qarorini o'zgartira olmaydi.")
doc.add_paragraph("Eskalatsiya qoidalari quyidagilarni belgilaydi:")
esc = [
    "qaysi holatda bankka yuborish;",
    "javob kechiksa kimga va qachon eslatish;",
    "kanal ishlamasa muqobil rasmiy aloqa yo'li;",
    "qo'shimcha ma'lumotni kim so'rashi mumkin;",
    "Case'ni kim yopishi va yopish sabablari;",
    "noto'g'ri tasniflangan Case'ni tuzatish tartibi;",
    "fuqaro shikoyati va qayta ko'rib chiqish yo'li."
]
for e in esc:
    doc.add_paragraph(e, style='List Bullet')
doc.add_paragraph("Risk darajasi avtomatik ayblov, jazolash yoki bank qarorini o'zgartirish uchun yakka asos bo'la olmaydi.")

doc.add_heading("11. Audit, maxfiylik va ichki tahdid", level=1)
doc.add_paragraph("Audit yozuvlari kim, qachon, qaysi ma'lumotni ko'rgan yoki o'zgartirganini, nima sababdan va qaysi vakolat bilan bajarganini tiklashga yetarli bo'lishi kerak. Audit jurnali oddiy foydalanuvchi yoki amalni bajargan xodim tomonidan yashirincha o'zgartirilishidan himoyalanadi.")
doc.add_paragraph("Ma'lumotlarni minimallashtirish:")
doc.add_paragraph("• vazifa uchun zarur bo'lmagan ma'lumotni yig'maslik;", style='List Bullet')
doc.add_paragraph("• karta to'liq raqami va maxfiy autentifikatsiya ma'lumotlarini odatiy ekranda ko'rsatmaslik;", style='List Bullet')
doc.add_paragraph("• saqlash muddati va o'chirish tartibini belgilash;", style='List Bullet')
doc.add_paragraph("• testda haqiqiy bank/shaxsiy ma'lumotlardan foydalanmaslik yoki ularni tasdiqlangan tarzda himoyalash;", style='List Bullet')
doc.add_paragraph("• eksport va ommaviy qidiruv huquqlarini cheklash;", style='List Bullet')
doc.add_paragraph("• ma'lumot buzilishi yoki ruxsatsiz kirishda javob berish jarayonini belgilash.", style='List Bullet')
doc.add_paragraph("Ichki tahdidga qarshi nazoratlar: vazifalar ajratilishi, noodatiy kirish monitoringi, davriy ruxsat auditi, ommaviy ko'rish/eksport ogohlantirishlari va hodisani mustaqil tekshirish. Saqlash muddatlari va qonuniy asoslar mutaxassislar tomonidan tasdiqlanadi.")

doc.add_heading("12. Monitoring, xatolar va uzluksizlik", level=1)
doc.add_paragraph("Monitoring quyidagilarni kuzatishi kerak: bank kanali mavjudligi va javob vaqti; yuborish xatolari va takroriy yuborishlar; eski holatlar; sinxronlash nomuvofiqliklari; ruxsatsiz kirish urinishlari; Case navbati; zaxira nusxa va tiklash sinovlari; AI javoblaridagi manba yo'qligi va noto'g'ri statuslar.")
doc.add_paragraph("Zaxira nusxa, falokatdan tiklash (DR) va biznes uzluksizligi (BCP) uchun RPO/RTO maqsadlari, javobgarlar, zaxira joyi, tiklash ketma-ketligi va davriy mashqlar belgilanadi. Aniq vaqt maqsadlari arxitektura, risk va xizmat kelishuvlari asosida tasdiqlanadi; tekshirilmagan raqamlar fakt sifatida kiritilmaydi.")
doc.add_paragraph("Aloqa uzilganda tizim xabarni yuborilgan deb ko'rsatmaydi. Qayta urinishlar dublikat yaratmasligi uchun idempotent identifikatorlar va kuzatuv ishlatiladi. Xizmat tiklangach, navbatdagi xabarlar va holatlar muvofiqlashtiriladi.")

doc.add_heading("13. Sinov ssenariylari va qabul mezonlari", level=1)
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
    "Bank tasdig'isiz 'bloklandi' statusi chiqmasligi.",
    "Bank rad javobi kelganda keyingi qadam tushuntirilishi.",
    "Javob kelmaganda 'javob kutilmoqda' va eskalatsiya yo'li ishlashi.",
    "Takroriy bosishlar nazoratsiz dublikat Case yaratmasligi.",
    "Kechikkan yoki ziddiyatli javoblar auditda saqlanishi.",
    "Case statusini kim o'zgartirgani qayd etilishi.",
    "Vakolat bekor qilingach eski sessiya orqali ma'lumot ochilmasligi.",
    "Vaqtinchalik o'rinbosarlik muddati tugagach avtomatik to'xtashi.",
    "Favqulodda kirish sababi va alohida audit iziga ega bo'lishi.",
    "Xodim audit yozuvini yashirincha o'chira olmasligi.",
    "Eksport alohida ruxsat va auditga ega bo'lishi.",
    "Tarmoq uzilganda noto'g'ri muvaffaqiyat xabari chiqmasligi.",
    "Qayta yuborish dublikat yoki status buzilishiga olib kelmasligi.",
    "Eskirgan ma'lumot foydalanuvchiga ko'rsatilishi yoki ogohlantirilishi.",
    "Zaxira nusxadan tiklash amaliy sinovdan o'tishi.",
    "AI mavjud bo'lmagan bank qarorini uydirmasligi.",
    "AI yetarli dalil bo'lmaganda noaniqlikni ochiq aytishi.",
    "AI signalni firibgarlik isboti yoki aybdorlik deb atamasligi.",
    "AI authoritative bilim bazasini tasdiqsiz o'zgartira olmasligi.",
    "O'zbek, qoraqalpoq, qozoq, rus va ingliz tilidagi muhim xabarlar tekshirilishi.",
    "Accessibility: matn, xato xabari va yordam yo'li tushunarli bo'lishi.",
    "False positive va false negative alohida o'lchanishi.",
    "Retrieval sifati Recall@10 va boshqa ko'rsatkichlar bilan belgilangan test to'plamida hisoblanishi.",
    "Har bir test uchun kutilgan/haqiqiy natija, dalil, versiya, bajaruvchi va sana saqlanishi."
]

for i, t in enumerate(tests, 1):
    doc.add_paragraph(f"{i}. {t}")

doc.add_paragraph("Qabul mezoni: kritik xavfsizlik sinovi muvaffaqiyatsiz bo'lsa, tegishli funksiya pilotga chiqarilmaydi. 'O'tdi' natijasi qayta bajariladigan dalil va tasdiqlovchi shaxsga ega bo'lishi kerak.")

doc.add_heading("14. Pilotga tayyorgarlik va ekspert tasdiqlari", level=1)
doc.add_paragraph("Pilotdan oldin quyidagilar tasdiqlanishi kerak:")
pilot = [
    "pilot banklari, tashkilotlari va kanallari;",
    "huquqiy asos, javobgarlik va ma'lumot almashish chegarasi;",
    "fuqaro identifikatsiyasi va karta bilan bog'lash ishonchliligi;",
    "xodim rollari va ruxsatlar matritsasi;",
    "Case holatlari, javob muddati va eskalatsiya qoidalari;",
    "shaxsiy ma'lumotlar, saqlash muddati, audit va hodisaga javob siyosati;",
    "xavfsizlik arxitekturasi va mustaqil sinov natijalari;",
    "uzilish, tiklash va bank kanali ishlamasligi bo'yicha mashqlar;",
    "fuqaro uchun yordam, shikoyat va tuzatish yo'li; KPI va pilotni to'xtatish mezonlari."
]
for p in pilot:
    doc.add_paragraph(p, style='List Bullet')

doc.add_paragraph("Signal sonining o'zi muvaffaqiyat mezoni emas. Javob vaqti, noto'g'ri signal ulushi, tasdiqlangan natijalar, murojaat yo'qolishi, kanal xatolari, fuqarolar tushunishi, FP/FN va xavfsizlik hodisalari birgalikda baholanadi. Ushbu FDPning o'zi pilotni boshlash uchun ruxsat hisoblanmaydi.")

doc.add_heading("15. Ochiq masalalar, talablar reyestri va lug'at", level=1)
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
    "Qaysi KPI pilotni davom ettirish yoki to'xtatishni belgilaydi?",
    "Qaysi talablar kodda mavjud, qaysilari faqat hujjatda yoki kelajak rejasida?"
]
for i, q in enumerate(open_q, 1):
    doc.add_paragraph(f"{i}. {q}")

doc.add_paragraph("Talablar reyestri ustunlari: talab ID; talab matni; manba/bob; holat belgisi; xavf darajasi; mas'ul tomon; amalga oshirish dalili; sinov ID; sinov natijasi; ochiq savol; tasdiqlovchi; sana va versiya.")

doc.add_paragraph("Lug'at:")
doc.add_paragraph("• Signal: shubha yoki hodisa haqidagi boshlang'ich xabar.", style='List Bullet')
doc.add_paragraph("• Case: tekshirish va qarorlar tarixini saqlovchi ish yozuvi.", style='List Bullet')
doc.add_paragraph("• Hamkor-bank: tegishli kelishuv va vakolatli ma'lumot almashish kanali mavjud bank.", style='List Bullet')
doc.add_paragraph("• Texnik qabul tasdig'i: xabar kanal tomonidan qabul qilinganini bildiruvchi texnik dalil, bank qarori emas.", style='List Bullet')
doc.add_paragraph("• Provenance: ma'lumot manbasi, vaqti va kelib chiqish izlari.", style='List Bullet')
doc.add_paragraph("• Least privilege: vazifa uchun zarur eng kam vakolat.", style='List Bullet')
doc.add_paragraph("• FP/FN: noto'g'ri ijobiy va noto'g'ri salbiy natijalar.", style='List Bullet')
doc.add_paragraph("• Recall@10: tegishli natijalarning top-10 ichida topilish ulushi.", style='List Bullet')
doc.add_paragraph("• RPO/RTO: tiklashda yo'qotilishi mumkin bo'lgan ma'lumot davri va xizmatni tiklash maqsadli vaqti.", style='List Bullet')

doc.add_paragraph("Yakuniy qoida: ushbu FDP talablar va sinov mezonlarini belgilaydi; u implementatsiya mavjudligini, bank integratsiyasi ishlashini yoki productionga tayyorlikni o'zi bilan isbotlamaydi. FINZANJIR V14 asosiy konsepsiyasi o'zgartirilmaydi.")

save_path = "/sdcard/Download/FINZANJIR_Fuqaro_Xavfsizligi_TUZATILGAN.docx"
doc.save(save_path)
print("MUVAFFAQIYATLI YARATILDI: " + save_path)
