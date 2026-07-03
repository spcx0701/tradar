package kr.tradewind.app.data

import kr.tradewind.app.domain.Market
import kotlinx.coroutines.runBlocking
import org.json.JSONObject
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class KoreanLlmClientTest {
    @Test
    fun postsAdvisorQuestionToConfiguredEndpointAndParsesGroundedAnswer() = runBlocking {
        val poster = CapturingPoster(
            """
            {
              "answer": "국산 LLM 응답",
              "engine": "solar",
              "evidence": [{"label": "미국 라면", "value": "YoY +65%"}],
              "suggestions": ["리스크도 알려줘"]
            }
            """.trimIndent()
        )
        val client = KoreanLlmClient("https://api.example.test/api/advisor", poster)

        val answer = client.ask("라면 어디에 수출하면 좋을까?")

        assertEquals("https://api.example.test/api/advisor", poster.url)
        assertEquals("라면 어디에 수출하면 좋을까?", JSONObject(poster.body).getString("question"))
        assertEquals("국산 LLM 응답", answer?.answer)
        assertEquals("solar", answer?.engine)
        assertEquals("미국 라면", answer?.evidence?.single()?.label)
        assertEquals("리스크도 알려줘", answer?.suggestions?.single())
    }

    @Test
    fun blankEndpointSkipsNetworkCall() = runBlocking {
        val poster = CapturingPoster("{}")
        val client = KoreanLlmClient("", poster)

        val answer = client.ask("라면?")

        assertNull(answer)
        assertFalse(poster.called)
    }

    @Test
    fun localAssistantUsesMarketEvidenceWhenNetworkIsUnavailable() {
        val answer = LocalAssistant.answer(
            question = "라면 어디가 좋아?",
            markets = listOf(
                Market("1902.30", "라면", "K-Food", "US", "미국", 0.65, 0.12, 0.3, 0.1, 0.2, 0.35, 100_000, 73.0, 22.0, "surge"),
                Market("2106.90", "김", "K-Food", "GB", "영국", 0.40, 0.10, 0.2, 0.1, 0.2, 0.20, 80_000, 70.0, 25.0, "rising"),
            ),
        )

        assertTrue(answer.answer.contains("미국"))
        assertTrue(answer.answer.contains("라면"))
        assertTrue(answer.answer.contains("+65%"))
        assertEquals("local-grounded", answer.engine)
    }
}

private class CapturingPoster(private val response: String) : JsonPoster {
    var called = false
    var url = ""
    var body = ""

    override suspend fun postJson(url: String, body: String): String {
        called = true
        this.url = url
        this.body = body
        return response
    }
}
