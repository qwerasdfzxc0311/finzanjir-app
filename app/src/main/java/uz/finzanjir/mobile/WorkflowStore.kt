package uz.finzanjir.mobile

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject
import java.util.UUID

data class WorkflowRecord(
    val id: String,
    val type: String,
    val status: String,
    val title: String,
    val details: String,
    val source: String,
    val timestamp: Long,
    val eventId: String,
    val signalId: String,
    val caseId: String,
    val relatedIds: List<String>
)

data class WorkflowSnapshot(
    val eventId: String,
    val signalId: String,
    val caseId: String,
    val eventStatus: String,
    val signalStatus: String,
    val caseStatus: String,
    val reviewStatus: String,
    val records: List<WorkflowRecord>,
    val audit: List<WorkflowRecord>
)

/**
 * One local synthetic workflow shared by citizen, analyst and review workspaces.
 * Every record carries the same Event/Signal/Case keys plus explicit related record IDs.
 * This is a prototype store, not production RBAC, a bank connection or a real case system.
 */
object WorkflowStore {
    private const val PREFS = "finzanjir_demo_workflow_v1"
    private const val KEY_STATE = "workflow_state"
    private val lock = Any()

    fun load(context: Context): WorkflowSnapshot = synchronized(lock) {
        val prefs = context.applicationContext.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        val stored = prefs.getString(KEY_STATE, null)
        val state = if (stored.isNullOrBlank()) seed().also {
            prefs.edit().putString(KEY_STATE, it.toString()).apply()
        } else {
            try { JSONObject(stored) } catch (_: Exception) {
                seed().also { prefs.edit().putString(KEY_STATE, it.toString()).apply() }
            }
        }
        val entityLinksChanged = ensureEntityChain(state)
        val duplicateCleanupChanged = removeLegacyStageDuplicates(state)
        if (entityLinksChanged || duplicateCleanupChanged) {
            prefs.edit().putString(KEY_STATE, state.toString()).apply()
        }
        snapshot(state)
    }

    fun recordReview(context: Context, decision: String, reason: String): WorkflowSnapshot = synchronized(lock) {
        require(decision in setOf("SUPPORTED_FOR_FURTHER_CHECK", "NOT_SUPPORTED", "MORE_INFORMATION", "RECHECK", "ESCALATED")) {
            "Noto‘g‘ri review qarori"
        }
        val cleanReason = reason.trim()
        require(cleanReason.length >= 4) { "Qaror sababi kamida 4 belgidan iborat bo‘lsin." }
        val prefs = context.applicationContext.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        val state = try {
            prefs.getString(KEY_STATE, null)?.let { JSONObject(it) } ?: seed()
        } catch (_: Exception) { seed() }

        ensureEntityChain(state)
        val now = System.currentTimeMillis()
        val reviewId = "REV-" + UUID.randomUUID().toString()
        val nextCaseStatus = when (decision) {
            "SUPPORTED_FOR_FURTHER_CHECK" -> "REVIEW_SUPPORTED_NOT_VERDICT"
            "NOT_SUPPORTED" -> "REVIEW_NOT_SUPPORTED"
            "MORE_INFORMATION" -> "MORE_INFORMATION_REQUIRED"
            "RECHECK" -> "RECHECK_REQUIRED"
            else -> "ESCALATED_FOR_AUTHORIZED_REVIEW"
        }
        state.put("case_status", nextCaseStatus)
        state.put("review_status", decision)
        state.getJSONArray("records").put(recordJson(
            reviewId, "HUMAN_REVIEW", decision,
            "Mutaxassis ko‘rigi qayd etildi",
            cleanReason,
            "DEMO_REVIEWER",
            now,
            state.optString("event_id"), state.optString("signal_id"), state.optString("case_id"),
            listOf(state.optString("event_id"), state.optString("signal_id"), state.optString("case_id"))
        ))
        state.getJSONArray("audit").put(recordJson(
            "AUD-" + UUID.randomUUID().toString(), "AUDIT", "RECORDED",
            "Human Review holati o‘zgardi",
            "Case ${state.getString("case_id")}: ${decision}. Sabab: ${cleanReason}",
            "DEMO_REVIEWER",
            now,
            state.optString("event_id"), state.optString("signal_id"), state.optString("case_id"),
            listOf(state.optString("event_id"), state.optString("signal_id"), state.optString("case_id"))
        ))
        prefs.edit().putString(KEY_STATE, state.toString()).apply()
        snapshot(state)
    }

