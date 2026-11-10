package uz.finzanjir.mobile

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.runtime.rememberCoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

private val Navy = Color(0xFF10243D)
private val Blue = Color(0xFF2878C8)
private val Teal = Color(0xFF168C87)
private val Canvas = Color(0xFFF3F6FA)
private val Ink = Color(0xFF1D2D42)
private val Muted = Color(0xFF65758B)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { FinzanjirApp() }
    }
}

@Composable
private fun FinzanjirApp() {
    var page by remember { mutableStateOf("Bosh sahifa") }
    MaterialTheme(colorScheme = lightColorScheme(primary = Navy, secondary = Teal, background = Canvas, surface = Color.White)) {
        Surface(Modifier.fillMaxSize(), color = Canvas) {
            MainScreen(page, { page = it })
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun MainScreen(page: String, select: (String) -> Unit) {
    val nav = listOf("Bosh sahifa", "Jarayon", "Signallar", "Risk Engine", "Cross-Match", "Fraud Graph", "Timeline", "Case", "Human Review", "FIN-RECOVERY", "Fuqaro oynasi", "Mutaxassis ish joyi", "16 qatlam", "AI yordamchi", "Cheklovlar")
    Scaffold(
        topBar = {
            TopAppBar(title = { Column {
                Text("FINZANJIR", color = Navy, fontWeight = FontWeight.ExtraBold, fontSize = 18.sp)
                Text("Ochiq mutaxassislar prototipi · v1", color = Muted, fontSize = 10.sp)
            } }, colors = TopAppBarDefaults.topAppBarColors(containerColor = Canvas))
        },
        bottomBar = {
            NavigationBar(containerColor = Color.White) {
                val bottom = listOf("Bosh sahifa", "Jarayon", "Signallar", "AI yordamchi")
                bottom.forEachIndexed { i, label ->
                    NavigationBarItem(selected = page == label, onClick = { select(label) },
                        icon = { Icon(listOf(Icons.Default.Dashboard, Icons.Default.AccountTree, Icons.Default.Bolt, Icons.Default.Psychology)[i], null) },
                        label = { Text(listOf("Bosh", "Jarayon", "Signal", "AI")[i], fontSize = 9.sp) })
                }
            }
        }, containerColor = Canvas
    ) { padding ->
        Column(Modifier.fillMaxSize().padding(padding)) {
            ScrollableTabRow(selectedTabIndex = nav.indexOf(page).coerceAtLeast(0), edgePadding = 12.dp) {
                nav.forEach { Tab(page == it, { select(it) }, text = { Text(it, fontSize = 10.sp) }) }
            }
            when (page) {
                "Bosh sahifa" -> Home { select("Jarayon") }
                "Jarayon" -> WorkflowPanel("Jarayon")
                "Signallar" -> WorkflowPanel("Signallar")
                "16 qatlam" -> InfoList("16 qatlam katalogi", "Katalog ko‘rsatilishi to‘liq implementatsiya degani emas", listOf(
                    "L01 Evidence & Data Provenance — dalil kelib chiqishi va manba izi",
                    "L02 Data Quality & Reliability — ma’lumot sifati va ishonchliligi",
                    "L03 Risk & Uncertainty — xavf va noaniqlikni baholash",
                    "L04 Human Oversight & Correction — inson nazorati va tuzatish",
                    "L05 Rule & Model Governance — qoida va model boshqaruvi",
                    "L06 Data Disclosure & Sharing Control — ma’lumotni oshkor qilish/almashish nazorati",
                    "L07 Automation Safety & Control — avtomatlashtirish xavfsizligi",
                    "L08 Transaction Chain & Case Correlation — tranzaksiya zanjiri va Case bog‘lanishi",
                    "L09 Citizen Transparency & Appeal — fuqaro shaffofligi va e’tiroz",
                    "L10 Privacy & Data Lifecycle — maxfiylik va ma’lumot hayot sikli",
                    "L11 Security Incident Response — xavfsizlik hodisasiga javob",
                    "L12 Knowledge Governance & AI Reliability — bilim boshqaruvi va AI ishonchliligi",
                    "L13 Testing & Independent Evaluation — sinov va mustaqil baholash",
                    "L14 Bank Integration Readiness — bank integratsiyasiga tayyorlik",
                    "L15 Performance & Capacity Management — samaradorlik va quvvatni boshqarish",
                    "L16 Impact & Harm Reduction — ta’sir va zarar kamayishini o‘lchash"
                ))
                "Case" -> WorkflowPanel("Case")
                "Human Review" -> WorkflowPanel("Human Review")
                "Risk Engine", "Cross-Match", "Fraud Graph", "Timeline", "FIN-RECOVERY", "Fuqaro oynasi", "Mutaxassis ish joyi" -> PlatformPanel(page)
                "AI yordamchi" -> KnowledgeAssistant()
                else -> InfoList("Prototip cheklovlari", "Mavjud bo‘lmagan imkoniyatlar bor deb ko‘rsatilmaydi", listOf(
                    "Bank API yoki haqiqiy bank ma’lumotlari ulanmagan",
                    "Namoyish signallari va Case sintetik",
                    "FINZANJIR karta, hisob yoki tranzaksiyani avtomatik bloklamaydi",
                    "Signal va Case aybdorlik hukmi emas",
                    "16 qatlam katalogi to‘liq implementatsiya yoki ekspert tasdig‘i emas",
                    "AI bilim mexanizmi hozircha lokal prototip yozuvlari bilan ishlaydi; to‘liq arxiv importi alohida bajariladi",
                    "Production xavfsizlik, server RBAC, audit va bank integratsiyalari hali sinovdan o‘tmagan"
                ))
            }
        }
    }
}

@Composable
private fun WorkflowPanel(page: String) {
    val context = LocalContext.current
    var snapshot by remember(page) { mutableStateOf(WorkflowStore.load(context)) }
    var reason by remember { mutableStateOf("") }
    var actionError by remember { mutableStateOf<String?>(null) }

    Column(Modifier.fillMaxSize().padding(16.dp)) {
        Text(
            when (page) {
                "Jarayon" -> "Yagona FINZANJIR ish oqimi"
                "Signallar" -> "Signal reyestri"
                "Case" -> "Case markazi"
                else -> "Human Review"
            },
            color = Navy, fontSize = 20.sp, fontWeight = FontWeight.ExtraBold
        )
        Text(
            "Barcha tegishli oynalar bitta sintetik Event / Signal / Case zanjiridan foydalanadi. Demo ma’lumotlari real bank yozuvi emas.",
            color = Muted, fontSize = 11.sp, modifier = Modifier.padding(top = 5.dp, bottom = 10.dp)
        )
        Card(colors = CardDefaults.cardColors(containerColor = Color.White)) {
            Column(Modifier.fillMaxWidth().padding(12.dp)) {
                Text("Event ID: ${snapshot.eventId}", color = Ink, fontSize = 11.sp)
                Text("Signal ID: ${snapshot.signalId}", color = Ink, fontSize = 11.sp)
                Text("Case ID: ${snapshot.caseId}", color = Ink, fontSize = 11.sp)
                Text("Case holati: ${snapshot.caseStatus}", color = Blue, fontSize = 12.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(top = 5.dp))
                Text("Review holati: ${snapshot.reviewStatus}", color = Muted, fontSize = 10.sp)
            }
        }

        when (page) {
            "Jarayon" -> {
                Text("Event → Signal → Case → Human Review → Audit", color = Navy, fontWeight = FontWeight.Bold, fontSize = 12.sp, modifier = Modifier.padding(top = 13.dp, bottom = 7.dp))
                snapshot.records.forEach { WorkflowRecordCard(it) }
            }
            "Signallar" -> {
                Text("Signal — tekshiruv indikatori, ayblov yoki firibgarlik isboti emas.", color = Muted, fontSize = 11.sp, modifier = Modifier.padding(vertical = 8.dp))
                snapshot.records.filter { it.type == "SIGNAL" }.forEach { WorkflowRecordCard(it) }
            }
            "Case" -> {
                Text("Dalillar, qarshi dalillar va noma’lumlar bir Case ID ostida saqlanadi.", color = Muted, fontSize = 11.sp, modifier = Modifier.padding(vertical = 8.dp))
                snapshot.records.filter { it.type in setOf("EVIDENCE", "COUNTER_EVIDENCE", "UNKNOWN", "HUMAN_REVIEW") }.forEach { WorkflowRecordCard(it) }
            }
            "Human Review" -> {
                Text("AI yoki signal yakuniy qaror chiqarmaydi. Quyidagi demo amallar faqat review holatini va audit yozuvini o‘zgartiradi.", color = Muted, fontSize = 11.sp, modifier = Modifier.padding(vertical = 8.dp))
                snapshot.records.filter { it.type in setOf("EVIDENCE", "COUNTER_EVIDENCE", "UNKNOWN", "HUMAN_REVIEW") }.forEach { WorkflowRecordCard(it) }
                OutlinedTextField(
                    value = reason, onValueChange = { reason = it },
                    modifier = Modifier.fillMaxWidth().padding(top = 8.dp),
                    label = { Text("Ko‘rib chiqish sababi") }, minLines = 2
                )
                val decisions = listOf(
                    "SUPPORTED_FOR_FURTHER_CHECK" to "Tekshiruvni davom ettirish",
                    "NOT_SUPPORTED" to "Asos yetarli emas",
                    "MORE_INFORMATION" to "Qo‘shimcha ma’lumot",
                    "RECHECK" to "Qayta tekshirish",
                    "ESCALATED" to "Vakolatli mutaxassisga yuborish"
                )
                decisions.forEach { (code, label) ->
                    OutlinedButton(
                        onClick = {
                            try {
                                snapshot = WorkflowStore.recordReview(context, code, reason)
                                reason = ""
                                actionError = null
                            } catch (e: Exception) {
                                actionError = e.message ?: "Review amalini saqlab bo‘lmadi"
                            }
                        },
                        enabled = reason.trim().length >= 4,
                        modifier = Modifier.fillMaxWidth().padding(top = 5.dp)
                    ) { Text(label) }
                }
                actionError?.let { Text(it, color = Color(0xFFB3261E), fontSize = 11.sp, modifier = Modifier.padding(top = 6.dp)) }
            }
        }

        Text("Audit izi · oxirgi yozuvlar", color = Navy, fontWeight = FontWeight.Bold, fontSize = 13.sp, modifier = Modifier.padding(top = 13.dp, bottom = 6.dp))
        snapshot.audit.takeLast(8).reversed().forEach { WorkflowRecordCard(it) }
        Text("Prototip cheklovi: bu lokal SharedPreferences demo ombori; production DB, server RBAC, bank API yoki huquqiy qaror emas.", color = Muted, fontSize = 10.sp, modifier = Modifier.padding(top = 8.dp))
    }
}

@Composable
private fun WorkflowRecordCard(record: WorkflowRecord) {
    Card(
        Modifier.fillMaxWidth().padding(vertical = 3.dp),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White)
    ) {
        Column(Modifier.padding(11.dp)) {
            Text("${record.type} · ${record.status}", color = Blue, fontSize = 9.sp, fontWeight = FontWeight.Bold)
            Text(record.title, color = Ink, fontSize = 12.sp, fontWeight = FontWeight.SemiBold, modifier = Modifier.padding(top = 3.dp))
            Text(record.details, color = Muted, fontSize = 11.sp, lineHeight = 15.sp, modifier = Modifier.padding(top = 3.dp))
            Text("ID: ${record.id} · Manba: ${record.source}", color = Muted, fontSize = 9.sp, modifier = Modifier.padding(top = 4.dp))
        }
    }
}

@Composable
private fun PlatformPanel(page: String) {
    val context = LocalContext.current
    var snapshot by remember(page) { mutableStateOf(WorkflowStore.load(context)) }
    var message by remember { mutableStateOf<String?>(null) }
    val stage = when (page) {
        "Risk Engine" -> "RISK_ENGINE"
        "Cross-Match" -> "CROSS_MATCH"
        "Fraud Graph" -> "FRAUD_GRAPH"
        "Timeline" -> "TIMELINE"
        "FIN-RECOVERY" -> "FIN_RECOVERY"
        else -> ""
    }
    val citizen = page == "Fuqaro oynasi"
    val expert = page == "Mutaxassis ish joyi"

    LazyColumn(Modifier.fillMaxSize().padding(horizontal = 16.dp), contentPadding = PaddingValues(top = 14.dp, bottom = 20.dp)) {
        item {
            Text(page, color = Navy, fontSize = 21.sp, fontWeight = FontWeight.ExtraBold)
            Text("Yagona ma’lumot zanjiri · Event / Signal / Case ID", color = Muted, fontSize = 11.sp, modifier = Modifier.padding(top = 4.dp, bottom = 10.dp))
            Card(colors = CardDefaults.cardColors(containerColor = Color.White)) {
                Column(Modifier.fillMaxWidth().padding(12.dp)) {
                    Text("Event: ${snapshot.eventId}", color = Ink, fontSize = 11.sp)
                    Text("Signal: ${snapshot.signalId}", color = Ink, fontSize = 11.sp)
                    Text("Case: ${snapshot.caseId}", color = Ink, fontSize = 11.sp)
                    Text("Case holati: ${snapshot.caseStatus}", color = Blue, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    Text("Review: ${snapshot.reviewStatus}", color = Muted, fontSize = 10.sp)
                }
            }
            Spacer(Modifier.height(10.dp))
        }
        if (citizen) {
            item {
                Text("Fuqaro uchun tushunarli ko‘rinish", color = Navy, fontWeight = FontWeight.Bold, fontSize = 15.sp)
                Text("FINZANJIR shubhali belgilarni ko‘rsatishi mumkin, lekin bu sizni firibgar yoki aybdor deb belgilamaydi. Yakuniy ko‘rib chiqish vakolatli inson tomonidan amalga oshiriladi.", color = Ink, fontSize = 12.sp, lineHeight = 18.sp, modifier = Modifier.padding(vertical = 8.dp))
                listOf(
                    "Mening kartalarim — o‘zimniki, tanimayman yoki yo‘qotilgan holatlarini qayd etish uchun mo‘ljallangan; hozircha bank bilan real sinxronlash yo‘q.",
                    "Xavfsizlik — OTP, PIN, CVV va parollarni hech kimga bermang; shubhali havolalarga kirmang.",
                    "Murojaat — hodisa yuz bersa bankning rasmiy aloqa kanaliga murojaat qiling va murojaat raqamini saqlang.",
                    "Shaffoflik — signalning sababi va noaniqliklari tushuntirilishi kerak; noto‘g‘ri ma’lumotni tuzatish inson ko‘rigi orqali amalga oshiriladi."
                ).forEach { line ->
                    Card(Modifier.fillMaxWidth().padding(vertical = 4.dp), colors = CardDefaults.cardColors(containerColor = Color.White)) {
                        Text(line, color = Ink, fontSize = 12.sp, lineHeight = 17.sp, modifier = Modifier.padding(12.dp))
                    }
                }
                Text("Bu fuqaro interfeysining birinchi demo ko‘rinishi. Karta ro‘yxati, e’tiroz yuborish va bankdan ma’lumot olish hali real xizmat sifatida ulanmagan.", color = Muted, fontSize = 10.sp, modifier = Modifier.padding(top = 8.dp))
            }
        } else if (expert) {
            item {
                Text("Mutaxassis ish joyi", color = Navy, fontWeight = FontWeight.Bold, fontSize = 15.sp)
                Text("Barcha mutaxassis oynalari bitta Case ID, umumiy vaqt chizig‘i va audit yozuvlariga tayanadi. Ushbu demo autentifikatsiya yoki production RBAC emas.", color = Muted, fontSize = 11.sp, modifier = Modifier.padding(vertical = 7.dp))
                val actions = listOf(
                    "RISK_ENGINE" to "Risk Engine ishga tushirish",
                    "CROSS_MATCH" to "Cross-Match bajarish",
                    "FRAUD_GRAPH" to "Fraud Graph tuzish",
                    "TIMELINE" to "Timeline yangilash",
                    "FIN_RECOVERY" to "FIN-RECOVERY yo‘riqnomasi"
                )
                actions.forEach { (code, label) ->
                    OutlinedButton(onClick = {
                        snapshot = WorkflowStore.runStage(context, code)
                        message = "$label: demo natijasi Case tarixiga yozildi."
                    }, modifier = Modifier.fillMaxWidth().padding(vertical = 3.dp)) { Text(label) }
                }
                message?.let { Text(it, color = Teal, fontSize = 10.sp, modifier = Modifier.padding(vertical = 6.dp)) }
                Text("Yagona Case yozuvlari", color = Navy, fontWeight = FontWeight.Bold, modifier = Modifier.padding(top = 10.dp, bottom = 5.dp))
            }
            items(snapshot.records.reversed()) { WorkflowRecordCard(it) }
            item {
                Text("Audit izi", color = Navy, fontWeight = FontWeight.Bold, modifier = Modifier.padding(top = 10.dp, bottom = 5.dp))
            }
            items(snapshot.audit.reversed()) { WorkflowRecordCard(it) }
        } else {
            item {
                val description = when (stage) {
                    "RISK_ENGINE" -> "Risk Engine: izohlanadigan risk omillari, qarshi kontekst va noaniqlikni ko‘rsatadi. Ball hozir sintetik demo; kalibrlanmagan."
                    "CROSS_MATCH" -> "Cross-Match: turli manbalardagi atributlar o‘rtasida ehtimoliy mosliklarni izlaydi. Moslik shaxsni aniqlash yoki ayblash emas."
                    "FRAUD_GRAPH" -> "Fraud Graph: fuqaro, kanal, karta, hisob, telefon, qurilma/IP, qabul qiluvchi va tranzaksiya aloqalarini ko‘rsatish uchun graf yozuvlarini yaratadi."
                    "TIMELINE" -> "Timeline: hodisa, signal, dalil, qarshi dalil, review va recovery harakatlarini yagona Case ID bo‘yicha vaqt tartibida jamlaydi."
                    else -> "FIN-RECOVERY: hodisadan keyingi xavfsiz amallarni eslatadi va murojaat izini saqlashga yordam beradi. Pul qaytishini kafolatlamaydi."
                }
                Text(description, color = Ink, fontSize = 12.sp, lineHeight = 18.sp, modifier = Modifier.padding(vertical = 7.dp))
                Button(onClick = {
                    snapshot = WorkflowStore.runStage(context, stage)
                    message = "Demo bosqichi bajarildi va umumiy Case tarixiga yozildi."
                }, modifier = Modifier.fillMaxWidth()) { Text("Demo bosqichini bajarish") }
                message?.let { Text(it, color = Teal, fontSize = 10.sp, modifier = Modifier.padding(top = 6.dp)) }
                Text("Shu bosqichga tegishli yozuvlar", color = Navy, fontWeight = FontWeight.Bold, modifier = Modifier.padding(top = 12.dp, bottom = 5.dp))
            }
            val types = when (stage) {
                "RISK_ENGINE" -> setOf("RISK_ASSESSMENT")
                "CROSS_MATCH" -> setOf("CROSS_MATCH", "UNKNOWN")
                "FRAUD_GRAPH" -> setOf("GRAPH_NODE", "GRAPH_EDGE")
                "TIMELINE" -> setOf("TIMELINE")
                else -> setOf("RECOVERY_CASE")
            }
            items(snapshot.records.filter { it.type in types }.reversed()) { WorkflowRecordCard(it) }
            if (stage == "TIMELINE") {
                item { Text("To‘liq vaqt chizig‘i", color = Navy, fontWeight = FontWeight.Bold, modifier = Modifier.padding(top = 10.dp, bottom = 5.dp)) }
                items(snapshot.records.sortedBy { it.timestamp }) { WorkflowRecordCard(it) }
            }
            if (stage == "FIN_RECOVERY") {
                item { Text("FIN-RECOVERY xavfsizlik yo‘riqnomasi", color = Navy, fontWeight = FontWeight.Bold, modifier = Modifier.padding(top = 10.dp)) }
            }
        }
        item {
            Text("Cheklov: bu lokal sintetik demo. Haqiqiy bank ma’lumoti, real shaxslararo bog‘lanish, production Risk Score, avtomatik bloklash yoki pulni qaytarish amali bajarilmaydi.", color = Muted, fontSize = 10.sp, lineHeight = 14.sp, modifier = Modifier.padding(top = 12.dp))
        }
    }
}

@Composable
private fun KnowledgeAssistant() {
    val context = LocalContext.current
    var question by remember { mutableStateOf("") }
    var answer by remember { mutableStateOf<KnowledgeAnswer?>(null) }
    var expertMode by remember { mutableStateOf(false) }
    var loading by remember { mutableStateOf(false) }
    var loadedCount by remember { mutableStateOf<Int?>(null) }
    var loadError by remember { mutableStateOf<String?>(null) }
    val scope = rememberCoroutineScope()
    LaunchedEffect(Unit) {
        loading = true
        try { loadedCount = withContext(Dispatchers.IO) { FinzanjirKnowledgeBase.count(context) } }
        catch (e: Exception) { loadError = e.message ?: "Bilimlar bazasini ochib bo‘lmadi" }
        finally { loading = false }
    }
    Column(Modifier.fillMaxSize().padding(16.dp)) {
        Text("FINZANJIR AI · bilim yordamchisi", color = Navy, fontSize = 20.sp, fontWeight = FontWeight.ExtraBold)
        Text("O‘zbekcha va qoraqalpoqcha savollar, oddiy yozuv xatolari va atama variantlari bilan ishlashga mo‘ljallangan. Bir nechta hujjat dalillari manbalari bilan birlashtiriladi.", color = Muted, fontSize = 12.sp, modifier = Modifier.padding(top = 5.dp, bottom = 12.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.padding(bottom = 8.dp)) {
            FilterChip(selected = !expertMode, onClick = { expertMode = false }, label = { Text("Fuqaro") })
            FilterChip(selected = expertMode, onClick = { expertMode = true }, label = { Text("Mutaxassis") })
        }
        Text(
            if (expertMode) "Mutaxassis rejimi: texnik tafsilotlar, manba versiyasi, hujjat maqomi va ehtimoliy ziddiyatlar. Bu demo ko‘rinish, autentifikatsiya emas."
            else "Fuqaro rejimi: sodda izoh, asosiy tushunchalar va xavfsizlikka oid ma’lumotlar. Texnik atamalar qisqacha tushuntiriladi.",
            color = Muted, fontSize = 10.sp, modifier = Modifier.padding(bottom = 8.dp)
        )
        OutlinedTextField(value = question, onValueChange = { question = it }, modifier = Modifier.fillMaxWidth(),
            label = { Text("Masalan: Case nima va qachon ochiladi?") }, minLines = 2)
        Button(onClick = { scope.launch {
            loading = true
            loadError = null
            try {
                val result = withContext(Dispatchers.IO) { FinzanjirKnowledgeBase.search(context, question, expertMode) }
                answer = result
                loadedCount = result.recordCount
            } catch (e: Exception) { loadError = e.message ?: "Qidiruvda xato yuz berdi" }
            finally { loading = false }
        } }, enabled = !loading && question.isNotBlank(), modifier = Modifier.fillMaxWidth().padding(top = 8.dp)) {
            Icon(Icons.Default.Search, null); Spacer(Modifier.width(7.dp)); Text(if (loading) "Bilimlar tayyorlanmoqda…" else "FINZANJIR yadrosidan javob olish")
        }
        answer?.let { result ->
            Card(Modifier.fillMaxWidth().padding(top = 14.dp), shape = RoundedCornerShape(16.dp), colors = CardDefaults.cardColors(containerColor = Color.White)) {
                Column(Modifier.padding(15.dp)) {
                    Text(result.answer, color = Ink, fontSize = 13.sp, lineHeight = 19.sp)
                    if (result.sources.isNotEmpty()) {
                        Text("Manbalar", color = Navy, fontWeight = FontWeight.Bold, modifier = Modifier.padding(top = 12.dp))
                        result.sources.forEach { Text("• $it", color = Muted, fontSize = 11.sp) }
                    }
                    Text("Holat: ${result.confidence}", color = Blue, fontSize = 10.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(top = 9.dp))
                    Text(result.notice, color = Muted, fontSize = 10.sp, modifier = Modifier.padding(top = 5.dp))
                }
            }
        }
        Spacer(Modifier.height(12.dp))
        Text("Bilimlar yadrosi: ${FinzanjirKnowledgeBase.VERSION} · " + (loadedCount?.let { "$it ta yozuv tekshirildi" } ?: "bazani tayyorlash kutilmoqda"), color = Muted, fontSize = 10.sp)
        loadError?.let { Text("Xato: $it", color = Color(0xFFB3261E), fontSize = 11.sp, modifier = Modifier.padding(top = 5.dp)) }
        Text("Bu lokal qidiruv va dalilga tayangan javob sintezi. Risk Engine, Fraud Graph, bank API va boshqa platforma imkoniyatlari loyiha rejasida ishlab chiqilishi ko‘zda tutilgan; bu ekran ularning to‘liq ishlayotganini anglatmaydi.", color = Muted, fontSize = 10.sp, modifier = Modifier.padding(top = 7.dp))
    }
}

@Composable
private fun Home(open: () -> Unit) {
    Column(Modifier.fillMaxSize().padding(18.dp)) {
        Card(shape = RoundedCornerShape(22.dp), colors = CardDefaults.cardColors(containerColor = Navy)) {
            Column(Modifier.padding(22.dp)) {
                Text("DALIL. KONTEKST. INSON NAZORATI.", color = Color(0xFF8FC7F4), fontSize = 10.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(10.dp))
                Text("Moliyaviy xavfni tizimli ko‘rib chiqish", color = Color.White, fontSize = 23.sp, fontWeight = FontWeight.ExtraBold, lineHeight = 29.sp)
                Text("FINZANJIR signallarni tartiblaydi, dalillar va noaniqliklarni ko‘rsatadi hamda inson ko‘rigini qo‘llab-quvvatlaydi.", color = Color(0xFFD7E4F2), fontSize = 13.sp, modifier = Modifier.padding(top = 9.dp))
                Surface(color = Color(0xFF1D466B), shape = CircleShape, modifier = Modifier.padding(top = 15.dp)) {
                    Text("AVTOMATIK BLOKLASH YO‘Q", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 10.sp, modifier = Modifier.padding(horizontal = 12.dp, vertical = 7.dp))
                }
            }
        }
        Spacer(Modifier.height(16.dp))
        Text("Prototip holati", color = Navy, fontWeight = FontWeight.Bold, fontSize = 17.sp)
        Row(Modifier.fillMaxWidth().padding(top = 9.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Metric("16", "qatlam", Modifier.weight(1f)); Metric("0", "bank API", Modifier.weight(1f)); Metric("DEMO", "ma’lumot", Modifier.weight(1f))
        }
        Text("Asosiy ketma-ketlik", color = Navy, fontWeight = FontWeight.Bold, fontSize = 17.sp, modifier = Modifier.padding(top = 18.dp, bottom = 8.dp))
        listOf("Hodisa va manba","Ma’lumot sifati","Signal va dalillar","Case mezonlari","Human Review","Audit izi").forEachIndexed { i, s ->
            Row(Modifier.padding(vertical = 5.dp), verticalAlignment = Alignment.CenterVertically) {
                Box(Modifier.size(26.dp).background(Color(0xFFE4EEF8), CircleShape), Alignment.Center) { Text((i+1).toString(), color = Blue, fontWeight = FontWeight.Bold, fontSize = 11.sp) }
                Text(s, color = Ink, fontSize = 13.sp, modifier = Modifier.padding(start = 11.dp))
            }
        }
        Button(open, modifier = Modifier.fillMaxWidth().padding(top = 10.dp)) { Text("Ish jarayonini ko‘rish") }
        Text("Barcha ekranlar mutaxassislar ko‘rishi uchun ochiq. Namoyish prototipi; real bank aniqligini isbotlamaydi.", color = Muted, fontSize = 10.sp, modifier = Modifier.padding(top = 10.dp))
    }
}

@Composable
private fun Metric(value: String, label: String, modifier: Modifier) {
    Card(modifier, shape = RoundedCornerShape(14.dp), colors = CardDefaults.cardColors(containerColor = Color.White)) {
        Column(Modifier.padding(12.dp)) { Text(value, color = Navy, fontWeight = FontWeight.ExtraBold, fontSize = 19.sp); Text(label, color = Muted, fontSize = 10.sp) }
    }
}

@Composable
private fun InfoList(title: String, subtitle: String, rows: List<String>) {
    Column(Modifier.fillMaxSize().padding(horizontal = 17.dp, vertical = 13.dp)) {
        Text(title, color = Navy, fontSize = 20.sp, fontWeight = FontWeight.ExtraBold)
        Text(subtitle, color = Muted, fontSize = 12.sp, modifier = Modifier.padding(top = 4.dp, bottom = 13.dp))
        LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            items(rows) { row ->
                Card(shape = RoundedCornerShape(14.dp), colors = CardDefaults.cardColors(containerColor = Color.White)) {
                    Text(row, color = Ink, fontSize = 12.sp, lineHeight = 18.sp, modifier = Modifier.fillMaxWidth().padding(14.dp))
                }
            }
        }
    }
}
