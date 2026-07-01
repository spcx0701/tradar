"""API, 설정, 데이터 파이프라인 회귀 테스트."""
from __future__ import annotations

import json
import shutil
from datetime import datetime

import numpy as np
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from scripts import build_app_data, build_tradar_data, generate_snapshot
from server.advisor import KoreanLLMAdapter, answer
from server.config import Settings
from server.customs_client import CustomsClient, _to_int
from server.dataset import Dataset, get_dataset
from server.main import app
from server.schemas import AdvisorRequest


def test_settings_reads_environment(monkeypatch):
    monkeypatch.setenv("DATA_GO_KR_KEY", "demo-key")
    monkeypatch.setenv("TW_LLM_PROVIDER", "solar")
    monkeypatch.setenv("TW_LLM_KEY", "llm-key")
    monkeypatch.setenv("TW_CORS", "https://example.test")

    settings = Settings()

    assert settings.live_data is True
    assert settings.data_go_kr_key == "demo-key"
    assert settings.llm_provider == "solar"
    assert settings.llm_api_key == "llm-key"
    assert settings.cors_origins == "https://example.test"


def test_customs_client_parses_xml_and_requires_key():
    xml = """
    <response><body><items>
      <item>
        <year>2025</year><statKor>미국</statKor>
        <expDlr>1,234.0</expDlr><expWgt>5,678</expWgt>
        <impDlr></impDlr><impWgt>bad</impWgt>
      </item>
    </items></body></response>
    """

    row = CustomsClient._parse(xml)[0]

    assert row == {
        "year": "2025",
        "country_name": "미국",
        "exp_usd": 1234,
        "exp_kg": 5678,
        "imp_usd": 0,
        "imp_kg": 0,
    }
    assert _to_int("1,000.9") == 1000
    with pytest.raises(RuntimeError):
        CustomsClient(service_key="").fetch_item_country("1902.30", "202401", "202412")


def test_dataset_fallbacks_and_aggregates():
    raw = {
        "meta": {"period": "2024-01 ~ 2025-12"},
        "months": [f"2024-{m:02d}" for m in range(1, 13)]
        + [f"2025-{m:02d}" for m in range(1, 13)],
        "countries": {"US": "미국"},
        "products": [{"hs": "1902.30", "name_ko": "라면", "category": "K-Food"}],
        "series": [
            {"hs": "1902.30", "country": "US", "exp_usd": list(range(1, 25))},
            {"hs": "1902.30", "country": "JP", "exp_usd": [2] * 24},
        ],
    }
    ds = Dataset(raw)

    assert ds.product_name("9999.99") == "9999.99"
    assert ds.country_name("ZZ") == "ZZ"
    assert sorted(ds.markets_of("1902.30")) == ["JP", "US"]
    assert ds.series("1902.30", "US").tolist() == list(range(1, 25))
    assert ds.product_total("1902.30").shape == (24,)
    assert ds.product_total("missing").tolist() == [0] * 24
    assert ds.market_total("US").tolist() == list(range(1, 25))
    assert ds.last_n_sum(np.array([1, 2, 3]), 2) == 5.0
    assert ds.yoy(np.array([1, 2, 3])) == 0.0
    assert ds.yoy(np.array([0] * 12 + [1] * 12)) == 0.0


def test_api_endpoints_cover_success_and_not_found():
    client = TestClient(app)

    assert client.get("/").status_code == 200
    health = client.get("/api/health").json()
    assert health["status"] == "ok"
    assert health["products"] == 12
    catalog = client.get("/api/catalog").json()
    assert "countries" in catalog and "products" in catalog

    forecast = client.get("/api/forecast", params={"hs": "1902.30", "country": "US", "horizon": 3}).json()
    assert forecast["country_name"] == "미국"
    assert len(forecast["fc_months"]) == 3
    assert client.get("/api/forecast", params={"hs": "bad", "country": "ZZ"}).status_code == 404

    radar = client.get("/api/radar", params={"limit": 3}).json()
    assert len(radar["top"]) == 3
    product = client.get("/api/radar/product/1902.30").json()
    assert product["product"].startswith("라면")
    assert client.get("/api/radar/product/bad").status_code == 404

    advisor = client.post("/api/advisor", json={"question": "라면 어디에 수출하면 좋을까?"}).json()
    assert advisor["question"]
    assert advisor["evidence"]


