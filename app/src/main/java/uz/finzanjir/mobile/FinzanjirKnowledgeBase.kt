package uz.finzanjir.mobile

import android.content.Context
import org.json.JSONArray
import java.text.Normalizer
import java.util.Locale
import kotlin.math.ln

data class KnowledgeAnswer(
    val answer: String,
    val sources: List<String>,
    val confidence: String,
    val notice: String
)

object FinzanjirKnowledgeBase {
    const val VERSION = "v5-retrieval-foundation-2026-11-09"
    private const val ASSET = "finzanjir_knowledge.json"

    private data class Record(
        val id: String,
        val text: String,
        val approval: String,
        val sourceId: String,
        val sourceVersion: String,
        val sourceSection: String,
        val sourcePath: String,
        val recordType: String,
        val audience: String,
        val domain: String
    )

    private data class IndexedRecord(
        val record: Record,
        val normalized: String,
        val normalizedText: String,
        val termCounts: Map<String, Int>
    )

    @Volatile private var cached: List<IndexedRecord>? = null

    fun count(context: Context): Int = load(context).size

    fun search(context: Context, question: String, expertMode: Boolean = false): KnowledgeAnswer {
        val normalizedQuestion = normalize(question)
        if (normalizedQuestion.isBlank()) {
            return KnowledgeAnswer(
                "Savolingizni yozing. Masalan: “L12 nima?”, “Bank integratsiyasi qanday ishlaydi?” yoki “AI javobni qanday tekshiradi?”",
                emptyList(), "NO_QUERY",
                "Bilimlar bazasida tasdiqlangan, nomzod va tarixiy manbalar maqomi alohida saqlanadi."
            )
        }

        val queryTokens = tokens(normalizedQuestion).distinct()
        if (queryTokens.isEmpty()) return insufficient()

        val all = load(context)
        val layerId = Regex("\\bL(0?[1-9]|1[0-6])\\b", RegexOption.IGNORE_CASE)
            .find(question)?.groupValues?.get(1)?.toIntOrNull()

        val isLayerOverview = listOf("16 qatlam", "barcha qatlam", "qatlamlar").any {
            normalizedQuestion.contains(normalize(it))
        }
        val isAuthorQuestion = listOf("muallif", "salamat", "smaylov", "tangrbergen", "asoschi")
            .any { normalizedQuestion.contains(normalize(it)) }

        // Index-only va alias yozuvlari javob dalili sifatida ishlatilmaydi.
        // Ular manba korpusida saqlanadi; asl yozuvlar o‘chirilmaydi.
        val eligible = all.filter { indexed ->
            val r = indexed.record
            val type = r.recordType.lowercase(Locale.ROOT)
            r.approval != "index_only" &&
                !type.contains("alias") &&
                !type.contains("query_pattern") &&
                (expertMode || r.audience == "general" || r.audience == "general_and_expert") &&
                (!isAuthorRecord(r) || isAuthorQuestion || expertMode)
        }

        val selected: List<Pair<IndexedRecord, Double>> = when {
            layerId != null -> {
                val id = "V4-L%02d".format(Locale.ROOT, layerId)
                eligible.filter { it.record.id.equals(id, true) }.map { it to 1000.0 }
            }
            isLayerOverview -> {
                eligible.filter { it.record.recordType == "layer_catalog_candidate" }
                    .sortedBy { it.record.id }
                    .map { it to 100.0 }
            }
            else -> rank(eligible, queryTokens, normalizedQuestion)
                // Bir xil matnli yozuvlar korpusda qoladi, lekin javobda takrorlanmaydi.
                .distinctBy { it.first.normalizedText }
                .take(5)
        }

        if (selected.isEmpty()) return insufficient()

        val answerRecords = if (isLayerOverview) selected else selected.take(5)
        val answer = buildString {
            answerRecords.forEachIndexed { index, pair ->
                if (index > 0) append("\n\nBog‘liq bilim yozuvi:\n")
                append(pair.first.record.text)
            }
        }

        // Takror matn bir marta ko‘rsatiladi, ammo unga tegishli barcha source izlari saqlanadi.
        val sourceLines = answerRecords.flatMap { (indexed, _) ->
            eligible.filter { it.normalizedText == indexed.normalizedText }.map { match ->
                val r = match.record
                r.id + " | " + r.sourceId + " | " + r.sourceVersion + " | " +
                    r.sourceSection + " | " + r.sourcePath + " | " + r.approval
            }
        }.distinct()

        val approvals = answerRecords.map { it.first.record.approval }.distinct()
        val notice = when {
            approvals.all { it == "candidate_not_authoritative" || it == "candidate" || it == "not_auto_promoted" } ->
                "Topilgan materiallar loyiha manbasi yoki tasdiqlanmagan nomzod yozuvlardir. Ular ekspert tasdig‘i yoki amaldagi tizimda joriy etilganini o‘z-o‘zidan isbotlamaydi."
            approvals.any { it == "unclassified" || it == "unknown" } ->
                "Natijada maqomi to‘liq aniqlanmagan yozuvlar bor. Manba, versiya va tasdiqlash holatini alohida tekshirish kerak."
            else ->
                "Qidiruv mosligi faktning to‘g‘riligini, amaldagi qonuniy kuchini yoki prototipda funksiya ishlayotganini isbotlamaydi."
        }

        return KnowledgeAnswer(
            answer,
            sourceLines,
            if (answerRecords.first().second >= 5.0) "MOS YOZUV TOPILDI" else "QISMAN MOSLIK",
            notice
        )
    }

