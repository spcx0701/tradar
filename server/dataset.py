"""스냅샷 로더 및 조회 헬퍼.

snapshot.json(관세청 품목별 국가별 수출입실적 호환)을 메모리로 올리고,
품목/국가/기간 단위 조회·집계를 제공한다. 예측·레이더·상담 모듈이 공유한다.
"""
from __future__ import annotations

import functools
import json
import os

import numpy as np

_SNAPSHOT_PATH = os.path.join(os.path.dirname(__file__), "data", "snapshot.json")


@functools.lru_cache(maxsize=1)
def _raw() -> dict:
    with open(_SNAPSHOT_PATH, encoding="utf-8") as f:
        return json.load(f)


class Dataset:
    """스냅샷을 감싼 조회 객체(불변)."""

    def __init__(self, raw: dict | None = None):
        raw = raw or _raw()
        self.meta: dict = raw["meta"]
        self.months: list[str] = raw["months"]
        self.countries: dict[str, str] = raw["countries"]
        self.products: list[dict] = raw["products"]
        self._product_by_hs = {p["hs"]: p for p in self.products}
        self._series: dict[tuple[str, str], np.ndarray] = {}
        for s in raw["series"]:
            self._series[(s["hs"], s["country"])] = np.asarray(s["exp_usd"], dtype=np.float64)

    # ── 메타 ────────────────────────────────────────────────
    def product(self, hs: str) -> dict:
        return self._product_by_hs[hs]

    def product_name(self, hs: str) -> str:
        p = self._product_by_hs.get(hs)
        return p["name_ko"] if p else hs

    def country_name(self, cc: str) -> str:
        return self.countries.get(cc, cc)

    def markets_of(self, hs: str) -> list[str]:
        return [cc for (h, cc) in self._series if h == hs]

    # ── 시계열 ──────────────────────────────────────────────
    def series(self, hs: str, cc: str) -> np.ndarray | None:
        return self._series.get((hs, cc))

    def product_total(self, hs: str) -> np.ndarray:
        arrs = [v for (h, _), v in self._series.items() if h == hs]
        return np.sum(arrs, axis=0) if arrs else np.zeros(len(self.months))

    def market_total(self, cc: str) -> np.ndarray:
        arrs = [v for (_, c), v in self._series.items() if c == cc]
        return np.sum(arrs, axis=0) if arrs else np.zeros(len(self.months))

    def grand_total(self) -> np.ndarray:
        return np.sum(list(self._series.values()), axis=0)

    # ── 집계 유틸 ───────────────────────────────────────────
    def last_n_sum(self, arr: np.ndarray, n: int = 12) -> float:
        return float(arr[-n:].sum())

    def yoy(self, arr: np.ndarray) -> float:
        """최근 12개월 합 대비 직전 12개월 합 증감률."""
        if len(arr) < 24:
            return 0.0
        recent = arr[-12:].sum()
        prev = arr[-24:-12].sum()
        return float((recent - prev) / prev) if prev > 0 else 0.0


@functools.lru_cache(maxsize=1)
def get_dataset() -> Dataset:
    return Dataset()
