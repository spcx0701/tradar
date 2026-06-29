#!/usr/bin/env python3
"""정적 PWA용 데이터 빌드 — AI 결과를 JSON으로 굽는다.

예측·레이더 엔진을 전 품목×국가에 대해 미리 실행해 app/data/*.json 으로 출력한다.
정적 웹앱(백엔드 없이)이 이 파일만으로 100% 동작 → 데모가 항상 작동(오프라인).
운영 환경에서는 FastAPI(server/main.py)가 동일 결과를 실시간 API로 제공한다.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from server.dataset import get_dataset           # noqa: E402
from server.forecasting import forecast          # noqa: E402
from server.radar import (                        # noqa: E402
    market_signal, radar_for_product, risk_alerts, top_opportunities,
)

OUT = os.path.join(os.path.dirname(__file__), "..", "app", "data")
HORIZON = 6


def future_months(months: list[str], h: int) -> list[str]:
    y, m = int(months[-1][:4]), int(months[-1][5:])
    out = []
    for _ in range(h):
        m += 1
        if m > 12:
            m = 1
            y += 1
        out.append(f"{y:04d}-{m:02d}")
    return out


def main() -> None:
    ds = get_dataset()
    os.makedirs(OUT, exist_ok=True)
    fc_months = future_months(ds.months, HORIZON)

    # 1) catalog.json
    products = []
    for p in ds.products:
        tot = ds.product_total(p["hs"])
        products.append({
            **p,
            "latest12_usd": round(float(tot[-12:].sum())),
            "yoy": round(ds.yoy(tot), 3),
        })
    catalog = {"meta": ds.meta, "countries": ds.countries, "products": products,
               "categories": sorted({p["category"] for p in ds.products})}
    _dump("catalog.json", catalog)

    # 2) forecast.json — 시계열 + 예측 + 신호(품목×국가)
    series = {}
    for p in ds.products:
        hs = p["hs"]
        for cc in ds.markets_of(hs):
            y = ds.series(hs, cc)
            fc = forecast(y, HORIZON)
            sig = market_signal(y)
            series[f"{hs}|{cc}"] = {
                "hist": [round(v) for v in y.tolist()],
                "mean": fc.mean, "lo": fc.lo, "hi": fc.hi,
                "yoy": sig["yoy"], "growth3": sig["growth3"], "fc6": sig["fc_growth6"],
                "status": sig["status"], "opportunity": sig["opportunity"],
                "risk": sig["risk"], "mape": fc.mape, "trend": fc.trend_pct,
                "cv": sig["cv"], "recent12_usd": sig["recent12_usd"],
            }
    _dump("forecast.json", {"months": ds.months, "fc_months": fc_months, "series": series})

    # 3) radar.json — 기회·리스크·품목별 랭킹
    by_product = {p["hs"]: radar_for_product(ds, p["hs"]) for p in ds.products}
    radar = {
        "top": top_opportunities(ds, 24),
        "risk": risk_alerts(ds, 12),
        "by_product": by_product,
        "generated_period": ds.meta["period"],
    }
    _dump("radar.json", radar)

    # 4) 국가별 총수출(대시보드 히트맵용)
    country_totals = []
    for cc, name in ds.countries.items():
        arr = ds.market_total(cc)
        if arr.sum() <= 0:
            continue
        country_totals.append({
            "country": cc, "country_name": name,
            "latest12_usd": round(float(arr[-12:].sum())),
            "yoy": round(ds.yoy(arr), 3),
        })
    country_totals.sort(key=lambda r: r["latest12_usd"], reverse=True)
    _dump("countries.json", {"countries": country_totals})

    print(f"✓ app/data: catalog({len(products)} 품목) · forecast({len(series)} 시계열) · "
          f"radar(top {len(radar['top'])}/risk {len(radar['risk'])}) · countries({len(country_totals)})")


def _dump(name: str, obj) -> None:
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))


if __name__ == "__main__":
    main()
