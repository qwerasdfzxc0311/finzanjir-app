package uz.finzanjir.mobile

import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import android.util.JsonReader
import android.util.JsonToken
import org.json.JSONObject
import java.io.File
import java.io.FileInputStream
import java.io.InputStreamReader
import java.security.MessageDigest
import java.text.Normalizer
import java.util.Locale

data class KnowledgeAnswer(
    val answer: String,
    val sources: List<String>,
    val confidence: String,
    val notice: String,
    val recordCount: Int
)

/**
 * Lightweight FINZANJIR knowledge core.
 * No BM25, embeddings, vector database, model download or full-corpus RAM index.
 * A one-time streaming import builds a local SQLite FTS4 index. Each question
 * reads a small candidate set, then composes an evidence-grounded answer.
 */
object FinzanjirKnowledgeBase {
    const val VERSION = "v6-lightweight-fts4-core-2026-11-10"
    private const val ASSET = "finzanjir_knowledge.json"
    private const val MANIFEST = "knowledge_manifest.json"
    private const val DB_NAME = "finzanjir_knowledge_v6.db"
    private const val DB_VERSION = 1
    private const val MAX_CANDIDATES = 48
    private const val MAX_ANSWER_RECORDS = 4

    private data class Record(
        val rowId: Long,
        val id: String,
        val text: String,
        val approval: String,
        val sourceId: String,
        val sourceVersion: String,
        val sourceSection: String,
        val sourcePath: String,
        val recordType: String,
        val audience: String,
        val domain: String,
        val language: String
    )
    private data class Candidate(val record: Record, val score: Int)

