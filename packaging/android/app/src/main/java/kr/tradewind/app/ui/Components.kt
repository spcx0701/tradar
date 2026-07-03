package kr.tradewind.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import kr.tradewind.app.domain.Market
import kr.tradewind.app.domain.Product
import kr.tradewind.app.domain.TradarQueries
import kr.tradewind.app.domain.pct
import kr.tradewind.app.domain.statusLabel
import kr.tradewind.app.domain.usd
import kr.tradewind.app.ui.theme.Blue
import kr.tradewind.app.ui.theme.Cool
import kr.tradewind.app.ui.theme.Ink
import kr.tradewind.app.ui.theme.Muted
import kr.tradewind.app.ui.theme.Surge
import kr.tradewind.app.ui.theme.Teal

@Composable
fun SectionTitle(title: String, action: String? = null, onAction: (() -> Unit)? = null) {
    Row(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = Ink)
        if (action != null && onAction != null) {
            Text(
                action,
                modifier = Modifier.clickable(onClick = onAction).padding(4.dp),
                style = MaterialTheme.typography.labelLarge,
                color = Blue,
                fontWeight = FontWeight.Bold,
            )
        }
    }
}

@Composable
fun MetricCard(label: String, value: String, modifier: Modifier = Modifier) {
    Card(
        modifier = modifier,
        shape = RoundedCornerShape(8.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
    ) {
        Column(Modifier.padding(12.dp)) {
            Text(label, style = MaterialTheme.typography.labelSmall, color = Muted)
            Spacer(Modifier.height(4.dp))
            Text(value, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.ExtraBold, color = Ink)
        }
    }
}

@Composable
fun StatusChip(status: String) {
    val color = when (status) {
        "surge" -> Surge
        "rising" -> Teal
        "cooling" -> Cool
        else -> Muted
    }
    Surface(
        shape = RoundedCornerShape(999.dp),
        color = color.copy(alpha = 0.13f),
    ) {
        Text(
            statusLabel(status),
            modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp),
            style = MaterialTheme.typography.labelSmall,
            color = color,
            fontWeight = FontWeight.Bold,
        )
    }
}

@Composable
fun MarketCard(
    market: Market,
    onClick: () -> Unit,
    trailing: @Composable (() -> Unit)? = null,
) {
    Card(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 5.dp).clickable(onClick = onClick),
        shape = RoundedCornerShape(8.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
    ) {
        Row(Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
            Column(Modifier.weight(1f)) {
                Text("${market.countryName} · ${market.product}", fontWeight = FontWeight.Bold, color = Ink)
                Spacer(Modifier.height(6.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    StatusChip(market.status)
                    Spacer(Modifier.width(8.dp))
                    Text(
                        "YoY ${pct(market.yoy)} · 6M ${pct(market.forecastGrowth6)}",
                        style = MaterialTheme.typography.bodySmall,
                        color = Muted,
                    )
                }
                Spacer(Modifier.height(4.dp))
                Text(usd(market.recent12Usd), style = MaterialTheme.typography.bodySmall, color = Muted)
            }
            if (trailing != null) {
                trailing()
            } else {
                Column(horizontalAlignment = Alignment.End) {
                    Text("${market.opportunity.toInt()}", fontWeight = FontWeight.ExtraBold, color = Blue)
                    Text("기회", style = MaterialTheme.typography.labelSmall, color = Muted)
                }
            }
        }
    }
}

@Composable
fun ProductCard(product: Product, bestMarket: Market?, isSaved: Boolean, onClick: () -> Unit, onToggleSave: () -> Unit) {
    Card(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 5.dp),
        shape = RoundedCornerShape(8.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
    ) {
        Row(Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
            Column(Modifier.weight(1f).clickable(onClick = onClick)) {
                Text(product.nameKo, fontWeight = FontWeight.Bold, color = Ink)
                Text("HS ${product.hs} · ${product.category}", style = MaterialTheme.typography.bodySmall, color = Muted)
                if (bestMarket != null) {
                    Text(
                        "최고 기회: ${bestMarket.countryName} ${bestMarket.opportunity.toInt()}점",
                        style = MaterialTheme.typography.bodySmall,
                        color = Blue,
                    )
                }
            }
            Text(
                if (isSaved) "저장됨" else "저장",
                modifier = Modifier
                    .background(if (isSaved) Teal.copy(alpha = 0.12f) else Blue.copy(alpha = 0.1f), RoundedCornerShape(8.dp))
                    .clickable(onClick = onToggleSave)
                    .padding(horizontal = 10.dp, vertical = 7.dp),
                color = if (isSaved) Teal else Blue,
                fontWeight = FontWeight.Bold,
                style = MaterialTheme.typography.labelMedium,
            )
        }
    }
}

@Composable
fun EmptyState(title: String, body: String) {
    Column(Modifier.fillMaxWidth().padding(28.dp), horizontalAlignment = Alignment.CenterHorizontally) {
        Text(title, fontWeight = FontWeight.Bold, color = Ink)
        Spacer(Modifier.height(6.dp))
        Text(body, style = MaterialTheme.typography.bodySmall, color = Muted)
    }
}

fun Product.bestMarket(data: kr.tradewind.app.domain.TradarData): Market? =
    TradarQueries.marketsForProduct(data, hs).maxByOrNull { it.opportunity }
