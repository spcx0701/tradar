"""AI 무역참모 '바람이' — 수치 근거 기반 상담(grounded NLG).

사용자의 한국어 질문에서 품목·국가·의도를 추출하고, 예측·레이더 엔진의 결과를
근거(evidence)로 묶어 한국어 답변을 생성한다.

- 데모: 외부 호출 없이 검색·규칙 기반 NLG로 항상 동작(오프라인).
- 운영: 동일한 evidence 팩을 운영자가 선택한 LLM(Solar·Gemini Flash 등)
  어댑터에 넘겨 자연스러운 문장으로 다듬는다. 어댑터 미설정 시 데모 NLG로 폴백.

핵심: 모든 문장은 실제 수출 통계 수치에 근거하며, 근거를 함께 반환한다(환각 차단).
"""
from __future__ import annotations

import json
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .config import Settings, settings
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
SMALLTALK_INPUTS = {
    "안녕", "안녕하세요", "녕", "하이", "ㅎㅇ", "헬로", "반가워",
    "hi", "hello", "hey",
}


def _won(usd: float) -> str:
    """USD를 읽기 쉬운 한국어 규모로."""
    if usd >= 1e9:
        return f"{usd/1e9:.1f}억 달러"
    if usd >= 1e6:
        return f"{usd/1e6:.0f}백만 달러"
    return f"{usd/1e3:.0f}천 달러"


def extract_intent(question: str, ds: Dataset) -> dict:
    q = question.lower().replace(" ", "")
    compact = q.strip("!?.,。~…")
    if compact in SMALLTALK_INPUTS:
        return {"hs": None, "country": None, "intent": "smalltalk"}
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
    engine = "demo-grounded"
    llm_error = None
    if intent["intent"] == "smalltalk" and llm is None:
        return {
            "question": question,
            "intent": intent,
            "answer": (
                "한국 LLM이 설정되지 않아 일반 대화 응답을 생성할 수 없습니다. "
                "인사 응답을 하드코딩으로 대신하지 않습니다. TW_LLM_PROVIDER와 TW_LLM_KEY를 확인해 주세요."
            ),
            "evidence": pack["evidence"],
            "suggestions": pack["suggestions"],
            "chart": pack.get("chart"),
            "engine": "llm-not-configured",
            "llm_error": "Korean LLM is not configured",
        }
    if llm is not None:
        try:
            text = llm.refine(question, pack, text)
            engine = getattr(llm, "engine_name", getattr(llm, "provider", "korean-llm"))
        except Exception as exc:  # noqa: BLE001 — 운영 상태를 응답에 드러낸다
            engine = "demo-grounded-fallback"
            llm_error = _public_llm_error(exc)
            if intent["intent"] == "smalltalk":
                text = (
                    f"한국 LLM 연결에 실패했습니다: {llm_error}\n\n"
                    "인사나 일반 대화 응답을 하드코딩으로 대신하지 않습니다. "
                    "TW_LLM_KEY, provider 크레딧, 모델 설정을 확인해 주세요."
                )
            else:
                text = (
                    f"한국 LLM 연결에 실패했습니다: {llm_error}\n\n"
                    "아래는 LLM이 아니라 관세청 데이터 기반 규칙 초안입니다.\n\n"
                    f"{text}"
                )
    return {"question": question, "intent": intent,
            "answer": text, "evidence": pack["evidence"],
            "suggestions": pack["suggestions"], "chart": pack.get("chart"),
            "engine": engine, "llm_error": llm_error}


def _public_llm_error(exc: Exception) -> str:
    msg = str(exc).strip() or exc.__class__.__name__
    return " ".join(msg.split())[:280]


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

    elif kind == "smalltalk":
        headline = (
            "사용자가 인사했습니다. Tradar의 역할을 짧게 소개하고 "
            "품목, 국가, 수출 추세, 리스크, 시장 비교 질문을 자연스럽게 유도하세요."
        )
        sug = ["라면 수출 추세 보여줘", "K-뷰티 핵심 시장 비교", "리스크 대비 기회 매트릭스"]

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


ChatTransport = Callable[[str, dict[str, str], dict[str, Any], float], dict[str, Any]]


PROVIDER_ALIASES = {
    "openrouter": "openrouter-solar-free",
    "openrouter-solar": "openrouter-solar-free",
    "solar-free": "openrouter-solar-free",
    "solar-openrouter": "openrouter-solar-free",
    "gemini": "gemini-flash",
    "gemini-flash": "gemini-flash",
}

PROVIDER_DEFAULTS = {
    "solar": {"base_url": "https://api.upstage.ai/v1", "model": "solar-pro3"},
    "upstage": {"base_url": "https://api.upstage.ai/v1", "model": "solar-pro3"},
    "openrouter-solar-free": {
        "base_url": "https://openrouter.ai/api/v1",
        "model": "upstage/solar-pro-3:free",
    },
    "gemini-flash": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "model": "gemini-3.5-flash",
    },
}


