# Tradar Android Commercial MVP Design

## Purpose

Build the first commercial-quality Android MVP for Tradar as a native Kotlin companion app, not only a web wrapper. The MVP should feel useful in a field setting: quick market lookup, saved watch items, risk/opportunity alerts, concise AI-style summaries, and a reliable path into the full web dashboard.

## Current Baseline

The existing Android project lives in `packaging/android`. It already has a small Jetpack Compose home screen, a repository that reads `radar.json`, bundled `radar.json` and `catalog.json` assets, and a Custom Tabs/TWA entry to the hosted web app. It does not yet have native navigation, search, product detail screens, local watch state, alerts UI, parser tests, app state tests, a committed Gradle wrapper executable/jar pair, or Android CI coverage.

## Goals

- Provide a native Compose app shell with bottom navigation for Home, Search, Watchlist, Alerts, and Assistant.
- Parse both `radar.json` and `catalog.json` into typed Kotlin domain models.
- Support offline-first startup by loading bundled assets when remote JSON is unavailable.
- Add quick product and market search across HS code, Korean product name, category, country, and status.
- Add product detail and market detail views with opportunity, risk, YoY, six-month forecast growth, recent export value, and plain Korean interpretation.
- Add a local watchlist backed by `SharedPreferences` so saved products survive app restarts.
- Add an alerts center generated from risk markets and fast-growing opportunities.
- Add an assistant screen that produces deterministic, evidence-based Korean summaries from the local data.
- Keep full dashboard access through Custom Tabs/TWA for map, score, news, and richer desktop-oriented views.
- Restore a reproducible Android build surface with Gradle wrapper files, unit tests, and debug assembly instructions.

## Non-Goals

- No Play Store release, signing-key flow, or store listing in this phase.
- No real push notification backend in this phase.
- No camera, barcode, or OCR scanner in this phase.
- No full native reimplementation of the web treemap, score dashboard, news intelligence, or generative chat workflow.
- No mutation of existing deliverables, PDFs, or business-plan documents.

## User Experience

The app opens to a dense but calm command screen:

- Top summary: generated data period, number of products, number of countries, and offline/remote data status.
- Opportunity strip: top markets sorted by Tradar opportunity score.
- Risk strip: cooling markets sorted by risk score.
- Primary action: open the full Tradar platform in Custom Tabs/TWA.

Bottom navigation exposes five tabs:

- Home: summary, top opportunities, risk highlights, and full-platform button.
- Search: searchable product and market list with filters for category and status.
- Watchlist: saved products and their best markets, with remove controls.
- Alerts: generated risk and opportunity alerts with severity, reason, and related product/country.
- Assistant: deterministic Korean Q&A suggestions and generated evidence summaries such as "미국 라면 시장 요약".

Detail views use full-screen Compose navigation. Product detail shows catalog facts plus the country's best market rows from `by_product`. Market detail shows one market row with status, opportunity, risk, growth metrics, recent export value, and interpretation text.

## Architecture

Use a small MVVM-style structure without introducing heavy framework complexity:

- `data`: asset/remote JSON loading, JSON parsing, local persistence, repository facade.
- `domain`: typed models and pure query/summary functions.
- `ui`: Compose screens, reusable components, navigation state, and theme.
- `MainActivity`: dependency creation and app composition only.

The repository is the boundary between Android IO and pure app behavior. JSON parsing and query logic should be testable on the JVM without launching Android UI.

## Data Flow

1. App starts and creates `TradarRepository`.
2. Repository tries remote static JSON with short timeouts.
3. If remote fetch fails or JSON is invalid, repository loads bundled `assets/radar.json` and `assets/catalog.json`.
4. Parsed data is exposed as an immutable `TradarData` object.
5. UI screens derive filtered lists, watchlist rows, alerts, and assistant summaries from `TradarData`.
6. Watchlist state is read from and written to `SharedPreferences` as a stable set of HS codes.

## Error Handling

- If remote data fails, the app silently uses bundled assets and marks the source as offline snapshot.
- If both remote and bundled data fail, the UI shows a blocking error state with a retry action and a full-platform fallback button.
- JSON parsing should ignore unknown fields and use stable defaults for optional numeric fields.
- Search empty states should explain that no product or market matched the entered term.
- Watchlist empty state should show saved-item affordances through Search and Home rows.

## Testing

Use test-first implementation for behavior:

- Parser tests for catalog and radar JSON.
- Repository source tests for remote-failure asset fallback.
- Query tests for product search, market search, top opportunities, risk alerts, and assistant summaries.
- Watchlist tests for stable add/remove/toggle behavior.
- A lightweight Compose smoke test can be added if the local Android test stack is available; otherwise keep this phase focused on JVM unit tests and debug assembly.

## Build And Verification

The implementation should leave these commands as the expected verification surface from `packaging/android`:

```bash
./gradlew :app:testDebugUnitTest
./gradlew :app:assembleDebug
```

If the local machine lacks Android SDK configuration, the repo still needs committed wrapper files and instructions so Android Studio or CI can run the same commands.

## Acceptance Criteria

- The Android app has native Home, Search, Watchlist, Alerts, Assistant, Product Detail, and Market Detail surfaces.
- The app can start and show bundled data with network disabled.
- Search returns relevant products and markets by HS code, Korean product name, category, country, and status.
- Watchlist state persists across app restarts.
- Alerts and assistant summaries are deterministic and grounded in parsed numeric data.
- The full web platform remains reachable through Custom Tabs/TWA.
- Android unit tests cover parser, query, assistant, and watchlist behavior.
- The Android project has a reproducible Gradle wrapper path and documented verification commands.
