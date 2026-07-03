package kr.tradewind.app.ui

enum class AppTab(val label: String) {
    Home("홈"),
    Search("검색"),
    Watchlist("관심"),
    Alerts("알림"),
    Assistant("AI"),
}

sealed interface ScreenRoute {
    data object Tabs : ScreenRoute
    data class ProductDetail(val hs: String) : ScreenRoute
    data class MarketDetail(val hs: String, val country: String) : ScreenRoute
}
