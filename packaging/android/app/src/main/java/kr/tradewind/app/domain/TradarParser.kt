package kr.tradewind.app.domain

import org.json.JSONArray
import org.json.JSONObject

object TradarParser {
    fun parseData(catalogJson: String, radarJson: String, source: DataSource): TradarData {
        val catalog = parseCatalog(catalogJson)
        val radar = parseRadar(radarJson, catalog)
        return TradarData(catalog = catalog, radar = radar, source = source)
    }

    fun parseCatalog(raw: String): TradarCatalog {
        val root = JSONObject(raw)
        val meta = root.optJSONObject("meta") ?: JSONObject()
        val countries = root.optJSONObject("countries")?.toStringMap().orEmpty()
        val products = root.optJSONArray("products").orEmptyArray().mapObjects { product ->
            Product(
                hs = product.optString("hs"),
                nameKo = product.optString("name_ko"),
                category = product.optString("category"),
                anchor2024Musd = product.optDouble("anchor_2024_musd", 0.0),
                latest12Usd = product.optLong("latest12_usd", 0L),
                yoy = product.optDouble("yoy", 0.0),
            )
        }
        val categories = root.optJSONArray("categories").orEmptyArray().mapStrings()

        return TradarCatalog(
            meta = CatalogMeta(
                generatedAt = meta.optString("generated_at"),
                source = meta.optString("source"),
                sourceApi = meta.optString("source_api"),
                unit = meta.optString("unit"),
                period = meta.optString("period"),
                note = meta.optString("note"),
            ),
            countries = countries,
            products = products,
            categories = categories,
        )
    }

    fun parseRadar(raw: String, catalog: TradarCatalog? = null): TradarRadar {
        val root = JSONObject(raw)
        val productsByHs = catalog?.products?.associateBy { it.hs }.orEmpty()
        val top = root.optJSONArray("top").orEmptyArray().mapObjects { it.toMarket(productsByHs = productsByHs) }
        val risk = root.optJSONArray("risk").orEmptyArray().mapObjects { it.toMarket(productsByHs = productsByHs) }
        val byProductRoot = root.optJSONObject("by_product") ?: JSONObject()
        val byProduct = mutableMapOf<String, List<Market>>()

        byProductRoot.keys().forEach { hs ->
            val product = productsByHs[hs]
            val markets = byProductRoot.optJSONArray(hs).orEmptyArray().mapObjects {
                it.toMarket(
                    hsOverride = hs,
                    productOverride = product?.nameKo.orEmpty(),
                    categoryOverride = product?.category.orEmpty(),
                    productsByHs = productsByHs,
                )
            }
            byProduct[hs] = markets
        }

        return TradarRadar(
            top = top,
            risk = risk,
            byProduct = byProduct.toSortedMap(),
            generatedPeriod = root.optString("generated_period"),
        )
    }

    private fun JSONObject.toMarket(
        hsOverride: String? = null,
        productOverride: String? = null,
        categoryOverride: String? = null,
        productsByHs: Map<String, Product> = emptyMap(),
    ): Market {
        val hs = hsOverride ?: optString("hs")
        val product = productsByHs[hs]
        return Market(
            hs = hs,
            product = optString("product", productOverride ?: product?.nameKo.orEmpty()),
            category = optString("category", categoryOverride ?: product?.category.orEmpty()),
            country = optString("country"),
            countryName = optString("country_name", optString("country")),
            yoy = optDouble("yoy", 0.0),
            growth3 = optDouble("growth3", 0.0),
            slope = optDouble("slope", 0.0),
            accel = optDouble("accel", 0.0),
            cv = optDouble("cv", 0.0),
            forecastGrowth6 = optDouble("fc_growth6", 0.0),
            recent12Usd = optLong("recent12_usd", 0L),
            opportunity = optDouble("opportunity", 0.0),
            risk = optDouble("risk", 0.0),
            status = optString("status", "stable"),
        )
    }
}

private fun JSONObject.toStringMap(): Map<String, String> =
    keys().asSequence().associateWith { key -> optString(key) }.toSortedMap()

private fun JSONArray?.orEmptyArray(): JSONArray = this ?: JSONArray()

private fun JSONArray.mapStrings(): List<String> = (0 until length()).map { index -> optString(index) }

private fun <T> JSONArray.mapObjects(block: (JSONObject) -> T): List<T> =
    (0 until length()).map { index -> block(getJSONObject(index)) }
