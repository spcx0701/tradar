#!/usr/bin/env python3
"""산업통상부 공공데이터 동기화 — app/app/data/motie.js 생성.

산업통상부 산하기관(K-SURE·KOTRA) 공공데이터를 받아 Tradar 대시보드가 소비하는
``window.TRADAR_MOTIE`` 페이로드(app/app/data/motie.js)를 재생성한다.

- ``DATA_GO_KR_KEY`` 설정 시: K-SURE 국별신용등급·KOTRA 해외시장뉴스 실데이터 동기화.
- 미설정 시: 공표치 앵커(K-SURE 등급·OECD 국가위험분류·對韓 수입규제 집계) 유지 — 데모는 항상 동작.

사용: python scripts/sync_motie_data.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from server.motie_client import MotieClient  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
TRADAR_JS = os.path.join(ROOT, "app", "app", "data", "tradar.js")
MOTIE_JS = os.path.join(ROOT, "app", "app", "data", "motie.js")


def market_codes() -> list[str]:
    """대시보드 markets 국가 코드 목록(tradar.js 기준) — node로 평가."""
    js = ("globalThis.window=globalThis.window||{};"
          f"require({json.dumps(os.path.abspath(TRADAR_JS))});"
          "process.stdout.write(JSON.stringify(window.TRADAR_DATA.markets.map(m=>m.code)));")
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def main() -> None:
    codes = market_codes()
    client = MotieClient()
    payload = client.build_payload(codes)
    payload["generated"] = datetime.now().isoformat(timespec="seconds")

    header = ("/* Tradar 산업통상부 공공데이터 레이어 — K-SURE 국별신용등급·위험지수, "
              "KOTRA 해외시장뉴스·수입규제.\n"
              f"   생성: {payload['generated']} · scripts/sync_motie_data.py 로 재생성. */\n")
    body = "window.TRADAR_MOTIE = " + json.dumps(payload, ensure_ascii=False, indent=1) + ";\n"
    with open(MOTIE_JS, "w", encoding="utf-8") as f:
        f.write(header + body)

    tag = "실데이터 동기화" if payload["mode"] == "live" else "공표치 앵커(데모)"
    print(f"✓ 산업부 데이터 {tag} — 국가 {len(payload['countries'])} · "
          f"KOTRA 뉴스 {len(payload['news'])} → {os.path.relpath(MOTIE_JS)}")
    if payload["mode"] == "anchor":
        print("  DATA_GO_KR_KEY 설정 시 K-SURE·KOTRA OpenAPI 실시간 동기화로 전환됩니다.")


if __name__ == "__main__":
    main()
