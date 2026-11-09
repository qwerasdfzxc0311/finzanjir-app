package uz.finzanjir.mobile

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.UUID

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

private data class WorkflowCase(
    val id: String,
    val category: String,
    val description: String,
    val status: String,
    val createdAt: Long,
    val signal: String,
    val events: List<String>,
    val correction: String = "",
    val bankRequest: String = "",
    val bankResponse: String = ""
)

private object WorkflowRepository {
    private const val PREFS = "finzanjir_workflow_demo"
    private const val KEY_CASES = "cases"

    fun load(context: Context): List<WorkflowCase> {
        val raw = context.getSharedPreferences(PREFS, Context.MODE_PRIVATE).getString(KEY_CASES, "[]") ?: "[]"
        val array = JSONArray(raw)
        return (0 until array.length()).mapNotNull { i ->
            val o = array.optJSONObject(i) ?: return@mapNotNull null
            WorkflowCase(
                id = o.optString("id"), category = o.optString("category"),
                description = o.optString("description"), status = o.optString("status"),
                createdAt = o.optLong("createdAt"), signal = o.optString("signal"),
                events = o.optJSONArray("events")?.let { a -> (0 until a.length()).map { a.optString(it) } } ?: emptyList(),
                correction = o.optString("correction"), bankRequest = o.optString("bankRequest"),
                bankResponse = o.optString("bankResponse")
            )
        }.sortedByDescending { it.createdAt }
    }

    fun save(context: Context, cases: List<WorkflowCase>) {
        val array = JSONArray()
        cases.forEach { c ->
            val events = JSONArray()
            c.events.forEach { events.put(it) }
            array.put(JSONObject().apply {
                put("id", c.id); put("category", c.category); put("description", c.description)
                put("status", c.status); put("createdAt", c.createdAt); put("signal", c.signal)
                put("events", events); put("correction", c.correction)
                put("bankRequest", c.bankRequest); put("bankResponse", c.bankResponse)
            })
        }
        context.getSharedPreferences(PREFS, Context.MODE_PRIVATE).edit().putString(KEY_CASES, array.toString()).apply()
    }

    fun create(context: Context, category: String, description: String): WorkflowCase {
        val now = System.currentTimeMillis()
        val id = "FZ-" + SimpleDateFormat("yyMMdd-HHmmss", Locale.ROOT).format(Date(now)) +
            "-" + UUID.randomUUID().toString().take(4).uppercase(Locale.ROOT)
        val signal = when {
            description.length < 30 -> "DATA_REVIEW · tavsif qisqa, qo‘shimcha kontekst kerak"
            category.contains("ruxsatsiz", true) -> "CONSENT_UNCLEAR · rozilik holati inson tomonidan tekshiriladi"
            category.contains("yo‘qolgan", true) -> "CARD_SECURITY_REVIEW · karta holati bo‘yicha bankka murojaat qilish kerak"
            else -> "INCIDENT_REPORTED · fuqaro xabari qayd etildi"
        }
        return WorkflowCase(
            id, category, description.trim(), "REVIEW_PENDING", now, signal,
            listOf(stamp(now) + " · Fuqaro murojaati qabul qilindi (demo)", stamp(now) + " · Signal yaratildi: $signal")
        ).also { save(context, listOf(it) + load(context)) }
    }

    fun update(context: Context, target: WorkflowCase) {
        val all = load(context).toMutableList()
        val index = all.indexOfFirst { it.id == target.id }
        if (index >= 0) all[index] = target else all.add(0, target)
        save(context, all)
    }

