#!/usr/bin/env python3
"""Tradar 데이터 파이프라인 — 관세청 실데이터 연동.

Tradar 대시보드가 소비하는 app/data/tradar.js( window.TRADAR_DATA = {P, markets, news} )를
관세청 **품목별 국가별 수출입실적**(data.go.kr, HS코드 기준)에 연동해 재생성한다.

- `DATA_GO_KR_KEY` 설정 시: 각 품목의 HS코드로 실데이터를 받아 연수출액(ann)·전년比(yoy)·
  국가별 비중/증감(mk)을 실측치로 갱신한다(server/customs_client.py).
- 미설정 시: 2024년 관세청 공표치에 앵커링된 기존 값을 유지(데모가 항상 동작).
- news는 큐레이션 항목이라 통계 갱신 대상이 아니며 그대로 보존한다.

사용: python scripts/build_tradar_data.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from server.customs_client import CustomsClient  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
TRADAR_JS = os.path.join(ROOT, "app", "app", "data", "tradar.js")


def load_data() -> dict:
    """node로 tradar.js를 평가해 window.TRADAR_DATA를 JSON으로 추출."""
    js = ("globalThis.window=globalThis.window||{};"
          f"require({json.dumps(os.path.abspath(TRADAR_JS))});"
          "process.stdout.write(JSON.stringify(window.TRADAR_DATA));")
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def load_trade_intel() -> dict | None:
    """기존 거래 인텔리전스 섹션을 읽어 관세청 통계 빌드 때 보존한다."""
    js = ("globalThis.window=globalThis.window||{};"
          f"require({json.dumps(os.path.abspath(TRADAR_JS))});"
          "process.stdout.write(JSON.stringify(window.TRADAR_TRADE_INTEL||null));")
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def _ym(dt: datetime) -> str:
    return f"{dt.year:04d}{dt.month:02d}"


def refresh_from_customs(data: dict, client: CustomsClient) -> int:
    """각 품목 HS코드로 실데이터를 받아 ann/yoy/mk 갱신. 갱신 건수 반환."""
    now = datetime.now()
    end = _ym(now)
    start = _ym(now.replace(year=now.year - 2))
    updated = 0
    for p in data["P"]:
        hs = p.get("hs")
        if not hs:
            continue
        try:
            rows = client.fetch_item_country(hs, start, end)
        except Exception as e:  # noqa: BLE001
            print(f"  ! {p['id']} ({hs}) 조회 실패: {e}")
            continue
        # 연 단위 집계 → 최근연도 vs 직전연도
        by_year_country: dict = {}
        for r in rows:
            by_year_country.setdefault(r["year"], {})[r["country_name"]] = r["exp_usd"]
        years = sorted(by_year_country)
        if len(years) < 1:
            continue
        cur, prev = years[-1], (years[-2] if len(years) > 1 else years[-1])
        cur_total = sum(by_year_country[cur].values())
        prev_total = sum(by_year_country.get(prev, {}).values()) or cur_total
        p["ann"] = round(cur_total / 1e6)  # 백만 달러
        p["yoy"] = round((cur_total - prev_total) / prev_total * 100, 1) if prev_total else 0.0
        # 국가별 비중·증감 상위 4
        tops = sorted(by_year_country[cur].items(), key=lambda kv: kv[1], reverse=True)[:4]
        mk = []
        for name, val in tops:
            share = round(val / cur_total * 100) if cur_total else 0
            pv = by_year_country.get(prev, {}).get(name, val)
            g = round((val - pv) / pv * 100) if pv else 0
            mk.append([_country_code(name), share, g])
        if mk:
            p["mk"] = mk
        updated += 1
    return updated


# 관세청 통계 국가명 → ISO 코드(디자인 markets 코드계와 일치)
_C2CODE = {
    "미국": "US", "중국": "CN", "베트남": "VN", "일본": "JP", "홍콩": "HK", "대만": "TW",
    "싱가포르": "SG", "인도": "IN", "멕시코": "MX", "독일": "DE", "네덜란드": "NL",
    "폴란드": "PL", "아랍에미리트연합": "AE", "인도네시아": "ID", "태국": "TH", "영국": "GB",
    "라이베리아": "LR", "파나마": "PA", "헝가리": "HU", "호주": "AU",
}


def _country_code(name: str) -> str:
    for ko, code in _C2CODE.items():
        if ko in name:
            return code
    return name[:2].upper()


def emit(data: dict) -> None:
    trade_intel = load_trade_intel()
    header = ("/* Tradar 데이터 — 관세청 품목별 국가별 수출입실적(HS코드 기준) 연동.\n"
              f"   생성: {datetime.now().isoformat(timespec='seconds')} · "
              "scripts/build_tradar_data.py 로 재생성. */\n")
    body = "window.TRADAR_DATA = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n"
    if trade_intel:
        body += "\nwindow.TRADAR_TRADE_INTEL = " + json.dumps(trade_intel, ensure_ascii=False, indent=1) + ";\n"
    with open(TRADAR_JS, "w", encoding="utf-8") as f:
        f.write(header + body)


def main() -> None:
    data = load_data()
    client = CustomsClient()
    if client.available:
        n = refresh_from_customs(data, client)
        emit(data)
        print(f"✓ 관세청 실데이터로 {n}개 품목 갱신 → {os.path.relpath(TRADAR_JS)}")
    else:
        print("· DATA_GO_KR_KEY 미설정 — 2024 관세청 공표치 앵커 유지(데모).")
        print(f"  품목 {len(data['P'])} · 시장 {len(data['markets'])} · 뉴스 {len(data['news'])}")
        print("  인증키 발급: https://www.data.go.kr/data/15100475/openapi.do")


if __name__ == "__main__":
    main()
