"""핵심 엔진(데이터·예측·레이더·상담) 단위 테스트."""
import numpy as np

from server.advisor import answer, extract_intent
from server.dataset import get_dataset
from server.forecasting import forecast
from server.radar import market_signal, risk_alerts, top_opportunities


def test_dataset_loads():
    ds = get_dataset()
    assert len(ds.products) == 12
    assert len(ds.months) == 60
    assert ds.series("1902.30", "US") is not None


def test_forecast_shape_and_positive():
    ds = get_dataset()
    fc = forecast(ds.series("1902.30", "US"), 6)
    assert len(fc.mean) == 6
    assert all(m > 0 for m in fc.mean)
    assert all(lo <= m <= hi for lo, m, hi in zip(fc.lo, fc.mean, fc.hi))
    assert 0 <= fc.mape < 1.0


def test_forecast_horizon_is_bounded():
    ds = get_dataset()
    fc = forecast(ds.series("1902.30", "US"), 999)
    assert fc.horizon == 12
    assert len(fc.mean) == 12
    assert len(fc.lo) == 12
    assert len(fc.hi) == 12


def test_forecast_tracks_trend():
    """상승 추세 시계열은 마지막 값 부근 이상으로 예측해야(평균회귀 아님)."""
    y = np.array([100 * (1.04 ** i) * (1.0 + 0.05 * np.sin(i)) for i in range(48)])
    fc = forecast(y, 6)
    assert fc.trend_pct > 0
    assert max(fc.mean) >= y[-1] * 0.9


def test_radar_signal_keys():
    ds = get_dataset()
    sig = market_signal(ds.series("3304.99", "CN"))
    for k in ("yoy", "opportunity", "risk", "status", "fc_growth6"):
        assert k in sig
    assert sig["status"] in {"surge", "rising", "stable", "cooling", "volatile"}


def test_top_opportunities_sorted():
    ds = get_dataset()
    top = top_opportunities(ds, 10)
    assert len(top) <= 10
    opps = [r["opportunity"] for r in top]
    assert opps == sorted(opps, reverse=True)


def test_risk_alerts_are_cooling():
    ds = get_dataset()
    for r in risk_alerts(ds, 8):
        assert r["status"] == "cooling"


def test_advisor_intents():
    ds = get_dataset()
    assert extract_intent("라면 어디에 수출할까?", ds)["intent"] == "recommend"
    assert extract_intent("화장품 미국 예측", ds)["intent"] == "forecast"
    assert extract_intent("위험한 시장 알려줘", ds)["intent"] == "risk"
    assert extract_intent("안녕", ds)["intent"] == "smalltalk"
    assert extract_intent("녕", ds)["intent"] == "smalltalk"


def test_advisor_grounded_answer():
    ds = get_dataset()
    r = answer(ds, "화장품 미국 수요 예측")
    assert "미국" in r["answer"] and "화장품" in r["answer"]
    assert len(r["evidence"]) > 0
    assert r["intent"]["country"] == "US"


def test_advisor_greeting_answers_without_default_market_overview():
    ds = get_dataset()
    r = answer(ds, "안녕")

    assert r["intent"]["intent"] == "smalltalk"
    assert "안녕하세요" in r["answer"]
    assert "최근 12개월 분석 대상 수출 합계" not in r["answer"]
    assert r["evidence"] == []
    assert r["suggestions"]


def test_tradar_score():
    from server import scoring
    ds = get_dataset()
    sc = scoring.compute(market_signal(ds.series("1212.21", "US")))
    assert 0 <= sc["score"] <= 100
    assert sc["stage"] in scoring.STAGE
    assert set(sc["sub"]) == {"demand", "growth", "stability", "potential"}
    assert all(0 <= v <= 100 for v in sc["sub"].values())
