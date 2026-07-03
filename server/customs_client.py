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
from typing import Iterable

from .env import load_env_file

load_env_file()

BASE_URL = "https://apis.data.go.kr/1220000/nitemtrade/getNitemtradeList"
DEFAULT_COUNTRY_CODES = [
    "US", "CN", "VN", "JP", "HK", "TW", "SG", "IN", "MX", "DE", "NL", "PL",
    "AE", "ID", "TH", "GB", "LR", "PA", "HU", "AU",
]


class CustomsClient:
    def __init__(self, service_key: str | None = None, timeout: int = 20):
        self.service_key = os.environ.get("DATA_GO_KR_KEY", "") if service_key is None else service_key
        self.timeout = timeout

    @property
    def available(self) -> bool:
        return bool(self.service_key)

    def fetch_item_country(self, hs_sgn: str, start_ym: str, end_ym: str,
                           country_codes: Iterable[str] | None = None) -> list[dict]:
        """품목(HS)·기간별 국가별 수출입실적 조회.

        Args:
            hs_sgn: HS 부호(예 '1902.30' → '190230').
            start_ym, end_ym: 'YYYYMM'.
            country_codes: data.go.kr 필수 파라미터 cntyCd. 없으면 주요 수출국 기본값.
        Returns: [{'year','month','country','exp_usd','exp_kg','imp_usd','imp_kg'}, ...]
        """
        if not self.available:
            raise RuntimeError("DATA_GO_KR_KEY 미설정 — 데모 스냅샷을 사용하세요.")
        rows: list[dict] = []
        for country in country_codes or DEFAULT_COUNTRY_CODES:
            for start, end in self._month_windows(start_ym, end_ym):
                url = self._build_url(hs_sgn, start, end, country)
                req = urllib.request.Request(url, headers={"User-Agent": "tradewind/1.0"})
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:  # noqa: S310
                    body = resp.read().decode("utf-8")
                rows.extend(self._parse(body, fallback_country=country))
        return rows

    def _build_url(self, hs_sgn: str, start_ym: str, end_ym: str, country_code: str) -> str:
        params = {
            "serviceKey": self.service_key,
            "strtYymm": start_ym,
            "endYymm": end_ym,
            "hsSgn": hs_sgn.replace(".", ""),
            "cntyCd": country_code.upper(),
        }
        return f"{BASE_URL}?{urllib.parse.urlencode(params, safe='%')}"

    @staticmethod
    def _month_windows(start_ym: str, end_ym: str, max_months: int = 12) -> list[tuple[str, str]]:
        start_i = _ym_to_index(start_ym)
        end_i = _ym_to_index(end_ym)
        if end_i < start_i:
            return []
        out: list[tuple[str, str]] = []
        cur = start_i
        while cur <= end_i:
            window_end = min(end_i, cur + max_months - 1)
            out.append((_index_to_ym(cur), _index_to_ym(window_end)))
            cur = window_end + 1
        return out

    @staticmethod
    def _parse(body: str, fallback_country: str = "") -> list[dict]:
        rows: list[dict] = []
        root = ET.fromstring(body)
        for item in root.iter("item"):
            def g(tag: str) -> str:
                el = item.find(tag)
                return el.text.strip() if el is not None and el.text else ""
            period = g("year")
            country = g("statCd") or fallback_country
            country_name = g("statCdCntnKor1") or g("statKor") or country
            rows.append({
                "year": period[:4],
                "month": period[5:7] if "." in period else period[4:6],
                "country": country,
                "country_name": country_name,
                "hs": g("hsCd"),
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


def _ym_to_index(ym: str) -> int:
    return int(ym[:4]) * 12 + int(ym[4:6]) - 1


def _index_to_ym(index: int) -> str:
    year = index // 12
    month = index % 12 + 1
    return f"{year:04d}{month:02d}"
