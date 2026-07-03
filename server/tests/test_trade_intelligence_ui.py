"""거래 인텔리전스 화면과 무료 데이터 계층 회귀 테스트."""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
APP_INDEX = ROOT / "app" / "index.html"
APP_DATA = ROOT / "app" / "data" / "tradar.js"


def test_trade_intelligence_screen_exposes_commercial_workflow():
    html = APP_INDEX.read_text(encoding="utf-8")

    assert "거래 인텔리전스" in html
    assert "buildTradeIntelligence" in html
    assert "downloadTradeCsv" in html
    assert "isTradeIntel" in html
    assert "기업 → 상품 → 시장 → 바이어" in html
    assert "운영 상태" in html
    assert "데이터 신선도" in html
    assert "품질 점수" in html
    assert "커넥터 상태" in html
    assert "tdr-quality-status-badge" in html
    assert "renderTradeOps" in html
    assert "무료 공개데이터 MVP" not in html

    for tier in ("공식", "공개 B/L", "추정", "업로드"):
        assert tier in html

    for question in (
        "어떤 기업이",
        "어디에 얼마로",
        "얼마나 팔고",
        "바이어 후보",
    ):
        assert question in html


def _load_tradar_payload() -> dict:
    if shutil.which("node") is None:
        pytest.skip("node is required to evaluate tradar.js")

    script = """
      global.window = {};
      require(process.argv[1]);
      console.log(JSON.stringify({
        data: window.TRADAR_DATA,
        trade: window.TRADAR_TRADE_INTEL
      }));
    """
    proc = subprocess.run(
        ["node", "-e", script, str(APP_DATA)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def test_company_flow_payload_separates_free_data_tiers():
    payload = _load_tradar_payload()
    trade = payload["trade"]

    assert trade["version"] == 1
    assert trade["quality"]["status"] in {"operational", "degraded"}
    assert trade["quality"]["flowCount"] >= 5
    assert trade["quality"]["coverageScore"] >= 50
    assert {s["tier"] for s in trade["sources"]} >= {"official", "public_bl", "estimate", "upload"}
    assert "ramen" in trade["products"]

    ramen = trade["products"]["ramen"]
    assert ramen["hs"] == "1902.30"
    assert len(ramen["flows"]) >= 5

    for flow in ramen["flows"]:
        assert {"seller", "buyer", "product", "market", "unitPriceUsd", "volume", "valueUsd"} <= set(flow)
        assert flow["sourceTier"] in {"official", "public_bl", "estimate", "upload"}
        assert flow["priceStatus"] in {"market_average", "estimated", "uploaded_exact", "not_available"}
        assert 0 <= flow["confidence"] <= 100
        assert flow["evidence"]

    confirmed = [f for f in ramen["flows"] if f["priceStatus"] == "uploaded_exact"]
    assert confirmed == []
