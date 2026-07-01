"""무역풍 REST API 라우터 — 예측·레이더·AI 상담(실시간)."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from ..advisor import answer as advisor_answer
from ..dataset import get_dataset
from ..forecasting import MAX_HORIZON, clamp_horizon, forecast
from ..radar import market_signal, radar_for_product, risk_alerts, top_opportunities
from ..schemas import AdvisorRequest, AdvisorResponse

router = APIRouter(prefix="/api", tags=["tradewind"])

HORIZON = 6
MAX_RADAR_LIMIT = 60


def _bounded_limit(value: int) -> int:
    return min(max(int(value), 1), MAX_RADAR_LIMIT)


def _future_months(months, h):
    safe_horizon = clamp_horizon(h)
    y, m = int(months[-1][:4]), int(months[-1][5:])
    out = []
    for _ in range(safe_horizon):
        m += 1
        if m > 12:
            m, y = 1, y + 1
        out.append(f"{y:04d}-{m:02d}")
    return out


@router.get("/health")
def health():
    ds = get_dataset()
    return {"status": "ok", "period": ds.meta["period"], "products": len(ds.products)}


@router.get("/catalog")
def catalog():
    ds = get_dataset()
    return {"meta": ds.meta, "countries": ds.countries, "products": ds.products}


@router.get("/forecast")
def forecast_endpoint(
    hs: str = Query(..., examples=["1902.30"]),
    country: str = Query(..., examples=["US"]),
    horizon: int = Query(HORIZON, ge=1, le=MAX_HORIZON),
):
    ds = get_dataset()
    y = ds.series(hs, country)
    if y is None:
        raise HTTPException(404, f"시계열 없음: {hs} / {country}")
    safe_horizon = clamp_horizon(horizon)
    fc = forecast(y, safe_horizon)
    sig = market_signal(y)
    return {
        "hs": hs, "product": ds.product_name(hs),
        "country": country, "country_name": ds.country_name(country),
        "months": ds.months, "fc_months": _future_months(ds.months, safe_horizon),
        "hist": [round(v) for v in y.tolist()],
        "mean": fc.mean, "lo": fc.lo, "hi": fc.hi,
        "mape": fc.mape, "trend": fc.trend_pct, "season_strength": fc.season_strength,
        "signal": sig,
    }


@router.get("/radar")
def radar(limit: int = Query(24, ge=1, le=60)):
    ds = get_dataset()
    return {"top": top_opportunities(ds, _bounded_limit(limit)), "risk": risk_alerts(ds, 12)}


@router.get("/radar/product/{hs}")
def radar_product(hs: str):
    ds = get_dataset()
    rows = radar_for_product(ds, hs)
    if not rows:
        raise HTTPException(404, f"품목 없음: {hs}")
    return {"hs": hs, "product": ds.product_name(hs), "markets": rows}


@router.post("/advisor", response_model=AdvisorResponse)
def advisor(req: AdvisorRequest):
    ds = get_dataset()
    return advisor_answer(ds, req.question)