    private fun isAuthorRecord(r: Record): Boolean {
        val t = r.recordType.lowercase(Locale.ROOT)
        return t.contains("author") || t.contains("founder") ||
            r.approval == "author_visible_on_direct_request"
    }

    private fun rank(
        records: List<IndexedRecord>,
        queryTokens: List<String>,
        normalizedQuestion: String
    ): List<Pair<IndexedRecord, Double>> {
        if (records.isEmpty()) return emptyList()
        val querySet = queryTokens.toSet()
        val documentFrequency = HashMap<String, Int>()
        records.forEach { indexed ->
            querySet.forEach { token ->
                if ((indexed.termCounts[token] ?: 0) > 0) {
                    documentFrequency[token] = (documentFrequency[token] ?: 0) + 1
                }
            }
        }

        val n = records.size.toDouble()
        return records.mapNotNull { indexed ->
            var score = 0.0
            var matched = 0
            querySet.forEach { token ->
                val tf = indexed.termCounts[token] ?: 0
                if (tf > 0) {
                    matched++
                    val df = (documentFrequency[token] ?: 0).toDouble()
                    val idf = ln(1.0 + (n - df + 0.5) / (df + 0.5))
                    val saturatedTf = (tf * 2.2) / (tf + 1.2)
                    score += idf * saturatedTf
                }
            }
            if (matched == 0) return@mapNotNull null

            val coverage = matched.toDouble() / querySet.size.coerceAtLeast(1)
            if (indexed.normalized.contains(normalizedQuestion)) score += 5.0
            if (normalize(indexed.record.sourceSection).contains(normalizedQuestion)) score += 2.5
            if (indexed.record.domain == "finzanjir") score += 0.6
            score += coverage * 2.0
            indexed to score
        }.sortedByDescending { it.second }
    }

    private fun insufficient() = KnowledgeAnswer(
        "Import qilingan bilimlarda bu savolga yetarli asos topilmadi. Taxminni fakt sifatida bermayman. Tegishli hujjat yoki bo‘limni tekshirish kerak bo‘lishi mumkin.",
        emptyList(), "YETARLI DALIL TOPILMADI",
        "Topilmagan javob FINZANJIR konsepsiyasida bunday qoida yo‘q degani emas; qidiruv indeksi to‘liq bo‘lmasligi yoki savol boshqacha ifodalangan bo‘lishi mumkin."
    )

