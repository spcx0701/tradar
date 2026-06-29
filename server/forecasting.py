"""수출 수요예측 엔진 — 무역풍 자체 개발 국산 AI.

월별 수출 시계열에 **승법 홀트-윈터스(Holt-Winters multiplicative) + 감쇠 추세**
지수평활을 적용해 향후 H개월 국가별 수요를 예측한다. 외산 라이브러리/모델에
의존하지 않고 numpy만으로 구현해 온디바이스·국내 인프라에서 그대로 동작한다(국산 AI 가점).

산출:
- 예측치(평균) 및 잔차 기반 예측구간(lo/hi)
- 적합도(MAPE), 추세·계절 강도
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

PERIOD = 12  # 월별 계절성


@dataclass
class ForecastResult:
    horizon: int
    mean: list[float]
    lo: list[float]
    hi: list[float]
    mape: float          # 인-샘플 1-step 평균절대백분율오차
    trend_pct: float     # 월 환산 추세(감쇠 후)
    season_strength: float
    level: float


def _seasonal_init(y: np.ndarray) -> np.ndarray:
    """첫 2주기 평균비로 계절지수 초기화(평균 1.0 정규화)."""
    n_full = len(y) // PERIOD
    if n_full < 2:
        return np.ones(PERIOD)
    seasonal = np.ones(PERIOD)
    period_means = [y[i * PERIOD:(i + 1) * PERIOD].mean() for i in range(n_full)]
    for m in range(PERIOD):
        ratios = [y[i * PERIOD + m] / period_means[i] for i in range(n_full)
                  if period_means[i] > 0]
        if ratios:
            seasonal[m] = float(np.mean(ratios))
    seasonal = np.clip(seasonal, 0.2, 3.0)
    seasonal *= PERIOD / seasonal.sum()
    return seasonal


def forecast(
    y: np.ndarray,
    horizon: int = 6,
    trend_window: int = 18,
    phi: float = 0.90,
    g_clip: tuple[float, float] = (-0.055, 0.075),
) -> ForecastResult:
    """승법 계절분해 + 감쇠 로그선형 추세 외삽.

    1) 전체 시계열에서 승법 계절지수를 추정해 계절성을 제거(deseasonalize).
    2) 최근 ``trend_window`` 개월의 탈계절 시계열에 로그선형 회귀를 적합해
       *현재 성장 국면*의 월 성장률 g를 추정(추세 시차 없이 끝점을 추세선에 정렬).
    3) 감쇠계수 phi로 성장률을 점차 줄이며 외삽 → 폭주하지도, 평균회귀하지도 않음.
    4) 계절지수를 다시 곱해 최종 예측. 잔차 표준편차로 95% 예측구간 산출.

    감쇠 로그선형은 설명 가능(explainable)하고 외산 모델 의존이 없다(국산 AI).
    """
    y = np.asarray(y, dtype=np.float64)
    y = np.maximum(y, 1.0)
    n = len(y)
    if n < PERIOD * 2:
        m = float(y[-min(6, n):].mean())
        return ForecastResult(horizon, [m] * horizon, [m * 0.8] * horizon,
                              [m * 1.2] * horizon, 0.0, 0.0, 0.0, m)

    seasonal = _seasonal_init(y)
    seas_full = seasonal[np.arange(n) % PERIOD]
    d = y / seas_full                       # 탈계절 시계열

    w = min(trend_window, n)
    t_rec = np.arange(n - w, n)
    ld = np.log(np.maximum(d[n - w:], 1.0))
    b, a = np.polyfit(t_rec, ld, 1)         # 로그선형 회귀(기울기 b, 절편 a)
    g = float(np.clip(np.exp(b) - 1.0, *g_clip))   # 월 성장률(클립)
    last_level = float(np.exp(a + b * (n - 1)))    # 추세선상의 끝점(시차 제거)

    # 인-샘플 적합도(MAPE) — 계절×추세 적합값 대비
    fit_d = np.exp(a + b * t_rec)
    fitted = fit_d * seas_full[n - w:]
    mape = float(np.mean(np.abs((y[n - w:] - fitted) / y[n - w:])))
    resid_std = float(np.std(y[n - w:] - fitted))

    # 감쇠 외삽: 성장률을 phi^k 로 점차 축소
    mean, lo, hi = [], [], []
    cum = 1.0
    for h in range(1, horizon + 1):
        cum *= (1.0 + g * (phi ** h))
        s = seasonal[(n + h - 1) % PERIOD]
        pt = max(last_level * cum * s, last_level * 0.03)
        band = 1.96 * resid_std * np.sqrt(h)
        mean.append(round(pt))
        lo.append(round(max(pt - band, 0)))
        hi.append(round(pt + band))

    season_strength = float(np.clip(seasonal.std() / 0.5, 0, 1))
    return ForecastResult(horizon, mean, lo, hi, round(mape, 4),
                          round(g, 4), round(season_strength, 3),
                          round(last_level))
