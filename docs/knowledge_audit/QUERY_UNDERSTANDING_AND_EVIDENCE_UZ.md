# FINZANJIR AI — so‘rovni tushunish va dalil sintezi

Sana: 2026-11-10  
Kod liniyasi: `v7-multilingual-evidence-fts4-2026-11-10`

## Amalga oshirilgan prototip yaxshilanishlari

1. **So‘rovni normallashtirish:** o‘zbek lotin/kirill yozuvlari bir xil qidiruv shakliga keltiriladi. Qoraqalpoq tilidagi ayrim kirill harflari (`ә, ң, ғ, қ, ө, ү, ұ, і, һ`) transliteratsiya qilinadi.
2. **Tilni taxminiy aniqlash:** o‘zbek, qoraqalpoq, qozoq va rus yozuviga oid belgilar/markerlar ajratiladi. Bu tilni mutlaq aniqlash emas; noaniq holatda qidiruv normallashtirilgan matn bo‘yicha davom etadi.
3. **Yozuv xatolariga chidamlilik:** ko‘p uchraydigan FINZANJIR atama xatolari uchun tuzatishlar va korpusdan quriladigan kichik token lug‘ati ishlatiladi. 1 belgigacha tahrir masofasi bilan cheklangan fuzzy moslik qo‘llanadi. Bu barcha imlo xatolarini tushunishni kafolatlamaydi.
4. **Ko‘p manbali qidiruv:** qat’iy AND qidiruvi va kengroq OR qidiruvi natijalari birlashtiriladi; takroriy IDlar bitta natijaga jamlanadi. Javobga eng mos oltitagacha dalil yozuvi kiritilishi mumkin.
5. **Manba izlari:** yozuv IDsi, manba identifikatori, versiya, bo‘lim, fayl yo‘li va approval maqomi javob manbalari ro‘yxatida saqlanadi.
6. **Ehtimoliy zidliklar:** bir-biriga yaqin matnlarda ijobiy va inkor mazmunli bayonlar turli manbalardan topilsa, ular ehtimoliy zidlik sifatida alohida ko‘rsatiladi. Bu avtomatik ekspert xulosasi emas; inson tekshirishi shart.
7. **Fuqaro rejimi:** umumiy auditoriyaga mo‘ljallangan materiallar, sodda izoh va Risk Engine, Fraud Graph, Case, Human Review hamda FIN-RECOVERY uchun qisqa atama izohlari.
8. **Mutaxassis rejimi:** texnik auditoriya yozuvlari ham qidiriladi; manba/versiya/maqom izlari ko‘rsatiladi. Rejim tanlovi autentifikatsiya yoki RBAC o‘rnini bosmaydi.

## Ishlash chegaralari

- Qidiruv SQLite FTS4 va yengil token lug‘atidan foydalanadi; BM25, embedding, vector database yoki majburiy LLM yuklab olish talab qilinmaydi.
- Bu generativ til modeli emas. U topilgan hujjat dalillarini saralab, ulardan qisqa javob tuzadi.
- Qarama-qarshilik aniqlash qoidaviy va konservativ prototipdir; u mazmuniy ziddiyatni har doim aniqlay olmaydi, ayrim o‘xshash jumlalarni esa noto‘g‘ri zid deb belgilashi mumkin.
- Qoraqalpoqcha lug‘at va morfologiya hali to‘liq qamrab olinmagan. Dialekt, apostrof, lotin/kirill aralashuvi va murakkab so‘z yasalishi bo‘yicha real foydalanuvchi sinovlari zarur.
- 5,607 yozuvli migratsiya nomzodi alohida aktivatsiya tekshiruvini talab qiladi. Ushbu kod yangilanishi o‘z-o‘zidan 5,607 yozuvli assetni GitHub Android aktiv assetiga ko‘chirmaydi.
- Hujjatdagi loyiha moduli yoki integratsiya ta’rifi uning amalda ishlab turganini anglatmaydi. Bank API ulanmagan. Risk signali aybdorlik isboti emas; AI yakuniy qaror bermaydi.

## Sinov uchun so‘rovlar

- `Risk Engin nima?`
- `fraud graf qanday isleydi?`
- `FINZAJIR da 16 qatlam neler?`
- `aqsha kartamnan joǵaldi, ne islew kerek?`
- `қарақалпақша: картадан ақшам жоғалды, не істеймен?`
- `Case qashan ashıladı?`
- `Mutaxassis rejimida L12 va manbalarini ko‘rsat`
- `Bank API hozir ulanganmi?`

Natija sifati Android qurilmasida, aynan aktiv korpus bilan sinovdan o‘tkazilishi kerak.