    private fun load(context: Context): List<IndexedRecord> {
        cached?.let { return it }
        synchronized(this) {
            cached?.let { return it }
            val json = context.assets.open(ASSET).bufferedReader(Charsets.UTF_8).use { it.readText() }
            val array = JSONArray(json)
            val rows = ArrayList<IndexedRecord>(array.length())
            for (i in 0 until array.length()) {
                val item = array.optJSONObject(i) ?: continue
                val id = item.optString("id").takeIf { it.isNotBlank() } ?: continue
                val text = item.optString("text").takeIf { it.isNotBlank() } ?: continue
                val record = Record(
                    id = id,
                    text = text,
                    approval = item.optString("approval", item.optString("record_status", "unknown")),
                    sourceId = item.optString("source_id", item.optString("source", "unknown")),
                    sourceVersion = item.optString("source_version", "unknown"),
                    sourceSection = item.optString("source_section", item.optString("section", "unknown")),
                    sourcePath = item.optString("source_path", item.optString("source", "unknown")),
                    recordType = item.optString("record_type", item.optString("kind", "unknown")),
                    audience = item.optString("audience", "general"),
                    domain = item.optString("domain", "unclassified")
                )
                val normalizedText = normalize(text)
                val searchable = normalize(text + " " + id + " " + record.sourceSection + " " + record.recordType)
                val counts = tokens(searchable).groupingBy { it }.eachCount()
                rows += IndexedRecord(record, searchable, normalizedText, counts)
            }
            if (rows.isEmpty()) throw IllegalStateException("FINZANJIR bilimlar bazasida yaroqli yozuv topilmadi.")
            cached = rows
            return rows
        }
    }

    private fun tokens(value: String): List<String> = normalize(value)
        .split(Regex("\\s+"))
        .map { token ->
            when (token) {
                "qatlamlar", "qatlamning", "qatlamga", "qatlamni" -> "qatlam"
                "signallar", "signalni", "signali" -> "signal"
                "dalillar", "dalilni", "dalili" -> "dalil"
                "bloklaydimi", "bloklamaydi", "bloklash", "bloklandi" -> "blokla"
                "tranzaksiya", "tranzaksiyalar", "tranzaksiyani" -> "operatsiya"
                "ma'lumotlar", "malumotlar", "ma'lumotni" -> "malumot"
                "firibgarlik", "firibgarligi", "firibgarlikka" -> "firibgar"
                "integratsiyasi", "integratsiyaga", "integratsiyani" -> "integratsiya"
                "mutaxassislar", "mutaxassisni" -> "mutaxassis"
                else -> token
            }
        }
        .filter {
            it.length >= 2 && it !in setOf(
                "va", "yoki", "bu", "shu", "uchun", "bilan", "ham", "nima",
                "qanday", "qaysi", "haqida", "bor", "deb", "esa", "men"
            )
        }
        .distinct()

    private fun normalize(value: String): String {
        val lower = Normalizer.normalize(value.lowercase(Locale.ROOT), Normalizer.Form.NFKC)
        val latin = buildString {
            lower.forEach { c ->
                append(when (c) {
                    'а' -> "a"; 'б' -> "b"; 'в' -> "v"; 'г' -> "g"; 'д' -> "d"; 'е' -> "e"; 'ё' -> "yo"
                    'ж' -> "j"; 'з' -> "z"; 'и' -> "i"; 'й' -> "y"; 'к' -> "k"; 'л' -> "l"; 'м' -> "m"
                    'н' -> "n"; 'о' -> "o"; 'п' -> "p"; 'р' -> "r"; 'с' -> "s"; 'т' -> "t"; 'у' -> "u"
                    'ф' -> "f"; 'х' -> "x"; 'ц' -> "ts"; 'ч' -> "ch"; 'ш' -> "sh"; 'щ' -> "sh"
                    'ъ', 'ь' -> ""; 'ы' -> "i"; 'э' -> "e"; 'ю' -> "yu"; 'я' -> "ya"
                    'ў' -> "o"; 'қ' -> "q"; 'ғ' -> "g"; 'ҳ' -> "h"
                    '’', 'ʻ', '\u0060', 'ʼ' -> "'"
                    else -> c.toString()
                })
            }
        }
        return latin.replace(Regex("[^a-z0-9']+"), " ").trim().replace(Regex("\\s+"), " ")
    }
}
