package uz.finzanjir.mobile

import android.content.Context
import android.os.Bundle
import android.util.Base64
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import javax.crypto.SecretKeyFactory
import javax.crypto.spec.PBEKeySpec
import java.security.SecureRandom

private val Navy = Color(0xFF10243D)
private val Blue = Color(0xFF2878C8)
private val Teal = Color(0xFF168C87)
private val Canvas = Color(0xFFF3F6FA)
private val Ink = Color(0xFF1D2D42)
private val Muted = Color(0xFF65758B)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { FinzanjirApp(this) }
    }
}

@Composable
private fun FinzanjirApp(context: Context) {
    val prefs = remember { context.getSharedPreferences("owner_access", Context.MODE_PRIVATE) }
    var unlocked by remember { mutableStateOf(false) }
    var hasPin by remember { mutableStateOf(prefs.contains("hash")) }
    var page by remember { mutableStateOf("Bosh sahifa") }
    var pin by remember { mutableStateOf("") }
    var confirm by remember { mutableStateOf("") }
    var error by remember { mutableStateOf("") }
    MaterialTheme(colorScheme = lightColorScheme(primary = Navy, secondary = Teal, background = Canvas, surface = Color.White)) {
        Surface(Modifier.fillMaxSize(), color = Canvas) {
            if (!unlocked) {
                OwnerGate(hasPin, pin, confirm, error, { pin = it; error = "" }, { confirm = it; error = "" }) {
                    if (pin.length < 8) error = "Kamida 8 belgili parol kiriting."
                    else if (!hasPin && pin != confirm) error = "Parollar mos kelmadi."
                    else if (!hasPin) {
                        val salt = ByteArray(16).also { SecureRandom().nextBytes(it) }
                        prefs.edit().putString("salt", Base64.encodeToString(salt, Base64.NO_WRAP))
                            .putString("hash", Base64.encodeToString(hashPin(pin, salt), Base64.NO_WRAP)).apply()
                        hasPin = true; unlocked = true; pin = ""; confirm = ""
                    } else {
                        val salt = Base64.decode(prefs.getString("salt", ""), Base64.DEFAULT)
                        val expected = Base64.decode(prefs.getString("hash", ""), Base64.DEFAULT)
                        if (hashPin(pin, salt).contentEquals(expected)) unlocked = true else error = "Parol noto‘g‘ri."
                        pin = ""
                    }
                }
            } else {
                MainScreen(page, { page = it }, { unlocked = false })
            }
        }
    }
}

private fun hashPin(pin: String, salt: ByteArray): ByteArray {
    val spec = PBEKeySpec(pin.toCharArray(), salt, 120000, 256)
    return SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256").generateSecret(spec).encoded
}

@Composable
private fun OwnerGate(hasPin: Boolean, pin: String, confirm: String, error: String,
                      onPin: (String) -> Unit, onConfirm: (String) -> Unit, submit: () -> Unit) {
    Column(Modifier.fillMaxSize().background(Navy).padding(26.dp), verticalArrangement = Arrangement.Center) {
        Icon(Icons.Default.Shield, null, tint = Color.White, modifier = Modifier.size(48.dp))
        Spacer(Modifier.height(18.dp))
        Text("FINZANJIR", color = Color.White, fontSize = 29.sp, fontWeight = FontWeight.ExtraBold)
        Text("Dalil. Kontekst. Inson nazorati.", color = Color(0xFFCAD8E8), fontSize = 13.sp)
        Spacer(Modifier.height(30.dp))
        Text(if (hasPin) "Muallif kirishi" else "Muallif parolini yarating", color = Color.White, fontSize = 21.sp, fontWeight = FontWeight.Bold)
        Text(if (hasPin) "Muallif paneliga kirish uchun parolni kiriting." else "Bu parol ushbu qurilmadagi muallif panelini mahalliy himoya qiladi.", color = Color(0xFFCAD8E8), fontSize = 12.sp, modifier = Modifier.padding(top = 7.dp, bottom = 16.dp))
        OutlinedTextField(pin, onPin, label = { Text("Parol") }, singleLine = true, visualTransformation = PasswordVisualTransformation(), keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password), modifier = Modifier.fillMaxWidth())
        if (!hasPin) {
            Spacer(Modifier.height(9.dp))
            OutlinedTextField(confirm, onConfirm, label = { Text("Parolni takrorlang") }, singleLine = true, visualTransformation = PasswordVisualTransformation(), keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password), modifier = Modifier.fillMaxWidth())
        }
        if (error.isNotBlank()) Text(error, color = Color(0xFFFFC1B8), modifier = Modifier.padding(top = 9.dp))
        Spacer(Modifier.height(18.dp))
        Button(submit, modifier = Modifier.fillMaxWidth().height(52.dp)) { Text(if (hasPin) "Kirish" else "Parolni saqlash") }
        Text("Mahalliy prototip himoyasi; production SSO/RBAC emas.", color = Color(0xFF9EB1C6), fontSize = 10.sp, modifier = Modifier.padding(top = 15.dp))
    }
}

