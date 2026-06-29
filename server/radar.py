"""급등시장 레이더 & 리스크 조기경보.

품목×국가 시계열에서 모멘텀·가속도·변동성을 추출해
① 떠오르는 시장(기회) ② 식어가는 시장(리스크)을 조기에 신호한다.
예측 엔진(forecasting.forecast)의 향후 성장 전망을 결합한다.
"""
from __future__ import annotations

import numpy as np

from .forecasting import forecast


def _slope_log(y: np.ndarray) -> float:
    """로그 추세선 기울기(월 성장률 근사)."""
    y = np.maximum(np.asarray(y, dtype=np.float64), 1.0)
    t = np.arange(len(y))
    b = np.polyfit(t, np.log(y), 1)[0]
    return float(np.exp(b) - 1.0)


def market_signal(y: np.ndarray) -> dict:
    y = np.asarray(y, dtype=np.float64)
    recent3 = y[-3:].sum()
    prev3 = y[-6:-3].sum()
    growth3 = (recent3 - prev3) / prev3 if prev3 > 0 else 0.0
    recent12 = y[-12:].sum()
    prev12 = y[-24:-12].sum() if len(y) >= 24 else recent12
    yoy = (recent12 - prev12) / prev12 if prev12 > 0 else 0.0
    slope = _slope_log(y)
    # 가속도: 최근 6개월 기울기 - 직전 6개월 기울기
    accel = _slope_log(y[-6:]) - _slope_log(y[-12:-6]) if len(y) >= 12 else 0.0
    cv = float(np.std(y[-12:]) / max(np.mean(y[-12:]), 1e-9))  # 변동계수

    fc = forecast(y, horizon=6)
    fut6 = sum(fc.mean)
    # 예측 구간(향후 6개월)을 전년 동기 6개월과 비교 — 계절 영향 제거한 진짜 YoY 전망
    base6 = float(y[-12:-6].sum()) if len(y) >= 12 else float(y[-6:].sum())
    fc_growth = (fut6 - base6) / base6 if base6 > 0 else 0.0

    size = float(recent12)
    size_w = float(np.clip(np.log10(max(size, 1)) / 8.0, 0.1, 1.0))

    # 기회 점수(0~100): 단기성장·전망·가속도·규모, 변동성 페널티
    raw = (0.32 * np.clip(growth3, -0.5, 1.2)
           + 0.26 * np.clip(fc_growth, -0.5, 1.2)
           + 0.18 * np.clip(yoy, -0.5, 1.2)
           + 0.12 * np.clip(accel, -0.5, 1.0)
           + 0.12 * size_w
           - 0.08 * np.clip(cv, 0, 1.0))
    opportunity = float(np.clip(50 + raw * 60, 0, 100))

    # 리스크 점수(0~100): 둔화·변동성
    risk = float(np.clip(50 - (yoy * 70) - (growth3 * 40) + cv * 30, 0, 100))

    if growth3 > 0.18 and yoy > 0.1:
        status = "surge"        # 급등
    elif yoy > 0.07:
        status = "rising"       # 상승
    elif yoy < -0.08 or growth3 < -0.12:
        status = "cooling"      # 둔화(경보)
    elif cv > 0.45:
        status = "volatile"     # 변동성
    else:
        status = "stable"       # 안정

    return {
        "yoy": round(yoy, 3),
        "growth3": round(growth3, 3),
        "slope": round(slope, 4),
        "accel": round(accel, 4),
        "cv": round(cv, 3),
        "fc_growth6": round(fc_growth, 3),
        "recent12_usd": round(size),
        "opportunity": round(opportunity, 1),
        "risk": round(risk, 1),
        "status": status,
    }


def radar_for_product(ds, hs: str) -> list[dict]:
    """한 품목의 국가별 신호(기회 점수 내림차순)."""
    rows = []
    for cc in ds.markets_of(hs):
        y = ds.series(hs, cc)
        sig = market_signal(y)
        sig.update({"country": cc, "country_name": ds.country_name(cc)})
        rows.append(sig)
    rows.sort(key=lambda r: r["opportunity"], reverse=True)
    return rows


def top_opportunities(ds, limit: int = 12, status=("surge", "rising")) -> list[dict]:
    """전 품목×국가에서 떠오르는 시장 상위."""
    rows = []
    for p in ds.products:
        hs = p["hs"]
        for cc in ds.markets_of(hs):
            sig = market_signal(ds.series(hs, cc))
            if sig["status"] in status:
                sig.update({
                    "hs": hs, "product": ds.product_name(hs),
                    "category": p["category"],
                    "country": cc, "country_name": ds.country_name(cc),
                })
                rows.append(sig)
    rows.sort(key=lambda r: r["opportunity"], reverse=True)
    return rows[:limit]


def risk_alerts(ds, limit: int = 8) -> list[dict]:
    """식어가는(둔화) 시장 경보 상위 — 규모가 큰 시장 우선."""
    rows = []
    for p in ds.products:
        hs = p["hs"]
        for cc in ds.markets_of(hs):
            sig = market_signal(ds.series(hs, cc))
            if sig["status"] == "cooling" and sig["recent12_usd"] > 2_000_000:
                sig.update({
                    "hs": hs, "product": ds.product_name(hs),
                    "category": p["category"],
                    "country": cc, "country_name": ds.country_name(cc),
                })
                rows.append(sig)
    rows.sort(key=lambda r: (r["recent12_usd"], r["risk"]), reverse=True)
    return rows[:limit]
