package kr.tradewind.app

import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.browser.customtabs.CustomTabsIntent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import kr.tradewind.app.data.SharedPreferencesKeyValueStore
import kr.tradewind.app.data.TradarRepository
import kr.tradewind.app.data.WatchlistStore
import kr.tradewind.app.ui.TradarApp
import kr.tradewind.app.ui.theme.TradewindTheme

/**
 * 무역풍 네이티브 진입점.
 * - 기본: Jetpack Compose 네이티브 companion 앱.
 * - 전체 웹앱(예보·AI 참모·리포트·대시보드)은 Custom Tabs/TWA 로 전체화면 실행.
 */
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val repository = TradarRepository(applicationContext)
        val watchlistStore = WatchlistStore(
            SharedPreferencesKeyValueStore(
                getSharedPreferences("tradewind_preferences", MODE_PRIVATE),
            ),
        )
        setContent {
            TradewindTheme {
                Surface(Modifier.fillMaxSize()) {
                    App(repository = repository, watchlistStore = watchlistStore)
                }
            }
        }
    }
}

private const val WEB_APP_URL = "https://tradar.onrender.com/"

@Composable
private fun App(repository: TradarRepository, watchlistStore: WatchlistStore) {
    val context = LocalContext.current
    TradarApp(
        repository = repository,
        watchlistStore = watchlistStore,
        onOpenWebApp = {
            CustomTabsIntent.Builder()
                .setShowTitle(true)
                .build()
                .launchUrl(context, Uri.parse(WEB_APP_URL))
        },
    )
}