    fun updateCitizenCardStatus(context: Context, status: String): WorkflowSnapshot = synchronized(lock) {
        require(status in setOf("OWNED", "UNKNOWN", "LOST")) { "Noma’lum karta holati" }
        val prefs = context.applicationContext.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        val state = try { prefs.getString(KEY_STATE, null)?.let { JSONObject(it) } ?: seed() }
            catch (_: Exception) { seed() }
        ensureEntityChain(state)
        val records = state.getJSONArray("records")
        for (index in records.length() - 1 downTo 0) {
            if (records.optJSONObject(index)?.optString("id") == "CARD-DEMO-0001") records.remove(index)
        }
        val now = System.currentTimeMillis()
        val details = when (status) {
            "OWNED" -> "Fuqaro sintetik demo kartani o‘ziniki deb belgiladi. Real karta raqami yoki bank rekviziti saqlanmaydi."
            "UNKNOWN" -> "Fuqaro kartani tanimaydi deb belgiladi. Bu shubha qaydi; firibgarlik hukmi yoki avtomatik bloklash emas."
            else -> "Fuqaro demo kartani yo‘qotilgan deb belgiladi. Real bank bloklashi bajarilmaydi; fuqaro bankning rasmiy kanaliga murojaat qilishi kerak."
        }
        records.put(recordJson("CARD-DEMO-0001", "CITIZEN_CARD", status,
            "Mening kartalarim holati yangilandi", details, "CITIZEN_DEMO", now,
            state.optString("event_id"), state.optString("signal_id"), state.optString("case_id"),
            listOf("ENT-CARD-DEMO-0001", state.optString("case_id"))))
        state.getJSONArray("audit").put(recordJson("AUD-" + UUID.randomUUID().toString(),
            "AUDIT", "RECORDED", "Fuqaro karta holatini belgiladi",
            "CARD-DEMO-0001: $status. Bu faqat lokal sintetik demo qaydi.",
            "CITIZEN_DEMO", now, state.optString("event_id"), state.optString("signal_id"),
            state.optString("case_id"), listOf("CARD-DEMO-0001", state.optString("case_id"))))
        prefs.edit().putString(KEY_STATE, state.toString()).apply()
        snapshot(state)
    }

