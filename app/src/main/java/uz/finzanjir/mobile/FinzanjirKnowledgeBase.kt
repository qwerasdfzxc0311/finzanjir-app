package uz.finzanjir.mobile

/**
 * FINZANJIR knowledge layer — prototype implementation.
 *
 * This is a structured, source-aware knowledge mechanism, not a claim that
 * the complete V14 dossier or every AI corpus record has already been imported.
 * Each entry keeps its meaning, explanation, keywords, source and status.
 */
data class KnowledgeEntry(
    val id: String,
    val title: String,
    val shortMeaning: String,
    val explanation: String,
    val keywords: List<String>,
    val source: String,
    val status: String = "CONCEPT"
)

data class KnowledgeAnswer(
    val answer: String,
    val sources: List<String>,
    val confidence: String,
    val notice: String
)

object FinzanjirKnowledgeBase {
    const val VERSION = "prototype-kb-0.1"
    const val PRIMARY_SOURCE = "FINZANJIR V14 — loyiha konsepsiyasi (2026)"

    // The source labels are explicit. No entry is silently promoted to a
    // bank-approved rule, operational capability, or verified fact.
    val entries = listOf(
        KnowledgeEntry(
            "CORE-001", "FINZANJIR nima?",
            "Raqamli moliyaviy xavfsizlik platformasi konsepsiyasi.",
            "FINZANJIR fuqarolar, banklar va to‘lov infratuzilmasi uchun firibgarlik xavfini erta aniqlash, signal va dalillarni tartiblash, ogohlantirish hamda vakolatli inson tekshiruvini qo‘llab-quvvatlashga qaratilgan loyiha konsepsiyasidir. Hozirgi Android ilova — mutaxassislar ko‘rib chiqishi uchun prototip; u to‘liq bank platformasi yoki sinovdan o‘tgan ishlab chiqarish tizimi deb hisoblanmaydi.",
            listOf("finzanjir", "platforma", "loyiha", "konsepsiya", "maqsad", "nima"),
            PRIMARY_SOURCE
        ),
        KnowledgeEntry(
            "CORE-002", "FINZANJIR avtomatik bloklaydimi?",
            "Yo‘q. FINZANJIR avtomatik karta yoki tranzaksiya bloklash mexanizmi sifatida ta’riflanmaydi.",
            "Loyihaning asosiy yondashuvi — signal va kontekstni yig‘ish, xavfga oid dalillarni hamda qarshi dalillarni ko‘rsatish, noma’lum jihatlarni alohida qayd etish va zarur bo‘lsa Case ochish hamda Human Review jarayonini qo‘llab-quvvatlash. Yakuniy qaror vakolatli inson yoki tegishli tashkilot vakolatida qoladi. Ball yoki indikatorning o‘zi avtomatik aybdorlik yoki bloklash qarori bo‘la olmaydi.",
            listOf("bloklash", "avtomatik", "karta", "tranzaksiya", "90 ball", "human review"),
            "FINZANJIR loyiha qoidalari; V14 konsepsiyasi bilan uyg‘unlashtirilgan"
        ),
        KnowledgeEntry(
            "CORE-003", "Signal nima?",
            "Tekshirishga sabab bo‘lishi mumkin bo‘lgan kuzatuv yoki indikator.",
            "Signal — o‘z-o‘zidan firibgarlik isboti ham, shaxs aybdorligining hukmi ham emas. Signal qaysi manbadan olingani, qachon kuzatilgani, qanchalik ishonchli ekani, qaysi holatni tasdiqlashi yoki rad etishi mumkinligi bilan birga ko‘riladi. Yetishmayotgan ma’lumot va muqobil izohlar ham qayd etiladi.",
            listOf("signal", "indikator", "dalil", "kuzatuv", "shubha"),
            "FINZANJIR loyiha qoidalari"
        ),
        KnowledgeEntry(
            "CORE-004", "Case nima?",
            "Bir-biriga aloqador signallar, dalillar va tekshiruv holatlarini birlashtiruvchi ish yozuvi.",
            "Case — tekshiruv uchun kontekstni bir joyga jamlash vositasi. Unda hodisa, manba, vaqt, rozilik doirasi, tasdiqlovchi va rad etuvchi dalillar, noma’lum jihatlar, ko‘rilgan choralar va audit izi saqlanishi ko‘zda tutiladi. Case ochilishi firibgarlik tasdiqlandi degani emas.",
            listOf("case", "ish", "hodisa", "case ochish", "reyestr"),
            "FINZANJIR loyiha qoidalari"
        ),
        KnowledgeEntry(
            "CORE-005", "Human Review nima?",
            "Vakolatli inson tomonidan dalillar va kontekstni ko‘rib chiqish.",
            "Human Review jarayonida mutaxassis manba ishonchliligini, hodisalar ketma-ketligini, rozilik chegarasini, tasdiqlovchi va qarshi dalillarni hamda noma’lum jihatlarni tekshiradi. Natija tasdiqlash, rad etish, qo‘shimcha ma’lumot so‘rash yoki qayta tekshiruv bo‘lishi mumkin. AI yoki avtomatik qoida inson vakolatini egallamaydi.",
            listOf("human review", "inson", "ko‘rib chiqish", "mutaxassis", "qaror"),
            "FINZANJIR loyiha qoidalari"
        ),
        KnowledgeEntry(
            "CORE-006", "Rozilik doirasi nima?",
            "Foydalanuvchi aynan nimaga rozilik berganini alohida aniqlash.",
            "Qurilmadan foydalanishga ruxsat berish, hisobdan foydalanishga ruxsat berish va muayyan pul o‘tkazmasini tasdiqlash bir xil rozilik emas. Tekshiruvda rozilik qaysi obyektga, qaysi vaqtga va qaysi amal doirasiga tegishli ekani aniqlanishi kerak. Bir turdagi rozilik boshqasini avtomatik isbotlamaydi.",
            listOf("rozilik", "consent", "qurilma", "hisob", "o‘tkazma", "ruxsat"),
            "FINZANJIR loyiha qoidalari"
        ),
        KnowledgeEntry(
            "CORE-007", "Qarshi dalil va noma’lum holat",
            "Faqat shubhani kuchaytiruvchi belgilar emas, uni zaiflashtiruvchi ma’lumotlar ham tekshiriladi.",
            "Tizim tasdiqlovchi dalillar bilan birga rad etuvchi yoki muqobil izoh beruvchi dalillarni ham ko‘rsatishi kerak. Ma’lumot topilmagan bo‘lsa, uni avtomatik ravishda yolg‘on yoki firibgarlik deb belgilash mumkin emas. Bunday holat UNKNOWN yoki yetarli ma’lumot yo‘q deb qayd etiladi.",
            listOf("qarshi dalil", "unknown", "noma’lum", "rad etish", "noaniqlik", "false positive"),
            "FINZANJIR loyiha qoidalari"
        ),
        KnowledgeEntry(
            "CORE-008", "16 qatlam nimani anglatadi?",
            "Xavfsizlik, dalil, sifat, boshqaruv va tekshiruv talablarini qatlamlar bo‘yicha tartiblash modeli.",
            "16 qatlam — konsepsiyadagi funksional va boshqaruv yo‘nalishlarini bir-biridan ajratib ko‘rish uchun ishlatiladigan arxitektura modeli. Ilovada qatlam nomlari ko‘rsatilishi ularning barchasi to‘liq kodlangan, bankda ishlayotgan yoki mustaqil ekspertizadan o‘tganini anglatmaydi. Har bir qatlam uchun talab, ma’lumot manbasi, sinov, qabul mezoni va ochiq savollar alohida tekshirilishi kerak.",
            listOf("16 qatlam", "layer", "arxitektura", "qatlamlar", "talab"),
            PRIMARY_SOURCE
        ),
        KnowledgeEntry(
            "CORE-009", "Banklararo signal almashish",
            "Bir bank ko‘rmaydigan kontekstni qonuniy va xavfsiz tartibda bog‘lash maqsadi.",
            "Banklararo yondashuvning maqsadi — tegishli huquqiy asos, ma’lumotlarni minimallashtirish, rozilik va vakolatlar, xavfsiz integratsiya hamda audit talablariga rioya qilgan holda bir nechta manbadagi signallarni bog‘lash imkoniyatini o‘rganish. Hozirgi prototipda real bank API ulanishi mavjud deb da’vo qilinmaydi.",
            listOf("banklararo", "bank", "API", "integratsiya", "signal almashish"),
            PRIMARY_SOURCE
        ),
        KnowledgeEntry(
            "CORE-010", "FINZANJIR AI vazifasi",
            "Loyiha bilimlarini topish, izohlash va manbasini ko‘rsatishga yordam beruvchi yordamchi.",
            "AI foydalanuvchi savolini tushunib, ichki bilimlar bazasidan mos parchalarni qidirishi, ularning manbasi, versiyasi va maqomini ko‘rsatishi, keyin sodda va texnik izoh berishi kerak. Manbada javob bo‘lmasa, buni ochiq aytadi va taxminni fakt sifatida bermaydi. AI rasmiy bank, huquqiy yoki ekspert qarorini almashtirmaydi.",
            listOf("AI", "sun’iy ong", "bilimlar bazasi", "qidiruv", "manba", "uydirmaslik"),
            PRIMARY_SOURCE
        ),
        KnowledgeEntry(
            "CORE-011", "Prototipning hozirgi chegarasi",
            "Mutaxassislar fikri va keyingi ishlab chiqish uchun namoyish qilinadigan dastlabki model.",
            "Prototip konsepsiya va ish jarayonini ko‘rsatish uchun xizmat qiladi. Sintetik ma’lumotlar real bank ma’lumotlari emas. Bank API, production autentifikatsiya, to‘liq RBAC, real vaqt risk modeli, mustaqil audit va bank muhitidagi sinovlar mavjud deb ko‘rsatilmaydi. Bu cheklovlarni ochiq ko‘rsatish mutaxassis bahosi uchun muhim.",
            listOf("prototip", "MVP", "cheklov", "sinov", "real bank", "production"),
            "FINZANJIR loyiha qoidalari"
        ),
        KnowledgeEntry(
            "CORE-012", "Muallifning ijtimoiy maqsadi",
            "Moliyaviy xavfsizlik va savodxonlikni oshirishga hissa qo‘shish.",
            "V14 hujjatida loyiha motivatsiyasi faqat tijoriy mahsulot yaratish bilan cheklanmasligi, balki fuqarolarni moliyaviy firibgarlikdan oldinroq ogohlantirish, xavf sabablarini tushuntirish va moliyaviy xavfsizlik madaniyatini kuchaytirishga qaratilgani bayon etiladi. Hujjat 100 foiz himoya yoki daromad kafolatini va’da qilmaydi.",
            listOf("muallif", "motivatsiya", "ijtimoiy maqsad", "fuqaro", "moliyaviy savodxonlik"),
            PRIMARY_SOURCE
        )
    )

