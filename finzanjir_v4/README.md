# FINZANJIR v4 — Yagona ish jarayoni prototipi

**Development branch:** `finzanjir-v4-unified-workflow-uz`  
**Streamlit main file:** `finzanjir_v4/app.py`

## Ishlab chiqish maqsadi

Bitta tushunarli operator interfeysida quyidagi zanjirni ko'rsatish:

Manba/hodisa → ma'lumot sifati → 16 qatlam → signal/dalil/noma'lum → Case mezonlari → Case → Human Review → audit/yakun.

Bu yangi, alohida ishlab chiqish yo'nalishi. `main`, `concept-aligned-v1` va `finzanjir-v3-synthetic-ai-uz` branchlari saqlanadi va o'zgartirilmaydi.

## Hozirgi holat

- [x] Yangi branch ochildi.
- [x] Yagona arxitektura blueprint yozildi.
- [x] 16 qatlam nomlari va talab mazmuni manba reyestridan katalogga ko'chirildi.
- [x] Dastlabki yagona UI poydevori yaratildi.
- [ ] 16 qatlamlararo aloqa matritsasini manba bilan tekshirib, v4 ma'lumot modeliga kiritish.
- [ ] v3 sintetik bank laboratoriyasini audit qilib, v4 pipeline bilan to'g'ri integratsiya qilish.
- [ ] Case state machine va signal/evidence/unknown/consent modeli.
- [ ] Human Review vakolatlari, review checklist va audit saqlovi.
- [ ] L11 favqulodda boshqaruv va xavfsiz tiklash.
- [ ] Regression/unit/integration testlar.
- [ ] Streamlit Cloud brauzer va mobil tekshiruvi.

## Ishga tushirish

Streamlit Cloud sozlamasida branch sifatida `finzanjir-v4-unified-workflow-uz`, main file path sifatida `finzanjir_v4/app.py` tanlanadi.

Lokal ishga tushirish:

```bash
pip install -r requirements.txt
streamlit run finzanjir_v4/app.py
```

## Muhim cheklovlar

Hozirgi UI foundation'dagi barcha yozuvlar sintetik namunalar. Human Review qarorlari faqat Streamlit session state'da saqlanadi; doimiy ma'lumotlar bazasi va audit jurnali hali ulanmagan. 400 hodisali v3 laboratoriyasi v4 ga hali integratsiya qilinmagan. 16 qatlam kartalari hozircha tushuntiruvchi katalog; qatlamlar to'liq implementatsiya qilingan deb bo'lmaydi. Qatlamlararo LINK-PROP nomzodlari rasmiy LINK-ID yoki mustaqil texnik interfeys hisoblanmaydi.

FINZANJIR karta, hisob yoki tranzaksiyani avtomatik bloklamaydi. Sintetik natijalar real bank aniqligi yoki production tayyorligini isbotlamaydi.

Batafsil:
- `ARCHITECTURE_BLUEPRINT_UZ.md`
- `LAYER_CATALOG_SOURCE_UZ.md`
