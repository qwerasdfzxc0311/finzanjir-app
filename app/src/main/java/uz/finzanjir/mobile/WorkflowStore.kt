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
    val timestamp: Long
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
 * One local synthetic workflow shared by Jarayon, Signallar, Case and Human Review.
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
            now
        ))
        state.getJSONArray("audit").put(recordJson(
            "AUD-" + UUID.randomUUID().toString(), "AUDIT", "RECORDED",
            "Human Review holati o‘zgardi",
            "Case ${state.getString("case_id")}: ${decision}. Sabab: ${cleanReason}",
            "DEMO_REVIEWER",
            now
        ))
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
        val now = System.currentTimeMillis()
        val suffix = now.toString()
        val records = state.getJSONArray("records")
        val audit = state.getJSONArray("audit")
        fun upsert(id: String, type: String, status: String, title: String, details: String, source: String) {
            // One canonical record per stage and Case; reruns update instead of duplicating.
            for (index in records.length() - 1 downTo 0) {
                if (records.optJSONObject(index)?.optString("id") == id) records.remove(index)
            }
            records.put(recordJson(id, type, status, title, details, source, now))
        }
        val caseKey = state.optString("case_id", "CASE-DEMO-0001")
        fun add(stagePrefix: String, type: String, status: String, title: String, details: String, source: String) {
            upsert(stagePrefix + "-" + caseKey, type, status, title, details, source)
        }
        when (stage) {
            "RISK_ENGINE" -> {
                // Deliberately fixed synthetic score: this demonstrates explanation, not calibrated risk.
                state.put("demo_risk_score", 62)
                state.put("demo_risk_band", "YUQORI · DEMO")
                add("RSK", "RISK_ASSESSMENT", "DEMO_ONLY",
                    "Izohlanadigan xavf bahosi: 62/100",
                    "Sintetik misol. Omillar: vaqt ketma-ketligi bo‘yicha mos kelmaslik (+24); qurilma atributi mosligi (+18); ma’lumot yetishmasligi (+20). Qarshi kontekst: qurilma umumiy foydalanishda bo‘lishi mumkin. Ball kalibrlanmagan, haqiqiy fuqaro yoki tranzaksiyaga tatbiq etilmaydi.",
                    "DEMO_RISK_ENGINE")
            }
            "CROSS_MATCH" -> {
                add("XMT", "CROSS_MATCH", "CANDIDATE_LINKS",
                    "Sintetik Cross-Match natijasi",
                    "2 ta ehtimoliy atribut mosligi va 1 ta qarshi moslik topildi. Moslik shaxs aynan bir xil degani emas; manba, vaqt va mustaqil tasdiq talab qilinadi.",
                    "DEMO_CROSS_MATCH")
                add("XMU", "UNKNOWN", "UNRESOLVED",
                    "Cross-Match noaniqligi",
                    "Bir xil qurilma yoki tarmoqdan bir nechta fuqaro foydalanishi mumkin. Aloqa yakuniy identifikatsiya emas.",
                    "DEMO_CROSS_MATCH")
            }
            "FRAUD_GRAPH" -> {
                add("GRF", "GRAPH_NODE", "SYNTHETIC",
                    "Graf tugunlari: karta · hisob · qurilma · IP · qabul qiluvchi",
                    "Barcha tugunlar namoyish uchun yaratilgan. Tugunlar orasidagi aloqa faqat tekshiruv yo‘nalishini ko‘rsatadi.",
                    "DEMO_FRAUD_GRAPH")
                add("GRE", "GRAPH_EDGE", "CANDIDATE",
                    "Graf qirralari: vaqt va atribut mosligi",
                    "2 ta sintetik qirra ko‘rsatildi. Umumiy qurilma yoki IP egalik/aybdorlikni isbotlamaydi.",
                    "DEMO_FRAUD_GRAPH")
            }
            "TIMELINE" -> {
                add("TLN", "TIMELINE", "GENERATED",
                    "Case vaqt chizig‘i yangilandi",
                    "Event, Signal, dalillar, Cross-Match va Human Review yozuvlari vaqt tamg‘asi bo‘yicha bitta Case ID ostida jamlanadi.",
                    "DEMO_TIMELINE")
            }
            "FIN_RECOVERY" -> {
                add("REC", "RECOVERY_CASE", "GUIDANCE_ONLY",
                    "FIN-RECOVERY yo‘riqnomasi yaratildi",
                    "1) Kartani chiqargan bankning rasmiy kanaliga zudlik bilan murojaat qilish. 2) Bankdan tranzaksiyani tekshirish va mavjud bo‘lsa nizolash tartibini so‘rash. 3) Murojaat raqami va vaqtini saqlash. 4) Firibgarlik gumoni bo‘lsa vakolatli organlarga xabar berish. 5) OTP, PIN va CVVni hech kimga bermaslik. Pul qaytishi kafolatlanmaydi.",
                    "DEMO_FIN_RECOVERY")
            }
        }
        audit.put(recordJson("AUD-" + UUID.randomUUID().toString(), "AUDIT", "RECORDED",
            "$stage bosqichi bajarildi",
            "Case ${state.optString("case_id")} uchun sintetik demo yozuvi qo‘shildi.",
            "LOCAL_DEMO", now))
        prefs.edit().putString(KEY_STATE, state.toString()).apply()
        snapshot(state)
    }

    private fun seed(): JSONObject {
        val now = System.currentTimeMillis()
        val state = JSONObject()
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
        records.put(recordJson("EVT-DEMO-0001", "EVENT", "SYNTHETIC",
            "Namoyish hodisasi qayd etildi",
            "To‘lovga oid sintetik hodisa. Haqiqiy fuqaro, karta yoki bank ma’lumoti ishlatilmagan.",
            "LOCAL_DEMO", now - 300000))
        records.put(recordJson("SIG-DEMO-0001", "SIGNAL", "OBSERVATION_ONLY",
            "Qurilma va vaqt ketma-ketligi bo‘yicha tekshiruv signali",
            "Signal tekshirish indikatori; firibgarlik isboti yoki ayblov emas.",
            "SYNTHETIC_RULE_DEMO", now - 240000))
        records.put(recordJson("EVD-DEMO-0001", "EVIDENCE", "CANDIDATE",
            "Tasdiqlovchi kontekst",
            "Qurilma atributlari orasida moslik borligi haqidagi sintetik kuzatuv; mustaqil tasdiq talab etiladi.",
            "SYNTHETIC_SOURCE_A", now - 180000))
        records.put(recordJson("CEV-DEMO-0001", "COUNTER_EVIDENCE", "CANDIDATE",
            "Qarshi dalil",
            "Qurilma oilaviy yoki umumiy foydalanishda bo‘lishi mumkin; atribut mosligi shaxsni aniqlamaydi.",
            "SYNTHETIC_SOURCE_B", now - 120000))
        records.put(recordJson("UNK-DEMO-0001", "UNKNOWN", "UNRESOLVED",
            "Aniqlashtirilmagan ma’lumot",
            "Qurilma hodisa vaqtida kimning nazoratida bo‘lgani noma’lum.",
            "NOT_PROVIDED", now - 60000))
        state.getJSONArray("audit").put(recordJson(
            "AUD-SEED-0001", "AUDIT", "CREATED",
            "Sintetik demo oqimi yaratildi",
            "Bitta Event, Signal va Case ID barcha tegishli oynalarda umumiy ishlatiladi.",
            "SYSTEM_DEMO", now
        ))
        return state
    }

    private fun recordJson(
        id: String, type: String, status: String, title: String,
        details: String, source: String, timestamp: Long
    ) = JSONObject()
        .put("id", id).put("type", type).put("status", status)
        .put("title", title).put("details", details)
        .put("source", source).put("timestamp", timestamp)

    private fun snapshot(state: JSONObject): WorkflowSnapshot {
        fun readRecords(key: String): List<WorkflowRecord> {
            val array = state.optJSONArray(key) ?: JSONArray()
            return (0 until array.length()).mapNotNull { index ->
                val item = array.optJSONObject(index) ?: return@mapNotNull null
                WorkflowRecord(
                    item.optString("id"), item.optString("type"), item.optString("status"),
                    item.optString("title"), item.optString("details"), item.optString("source"),
                    item.optLong("timestamp")
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