    private class DbHelper(context: Context) :
        SQLiteOpenHelper(context.applicationContext, DB_NAME, null, DB_VERSION) {
        override fun onCreate(db: SQLiteDatabase) {
            db.execSQL("""CREATE TABLE knowledge_meta(
                _id INTEGER PRIMARY KEY, id TEXT NOT NULL UNIQUE, body TEXT NOT NULL, approval TEXT NOT NULL,
                source_id TEXT NOT NULL, source_version TEXT NOT NULL, source_section TEXT NOT NULL,
                source_path TEXT NOT NULL, record_type TEXT NOT NULL, audience TEXT NOT NULL,
                domain TEXT NOT NULL, language TEXT NOT NULL
            )""")
            db.execSQL("CREATE VIRTUAL TABLE knowledge_fts USING fts4(search_text, tokenize=unicode61)")
            db.execSQL("CREATE TABLE knowledge_state(key TEXT PRIMARY KEY, value TEXT NOT NULL)")
            db.execSQL("CREATE INDEX knowledge_meta_type ON knowledge_meta(record_type)")
            db.execSQL("CREATE INDEX knowledge_meta_approval ON knowledge_meta(approval)")
        }
        override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
            db.execSQL("DROP TABLE IF EXISTS knowledge_fts")
            db.execSQL("DROP TABLE IF EXISTS knowledge_meta")
            db.execSQL("DROP TABLE IF EXISTS knowledge_state")
            onCreate(db)
        }
    }

    @Volatile private var helper: DbHelper? = null
    @Volatile private var preparedAssetSha: String? = null
    @Synchronized private fun db(context: Context): SQLiteDatabase {
        if (helper == null) helper = DbHelper(context.applicationContext)
        return helper!!.writableDatabase
    }

    fun count(context: Context): Int {
        ensureReady(context)
        return db(context).rawQuery("SELECT COUNT(*) FROM knowledge_meta", null).use { c ->
            if (c.moveToFirst()) c.getInt(0) else 0
        }
    }

    fun search(context: Context, question: String, expertMode: Boolean = false): KnowledgeAnswer {
        val q = normalize(question)
        if (q.isBlank()) return KnowledgeAnswer(
            "Savolingizni yozing. Masalan: “Risk Engine nima?”, “L12 nima?” yoki “Fraud Graph qanday ishlashi ko‘zda tutilgan?”",
            emptyList(), "NO_QUERY", "Javoblar manba va hujjat maqomi bilan ko‘rsatiladi.", count(context)
        )
        ensureReady(context)
        val database = db(context)
        val authorQuestion = listOf("muallif", "salamat", "smaylov", "tangrbergen", "asoschi", "author", "founder")
            .any { q.contains(normalize(it)) }
        val layerNumber = Regex("\\bL(0?[1-9]|1[0-6])\\b", RegexOption.IGNORE_CASE)
            .find(question)?.groupValues?.get(1)?.toIntOrNull()
        val layerOverview = listOf("16 qatlam", "barcha qatlam", "qatlamlar").any { q.contains(normalize(it)) }

        val rows = when {
            layerNumber != null -> exactLayer(database, layerNumber)
            layerOverview -> allLayers(database)
            authorQuestion -> authorRecords(database)
            else -> retrieve(database, question, expertMode, authorQuestion)
        }.filter { r ->
            val type = r.recordType.lowercase(Locale.ROOT)
            r.approval != "index_only" && !type.contains("alias") && !type.contains("query_pattern") &&
                (expertMode || r.audience == "general" || r.audience == "general_and_expert") &&
                (authorQuestion || !isAuthorRecord(r))
        }
        if (rows.isEmpty()) return insufficient(count(context))

        val selected = if (layerNumber != null || layerOverview || authorQuestion) {
            rows.map { Candidate(it, 100) }
        } else {
            scoreCandidates(question, rows).distinctBy { normalize(it.record.text) }.take(MAX_ANSWER_RECORDS)
        }
        if (selected.isEmpty()) return insufficient(count(context))

        val baseAnswer = composeAnswer(question, selected, layerOverview)
        val answer = if (Regex("\\brecal\\b", RegexOption.IGNORE_CASE).containsMatchIn(question))
            "Yuklangan manbalarda “ReCAL” nomli alohida modul yoki qisqartma mustaqil ta’riflanmagan. Quyidagi dalillar faqat risk modelini qayta kalibrlash (recalibration) mavzusiga yaqin; uni FIN-RECOVERY bilan tenglashtirmayman.\\n\\n" + baseAnswer
        else baseAnswer
        val sources = selected.map { c ->
            val r = c.record
            r.id + " | " + r.sourceId + " | " + r.sourceVersion + " | " +
                r.sourceSection + " | " + r.sourcePath + " | " + r.approval
        }.distinct()
        val approvals = selected.map { it.record.approval }.distinct()
        val statusNotice = when {
            approvals.all { it in setOf("candidate_not_authoritative", "candidate", "not_auto_promoted") } ->
                "Topilgan manbalar loyiha konsepsiyasi yoki tasdiqlanmagan nomzod materiallaridir."
            approvals.any { it in setOf("unclassified", "unknown") } ->
                "Ayrim yozuvlarning maqomi to‘liq aniqlanmagan; manba va versiyani alohida tekshirish kerak."
            else ->
                "Qidiruv mosligi mustaqil tasdiq emas."
        }
        val visualNotice = if (selected.any { it.record.recordType == "visual_ocr_candidate" })
            " OCR yozuvlari vizual ekspert tekshiruvini kutadi." else ""
        val notice = statusNotice + visualNotice +
            " FINZANJIR konsepsiyasi va prototipi ishlab chiqilmoqda: matndagi modul yoki integratsiya tavsifi uning hozir amalda ishlayotganini anglatmaydi. Mutaxassislar bilan tekshirish va vakolatli inson nazorati ko‘zda tutiladi. Risk signali aybdorlik isboti emas."
        return KnowledgeAnswer(
            answer, sources,
            if (selected.first().score >= 6) "MOS BILIM TOPILDI" else "QISMAN MOSLIK",
            notice, count(context)
        )
    }

    private fun ensureReady(context: Context) {
        if (preparedAssetSha != null) return
        val database = db(context)
        val manifest = JSONObject(context.assets.open(MANIFEST).bufferedReader(Charsets.UTF_8).use { it.readText() })
        val expectedCount = manifest.optInt("record_count", -1)
        val expectedSha = manifest.optString("asset_sha256", manifest.optString("sha256", ""))
        val staged = File(context.cacheDir, "finzanjir_knowledge_import.json")
        val digest = MessageDigest.getInstance("SHA-256")
        context.assets.open(ASSET).use { input ->
            staged.outputStream().use { output ->
                val buffer = ByteArray(32768)
                while (true) {
                    val n = input.read(buffer)
                    if (n < 0) break
                    digest.update(buffer, 0, n)
                    output.write(buffer, 0, n)
                }
            }
        }
        val actualSha = digest.digest().joinToString("") { "%02x".format(it) }
        if (expectedSha.isNotBlank() && !actualSha.equals(expectedSha, true)) {
            staged.delete()
            throw IllegalStateException("Bilim asset SHA-256 manifestga mos emas. Import to‘xtatildi.")
        }
        val oldSha = database.rawQuery("SELECT value FROM knowledge_state WHERE key='corpus_sha256'", null).use {
            if (it.moveToFirst()) it.getString(0) else ""
        }
        val oldCount = database.rawQuery("SELECT COUNT(*) FROM knowledge_meta", null).use {
            if (it.moveToFirst()) it.getInt(0) else 0
        }
        if (oldSha == actualSha && oldCount > 0 && (expectedCount <= 0 || oldCount == expectedCount)) {
            staged.delete()
            preparedAssetSha = actualSha
            return
        }

        database.beginTransaction()
        try {
            database.delete("knowledge_fts", null, null)
            database.delete("knowledge_meta", null, null)
            database.delete("knowledge_state", null, null)
            val metaInsert = database.compileStatement(
                """INSERT INTO knowledge_meta(id,body,approval,source_id,source_version,source_section,
                source_path,record_type,audience,domain,language) VALUES(?,?,?,?,?,?,?,?,?,?,?)"""
            )
            val ftsInsert = database.compileStatement(
                "INSERT INTO knowledge_fts(docid,search_text) VALUES(?,?)"
            )
            var imported = 0
            JsonReader(InputStreamReader(FileInputStream(staged), Charsets.UTF_8)).use { reader ->
                reader.beginArray()
                while (reader.hasNext()) {
                    val r = readRecord(reader)
                    if (r.id.isBlank() || r.text.isBlank()) continue
                    metaInsert.clearBindings()
                    listOf(r.id,r.text,r.approval,r.sourceId,r.sourceVersion,r.sourceSection,r.sourcePath,
                        r.recordType,r.audience,r.domain,r.language).forEachIndexed { i, value ->
                        metaInsert.bindString(i + 1, value)
                    }
                    val rowId = metaInsert.executeInsert()
                    ftsInsert.clearBindings()
                    ftsInsert.bindLong(1, rowId)
                    ftsInsert.bindString(2, normalize(r.text + " " + r.id + " " + r.sourceSection + " " + r.recordType + " " + r.domain))
                    ftsInsert.executeInsert()
                    imported++
                }
                reader.endArray()
            }
            if (expectedCount > 0 && imported != expectedCount) {
                throw IllegalStateException("Bilim yozuvlari soni mos emas: " + imported + " / " + expectedCount)
            }
            database.execSQL("INSERT INTO knowledge_state(key,value) VALUES('corpus_sha256',?)", arrayOf(actualSha))
            database.execSQL("INSERT INTO knowledge_state(key,value) VALUES('record_count',?)", arrayOf(imported.toString()))
            database.setTransactionSuccessful()
            preparedAssetSha = actualSha
        } finally {
            database.endTransaction()
            staged.delete()
        }
    }

    private data class RawRecord(
        var id: String = "", var text: String = "", var approval: String = "unknown",
        var sourceId: String = "unknown", var sourceVersion: String = "unknown",
        var sourceSection: String = "unknown", var sourcePath: String = "unknown",
        var recordType: String = "unknown", var audience: String = "general",
        var domain: String = "unclassified", var language: String = "und"
    )

    private fun readRecord(reader: JsonReader): RawRecord {
        val r = RawRecord()
        reader.beginObject()
        while (reader.hasNext()) {
            when (reader.nextName()) {
                "id" -> r.id = readScalar(reader)
                "text" -> r.text = readScalar(reader)
                "approval" -> r.approval = readScalar(reader)
                "source_id", "source" -> r.sourceId = readScalar(reader)
                "source_version" -> r.sourceVersion = readScalar(reader)
                "source_section", "section" -> r.sourceSection = readScalar(reader)
                "source_path" -> r.sourcePath = readScalar(reader)
                "record_type", "kind" -> r.recordType = readScalar(reader)
                "audience" -> r.audience = readScalar(reader)
                "domain" -> r.domain = readScalar(reader)
                "source_language", "language" -> r.language = readScalar(reader)
                else -> reader.skipValue()
            }
        }
        reader.endObject()
        return r
    }

    private fun readScalar(reader: JsonReader): String = when (reader.peek()) {
        JsonToken.STRING, JsonToken.NUMBER -> reader.nextString()
        JsonToken.BOOLEAN -> reader.nextBoolean().toString()
        JsonToken.NULL -> { reader.nextNull(); "" }
        else -> { reader.skipValue(); "" }
    }

    private fun exactLayer(database: SQLiteDatabase, layer: Int): List<Record> {
        val id = "V4-L%02d".format(Locale.ROOT, layer)
        return queryMeta(database, "SELECT m.* FROM knowledge_meta m WHERE m.id=?", arrayOf(id))
    }

    private fun allLayers(database: SQLiteDatabase): List<Record> =
        queryMeta(database,
            "SELECT m.* FROM knowledge_meta m WHERE m.record_type LIKE '%layer%' OR m.id LIKE 'V4-L%' ORDER BY m.id",
            emptyArray())

    private fun authorRecords(database: SQLiteDatabase): List<Record> =
        queryMeta(database,
            """SELECT m.* FROM knowledge_meta m
               WHERE m.record_type IN ('author_biography','founder_multilingual_bio')
                  OR m.approval='author_visible_on_direct_request'
               ORDER BY CASE WHEN m.approval='author_visible_on_direct_request' THEN 0 ELSE 1 END,
                        m.id LIMIT 8""",
            emptyArray())

    private fun retrieve(database: SQLiteDatabase, question: String, expertMode: Boolean, authorQuestion: Boolean): List<Record> {
        val terms = queryTerms(question).take(8)
        if (terms.isEmpty()) return emptyList()
        val expressions = listOf(
            terms.joinToString(" AND ") { "\"" + it + "\"" },
            terms.joinToString(" OR ") { "\"" + it + "\"" }
        )
        for (expression in expressions) {
            val found = queryMeta(database,
                """SELECT m.* FROM knowledge_fts f
                   JOIN knowledge_meta m ON m._id=f.docid
                   WHERE knowledge_fts MATCH ? LIMIT $MAX_CANDIDATES""",
                arrayOf(expression)).filter { r ->
                val type = r.recordType.lowercase(Locale.ROOT)
                r.approval != "index_only" && !type.contains("alias") && !type.contains("query_pattern") &&
                    (expertMode || r.audience == "general" || r.audience == "general_and_expert") &&
                    (authorQuestion || !isAuthorRecord(r))
            }
            if (found.isNotEmpty()) return found
        }
        return emptyList()
    }

    private fun queryMeta(database: SQLiteDatabase, sql: String, args: Array<String>): List<Record> {
        val rows = ArrayList<Record>()
        database.rawQuery(sql, args).use { c ->
            while (c.moveToNext()) {
                rows += Record(
                    rowId = c.getLong(c.getColumnIndexOrThrow("_id")),
                    id = c.getString(c.getColumnIndexOrThrow("id")),
                    text = c.getString(c.getColumnIndexOrThrow("body")),
                    approval = c.getString(c.getColumnIndexOrThrow("approval")),
                    sourceId = c.getString(c.getColumnIndexOrThrow("source_id")),
                    sourceVersion = c.getString(c.getColumnIndexOrThrow("source_version")),
                    sourceSection = c.getString(c.getColumnIndexOrThrow("source_section")),
                    sourcePath = c.getString(c.getColumnIndexOrThrow("source_path")),
                    recordType = c.getString(c.getColumnIndexOrThrow("record_type")),
                    audience = c.getString(c.getColumnIndexOrThrow("audience")),
                    domain = c.getString(c.getColumnIndexOrThrow("domain")),
                    language = c.getString(c.getColumnIndexOrThrow("language"))
                )
            }
        }
        return rows
    }

    private fun scoreCandidates(question: String, rows: List<Record>): List<Candidate> {
        val terms = queryTerms(question).toSet()
        val phrase = normalize(question)
        return rows.mapNotNull { r ->
            val body = normalize(r.text)
            val hits = terms.count { body.contains(it) }
            if (hits == 0) return@mapNotNull null
            val score = (hits * 4 / terms.size.coerceAtLeast(1)) +
                (if (phrase.length > 4 && body.contains(phrase)) 5 else 0) +
                (if (r.domain == "finzanjir") 2 else 0)
            Candidate(r, score)
        }.sortedByDescending { it.score }
    }

    private fun composeAnswer(question: String, rows: List<Candidate>, layerOverview: Boolean): String {
        if (layerOverview) return rows.joinToString("\n\n") { it.record.text.take(900) }
        val terms = queryTerms(question).toSet()
        return rows.mapIndexed { index, candidate ->
            val r = candidate.record
            val sentences = r.text.split(Regex("(?<=[.!?])\\s+|\\n+"))
                .map { it.trim() }.filter { it.length > 30 }
            val chosen = sentences.map { s -> s to terms.count { normalize(s).contains(it) } }
                .filter { it.second > 0 }.sortedByDescending { it.second }
                .take(if (index == 0) 3 else 2).map { it.first }
            val body = if (chosen.isNotEmpty()) chosen.joinToString(" ") else r.text.take(900)
            (if (index == 0) "" else "\n\nBog‘liq manba: ") + body
        }.joinToString("").take(5200)
    }

    private fun isAuthorRecord(r: Record): Boolean {
        val t = r.recordType.lowercase(Locale.ROOT)
        return t.contains("author") || t.contains("founder") ||
            r.approval == "author_visible_on_direct_request"
    }

    private fun queryTerms(value: String): List<String> {
        val stop = setOf("va","yoki","bu","shu","uchun","bilan","ham","nima","qanday","qaysi","haqida","bor","deb","esa","men",
            "the","what","how","does","is","are","and","with","for","about","who","why","это","как","что","для","кто")
        val base = normalize(value).split(Regex("\\s+")).map { token ->
            when (token) {
                "qatlamlar","qatlamning","qatlamga","qatlamni" -> "qatlam"
                "signallar","signalni","signali" -> "signal"
                "dalillar","dalilni","dalili" -> "dalil"
                "tranzaksiya","tranzaksiyalar","tranzaksiyani" -> "operatsiya"
                "firibgarlik","firibgarligi","firibgarlikka" -> "firibgar"
                "integratsiyasi","integratsiyaga","integratsiyani" -> "integratsiya"
                "mutaxassislar","mutaxassisni" -> "mutaxassis"
                else -> token
            }
        }.filter { it.length >= 2 && it !in stop }
        val aliases = mapOf(
            "riskengine" to listOf("risk","engine"), "risk" to listOf("risk","xavf"),
            "fraudgraph" to listOf("fraud","graph","firibgar","graf"),
            "fraud" to listOf("fraud","firibgar"), "graph" to listOf("graph","graf","boglanish"),
            "recal" to listOf("recalibration","kalibratsiya","kalibrlash"),
            "finrecovery" to listOf("fin","recovery","tiklash"),
            "case" to listOf("case","hodisa","ish"),
            "humanreview" to listOf("human","review","inson","mutaxassis","korik"),
            "explainable" to listOf("explainable","izohlanadigan","tushuntirish")
        )
        return (base + base.flatMap { aliases[it].orEmpty() }).distinct().take(12)
    }

    private fun insufficient(count: Int) = KnowledgeAnswer(
        "Import qilingan bilimlardan bu savolga yetarli dalil topilmadi. Taxminni fakt sifatida bermayman. Savolni aniqlashtirish yoki tegishli hujjatni tekshirish kerak.",
        emptyList(), "YETARLI DALIL TOPILMADI",
        "Bu FINZANJIR konsepsiyasida bunday qoida yo‘q degani emas. Qidiruvda mos yozuv topilmadi yoki savol boshqacha ifodalangan bo‘lishi mumkin.",
        count
    )

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
