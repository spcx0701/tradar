"""관세청 공공데이터 오픈API 클라이언트 (실 서비스 동기화 경로).

data.go.kr ``관세청_품목별 국가별 수출입실적(GW)`` API를 호출해
HS코드×국가×월 수출입실적을 받아 snapshot.json 형식으로 적재한다.

- 엔드포인트: https://apis.data.go.kr/1220000/nitemtrade/getNitemtradeList
- 인증: data.go.kr 일반 인증키(serviceKey). 환경변수 ``DATA_GO_KR_KEY`` 로 주입.
- 외부 의존성 없이 표준 라이브러리(urllib)만 사용.

인증키가 없으면 데모 스냅샷(scripts/generate_snapshot.py)을 사용한다.
이 모듈은 키가 주입된 운영 환경에서 ``sync_snapshot()`` 으로 실데이터를 적재한다.
"""
from __future__ import annotations

import os
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

BASE_URL = "https://apis.data.go.kr/1220000/nitemtrade/getNitemtradeList"


class CustomsClient:
    def __init__(self, service_key: str | None = None, timeout: int = 20):
        self.service_key = service_key or os.environ.get("DATA_GO_KR_KEY", "")
        self.timeout = timeout

    @property
    def available(self) -> bool:
        return bool(self.service_key)

    def fetch_item_country(self, hs_sgn: str, start_ym: str, end_ym: str) -> list[dict]:
        """품목(HS)·기간별 국가별 수출입실적 조회.

        Args:
            hs_sgn: HS 부호(예 '1902.30' → '190230').
            start_ym, end_ym: 'YYYYMM'.
        Returns: [{'year','month','country','exp_usd','exp_kg','imp_usd','imp_kg'}, ...]
        """
        if not self.available:
            raise RuntimeError("DATA_GO_KR_KEY 미설정 — 데모 스냅샷을 사용하세요.")
        params = {
            "serviceKey": self.service_key,
            "strtYymm": start_ym,
            "endYymm": end_ym,
            "hsSgn": hs_sgn.replace(".", ""),
        }
        url = f"{BASE_URL}?{urllib.parse.urlencode(params, safe='%')}"
        req = urllib.request.Request(url, headers={"User-Agent": "tradewind/1.0"})
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:  # noqa: S310
            body = resp.read().decode("utf-8")
        return self._parse(body)

    @staticmethod
    def _parse(body: str) -> list[dict]:
        rows: list[dict] = []
        root = ET.fromstring(body)
        for item in root.iter("item"):
            def g(tag: str) -> str:
                el = item.find(tag)
                return el.text.strip() if el is not None and el.text else ""
            # API 필드: year, statKor(국가명), expDlr(수출금액), expWgt, impDlr, impWgt
            rows.append({
                "year": g("year"),
                "country_name": g("statKor"),
                "exp_usd": _to_int(g("expDlr")),
                "exp_kg": _to_int(g("expWgt")),
                "imp_usd": _to_int(g("impDlr")),
                "imp_kg": _to_int(g("impWgt")),
            })
        return rows


def _to_int(s: str) -> int:
    try:
        return int(float(s.replace(",", ""))) if s else 0
    except ValueError:
        return 0