    fun search(question: String): KnowledgeAnswer {
        val q = normalize(question)
        if (q.isBlank()) return KnowledgeAnswer(
            "Savolingizni yozing. Masalan: “Case nima?” yoki “FINZANJIR avtomatik bloklaydimi?”",
            emptyList(), "NO_QUERY", "Bilimlar bazasi prototip holatida."
        )

        val ranked = entries.map { entry ->
            val haystack = normalize(entry.title + " " + entry.shortMeaning + " " + entry.explanation + " " + entry.keywords.joinToString(" "))
            val tokens = q.split(" ").filter { it.length >= 2 }.distinct()
            val score = tokens.count { token -> haystack.contains(token) } +
                if (haystack.contains(q)) 3 else 0
            entry to score
        }.filter { it.second > 0 }.sortedByDescending { it.second }.take(3)

        if (ranked.isEmpty()) return KnowledgeAnswer(
            "Mavjud FINZANJIR bilim yozuvlarida bu savolga yetarli asos topilmadi. Taxminni fakt sifatida aytmayman. Savolni boshqacha ifodalash yoki tegishli hujjat bo‘limini kiritish kerak.",
            emptyList(), "INSUFFICIENT_EVIDENCE",
            "Javob topilmagani firibgarlik yoki noto‘g‘ri holat borligini anglatmaydi."
        )

        val best = ranked.first().first
        val extra = ranked.drop(1).joinToString("\n\n") { it.first.title + ": " + it.first.shortMeaning }
        val answer = buildString {
            append(best.title).append("\n")
            append(best.shortMeaning).append("\n\n")
            append(best.explanation)
            if (extra.isNotBlank()) append("\n\nBog‘liq tushunchalar:\n").append(extra)
        }
        return KnowledgeAnswer(
            answer,
            ranked.map { it.first.id + " — " + it.first.source }.distinct(),
            if (ranked.first().second >= 3) "MATCHED" else "PARTIAL_MATCH",
            "Bu javob prototip bilim yozuvlariga asoslangan; rasmiy ekspert yoki bank qarori emas."
        )
    }

    private fun normalize(value: String): String = value.lowercase()
        .replace('ў', 'у').replace('қ', 'к').replace('ғ', 'г')
        .replace('ҳ', 'х').replace('ё', 'е')
        .replace(Regex("[^\\p{L}\\p{N}]+"), " ")
        .trim()
}
