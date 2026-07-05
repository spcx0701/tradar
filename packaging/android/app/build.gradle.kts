plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.plugin.compose")
}

fun configString(propName: String, envName: String, defaultValue: String = ""): String =
    providers.gradleProperty(propName)
        .orElse(providers.environmentVariable(envName))
        .getOrElse(defaultValue)

fun androidStringLiteral(value: String): String =
    "\"" + value.replace("\\", "\\\\").replace("\"", "\\\"") + "\""

android {
    namespace = "kr.tradewind.app"
    compileSdk = 37

    defaultConfig {
        applicationId = "kr.tradewind.app"
        minSdk = 24
        targetSdk = 34
        versionCode = 2
        versionName = "1.1.0"
        val dataBase = configString("tradarDataBase", "TRADAR_DATA_BASE", "https://tradar.onrender.com/data")
        val apiBase = configString("tradewindApiBase", "TRADEWIND_API_BASE", "https://tradar.onrender.com/api")
        val llmEndpointDefault = if (apiBase.isBlank()) "" else "${apiBase.trimEnd('/')}/advisor"
        val llmEndpoint = configString("koreanLlmEndpoint", "KOREAN_LLM_ENDPOINT", llmEndpointDefault)
        buildConfigField("String", "TRADAR_DATA_BASE", androidStringLiteral(dataBase))
        buildConfigField("String", "KOREAN_LLM_ENDPOINT", androidStringLiteral(llmEndpoint))
        // TWA가 띄울 PWA 주소(라이브 배포 URL). assetlinks.json 으로 도메인 검증.
        manifestPlaceholders["twaUrl"] = "https://tradar.onrender.com/"
        manifestPlaceholders["twaHost"] = "tradar.onrender.com"
    }
    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    buildFeatures {
        compose = true
        buildConfig = true
    }
}

dependencies {
    implementation(platform("androidx.compose:compose-bom:2026.06.01"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    implementation("androidx.activity:activity-compose:1.13.0")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.11.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.11.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.11.0")
    // TWA(전체화면 웹앱) + Custom Tabs
    implementation("com.google.androidbrowserhelper:androidbrowserhelper:2.7.2")
    implementation("androidx.browser:browser:1.10.0")
    testImplementation("junit:junit:4.13.2")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.11.0")
    testImplementation("org.json:json:20240303")
    debugImplementation("androidx.compose.ui:ui-tooling")
}
