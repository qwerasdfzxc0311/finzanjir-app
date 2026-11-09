# FINZANJIR Android — 16 qatlam bo‘yicha dastlabki implementatsiya farqi

**Taqqoslangan branch:** finzanjir-android-v1  
**Audit branch:** finzanjir-knowledge-audit-2026-11  
**Maqom:** statik kod ko‘rigi; real qurilma, bank sandbox yoki production sinovi emas.

Ushbu matritsa 16 qatlam hujjatidagi talablar bilan Android Kotlin/Compose prototipining ko‘rilgan kodini taqqoslaydi. Ekranda nom yoki matn ko‘rinishi qatlamning to‘liq ishlayotganini anglatmaydi.

| Qatlam | Hujjatdagi vazifa | Ko‘rilgan Android dalili | Dastlabki holat |
|---|---|---|---|
| L01 Evidence & Data Provenance | Manba, vaqt, kelib chiqish va dalil yaxlitligi | KB javobida source ID/version/section/path ko‘rsatiladi; real tranzaksiya dalil oqimi yo‘q | **Qisman** — faqat bilim yozuvi manbasi |
| L02 Data Quality & Reliability | To‘liqlik, eskirish, dublikat, noto‘g‘ri format nazorati | Real bank ma’lumot ingestioni va data-quality pipeline ko‘rilmadi | **Mavjudligi tasdiqlanmagan** |
| L03 Risk & Uncertainty | Risk va noaniqlikni dalil bilan ajratish | Statik demo jarayoni va izohlar bor; kalibrlangan risk modeli yo‘q | **Demo/konsept** |
| L04 Human Oversight & Correction | Vakolatli inson ko‘rigi va tuzatish | Human Review ekrani statik checklist ko‘rsatadi; haqiqiy ish navbati/rol tekshiruvi yo‘q | **UI namoyishi** |
| L05 Rule & Model Governance | Qoida/model versiyasi, tasdiq, rollback | Kodda boshqariladigan rule registry yoki tasdiqlash jarayoni ko‘rilmadi | **Mavjudligi tasdiqlanmagan** |
| L06 Data Disclosure & Sharing Control | Qonuniy, minimal va ruxsatli almashuv | Bank adapteri yoki data-sharing ruxsat mexanizmi yo‘q | **Mavjudligi tasdiqlanmagan** |
| L07 Automation Safety & Control | Xavfsiz avtomatlashtirish, pauza, kill switch | Real avtomatik bank amali yo‘q; xavfsizlik matni faqat tushuntirish darajasida | **Mavjudligi tasdiqlanmagan** |
| L08 Transaction Chain & Case Correlation | Tranzaksiya zanjiri va Case bog‘lash | Case DEMO yozuvi va jarayon tavsifi statik; real bog‘lash engine yo‘q | **Demo/konsept** |
| L09 Citizen Transparency & Appeal | Fuqaro ko‘rinishi, tuzatish va shikoyat | Alohida fuqarolik workflow va appeal backend ko‘rilmadi | **Mavjudligi tasdiqlanmagan** |
| L10 Privacy & Data Lifecycle | Ma’lumotga kirish, saqlash, o‘chirish | Real shaxsiy/bank ma’lumoti ulanmagan; server-side lifecycle yo‘q | **Mavjudligi tasdiqlanmagan** |
| L11 Security Incident Response | Hodisani aniqlash, javob va tiklash | Android prototipida operatsion incident-response backend ko‘rilmadi | **Mavjudligi tasdiqlanmagan** |
| L12 Knowledge Governance & AI Reliability | Bilim maqomi, manba, AI cheklovi, tuzatish | Candidate maqomi va manba izi ko‘rsatiladi; mustaqil tasdiq workflow va to‘liq conflict handling yo‘q | **Qisman** |
| L13 Testing & Independent Evaluation | Regressiya, mustaqil baholash, dalil | GitHub Actions assembleDebug build mavjud; bu 16 qatlam testlari yoki ekspert bahosi emas | **Qisman — faqat build dalili** |
| L14 Bank Integration Readiness | Bank bilan kelishuv, API, sandbox, security acceptance | README bank API va real ma’lumot ulanmaganini bildiradi | **Kelajak talabi** |
| L15 Performance & Capacity Management | Yuklama, latency, sig‘im va degradatsiya | Yuklama/stress benchmark dalili ko‘rilmadi | **Mavjudligi tasdiqlanmagan** |
| L16 Impact & Harm Reduction | FP/FN, zarar, foyda va ta’sirni o‘lchash | Pilot ground truth/KPI o‘lchovi yo‘q | **Mavjudligi tasdiqlanmagan** |

## Namoyishda qanday ko‘rsatish kerak

- Hozirgi APK’da haqiqatan ko‘rsatiladigan narsalar: ekranlar, statik jarayon tavsifi, sintetik signal/Case, bilim qidiruvi va topilgan bilim yozuvlarining manba metama’lumoti.
- Hozircha ishlayotgan deb aytilmaydigan narsalar: real bank signal oqimi, real karta/operatsiya, banklararo Case uzatish, server RBAC, real Human Review navbati, real-time monitoring, avtomatik bloklash, production incident response.
- GitHub Actions assembleDebug muvaffaqiyati faqat build kompilyatsiyasini tasdiqlaydi. U qurilmaga o‘rnatish, barcha ekranlarning runtime xulqi, bank integratsiyasi yoki xavfsizlik qabulini isbotlamaydi.

## Keyingi kod auditida tekshiriladigan narsalar

1. Bilim bazasining JSON schema va har bir yozuv maydonlari.
2. 1,121 yozuvning to‘liq soni, record type, source coverage va duplicate mapping.
3. AI qidiruvining query frame, domain filtering, source ranking, contradiction handling, abstention va javob-savol mosligi.
4. Muallif tasdig‘i va mustaqil ekspert/bank tasdig‘ining UI’da ikki alohida o‘q sifatida ko‘rsatilishi.
5. Sintetik demo ma’lumotlar production ma’lumotidan aniq ajratilishi.
6. Testlar uchun mustaqil holdout to‘plami va qayta bajariladigan natijalar.

**Muhim:** bu matritsa kodning ko‘rilgan qismiga asoslangan statik audit. Kodda topilmagan imkoniyat boshqa faylda bor-yo‘qligi alohida tekshirilmaguncha “umuman mavjud emas” deb qat’iy xulosa qilinmaydi.
