# FINZANJIR — yagona ish jarayoni (integratsiya spetsifikatsiyasi)

## Maqsad
Fuqaro murojaati, signal, Case, Human Review, tuzatish, bank ko‘rigi va yakuniy natija bitta umumiy Case identifikatori bilan bog‘lanadi. Ekranlar alohida ma’lumot nusxalarini yuritmaydi.

## Joriy demo oqimi
1. Fuqaro hodisa turini tanlaydi va maxfiy to‘lov ma’lumotlarisiz tavsif kiritadi.
2. Tizim murojaatni lokal demo omboriga yozadi, Case ID yaratadi va izohlanadigan demo signal biriktiradi.
3. Signallar, Jarayon, Case va Human Review navigatsiyasi ayni Case reyestrini ochadi.
4. Mutaxassis demo holatida qo‘shimcha ma’lumot/tuzatish so‘rashi, mock bank ko‘rigi so‘rovini tayyorlashi, Case'ni yopishi yoki qayta ko‘rikka qaytarishi mumkin.
5. Tuzatish qayta ko‘rik navbatiga tushadi; mock bank javobi Case ichida alohida qayd etiladi.
6. Har bir harakat vaqt tamg‘asi bilan Case voqealar tarixiga qo‘shiladi.

## Holatlar
- `REVIEW_PENDING`: inson ko‘rigini kutmoqda.
- `CORRECTION_REQUIRED`: qo‘shimcha ma’lumot yoki tuzatish so‘ralgan.
- `NOT_CONFIRMED`: mutaxassis mavjud dalil bilan signalni tasdiqlamadi; ayblov chiqarilmaydi.
- `BANK_REVIEW_REQUESTED`: mock bank adapteriga demo so‘rov tayyorlangan.
- `BANK_RESPONSE_RECORDED`: demo bank javobi Case tarixiga kiritilgan.
- `CLOSED`: demo Case yopilgan.

## O‘zgarmas xavfsizlik qoidalari
- Signal, risk indikatori yoki Case aybdorlik hukmi emas.
- Demo qoidalari kalibrlangan Risk Score yoki real firibgarlik detektori sifatida ko‘rsatilmaydi.
- Mock bank so‘rovi tashqi tarmoqqa yuborilmaydi; haqiqiy bank qarori faqat bank vakolatida.
- Avtomatik bloklash, hisob yopish, pulni qaytarish yoki firibgarlikni tasdiqlash mavjud emas.
- CVV, OTP, to‘liq karta raqami, parol va boshqa maxfiy ma’lumotlarni demo maydonlariga kiritmang.
- Hozirgi saqlash usuli qurilmadagi SharedPreferences; bu production ma’lumot ombori, shifrlangan server audit logi yoki ko‘p foydalanuvchili sinxronlash emas.

## Keyingi texnik bosqichlar
1. Case, Signal, Evidence, ReviewDecision, CorrectionRequest, BankRequest va AuditEvent uchun alohida typed domain modellar.
2. Repository va use-case qatlamini UI'dan ajratish; mock/real bank adapteri uchun aniq interfeys.
3. Fuqaro va mutaxassis ish ko‘rinishlarini bir xil Case ID va ruxsatli amallar bilan ulash; server RBAC va audit.
4. Dalil/qarshi dalil, manba kelib chiqishi, rozilik doirasi va noma’lum holatlarni strukturali saqlash.
5. API kontrakti, idempotency, xatolarni qayta ishlash, sinxronlash va avtomatik testlar.
6. Real bank integratsiyasini faqat ruxsat, shartnoma, xavfsizlik bahosi va bank sinov muhiti mavjud bo‘lganda ulash.

## Qabul mezonlari
- Yaratilgan Case ilova qayta ochilganda demo holatda saqlanadi.
- Har bir harakat o‘sha Case ID ostida tarixga yoziladi.
- Tuzatish Case'ni qayta ko‘rik holatiga qaytaradi.
- Mock bank javobi real bank javobi deb ko‘rsatilmaydi.
- Biror UI harakati karta/hisob/tranzaksiyani bloklamaydi yoki real pul operatsiyasini bajarmaydi.
- CI build va real Android qurilma sinovi muvaffaqiyatli bo‘lmaguncha integratsiya production tayyor deb belgilanmaydi.
