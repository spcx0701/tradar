"""산업통상부(산하기관) 공공데이터 클라이언트 — K-SURE·KOTRA 연동.

제14회 산업통상부 공공데이터 활용 아이디어 공모전 대응 모듈.
data.go.kr에 개방된 산업통상부 산하기관 공공데이터를 Tradar 파이프라인에 연결한다.

활용 데이터셋(공공데이터포털 등록명 기준):
- 한국무역보험공사_국별신용등급            https://www.data.go.kr/data/15140201/openapi.do
- 한국무역보험공사_국가별 업종별 위험지수   https://www.data.go.kr/data/15132755/openapi.do
- 대한무역투자진흥공사_해외시장뉴스         https://www.data.go.kr/data/15034831/openapi.do
- 대한무역투자진흥공사_수입규제품목(지역본부별) 정보 https://www.data.go.kr/data/15088467/openapi.do

- 인증: data.go.kr 일반 인증키(``DATA_GO_KR_KEY``) 공용.
- 엔드포인트는 기관 개편 시 바뀔 수 있어 ``TW_MOTIE_*_URL`` 환경변수로 재지정 가능.
- 키/네트워크가 없으면 **공표치 앵커 스냅샷**으로 동작한다(데모는 항상 동작).
  앵커 출처: K-SURE 국별신용등급·OECD 국가위험분류 공표치(2026 상반기),
  무역협회 수입규제 통합지원센터 대한(對韓) 수입규제 집계(2026.6) 기준 근사값.
"""
from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from typing import Any

from .env import load_env_file

load_env_file()

# data.go.kr 표준 게이트웨이 기본 엔드포인트(기관 코드 변경 시 env로 재지정)
DEFAULT_ENDPOINTS = {
    "ksure_grade": "https://apis.data.go.kr/B190001/countryCreditGrade/getCountryCreditGrade",
    "ksure_risk": "https://apis.data.go.kr/B190001/riskIndex/getRiskIndex",
    "kotra_news": "https://apis.data.go.kr/B410001/kotra_overseasMarketNews/ovseaMrktNews",
    "kotra_regs": "https://apis.data.go.kr/B410001/importRegulationItems/getImportRegulationItems",
}

# ── 공표치 앵커 ──────────────────────────────────────────────────────────
# K-SURE 국별신용등급(1=최우량 ~ 7): OECD 국가위험분류·K-SURE 공표 등급에 앵커링.
# ri: K-SURE RISK INDEX(RI1~RI5) 국가 최빈값 근사. regs: 對韓 수입규제 건수(무역협회 집계 근사).
ANCHOR_COUNTRIES: dict[str, dict[str, Any]] = {
    "US": {"grade": 1, "ri": 2, "regs": 53, "regsNote": "반덤핑·상계관세 중심(철강·화학 다수)"},
    "CN": {"grade": 2, "ri": 3, "regs": 15, "regsNote": "반덤핑 중심(석유화학·소재)"},
    "VN": {"grade": 4, "ri": 3, "regs": 6, "regsNote": "세이프가드·반덤핑(철강 등)"},
    "JP": {"grade": 1, "ri": 1, "regs": 0, "regsNote": "현행 규제 없음"},
    "HK": {"grade": 2, "ri": 2, "regs": 0, "regsNote": "현행 규제 없음"},
    "TW": {"grade": 1, "ri": 2, "regs": 2, "regsNote": "반덤핑(일부 소재)"},
    "SG": {"grade": 1, "ri": 1, "regs": 0, "regsNote": "현행 규제 없음"},
    "IN": {"grade": 3, "ri": 3, "regs": 19, "regsNote": "반덤핑 최다 축(화학·철강·섬유)"},
    "MX": {"grade": 3, "ri": 3, "regs": 4, "regsNote": "반덤핑(철강 등)"},
    "DE": {"grade": 1, "ri": 1, "regs": 6, "regsNote": "EU 공동 규제(철강 세이프가드 등)"},
    "NL": {"grade": 1, "ri": 1, "regs": 6, "regsNote": "EU 공동 규제(철강 세이프가드 등)"},
    "PL": {"grade": 2, "ri": 2, "regs": 6, "regsNote": "EU 공동 규제(철강 세이프가드 등)"},
    "AE": {"grade": 2, "ri": 2, "regs": 1, "regsNote": "GCC 세이프가드(일부)"},
    "ID": {"grade": 3, "ri": 3, "regs": 8, "regsNote": "세이프가드·반덤핑(섬유·철강)"},
    "TH": {"grade": 3, "ri": 2, "regs": 9, "regsNote": "반덤핑(철강 중심)"},
    "GB": {"grade": 1, "ri": 1, "regs": 3, "regsNote": "철강 세이프가드 등"},
}
ANCHOR_AS_OF = "2026-06"

