# FTS4 provenance-preserving schema v4

Sana: 2026-11-10
Branch: `integrated-workflow-foundation-2026-11-10`

## Ushbu bosqichda bajarilgan ish

- SQLite knowledge DB schema versiyasi 3 dan 4 ga ko'tarildi.
- `knowledge_meta` jadvaliga `legacy_versions_json` va `legacy_provenance_json` maydonlari qo'shildi.
- JSON streaming importer endi `legacy_versions` va `legacy_provenance` ichidagi ichma-ich obyekt/array qiymatlarini o'qiydi.
- Javob manbalari ro'yxatida canonical manba bilan birga tarixiy versiya va oldingi provenance izlari ham ko'rsatiladi.
- `search_aliases` FTS4 qidiruv matniga qo'shilishda davom etadi; tarixiy matn canonical yozuv o'rniga javob sifatida chiqarilmaydi.
- DB schema upgrade endi jadvallarni DROP qilmaydi. Yetishmayotgan ustunlar additive migration bilan qo'shiladi.
- SQLite FTS4 saqlanadi. BM25, embedding, vector DB yoki majburiy model qo'shilmagan.

## Ma'lumot xavfsizligi

Schema upgrade mavjud lokal indeksni va uning yozuvlarini saqlaydi. Asset SHA o'zgarganida korpusni qayta import qilish alohida transaction ichida bajariladi; import xatosi transaction rollback orqali oldingi indeksni saqlab qolishi kerak.

Bir xil ID va bir xil matn bitta canonical yozuv bo'lib qoladi. Bir xil ID, ammo matni farqli holatda yangi canonical matn, eski matn esa `legacy_versions` va qidiruv aliasi sifatida saqlanadi. Har ikkala holatda ham manba izlari yo'qotilmaydi.

## Hozircha bajarilmagan va bloklangan ishlar

- 6,679 yozuvli birlashtirilgan candidate GitHub'da 12 ta JSON bo'lagida saqlandi: `source-import/candidates/finzanjir_knowledge_merged_6679_part_01.json` ... `part_12.json`.
- Candidate manifest: `source-import/candidates/finzanjir_knowledge_merged_6679_manifest.json`; birlashtirilgan JSON SHA-256: `301a1889ef4245eb72a4c68b7e678d842e5e5bf1a68c1507066e4801bc0051af`.
- Bo'laklar APK asset papkasidan tashqarida. Aktiv Android asset hanuz 1,121 yozuv; manifest va APK asset yo'li almashtirilmagan. 6,679 yozuv hali aktiv korpus deb e'lon qilinmaydi.
- Manifest faqat birlashtirilgan fayl va uning SHA/count tekshiruvi tayyor bo'lgandan keyin yangilanadi.
- Android Gradle build, FTS4 import/search regression va jismoniy Samsung qurilmasidagi runtime tekshiruvlar hali alohida dalil talab qiladi.

## Keyingi xavfsiz qadam

1. 5,607 candidate JSONni aniq manbadan olish va SHA-256 ni auditdagi qiymat bilan tekshirish.
2. Mavjud 1,121 aktiv JSON bilan merge skriptini ishlatib, 6,679 unique ID invariantini tasdiqlash.
3. 18 tarixiy matn va barcha provenance maydonlari saqlanganini tekshirish.
4. Faqat shundan keyin merged JSON va manifestni yangi candidate asset sifatida commit qilish.
5. APK build, import count/SHA, FTS4 savol to'plami va telefon sinovlaridan keyin aktivlashtirish haqida qaror qilish.

Bu hujjat schema tayyorgarligini qayd etadi; 6,679 yozuvli korpus aktivlashtirilganini yoki Samsung qurilmada sinovdan o'tganini anglatmaydi.


## 2026-11-10 candidate birlashtirish natijasi

6,679 yozuvli candidate alohida source-import bo'laklari sifatida saqlandi. SQLite FTS4 sinovi uchun `tools/validate_merged_knowledge_fts4.py` qo'shildi. U manifestdagi tartibda bo'laklarni yig'adi, SHA/count/ID invariantlarini tekshiradi, tarixiy versiyalar va provenance sonini tekshiradi hamda SQLite FTS4 virtual jadvalida Risk Engine, Cross-Match, Fraud Graph, Timeline, FIN-RECOVERY, Human Review, fuqaro kartalari va OTP/CVV so'rovlarini sinaydi.

Bu CI darajasidagi SQLite FTS4 tekshiruvi; Android qurilmasidagi SQLite/Compose runtime testi emas.
