#!/usr/bin/env python3
"""거래 인텔리전스 payload 배포 전 감사 CLI."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from server.trade_intelligence import validate_trade_intel_payload  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TRADAR_JS = ROOT / "app" / "data" / "tradar.js"


def load_trade_intel(tradar_js: str) -> dict:
    script = (
        "globalThis.window=globalThis.window||{};"
        f"require({json.dumps(os.path.abspath(tradar_js))});"
        "process.stdout.write(JSON.stringify(window.TRADAR_TRADE_INTEL||{}));"
    )
    out = subprocess.run(["node", "-e", script], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit generated TRADAR_TRADE_INTEL before PR/deploy")
    parser.add_argument("--tradar-js", default=str(TRADAR_JS), help="app/data/tradar.js path")
    parser.add_argument("--now", default=None, help="ISO timestamp used for deterministic stale checks")
    parser.add_argument("--max-age-hours", type=int, default=72)
    parser.add_argument("--min-products", type=int, default=1)
    parser.add_argument("--min-flows", type=int, default=1)
    args = parser.parse_args()

    payload = load_trade_intel(args.tradar_js)
    errors = validate_trade_intel_payload(
        payload,
        now=args.now,
        max_age_hours=args.max_age_hours,
        min_products=args.min_products,
        min_flows=args.min_flows,
    )
    if errors:
        print("trade intelligence audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    quality = payload.get("quality") or {}
    print(
        "trade intelligence audit passed: "
        f"status={quality.get('status', 'unknown')} "
        f"products={len(payload.get('products') or {})} "
        f"flows={quality.get('flowCount', 'unknown')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
