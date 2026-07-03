package kr.tradewind.app.domain

enum class DataSource {
    Remote,
    Bundled,
}

data class CatalogMeta(
    val generatedAt: String,
    val source: String,
    val sourceApi: String,
    val unit: String,
    val period: String,
    val note: String,
)

data class Product(
    val hs: String,
    val nameKo: String,
    val category: String,
    val anchor2024Musd: Double,
    val latest12Usd: Long,
    val yoy: Double,
)

data class TradarCatalog(
    val meta: CatalogMeta,
    val countries: Map<String, String>,
    val products: List<Product>,
    val categories: List<String>,
)

data class Market(
    val hs: String,
    val product: String,
    val category: String,
    val country: String,
    val countryName: String,
    val yoy: Double,
    val growth3: Double,
    val slope: Double,
    val accel: Double,
    val cv: Double,
    val forecastGrowth6: Double,
    val recent12Usd: Long,
    val opportunity: Double,
    val risk: Double,
    val status: String,
)

data class TradarRadar(
    val top: List<Market>,
    val risk: List<Market>,
    val byProduct: Map<String, List<Market>>,
    val generatedPeriod: String,
)

data class TradarData(
    val catalog: TradarCatalog,
    val radar: TradarRadar,
    val source: DataSource,
)

enum class AlertSeverity {
    Opportunity,
    Risk,
}

data class TradarAlert(
    val id: String,
    val severity: AlertSeverity,
    val title: String,
    val reason: String,
    val market: Market,
)
