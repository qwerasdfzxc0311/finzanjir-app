package uz.finzanjir.mobile

import android.content.Context
import org.json.JSONArray
import java.text.Normalizer
import java.util.Locale

data class KnowledgeAnswer(
    val answer: String,
    val sources: List<String>,
    val confidence: String,
    val notice: String
)

object FinzanjirKnowledgeBase {
    const val VERSION = "v4-corpus-0.4.1+v14"
    private const val ASSET = "finzanjir_knowledge.json"

    private data class Record(
        val id: String,
        val text: String,
        val approval: String,
        val sourceId: String,
        val sourceVersion: String,
        val sourceSection: String,
        val sourcePath: String,
        val recordType: String
    )

    @Volatile private var cached: List<Record>? = null

    fun count(context: Context): Int = load(context).size

    fun search(context: Context, question: String): KnowledgeAnswer {
        val q = normalize(question)
        if (q.isBlank()) return KnowledgeAnswer(
            "Savolingizni yozing. Masalan: “Case nima?”, “L13 nimani anglatadi?” yoki “FINZANJIR avtomatik bloklaydimi?”",
            emptyList(), "NO_QUERY",
            "Bilimlar bazasi prototip korpusi; barcha yozuvlar tasdiqlanmagan nomzod materialidir."
        )

        val queryTokens = tokens(q)
        if (queryTokens.isEmpty()) return insufficient()

        val records = load(context)
        val layerId = Regex("\\bL(0?[1-9]|1[0-6])\\b", RegexOption.IGNORE_CASE)
            .find(question)?.groupValues?.get(1)?.toIntOrNull()
        val layerRecords = records.filter { it.recordType == "layer_catalog_candidate" }

        val selected: List<Pair<Record, Int>> = if (layerId != null) {
            val id = "V4-L%02d".format(Locale.ROOT, layerId)
            val exact = layerRecords.filter { it.id.equals(id, true) }
            if (exact.isNotEmpty()) exact.map { it to 1000 } else emptyList()
        } else if (q.contains("16 qatlam") || q.contains("barcha qatlam") || q.contains("qatlamlar")) {
            layerRecords.sortedBy { it.id }.map { it to 100 }
        } else {
            val ranked = records.mapNotNull { record ->
                val body = normalize(record.text + " " + record.id + " " + record.recordType)
                val bodyTokens = tokens(body).toSet()
                val overlap = queryTokens.toSet().intersect(bodyTokens)
                if (overlap.isEmpty()) null else {
                    val coverage = overlap.size.toDouble() / queryTokens.toSet().size.coerceAtLeast(1)
                    val phraseBonus = if (body.contains(q)) 3 else 0
                    val idBonus = if (normalize(record.id).contains(q)) 8 else 0
                    record to (overlap.size * 2 + (coverage * 4).toInt() + phraseBonus + idBonus)
                }
            }.sortedByDescending { it.second }.take(5)
            ranked
        }

        if (selected.isEmpty()) return insufficient()
        val best = if (q.contains("16 qatlam") || q.contains("barcha qatlam") || q.contains("qatlamlar")) selected else selected.take(5)
        val answer = buildString {
            append(best.first().first.text)
            if (best.size > 1) {
                append("\n\nBog‘liq bilim yozuvlari:")
                best.drop(1).forEach { (record, _) ->
                    append("\n• ").append(record.id).append(" — ").append(record.text)
                }
            }
        }
        val sourceLines = best.map { (record, _) ->
            "${record.id} | ${record.sourceId} | ${record.sourceVersion} | ${record.sourceSection} | ${record.sourcePath} | ${record.approval}"
        }.distinct()

        val allCandidate = best.all { it.first.approval == "candidate_not_authoritative" }
        return KnowledgeAnswer(
            answer,
            sourceLines,
            if (best.first().second >= 5) "MOS YOZUV TOPILDI" else "QISMAN MOSLIK",
            if (allCandidate) {
                "Barcha topilgan yozuvlar candidate_not_authoritative: tasdiqlanmagan loyiha materiali. Qidiruv mosligi faktning to‘g‘riligini yoki ekspert tasdig‘ini anglatmaydi."
            } else {
                "Yozuv maqomini alohida tekshiring. Qidiruv mosligi faktning to‘g‘riligini anglatmaydi."
            }
        )
    }

    private fun insufficient() = KnowledgeAnswer(
        "Mavjud import qilingan bilim yozuvlarida bu savolga yetarli asos topilmadi. Taxminni fakt sifatida bermayman. Tegishli hujjat yoki bo‘lim import qilinishi kerak bo‘lishi mumkin.",
        emptyList(), "YETARLI DALIL TOPILMADI",
        "Topilmagan javob FINZANJIR konsepsiyasida bunday qoida yo‘q degani emas; korpus to‘liq emas."
    )

    private fun load(context: Context): List<Record> {
        cached?.let { return it }
        synchronized(this) {
            cached?.let { return it }
            val json = context.assets.open(ASSET).bufferedReader(Charsets.UTF_8).use { it.readText() }
            val array = JSONArray(json)
            val rows = ArrayList<Record>(array.length())
            for (i in 0 until array.length()) {
                val item = array.optJSONObject(i) ?: continue
                val id = item.optString("id").takeIf { it.isNotBlank() } ?: continue
                val text = item.optString("text").takeIf { it.isNotBlank() } ?: continue
                rows += Record(
                    id = id,
                    text = text,
                    approval = item.optString("approval", item.optString("record_status", "unknown")),
                    sourceId = item.optString("source_id", "unknown"),
                    sourceVersion = item.optString("source_version", "unknown"),
                    sourceSection = item.optString("source_section", "unknown"),
                    sourcePath = item.optString("source_path", "unknown"),
                    recordType = item.optString("record_type", "unknown")
                )
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
                "qatlamlar", "qatlamning", "qatlamga" -> "qatlam"
                "signallar", "signalni" -> "signal"
                "dalillar", "dalilni" -> "dalil"
                "bloklaydimi", "bloklamaydi", "bloklash" -> "blokla"
                "tranzaksiya", "tranzaksiyalar" -> "operatsiya"
                "ma'lumotlar", "malumotlar" -> "malumot"
                "firibgarlik", "firibgarligi" -> "firibgar"
                else -> token
            }
        }
        .filter { it.length >= 2 && it !in setOf("va", "yoki", "bu", "shu", "uchun", "bilan", "ham", "nima", "qanday", "qaysi", "haqida") }
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
                    '’', 'ʻ', '`' -> "'"
                    else -> c.toString()
                })
            }
        }
        return latin.replace(Regex("[^a-z0-9']+"), " ").trim().replace(Regex("\\s+"), " ")
    }
}
