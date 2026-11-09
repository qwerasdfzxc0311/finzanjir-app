# FINZANJIR v4 — Yagona ish jarayoni, ochiq ko‘rish prototipi

**Branch:** `finzanjir-v4-unified-workflow-uz`  
**Streamlit main file:** `finzanjir_v4/app.py`

## Hozirgi interfeys

v4 ommaviy interfeysi yagona, mobilga mos va **read-only** ko‘rish rejimida ishlab chiqilmoqda. Bo‘lim tanlash, qatlam qidiruvi va sintetik misol tanlash faqat ko‘rsatiladigan ma’lumotni o‘zgartiradi. Ommaviy interfeysda Case holatini saqlash, Human Review qarorini kiritish, ma’lumot yozish yoki tizim sozlamalarini o‘zgartirish funksiyasi yo‘q.

## Ochiq bo‘limlar

1. Bosh sahifa — loyiha maqsadi, chegaralari va umumiy jarayon.
2. Boshqaruv paneli — v4 dagi to‘rtta sintetik namuna bo‘yicha holatlar.
3. Sun’iy bank laboratoriyasi — v3 dagi alohida 4 manbali/400 ssenariyli laboratoriya yo‘nalishi haqida; v4 ga hali ulanmagan.
4. Yagona ish jarayoni — hodisadan ma’lumot sifati, signal/dalil, Case mezonlari va Human Reviewgacha.
5. Signallar reyestri — indikator, dalil, qarshi dalil va noma’lum jihatlar.
6. 16 qatlam — har bir qatlamning sodda izohi, maqsadi, savoli, talab darajasidagi kirish/chiqishi va cheklovi.
7. Case markazi — sintetik Case va rozilik doirasining alohida ko‘rinishi.
8. Human Review — mutaxassis ko‘rib chiqishi kerak bo‘lgan savollar va mumkin bo‘lgan natijalar; qaror kiritish yo‘q.
9. Banklararo tahlil — atribut mosligi bo‘yicha ehtiyot chegaralari; real banklararo grafik emas.
10. KPI dashboard — faqat sintetik jarayon sonlari; aniqlik yoki FP/FN natijasi emas.
11. Fuqaro uchun tushuntirish — konsepsiyani sodda tilda izohlash.
12. Audit jurnali — ko‘rgazmali vaqt chizig‘i; doimiy audit ombori emas.
13. Qatlamlararo xarita — jarayon bosqichlari va mazmuniy qatlam qamrovi; rasmiy LINK-ID yoki texnik API emas.
14. Sintetik sinovlar — tushuntiruvchi ssenariylar, real aniqlik da’vosi emas.
15. Atamalar va cheklovlar — oddiy va texnik izohlar.

## Ishga tushirish

Streamlit Cloud sozlamasida:
- Branch: `finzanjir-v4-unified-workflow-uz`
- Main file path: `finzanjir_v4/app.py`

Lokal ishga tushirish:

```bash
pip install -r requirements.txt
streamlit run finzanjir_v4/app.py
```

## Halol holat va cheklovlar

- Barcha v4 hodisalari sintetik namuna.
- 16 qatlam katalogi talablar mazmunini tushuntiradi; barcha qatlamlar to‘liq implementatsiya qilingan yoki ekspertlar tasdiqlagan degani emas.
- Har bir qatlam PLANNED / EXPERT_VALIDATION_PENDING holatida ko‘riladi.
- Qatlamlararo ko‘rinish jarayon xaritasi; rasmiy LINK-ID, mustaqil servis yoki API mavjudligini anglatmaydi.
- Case va Human Review faqat ko‘rgazmali; haqiqiy reviewer autentifikatsiyasi, vakolat nazorati va doimiy audit ulanmagan.
- 400 hodisali v3 laboratoriyasi v4 yagona jarayoniga hali integratsiya qilinmagan.
- AI moduli v4 interfeysga ulanmagan va alohida tekshiruv bosqichi.
- Haqiqiy bank API, mijoz ma’lumotlari, production SSO/RBAC va production tayyorligi mavjud deb da’vo qilinmaydi.
- FINZANJIR karta, hisob yoki tranzaksiyani avtomatik bloklamaydi.
- Sintetik sinovlar real firibgarlik aniqligi yoki bank sharoitidagi samaradorlikni isbotlamaydi.

## Ishlab chiqish qarorlari

- Eski `main`, `concept-aligned-v1` va `finzanjir-v3-synthetic-ai-uz` branchlari o‘zgartirilmaydi.
- Ommaviy v4 interfeysi ko‘rish uchun; tahrirlash yoki qaror yozish funksiyalari kiritilmaydi.
- 16 qatlam nomi va vazifasi manba katalogidan olinadi; tasdiqlanmagan texnik aloqalar rasmiy aloqa sifatida ko‘rsatilmaydi.
- Keyingi bosqichlar: qatlamlararo aloqa matritsasini manba bilan tekshirish, v3 laboratoriyasini auditdan keyin integratsiya qilish, Case state machine, testlar va mobil brauzer tekshiruvi.
