# FINZANJIR — yagona AI bilim korpusi migratsiyasi auditi

**Sana:** 2026-11-09  
**Holat:** manba integratsiyasi tekshirilgan; GitHub aktiv Android assetiga ko‘chirish va qurilmadagi yakuniy sinov hali alohida bajarilishi kerak.

## 1. Tekshirilgan manbalar

1. `Finzanjir konsepsiyasi va qoshimsha malumotlar hujjatlar (1).zip` — 14 ta matnli hujjat (PDF/DOCX/PPTX), shu jumladan V14 konsepsiya, bank integratsiyasi texnik arxitekturasi, AI va bilim tizimi, 16 qatlam, signal reyestrlari, qo‘shimcha amaliy talablar va tarixiy ishchi hujjat.
2. `FINZANJIR_GLOBAL_KNOWLEDGE_SYSTEM_2026-10-12_v2.1_SEQUENTIAL_HYBRID_AI.zip` — oldingi AI knowledge index va uning manba/ishlash siyosati.
3. `FINZANJIR_KNOWLEDGE_MIGRATION_2026-11-09.zip` — V317 bazasi, yangi hujjat bo‘laklari va 16 qatlam yozuvlarini birlashtirgan migratsiya nomzodi.

## 2. Korpus tarkibi

- Yakuniy migratsiya nomzodi: **5,607 yozuv**.
- V317 asosiy yozuvlari: 4,671.
- Yangi hujjatlardan ajratilgan bo‘laklar: 893.
- 16 qatlam uchun alohida IDli yozuvlar: 16 (`V4-L01` ... `V4-L16`).
- AI v2.1 dagi 4,656 yozuvning barchasi ID bo‘yicha migratsiya nomzodida saqlangan.
- ID takrorlari: 0.
- Bir xil normallashtirilgan matnli guruhlar: 3 (jami 6 yozuv). 27 ta vizual OCR nomzodi (22 PDF ichki tasvir + 5 mustaqil diagramma) qo‘shildi; barchasi tekshiruv talab qiladigan candidate maqomida. Ular faqat bir xil matn sababli o‘chirilmadi; manba izi saqlanadi va qidiruv natijasida bir xil javobning qayta-qayta ko‘rinishi oldi olinishi kerak.

## 3. Maqom va tasdiqlash

Yangi yuklangan 893 hujjat bo‘lagi `candidate_not_authoritative` maqomida. Ular ekspert ko‘rigisiz tasdiqlangan siyosat yoki amalda ishlayotgan funksiya deb ko‘rsatilmaydi. V317 yozuvlarining avvalgi maqomlari saqlangan; `unclassified` va `index_only` yozuvlar alohida nazorat talab qiladi. 16 qatlam katalogi funksional/nazorat mas’uliyatlarini ifodalaydi; har biri alohida ekran yoki server bo‘lishi shart emas.

## 4. O‘zgarmas FINZANJIR qoidalari

- Shubhali ≠ firibgar/aybdor.
- Signal ≠ firibgarlik isboti.
- Risk balli ≠ huquqiy hukm.
- Fraud Graph aloqasi ≠ ayb isboti.
- Case ≠ yakuniy qaror.
- AI yakuniy bank, huquqiy yoki tergov qarorini mustaqil qabul qilmaydi.
- FINZANJIR bank API bilan real integratsiyalashgan deb faqat shartnoma, ruxsat, xavfsizlik tekshiruvi va runtime dalili bo‘lganda aytiladi.
- CVV, OTP, PIN, parol va maxfiy kalitlar bilim korpusiga kiritilmaydi.

## 5. AI ishlash arxitekturasi

Savol/kontekst → til va matnni normallashtirish → intent → maxfiylik/xavfsizlik tekshiruvi → mos bilim qidiruvi → manba/versiya/maqom/ziddiyat → dalil yetarliligi → javob sintezi → yakuniy xavfsizlik tekshiruvi → nazoratli feedback.

Bilim qo‘shilishi model vaznlarini fine-tuning qilish emas. Ushbu migratsiya RAG/qidiruv korpusini kengaytiradi; lokal LLM ulanishi, inference sifati va haqiqiy fine-tuning alohida tekshiriladi.

## 6. Tekshiruv natijalari

Migratsiya paketining dastlabki 5,580 yozuvli korpusida 23/23 smoke-test PASS bo‘lgan. 5,607 yozuvli vizual OCR qo‘shilgan korpusda ham Kotlin BM25-ekvivalent ranking simulyatsiyasi bo‘yicha 23/23 source-aware regression PASS. Bu Android runtime testi emas. APK build, o‘rnatish, telefon sinovi va AI javoblarining to‘liq regressiya testi bajarilgan deb talqin qilinmaydi.

## 7. GitHub branchida bajarilgan kod ishlari

- AI qidiruvi oddiy token ustma-ustligidan BM25-uslubidagi term weightingga o‘tkazildi.
- Fuqaro va Mutaxassis qidiruv ko‘rinishlari qo‘shildi. Mutaxassis ko‘rinishi texnik, qatlamlar, bank integratsiyasi va tarixiy loyiha manbalarini ham qidiradi; bu demo filtri, server autentifikatsiyasi yoki RBAC emas.
- Bir xil matnli yozuvlar korpusdan o‘chirilmaydi; javobda bir marta ko‘rsatiladi va mos kelgan barcha manba izlari saqlanadi.
- Kotlin knowledge engine minimal Android/JSON stub muhitida sintaksis bo‘yicha kompilyatsiyadan o‘tdi. GitHub Actions orqali Android Gradle debug APK build ham muvaffaqiyatli yakunlandi (run 42680177385 va 42680010769). Bu faqat build; 5,607 yozuvli asset hali aktiv emas va qurilmadagi runtime sinovi bajarilmagan.
- GitHub Actions workflow yangi branchni ham kuzatadigan qilib yangilandi; tekshiruv vaqtida ushbu branch uchun workflow run hali qaytmadi.

## 8. Hali ochiq qolgan ishlar

1. 5,607 yozuvli JSON assetni GitHub Android branchidagi eski 1,121 yozuvli asset bilan almashtirishdan oldin manba/maqom/duplikat nazoratini yakunlash.
2. 37 ta PDF ichki rasm/diagrammaning 26 tasida OCR urinishlari bajarildi; 22 tasining matni va 5 ta mustaqil diagramma OCRi 27 ta candidate yozuvga kiritildi. Ularning barchasi hali vizual ekspert tekshiruvini kutmoqda.
3. 3 ta aynan takror matnli guruhni source provenance yo‘qotmasdan retrieval natijasida bir marta ko‘rsatish.
4. Android Kotlin qidiruvi, fuqarolik/mutaxassis rejimi, 16 qatlam ID marshruti, manba ko‘rsatish va yetarli dalil bo‘lmagandagi fallbackni 5,580 yozuv bilan sinash.
5. APK build va real qurilmadagi sinovlarni alohida bajarish.

## 9. Muhim holat

Ushbu audit GitHub branchidagi amaldagi Android asset allaqachon 5,580 yozuvga yangilandi degani emas. Migratsiya ZIPida 5,607 yozuvli asset mavjud. SHA-256: `f3457b372c5e7f79a0875603cb33987a7720f96061c1ac23ea038b69f2dfb250`. GitHub branchidagi aktiv asset va manifestni yangilash faqat to‘liq asset aynan shu branchga yozilib, SHA-256 va record count qayta tekshirilgandan keyin tasdiqlanadi.