    fun stamp(time: Long = System.currentTimeMillis()): String =
        SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.ROOT).format(Date(time))
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun UnifiedWorkflowScreen() {
    val context = LocalContext.current
    var cases by remember { mutableStateOf(WorkflowRepository.load(context)) }
    var selectedId by remember { mutableStateOf(cases.firstOrNull()?.id.orEmpty()) }
    var category by remember { mutableStateOf("Shubhali tranzaksiya") }
    var report by remember { mutableStateOf("") }
    var correction by remember { mutableStateOf("") }
    var bankReply by remember { mutableStateOf("") }
    var notice by remember { mutableStateOf("Barcha yozuvlar ushbu qurilmada demo sifatida saqlanadi. Real bankka so‘rov yuborilmaydi.") }
    val selected = cases.firstOrNull { it.id == selectedId }

    fun refresh(newSelected: String? = null) {
        cases = WorkflowRepository.load(context)
        if (newSelected != null) selectedId = newSelected
    }
    fun changeCase(c: WorkflowCase, status: String, event: String, correctionText: String = c.correction,
                   request: String = c.bankRequest, response: String = c.bankResponse) {
        val updated = c.copy(status = status, events = c.events + (WorkflowRepository.stamp() + " · " + event),
            correction = correctionText, bankRequest = request, bankResponse = response)
        WorkflowRepository.update(context, updated)
        refresh(updated.id)
    }

    Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(14.dp)) {
        Text("Yagona FINZANJIR ish jarayoni", fontSize = 20.sp, fontWeight = FontWeight.Bold)
        Text("Fuqaro → signal → Case → Human Review → tuzatish yoki bank ko‘rigi → natija", fontSize = 11.sp,
            modifier = Modifier.padding(top = 4.dp, bottom = 10.dp))
        Card(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(12.dp)) {
                Text("1. Fuqaro murojaati", fontWeight = FontWeight.Bold)
                var expanded by remember { mutableStateOf(false) }
                ExposedDropdownMenuBox(expanded = expanded, onExpandedChange = { expanded = !expanded }) {
                    OutlinedTextField(value = category, onValueChange = {}, readOnly = true,
                        label = { Text("Murojaat turi") }, modifier = Modifier.fillMaxWidth().menuAnchor())
                    ExposedDropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                        listOf("Shubhali tranzaksiya", "Ruxsatsiz operatsiya", "Yo‘qolgan karta", "Aldov yoki firibgarlik", "Boshqa holat").forEach {
                            DropdownMenuItem(text = { Text(it) }, onClick = { category = it; expanded = false })
                        }
                    }
                }
                OutlinedTextField(value = report, onValueChange = { report = it }, modifier = Modifier.fillMaxWidth(),
                    label = { Text("Hodisani tushuntiring (karta raqami, CVV yoki OTP yozmang)") }, minLines = 3)
                Button(onClick = {
                    if (report.trim().length < 8) notice = "Murojaatni tushunish uchun kamida 8 ta belgi kiriting."
                    else {
                        val created = WorkflowRepository.create(context, category, report)
                        report = ""; notice = "Demo Case yaratildi: ${created.id}"
                        refresh(created.id)
                    }
                }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp)) { Text("Murojaatni qayd etish va Case ochish") }
            }
        }
        Text(notice, fontSize = 10.sp, modifier = Modifier.padding(vertical = 8.dp))
        Text("2. Case reyestri · ${cases.size} ta", fontWeight = FontWeight.Bold)
        if (cases.isEmpty()) {
            Text("Hozircha Case yo‘q. Yuqoridagi murojaat shaklidan demo Case yarating.", fontSize = 12.sp,
                modifier = Modifier.padding(vertical = 8.dp))
        } else {
            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                cases.forEach { c ->
                    Card(onClick = { selectedId = c.id }, colors = CardDefaults.cardColors(
                        containerColor = if (c.id == selectedId) MaterialTheme.colorScheme.secondaryContainer else MaterialTheme.colorScheme.surface)) {
                        Column(Modifier.padding(10.dp)) {
                            Text(c.id, fontWeight = FontWeight.Bold, fontSize = 12.sp)
                            Text(c.category + " · " + c.status, fontSize = 10.sp)
                            Text(c.description, fontSize = 11.sp, maxLines = 2)
                        }
                    }
                }
            }
        }
        selected?.let { c ->
            HorizontalDivider(Modifier.padding(vertical = 8.dp))
            Text("3. Tanlangan Case: ${c.id}", fontWeight = FontWeight.Bold)
            Text("Signal: ${c.signal}", fontSize = 11.sp)
            Text("Holat: ${c.status}", fontSize = 11.sp)
            Text("4. Human Review — inson ko‘rigi", fontWeight = FontWeight.Bold, modifier = Modifier.padding(top = 8.dp))
            Text("Mutaxassis dalil, qarshi dalil, rozilik va noma’lumlarni tekshiradi. Signal aybdorlik hukmi emas.", fontSize = 10.sp)
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                OutlinedButton(onClick = { changeCase(c, "CORRECTION_REQUIRED", "Mutaxassis qo‘shimcha ma’lumot/tuzatish so‘radi") }, modifier = Modifier.weight(1f)) {
                    Text("Tuzatish so‘rash", fontSize = 10.sp)
                }
                OutlinedButton(onClick = {
                    val request = "DEMO-REQUEST:${c.id} | ${c.category} | bank tomonidan tekshirish so‘raladi"
                    changeCase(c, "BANK_REVIEW_REQUESTED", "Mock bank so‘rovi tayyorlandi; tashqi bankka yuborilmadi", request = request)
                    notice = "Mock bank so‘rovi Case ichida qayd etildi. Haqiqiy bank API ulanmagan."
                }, modifier = Modifier.weight(1f)) { Text("Bank ko‘rigi (demo)", fontSize = 10.sp) }
            }
            if (c.status == "CORRECTION_REQUIRED") {
                OutlinedTextField(value = correction, onValueChange = { correction = it }, modifier = Modifier.fillMaxWidth(),
                    label = { Text("Tuzatish yoki qo‘shimcha ma’lumot") }, minLines = 2)
                Button(onClick = {
                    if (correction.isBlank()) notice = "Tuzatish matnini kiriting."
                    else { changeCase(c, "REVIEW_PENDING", "Fuqaro/mutaxassis tuzatish yubordi; qayta ko‘rikka qaytdi",
                        correctionText = correction); correction = ""; notice = "Case qayta Human Review navbatiga qaytdi." }
                }, modifier = Modifier.fillMaxWidth()) { Text("Tuzatishni yuborish") }
            }
            if (c.bankRequest.isNotBlank()) {
                Text("5. Mock bank adapteri", fontWeight = FontWeight.Bold, modifier = Modifier.padding(top = 7.dp))
                Text(c.bankRequest, fontSize = 10.sp)
                OutlinedTextField(value = bankReply, onValueChange = { bankReply = it }, modifier = Modifier.fillMaxWidth(),
                    label = { Text("Demo bank javobi (qo‘lda kiritiladi)") }, minLines = 2)
                Button(onClick = {
                    if (bankReply.isBlank()) notice = "Demo javob matnini kiriting."
                    else { changeCase(c, "BANK_RESPONSE_RECORDED", "Demo bank javobi qayd etildi; haqiqiy bank javobi emas",
                        response = bankReply); bankReply = ""; notice = "Demo javob Case tarixiga qo‘shildi." }
                }, modifier = Modifier.fillMaxWidth()) { Text("Demo javobni qayd etish") }
            }
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                OutlinedButton(onClick = { changeCase(c, "CLOSED", "Case inson tomonidan demo tarzda yopildi") }, modifier = Modifier.weight(1f)) {
                    Text("Case yopish", fontSize = 10.sp)
                }
                OutlinedButton(onClick = { changeCase(c, "REVIEW_PENDING", "Case qayta ko‘rib chiqishga yuborildi") }, modifier = Modifier.weight(1f)) {
                    Text("Qayta ko‘rik", fontSize = 10.sp)
                }
            }
            Text("6. Audit tarixi", fontWeight = FontWeight.Bold, modifier = Modifier.padding(top = 8.dp))
            c.events.asReversed().forEach { Text("• $it", fontSize = 9.sp, modifier = Modifier.padding(vertical = 2.dp)) }
            if (c.bankResponse.isNotBlank()) Text("Bank javobi (demo): ${c.bankResponse}", fontSize = 10.sp)
            if (c.correction.isNotBlank()) Text("Tuzatish: ${c.correction}", fontSize = 10.sp)
        }
        Text("Xavfsizlik chegarasi: bu lokal demo; real bank, karta, hisob yoki tranzaksiyaga ulanmaydi va hech narsani bloklamaydi.",
            fontSize = 9.sp, modifier = Modifier.padding(top = 8.dp))
    }
}
