package kr.tradewind.app.data

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

/** 떠오르는/식어가는 시장 한 줄. */
data class Market(
    val product: String,
    val country: String,
    val opportunity: Double,
    val yoy: Double,
    val fcGrowth6: Double,
    val status: String,
)

/**
 * 레이더 데이터 저장소.
 * 우선 라이브 API(server/main.py)를 시도하고, 실패 시 앱에 번들된 radar.json 으로 폴백한다.
 * → 무역풍 정적 데모와 동일하게 오프라인에서도 동작.
 */
class Repository(private val context: Context) {

    private val apiBase = "https://spcx0701.github.io/tradewind/data" // 정적 JSON 호스팅

    suspend fun topMarkets(): List<Market> = withContext(Dispatchers.IO) {
        val json = fetchRemote("$apiBase/radar.json") ?: readAsset("radar.json")
        parseTop(json)
    }

    private fun parseTop(raw: String): List<Market> {
        val arr = JSONObject(raw).getJSONArray("top")
        return (0 until arr.length()).map { i ->
            val o = arr.getJSONObject(i)
            Market(
                product = o.optString("product", o.optString("hs")),
                country = o.optString("country_name", o.optString("country")),
                opportunity = o.optDouble("opportunity"),
                yoy = o.optDouble("yoy"),
                fcGrowth6 = o.optDouble("fc_growth6"),
                status = o.optString("status", "stable"),
            )
        }
    }

    private fun readAsset(name: String): String =
        context.assets.open(name).bufferedReader().use { it.readText() }

    private fun fetchRemote(url: String): String? = try {
        (URL(url).openConnection() as HttpURLConnection).run {
            connectTimeout = 3000; readTimeout = 3000
            if (responseCode == 200) inputStream.bufferedReader().use { it.readText() } else null
        }
    } catch (e: Exception) {
        null
    }
}
