package uz.finzanjir.mobile

import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import android.util.JsonReader
import android.util.JsonToken
import org.json.JSONArray
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
    const val VERSION = "v7-multilingual-evidence-fts4-2026-11-10"
    private const val ASSET = "finzanjir_knowledge.json"
    private const val MANIFEST = "knowledge_manifest.json"
    private const val DB_NAME = "finzanjir_knowledge_v6.db"
    private const val DB_VERSION = 4
    private const val MAX_CANDIDATES = 48
    private const val MAX_ANSWER_RECORDS = 6

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
        val language: String,
        val legacyVersionsJson: String,
        val legacyProvenanceJson: String
    )
    private data class Candidate(val record: Record, val score: Int)

    private class DbHelper(context: Context) :
        SQLiteOpenHelper(context.applicationContext, DB_NAME, null, DB_VERSION) {
        override fun onCreate(db: SQLiteDatabase) {
            db.execSQL("""CREATE TABLE IF NOT EXISTS knowledge_meta(
                _id INTEGER PRIMARY KEY, id TEXT NOT NULL UNIQUE, body TEXT NOT NULL, approval TEXT NOT NULL,
                source_id TEXT NOT NULL, source_version TEXT NOT NULL, source_section TEXT NOT NULL,
                source_path TEXT NOT NULL, record_type TEXT NOT NULL, audience TEXT NOT NULL,
                domain TEXT NOT NULL, language TEXT NOT NULL,
                legacy_versions_json TEXT NOT NULL DEFAULT '[]',
                legacy_provenance_json TEXT NOT NULL DEFAULT '[]'
            )""")
            db.execSQL("CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts USING fts4(search_text, tokenize=unicode61)")
            db.execSQL("CREATE TABLE IF NOT EXISTS knowledge_state(key TEXT PRIMARY KEY, value TEXT NOT NULL)")
            db.execSQL("CREATE TABLE IF NOT EXISTS token_lexicon(term TEXT PRIMARY KEY)")
            db.execSQL("CREATE INDEX IF NOT EXISTS knowledge_meta_type ON knowledge_meta(record_type)")
            db.execSQL("CREATE INDEX IF NOT EXISTS knowledge_meta_approval ON knowledge_meta(approval)")
        }
        override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
            // Additive migration: retain the existing local index and all source history.
            onCreate(db)
            ensureColumn(db, "knowledge_meta", "legacy_versions_json", "TEXT NOT NULL DEFAULT '[]'")
            ensureColumn(db, "knowledge_meta", "legacy_provenance_json", "TEXT NOT NULL DEFAULT '[]'")
        }

        private fun ensureColumn(db: SQLiteDatabase, table: String, column: String, definition: String) {
            val exists = db.rawQuery("PRAGMA table_info($table)", null).use { cursor ->
                var found = false
                while (cursor.moveToNext()) {
                    if (cursor.getString(cursor.getColumnIndexOrThrow("name")) == column) found = true
                }
                found
            }
            if (!exists) db.execSQL("ALTER TABLE $table ADD COLUMN $column $definition")
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
        val understood = understandQuery(question)
        val q = normalize(understood)
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
            authorQuestion -> authorRecords(database, question)
            else -> retrieve(database, understood, expertMode, authorQuestion)
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
            scoreCandidates(understood, rows).distinctBy { normalize(it.record.text) }.take(MAX_ANSWER_RECORDS)
        }
        if (selected.isEmpty()) return insufficient(count(context))

        val baseAnswer = composeAnswer(understood, selected, layerOverview)
        val conflicts = detectConflicts(selected)
        val modeIntro = if (expertMode) "MUTAXASSIS REJIMI — texnik izohlar va to‘liq manba izi.\n\n"
            else "FUQARO REJIMI — sodda izoh; risk signali aybdorlik isboti emas.\n\n"
        val conflictBlock = if (conflicts.isEmpty()) "" else
            "\n\nMANBALARDA EHTIMOLIY ZIDLIK: bu bayonlar bir-biriga mos kelmasligi mumkin; ularni yashirmadim. Inson tekshiruvi zarur:\n" +
                conflicts.joinToString("\n") { "• " + it }
        val citizenHelp = if (expertMode) "" else citizenGlossary(question)
        val answer = modeIntro + citizenHelp + (if (Regex("\\brecal\\b", RegexOption.IGNORE_CASE).containsMatchIn(question))
            "Yuklangan manbalarda “ReCAL” nomli alohida modul yoki qisqartma mustaqil ta’riflanmagan. Quyidagi dalillar faqat risk modelini qayta kalibrlash (recalibration) mavzusiga yaqin; uni FIN-RECOVERY bilan tenglashtirmayman.\\n\\n" + baseAnswer
        else baseAnswer) + conflictBlock
        // Exact-text duplicates remain separate source records in SQLite.
        // Collapse repeated answer text, but retain every matching provenance row.
        val provenance = LinkedHashMap<String, Record>()
        selected.forEach { candidate ->
            val matchingSources = queryMeta(
                database,
                "SELECT m.* FROM knowledge_meta m WHERE m.body=?",
                arrayOf(candidate.record.text)
            )
            matchingSources.forEach { source -> provenance.putIfAbsent(source.id, source) }
            rows.filter { normalize(it.text) == normalize(candidate.record.text) }
                .forEach { source -> provenance.putIfAbsent(source.id, source) }
        }
        val sources = provenance.values.flatMap { r ->
            val lines = ArrayList<String>()
            lines += r.id + " | " + r.sourceId + " | " + r.sourceVersion + " | " +
                r.sourceSection + " | " + r.sourcePath + " | " + r.approval
            val oldSources = safeArray(r.legacyProvenanceJson)
            for (i in 0 until oldSources.length()) {
                val old = oldSources.optJSONObject(i) ?: continue
                lines += "LEGACY_PROVENANCE | " + old.optString("id") + " | " +
                    old.optString("source_id") + " | " + old.optString("source_version") + " | " +
                    old.optString("source_section") + " | " + old.optString("source_path") +
                    " | " + old.optString("snapshot")
            }
            val versions = safeArray(r.legacyVersionsJson)
            for (i in 0 until versions.length()) {
                val version = versions.optJSONObject(i) ?: continue
                val old = version.optJSONObject("provenance") ?: JSONObject()
                lines += "HISTORICAL_VERSION | " + old.optString("id") + " | " +
                    old.optString("source_id") + " | " + old.optString("source_version") + " | " +
                    old.optString("source_section") + " | " + old.optString("source_path") +
                    " | " + version.optString("version_status")
            }
            lines
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
            " So‘rov tili taxmini: " + detectLanguage(question).uppercase(Locale.ROOT) +
            "; yozuv variantlari normallashtiriladi, imlo tuzatishi taxminiy bo‘lishi mumkin. " +
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
            database.delete("token_lexicon", null, null)
            val metaInsert = database.compileStatement(
                """INSERT INTO knowledge_meta(id,body,approval,source_id,source_version,source_section,
                source_path,record_type,audience,domain,language,legacy_versions_json,legacy_provenance_json)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)"""
            )
            val ftsInsert = database.compileStatement(
                "INSERT INTO knowledge_fts(docid,search_text) VALUES(?,?)"
            )
            val lexiconInsert = database.compileStatement("INSERT OR IGNORE INTO token_lexicon(term) VALUES(?)")
            var imported = 0
            JsonReader(InputStreamReader(FileInputStream(staged), Charsets.UTF_8)).use { reader ->
                reader.beginArray()
                while (reader.hasNext()) {
                    val r = readRecord(reader)
                    if (r.id.isBlank() || r.text.isBlank()) continue
                    metaInsert.clearBindings()
                    listOf(r.id,r.text,r.approval,r.sourceId,r.sourceVersion,r.sourceSection,r.sourcePath,
                        r.recordType,r.audience,r.domain,r.language,r.legacyVersionsJson,r.legacyProvenanceJson).forEachIndexed { i, value ->
                        metaInsert.bindString(i + 1, value)
                    }
                    val rowId = metaInsert.executeInsert()
                    ftsInsert.clearBindings()
                    ftsInsert.bindLong(1, rowId)
                    // Legacy text aliases remain searchable without creating duplicate records.
                    val searchable = normalize(
                        r.text + " " + r.searchAliases.joinToString(" ") + " " + r.id + " " +
                            r.sourceSection + " " + r.recordType + " " + r.domain
                    )
                    ftsInsert.bindString(2, searchable)
                    ftsInsert.executeInsert()
                    searchable.split(" ").filter { it.length >= 3 && it.length <= 32 }.distinct().forEach { term ->
                        lexiconInsert.clearBindings()
                        lexiconInsert.bindString(1, term)
                        lexiconInsert.executeInsert()
                    }
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
        var domain: String = "unclassified", var language: String = "und",
        var searchAliases: List<String> = emptyList(),
        var legacyVersionsJson: String = "[]",
        var legacyProvenanceJson: String = "[]"
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
                "search_aliases" -> r.searchAliases = readStringArray(reader)
                "legacy_versions" -> r.legacyVersionsJson = readJsonValue(reader).toString()
                "legacy_provenance" -> r.legacyProvenanceJson = readJsonValue(reader).toString()
                else -> reader.skipValue()
            }
        }
        reader.endObject()
        return r
    }

    private fun readJsonValue(reader: JsonReader): Any? = when (reader.peek()) {
        JsonToken.BEGIN_OBJECT -> {
            val obj = JSONObject()
            reader.beginObject()
            while (reader.hasNext()) {
                val key = reader.nextName()
                obj.put(key, readJsonValue(reader))
            }
            reader.endObject()
            obj
        }
        JsonToken.BEGIN_ARRAY -> {
            val array = JSONArray()
            reader.beginArray()
            while (reader.hasNext()) array.put(readJsonValue(reader))
            reader.endArray()
            array
        }
        JsonToken.STRING, JsonToken.NUMBER -> reader.nextString()
        JsonToken.BOOLEAN -> reader.nextBoolean()
        JsonToken.NULL -> { reader.nextNull(); JSONObject.NULL }
        else -> { reader.skipValue(); JSONObject.NULL }
    }

    private fun readStringArray(reader: JsonReader): List<String> {
        if (reader.peek() == JsonToken.NULL) {
            reader.nextNull()
            return emptyList()
        }
        if (reader.peek() != JsonToken.BEGIN_ARRAY) {
            reader.skipValue()
            return emptyList()
        }
        val values = ArrayList<String>()
        reader.beginArray()
        while (reader.hasNext()) {
            when (reader.peek()) {
                JsonToken.STRING, JsonToken.NUMBER -> values.add(reader.nextString())
                JsonToken.NULL -> reader.nextNull()
                else -> reader.skipValue()
            }
        }
        reader.endArray()
        return values
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

    private fun authorRecords(database: SQLiteDatabase, question: String): List<Record> {
        val language = detectLanguage(question)
        val sourceLanguage = if (language == "uz") "und" else language
        return queryMeta(database,
            """SELECT m.* FROM knowledge_meta m
               WHERE (m.record_type IN ('author_biography','founder_multilingual_bio')
                  OR m.approval='author_visible_on_direct_request')
                 AND (m.language=? OR m.language='und')
               ORDER BY CASE WHEN m.language=? THEN 0 ELSE 1 END, m.id LIMIT 1""",
            arrayOf(sourceLanguage, sourceLanguage))
    }

    private fun detectLanguage(question: String): String {
        val q = question.lowercase(Locale.ROOT)
        return when {
            q.contains("qaraqalpaq") || q.contains("qoraqalpoq") || q.contains("қарақалпақ") ||
                q.contains("ақша") || q.contains("жоғалды") || q.contains("істеймен") ||
                listOf("aqsha", "qalay", "jaqsi", "jaman", "menin", "bizdin", "qaysi")
                    .any { Regex("\\b" + it + "\\b").containsMatchIn(q) } -> "kaa"
            listOf("ў", "ҳ", "қиламан", "бўйича", "ўзбек").any { q.contains(it) } -> "uz"
            Regex("[әіңғүұқөһ]").containsMatchIn(q) -> "kk"
            Regex("[áǵńóúı]").containsMatchIn(q) -> "kaa"
            Regex("[а-яё]").containsMatchIn(q) && !Regex("[қғңәіңұүөһ]").containsMatchIn(q) -> "ru"
            Regex("\\b(what|who|why|how|english|author)\\b").containsMatchIn(q) -> "en"
            else -> "uz"
        }
    }

    private fun retrieve(database: SQLiteDatabase, question: String, expertMode: Boolean, authorQuestion: Boolean): List<Record> {
        val terms = queryTerms(question).take(10)
        if (terms.isEmpty()) return emptyList()
        val correctedTerms = correctTerms(database, terms)
        val expressions = listOf(
            correctedTerms.take(5).joinToString(" AND ") { "\"" + it + "\"" },
            correctedTerms.joinToString(" OR ") { "\"" + it + "\"" }
        ).distinct()
        val gathered = LinkedHashMap<String, Record>()
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
            found.forEach { gathered.putIfAbsent(it.id, it) }
            if (gathered.size >= MAX_CANDIDATES * 2) break
        }
        return gathered.values.toList()
    }

    private fun correctTerms(database: SQLiteDatabase, terms: List<String>): List<String> {
        return terms.map { term ->
            val exact = database.rawQuery("SELECT 1 FROM token_lexicon WHERE term=? LIMIT 1", arrayOf(term)).use { it.moveToFirst() }
            if (exact || term.length < 5) term
            else {
                val min = (term.length - 1).coerceAtLeast(4)
                val max = term.length + 1
                val candidates = ArrayList<String>()
                database.rawQuery("SELECT term FROM token_lexicon WHERE substr(term,1,1)=substr(?,1,1) AND length(term) BETWEEN ? AND ? LIMIT 1200", arrayOf(term, min.toString(), max.toString())).use { c ->
                    while (c.moveToNext()) candidates += c.getString(0)
                }
                candidates.asSequence()
                    .map { it to editDistanceAtMostOne(term, it) }
                    .filter { it.second }
                    .map { it.first }
                    .sortedBy { kotlin.math.abs(it.length - term.length) }
                    .firstOrNull() ?: term
            }
        }.distinct()
    }

    private fun editDistanceAtMostOne(a: String, b: String): Boolean {
        if (kotlin.math.abs(a.length - b.length) > 1) return false
        var i = 0
        var j = 0
        var edits = 0
        while (i < a.length && j < b.length) {
            if (a[i] == b[j]) { i++; j++ }
            else {
                edits++
                if (edits > 1) return false
                if (a.length > b.length) i++
                else if (b.length > a.length) j++
                else { i++; j++ }
            }
        }
        if (i < a.length || j < b.length) edits++
        return edits <= 1
    }

    private fun safeArray(json: String): JSONArray = try {
        JSONArray(json)
    } catch (_: Exception) {
        JSONArray()
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
                    language = c.getString(c.getColumnIndexOrThrow("language")),
                    legacyVersionsJson = c.getString(c.getColumnIndexOrThrow("legacy_versions_json")),
                    legacyProvenanceJson = c.getString(c.getColumnIndexOrThrow("legacy_provenance_json"))
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
            val bodyTerms = body.split(" ").filter { it.length >= 4 }
            val hits = terms.count { term -> body.contains(term) || bodyTerms.any { editDistanceAtMostOne(term, it) } }
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
            var body = if (chosen.isNotEmpty()) chosen.joinToString(" ") else r.text.take(900)
            if (r.recordType == "author_biography") {
                body = body.replace("Smaylov Salamat Tangrbergen uli", "Salamat Smaylov Tangrbergen uli")
            }
            (if (index == 0) "" else "\n\nBog‘liq manba: ") + body
        }.joinToString("").take(5200)
    }

    private fun citizenGlossary(question: String): String {
        val q = normalize(question)
        val notes = ArrayList<String>()
        if (q.contains("risk") || q.contains("xavf")) notes += "Risk Engine — xavf belgilarini bir joyga jamlab, tekshiruvga yordam beradigan baholash mexanizmi."
        if (q.contains("fraud") || q.contains("graf")) notes += "Fraud Graph — karta, hisob, qurilma va tranzaksiyalar orasidagi bog‘lanishlarni ko‘rsatish usuli."
        if (q.contains("case") || q.contains("hodisa")) notes += "Case — tekshirish uchun yig‘ilgan hodisa materiallari; Case ochilishi aybdorlikni anglatmaydi."
        if (q.contains("human") || q.contains("review") || q.contains("inson")) notes += "Human Review — dalillarni vakolatli mutaxassisning inson sifatida ko‘rib chiqishi."
        if (q.contains("recovery") || q.contains("tiklash")) notes += "FIN-RECOVERY — hodisadan keyingi tiklash jarayonini qo‘llab-quvvatlash konsepsiyasi; pul qaytishini kafolatlamaydi."
        return if (notes.isEmpty()) "" else notes.joinToString("\n", "Qisqa izoh:\n", "\n\n") + ""
    }

    private fun detectConflicts(rows: List<Candidate>): List<String> {
        val positive = listOf("mavjud", "ulanadi", "ishlaydi", "tasdiqlangan", "faol", "bor")
        val negative = listOf("mavjud emas", "ulanmagan", "ishlamaydi", "tasdiqlanmagan", "faol emas", "yo‘q", "yo'q")
        val claims = rows.flatMap { candidate ->
            val record = candidate.record
            record.text.split(Regex("(?<=[.!?])\\s+|\\n+")).mapNotNull { sentence ->
                val normalized = normalize(sentence)
                val neg = negative.any { normalized.contains(normalize(it)) }
                val pos = !neg && positive.any { normalized.contains(normalize(it)) }
                if (pos == neg || sentence.length < 45) null
                else Triple(record, sentence.trim().take(220), if (pos) 1 else -1)
            }
        }
        val conflicts = ArrayList<String>()
        for (i in claims.indices) for (j in i + 1 until claims.size) {
            val a = claims[i]; val b = claims[j]
            if (a.third == b.third || a.first.sourceId == b.first.sourceId) continue
            val at = normalize(a.second).split(" ").filter { it.length > 3 }.toSet()
            val bt = normalize(b.second).split(" ").filter { it.length > 3 }.toSet()
            val common = at.intersect(bt).size
            val similarity = common.toDouble() / at.union(bt).size.coerceAtLeast(1)
            if (common >= 3 && similarity >= 0.28) {
                conflicts += "${a.first.sourceId}: “${a.second}” ↔ ${b.first.sourceId}: “${b.second}”"
                if (conflicts.size >= 3) return conflicts
            }
        }
        return conflicts.distinct()
    }

    private fun understandQuery(question: String): String {
        var value = question.lowercase(Locale.ROOT)
        val corrections = mapOf(
            "finzajir" to "finzanjir", "finzanjr" to "finzanjir",
            "risk engin" to "risk engine", "riskengine" to "risk engine",
            "fraud graf" to "fraud graph", "fraudgraph" to "fraud graph",
            "human revyu" to "human review", "humanreview" to "human review",
            "mutahasis" to "mutaxassis", "mutaxasis" to "mutaxassis",
            "qatlamla" to "qatlamlar", "firibgarlk" to "firibgarlik",
            "qaraqalpaqsha" to "qaraqalpaq", "qarakalpak" to "qaraqalpaq",
            "qoraqalpoqcha" to "qoraqalpoq", "ақша" to "pul",
            "жоғалды" to "yoqoldi", "не істеймен" to "nima qilaman"
        )
        corrections.forEach { (wrong, right) -> value = value.replace(wrong, right) }
        val language = detectLanguage(question)
        if (language == "kk" || language == "kaa") {
            val aliases = mapOf("aqsha" to "pul", "qarjiliq" to "moliyaviy",
                "qorǵaw" to "himoya", "aldaw" to "firibgarlik")
            aliases.forEach { (from, to) -> value = value.replace(from, to) }
        }
        return value
    }

    private fun isAuthorRecord(r: Record): Boolean {
        val t = r.recordType.lowercase(Locale.ROOT)
        return t.contains("author") || t.contains("founder") ||
            r.approval == "author_visible_on_direct_request"
    }

    private fun stemToken(input: String): String {
        val suffixes = listOf("laring", "lering", "lardan", "lerden", "larning",
            "ning", "nen", "nan", "dan", "den", "men", "ben", "lar", "ler",
            "ga", "ge", "qa", "ke", "ni", "nı", "di", "dı", "ti", "tı", "da", "de", "ta", "te")
        for (suffix in suffixes.sortedByDescending { it.length }) {
            if (input.endsWith(suffix) && input.length - suffix.length >= 4) {
                return input.dropLast(suffix.length)
            }
        }
        return input
    }

    private fun queryTerms(value: String): List<String> {
        val stop = setOf("va","yoki","bu","shu","uchun","bilan","ham","nima","qanday","qaysi","haqida","bor","deb","esa","men",
            "the","what","how","does","is","are","and","with","for","about","who","why","это","как","что","для","кто","ne","kerek","qalay","islew")
        val base = normalize(value).split(Regex("\\s+")).map { rawToken ->
            val token = stemToken(rawToken)
            when (token) {
                "qatlamlar","qatlamning","qatlamga","qatlamni","qatlamlardi","qatlamlarnı" -> "qatlam"
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
            "riskengine" to listOf("risk","engine"), "risk" to listOf("risk","xavf","qawip"),
            "finzanjir" to listOf("finzanjir","moliyaviy","zanjir"),
            "qaraqalpaq" to listOf("qaraqalpaq","qoraqalpoq","karakalpak"),
            "qoraqalpoq" to listOf("qoraqalpoq","qaraqalpaq","karakalpak"),
            "aqsha" to listOf("aqsha","aqsham","pul","money","qarji"),
            "aqsham" to listOf("aqsham","aqsha","pul","qarji"),
            "kartam" to listOf("kartam","karta","card"),
            "jogaldi" to listOf("jogaldi","jogal","yoqoldi","yoqol","yoqolgan","lost","joq"),
            "jogal" to listOf("jogal","jogaldi","yoqoldi","yoqol","yoqolgan","lost","joq"),
            "yoqol" to listOf("yoqol","yoqoldi","yoqolgan","lost","joq"),
            "yo'qol" to listOf("yo'qol","yoqoldi","yoqolgan","lost","joq"),
            "yoqoldi" to listOf("yoqoldi","yoqolgan","lost","joq"),
            "firibgar" to listOf("firibgar","aldaw","aldash"),
            "aldaw" to listOf("aldaw","firibgar","firibgarlik"),
            "qorgaw" to listOf("qorgaw","himoya","protect"),
            "qalay" to listOf("qalay","qanday","how"),
            "graf" to listOf("graf","graph","fraud"),
            "isley" to listOf("isley","islew","ishlash","work"),
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
                    'н' -> "n"; 'ң' -> "ng"; 'ә' -> "a"; 'ө' -> "o"; 'ү' -> "u"; 'ұ' -> "u"; 'і' -> "i"
                    'о' -> "o"; 'п' -> "p"; 'р' -> "r"; 'с' -> "s"; 'т' -> "t"; 'у' -> "u"
                    'ф' -> "f"; 'х' -> "x"; 'ц' -> "ts"; 'ч' -> "ch"; 'ш' -> "sh"; 'щ' -> "sh"
                    'ъ', 'ь' -> ""; 'ы' -> "i"; 'э' -> "e"; 'ю' -> "yu"; 'я' -> "ya"
                    'ў' -> "o"; 'қ' -> "q"; 'ғ' -> "g"; 'ҳ' -> "h"
                    'á' -> "a"; 'ǵ' -> "g"; 'ń' -> "n"; 'ó' -> "o"; 'ú' -> "u"; 'ı' -> "i"
                    '’', 'ʻ', '\u0060', 'ʼ' -> "'"
                    else -> c.toString()
                })
            }
        }
        return latin.replace(Regex("[^a-z0-9']+"), " ").trim().replace(Regex("\\s+"), " ")
    }
}
