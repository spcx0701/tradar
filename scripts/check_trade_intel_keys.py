#!/usr/bin/env python3
"""Report Tradar connector key readiness without printing secret values."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from server.env import load_env_file  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


KEYS = [
    ("DATA_GO_KR_KEY", "관세청 공식 HS 통계"),
    ("TRADE_INTEL_PUBLIC_BL_API_KEY", "공개 B/L JSON API"),
    ("IMPORTYETI_API_KEY", "ImportYeti API"),
    ("TW_LLM_KEY", "AI 답변 보강 LLM"),
]


def status_for_value(value: str) -> dict:
    return {"status": "set" if value else "missing", "length": len(value) if value else 0}


def build_status() -> dict:
    keys = {
        key: {"label": label, **status_for_value(os.environ.get(key, ""))}
        for key, label in KEYS
    }
    public_csv = os.environ.get("TRADE_INTEL_PUBLIC_BL_CSV", "")
    public_api = os.environ.get("TRADE_INTEL_PUBLIC_BL_API_URL", "")
    sources = {
        "public_bl_csv": {
            "label": "공개 B/L CSV",
            "status": "set" if public_csv else "missing",
            "pathExists": bool(public_csv and (ROOT / public_csv).exists()),
        },
        "public_bl_api": {
            "label": "공개 B/L JSON API",
            "status": "set" if public_api else "missing",
            "needsKey": bool(public_api and not os.environ.get("TRADE_INTEL_PUBLIC_BL_API_KEY", "")),
        },
        "importyeti": {
            "label": "ImportYeti API",
            "status": "set" if os.environ.get("IMPORTYETI_API_KEY", "") else "missing",
        },
    }
    live_ready = bool(keys["DATA_GO_KR_KEY"]["status"] == "set") and any(
        source["status"] == "set" for source in sources.values()
    )
    return {"liveReady": live_ready, "keys": keys, "sources": sources}


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Tradar trade-intelligence keys without exposing secrets")
    parser.add_argument("--env-file", default=str(ROOT / ".env"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    load_env_file(args.env_file)
    status = build_status()
    if args.json:
        print(json.dumps(status, ensure_ascii=False, indent=2))
        return 0
    print("거래 인텔리전스 키 상태")
    print(f"- liveReady: {status['liveReady']}")
    for key, info in status["keys"].items():
        print(f"- {key}: {info['status']} (len={info['length']}) · {info['label']}")
    for source, info in status["sources"].items():
        suffix = ""
        if "pathExists" in info:
            suffix = f" · pathExists={info['pathExists']}"
        if info.get("needsKey"):
            suffix += " · api key missing"
        print(f"- {source}: {info['status']} · {info['label']}{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