    fun runStage(context: Context, stage: String): WorkflowSnapshot = synchronized(lock) {
        require(stage in setOf("RISK_ENGINE", "CROSS_MATCH", "FRAUD_GRAPH", "TIMELINE", "FIN_RECOVERY")) {
            "Noma’lum platforma bosqichi"
        }
        val prefs = context.applicationContext.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        val state = try { prefs.getString(KEY_STATE, null)?.let { JSONObject(it) } ?: seed() }
            catch (_: Exception) { seed() }
        ensureEntityChain(state)
        removeLegacyStageDuplicates(state)
        val now = System.currentTimeMillis()
        val records = state.getJSONArray("records")
        val audit = state.getJSONArray("audit")
        val caseKey = state.optString("case_id", "CASE-DEMO-0001")
        val eventKey = state.optString("event_id", "EVT-DEMO-0001")
        val signalKey = state.optString("signal_id", "SIG-DEMO-0001")
        fun upsert(id: String, type: String, status: String, title: String, details: String, source: String, relatedIds: List<String> = emptyList()) {
            // One canonical record per stage and Case; reruns update instead of duplicating.
            for (index in records.length() - 1 downTo 0) {
                if (records.optJSONObject(index)?.optString("id") == id) records.remove(index)
            }
            records.put(recordJson(id, type, status, title, details, source, now,
                eventKey, signalKey, caseKey, relatedIds))
        }
        fun add(stagePrefix: String, type: String, status: String, title: String, details: String, source: String, relatedIds: List<String> = emptyList()) {
            upsert(stagePrefix + "-" + caseKey, type, status, title, details, source, relatedIds)
        }
        when (stage) {
            "RISK_ENGINE" -> {
                // Deliberately fixed synthetic score: this demonstrates explanation, not calibrated risk.
                state.put("demo_risk_score", 62)
                state.put("demo_risk_band", "YUQORI · DEMO")
                add("RSK", "RISK_ASSESSMENT", "DEMO_ONLY",
                    "Izohlanadigan xavf bahosi: 62/100",
                    "Sintetik misol. Omillar: vaqt ketma-ketligi bo‘yicha mos kelmaslik (+24); qurilma atributi mosligi (+18); ma’lumot yetishmasligi (+20). Qarshi kontekst: qurilma umumiy foydalanishda bo‘lishi mumkin. Ball kalibrlanmagan, haqiqiy fuqaro yoki tranzaksiyaga tatbiq etilmaydi.",
                    "DEMO_RISK_ENGINE", listOf(eventKey, signalKey, "ENT-DEVICE-DEMO-0001", "ENT-IP-DEMO-0001"))
            }
            "CROSS_MATCH" -> {
                add("XMT", "CROSS_MATCH", "CANDIDATE_LINKS",
                    "Sintetik Cross-Match natijasi",
                    "2 ta ehtimoliy atribut mosligi va 1 ta qarshi moslik topildi. Moslik shaxs aynan bir xil degani emas; manba, vaqt va mustaqil tasdiq talab qilinadi.",
                    "DEMO_CROSS_MATCH", listOf(signalKey, "ENT-DEVICE-DEMO-0001", "ENT-IP-DEMO-0001"))
                add("XMU", "UNKNOWN", "UNRESOLVED",
                    "Cross-Match noaniqligi",
                    "Bir xil qurilma yoki tarmoqdan bir nechta fuqaro foydalanishi mumkin. Aloqa yakuniy identifikatsiya emas.",
                    "DEMO_CROSS_MATCH", listOf("ENT-DEVICE-DEMO-0001", "ENT-IP-DEMO-0001", "ENT-CITIZEN-DEMO-0001"))
            }
            "FRAUD_GRAPH" -> {
                add("GRF", "GRAPH_NODE", "SYNTHETIC",
                    "Graf tugunlari: karta · hisob · qurilma · IP · qabul qiluvchi",
                    "Barcha tugunlar namoyish uchun yaratilgan. Tugunlar orasidagi aloqa faqat tekshiruv yo‘nalishini ko‘rsatadi.",
                    "DEMO_FRAUD_GRAPH", listOf("ENT-CITIZEN-DEMO-0001", "ENT-CHANNEL-DEMO-0001", "ENT-CARD-DEMO-0001", "ENT-ACCOUNT-DEMO-0001", "ENT-PHONE-DEMO-0001", "ENT-DEVICE-DEMO-0001", "ENT-IP-DEMO-0001", "ENT-RECIPIENT-DEMO-0001", "ENT-TRANSACTION-DEMO-0001"))
                add("GRE", "GRAPH_EDGE", "CANDIDATE",
                    "Graf qirralari: vaqt va atribut mosligi",
                    "2 ta sintetik qirra ko‘rsatildi. Umumiy qurilma yoki IP egalik/aybdorlikni isbotlamaydi.",
                    "DEMO_FRAUD_GRAPH", listOf("ENT-DEVICE-DEMO-0001", "ENT-IP-DEMO-0001", "ENT-RECIPIENT-DEMO-0001", "ENT-TRANSACTION-DEMO-0001"))
            }
            "TIMELINE" -> {
                add("TLN", "TIMELINE", "GENERATED",
                    "Case vaqt chizig‘i yangilandi",
                    "Event, Signal, dalillar, Cross-Match va Human Review yozuvlari vaqt tamg‘asi bo‘yicha bitta Case ID ostida jamlanadi.",
                    "DEMO_TIMELINE", (0 until records.length()).mapNotNull { records.optJSONObject(it)?.optString("id") }.take(80))
            }
            "FIN_RECOVERY" -> {
                add("REC", "RECOVERY_CASE", "GUIDANCE_ONLY",
                    "FIN-RECOVERY yo‘riqnomasi yaratildi",
                    "1) Kartani chiqargan bankning rasmiy kanaliga zudlik bilan murojaat qilish. 2) Bankdan tranzaksiyani tekshirish va mavjud bo‘lsa nizolash tartibini so‘rash. 3) Murojaat raqami va vaqtini saqlash. 4) Firibgarlik gumoni bo‘lsa vakolatli organlarga xabar berish. 5) OTP, PIN va CVVni hech kimga bermaslik. Pul qaytishi kafolatlanmaydi.",
                    "DEMO_FIN_RECOVERY", listOf(eventKey, signalKey, caseKey))
            }
        }
        audit.put(recordJson("AUD-" + UUID.randomUUID().toString(), "AUDIT", "RECORDED",
            "$stage bosqichi bajarildi",
            "Case ${state.optString("case_id")} uchun sintetik demo yozuvi qo‘shildi.",
            "LOCAL_DEMO", now, eventKey, signalKey, caseKey,
            listOf(eventKey, signalKey, caseKey)))
        prefs.edit().putString(KEY_STATE, state.toString()).apply()
        snapshot(state)
    }

