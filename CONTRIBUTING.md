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

## Pull request 절차

1. `main`에서 새 브랜치를 만들고 변경 범위를 작게 유지합니다.
2. 사용자에게 보이는 동작, API 응답, 데이터 산출 로직이 바뀌면 관련 테스트를 추가하거나 기존 테스트를 갱신합니다.
3. PR 설명에는 변경 이유, 검증 명령, UI/API 영향, 보안 또는 데이터 취급 영향이 있으면 함께 적습니다.
4. 리뷰에서 요청된 수정은 같은 PR 안에서 반영하고, 관련 대화가 끝난 뒤 머지합니다.

## 기여 요구 사항

- Python 코드는 `ruff check server scripts`를 통과해야 합니다.
- 서버와 데이터 파이프라인 변경은 `pytest -q`를 통과해야 합니다.
- API 계약이 바뀌면 `README.md`의 API 인터페이스 표와 테스트를 함께 갱신합니다.
- 보안 관련 변경은 `SECURITY.md`의 비공개 신고 절차와 충돌하지 않아야 합니다.
- 새 기능에는 가능하면 회귀 테스트를 추가하고, 테스트를 추가하지 못한 경우 PR에 이유를 남깁니다.

## 원칙
- **데모는 항상 동작해야 한다.** 외부 키 없이도 스냅샷·자체 NLG로 완결되게 유지.
- **AI 출력은 근거(수치)와 함께.** 환각을 만들지 않는다.
- 한국어 우선. 코드 주석·문서는 한국어, 식별자는 영어.

## 실데이터 연동
`DATA_GO_KR_KEY` 발급 후 `server/customs_client.py`로 스냅샷을 실데이터로 교체할 수 있습니다.
