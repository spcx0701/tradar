package kr.tradewind.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Chat
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import kr.tradewind.app.data.TradarLoadResult
import kr.tradewind.app.data.TradarRepository
import kr.tradewind.app.data.WatchlistStore
import kr.tradewind.app.domain.Market
import kr.tradewind.app.domain.TradarData
import kr.tradewind.app.domain.TradarQueries
import kr.tradewind.app.ui.theme.BgLight
import kr.tradewind.app.ui.theme.Muted

@Composable
fun TradarApp(
    repository: TradarRepository,
    watchlistStore: WatchlistStore,
    onOpenWebApp: () -> Unit,
) {
    var loadResult by remember { mutableStateOf<TradarLoadResult?>(null) }
    var retryToken by remember { mutableIntStateOf(0) }
    var tab by remember { mutableStateOf(AppTab.Home) }
    var route by remember { mutableStateOf<ScreenRoute>(ScreenRoute.Tabs) }
    var savedHsCodes by remember { mutableStateOf(watchlistStore.savedHsCodes()) }

    fun toggleSave(hs: String) {
        watchlistStore.toggle(hs)
        savedHsCodes = watchlistStore.savedHsCodes()
    }

    LaunchedEffect(retryToken) {
        loadResult = null
        loadResult = repository.load()
    }

    when (val result = loadResult) {
        null -> LoadingScreen()
        is TradarLoadResult.Failure -> FailureScreen(
            message = result.message,
            onRetry = { retryToken += 1 },
            onOpenWebApp = onOpenWebApp,
        )
        is TradarLoadResult.Success -> DataAppScaffold(
            data = result.data,
            sourceMessage = result.message,
            tab = tab,
            route = route,
            savedHsCodes = savedHsCodes,
            onSelectTab = {
                tab = it
                route = ScreenRoute.Tabs
            },
            onOpenWebApp = onOpenWebApp,
            onOpenProduct = { route = ScreenRoute.ProductDetail(it.hs) },
            onOpenMarket = { route = ScreenRoute.MarketDetail(it.hs, it.country) },
            onToggleSave = ::toggleSave,
        )
    }
}

@Composable
private fun DataAppScaffold(
    data: TradarData,
    sourceMessage: String,
    tab: AppTab,
    route: ScreenRoute,
    savedHsCodes: List<String>,
    onSelectTab: (AppTab) -> Unit,
    onOpenWebApp: () -> Unit,
    onOpenProduct: (kr.tradewind.app.domain.Product) -> Unit,
    onOpenMarket: (Market) -> Unit,
    onToggleSave: (String) -> Unit,
) {
    Scaffold(
        bottomBar = {
            if (route == ScreenRoute.Tabs) {
                NavigationBar {
                    AppTab.entries.forEach { item ->
                        NavigationBarItem(
                            selected = tab == item,
                            onClick = { onSelectTab(item) },
                            icon = { Icon(item.icon, contentDescription = item.label) },
                            label = { Text(item.label) },
                        )
                    }
                }
            }
        },
    ) { padding ->
        Box(
            modifier = Modifier.fillMaxSize().background(BgLight).padding(padding),
        ) {
            when (route) {
                ScreenRoute.Tabs -> when (tab) {
                    AppTab.Home -> HomeScreen(
                        data = data,
                        sourceMessage = sourceMessage,
                        onOpenWebApp = onOpenWebApp,
                        onOpenMarket = onOpenMarket,
                        onOpenSearch = { onSelectTab(AppTab.Search) },
                    )
                    AppTab.Search -> SearchScreen(
                        data = data,
                        savedHsCodes = savedHsCodes,
                        onOpenProduct = onOpenProduct,
                        onOpenMarket = onOpenMarket,
                        onToggleSave = onToggleSave,
                    )
                    AppTab.Watchlist -> WatchlistScreen(
                        data = data,
                        savedHsCodes = savedHsCodes,
                        onOpenProduct = onOpenProduct,
                        onToggleSave = onToggleSave,
                        onGoSearch = { onSelectTab(AppTab.Search) },
                    )
                    AppTab.Alerts -> AlertsScreen(data = data, onOpenMarket = onOpenMarket)
                    AppTab.Assistant -> AssistantScreen(
                        data = data,
                        onOpenProduct = onOpenProduct,
                        onOpenMarket = onOpenMarket,
                    )
                }
                is ScreenRoute.ProductDetail -> ProductDetailScreen(
                    data = data,
                    hs = route.hs,
                    saved = route.hs in savedHsCodes,
                    onBack = { routeBack(onSelectTab, tab) },
                    onToggleSave = { onToggleSave(route.hs) },
                    onOpenMarket = onOpenMarket,
                )
                is ScreenRoute.MarketDetail -> {
                    val market = TradarQueries.allMarkets(data).firstOrNull {
                        it.hs == route.hs && it.country == route.country
                    }
                    if (market == null) {
                        FailureScreen("시장 데이터를 찾을 수 없습니다.", onRetry = { onSelectTab(tab) }, onOpenWebApp = onOpenWebApp)
                    } else {
                        MarketDetailScreen(market = market, onBack = { routeBack(onSelectTab, tab) })
                    }
                }
            }
        }
    }
}

private fun routeBack(onSelectTab: (AppTab) -> Unit, tab: AppTab) {
    onSelectTab(tab)
}

@Composable
private fun LoadingScreen() {
    Box(Modifier.fillMaxSize().background(BgLight), contentAlignment = Alignment.Center) {
        CircularProgressIndicator()
    }
}

@Composable
private fun FailureScreen(message: String, onRetry: () -> Unit, onOpenWebApp: () -> Unit) {
    Box(Modifier.fillMaxSize().background(BgLight), contentAlignment = Alignment.Center) {
        Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.padding(24.dp)) {
            Text("데이터 로딩 실패", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            Text(message, color = Muted)
            Button(onClick = onRetry, modifier = Modifier.padding(top = 14.dp)) { Text("다시 시도") }
            Button(onClick = onOpenWebApp, modifier = Modifier.padding(top = 8.dp)) { Text("웹 플랫폼 열기") }
        }
    }
}

private val AppTab.icon: ImageVector
    get() = when (this) {
        AppTab.Home -> Icons.Default.Home
        AppTab.Search -> Icons.Default.Search
        AppTab.Watchlist -> Icons.Default.Star
        AppTab.Alerts -> Icons.Default.Notifications
        AppTab.Assistant -> Icons.AutoMirrored.Filled.Chat
    }