    /**
     * Add the synthetic entity chain to older local workflow snapshots without
     * replacing existing Event, Signal, Case, evidence, review or audit records.
     */
    private fun ensureEntityChain(state: JSONObject): Boolean {
        val records = state.optJSONArray("records") ?: JSONArray().also { state.put("records", it) }
        val existing = (0 until records.length()).mapNotNull { records.optJSONObject(it)?.optString("id") }.toSet()
        state.put("workflow_schema_version", 2)
        val eventId = state.optString("event_id", "EVT-DEMO-0001")
        val signalId = state.optString("signal_id", "SIG-DEMO-0001")
        val caseId = state.optString("case_id", "CASE-DEMO-0001")
        val entities = listOf(
            Triple("ENT-CITIZEN-DEMO-0001", "Fuqaro", "Fuqaro uchun sintetik demo tuguni; haqiqiy shaxs ma’lumoti yo‘q."),
            Triple("ENT-CHANNEL-DEMO-0001", "Kanal", "To‘lov kanali uchun sintetik tugun."),
            Triple("ENT-CARD-DEMO-0001", "Karta", "Karta identifikatori saqlanmaydi; bu faqat sintetik obyekt."),
            Triple("ENT-ACCOUNT-DEMO-0001", "Hisob", "Hisob raqami yoki bank rekviziti saqlanmaydi."),
            Triple("ENT-PHONE-DEMO-0001", "Telefon", "Telefon raqami saqlanmaydi; faqat obyekt turi ko‘rsatiladi."),
            Triple("ENT-DEVICE-DEMO-0001", "Qurilma", "Qurilma atributlari namoyish uchun sintetik."),
            Triple("ENT-IP-DEMO-0001", "IP", "IP manzili saqlanmaydi; bu sintetik graf tuguni."),
            Triple("ENT-RECIPIENT-DEMO-0001", "Qabul qiluvchi", "Qabul qiluvchi shaxs yoki hisobining haqiqiy ma’lumoti yo‘q."),
            Triple("ENT-TRANSACTION-DEMO-0001", "Tranzaksiya", "Tranzaksiya summasi yoki real bank yozuvi yo‘q.")
        )
        var changed = false
        val now = System.currentTimeMillis()
        entities.forEachIndexed { index, entity ->
            if (entity.first !in existing) {
                val nextId = entities.getOrNull(index + 1)?.first ?: eventId
                records.put(recordJson(entity.first, "ENTITY", "SYNTHETIC_NODE",
                    entity.second, entity.third, "SYNTHETIC_ENTITY", now + index,
                    eventId, signalId, caseId, listOf(nextId)))
                changed = true
            }
        }

        // Backfill explicit links for older records without deleting or rewriting their content.
        val audit = state.optJSONArray("audit") ?: JSONArray()
        listOf(records, audit).forEach { array ->
            for (index in 0 until array.length()) {
                val item = array.optJSONObject(index) ?: continue
                if (item.optString("event_id").isBlank()) {
                    item.put("event_id", eventId); changed = true
                }
                if (item.optString("signal_id").isBlank()) {
                    item.put("signal_id", signalId); changed = true
                }
                if (item.optString("case_id").isBlank()) {
                    item.put("case_id", caseId); changed = true
                }
                val currentLinks = item.optJSONArray("related_ids")
                if (currentLinks == null || currentLinks.length() == 0) {
                    val links = when (item.optString("type")) {
                        "EVENT" -> listOf("ENT-TRANSACTION-DEMO-0001", signalId)
                        "SIGNAL" -> listOf(eventId, "ENT-DEVICE-DEMO-0001", "ENT-IP-DEMO-0001")
                        "EVIDENCE", "COUNTER_EVIDENCE", "UNKNOWN" ->
                            listOf("ENT-DEVICE-DEMO-0001", "ENT-IP-DEMO-0001")
                        "HUMAN_REVIEW", "AUDIT" -> listOf(eventId, signalId, caseId)
                        "RISK_ASSESSMENT" -> listOf(eventId, signalId, "ENT-DEVICE-DEMO-0001", "ENT-IP-DEMO-0001")
                        "CROSS_MATCH" -> listOf(signalId, "ENT-DEVICE-DEMO-0001", "ENT-IP-DEMO-0001")
                        "GRAPH_NODE" -> entities.map { it.first }
                        "GRAPH_EDGE" -> listOf("ENT-DEVICE-DEMO-0001", "ENT-IP-DEMO-0001", "ENT-RECIPIENT-DEMO-0001", "ENT-TRANSACTION-DEMO-0001")
                        "RECOVERY_CASE" -> listOf(eventId, signalId, caseId)
                        "CITIZEN_CARD" -> listOf("ENT-CARD-DEMO-0001", caseId)
                        else -> emptyList()
                    }
                    if (links.isNotEmpty()) {
                        item.put("related_ids", JSONArray(links))
                        changed = true
                    }
                }
            }
        }
        return changed
    }

