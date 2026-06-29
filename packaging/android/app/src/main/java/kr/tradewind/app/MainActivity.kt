package kr.tradewind.app

import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.browser.customtabs.CustomTabsIntent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import kr.tradewind.app.data.Repository
import kr.tradewind.app.ui.HomeScreen
import kr.tradewind.app.ui.theme.TradewindTheme

/**
 * 무역풍 네이티브 진입점.
 * - 기본: Jetpack Compose 네이티브 홈(떠오르는 시장).
 * - 전체 웹앱(예보·AI 참모·리포트·대시보드)은 Custom Tabs/TWA 로 전체화면 실행.
 */
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            TradewindTheme {
                Surface(Modifier.fillMaxSize()) { App() }
            }
        }
    }
}

private const val WEB_APP_URL = "https://spcx0701.github.io/tradewind/"

@Composable
private fun App() {
    val context = LocalContext.current
    val repo = Repository(context.applicationContext)
    HomeScreen(
        repo = repo,
        onOpenWebApp = {
            CustomTabsIntent.Builder()
                .setShowTitle(true)
                .build()
                .launchUrl(context, Uri.parse(WEB_APP_URL))
        },
    )
}
