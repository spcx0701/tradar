# 데이터 출처

## 필수 — 관세청 공공데이터
무역풍의 모든 분석은 관세청 수출입무역통계 위에서 동작한다.

| # | 데이터명 | 제공기관 | 획득 방법 / URL | 서비스 내 활용 |
|---|----------|----------|------------------|----------------|
| 1 | **품목별 국가별 수출입실적(GW)** | 관세청 | 공공데이터포털 OpenAPI<br>`apis.data.go.kr/1220000/nitemtrade`<br>https://www.data.go.kr/data/15100475/openapi.do | 핵심 시계열 — HS×국가×월 수출금액·중량. 수요예측·레이더·상담의 원천 |
| 2 | 품목별 수출입실적(GW) | 관세청 | 공공데이터포털 `15101609` | 품목 총수출 추세·시장 점유 산정 |
| 3 | 국가별 수출입실적(GW) | 관세청 | 공공데이터포털 `15101612` | 국가별 수출 비중(B2G 대시보드) |
| 4 | 국가별 관세율표 | 관세청 | 공공데이터포털 `15051176` | (로드맵) FTA·관세율 융합 landed-cost |
| 5 | 표준품명(HSK) | 관세청 | 공공데이터포털 `15049721` | HS코드↔품명 매핑·자동분류(로드맵) |

- 관세청 수출입무역통계 누리집: https://tradedata.go.kr
- 국가관세종합정보시스템(UNI-PASS): https://unipass.customs.go.kr
- 관세청 빅데이터 포털(수출입트렌드): https://bigdata.customs.go.kr

## 선택 — 타 기관 융합(로드맵)
| 데이터 | 기관 | 활용 |
|--------|------|------|
| 수출지원사업·해외시장 정보 | KOTRA | 떠오르는 시장에 매칭되는 지원사업 추천 |
| 환율 | 한국은행/관세청 환율 | 현지 통화 환산·가격 경쟁력 보정 |
| 해외 인구·소비 통계 | 통계청/유엔 | 시장 잠재력 정규화 |

## 거래 인텔리전스 자동수집
`거래 인텔리전스` 화면은 회사·상품·시장·바이어 흐름을 별도 payload인 `window.TRADAR_TRADE_INTEL`로 소비한다.

키는 저장소에 커밋하지 않는다. 로컬/운영 환경에서는 `.env` 또는 환경변수로 주입하며, 서버와 동기화 스크립트는 `.env`를 자동 로딩한다.

키 발급/연결 표:

| 키 | 발급/준비 위치 | 연결 변수 | 현재 구현 상태 |
|----|----------------|-----------|----------------|
| 관세청 품목별 국가별 수출입실적(GW) | https://www.data.go.kr/data/15100475/openapi.do 에서 로그인 후 `활용신청` | `DATA_GO_KR_KEY` | 공식 HS×국가×월 통계, 평균단가 보강 |
| 공개 B/L CSV | ImportYeti/Panjiva/내부 리서치에서 내려받은 선적 CSV 또는 고객 업로드 | `TRADE_INTEL_PUBLIC_BL_CSV` | 기업·바이어·상품·물량 흐름 수집 |
| 공개 B/L JSON API | records/results/data 배열을 반환하는 공개 B/L API | `TRADE_INTEL_PUBLIC_BL_API_URL`, `TRADE_INTEL_PUBLIC_BL_API_KEY` | 커넥터 정규화 지원 |
| ImportYeti API | https://www.importyeti.com/yeti-api 및 https://data.importyeti.com/ | `IMPORTYETI_API_KEY` | company supplier relationship 정규화 |
| AI 답변 보강 LLM | 운영자가 쓰는 Solar/HyperCLOVA X 등 | `TW_LLM_PROVIDER`, `TW_LLM_KEY` | 키 없으면 근거 기반 기본 답변 사용 |

키 상태 확인:

```bash
python scripts/check_trade_intel_keys.py
```

자동수집 커맨드:

```bash
DATA_GO_KR_KEY=... \
TRADE_INTEL_PUBLIC_BL_CSV=server/data/public_bl_sample.csv \
python scripts/sync_trade_intel.py
```

실행하면 `app/data/tradar.js`의 `window.TRADAR_TRADE_INTEL`이 재생성되고, 운영 리포트가 기본값 `server/data/trade_intel_last_run.json`에 저장된다. 리포트에는 커넥터별 `success/degraded/failed/skipped`, 수집 레코드 수, 품질 점수, stale 기준, 사용자에게 보여야 할 경고가 들어간다.