    /**
     * One local Case is stored in this demo. Older builds appended a fresh synthetic
     * result every time a stage button was tapped. Keep the newest result per
     * synthetic stage/type, while preserving every Human Review and audit event.
     */
    private fun removeLegacyStageDuplicates(state: JSONObject): Boolean {
        val records = state.optJSONArray("records") ?: return false
        val stageSources = setOf(
            "DEMO_RISK_ENGINE", "DEMO_CROSS_MATCH", "DEMO_FRAUD_GRAPH",
            "DEMO_TIMELINE", "DEMO_FIN_RECOVERY"
        )
        val latest = LinkedHashMap<String, JSONObject>()
        val preserved = ArrayList<JSONObject>()
        for (index in 0 until records.length()) {
            val item = records.optJSONObject(index) ?: continue
            val source = item.optString("source")
            if (source !in stageSources) {
                preserved.add(item)
            } else {
                val key = item.optString("type") + "|" + source
                val current = latest[key]
                if (current == null || item.optLong("timestamp") >= current.optLong("timestamp")) {
                    latest[key] = item
                }
            }
        }
        val rebuilt = JSONArray()
        preserved.forEach { rebuilt.put(it) }
        latest.values.sortedBy { it.optLong("timestamp") }.forEach { rebuilt.put(it) }
        val changed = rebuilt.length() != records.length()
        if (changed) state.put("records", rebuilt)
        return changed
    }

