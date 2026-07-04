"""API, 설정, 데이터 파이프라인 회귀 테스트."""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from datetime import datetime

import numpy as np
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from scripts import build_app_data, build_tradar_data, generate_snapshot
from server.advisor import KoreanLLMAdapter, answer, build_llm_adapter
from server.env import load_env_file
from server.config import Settings
from server.customs_client import CustomsClient, _to_int
from server.dataset import Dataset, get_dataset
from server.main import app
from server.schemas import AdvisorRequest

ROOT = Path(__file__).resolve().parents[2]


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


def test_render_blueprint_deploys_fastapi_server_and_pages_can_receive_api_base():
    render_yaml = (ROOT / "render.yaml").read_text(encoding="utf-8")
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "name: tradar" in render_yaml
    assert "region: singapore" in render_yaml
    assert "runtime: python" in render_yaml
    assert "pip install -r requirements.txt" in render_yaml
    assert "uvicorn server.main:app --host 0.0.0.0 --port $PORT" in render_yaml
    assert "https://spcx0701.github.io,https://tradar.onrender.com" in render_yaml
    assert "TW_LLM_PROVIDER" in render_yaml
    assert "sync: false" in render_yaml
    assert "TRADEWIND_API_BASE" in workflow
    assert "app/app/data/api-config.js" in workflow
    assert "window.TRADAR_API_BASE" in workflow


def test_public_app_surfaces_default_to_render_single_origin():
    expected_web = "https://tradar.onrender.com/"
    expected_api = "https://tradar.onrender.com/api"
    expected_data = "https://tradar.onrender.com/data"

    surfaces = {
        "README.md": ROOT / "README.md",
        "README.en.md": ROOT / "README.en.md",
        "docs/ARCHITECTURE.md": ROOT / "docs" / "ARCHITECTURE.md",
        "packaging/android/README.md": ROOT / "packaging" / "android" / "README.md",
        "packaging/android/app/build.gradle.kts": ROOT / "packaging" / "android" / "app" / "build.gradle.kts",
        "packaging/android/app/src/main/res/values/strings.xml": (
            ROOT / "packaging" / "android" / "app" / "src" / "main" / "res" / "values" / "strings.xml"
        ),
        "packaging/android/app/src/main/java/kr/tradewind/app/MainActivity.kt": (
            ROOT / "packaging" / "android" / "app" / "src" / "main" / "java" / "kr" / "tradewind" / "app" / "MainActivity.kt"
        ),
        "packaging/android/app/src/main/java/kr/tradewind/app/data/Repository.kt": (
            ROOT / "packaging" / "android" / "app" / "src" / "main" / "java" / "kr" / "tradewind" / "app" / "data" / "Repository.kt"
        ),
        ".env.example": ROOT / ".env.example",
    }

    text_by_name = {name: path.read_text(encoding="utf-8") for name, path in surfaces.items()}
    for name, text in text_by_name.items():
        assert "tradar-api.onrender.com" not in text, name

    assert expected_web in text_by_name["README.md"]
    assert expected_web in text_by_name["README.en.md"]
    assert expected_web in text_by_name["packaging/android/app/src/main/java/kr/tradewind/app/MainActivity.kt"]
    assert "site\\\": \\\"https://tradar.onrender.com\\\"" in text_by_name[
        "packaging/android/app/src/main/res/values/strings.xml"
    ]
    assert expected_api in text_by_name["packaging/android/README.md"]
    assert expected_api in text_by_name[".env.example"]
    assert expected_data in text_by_name["packaging/android/app/build.gradle.kts"]
    assert expected_data in text_by_name["packaging/android/app/src/main/java/kr/tradewind/app/data/Repository.kt"]


def test_load_env_file_reads_dotenv_without_overriding_existing_values(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join([
            "DATA_GO_KR_KEY=decoded-key",
            "TRADE_INTEL_PUBLIC_BL_CSV=server/data/public_bl_sample.csv",
            "IMPORTYETI_API_KEY='iy-key'",
            "TW_CORS=https://from-file.example",
        ]),
        encoding="utf-8",
    )
    monkeypatch.delenv("DATA_GO_KR_KEY", raising=False)
    monkeypatch.delenv("TRADE_INTEL_PUBLIC_BL_CSV", raising=False)
    monkeypatch.delenv("IMPORTYETI_API_KEY", raising=False)
    monkeypatch.setenv("TW_CORS", "https://already-set.example")

    loaded = load_env_file(env_file)

    assert loaded["DATA_GO_KR_KEY"] == "decoded-key"
    assert loaded["IMPORTYETI_API_KEY"] == "iy-key"
    assert os.environ["DATA_GO_KR_KEY"] == "decoded-key"
    assert os.environ["TRADE_INTEL_PUBLIC_BL_CSV"] == "server/data/public_bl_sample.csv"
    assert os.environ["TW_CORS"] == "https://already-set.example"


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

    assert row["year"] == "2025"
    assert row["country_name"] == "미국"
    assert row["exp_usd"] == 1234
    assert row["exp_kg"] == 5678
    assert row["imp_usd"] == 0
    assert row["imp_kg"] == 0
    assert _to_int("1,000.9") == 1000
    with pytest.raises(RuntimeError):
        CustomsClient(service_key="").fetch_item_country("1902.30", "202401", "202412")


