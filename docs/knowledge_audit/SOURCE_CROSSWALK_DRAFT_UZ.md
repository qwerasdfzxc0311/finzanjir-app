# FINZANJIR manba → prototip crosswalk (dastlabki)

**Holat:** birinchi taqqoslash; yakuniy audit emas.  
**Ishchi branch:** `finzanjir-knowledge-audit-2026-11`  
**Qoidasi:** “import qilingan” degan da’vo faqat aniq fayl/yozuv/commit dalili topilganda beriladi. Mazmun o‘xshashligi to‘liq nusxa ko‘chirilganini anglatmaydi.

| Manba | Hozirgi prototip/repo bilan dastlabki moslik | Holat | Keyingi ish |
|---|---|---|---|
| FINZANJIR KONSEPSIYA V14 (164 sahifa) | Android manifestida 164 ta V14 sahifa yozuvi qayd etilgan. | **Qisman** — matn sahifalangan; diagramma, rasm va murakkab jadvallar vizual tekshiruvsiz. Shaxsiy profil sahifalari maxfiylik auditi talab qiladi. | Sahifa→yozuv crosswalk; diagramma va jadval tekshiruvi; muallif shaxsiy ma’lumotlarini ommaviy qidiruvdan ajratish. |
| 16 qatlam chuqur tushuntirish DOCX | Android’da 16 nomdan iborat qatlam katalogi bor. To‘liq DOCX matni va jadvallari import qilingani tasdiqlanmagan. | **Qisman / manba nusxasi tasdiqlanmagan** | Har qatlamning maqsad, chegara, kirish/chiqish, xato holati, test va qatlamlararo aloqasini manbaga bog‘lash. |
| 16 qatlam talablar va sinovlar reyestri PDF | 24 REQ/TEST jufti va 10 DEC ochiq qarori mavjud. Android’da shu reyestrning to‘liq importi ko‘rsatilmagan. | **Import dalili topilmadi** | REQ-001…024 va DEC-01…10 ni alohida reyestrga, test holatlarini “taklif” sifatida ko‘chirish. |
| Asosiy signal reyestri DOCX | Android UI’da 4 ta sintetik demo signal bor; bu 15 ta signalning to‘liq implementatsiyasi emas. | **Faqat demo qismi mavjud** | SIG-001…015 uchun manba, talab qilinadigan ma’lumot, cheklov, test va ekspert tasdig‘i holatini saqlash. |
| Kichik signallar DOCX | Android UI’da to‘liq 10 ta kichik signal reyestri ko‘rinmaydi. | **Import dalili topilmadi** | 10 signalni alohida candidate reyestrga ko‘chirish; eskirgan ball/bloklash misollarini amaldagi qoida qilmaslik. |
| Ilg‘or signallar DOCX | Android’da 6 ilg‘or signalning ishlayotgan skaneri tasdiqlanmagan. Manbaning o‘zi kelajak V2 va kelishuvga bog‘laydi. | **Kelajak / import dalili topilmadi** | 6 signalni future/conditional deb belgilash; ruxsat, privacy va platforma cheklovlarini saqlash. |
| False-positive ekspertiza tuzatishi V2 | Android UI’da common-mode false positive, circuit breaker, canary, kill switch va rollbackning amaliy bajarilishi tasdiqlanmagan. | **Kritik talablar to‘liq ko‘chirilgani tasdiqlanmagan** | S-01…S-07 va T-01…T-06 ni talab/test reyestriga kiritish; eski signal ballari bilan ziddiyatini qayd etish. |
| Qo‘shimcha amaliy talablar PDF (19 sahifa) | 36 bo‘lim, jumladan 29–36 qo‘shimcha himoya va test bandlari bor. Android’da to‘liq matnli import dalili yo‘q. | **Import dalili topilmadi** | 1–36 bo‘limni, jadvallar, G0–G6 darvozalar, H-01…H-10, SEC testlar va ochiq qarorlarni to‘liq manbali yozuvlarga ajratish. |
| Qo‘shimcha FDP ishchi nusxasi DOCX | Android’da kuzatuvlar va takliflarning to‘liq, manbaga bog‘langan nusxasi tasdiqlanmagan. | **Import dalili topilmadi** | Muallif kuzatuvi / eshitilgan ma’lumot / gipoteza / taklifni alohida ajratib, cheklangan ko‘rinish siyosatini qo‘llash. |
| Fuqaro xavfsizligi FDP DOCX | Android UI’da real citizen workflow, hamkor-bank kartalari va server-side RBAC mavjudligi tasdiqlanmagan. | **Asosan kelajak talab; import dalili topilmadi** | Karta oxirgi 4 raqam, “Men bu kartani tanimayman”, yuborish statusi, bank javobi, xodim vakolati va 33 sinov bandini ko‘chirish. |
| Bank integratsiyasi texnik arxitekturasi PDF (V1.0, 66 sahifa) | Joriy Android manifesti original V8 hujjati to‘liq import qilinmaganini aytadi. ZIP-1 dagi 66 sahifali V1.0 hujjat aynan V8 deb tasdiqlanmagan va Android’da alohida manba sifatida yo‘q. | **Joriy Android’da topilmadi; versiya identifikatsiyasi ochiq** | V1.0 hujjatni alohida source ID bilan kiritish; avvalgi V8 deb nomlamaslik; API/ACK/idempotency, banklararo oqim va xavfsizlik bo‘limlarini solishtirish. |
| AI va bilim tizimi besh hujjati PDF (29 sahifa) | Android manifestida 42 ta AI arxitektura yozuvi bor, lekin aynan ushbu besh hujjatning sahifa/bo‘lim crosswalk’i yo‘q. | **Qisman mazmuniy o‘xshashlik; to‘liq import tasdiqlanmagan** | 5 hujjatni alohida bo‘limlarga ajratish: AI ichki oqimi, KB/xotira, mustaqil baholash, xato/regressiya, xavfsizlik/maxfiylik. |
| FINZANJIR taqdimoti PPTX (17 slayd) | Asosiy tamoyillar V14 bilan takrorlanadi; Android’da slaydlarning to‘liq manbali nusxasi tasdiqlanmagan. | **Taqdimot manbasi; bilimning mustaqil nusxasi emas** | Faqat V14 bilan farq qiladigan yoki ekspert taqdimotiga kerakli ma’lumotni crosswalk qilish; mexanik dublikat yaratmaslik. |
| Tarixiy ishchi hujjat | Eski nom va tarixiy materiallar hozirgi faol bilimdan ajratilishi kerak. | **Arxiv-only** | Asl nusxani tarixiy arxivda saqlash; faol FINZANJIR javoblarida eski loyiha nomini ishlatmaslik. |
| V317 full source candidate archive (7,053) | Joriy Android 1,121 yozuvli korpus; README’da V317 legacy’dan 33 yozuv qayd etilgan. | **Tanlangan qismgina** | To‘liq indexni ko‘r-ko‘rona import qilmaslik; metadata va source auditdan o‘tgan yozuvlarni tanlash. |
| V317 active index (4,671) | Joriy Android’ga to‘liq ko‘chirilmagan. | **Ko‘chirilmagan / faqat tanlangan mantiq** | Faqat kerakli konseptlarni, metadata tozalangach va Android Kotlin’ga moslashtirgach port qilish. |
| V317 515 ensiklopediya yozuvi | FINZANJIR domeniga xos emas. | **Alohida umumiy bilim qatlami** | Moliyaviy xavfsizlik qoidalari bilan aralashtirmaslik; kerak bo‘lsa mustaqil domain routing. |
| V317 2,000 regression savollari | Test dataset sifatida mavjud; faol bilimga kiritilmasligi kerak. | **Test-only** | Train/repair va holdout testlarni ajratish; test savollarini javob dalili sifatida ishlatmaslik. |
| V317 Java/WebView + Qwen JNI yo‘li | Joriy Android Kotlin/Compose branchidan farq qiladi; JNI/Qwen real qurilmada tasdiqlanmagan. | **Ko‘chirib olinmaydi** | BM25 va Qwen/JNI’ni ko‘chirmaslik; savol frame, evidence gate, abstention va javob mosligi g‘oyalarini tanlab, Kotlin’da alohida sinash. |

