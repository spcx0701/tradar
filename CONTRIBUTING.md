# 기여 가이드

무역풍(Tradewind)에 관심 가져주셔서 감사합니다.

## 개발 환경
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt

# 데이터 파이프라인(관세청 스냅샷 → AI 산출물 → 정적 JSON)
python scripts/generate_snapshot.py      # 스냅샷 생성/갱신
python scripts/build_app_data.py         # 예측·레이더 결과를 app/data/*.json 으로 빌드

# 웹앱(정적 PWA)
python scripts/serve.py                  # http://localhost:5183

# 라이브 API 서버(FastAPI)
uvicorn server.main:app --reload

# 테스트 / 린트
pytest -q
ruff check server scripts
```

## 원칙
- **데모는 항상 동작해야 한다.** 외부 키 없이도 스냅샷·자체 NLG로 완결되게 유지.
- **AI 출력은 근거(수치)와 함께.** 환각을 만들지 않는다.
- 한국어 우선. 코드 주석·문서는 한국어, 식별자는 영어.

## 실데이터 연동
`DATA_GO_KR_KEY` 발급 후 `server/customs_client.py`로 스냅샷을 실데이터로 교체할 수 있습니다.