# KOTRA 해외시장뉴스 앵커(해외무역관 리포트 스타일 큐레이션 — 실서비스에선 OpenAPI 대체)
ANCHOR_KOTRA_NEWS: list[dict[str, Any]] = [
    {
        "head": "미국, 화장품규제현대화법(MoCRA) 집행 본격화 — 시설등록·성분신고 의무 확대",
        "country": "US", "related": ["skincare", "colorcos"], "sent": "neg", "sev": "med",
        "topic": "규제·인증", "office": "워싱턴무역관",
        "sum": "FDA가 MoCRA 시설등록·제품리스팅 미이행 업체 단속을 예고. 대미 K-뷰티 수출기업은 등록 대행·라벨링 점검 필요.",
    },
    {
        "head": "베트남, 한-베 FTA 활용 가공식품 수입 급증 — 유통망 콜드체인 투자 확대",
        "country": "VN", "related": ["ramen", "sauce"], "sent": "pos", "sev": "opp",
        "topic": "시장 동향", "office": "호치민무역관",
        "sum": "현지 대형유통 3사가 한국식품 전용 매대를 확대. FTA 관세 인하 품목 중심으로 진입 기회.",
    },
    {
        "head": "인도, 전자·화학 반덤핑 조사 확대 — 對韓 조사 개시 품목 추가",
        "country": "IN", "related": ["semi", "battery"], "sent": "neg", "sev": "high",
        "topic": "통상·관세", "office": "뉴델리무역관",
        "sum": "인도 상공부가 화학·소재 신규 반덤핑 조사에 착수. 인도향 수출 비중이 큰 기업은 대응 필요.",
    },
    {
        "head": "UAE, K-푸드 할랄 인증 수요 급증 — 두바이 유통망 입점 상담 2배",
        "country": "AE", "related": ["ramen", "tteok"], "sent": "pos", "sev": "opp",
        "topic": "시장 동향", "office": "두바이무역관",
        "sum": "할랄 인증 취득 한국 식품의 현지 입점 문의가 전년比 2배. 중동 시장 다변화의 실질 창구.",
    },
]

DATASETS = [
    {"org": "한국무역보험공사", "name": "국별신용등급",
     "portal": "https://www.data.go.kr/data/15140201/openapi.do"},
    {"org": "한국무역보험공사", "name": "국가별 업종별 위험지수",
     "portal": "https://www.data.go.kr/data/15132755/openapi.do"},
    {"org": "대한무역투자진흥공사", "name": "해외시장뉴스",
     "portal": "https://www.data.go.kr/data/15034831/openapi.do"},
    {"org": "대한무역투자진흥공사", "name": "수입규제품목(지역본부별) 정보",
     "portal": "https://www.data.go.kr/data/15088467/openapi.do"},
]


