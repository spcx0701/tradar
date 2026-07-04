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
from server import scoring                        # noqa: E402
from server.radar import (                        # noqa: E402
    market_signal, radar_for_product, risk_alerts, top_opportunities,
)

OUT = os.path.join(os.path.dirname(__file__), "..", "app", "app", "data")
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

    # 2) forecast.json — 시계열 + 예측 + 신호 + Tradar Score(품목×국가)
    series = {}
    treemap = []
    cat_by_hs = {p["hs"]: p["category"] for p in ds.products}
    for p in ds.products:
        hs = p["hs"]
        for cc in ds.markets_of(hs):
            y = ds.series(hs, cc)
            fc = forecast(y, HORIZON)
            sig = market_signal(y)
            sc = scoring.compute(sig)
            series[f"{hs}|{cc}"] = {
                "hist": [round(v) for v in y.tolist()],
                "mean": fc.mean, "lo": fc.lo, "hi": fc.hi,
                "yoy": sig["yoy"], "growth3": sig["growth3"], "fc6": sig["fc_growth6"],
                "status": sig["status"], "opportunity": sig["opportunity"],
                "risk": sig["risk"], "mape": fc.mape, "trend": fc.trend_pct,
                "cv": sig["cv"], "recent12_usd": sig["recent12_usd"], "accel": sig["accel"],
                "score": sc["score"], "sub": sc["sub"], "stage": sc["stage"],
            }
            treemap.append({
                "hs": hs, "product": p["name_ko"], "category": cat_by_hs[hs],
                "country": cc, "country_name": ds.country_name(cc),
                "value": sig["recent12_usd"], "yoy": sig["yoy"], "growth3": sig["growth3"],
                "fc6": sig["fc_growth6"], "score": sc["score"], "momentum": sig["status"],
                "stage": sc["stage"], "opportunity": sig["opportunity"],
            })
    _dump("forecast.json", {"months": ds.months, "fc_months": fc_months, "series": series})
    _dump("treemap.json", {"leaves": treemap,
                           "stages": scoring.STAGE, "momentum": scoring.MOMENTUM})

    # 3) radar.json — 기회·리스크·품목별 랭킹 (+ score 부여)
    def _enrich(rows):
        for r in rows:
            key = f"{r['hs']}|{r['country']}" if "hs" in r else None
            if key and key in series:
                r["score"] = series[key]["score"]
                r["stage"] = series[key]["stage"]
        return rows
    by_product = {}
    for p in ds.products:
        rows = radar_for_product(ds, p["hs"])
        for r in rows:  # radar_for_product rows lack hs — add it
            r["hs"] = p["hs"]
            k = f"{p['hs']}|{r['country']}"
            if k in series:
                r["score"] = series[k]["score"]
                r["stage"] = series[k]["stage"]
        by_product[p["hs"]] = rows
    radar = {
        "top": _enrich(top_opportunities(ds, 30)),
        "risk": _enrich(risk_alerts(ds, 12)),
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

    print(f"✓ app/app/data: catalog({len(products)} 품목) · forecast({len(series)} 시계열) · "
          f"radar(top {len(radar['top'])}/risk {len(radar['risk'])}) · countries({len(country_totals)})")


def _dump(name: str, obj) -> None:
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))


if __name__ == "__main__":
    main()