## Ziddiyatlar va maxsus qarorlar

1. **Eski ball/bloklash misollari:** signal hujjatlarida 85/90/95 ball, avtomatik Case yoki “Bloklash” misollari bor. Ular manba tarixida saqlanadi, lekin tasdiqlangan operatsion qoida emas. False-positive V2 dagi shadow mode, bank vakolati, canary, circuit breaker, kill switch, rollback va legal-only testlar keyingi xavfsizlik talablarida ustuvor.
2. **Silent Hold:** taqdimotdagi atama bankning tranzaksiyani ushlab qolish vakolati bilan chalkashishi mumkin. Mutaxassislar aniqlamaguncha u bank qarori yoki FINZANJIR bloklash funksiyasi sifatida talqin qilinmaydi.
3. **SINBAD/ATMOS:** V14 10-bobida uchraydi, lekin hozirgi FINZANJIR ish doirasiga kiritilmaydi. Asl manbada tarix sifatida qoladi.
4. **Muallif profili:** mualliflik manbasi ko‘rsatilishi mumkin; shaxsiy telefon, email yoki manzil umumiy AI qidiruviga avtomatik chiqarilmaydi.
5. **Model o‘qitish:** hujjat importi yoki knowledge indexing model vaznlarini o‘qitish emas. Quantization alohida model tanlangandan keyin baholanadi.

## Keyingi tekshiruvlar

- Har bir manbaning to‘liq matni, jadvallari, diagrammalari va sahifa raqamlarini crosswalk qilish.
- ZIP-2 ichidagi 224 faylni source/test/code/archive toifalariga ajratish; barcha 224 faylni bir xil darajada faol bilim deb qabul qilmaslik.
- Android Kotlin kodidagi real implementatsiya bilan REQ/TEST talablarini birma-bir solishtirish.
- Dastlabki crosswalk yakunlangach, to‘liq matn nusxalarini alohida source-preserving fayllarga joylash rejasini tuzish.

**Eslatma:** bu jadval birinchi audit ko‘rinishi. “Import dalili topilmadi” — qidirilgan repo snapshotida aniq dalil ko‘rinmaganini bildiradi; manba boshqa branch yoki oldingi faylda umuman yo‘q degan universal xulosa emas.
