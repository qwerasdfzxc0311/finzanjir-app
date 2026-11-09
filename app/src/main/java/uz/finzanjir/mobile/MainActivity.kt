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
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

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
    val nav = listOf("Bosh sahifa", "Jarayon", "Signallar", "16 qatlam", "Case", "Human Review", "AI yordamchi", "Cheklovlar")
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
            if (page !in nav.take(4)) {
                ScrollableTabRow(selectedTabIndex = nav.indexOf(page).coerceAtLeast(0), edgePadding = 12.dp) {
                    nav.forEach { Tab(page == it, { select(it) }, text = { Text(it, fontSize = 10.sp) }) }
                }
            }
            when (page) {
                "Bosh sahifa" -> Home { select("Jarayon") }
                "Jarayon" -> InfoList("Yagona ish jarayoni", "Hodisadan inson ko‘rigigacha", listOf(
                    "1. Hodisa va manba — hozircha namoyish ma’lumotlari sintetik",
                    "2. Ma’lumot sifati — yetishmayotgan, eskirgan yoki zid ma’lumotlarni belgilash",
                    "3. 16 qatlam — tegishli talab va nazorat yo‘nalishlarini ko‘rib chiqish",
                    "4. Signal — kuzatuvni qayd etish; signal aybdorlik hukmi emas",
                    "5. Dalil va qarshi dalil — tasdiqlovchi hamda rad etuvchi ma’lumotlar",
                    "6. Rozilik doirasi — qurilma, hisob va aniq o‘tkazma roziligini ajratish",
                    "7. Case mezonlari — yetarli asos bo‘lsa tekshiruv ishini shakllantirish",
                    "8. Human Review — vakolatli inson tekshiradi va natijani qayd etadi",
                    "9. Audit izi — kim, qachon, qaysi manbaga tayanganini saqlash"
                ))
                "Signallar" -> InfoList("Signal reyestri", "Signal — tekshirish indikatori, yakuniy xulosa emas", listOf(
                    "SIG-DEMO-001 · Qurilma atributi mosligi · kontekst talab qiladi",
                    "SIG-DEMO-002 · Vaqt ketma-ketligi noodatiy · qayta tekshiruv",
                    "SIG-DEMO-003 · Rozilik doirasi noaniq · UNKNOWN",
                    "SIG-DEMO-004 · Manba ma’lumoti to‘liq emas · DATA_REVIEW",
                    "Har bir signal uchun manba, vaqt, ishonchlilik, tasdiqlash/rad etish munosabati va noma’lumlar talab qilinadi"
                ))
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
                    "L13 Cross-Bank Signal Exchange — banklararo signal almashish",
                    "L14 Fraud Typology & Consent Scope — firibgarlik turi va rozilik doirasi",
                    "L15 Case Lifecycle & Auditability — Case hayot sikli va audit",
                    "L16 Testing & Performance Validation — sinov va samaradorlikni tekshirish"
                ))
                "Case" -> InfoList("Case markazi", "Sintetik namuna; real bank Case emas", listOf(
                    "CASE-DEMO-001 · CASE_CANDIDATE",
                    "Tasdiqlovchi dalillar: hali namoyish uchun to‘liq manbali dalil ulanmagan",
                    "Qarshi dalillar: alohida qayd etilishi shart",
                    "Rozilik: qurilma / hisob / aniq o‘tkazma alohida tekshiriladi",
                    "Unknown: qurilma kimning nazoratida bo‘lgan?",
                    "Unknown: o‘tkazma aynan qaysi usulda tasdiqlangan?",
                    "Case ochilishi firibgarlik tasdiqlandi degani emas"
                ))
                "Human Review" -> InfoList("Human Review", "Yakuniy qaror vakolatli insonda qoladi", listOf(
                    "Dalillarni manba, vaqt va ishonchlilik bo‘yicha tekshirish",
                    "Rozilik doirasini alohida aniqlash",
                    "Qarshi dalillar va muqobil izohlarni ko‘rib chiqish",
                    "Noma’lum yoki yetishmayotgan ma’lumotlarni qayd etish",
                    "Natija: tasdiqlash / rad etish / qo‘shimcha ma’lumot / qayta tekshiruv",
                    "AI tavsiyasi rasmiy qaror o‘rnini bosmaydi"
                ))
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
private fun KnowledgeAssistant() {
    var question by remember { mutableStateOf("") }
    var answer by remember { mutableStateOf<KnowledgeAnswer?>(null) }
    Column(Modifier.fillMaxSize().padding(16.dp)) {
        Text("FINZANJIR AI · bilim yordamchisi", color = Navy, fontSize = 20.sp, fontWeight = FontWeight.ExtraBold)
        Text("Savol bering. Yordamchi ichki bilim yozuvlaridan mos tushunchalarni topib, sodda izoh va manbani ko‘rsatadi.", color = Muted, fontSize = 12.sp, modifier = Modifier.padding(top = 5.dp, bottom = 12.dp))
        OutlinedTextField(value = question, onValueChange = { question = it }, modifier = Modifier.fillMaxWidth(),
            label = { Text("Masalan: Case nima va qachon ochiladi?") }, minLines = 2)
        Button(onClick = { answer = FinzanjirKnowledgeBase.search(question) }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp)) {
            Icon(Icons.Default.Search, null); Spacer(Modifier.width(7.dp)); Text("Bilimlardan izlash")
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
        Text("Bilimlar bazasi: ${FinzanjirKnowledgeBase.VERSION} · ${FinzanjirKnowledgeBase.entries.size} ta strukturali yozuv", color = Muted, fontSize = 10.sp)
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
