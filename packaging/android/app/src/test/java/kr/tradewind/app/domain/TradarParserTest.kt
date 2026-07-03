package kr.tradewind.app.domain

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class TradarParserTest {
    private val catalogJson = """
        {
          "meta": {
            "generated_at": "2026-07-03T00:00:00Z",
            "period": "2021-01 ~ 2025-12",
            "unit": "USD"
          },
          "countries": {
            "US": "미국",
            "GB": "영국"
          },
          "products": [
            {
              "hs": "1902.30",
              "name_ko": "라면(즉석면)",
              "category": "K-Food",
              "anchor_2024_musd": 1240,
              "latest12_usd": 1667709276,
              "yoy": 0.303
            },
            {
              "hs": "3304.99",
              "name_ko": "화장품(기초·색조)",
              "category": "K-Beauty",
              "anchor_2024_musd": 10200,
              "latest12_usd": 11446299948,
              "yoy": 0.144
            }
          ],
          "categories": ["K-Food", "K-Beauty"]
        }
    """.trimIndent()

    private val radarJson = """
        {
          "top": [
            {
              "hs": "1902.30",
              "product": "라면(즉석면)",
              "category": "K-Food",
              "country": "US",
              "country_name": "미국",
              "yoy": 0.629,
              "growth3": 0.287,
              "fc_growth6": 0.45,
              "recent12_usd": 359226831,
              "opportunity": 75.3,
              "risk": 3.0,
              "status": "surge"
            }
          ],
          "risk": [
            {
              "hs": "3304.99",
              "product": "화장품(기초·색조)",
              "category": "K-Beauty",
              "country": "GB",
              "country_name": "영국",
              "yoy": -0.255,
              "growth3": -0.121,
              "fc_growth6": -0.237,
              "recent12_usd": 2065753011,
              "opportunity": 47.6,
              "risk": 76.5,
              "status": "cooling"
            }
          ],
          "by_product": {
            "1902.30": [
              {
                "country": "US",
                "country_name": "미국",
                "yoy": 0.629,
                "growth3": 0.287,
                "fc_growth6": 0.45,
                "recent12_usd": 359226831,
                "opportunity": 75.3,
                "risk": 3.0,
                "status": "surge"
              }
            ]
          },
          "generated_period": "2021-01 ~ 2025-12"
        }
    """.trimIndent()

    @Test
    fun parsesCatalogAndRadarIntoTypedData() {
        val data = TradarParser.parseData(catalogJson, radarJson, DataSource.Bundled)

        assertEquals(DataSource.Bundled, data.source)
        assertEquals("2021-01 ~ 2025-12", data.catalog.meta.period)
        assertEquals(2, data.catalog.products.size)
        assertEquals("미국", data.catalog.countries["US"])
        assertEquals("라면(즉석면)", data.radar.top.first().product)
        assertEquals("화장품(기초·색조)", data.radar.risk.first().product)
        assertEquals("라면(즉석면)", data.radar.byProduct.getValue("1902.30").first().product)
    }

    @Test
    fun searchesProductsByHsNameAndCategory() {
        val data = TradarParser.parseData(catalogJson, radarJson, DataSource.Bundled)

        assertEquals("라면(즉석면)", TradarQueries.searchProducts(data, "1902").single().nameKo)
        assertEquals("화장품(기초·색조)", TradarQueries.searchProducts(data, "화장").single().nameKo)
        assertEquals(1, TradarQueries.searchProducts(data, "beauty").size)
    }

    @Test
    fun searchesMarketsAndGeneratesAlerts() {
        val data = TradarParser.parseData(catalogJson, radarJson, DataSource.Bundled)

        val usMarkets = TradarQueries.searchMarkets(data, "미국")
        val coolingMarkets = TradarQueries.searchMarkets(data, "둔화")
        val alerts = TradarQueries.generatedAlerts(data)

        assertEquals("US", usMarkets.single().country)
        assertEquals("GB", coolingMarkets.single().country)
        assertTrue(alerts.any { it.title.contains("위험") && it.market.country == "GB" })
        assertTrue(alerts.any { it.title.contains("기회") && it.market.country == "US" })
    }
}