ImportYeti 회사 endpoint 또는 공개 B/L JSON API를 직접 붙이는 경우:

```bash
DATA_GO_KR_KEY=... IMPORTYETI_API_KEY=... \
python scripts/sync_trade_intel.py --product ramen --importyeti-company wal-mart

DATA_GO_KR_KEY=... TRADE_INTEL_PUBLIC_BL_API_KEY=... \
python scripts/sync_trade_intel.py --product ramen --public-bl-api-url https://example.com/public-bl
```

운영 옵션:

```bash
# 커넥터 하나라도 실패하면 즉시 실패
python scripts/sync_trade_intel.py --public-bl-csv server/data/public_bl_sample.csv --strict

# 실행 리포트 저장 위치와 stale 기준 변경
python scripts/sync_trade_intel.py \
  --public-bl-csv server/data/public_bl_sample.csv \
  --report-out server/data/trade_intel_last_run.json \
  --stale-after-hours 48

# 관세청 공식 API 호출 상한 조정
python scripts/sync_trade_intel.py \
  --public-bl-csv server/data/public_bl_sample.csv \
  --customs-timeout 8 \
  --customs-market-limit 3

# PR/배포 전 감사
python scripts/audit_trade_intel.py --max-age-hours 72
```

기본 동기화는 공개 B/L/CSV 등에서 실제 거래 흐름이 들어온 품목만 관세청 공식 HS 통계로 보강한다. 카탈로그 전체 20개 이상 품목을 기본 국가 20개로 모두 조회하지 않기 때문에, 외부 API 지연 하나가 전체 실행을 오래 붙잡지 않는다. 필요하면 `--product`로 특정 품목을 명시해 보강 범위를 넓힌다.

현재 저장소 샘플 실행은 공개 B/L CSV 9건을 성공 수집한다. `DATA_GO_KR_KEY`가 없으면 관세청 공식 HS 커넥터가 `skipped`로 기록되어 전체 상태가 `degraded`가 된다. 이 상태는 실패가 아니라 “공개 B/L/CSV 값은 표시 가능하지만 공식 API 최신 보강은 빠진 상태”를 뜻한다.

수집/보정 순서:

| 계층 | 자동수집 원천 | 구현 파일 | 서비스 내 표기 |
|------|---------------|-----------|----------------|
| 공식 | 관세청 품목별 국가별 수출입실적 API | `server/customs_client.py` | `공식` |
| 공개 B/L | 공개 선하증권 API, ImportYeti 회사 endpoint, 또는 공개 B/L에서 내려받은 CSV | `server/trade_intelligence.py`, `scripts/sync_trade_intel.py` | `공개 B/L` |
| 추정 | 공식 HS 평균단가 × 공개 B/L 물량 | `server/trade_intelligence.py` | `추정` |
| 업로드 | 사용자 CSV·ERP·견적서 | 같은 CSV 스키마의 `source_tier=upload` | `업로드` |

무료 공개 데이터만으로는 기업별 실제 계약 단가가 항상 공개되지 않는다. 따라서 자동수집 커넥터는 회사/바이어/물량 흐름을 공개 B/L에서 가져오고, 단가·거래액은 공식 평균단가로 추정해 `priceStatus=estimated`로 표시한다. 사용자가 내부 실거래 CSV를 올리면 `source_tier=upload`, `unit_price_usd`를 통해 확정 단가로 승격된다.

## 데모 데이터에 관하여
저장소의 `server/data/snapshot.json`은 위 #1 API와 **동일한 스키마**를 따르는 **대표 스냅샷**이다.

- 2024년 품목별 총수출 규모는 관세청·무역통계 **공표치에 앵커링**(예: 라면 약 12.4억 달러, 김 약 10억 달러, 화장품 약 102억 달러 등).
- 시장별 추세·계절성은 실제 한류 수출 패턴을 반영(예: 화장품 對중국 둔화, 김·김치 對미국 급등).
- 시드 고정으로 **재현 가능**하며, 개인·기업 식별정보를 포함하지 않는다.
- `DATA_GO_KR_KEY` 발급 후 `server/customs_client.py`로 실데이터 동기화 시 스냅샷이 대체된다.

생성: `python scripts/generate_snapshot.py`
