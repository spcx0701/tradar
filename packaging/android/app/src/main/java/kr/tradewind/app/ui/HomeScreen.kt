package kr.tradewind.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kr.tradewind.app.data.Market
import kr.tradewind.app.data.Repository
import kr.tradewind.app.ui.theme.*
import kotlin.math.roundToInt

/**
 * 네이티브 홈 화면(Jetpack Compose) — 관세청 데이터 기반 ‘지금 떠오르는 시장’을 네이티브로 렌더.
 * 데이터는 Repository(라이브 API → 번들 JSON 폴백)에서 온다.
 */
@Composable
fun HomeScreen(repo: Repository, onOpenWebApp: () -> Unit) {
    var markets by remember { mutableStateOf<List<Market>>(emptyList()) }
    var loading by remember { mutableStateOf(true) }
    LaunchedEffect(Unit) {
        markets = runCatching { repo.topMarkets() }.getOrDefault(emptyList())
        loading = false
    }

    Column(Modifier.fillMaxSize().background(BgLight)) {
        HeroHeader()
        Spacer(Modifier.height(8.dp))
        Button(
            onClick = onOpenWebApp,
            modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
        ) { Text("전체 웹앱 열기 (예보·AI 참모·리포트)") }
        Spacer(Modifier.height(10.dp))
        Text(
            "🌊 지금 떠오르는 한류 수출 시장",
            Modifier.padding(start = 16.dp, bottom = 6.dp),
            fontWeight = FontWeight.Bold, fontSize = 16.sp, color = Navy,
        )
        if (loading) {
            Box(Modifier.fillMaxWidth().padding(32.dp), Alignment.Center) { CircularProgressIndicator() }
        } else {
            LazyColumn(Modifier.padding(horizontal = 12.dp)) {
                items(markets) { MarketRow(it) }
            }
        }
    }
}

@Composable
private fun HeroHeader() {
    Box(
        Modifier.fillMaxWidth()
            .background(Brush.linearGradient(listOf(Navy, Blue, Teal)))
            .padding(20.dp),
    ) {
        Column {
            Text("무역풍 · Tradewind", color = androidx.compose.ui.graphics.Color.White,
                fontWeight = FontWeight.ExtraBold, fontSize = 22.sp)
            Text("관세청 수출입통계 · 국산 AI 무역참모", color = androidx.compose.ui.graphics.Color(0xCCFFFFFF), fontSize = 13.sp)
        }
    }
}

@Composable
private fun MarketRow(m: Market) {
    val (label, color) = when (m.status) {
        "surge" -> "급등" to Surge
        "rising" -> "상승" to Teal
        "cooling" -> "둔화" to Cool
        else -> "안정" to Muted
    }
    Card(
        Modifier.fillMaxWidth().padding(vertical = 5.dp),
        shape = RoundedCornerShape(14.dp),
    ) {
        Row(Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
            Column(Modifier.weight(1f)) {
                Text("${m.country} · ${m.product}", fontWeight = FontWeight.Bold, fontSize = 14.sp, color = Ink)
                Row(verticalAlignment = Alignment.CenterVertically) {
                    AssistChipLike(label, color)
                    Spacer(Modifier.width(6.dp))
                    Text("전년 ${pct(m.yoy)} · 6개월 ${pct(m.fcGrowth6)}", fontSize = 12.sp, color = Muted)
                }
            }
            Text("${m.opportunity.roundToInt()}", fontWeight = FontWeight.ExtraBold, fontSize = 20.sp, color = Blue)
        }
    }
}

@Composable
private fun AssistChipLike(text: String, color: androidx.compose.ui.graphics.Color) {
    Box(
        Modifier.background(color.copy(alpha = 0.14f), RoundedCornerShape(999.dp))
            .padding(horizontal = 8.dp, vertical = 2.dp),
    ) { Text(text, color = color, fontSize = 11.sp, fontWeight = FontWeight.Bold) }
}

private fun pct(v: Double): String = (if (v >= 0) "+" else "") + (v * 100).roundToInt() + "%"
