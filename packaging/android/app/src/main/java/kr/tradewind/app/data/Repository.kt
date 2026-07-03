package kr.tradewind.app.data

import android.content.Context
import kr.tradewind.app.BuildConfig
import kr.tradewind.app.domain.DataSource
import kr.tradewind.app.domain.TradarData
import kr.tradewind.app.domain.TradarParser
import kr.tradewind.app.domain.TradarQueries
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.net.HttpURLConnection
import java.net.URL

sealed interface TradarLoadResult {
    data class Success(
        val data: TradarData,
        val message: String,
    ) : TradarLoadResult

    data class Failure(
        val message: String,
        val cause: Throwable? = null,
    ) : TradarLoadResult
}

class TradarRepository(
    private val context: Context,
    private val remoteBaseUrl: String = BuildConfig.TRADAR_DATA_BASE.ifBlank {
        "https://tradar.onrender.com/data"
    },
    private val llmClient: KoreanLlmClient = KoreanLlmClient(BuildConfig.KOREAN_LLM_ENDPOINT),
) {
    suspend fun load(): TradarLoadResult = withContext(Dispatchers.IO) {
        val remote = runCatching {
            val catalog = fetchRemote("$remoteBaseUrl/catalog.json")
            val radar = fetchRemote("$remoteBaseUrl/radar.json")
            if (catalog != null && radar != null) {
                TradarParser.parseData(catalog, radar, DataSource.Remote)
            } else {
                null
            }
        }.getOrNull()

        if (remote != null) {
            return@withContext TradarLoadResult.Success(
                data = remote,
                message = "원격 최신 데이터",
            )
        }

        runCatching {
            TradarParser.parseData(
                catalogJson = readAsset("catalog.json"),
                radarJson = readAsset("radar.json"),
                source = DataSource.Bundled,
            )
        }.fold(
            onSuccess = { data ->
                TradarLoadResult.Success(
                    data = data,
                    message = "오프라인 번들 스냅샷",
                )
            },
            onFailure = { error ->
                TradarLoadResult.Failure(
                    message = "데이터를 불러오지 못했습니다. 네트워크와 앱 자산을 확인해 주세요.",
                    cause = error,
                )
            },
        )
    }

    suspend fun askAssistant(question: String, data: TradarData): AssistantAnswer {
        val remote = llmClient.ask(question)
        return remote ?: LocalAssistant.answer(question, TradarQueries.allMarkets(data))
    }

    private fun readAsset(name: String): String =
        context.assets.open(name).bufferedReader().use { it.readText() }

    private fun fetchRemote(url: String): String? = try {
        (URL(url).openConnection() as HttpURLConnection).run {
            connectTimeout = 2500
            readTimeout = 2500
            requestMethod = "GET"
            if (responseCode in 200..299) {
                inputStream.bufferedReader().use { it.readText() }
            } else {
                null
            }
        }
    } catch (_: Exception) {
        null
    }
}