    private fun seed(): JSONObject {
        val now = System.currentTimeMillis()
        val state = JSONObject()
            .put("workflow_schema_version", 2)
            .put("event_id", "EVT-DEMO-0001")
            .put("signal_id", "SIG-DEMO-0001")
            .put("case_id", "CASE-DEMO-0001")
            .put("event_status", "SYNTHETIC_EVENT_RECORDED")
            .put("signal_status", "OBSERVATION_REQUIRES_CONTEXT")
            .put("case_status", "CASE_CANDIDATE")
            .put("review_status", "PENDING_HUMAN_REVIEW")
            .put("records", JSONArray())
            .put("audit", JSONArray())

        val records = state.getJSONArray("records")
        val eventId = state.getString("event_id")
        val signalId = state.getString("signal_id")
        val caseId = state.getString("case_id")
        records.put(recordJson("EVT-DEMO-0001", "EVENT", "SYNTHETIC",
            "Namoyish hodisasi qayd etildi",
            "To‘lovga oid sintetik hodisa. Haqiqiy fuqaro, karta yoki bank ma’lumoti ishlatilmagan.",
            "LOCAL_DEMO", now - 300000, eventId, signalId, caseId, listOf("ENT-TRANSACTION-DEMO-0001", signalId)))
        records.put(recordJson("SIG-DEMO-0001", "SIGNAL", "OBSERVATION_ONLY",
            "Qurilma va vaqt ketma-ketligi bo‘yicha tekshiruv signali",
            "Signal tekshirish indikatori; firibgarlik isboti yoki ayblov emas.",
            "SYNTHETIC_RULE_DEMO", now - 240000, eventId, signalId, caseId, listOf(eventId, "ENT-DEVICE-DEMO-0001", "ENT-IP-DEMO-0001")))
        records.put(recordJson("EVD-DEMO-0001", "EVIDENCE", "CANDIDATE",
            "Tasdiqlovchi kontekst",
            "Qurilma atributlari orasida moslik borligi haqidagi sintetik kuzatuv; mustaqil tasdiq talab etiladi.",
            "SYNTHETIC_SOURCE_A", now - 180000, eventId, signalId, caseId, listOf("ENT-DEVICE-DEMO-0001", "ENT-IP-DEMO-0001")))
        records.put(recordJson("CEV-DEMO-0001", "COUNTER_EVIDENCE", "CANDIDATE",
            "Qarshi dalil",
            "Qurilma oilaviy yoki umumiy foydalanishda bo‘lishi mumkin; atribut mosligi shaxsni aniqlamaydi.",
            "SYNTHETIC_SOURCE_B", now - 120000, eventId, signalId, caseId, listOf("ENT-DEVICE-DEMO-0001", "ENT-CITIZEN-DEMO-0001")))
        records.put(recordJson("UNK-DEMO-0001", "UNKNOWN", "UNRESOLVED",
            "Aniqlashtirilmagan ma’lumot",
            "Qurilma hodisa vaqtida kimning nazoratida bo‘lgani noma’lum.",
            "NOT_PROVIDED", now - 60000, eventId, signalId, caseId, listOf("ENT-DEVICE-DEMO-0001", "ENT-IP-DEMO-0001")))
        val entityChain = listOf(
            Triple("ENT-CITIZEN-DEMO-0001", "Fuqaro", "Fuqaro uchun sintetik demo tuguni; haqiqiy shaxs ma’lumoti yo‘q."),
            Triple("ENT-CHANNEL-DEMO-0001", "Kanal", "To‘lov kanali uchun sintetik tugun."),
            Triple("ENT-CARD-DEMO-0001", "Karta", "Karta identifikatori saqlanmaydi; bu faqat sintetik obyekt."),
            Triple("ENT-ACCOUNT-DEMO-0001", "Hisob", "Hisob raqami yoki bank rekviziti saqlanmaydi."),
            Triple("ENT-PHONE-DEMO-0001", "Telefon", "Telefon raqami saqlanmaydi; faqat obyekt turi ko‘rsatiladi."),
            Triple("ENT-DEVICE-DEMO-0001", "Qurilma", "Qurilma atributlari namoyish uchun sintetik."),
            Triple("ENT-IP-DEMO-0001", "IP", "IP manzili saqlanmaydi; bu sintetik graf tuguni."),
            Triple("ENT-RECIPIENT-DEMO-0001", "Qabul qiluvchi", "Qabul qiluvchi shaxs yoki hisobining haqiqiy ma’lumoti yo‘q."),
            Triple("ENT-TRANSACTION-DEMO-0001", "Tranzaksiya", "Tranzaksiya summasi yoki real bank yozuvi yo‘q.")
        )
        entityChain.forEachIndexed { index, entity ->
            val nextId = entityChain.getOrNull(index + 1)?.first ?: eventId
            records.put(recordJson(entity.first, "ENTITY", "SYNTHETIC_NODE",
                entity.second, entity.third, "SYNTHETIC_ENTITY", now - 45000 + index * 1000,
                eventId, signalId, caseId, listOf(nextId)))
        }
        state.getJSONArray("audit").put(recordJson(
            "AUD-SEED-0001", "AUDIT", "CREATED",
            "Sintetik demo oqimi yaratildi",
            "Event, Signal, Case va fuqaro → kanal → karta → hisob → telefon → qurilma/IP → qabul qiluvchi → tranzaksiya zanjiri bitta umumiy modelga bog‘langan.",
            "SYSTEM_DEMO", now, eventId, signalId, caseId,
            listOf(eventId, signalId, caseId)
        ))
        return state
    }

