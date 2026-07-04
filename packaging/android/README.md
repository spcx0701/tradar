# Tradar Android (네이티브 Compose + TWA)

웹 플랫폼과 **병행**하는 Android companion 앱입니다. 1차 MVP는 현장 조회에 필요한 기능을 Kotlin/Jetpack Compose로 네이티브 구현하고, 마켓맵·스코어·뉴스 같은 전체 대시보드는 TWA/Custom Tabs로 연결합니다.

## MVP 화면

- **홈** — 데이터 기간, 품목/국가 수, 상위 기회, 리스크 경보, 전체 플랫폼 열기.
- **검색** — HS코드, 품목명, 카테고리, 국가명, 급등/상승/둔화 상태 검색.
- **관심목록** — 저장한 품목과 해당 품목의 최고 기회 시장.
- **알림센터** — 리스크 상위 시장과 급성장 기회 시장을 로컬 데이터에서 생성.
- **AI 무역참모** — 서버 `/api/advisor` 국산 LLM 프록시를 호출하고, 실패 시 로컬 수치에 근거한 결정적 한국어 요약으로 폴백.
- **상세 화면** — 품목 상세와 국가×품목 시장 상세.

## 데이터 동작

앱은 `catalog.json`과 `radar.json` 두 파일을 사용합니다.

1. `https://tradar.onrender.com/data/catalog.json`
2. `https://tradar.onrender.com/data/radar.json`
3. 실패 시 앱 번들 `assets/catalog.json`, `assets/radar.json`

따라서 네트워크가 없거나 원격 JSON이 아직 배포되지 않아도 번들 스냅샷으로 실행됩니다.

전체 웹앱은 PWA를 TWA/Custom Tabs로 열어 예보·AI 참모·리포트·대시보드까지 같은 Render 단일 오리진에서 사용합니다.

## 구조
```
app/src/main/
  java/kr/tradewind/app/
    MainActivity.kt        Compose 진입 + Custom Tabs 실행
    data/                  원격/번들 데이터 로딩, LLM 클라이언트, 관심목록 저장소
    domain/                모델, JSON 파서, 검색/알림/요약 로직
    ui/                    앱 라우팅, 화면, 컴포넌트, 테마
  assets/                  오프라인용 catalog/radar 번들 데이터
  res/                     아이콘·테마·문자열·TWA asset_statements
```

## 빌드
Android Studio(Koala+) 또는 CLI:
```bash
cd packaging/android
./gradlew :app:testDebugUnitTest
./gradlew :app:assembleDebug      # → app/build/outputs/apk/debug/app-debug.apk
./gradlew :app:bundleRelease      # Play Store AAB
```
요구: JDK 17, Android SDK 34. `applicationId = kr.tradewind.app`.

국산 LLM 연결 빌드:
```bash
# 서버는 TW_LLM_PROVIDER/TW_LLM_KEY/TW_LLM_MODEL/TW_LLM_BASE_URL 을 환경변수로 가진 FastAPI 배포본
./gradlew :app:assembleDebug -PtradewindApiBase=https://tradar.onrender.com/api

# 또는 advisor 엔드포인트를 직접 지정
./gradlew :app:assembleDebug -PkoreanLlmEndpoint=https://tradar.onrender.com/api/advisor
```

앱 APK에 LLM 제공자 키를 넣지 않습니다. 키는 서버 환경변수에만 있고 Android는 `/api/advisor`만 호출합니다.

## TWA 도메인 검증
배포 도메인 루트에 `/.well-known/assetlinks.json` 을 올리면 TWA가 전체화면(주소창 제거)으로 동작합니다.
`res/values/strings.xml`의 `asset_statements` 와 `app/build.gradle.kts`의 `twaUrl/twaHost` 를 실제 배포 도메인으로 맞추세요.

> 참고: Play Store 서명, 실제 푸시 알림, 카메라/바코드/OCR 스캔은 다음 단계 범위입니다.

## 라이선스

Android 모바일 클라이언트는 저장소 본문과 같이 [AGPL-3.0-or-later](../../LICENSE)로 배포되며,
앱스토어 배포를 위한 AGPL 7조 추가 허가가 적용됩니다. 이 추가 허가는 `packaging/android` 아래의
모바일 클라이언트에만 적용되고, `server/`의 FastAPI 백엔드와 `app/`의 웹/PWA 클라이언트에는 적용되지
않습니다. 정확한 범위는 [LICENSE](../../LICENSE)와 [NOTICE](../../NOTICE)를 확인하세요.
