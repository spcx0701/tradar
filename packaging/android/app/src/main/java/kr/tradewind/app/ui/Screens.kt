package kr.tradewind.app.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.AssistChip
import androidx.compose.material3.Button
import androidx.compose.material3.FilterChip
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import kr.tradewind.app.domain.AlertSeverity
import kr.tradewind.app.domain.Market
import kr.tradewind.app.domain.Product
import kr.tradewind.app.domain.TradarData
import kr.tradewind.app.domain.TradarQueries
import kr.tradewind.app.domain.pct
import kr.tradewind.app.domain.statusLabel
import kr.tradewind.app.domain.usd
import kr.tradewind.app.ui.theme.Blue
import kr.tradewind.app.ui.theme.Cool
import kr.tradewind.app.ui.theme.Muted
import kr.tradewind.app.ui.theme.Surge

@Composable
fun HomeScreen(
    data: TradarData,
    sourceMessage: String,
    onOpenWebApp: () -> Unit,
    onOpenMarket: (Market) -> Unit,
    onOpenSearch: () -> Unit,
) {
    LazyColumn {
        item {
            Column(Modifier.padding(16.dp)) {
                Text("Tradar", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.ExtraBold)
                Text("현장에서 바로 보는 수출 인텔리전스", color = Muted)
                Spacer(Modifier.height(12.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    MetricCard("데이터", sourceMessage, Modifier.weight(1f))
                    MetricCard("기간", data.radar.generatedPeriod.ifBlank { data.catalog.meta.period }, Modifier.weight(1f))
                }
                Spacer(Modifier.height(8.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    MetricCard("품목", "${data.catalog.products.size}", Modifier.weight(1f))
                    MetricCard("국가", "${data.catalog.countries.size}", Modifier.weight(1f))
                }
                Spacer(Modifier.height(12.dp))
                Button(onClick = onOpenWebApp, modifier = Modifier.fillMaxWidth()) {
                    Text("전체 플랫폼 열기")
                }
            }
        }
        item { SectionTitle("상위 기회", "검색", onOpenSearch) }
        items(TradarQueries.topOpportunities(data, 6)) { market ->
            MarketCard(market = market, onClick = { onOpenMarket(market) })
        }
        item { SectionTitle("리스크 경보") }
        items(TradarQueries.riskAlerts(data, 4)) { market ->
            MarketCard(market = market, onClick = { onOpenMarket(market) }) {
                Column {
                    Text("${market.risk.toInt()}", fontWeight = FontWeight.ExtraBold, color = Cool)
                    Text("위험", style = MaterialTheme.typography.labelSmall, color = Muted)
                }
            }
        }
    }
}

@Composable
fun SearchScreen(
    data: TradarData,
    savedHsCodes: List<String>,
    onOpenProduct: (Product) -> Unit,
    onOpenMarket: (Market) -> Unit,
    onToggleSave: (String) -> Unit,
) {
    var query by remember { mutableStateOf("") }
    var mode by remember { mutableStateOf("products") }
    val products = TradarQueries.searchProducts(data, query)
    val markets = TradarQueries.searchMarkets(data, query)

    LazyColumn {
        item {
            Column(Modifier.padding(16.dp)) {
                Text("빠른 조회", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                Spacer(Modifier.height(8.dp))
                OutlinedTextField(
                    value = query,
                    onValueChange = { query = it },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true,
                    label = { Text("HS, 품목, 국가, 상태") },
                )
                Spacer(Modifier.height(8.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    FilterChip(selected = mode == "products", onClick = { mode = "products" }, label = { Text("품목") })
                    FilterChip(selected = mode == "markets", onClick = { mode = "markets" }, label = { Text("시장") })
                }
            }
        }
        if (mode == "products") {
            if (products.isEmpty()) {
                item { EmptyState("검색 결과 없음", "다른 HS코드, 품목명, 카테고리로 검색해 보세요.") }
            } else {
                items(products) { product ->
                    ProductCard(
                        product = product,
                        bestMarket = product.bestMarket(data),
                        isSaved = product.hs in savedHsCodes,
                        onClick = { onOpenProduct(product) },
                        onToggleSave = { onToggleSave(product.hs) },
                    )
                }
            }
        } else {
            if (markets.isEmpty()) {
                item { EmptyState("검색 결과 없음", "국가명, 품목명, 급등/둔화 같은 상태로 검색해 보세요.") }
            } else {
                items(markets) { market -> MarketCard(market, onClick = { onOpenMarket(market) }) }
            }
        }
    }
}

@Composable
fun WatchlistScreen(
    data: TradarData,
    savedHsCodes: List<String>,
    onOpenProduct: (Product) -> Unit,
    onToggleSave: (String) -> Unit,
    onGoSearch: () -> Unit,
) {
    val products = data.catalog.products.filter { it.hs in savedHsCodes }
    LazyColumn {
        item { SectionTitle("관심목록", if (products.isEmpty()) "추가" else "검색", onGoSearch) }
        if (products.isEmpty()) {
            item { EmptyState("저장된 품목이 없습니다", "검색에서 품목을 저장하면 현장 체크리스트처럼 다시 볼 수 있습니다.") }
        } else {
            items(products) { product ->
                ProductCard(
                    product = product,
                    bestMarket = product.bestMarket(data),
                    isSaved = true,
                    onClick = { onOpenProduct(product) },
                    onToggleSave = { onToggleSave(product.hs) },
                )
            }
        }
    }
}

@Composable
fun AlertsScreen(data: TradarData, onOpenMarket: (Market) -> Unit) {
    val alerts = TradarQueries.generatedAlerts(data)
    LazyColumn {
        item { SectionTitle("알림센터") }
        if (alerts.isEmpty()) {
            item { EmptyState("생성된 알림이 없습니다", "현재 스냅샷에서는 임계값을 넘는 급등/둔화 신호가 없습니다.") }
        } else {
            items(alerts) { alert ->
                MarketCard(alert.market, onClick = { onOpenMarket(alert.market) }) {
                    Column {
                        Text(
                            if (alert.severity == AlertSeverity.Risk) "위험" else "기회",
                            color = if (alert.severity == AlertSeverity.Risk) Cool else Surge,
                            fontWeight = FontWeight.Bold,
                        )
                        Text(alert.reason, style = MaterialTheme.typography.labelSmall, color = Muted)
                    }
                }
            }
        }
    }
}

@Composable
fun AssistantScreen(data: TradarData, onOpenProduct: (Product) -> Unit, onOpenMarket: (Market) -> Unit) {
    val topProduct = data.catalog.products.maxByOrNull { it.latest12Usd }
    val topMarket = TradarQueries.topOpportunities(data, 1).firstOrNull()
    LazyColumn {
        item {
            Column(Modifier.padding(16.dp)) {
                Text("AI 무역참모", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                Text("현재 MVP는 로컬 데이터에 근거한 결정적 요약을 제공합니다.", color = Muted)
                Spacer(Modifier.height(12.dp))
                if (topProduct != null) {
                    AssistChip(onClick = { onOpenProduct(topProduct) }, label = { Text("${topProduct.nameKo} 요약") })
                    Spacer(Modifier.height(8.dp))
                    Text(TradarQueries.summaryForProduct(data, topProduct))
                }
                Spacer(Modifier.height(16.dp))
                if (topMarket != null) {
                    AssistChip(onClick = { onOpenMarket(topMarket) }, label = { Text("${topMarket.countryName} ${topMarket.product}") })
                    Spacer(Modifier.height(8.dp))
                    Text(TradarQueries.summaryForMarket(topMarket))
                }
            }
        }
    }
}

@Composable
fun ProductDetailScreen(data: TradarData, hs: String, saved: Boolean, onBack: () -> Unit, onToggleSave: () -> Unit, onOpenMarket: (Market) -> Unit) {
    val product = data.catalog.products.firstOrNull { it.hs == hs }
    val markets = TradarQueries.marketsForProduct(data, hs)
    LazyColumn {
        if (product == null) {
            item {
                Column(Modifier.padding(16.dp)) {
                    Button(onClick = onBack) { Text("뒤로") }
                    Spacer(Modifier.height(12.dp))
                    Text("품목을 찾을 수 없습니다.")
                }
            }
        } else {
            val currentProduct = product
            item {
                Column(Modifier.padding(16.dp)) {
                    Button(onClick = onBack) { Text("뒤로") }
                    Spacer(Modifier.height(12.dp))
                    Text(currentProduct.nameKo, style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.ExtraBold)
                    Text("HS ${currentProduct.hs} · ${currentProduct.category}", color = Muted)
                    Spacer(Modifier.height(12.dp))
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        MetricCard("최근 12개월", usd(currentProduct.latest12Usd), Modifier.weight(1f))
                        MetricCard("YoY", pct(currentProduct.yoy), Modifier.weight(1f))
                    }
                    Spacer(Modifier.height(8.dp))
                    Button(onClick = onToggleSave, modifier = Modifier.fillMaxWidth()) {
                        Text(if (saved) "관심목록에서 제거" else "관심목록에 저장")
                    }
                    Spacer(Modifier.height(12.dp))
                    Text(TradarQueries.summaryForProduct(data, currentProduct), color = Blue)
                }
            }
            item { SectionTitle("국가별 시장") }
            items(markets) { market -> MarketCard(market, onClick = { onOpenMarket(market) }) }
        }
    }
}

@Composable
fun MarketDetailScreen(market: Market, onBack: () -> Unit) {
    LazyColumn {
        item {
            Column(Modifier.padding(16.dp)) {
                Button(onClick = onBack) { Text("뒤로") }
                Spacer(Modifier.height(12.dp))
                Text("${market.countryName} · ${market.product}", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.ExtraBold)
                Text("HS ${market.hs} · ${market.category} · ${statusLabel(market.status)}", color = Muted)
                Spacer(Modifier.height(12.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    MetricCard("기회", "${market.opportunity.toInt()}점", Modifier.weight(1f))
                    MetricCard("리스크", "${market.risk.toInt()}점", Modifier.weight(1f))
                }
                Spacer(Modifier.height(8.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    MetricCard("YoY", pct(market.yoy), Modifier.weight(1f))
                    MetricCard("6개월 전망", pct(market.forecastGrowth6), Modifier.weight(1f))
                }
                Spacer(Modifier.height(12.dp))
                Text("최근 12개월 수출액 ${usd(market.recent12Usd)}", color = Muted)
                Spacer(Modifier.height(12.dp))
                Text(TradarQueries.summaryForMarket(market), color = Blue)
            }
        }
    }
}