@Composable
private fun MainScreen(page: String, select: (String) -> Unit, lock: () -> Unit) {
    val nav = listOf("Bosh sahifa", "Jarayon", "Signallar", "16 qatlam", "Case", "Human Review", "AI yordamchi", "Cheklovlar")
    Scaffold(
        topBar = {
            TopAppBar(title = { Column {
                Text("FINZANJIR", color = Navy, fontWeight = FontWeight.ExtraBold, fontSize = 18.sp)
                Text("Muallif ish maydoni · Android prototip", color = Muted, fontSize = 10.sp)
            } }, actions = { IconButton(onClick = lock) { Icon(Icons.Default.Lock, "Qulflash", tint = Navy) } },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Canvas))
        },
        bottomBar = {
            NavigationBar(containerColor = Color.White) {
                val bottom = listOf("Bosh sahifa", "Jarayon", "Signallar", "16 qatlam")
                bottom.forEachIndexed { i, label ->
                    NavigationBarItem(selected = page == label, onClick = { select(label) },
                        icon = { Icon(listOf(Icons.Default.Dashboard, Icons.Default.AccountTree, Icons.Default.Bolt, Icons.Default.Layers)[i], null) },
                        label = { Text(listOf("Bosh", "Jarayon", "Signal", "Qatlam")[i], fontSize = 9.sp) })
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
                    "Manba / bank adapteri — hozircha sintetik",
                    "Hodisa qabul qilinadi — ID, vaqt, sxema",
                    "Ma’lumot sifati — missing, eskirish, zidlik",
                    "16 qatlam tahlili — katalog asosida",
                    "Signal + dalil + qarshi dalil + unknown",
                    "Case mezonlari — bitta indikator yetarli emas",
                    "Case → Human Review → Audit izi"
                ))
                "Signallar" -> InfoList("Signal reyestri", "Signal aybdorlik hukmi yoki yakuniy dalil emas", listOf(
                    "SIG-DEMO-001 · Qurilma atributi mosligi · kontekst talab qiladi",
                    "SIG-DEMO-002 · Vaqt ketma-ketligi noodatiy · qayta tekshiruv",
                    "SIG-DEMO-003 · Rozilik doirasi noaniq · unknown",
                    "SIG-DEMO-004 · Manba ma’lumoti to‘liq emas · DATA_REVIEW"
                ))
                "16 qatlam" -> InfoList("16 qatlam katalogi", "Katalog mavjudligi implementatsiya qilinganini anglatmaydi", listOf(
                    "L01 Evidence & Data Provenance","L02 Data Quality & Reliability","L03 Risk & Uncertainty",
                    "L04 Human Oversight & Correction","L05 Rule & Model Governance","L06 Data Disclosure & Sharing Control",
                    "L07 Automation Safety & Control","L08 Transaction Chain & Case Correlation",
                    "L09 Citizen Transparency & Appeal","L10 Privacy & Data Lifecycle","L11 Security Incident Response",
                    "L12 Knowledge Governance & AI Reliability","L13 Cross-Bank Signal Exchange",
                    "L14 Fraud Typology & Consent Scope","L15 Case Lifecycle & Auditability","L16 Testing & Performance Validation"
                ))
                "Case" -> InfoList("Case markazi", "Faqat sintetik namuna; bank Case emas", listOf(
                    "CASE-DEMO-001 · CASE_CANDIDATE",
                    "Rozilik: qurilma / hisob / aniq o‘tkazma alohida tekshiriladi",
                    "Unknown: qurilma kimning nazoratida bo‘lgan?",
                    "Unknown: o‘tkazma aniq tasdiqlanganmi?",
                    "Unknown: manba dalillari o‘zaro mosmi?"
                ))
                "Human Review" -> InfoList("Human Review", "Yakuniy qaror inson vakolatida", listOf(
                    "Dalillarni manba, vaqt va ishonchlilik bo‘yicha tekshirish",
                    "Rozilik doirasini alohida aniqlash",
                    "Noma’lum va qarama-qarshi jihatlarni ko‘rib chiqish",
                    "Natija: tasdiqlash / rad etish / qo‘shimcha ma’lumot / qayta tekshiruv"
                ))
                "AI yordamchi" -> InfoList("FINZANJIR AI", "AI serveri hali Android ilovaga ulanmagan", listOf(
                    "Reja: savol → ichki bilim qidiruvi → manba/versiya/maqom → AI → manbali javob",
                    "Gemini kaliti APK ichiga joylanmaydi; xavfsiz server tomonda saqlanishi kerak",
                    "AI javobi rasmiy ekspert yoki bank qarori emas"
                ))
                else -> InfoList("Cheklovlar", "Prototipning mavjud bo‘lmagan imkoniyatlari bor deb ko‘rsatilmaydi", listOf(
                    "Bank API yoki haqiqiy bank ma’lumotlari ulanmagan",
                    "Barcha namoyish ma’lumotlari sintetik",
                    "FINZANJIR karta, hisob yoki tranzaksiyani avtomatik bloklamaydi",
                    "Signal va Case aybdorlik hukmi emas",
                    "16 qatlam katalogi to‘liq implementatsiya yoki ekspert tasdig‘i emas",
                    "Mahalliy parol production autentifikatsiya tizimi emas"
                ))
            }
        }
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
        Text("Sintetik namoyish. Real bank aniqligi yoki production tayyorligini isbotlamaydi.", color = Muted, fontSize = 10.sp, modifier = Modifier.padding(top = 10.dp))
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
            itemsIndexed(rows) { i, row ->
                Card(shape = RoundedCornerShape(14.dp), colors = CardDefaults.cardColors(containerColor = Color.White)) {
                    Row(Modifier.fillMaxWidth().padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
                        Box(Modifier.size(26.dp).background(Color(0xFFEAF2FA), CircleShape), Alignment.Center) {
                            Text(if (title == "16 qatlam katalogi") "L%02d".format(i+1) else (i+1).toString(), color = Blue, fontWeight = FontWeight.Bold, fontSize = 9.sp)
                        }
                        Text(row, color = Ink, fontSize = 12.sp, modifier = Modifier.padding(start = 11.dp).weight(1f))
                    }
                }
            }
        }
    }
}