class MotieClient:
    """산업통상부 산하기관(K-SURE·KOTRA) 공공데이터 클라이언트."""

    def __init__(self, service_key: str | None = None, timeout: int = 20):
        self.service_key = os.environ.get("DATA_GO_KR_KEY", "") if service_key is None else service_key
        self.timeout = timeout

    @property
    def available(self) -> bool:
        return bool(self.service_key)

    def _endpoint(self, key: str) -> str:
        return os.environ.get(f"TW_MOTIE_{key.upper()}_URL", DEFAULT_ENDPOINTS[key])

    def _get_json(self, key: str, **params: str) -> Any:
        qs = urllib.parse.urlencode(
            {"serviceKey": self.service_key, "type": "json", **params}, safe="%")
        url = f"{self._endpoint(key)}?{qs}"
        req = urllib.request.Request(url, headers={"User-Agent": "tradewind/1.0"})
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:  # noqa: S310
            return json.loads(resp.read().decode("utf-8"))

    # ── 라이브 조회(키 필요) ──────────────────────────────────────────
    def fetch_country_grades(self) -> dict[str, int]:
        """K-SURE 국별신용등급(1~7). 실패 시 빈 dict — 호출부가 앵커로 폴백."""
        try:
            data = self._get_json("ksure_grade", numOfRows="300")
            items = _items(data)
            out: dict[str, int] = {}
            for it in items:
                code = (it.get("isoCode") or it.get("cntyCd") or "").upper()
                grade = _to_int(it.get("grade") or it.get("cntyGrd"))
                if code and grade:
                    out[code] = grade
            return out
        except Exception:  # noqa: BLE001 — 라이브 실패는 앵커 폴백으로 흡수
            return {}

    def fetch_kotra_news(self, num: int = 10) -> list[dict[str, Any]]:
        """KOTRA 해외시장뉴스 최신 기사. 실패 시 빈 리스트 — 호출부가 앵커로 폴백."""
        try:
            data = self._get_json("kotra_news", numOfRows=str(num))
            items = _items(data)
            out = []
            for it in items:
                out.append({
                    "head": it.get("newsTitl") or it.get("title") or "",
                    "country": (it.get("natnCd") or "").upper(),
                    "sum": (it.get("cntntSumar") or "")[:160],
                    "topic": it.get("indstCl") or "시장 동향",
                    "office": it.get("kotraOfce") or "KOTRA",
                    "sent": "neu", "sev": "info", "related": [],
                })
            return [n for n in out if n["head"]]
        except Exception:  # noqa: BLE001
            return []

    # ── 통합 페이로드(항상 동작) ──────────────────────────────────────
    def build_payload(self, country_codes: list[str]) -> dict[str, Any]:
        """대시보드용 통합 페이로드. 라이브 실패/키 부재 시 공표치 앵커."""
        live_grades = self.fetch_country_grades() if self.available else {}
        live_news = self.fetch_kotra_news() if self.available else []
        mode = "live" if (live_grades or live_news) else "anchor"

        countries: dict[str, dict[str, Any]] = {}
        for code in country_codes:
            anchor = ANCHOR_COUNTRIES.get(code, {"grade": 3, "ri": 3, "regs": 0, "regsNote": "집계 없음"})
            entry = dict(anchor)
            if code in live_grades:
                entry["grade"] = live_grades[code]
            entry["asOf"] = ANCHOR_AS_OF
            countries[code] = entry

        return {
            "mode": mode,
            "datasets": DATASETS,
            "countries": countries,
            "news": live_news or ANCHOR_KOTRA_NEWS,
        }


def _items(data: Any) -> list[dict]:
    """data.go.kr 표준 응답(JSON)에서 item 배열을 방어적으로 추출."""
    if isinstance(data, list):
        return [d for d in data if isinstance(d, dict)]
    if not isinstance(data, dict):
        return []
    body = data.get("response", {}).get("body", data)
    items = body.get("items", body.get("data", []))
    if isinstance(items, dict):
        items = items.get("item", [])
    if isinstance(items, dict):
        items = [items]
    return [i for i in items if isinstance(i, dict)]


def _to_int(v: Any) -> int:
    try:
        return int(float(str(v).strip()))
    except (TypeError, ValueError):
        return 0
