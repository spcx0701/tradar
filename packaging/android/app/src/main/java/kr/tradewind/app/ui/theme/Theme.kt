package kr.tradewind.app.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Typography
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

val Navy = Color(0xFF0A2540)
val Blue = Color(0xFF0B5FA5)
val Teal = Color(0xFF12B3A6)
val Amber = Color(0xFFF59E0B)
val Surge = Color(0xFF16A34A)
val Cool = Color(0xFFDC2626)
val Ink = Color(0xFF16233A)
val Muted = Color(0xFF5B6B82)
val BgLight = Color(0xFFF5F8FC)

private val LightColors = lightColorScheme(
    primary = Blue, onPrimary = Color.White,
    secondary = Teal, tertiary = Amber,
    background = BgLight, surface = Color.White,
    onBackground = Ink, onSurface = Ink,
)
private val DarkColors = darkColorScheme(
    primary = Teal, onPrimary = Navy, secondary = Blue, tertiary = Amber,
)

@Composable
fun TradewindTheme(dark: Boolean = isSystemInDarkTheme(), content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = if (dark) DarkColors else LightColors,
        typography = Typography(),
        content = content,
    )
}
