# 무역풍 Android (네이티브 Compose + TWA)

웹과 **병행**하는 네이티브 안드로이드 앱입니다.

- **네이티브 홈** — Jetpack Compose로 ‘지금 떠오르는 한류 수출 시장’을 네이티브 UI로 렌더
  (데이터: 라이브 JSON → 실패 시 앱 번들 `assets/radar.json` 폴백 → 오프라인 동작).
- **전체 웹앱** — 예보·AI 참모·리포트·B2G는 PWA를 **TWA(Trusted Web Activity)/Custom Tabs**로 전체화면 실행
  (주소창 없는 네이티브 앱 경험). 단일 코드/배포로 웹·앱 기능 동등.

## 구조
```
app/src/main/
  java/kr/tradewind/app/
    MainActivity.kt        Compose 진입(네이티브 홈 + 웹앱 실행)
    ui/HomeScreen.kt       네이티브 홈 화면(떠오르는 시장)
    ui/theme/Theme.kt      브랜드 테마
    data/Repository.kt     라이브 API → 번들 JSON 폴백
  assets/radar.json        오프라인용 번들 데이터(scripts/build_app_data.py 산출)
  res/…                    아이콘·테마·문자열·TWA asset_statements
```

## 빌드
Android Studio(Koala+) 또는 CLI:
```bash
# 최초 1회 래퍼 생성(이 저장소는 바이너리 wrapper jar를 커밋하지 않음)
gradle wrapper --gradle-version 8.9
./gradlew :app:assembleDebug      # → app/build/outputs/apk/debug/app-debug.apk
./gradlew :app:bundleRelease      # Play Store AAB
```
요구: JDK 17, Android SDK 34. `applicationId = kr.tradewind.app`.

## TWA 도메인 검증
배포 도메인 루트에 `/.well-known/assetlinks.json` 을 올리면 TWA가 전체화면(주소창 제거)으로 동작합니다.
`res/values/strings.xml`의 `asset_statements` 와 `app/build.gradle.kts`의 `twaUrl/twaHost` 를 실제 배포 도메인으로 맞추세요.

> 참고: 본 저장소의 **실행 확인용 핵심 산출물은 웹 PWA**(설치 없이 URL·QR로 즉시 실행)이며,
> 안드로이드 앱은 이를 네이티브로 감싼 병행 산출물입니다.

## 라이선스

Android 모바일 클라이언트는 저장소 본문과 같이 [AGPL-3.0-or-later](../../LICENSE)로 배포되며,
앱스토어 배포를 위한 AGPL 7조 추가 허가가 적용됩니다. 이 추가 허가는 `packaging/android` 아래의
모바일 클라이언트에만 적용되고, `server/`의 FastAPI 백엔드와 `app/`의 웹/PWA 클라이언트에는 적용되지
않습니다. 정확한 범위는 [LICENSE](../../LICENSE)와 [NOTICE](../../NOTICE)를 확인하세요.
