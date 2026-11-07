# FINZANJIR v3 — V317 manbasini qayta ishlatish va xatolarni oldini olish auditi

Sana: 2026-11-07
Yangi branch: finzanjir-v3-synthetic-ai-uz

## Versiyalarni chalkashtirmaslik

- Foydalanuvchi yuborgan AI source arxivi nomi: FINZANJIR V317 SEMANTIC GATE + DOMAIN EXPANSION.
- Shu arxivdagi Android manba hujjatlarida versionCode 303 va versionName 3.2-retrieval-guard-candidate ko'rsatilgan.
- Arxiv tayyor APK emas; Qwen3-1.7B GGUF model fayli ichiga qo'shilmagan.
- Ushbu GitHub branch — yangi Streamlit v3 ishlab chiqish yo'nalishi. U Android APKning V317 yoki 3.2 release'i deb atalmasligi kerak.

## V317 manbasidan nimani oldik

- FINZANJIR konsepsiyasiga oid 33 ta o'zbekcha bilim kartasi.
- Semantik qidiruv, evidence gate, abstention, candidate va authoritative bilim ajratish tamoyillari.
- Model javobi avtomatik ravishda haqiqat bo'lmasligi, inson ko'rigi va manba talab qilinishi haqidagi xavfsizlik qoidalari.

33 ta yozuvning barchasi candidate_not_authoritative maqomida saqlanadi. Ular rasmiy tasdiqlangan bilim sifatida ko'rsatilmaydi. Butun 4,671 yozuvli indeks ko'r-ko'rona import qilinmadi: unda turli tillar, turli domenlar, arxiv va tasdiqlanmagan materiallar bor. V317 kengaytirish navbatidagi biologiya, astronomiya va boshqa umumiy domenlar FINZANJIR bank bilim bazasiga qo'shilmadi.

## Oldingi xatolarni takrorlamaslik

1. Bitta umumiy token mosligi asosida aloqasiz bilimni javobga qo'shmaslik.
2. Yetarli dalil bo'lmasa abstention — "ichki bilim yetarli emas" deb aytish.
3. Candidate materialni Authoritative KBga avtomatik ko'tarmaslik.
4. Muallif, bank integratsiyasi, production tayyorligi yoki real aniqlik haqida manbasiz da'vo qilmaslik.
5. Bir qurilma yoki umumiy atribut mosligini shaxs aybdorligining isboti deb ko'rsatmaslik.
6. Risk score'ni kalibrlangan firibgarlik ehtimoli deb talqin qilmaslik.
7. Sintetik test yorliqlarini ekspert tasdiqlagan ground-truth deb qabul qilmaslik.
8. Model importi yoki source test PASS natijasini Android inference ishladi deb ko'rsatmaslik.

## V317 arxivida ko'rilgan tekshiruv chegaralari

- Arxivdagi test hisobotlari source-level va mock sinovlarni ko'rsatadi; APK build, Android runtime, JNI link va Qwen inference tasdiqlanmagan.
- 2,000 savolli bankda javob bo'sh emasligi testi javob mazmunan to'g'ri ekanini bildirmaydi. Hisobotda oddiy diagnostik token mosligi 470/2,000 (23.5%) deb ko'rsatilgan; bu semantik sifat o'lchovi emas.
- V316 semantik/adversarial testlarining PASS natijalari barcha savollarga to'g'ri javob berilishini kafolatlamaydi.
- Qwen3-1.7B-Q8_0 model fayli alohida yuklanishi kerak; JNI/native kutubxonalar va telefon inference'i mustaqil release gate.

## Yangi v3 prototipidagi hozirgi chegaralar

- AI: tashqi model/API chaqirmaydigan o'zbekcha lexical evidence retrieval. Bu generativ LLM emas.
- Sun'iy banklar: to'rtta manba nomi va 400 sintetik hodisa; real bank emas.
- Duplicate delivery: bir event ID bilan takroriy yetkazish urinishlari test metama'lumotida ifodalanadi; bank webhook transporti bilan real ikki martalik yuborish hali ulanmagan.
- Bank javobi: referral/data request paketlari faqat READY_NOT_SENT yoki navbat holatida; haqiqiy bankka yuborilmaydi.
- L11: PAUSE/STOP/RESUME/RESET, navbatni saqlash va process restart aniqlanganda PAUSE recovery.
- 400 holatning kutilgan yorliqlari muhandislik ssenariy taxminlari; bank ekspertlari bilan tekshirilishi shart.
- Cloud deployment va Android offline deployment ikki alohida muhit. Streamlit Cloud'da ishlash telefon internetisiz offline ishlash degani emas.

## Keyingi tasdiqlash darvozalari

1. GitHub Actions: syntax + unit/regression tests.
2. Streamlit Cloud: app launch, buttons, queue persistence, UI and SQLite runtime.
3. Full 400-event run: confusion matrix, false positives/false negatives, duplicate/data-quality cases.
4. Domain review: FINZANJIR signal registry, 16 layers and bank data field contracts.
5. Local generative model: GGUF import, JNI build/link, device inference, RAM/latency/cancel and Uzbek answer quality.
6. Android packaging: APK build/install/offline test.
7. Bank pilot: only after legal, security, bank approval and expert validation.

Hech bir darvoza o'tmagan bo'lsa, keyingi bosqich tayyor deb e'lon qilinmaydi.
