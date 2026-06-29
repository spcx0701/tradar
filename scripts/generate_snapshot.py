#!/usr/bin/env python3
"""관세청 수출입무역통계 대표 스냅샷 생성기.

관세청 ``품목별 국가별 수출입실적``(data.go.kr nitemtrade) 오픈API와 **동일한 구조**의
월별 시계열을 생성한다. 총량은 2024년 실제 공표치(catalog.py의 anchor)에 앵커링하고,
시장별 모멘텀·계절성·노이즈를 결합해 현실적인 추세를 만든다.

실 서비스에서는 ``server/customs_client.py`` 가 인증키로 실데이터를 받아 이 스냅샷을
대체한다. 시드를 고정해 재현 가능(deterministic)하다 — 데모가 항상 동일하게 동작.

출력: server/data/snapshot.json
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from server.data.catalog import (  # noqa: E402
    COUNTRIES, MOMENTUM, N_MONTHS, PRODUCTS, SEASON, START_MONTH, START_YEAR,
)

RNG = np.random.default_rng(20260703)  # 접수 마감일 시드 — 재현성

# 카테고리별 대표 단가(USD/kg) — 중량 환산용(현실성)
UNIT_PRICE = {"K-Food": 7.0, "K-Beauty": 55.0, "K-Culture": 9.0, "K-Fruit": 12.0}


def month_labels() -> list[str]:
    labels = []
    y, m = START_YEAR, START_MONTH
    for _ in range(N_MONTHS):
        labels.append(f"{y:04d}-{m:02d}")
        m += 1
        if m > 12:
            m = 1
            y += 1
    return labels


def build_series(months: list[str]) -> list[dict]:
    idx = np.arange(N_MONTHS)
    # 2024년 월 인덱스의 중심(연 성장률 기준점)
    y2024 = [i for i, lab in enumerate(months) if lab.startswith("2024-")]
    center_2024 = float(np.mean(y2024))
    month_num = np.array([int(lab[-2:]) for lab in months])

    series = []
    for p in PRODUCTS:
        season = np.array(SEASON[p["season"]])
        unit_price = UNIT_PRICE[p["category"]]
        for cc, (share, mom) in p["markets"].items():
            g_med, vol = MOMENTUM[mom]
            # 시장별로 모멘텀 중앙값 부근에서 약간 흔들어 다양성 부여
            g = float(np.clip(RNG.normal(g_med, 0.05), -0.35, 0.75))
            market_2024_usd = share * p["anchor_2024_musd"] * 1_000_000
            base_monthly = market_2024_usd / 12.0

            # 시간가변 월 성장률 gm[t] — 구조적이고 매끄러운 추세(불연속 없음)
            gm = np.full(N_MONTHS, (1.0 + g) ** (1.0 / 12.0) - 1.0)
            if mom == "surge":          # 최근 18개월 완만한 가속
                k = max(N_MONTHS - 18, 0)
                gm[k:] += np.linspace(0.0, 0.030, N_MONTHS - k)
            elif mom == "cooling":      # 최근 14개월 완만한 둔화
                k = max(N_MONTHS - 14, 0)
                gm[k:] += np.linspace(0.0, -0.045, N_MONTHS - k)
            elif mom == "volatile":     # 추세 위에 사이클 가미
                gm += 0.02 * np.sin(idx / 5.0)

            level = np.cumprod(1.0 + gm)
            level = level / level[int(round(center_2024))]  # 2024 중심을 1로 정규화
            trend = base_monthly * level
            seas = season[month_num - 1]
            noise = 1.0 + RNG.normal(0.0, vol * 0.40, N_MONTHS)
            noise = np.clip(noise, 0.6, 1.5)
            vals = trend * seas * noise

            vals = np.maximum(vals, base_monthly * 0.05)
            exp_usd = np.round(vals).astype(np.int64)
            exp_kg = np.round(vals / unit_price).astype(np.int64)

            series.append({
                "hs": p["hs"],
                "country": cc,
                "exp_usd": exp_usd.tolist(),
                "exp_kg": exp_kg.tolist(),
            })
    return series


def main() -> None:
    months = month_labels()
    series = build_series(months)
    out = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source": "관세청 품목별 국가별 수출입실적(GW) 스키마 호환 대표 스냅샷",
            "source_api": "https://apis.data.go.kr/1220000/nitemtrade/getNitemtradeList",
            "unit": "USD (수출금액), kg (수출중량)",
            "period": f"{months[0]} ~ {months[-1]}",
            "anchor": "2024년 수출 실적은 관세청·무역통계 공표치에 앵커링",
            "note": "재현 가능한 데모 스냅샷. 실 서비스는 인증키로 실데이터 동기화.",
            "n_series": len(series),
            "n_months": len(months),
        },
        "months": months,
        "countries": COUNTRIES,
        "products": [
            {"hs": p["hs"], "name_ko": p["name_ko"], "category": p["category"],
             "anchor_2024_musd": p["anchor_2024_musd"]}
            for p in PRODUCTS
        ],
        "series": series,
    }
    dst = os.path.join(os.path.dirname(__file__), "..", "server", "data", "snapshot.json")
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    total24 = sum(
        sum(s["exp_usd"][i] for i, lab in enumerate(months) if lab.startswith("2024-"))
        for s in series
    )
    print(f"✓ snapshot.json — {len(series)} series × {len(months)} months")
    print(f"  2024 총수출(앵커 합계): ${total24/1e9:.1f}B  ·  {os.path.relpath(dst)}")


if __name__ == "__main__":
    main()
