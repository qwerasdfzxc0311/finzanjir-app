# FINZANJIR v4 — Yagona ish jarayoni, ochiq ko‘rish prototipi

**Branch:** `finzanjir-v4-unified-workflow-uz`  
**Streamlit main file:** `finzanjir_v4/app.py`

## Hozirgi interfeys

v4 ommaviy interfeysi yagona, mobilga mos va **read-only** ko‘rish rejimida ishlab chiqilmoqda. Tashrifchilar bo‘limlar orasida yurishi, qatlamlarni qidirishi va sintetik misollarni ko‘rishi mumkin. Ommaviy interfeysda Case holatini saqlash, Human Review qarorini kiritish, ma’lumot yozish yoki sozlamani o‘zgartirish tugmalari yo‘q.

## Asosiy bo‘limlar

- Bosh sahifa — loyiha maqsadi, chegaralari va jarayonning umumiy ko‘rinishi.
- Yagona ish jarayoni — hodisadan ma’lumot sifati, signal/dalil, Case mezonlari va Human Reviewgacha.
- 16 qatlam — har bir qatlamning sodda izohi, maqsadi, savoli, talab darajasidagi kirish/chiqishi va cheklovi.
- Signal va dalillar — indikator, dalil, qarshi dalil va noma’lum jihatlarni ajratish.
- Case markazi — faqat sintetik Case va rozilik doirasining alohida ko‘rinishi.
- Human Review — mutaxassis ko‘rib chiqishi kerak bo‘lgan savollar va mumkin bo‘lgan natijalar; qaror kiritish yo‘q.
- Qatlamlararo xarita — jarayon bosqichlari va mazmuniy qatlam qamrovi; rasmiy LINK-ID yoki texnik API deb ko‘rsatilmaydi.
- Sintetik sinovlar — tushuntiruvchi ssenariylar, real aniqlik da’vosi emas.
- Atamalar va cheklovlar — oddiy va texnik izohlar.

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

- Barcha ko‘rsatilgan hodisalar sintetik namuna.
- 16 qatlam katalogi talablar mazmunini tushuntiradi; barcha qatlamlar to‘liq implementatsiya qilingan yoki ekspertlar tasdiqlagan degani emas.
- Har bir qatlam holati PLANNED / EXPERT_VALIDATION_PENDING deb qaraladi.
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
