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


def test_web_chatbot_uses_deployed_advisor_api_without_local_answer_fallback():
    html = APP_INDEX.read_text(encoding="utf-8")

    assert "TRADAR_API_BASE" in html
    assert "callAdvisorApi" in html
    assert "fetch(base+'/advisor'" in html
    assert "location.hostname.indexOf('github.io') === -1" in html
    assert "location.origin + '/api'" in html
    assert "advisorSource" in html
    assert "api-fallback" not in html
    assert "this.respond(v)" not in html
    assert "서버의 한국 LLM 응답을 기다리는 중입니다." in html


def test_web_chatbot_file_url_defaults_to_render_api():
    html = APP_INDEX.read_text(encoding="utf-8")

    assert "location.protocol === 'file:'" in html
    assert "https://tradar.onrender.com/api" in html


def test_web_chatbot_does_not_hardcode_greeting_fallback():
    html = APP_INDEX.read_text(encoding="utf-8")

    assert "isChatGreeting(t)" not in html
    assert "안녕하세요. Tradar AI 애널리스트입니다." not in html


def test_web_chatbot_does_not_submit_during_korean_ime_composition():
    html = APP_INDEX.read_text(encoding="utf-8")

    assert "e.isComposing" in html
    assert "keyCode===229" in html


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
