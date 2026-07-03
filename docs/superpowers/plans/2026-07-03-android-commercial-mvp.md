# Android Commercial MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a commercial-quality Kotlin/Jetpack Compose Android MVP for Tradar with native Home, Search, Watchlist, Alerts, Assistant, Product Detail, Market Detail, offline data fallback, tests, and reproducible Gradle wrapper.

**Architecture:** Keep the app small and native: pure domain/query code, Android IO repositories, and Compose screens. The full web dashboard remains reachable through Custom Tabs/TWA, while field-oriented workflows are native.

**Tech Stack:** Kotlin, Android Gradle Plugin, Jetpack Compose Material 3, Coroutines, org.json, SharedPreferences, JVM unit tests.

---

### Task 1: Domain Models, Parser, And Query Tests

**Files:**
- Create: `packaging/android/app/src/main/java/kr/tradewind/app/domain/Models.kt`
- Create: `packaging/android/app/src/main/java/kr/tradewind/app/domain/TradarParser.kt`
- Create: `packaging/android/app/src/main/java/kr/tradewind/app/domain/TradarQueries.kt`
- Create: `packaging/android/app/src/test/java/kr/tradewind/app/domain/TradarParserTest.kt`
- Modify: `packaging/android/app/build.gradle.kts`

- [ ] **Step 1: Write failing parser/query tests**

Add tests that parse representative catalog/radar JSON, assert product and country counts, assert top/risk market parsing, assert product search by HS/name/category, and assert market search by Korean country/status.

- [ ] **Step 2: Run tests and confirm RED**

Run from `packaging/android`:

```bash
./gradlew :app:testDebugUnitTest --tests "kr.tradewind.app.domain.TradarParserTest"
```

Expected: fails because `TradarParser`, `TradarQueries`, and model classes do not exist.

- [ ] **Step 3: Implement minimal domain and parser**

Add immutable domain models for `Product`, `Market`, `TradarCatalog`, `TradarRadar`, `TradarData`, and `DataSource`. Implement `TradarParser.parseCatalog`, `parseRadar`, and `parseData` using `org.json.JSONObject`, ignoring unknown fields and defaulting missing optional numerics to `0.0`.

- [ ] **Step 4: Implement query helpers**

Add pure functions for `searchProducts`, `searchMarkets`, `marketsForProduct`, `topOpportunities`, `riskAlerts`, and `generatedAlerts`.

- [ ] **Step 5: Run tests and confirm GREEN**

Run the same targeted test command and confirm all parser/query tests pass.

### Task 2: Repository And Watchlist State

**Files:**
- Replace: `packaging/android/app/src/main/java/kr/tradewind/app/data/Repository.kt`
- Create: `packaging/android/app/src/main/java/kr/tradewind/app/data/WatchlistStore.kt`
- Create: `packaging/android/app/src/test/java/kr/tradewind/app/data/WatchlistStoreTest.kt`

- [ ] **Step 1: Write failing watchlist tests**

Add a fake in-memory preferences adapter and assert stable add/remove/toggle behavior, duplicate prevention, and sorted HS output.

- [ ] **Step 2: Run watchlist tests and confirm RED**

Run:

```bash
./gradlew :app:testDebugUnitTest --tests "kr.tradewind.app.data.WatchlistStoreTest"
```

Expected: fails because `WatchlistStore` does not exist.

- [ ] **Step 3: Implement repository facade**

Replace the thin `Repository` with `TradarRepository`, loading `catalog.json` and `radar.json` from remote first and assets second. Return `Result<TradarData>` or a sealed UI-friendly load state without throwing to callers.

- [ ] **Step 4: Implement watchlist persistence**

Implement `WatchlistStore` over a small `KeyValueStore` interface plus a `SharedPreferences` implementation. Store HS codes as a stable pipe-delimited string to keep unit tests JVM-only.

- [ ] **Step 5: Run repository/watchlist tests**

Run targeted tests and confirm GREEN.

### Task 3: Compose Navigation And Native Screens

**Files:**
- Replace: `packaging/android/app/src/main/java/kr/tradewind/app/MainActivity.kt`
- Replace: `packaging/android/app/src/main/java/kr/tradewind/app/ui/HomeScreen.kt`
- Create: `packaging/android/app/src/main/java/kr/tradewind/app/ui/TradarApp.kt`
- Create: `packaging/android/app/src/main/java/kr/tradewind/app/ui/AppState.kt`
- Create: `packaging/android/app/src/main/java/kr/tradewind/app/ui/Components.kt`
- Create: `packaging/android/app/src/main/java/kr/tradewind/app/ui/Screens.kt`
- Modify: `packaging/android/app/src/main/java/kr/tradewind/app/ui/theme/Theme.kt`

- [ ] **Step 1: Add UI state helpers**

Create `AppTab`, `ScreenRoute`, `TradarUiState`, and screen selection state with no external navigation dependency.

- [ ] **Step 2: Build shared components**

Add reusable cards, status chips, metric rows, empty states, primary action buttons, search field, and bottom navigation.

- [ ] **Step 3: Implement screens**

Implement Home, Search, Watchlist, Alerts, Assistant, Product Detail, and Market Detail screens. Keep text dense and operational, not marketing-heavy.

- [ ] **Step 4: Wire MainActivity**

Create repository and watchlist store in `MainActivity`, load data in Compose with retry, and keep Custom Tabs full-platform action.

- [ ] **Step 5: Compile check**

Run:

```bash
./gradlew :app:compileDebugKotlin
```

Expected: Kotlin compiles.

### Task 4: Gradle Wrapper, Android Test Surface, And Docs

**Files:**
- Create: `packaging/android/gradlew`
- Create: `packaging/android/gradle/wrapper/gradle-wrapper.jar`
- Modify: `packaging/android/gradle/wrapper/gradle-wrapper.properties`
- Modify: `packaging/android/README.md`
- Modify: `.github/workflows/ci.yml`

- [ ] **Step 1: Restore wrapper**

Add executable `gradlew` and wrapper jar compatible with the wrapper properties.

- [ ] **Step 2: Add Android CI job**

Add an Android job that sets up JDK 17, installs Android SDK through GitHub-hosted runner tooling, and runs `./gradlew :app:testDebugUnitTest`.

- [ ] **Step 3: Update Android README**

Document native MVP screens, offline data behavior, wrapper usage, and verification commands.

- [ ] **Step 4: Run full Android verification**

Run from `packaging/android`:

```bash
./gradlew :app:testDebugUnitTest
./gradlew :app:assembleDebug
```

Expected: tests and debug APK build pass when Android SDK is available.

### Task 5: Final Review

**Files:**
- All Android files touched above.

- [ ] **Step 1: Run final git diff review**

Review only Android, CI, and plan/doc changes. Confirm existing deliverables and unrelated dirty files were not edited.

- [ ] **Step 2: Run verification-before-completion**

Use fresh command outputs for test/build claims. If Android SDK is unavailable locally, report the exact blocker and the verification surface that was made reproducible.

- [ ] **Step 3: Commit implementation**

Stage only implementation files and commit with:

```bash
git commit -m "feat: build Android commercial MVP"
```
