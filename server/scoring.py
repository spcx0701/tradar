"""Tradar Score — 시장 매력도 종합 점수 (0~100) + 하위 점수.

Chartmetric의 CM Score / Career Stage / Momentum 개념을 무역 데이터에 대응:
- Tradar Score : 한 품목×국가 수출 시장의 종합 매력도
- 하위 점수     : 수요(Demand)·성장(Growth)·안정성(Stability)·잠재력(Potential)
- 시장 단계     : 최대시장→주력→성장→신흥→초기 (규모×성장으로 판정)
- 모멘텀        : 폭발적 성장→성장→안정→둔화→변동 (레이더 상태 매핑)

모든 값은 레이더 신호(market_signal)와 규모에서 파생 — 실 데이터 위에서 산출.
"""
from __future__ import annotations

import math

STAGE = {
    "dominant": {"key": "dominant", "ko": "최대시장", "en": "Dominant", "color": "#F5B301"},
    "core":     {"key": "core", "ko": "주력시장", "en": "Core", "color": "#7A5BF0"},
    "growing":  {"key": "growing", "ko": "성장시장", "en": "Growing", "color": "#1D68F0"},
    "emerging": {"key": "emerging", "ko": "신흥시장", "en": "Emerging", "color": "#16A8C8"},
    "nascent":  {"key": "nascent", "ko": "초기시장", "en": "Nascent", "color": "#9AA4B2"},
}
MOMENTUM = {
    "surge":    {"ko": "폭발적 성장", "en": "Explosive", "color": "#16B364"},
    "rising":   {"ko": "성장", "en": "Rising", "color": "#0E8B4B"},
    "stable":   {"ko": "안정", "en": "Steady", "color": "#9AA4B2"},
    "cooling":  {"ko": "둔화", "en": "Cooling", "color": "#F0443B"},
    "volatile": {"ko": "변동성", "en": "Volatile", "color": "#F2A20C"},
}


def _clip(v, lo=0.0, hi=100.0):
    return max(lo, min(hi, v))


def compute(sig: dict) -> dict:
    """레이더 신호(dict)로부터 Tradar Score + 하위 점수 + 단계 산출."""
    size = float(sig["recent12_usd"])
    yoy = sig["yoy"]
    fc6 = sig["fc_growth6"]
    cv = sig["cv"]
    accel = sig.get("accel", 0.0)

    # 하위 점수 (0~100)
    demand = _clip((math.log10(max(size, 1)) - 5.4) / (9.4 - 5.4) * 100)
    growth = _clip(50 + yoy * 55 + fc6 * 35)
    stability = _clip(100 - cv * 145)
    potential = _clip(50 + fc6 * 70 + accel * 45 + (yoy > 0) * 6)

    score = round(0.30 * growth + 0.24 * demand + 0.24 * potential + 0.22 * stability, 1)

    # 시장 단계: 규모(demand)와 성장(growth) 조합
    if demand >= 72:
        stage = "dominant" if growth >= 55 else "core"
    elif demand >= 50:
        stage = "core" if growth >= 60 else "growing"
    elif growth >= 62:
        stage = "growing"
    elif growth >= 52:
        stage = "emerging"
    else:
        stage = "nascent"

    return {
        "score": score,
        "sub": {
            "demand": round(demand),
            "growth": round(growth),
            "stability": round(stability),
            "potential": round(potential),
        },
        "stage": stage,
        "momentum": sig["status"],
    }
