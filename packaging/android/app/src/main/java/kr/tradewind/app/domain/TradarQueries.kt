package kr.tradewind.app.domain

import java.text.NumberFormat
import java.util.Locale
import kotlin.math.roundToInt

object TradarQueries {
    fun searchProducts(data: TradarData, query: String): List<Product> {
        val normalized = query.searchKey()
        if (normalized.isBlank()) return data.catalog.products
        return data.catalog.products.filter { product ->
            listOf(product.hs, product.nameKo, product.category).any { it.searchKey().contains(normalized) }
        }
    }

    fun searchMarkets(data: TradarData, query: String): List<Market> {
        val normalized = query.searchKey()
        if (normalized.isBlank()) return allMarkets(data)
        return allMarkets(data).filter { market ->
            listOf(
                market.hs,
                market.product,
                market.category,
                market.country,
                market.countryName,
                market.status,
                statusLabel(market.status),
            ).any { it.searchKey().contains(normalized) }
        }
    }

    fun marketsForProduct(data: TradarData, hs: String): List<Market> =
        data.radar.byProduct[hs].orEmpty().ifEmpty {
            allMarkets(data).filter { it.hs == hs }
        }.sortedWith(compareByDescending<Market> { it.opportunity }.thenBy { it.countryName })

    fun topOpportunities(data: TradarData, limit: Int = 8): List<Market> =
        data.radar.top.sortedByDescending { it.opportunity }.take(limit)

    fun riskAlerts(data: TradarData, limit: Int = 8): List<Market> =
        data.radar.risk.sortedByDescending { it.risk }.take(limit)

    fun generatedAlerts(data: TradarData): List<TradarAlert> {
        val risk = riskAlerts(data, limit = 6)
            .filter { it.risk >= 55.0 || it.status == "cooling" }
            .map { market ->
                TradarAlert(
                    id = "risk-${market.hs}-${market.country}",
                    severity = AlertSeverity.Risk,
                    title = "${market.countryName} ${market.product} 위험 신호",
                    reason = "리스크 ${market.risk.roundToInt()}점, 6개월 전망 ${pct(market.forecastGrowth6)}",
                    market = market,
                )
            }

        val opportunities = topOpportunities(data, limit = 6)
            .filter { it.opportunity >= 70.0 || it.status == "surge" }
            .map { market ->
                TradarAlert(
                    id = "opportunity-${market.hs}-${market.country}",
                    severity = AlertSeverity.Opportunity,
                    title = "${market.countryName} ${market.product} 기회 신호",
                    reason = "기회 ${market.opportunity.roundToInt()}점, 전년 대비 ${pct(market.yoy)}",
                    market = market,
                )
            }

        return (risk + opportunities).distinctBy { it.id }
    }

    fun allMarkets(data: TradarData): List<Market> =
        (data.radar.top + data.radar.risk + data.radar.byProduct.values.flatten())
            .distinctBy { "${it.hs}:${it.country}:${it.status}" }

    fun summaryForProduct(data: TradarData, product: Product): String {
        val markets = marketsForProduct(data, product.hs)
        val best = markets.maxByOrNull { it.opportunity }
        val risk = markets.maxByOrNull { it.risk }
        return buildString {
            append("${product.nameKo}은 ${product.category} 품목입니다. ")
            append("최근 12개월 수출액은 ${usd(product.latest12Usd)}이고 전년 대비 ${pct(product.yoy)}입니다.")
            if (best != null) append(" 가장 강한 기회 시장은 ${best.countryName}(${best.opportunity.roundToInt()}점)입니다.")
            if (risk != null && risk.risk >= 55.0) append(" 주의 시장은 ${risk.countryName}(${risk.risk.roundToInt()}점)입니다.")
        }
    }

    fun summaryForMarket(market: Market): String =
        "${market.countryName} ${market.product}: ${statusLabel(market.status)}, " +
            "기회 ${market.opportunity.roundToInt()}점, 리스크 ${market.risk.roundToInt()}점, " +
            "전년 대비 ${pct(market.yoy)}, 6개월 전망 ${pct(market.forecastGrowth6)}."
}

fun statusLabel(status: String): String = when (status) {
    "surge" -> "급등"
    "rising" -> "상승"
    "cooling" -> "둔화"
    else -> "안정"
}

fun pct(value: Double): String = (if (value >= 0) "+" else "") + "${(value * 100).roundToInt()}%"

fun usd(value: Long): String {
    val formatter = NumberFormat.getCurrencyInstance(Locale.US)
    formatter.maximumFractionDigits = 0
    return formatter.format(value)
}

private fun String.searchKey(): String = trim().lowercase(Locale.ROOT)