def test_customs_client_builds_country_scoped_url_and_parses_current_schema():
    url = CustomsClient(service_key="demo")._build_url("1902.30", "202501", "202512", "US")

    assert "hsSgn=190230" in url
    assert "strtYymm=202501" in url
    assert "endYymm=202512" in url
    assert "cntyCd=US" in url

    xml = """
    <response><body><items>
      <item>
        <year>2025.01</year><statCdCntnKor1>미국</statCdCntnKor1><statCd>US</statCd>
        <statKor>라면</statKor><hsCd>190230</hsCd>
        <expDlr>100</expDlr><expWgt>20</expWgt>
        <impDlr>7</impDlr><impWgt>3</impWgt>
      </item>
    </items></body></response>
    """

    row = CustomsClient._parse(xml)[0]

    assert row["year"] == "2025"
    assert row["month"] == "01"
    assert row["country_name"] == "미국"
    assert row["country"] == "US"
    assert row["hs"] == "190230"
    assert row["exp_usd"] == 100
    assert row["exp_kg"] == 20


def test_customs_client_splits_long_ranges_into_one_year_windows():
    assert CustomsClient._month_windows("202407", "202607") == [
        ("202407", "202506"),
        ("202507", "202606"),
        ("202607", "202607"),
    ]


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
    assert ds.last_n_sum(np.array([1, 2, 3]), 2) == pytest.approx(5.0)
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
    failed = answer(ds, "전체 현황 알려줘", llm=BrokenRefiner())
    assert failed["engine"] == "demo-grounded-fallback"
    assert failed["llm_error"] == "provider down"
    assert "한국 LLM 연결에 실패했습니다" in failed["answer"]
    assert "무역풍은" in failed["answer"]
    with pytest.raises(RuntimeError):
        KoreanLLMAdapter().refine("q", {"evidence": []}, "draft")


def test_advisor_greeting_does_not_mask_llm_failure_with_hardcoded_answer():
    ds = get_dataset()

    class BrokenRefiner:
        def refine(self, question, pack, draft):
            raise RuntimeError("provider suspended")

    failed = answer(ds, "안녕", llm=BrokenRefiner())

    assert failed["intent"]["intent"] == "smalltalk"
    assert failed["engine"] == "demo-grounded-fallback"
    assert failed["llm_error"] == "provider suspended"
    assert "한국 LLM 연결에 실패했습니다" in failed["answer"]
    assert "안녕하세요. Tradar AI 애널리스트입니다." not in failed["answer"]


def test_korean_llm_adapter_posts_grounded_chat_completion_payload():
    captured = {}

    def fake_transport(url, headers, payload, timeout):
        captured["url"] = url
        captured["headers"] = headers
        captured["payload"] = payload
        captured["timeout"] = timeout
        return {
            "choices": [
                {
                    "message": {
                        "content": "국산 LLM이 근거 수치를 유지해 다듬은 답변"
                    }
                }
            ]
        }

    adapter = KoreanLLMAdapter(
        provider="solar",
        api_key="test-key",
        model="solar-pro3",
        transport=fake_transport,
    )

    refined = adapter.refine(
        "라면 어디에 수출하면 좋을까?",
        {"headline": "초안", "evidence": [{"label": "미국 라면", "value": "YoY +65%"}]},
        "초안 답변",
    )

    assert refined == "국산 LLM이 근거 수치를 유지해 다듬은 답변"
    assert captured["url"] == "https://api.upstage.ai/v1/chat/completions"
    assert captured["headers"]["Authorization"] == "Bearer test-key"
    assert captured["payload"]["model"] == "solar-pro3"
    assert captured["payload"]["temperature"] == 0.2
    assert "YoY +65%" in captured["payload"]["messages"][1]["content"]


def test_build_llm_adapter_uses_configured_solar_defaults():
    settings = Settings()
    settings.llm_provider = "solar"
    settings.llm_api_key = "test-key"

    adapter = build_llm_adapter(settings)

    assert adapter is not None
    assert adapter.provider == "solar"
    assert adapter.model == "solar-pro3"


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