    private fun recordJson(
        id: String, type: String, status: String, title: String,
        details: String, source: String, timestamp: Long,
        eventId: String = "", signalId: String = "", caseId: String = "",
        relatedIds: List<String> = emptyList()
    ) = JSONObject()
        .put("id", id).put("type", type).put("status", status)
        .put("title", title).put("details", details)
        .put("source", source).put("timestamp", timestamp)
        .put("event_id", eventId).put("signal_id", signalId).put("case_id", caseId)
        .put("related_ids", JSONArray(relatedIds))

    private fun snapshot(state: JSONObject): WorkflowSnapshot {
        fun readRecords(key: String): List<WorkflowRecord> {
            val array = state.optJSONArray(key) ?: JSONArray()
            return (0 until array.length()).mapNotNull { index ->
                val item = array.optJSONObject(index) ?: return@mapNotNull null
                WorkflowRecord(
                    item.optString("id"), item.optString("type"), item.optString("status"),
                    item.optString("title"), item.optString("details"), item.optString("source"),
                    item.optLong("timestamp"),
                    item.optString("event_id").ifBlank { state.optString("event_id") },
                    item.optString("signal_id").ifBlank { state.optString("signal_id") },
                    item.optString("case_id").ifBlank { state.optString("case_id") },
                    (item.optJSONArray("related_ids") ?: JSONArray()).let { links ->
                        (0 until links.length()).map { links.optString(it) }.filter { it.isNotBlank() }
                    }
                )
            }
        }
        return WorkflowSnapshot(
            state.optString("event_id"), state.optString("signal_id"), state.optString("case_id"),
            state.optString("event_status"), state.optString("signal_status"),
            state.optString("case_status"), state.optString("review_status"),
            readRecords("records"), readRecords("audit")
        )
    }
}