def normalize_llm_provider(provider: str | None) -> str:
    value = (provider or "").strip().lower()
    return PROVIDER_ALIASES.get(value, value)


def _provider_connection(config: Settings, provider: str) -> dict[str, str]:
    defaults = PROVIDER_DEFAULTS.get(provider, {})
    if provider == "openrouter-solar-free":
        return {
            "api_key": config.openrouter_api_key or config.llm_api_key,
            "base_url": config.openrouter_base_url or defaults.get("base_url", ""),
            "model": config.openrouter_model or defaults.get("model", ""),
        }
    if provider == "gemini-flash":
        return {
            "api_key": config.gemini_api_key or config.llm_api_key,
            "base_url": config.gemini_base_url or defaults.get("base_url", ""),
            "model": config.gemini_model or defaults.get("model", ""),
        }
    return {
        "api_key": config.llm_api_key,
        "base_url": config.llm_base_url or defaults.get("base_url", ""),
        "model": config.llm_model or defaults.get("model", ""),
    }


def llm_provider_status(config: Settings = settings) -> list[dict[str, Any]]:
    providers = [
        ("solar", "Upstage Solar official"),
        ("openrouter-solar-free", "OpenRouter Solar Pro 3 free"),
        ("gemini-flash", "Google Gemini Flash"),
    ]
    status = []
    for provider, label in providers:
        conn = _provider_connection(config, provider)
        status.append(
            {
                "provider": provider,
                "label": label,
                "configured": bool(conn["api_key"] and conn["base_url"] and conn["model"]),
                "base_url": conn["base_url"],
                "model": conn["model"],
            }
        )
    return status


def _join_chat_completions_url(base_url: str) -> str:
    base = base_url.rstrip("/")
    if base.endswith("/chat/completions"):
        return base
    return f"{base}/chat/completions"


def _default_chat_transport(
    url: str,
    headers: dict[str, str],
    payload: dict[str, Any],
    timeout: float,
) -> dict[str, Any]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = Request(url, data=body, headers=headers, method="POST")
    try:
        with urlopen(req, timeout=timeout) as res:  # noqa: S310 - operator-configured LLM endpoint
            return json.loads(res.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:400]
        raise RuntimeError(f"LLM HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"LLM connection error: {exc.reason}") from exc


class KoreanLLMAdapter:
    """Grounded chat-completions LLM 어댑터.

    기본 운영 모드는 OpenAI-compatible Chat Completions API다.
    Solar, OpenRouter, Gemini OpenAI 호환 엔드포인트를 같은 근거 팩 계약으로 호출한다.
    """

    def __init__(
        self,
        provider: str = "solar",
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        timeout: float = 12,
        transport: ChatTransport | None = None,
    ):
        self.provider = normalize_llm_provider(provider)
        defaults = PROVIDER_DEFAULTS.get(self.provider, {})
        self.api_key = api_key or ""
        self.base_url = base_url or defaults.get("base_url", "")
        self.model = model or defaults.get("model", "")
        self.timeout = timeout
        self.transport = transport or _default_chat_transport
        self.engine_name = f"{self.provider}:{self.model}" if self.model else self.provider

    def refine(self, question: str, pack: dict, draft: str) -> str:
        if not self.api_key:
            raise RuntimeError("TW_LLM_KEY is required for Korean LLM mode")
        if not self.base_url or not self.model:
            raise RuntimeError("TW_LLM_BASE_URL and TW_LLM_MODEL are required for this LLM provider")

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "너는 한국 수출 데이터를 분석하는 Tradar AI 무역참모다. "
                        "제공된 근거 수치와 초안 안에서만 한국어 답변을 자연스럽게 다듬어라. "
                        "근거에 없는 회사명, 국가, 금액, 인증, 출처를 새로 만들지 마라. "
                        "수치가 부족한 부분은 추정하지 말고 확인 필요라고 말하라."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "question": question,
                            "draft_answer": draft,
                            "headline": pack.get("headline", ""),
                            "evidence": pack.get("evidence", []),
                            "suggestions": pack.get("suggestions", []),
                        },
                        ensure_ascii=False,
                    ),
                },
            ],
            "temperature": 0.2,
            "max_tokens": 700,
            "stream": False,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = self.transport(
            _join_chat_completions_url(self.base_url),
            headers,
            payload,
            self.timeout,
        )
        text = response["choices"][0]["message"]["content"].strip()
        if not text:
            raise RuntimeError("LLM returned an empty answer")
        return text


def build_llm_adapter(
    config: Settings = settings,
    provider_override: str | None = None,
) -> KoreanLLMAdapter | None:
    if not (provider_override or config.llm_provider):
        return None
    provider = normalize_llm_provider(provider_override or config.llm_provider)
    conn = _provider_connection(config, provider)
    if not conn["api_key"] or not conn["base_url"] or not conn["model"]:
        return None
    return KoreanLLMAdapter(
        provider=provider,
        api_key=conn["api_key"],
        base_url=conn["base_url"],
        model=conn["model"],
        timeout=config.llm_timeout,
    )
