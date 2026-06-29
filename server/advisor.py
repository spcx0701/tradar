"""AI 무역참모 '바람이' — 수치 근거 기반 상담(grounded NLG).

사용자의 한국어 질문에서 품목·국가·의도를 추출하고, 예측·레이더 엔진의 결과를
근거(evidence)로 묶어 한국어 답변을 생성한다.

- 데모: 외부 호출 없이 검색·규칙 기반 NLG로 항상 동작(오프라인).
- 운영: 동일한 evidence 팩을 **국산 LLM**(업스테이지 Solar·네이버 HyperCLOVA X 등)
  어댑터에 넘겨 자연스러운 문장으로 다듬는다. 어댑터 미설정 시 데모 NLG로 폴백.

핵심: 모든 문장은 실제 수출 통계 수치에 근거하며, 근거를 함께 반환한다(환각 차단).
"""
from __future__ import annotations

import re

from .dataset import Dataset
from .forecasting import forecast
from .radar import market_signal, radar_for_product, risk_alerts, top_opportunities

# ── 품목·국가 키워드 사전 ──────────────────────────────────
PRODUCT_KEYWORDS = {
    "1902.30": ["라면", "즉석면", "면", "noodle"],
    "1212.21": ["김", "조미김", "마른김", "laver", "seaweed", "김수출"],
    "3304.99": ["화장품", "뷰티", "k-뷰티", "코스메틱", "스킨", "cosmetic", "beauty"],
    "2005.99": ["김치", "kimchi"],
    "2103.90": ["고추장", "장류", "소스", "양념", "sauce"],
    "1905.31": ["과자", "제과", "스낵", "비스킷", "snack"],
    "2202.99": ["음료", "주스", "드링크", "beverage", "drink"],
    "2208.90": ["소주", "술", "주류", "증류주", "리큐르", "soju"],
    "0810.10": ["딸기", "strawberry"],
    "0806.10": ["포도", "샤인머스캣", "샤인", "grape"],
    "1211.20": ["인삼", "홍삼", "ginseng"],
    "1901.90": ["즉석밥", "떡", "쌀가공", "가공밥", "rice"],
}

COUNTRY_ALIASES = {
    "US": ["미국", "usa", "미국시장", "america"], "JP": ["일본", "japan"],
    "CN": ["중국", "china"], "VN": ["베트남", "vietnam"], "TH": ["태국", "thailand"],
    "ID": ["인도네시아", "indonesia"], "MY": ["말레이시아", "malaysia"],
    "PH": ["필리핀", "philippines"], "TW": ["대만", "taiwan"], "HK": ["홍콩", "hongkong"],
    "SG": ["싱가포르", "singapore"], "AU": ["호주", "australia"],
    "AE": ["아랍에미리트", "uae", "두바이"], "SA": ["사우디", "사우디아라비아"],
    "FR": ["프랑스", "france"], "DE": ["독일", "germany"], "GB": ["영국", "uk", "england"],
    "NL": ["네덜란드", "netherlands"], "CA": ["캐나다", "canada"],
    "MX": ["멕시코", "mexico"], "IN": ["인도", "india"], "MN": ["몽골", "mongolia"],
    "RU": ["러시아", "russia"], "BR": ["브라질", "brazil"],
}

STATUS_LABEL = {"surge": "급등", "rising": "상승", "stable": "안정",
                "cooling": "둔화", "volatile": "변동성 높음"}


def _won(usd: float) -> str:
    """USD를 읽기 쉬운 한국어 규모로."""
    if usd >= 1e9:
        return f"{usd/1e9:.1f}억 달러"
    if usd >= 1e6:
        return f"{usd/1e6:.0f}백만 달러"
    return f"{usd/1e3:.0f}천 달러"


def extract_intent(question: str, ds: Dataset) -> dict:
    q = question.lower().replace(" ", "")
    hs = None
    for code, kws in PRODUCT_KEYWORDS.items():
        if any(kw.replace(" ", "") in q for kw in kws):
            hs = code
            break
    cc = None
    for code, aliases in COUNTRY_ALIASES.items():
        if any(a in q for a in aliases):
            cc = code
            break
    if any(w in q for w in ["위험", "리스크", "둔화", "조심", "경보", "빠지"]):
        intent = "risk"
    elif cc and hs:
        intent = "forecast"
    elif any(w in q for w in ["어디", "어느나라", "추천", "유망", "확대", "신규", "뚫"]):
        intent = "recommend"
    elif hs:
        intent = "recommend"
    else:
        intent = "overview"
    return {"hs": hs, "country": cc, "intent": intent}


def answer(ds: Dataset, question: str, llm=None) -> dict:
    intent = extract_intent(question, ds)
    pack = build_evidence(ds, intent)
    text = compose(pack)
    if llm is not None:
        try:
            text = llm.refine(question, pack, text)
        except Exception:  # noqa: BLE001 — LLM 실패 시 데모 NLG로 폴백
            pass
    return {"question": question, "intent": intent,
            "answer": text, "evidence": pack["evidence"],
            "suggestions": pack["suggestions"], "chart": pack.get("chart")}


