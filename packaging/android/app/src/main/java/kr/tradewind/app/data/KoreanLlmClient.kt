package kr.tradewind.app.data

import kr.tradewind.app.domain.Market
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import kotlin.math.roundToInt

data class AssistantEvidence(
    val label: String,
    val value: String,
)

data class AssistantAnswer(
    val answer: String,
    val evidence: List<AssistantEvidence>,
    val suggestions: List<String>,
    val engine: String,
)

interface JsonPoster {
    suspend fun postJson(url: String, body: String): String
}

class HttpJsonPoster : JsonPoster {
    override suspend fun postJson(url: String, body: String): String = withContext(Dispatchers.IO) {
        (URL(url).openConnection() as HttpURLConnection).run {
            requestMethod = "POST"
            connectTimeout = 5000
            readTimeout = 15000
            doOutput = true
            setRequestProperty("Content-Type", "application/json; charset=utf-8")
            outputStream.use { it.write(body.toByteArray(Charsets.UTF_8)) }
            if (responseCode in 200..299) {
                inputStream.bufferedReader().use { it.readText() }
            } else {
                errorStream?.bufferedReader()?.use { it.readText() }
                throw RuntimeException("advisor endpoint returned HTTP $responseCode")
            }
        }
    }
}

class KoreanLlmClient(
    private val endpoint: String,
    private val poster: JsonPoster = HttpJsonPoster(),
) {
    suspend fun ask(question: String): AssistantAnswer? {
        val target = endpoint.trim()
        val cleaned = question.trim()
        if (target.isEmpty() || cleaned.isEmpty()) return null

        return runCatching {
            val body = JSONObject().put("question", cleaned).toString()
            parseAnswer(poster.postJson(target, body))
        }.getOrNull()
    }

    private fun parseAnswer(raw: String): AssistantAnswer {
        val obj = JSONObject(raw)
        val evidence = obj.optJSONArray("evidence")
        val suggestions = obj.optJSONArray("suggestions")
        return AssistantAnswer(
            answer = obj.getString("answer"),
            engine = obj.optString("engine", "korean-llm"),
            evidence = (0 until (evidence?.length() ?: 0)).map { i ->
                val item = evidence!!.getJSONObject(i)
                AssistantEvidence(
                    label = item.optString("label"),
                    value = item.optString("value"),
                )
            },
            suggestions = (0 until (suggestions?.length() ?: 0)).map { i ->
                suggestions!!.optString(i)
            }.filter { it.isNotBlank() },
        )
    }
}

object LocalAssistant {
    fun answer(question: String, markets: List<Market>): AssistantAnswer {
        val cleaned = question.trim()
        val picked = pickMarket(cleaned, markets)
        if (picked == null) {
            return AssistantAnswer(
                answer = "아직 분석할 시장 데이터가 없습니다. 네트워크가 복구되면 국산 LLM 무역참모가 같은 질문을 다시 처리합니다.",
                evidence = emptyList(),
                suggestions = listOf("라면 어디에 수출하면 좋을까?", "위험한 시장 알려줘"),
                engine = "local-grounded",
            )
        }

        val answer = "${picked.countryName} ${picked.product} 시장이 현재 가장 먼저 볼 후보입니다. " +
            "기회점수는 ${picked.opportunity.roundToInt()}점, 전년 대비 ${pct(picked.yoy)}, " +
            "향후 6개월 전망은 ${pct(picked.forecastGrowth6)}입니다. " +
            "국산 LLM 연결이 비활성화되었거나 실패해, 앱에 저장된 관세청 기반 지표로만 답했습니다."
        return AssistantAnswer(
            answer = answer,
            evidence = listOf(
                AssistantEvidence("${picked.countryName} ${picked.product}", "기회 ${picked.opportunity.roundToInt()}"),
                AssistantEvidence("전년 대비", pct(picked.yoy)),
                AssistantEvidence("향후 6개월", pct(picked.forecastGrowth6)),
            ),
            suggestions = listOf("${picked.product} 리스크도 알려줘", "오늘 뜨는 시장은?"),
            engine = "local-grounded",
        )
    }

    private fun pickMarket(question: String, markets: List<Market>): Market? {
        if (markets.isEmpty()) return null
        return markets.firstOrNull { question.contains(it.product.substringBefore("(")) }
            ?: markets.firstOrNull { question.contains(it.countryName) || question.contains(it.country) }
            ?: markets.maxByOrNull { it.opportunity }
    }

    private fun pct(value: Double): String = (if (value >= 0) "+" else "") + (value * 100).roundToInt() + "%"
}