def test_advisor_llm_fallback_and_refine():
    ds = get_dataset()

    class Refiner:
        def refine(self, question, pack, draft):
            assert question
            assert pack["evidence"]
            assert draft
            return "다듬은 답변"

    class BrokenRefiner:
        def refine(self, question, pack, draft):
            raise RuntimeError("provider down")

    assert answer(ds, "전체 현황 알려줘", llm=Refiner())["answer"] == "다듬은 답변"
    assert "무역풍은" in answer(ds, "전체 현황 알려줘", llm=BrokenRefiner())["answer"]
    with pytest.raises(NotImplementedError):
        KoreanLLMAdapter().refine("q", {"evidence": []}, "draft")


def test_schema_validation_rejects_blank_question():
    with pytest.raises(ValidationError):
        AdvisorRequest(question="")


def test_generate_snapshot_helpers_build_realistic_series():
    months = generate_snapshot.month_labels()
    series = generate_snapshot.build_series(months)

    assert months[0] == "2021-01"
    assert len(months) == generate_snapshot.N_MONTHS
    assert len(series) > len(generate_snapshot.PRODUCTS)
    first = series[0]
    assert {"hs", "country", "exp_usd", "exp_kg"} <= set(first)
    assert len(first["exp_usd"]) == len(months)
    assert all(v > 0 for v in first["exp_usd"])


def test_build_app_data_writes_static_payloads(tmp_path, monkeypatch):
    monkeypatch.setattr(build_app_data, "OUT", str(tmp_path))

    build_app_data.main()

    catalog = json.loads((tmp_path / "catalog.json").read_text(encoding="utf-8"))
    forecast = json.loads((tmp_path / "forecast.json").read_text(encoding="utf-8"))
    radar = json.loads((tmp_path / "radar.json").read_text(encoding="utf-8"))
    countries = json.loads((tmp_path / "countries.json").read_text(encoding="utf-8"))

    assert build_app_data.future_months(["2025-11"], 3) == ["2025-12", "2026-01", "2026-02"]
    assert catalog["products"]
    assert forecast["series"]
    assert radar["top"] and radar["by_product"]
    assert countries["countries"]


def test_build_tradar_data_refreshes_from_customs():
    data = {
        "P": [
            {"id": "ramen", "hs": "1902.30"},
            {"id": "static"},
            {"id": "bad", "hs": "0000.00"},
        ]
    }

    class FakeClient:
        def fetch_item_country(self, hs, start, end):
            assert start <= end
            if hs == "0000.00":
                raise RuntimeError("not found")
            return [
                {"year": "2024", "country_name": "미국", "exp_usd": 400_000_000},
                {"year": "2024", "country_name": "일본", "exp_usd": 100_000_000},
                {"year": "2025", "country_name": "미국", "exp_usd": 600_000_000},
                {"year": "2025", "country_name": "일본", "exp_usd": 300_000_000},
                {"year": "2025", "country_name": "독일", "exp_usd": 100_000_000},
            ]

    assert build_tradar_data.refresh_from_customs(data, FakeClient()) == 1
    assert data["P"][0]["ann"] == 1000
    assert data["P"][0]["yoy"] == 100.0
    assert data["P"][0]["mk"][0] == ["US", 60, 50]
    assert build_tradar_data._country_code("알수없는나라") == "알수"
    assert build_tradar_data._ym(datetime(2026, 7, 1)) == "202607"


def test_build_tradar_load_data_from_javascript(tmp_path, monkeypatch):
    if shutil.which("node") is None:
        pytest.skip("node is required to evaluate tradar.js")
    fixture = tmp_path / "tradar.js"
    fixture.write_text("window.TRADAR_DATA={P:[{id:'ramen'}],markets:{US:'미국'},news:[]};", encoding="utf-8")
    monkeypatch.setattr(build_tradar_data, "TRADAR_JS", str(fixture))

    assert build_tradar_data.load_data()["P"][0]["id"] == "ramen"