def build_evidence(ds: Dataset, intent: dict) -> dict:
    hs, cc, kind = intent["hs"], intent["country"], intent["intent"]
    ev: list[dict] = []
    sug: list[str] = []
    chart = None
    headline = ""

    if kind == "forecast" and hs and cc:
        y = ds.series(hs, cc)
        fc = forecast(y, 6)
        sig = market_signal(y)
        pname, cname = ds.product_name(hs), ds.country_name(cc)
        fut6, base6 = sum(fc.mean), float(y[-12:-6].sum())
        yoy_fc = (fut6 - base6) / base6 if base6 > 0 else 0.0
        headline = (f"{cname} {pname} 시장은 현재 '{STATUS_LABEL[sig['status']]}' 국면입니다. "
                    f"최근 12개월 수출은 전년 대비 {sig['yoy']*100:+.0f}%, "
                    f"향후 6개월은 전년 동기 대비 {yoy_fc*100:+.0f}% 전망(월 추세 {fc.trend_pct*100:+.1f}%).")
        ev = [
            {"label": f"{cname} {pname} 최근 12개월 수출", "value": _won(float(y[-12:].sum()))},
            {"label": "전년 대비 증감(YoY)", "value": f"{sig['yoy']*100:+.0f}%"},
            {"label": "향후 6개월 전망(전년 동기 대비)", "value": f"{yoy_fc*100:+.0f}%"},
            {"label": "예측 적합도(MAPE)", "value": f"{fc.mape*100:.1f}%"},
            {"label": "변동성(변동계수)", "value": f"{sig['cv']:.2f}"},
        ]
        chart = {"type": "forecast", "hs": hs, "country": cc}
        sug = [f"{pname} 어디에 더 수출하면 좋을까?", f"{cname}에서 위험한 품목은?"]

    elif kind == "recommend":
        if hs:
            rows = [r for r in radar_for_product(ds, hs)][:5]
            pname = ds.product_name(hs)
            top = rows[0]
            headline = (f"{pname} 수출을 확대한다면 지금은 '{top['country_name']}'이 1순위입니다. "
                        f"기회점수 {top['opportunity']:.0f}점, 전년 대비 {top['yoy']*100:+.0f}%, "
                        f"향후 6개월 {top['fc_growth6']*100:+.0f}% 전망입니다.")
            ev = [{"label": f"{i+1}. {r['country_name']}",
                   "value": f"기회 {r['opportunity']:.0f} · YoY {r['yoy']*100:+.0f}% · 전망 {r['fc_growth6']*100:+.0f}% [{STATUS_LABEL[r['status']]}]"}
                  for i, r in enumerate(rows)]
            chart = {"type": "radar", "hs": hs}
            sug = [f"{pname} {top['country_name']} 수요 예측 보여줘", f"{pname} 위험 시장은?"]
        else:
            rows = top_opportunities(ds, 6)
            top = rows[0]
            headline = (f"지금 가장 빠르게 떠오르는 한류 수출 기회는 '{top['country_name']}의 {top['product']}'입니다 "
                        f"(기회 {top['opportunity']:.0f}, YoY {top['yoy']*100:+.0f}%).")
            ev = [{"label": f"{i+1}. {r['country_name']} · {r['product']}",
                   "value": f"기회 {r['opportunity']:.0f} · YoY {r['yoy']*100:+.0f}%"}
                  for i, r in enumerate(rows)]
            sug = ["라면 어디에 수출하면 좋을까?", "위험한 시장 알려줘"]

    elif kind == "risk":
        rows = risk_alerts(ds, 6)
        if rows:
            top = rows[0]
            headline = (f"리스크 조기경보: '{top['country_name']}의 {top['product']}'이 식고 있습니다 "
                        f"(최근 3개월 {top['growth3']*100:+.0f}%, 규모 {_won(top['recent12_usd'])}). "
                        f"의존도가 높다면 대체 시장 다변화를 권장합니다.")
            ev = [{"label": f"⚠ {r['country_name']} · {r['product']}",
                   "value": f"최근3개월 {r['growth3']*100:+.0f}% · YoY {r['yoy']*100:+.0f}% · {_won(r['recent12_usd'])}"}
                  for r in rows]
        else:
            headline = "현재 규모 있는 시장 중 둔화 경보 신호는 없습니다."
        sug = ["떠오르는 시장 추천해줘", "화장품 중국 수요 예측"]

    else:  # overview
        total = ds.grand_total()
        opp = top_opportunities(ds, 3)
        headline = (f"무역풍은 관세청 수출입통계로 한류 품목의 국가별 수요를 예측합니다. "
                    f"최근 12개월 분석 대상 수출 합계는 {_won(float(total[-12:].sum()))}이며, "
                    f"가장 유망한 시장은 '{opp[0]['country_name']}의 {opp[0]['product']}'입니다.")
        ev = [{"label": f"{r['country_name']} · {r['product']}",
               "value": f"기회 {r['opportunity']:.0f} · YoY {r['yoy']*100:+.0f}%"} for r in opp]
        sug = ["라면 어디에 수출하면 좋을까?", "화장품 미국 수요 예측", "위험한 시장은?"]

    return {"headline": headline, "evidence": ev, "suggestions": sug, "chart": chart}


def compose(pack: dict) -> str:
    """근거 팩을 한국어 답변 문단으로 조립(데모 NLG)."""
    lines = [pack["headline"]]
    if pack["evidence"]:
        lines.append("")
        lines.append("근거가 된 수치:")
        for e in pack["evidence"]:
            lines.append(f"· {e['label']} — {e['value']}")
    return "\n".join(lines)


class KoreanLLMAdapter:
    """국산 LLM 어댑터 인터페이스(운영용).

    Solar(업스테이지)·HyperCLOVA X(네이버) 등의 한국어 모델을 연결한다.
    evidence 팩을 시스템 프롬프트의 '근거'로 고정해 환각 없이 문체만 다듬는다.
    데모에서는 사용하지 않으며, 키 설정 시 server/config.py 에서 주입한다.
    """

    def __init__(self, provider: str = "solar", api_key: str | None = None):
        self.provider = provider
        self.api_key = api_key

    def refine(self, question: str, pack: dict, draft: str) -> str:  # pragma: no cover
        raise NotImplementedError("운영 환경에서 국산 LLM provider를 구현해 주입")
