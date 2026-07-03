"""거래 인텔리전스 자동수집 커넥터 테스트."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from server.trade_intelligence import (
    ImportYetiClient,
    build_trade_intel_product,
    build_quality_summary,
    parse_company_flow_csv,
    validate_trade_intel_payload,
)
from scripts import build_tradar_data, sync_trade_intel

ROOT = Path(__file__).resolve().parents[2]


def test_public_bl_csv_and_official_stats_build_company_flows():
    public_bl = parse_company_flow_csv(
        """seller,buyer,product,market,marketName,volume_kg,shipments,port,channel
Samyang Foods,US Asian Grocery Network,Buldak ramen,US,미국,2000,3,Busan -> LA,아시안 그로서리
Nongshim,Japan Retail Desk,Bowl noodle,JP,일본,1500,2,Busan -> Osaka,편의점
"""
    )
    official_rows = [
        {"country_name": "미국", "exp_usd": 3000, "exp_kg": 1000},
        {"country_name": "일본", "exp_usd": 3600, "exp_kg": 1200},
    ]

    payload = build_trade_intel_product(
        product_id="ramen",
        product_name="라면",
        hs="1902.30",
        public_flows=public_bl,
        official_rows=official_rows,
    )

    assert payload["productId"] == "ramen"
    assert payload["hs"] == "1902.30"
    assert len(payload["flows"]) == 2
    assert payload["flows"][0]["seller"] == "Samyang Foods"
    assert payload["flows"][0]["unitPriceUsd"] == 3.0
    assert payload["flows"][0]["valueUsd"] == 6000
    assert payload["flows"][0]["sourceTier"] == "public_bl"
    assert payload["flows"][0]["priceStatus"] == "estimated"
    assert payload["flows"][0]["evidence"]


def test_importyeti_company_response_normalizes_supplier_relationships():
    flows = ImportYetiClient.flows_from_company_payload(
        company_slug="wal-mart",
        payload={
            "name": "Wal Mart",
            "top_suppliers": [
                {"name": "K Food Exporter", "country_code": "KR", "total_shipments": 42},
            ],
        },
        product_id="ramen",
        product_name="Instant noodles",
    )

    assert len(flows) == 1
    assert flows[0].product_id == "ramen"
    assert flows[0].seller == "K Food Exporter"
    assert flows[0].buyer == "Wal Mart"
    assert flows[0].market == "US"
    assert flows[0].shipments == 42


def test_sync_trade_intel_rewrites_tradar_js_section(tmp_path, monkeypatch):
    fixture = tmp_path / "tradar.js"
    fixture.write_text(
        "window.TRADAR_DATA = {\"P\":[{\"id\":\"ramen\",\"ko\":\"라면\",\"hs\":\"1902.30\"}],\"markets\":[],\"news\":[]};\n"
        "window.TRADAR_TRADE_INTEL = {\"version\":0,\"products\":{}};\n",
        encoding="utf-8",
    )
    public_csv = tmp_path / "public_bl.csv"
    public_csv.write_text(
        "product_id,seller,buyer,product,market,marketName,volume_kg,shipments\n"
        "ramen,Samyang Foods,US Asian Grocery Network,Buldak ramen,US,미국,2000,3\n",
        encoding="utf-8",
    )

    class FakeCustomsClient:
        available = True
        seen_country_codes = []

        def fetch_item_country(self, hs, start, end, country_codes=None):
            assert hs == "1902.30"
            assert start <= end
            self.seen_country_codes.append(country_codes)
            return [{"country_name": "미국", "exp_usd": 3000, "exp_kg": 1000}]

    monkeypatch.setattr(sync_trade_intel, "TRADAR_JS", str(fixture))

    result = sync_trade_intel.sync_trade_intelligence(
        public_bl_csv=str(public_csv),
        customs_client=FakeCustomsClient(),
        product_ids=["ramen"],
    )

    out = fixture.read_text(encoding="utf-8")
    assert result["updated"] == 1
    assert FakeCustomsClient.seen_country_codes == [["US"]]
    assert "window.TRADAR_DATA" in out
    assert "window.TRADAR_TRADE_INTEL" in out
    assert '"version": 1' in out
    assert "Samyang Foods" in out


def test_sync_trade_intel_limits_official_fetch_to_products_with_flows(tmp_path, monkeypatch):
    fixture = tmp_path / "tradar.js"
    fixture.write_text(
        "window.TRADAR_DATA = {\"P\":["
        "{\"id\":\"ramen\",\"ko\":\"라면\",\"hs\":\"1902.30\"},"
        "{\"id\":\"battery\",\"ko\":\"이차전지\",\"hs\":\"8507.60\"},"
        "{\"id\":\"snacks\",\"ko\":\"과자\",\"hs\":\"1905.90\"}"
        "],\"markets\":[],\"news\":[]};\n"
        "window.TRADAR_TRADE_INTEL = {\"version\":0,\"products\":{}};\n",
        encoding="utf-8",
    )
    public_csv = tmp_path / "public_bl.csv"
    public_csv.write_text(
        "product_id,seller,buyer,product,market,marketName,volume_kg,shipments\n"
        "ramen,Samyang Foods,US Asian Grocery Network,Buldak ramen,US,미국,2000,3\n"
        "battery,Cell Maker,US EV Assembly Plant,Li-ion battery module,US,미국,5000,2\n",
        encoding="utf-8",
    )

    class FakeCustomsClient:
        available = True
        seen = []

        def fetch_item_country(self, hs, start, end, country_codes=None):
            self.seen.append((hs, country_codes))
            return [{"country_name": "미국", "country": "US", "exp_usd": 3000, "exp_kg": 1000}]

    monkeypatch.setattr(sync_trade_intel, "TRADAR_JS", str(fixture))

    sync_trade_intel.sync_trade_intelligence(
        public_bl_csv=str(public_csv),
        customs_client=FakeCustomsClient(),
    )

    assert FakeCustomsClient.seen == [
        ("1902.30", ["US"]),
        ("8507.60", ["US"]),
    ]


def test_sync_trade_intel_partial_product_merge_preserves_other_products(tmp_path, monkeypatch):
    fixture = tmp_path / "tradar.js"
    fixture.write_text(
        "window.TRADAR_DATA = {\"P\":[{\"id\":\"ramen\",\"ko\":\"라면\",\"hs\":\"1902.30\"},{\"id\":\"skincare\",\"ko\":\"기초화장품\",\"hs\":\"3304.99\"}],\"markets\":[],\"news\":[]};\n"
        "window.TRADAR_TRADE_INTEL = {\"version\":1,\"sources\":[],\"products\":{\"skincare\":{\"productId\":\"skincare\",\"flows\":[{\"id\":\"keep\"}]}}};\n",
        encoding="utf-8",
    )
    public_csv = tmp_path / "public_bl.csv"
    public_csv.write_text(
        "product_id,seller,buyer,product,market,marketName,volume_kg,unit_price_usd,shipments\n"
        "ramen,Samyang Foods,US Asian Grocery Network,Buldak ramen,US,미국,2000,3.0,3\n",
        encoding="utf-8",
    )

    class FakeCustomsClient:
        available = False

    monkeypatch.setattr(sync_trade_intel, "TRADAR_JS", str(fixture))

    sync_trade_intel.sync_trade_intelligence(
        public_bl_csv=str(public_csv),
        customs_client=FakeCustomsClient(),
        product_ids=["ramen"],
    )

    out = fixture.read_text(encoding="utf-8")
    assert '"ramen"' in out
    assert '"skincare"' in out
    assert '"keep"' in out


def test_build_tradar_data_emit_preserves_trade_intel_section(tmp_path, monkeypatch):
    fixture = tmp_path / "tradar.js"
    fixture.write_text(
        "window.TRADAR_DATA = {\"P\":[]};\n"
        "window.TRADAR_TRADE_INTEL = {\"version\":1,\"products\":{\"ramen\":{\"flows\":[]}}};\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(build_tradar_data, "TRADAR_JS", str(fixture))

    build_tradar_data.emit({"P": [{"id": "ramen"}]})

    out = fixture.read_text(encoding="utf-8")
    assert "window.TRADAR_DATA" in out
    assert "window.TRADAR_TRADE_INTEL" in out
    assert '"ramen"' in out


def test_quality_summary_exposes_commercial_operating_state():
    payload = {
        "products": {
            "ramen": {
                "flows": [
                    {
                        "seller": "Samyang Foods",
                        "buyer": "US Asian Grocery Network",
                        "market": "US",
                        "confidence": 72,
                        "priceStatus": "estimated",
                        "sourceTier": "public_bl",
                    }
                ]
            }
        }
    }

    quality = build_quality_summary(
        payload,
        [
            {"id": "public_bl_csv", "label": "공개 B/L CSV", "status": "success", "records": 1},
            {"id": "public_bl_api", "label": "공개 B/L API", "status": "failed", "records": 0, "error": "timeout"},
        ],
        generated_at="2026-07-03T12:00:00",
    )

    assert quality["status"] == "degraded"
    assert quality["coverageScore"] < 100
    assert quality["flowCount"] == 1
    assert quality["sellerCount"] == 1
    assert quality["buyerCount"] == 1
    assert quality["estimatedPriceShare"] == 100
    assert quality["connectors"][1]["status"] == "failed"
    assert any("공개 B/L API" in warning for warning in quality["warnings"])


def test_quality_summary_marks_skipped_core_connector_as_degraded():
    payload = {
        "products": {
            "ramen": {
                "flows": [
                    {
                        "seller": "Samyang Foods",
                        "buyer": "US Asian Grocery Network",
                        "market": "US",
                        "confidence": 72,
                        "priceStatus": "estimated",
                        "sourceTier": "public_bl",
                    }
                ]
            }
        }
    }

    quality = build_quality_summary(
        payload,
        [
            {"id": "public_bl_csv", "label": "공개 B/L CSV", "status": "success", "records": 1},
            {"id": "official_customs", "label": "관세청 공식 HS 통계", "status": "skipped", "message": "DATA_GO_KR_KEY missing"},
        ],
        generated_at="2026-07-03T12:00:00",
    )

    assert quality["status"] == "degraded"
    assert any("관세청 공식 HS 통계" in warning for warning in quality["warnings"])


def test_sync_trade_intel_writes_run_report_and_tolerates_partial_connector_failure(tmp_path, monkeypatch):
    fixture = tmp_path / "tradar.js"
    fixture.write_text(
        "window.TRADAR_DATA = {\"P\":[{\"id\":\"ramen\",\"ko\":\"라면\",\"hs\":\"1902.30\"}],\"markets\":[],\"news\":[]};\n"
        "window.TRADAR_TRADE_INTEL = {\"version\":0,\"products\":{}};\n",
        encoding="utf-8",
    )
    public_csv = tmp_path / "public_bl.csv"
    public_csv.write_text(
        "product_id,seller,buyer,product,market,marketName,volume_kg,shipments\n"
        "ramen,Samyang Foods,US Asian Grocery Network,Buldak ramen,US,미국,2000,3\n",
        encoding="utf-8",
    )
    report = tmp_path / "trade_intel_last_run.json"

    class FakeCustomsClient:
        available = True
        seen_country_codes = []

        def fetch_item_country(self, hs, start, end, country_codes=None):
            self.seen_country_codes.append(country_codes)
            return [{"country_name": "미국", "exp_usd": 3000, "exp_kg": 1000}]

    class BrokenPublicBLJsonClient:
        def __init__(self, *args, **kwargs):
            pass

        def fetch(self, **params):
            raise TimeoutError("upstream timeout")

    monkeypatch.setattr(sync_trade_intel, "TRADAR_JS", str(fixture))
    monkeypatch.setattr(sync_trade_intel, "PublicBLJsonClient", BrokenPublicBLJsonClient)

    result = sync_trade_intel.sync_trade_intelligence(
        public_bl_csv=str(public_csv),
        public_bl_api_url="https://example.invalid/public-bl",
        customs_client=FakeCustomsClient(),
        product_ids=["ramen"],
        report_out=str(report),
    )

    out = fixture.read_text(encoding="utf-8")
    run_report = json.loads(report.read_text(encoding="utf-8"))
    assert result["status"] == "degraded"
    assert FakeCustomsClient.seen_country_codes == [["US"]]
    assert '"quality"' in out
    assert run_report["quality"]["status"] == "degraded"
    assert run_report["quality"]["flowCount"] == 1
    assert any(c["id"] == "public_bl_api" and c["status"] == "failed" for c in run_report["connectors"])


def test_trade_intel_validator_blocks_empty_or_stale_payload():
    errors = validate_trade_intel_payload(
        {
            "version": 1,
            "generated": "2026-06-01T00:00:00",
            "products": {},
            "quality": {"status": "blocked"},
        },
        now="2026-07-03T12:00:00",
        max_age_hours=48,
    )

    assert any("stale" in error for error in errors)
    assert any("product" in error for error in errors)
    assert any("blocked" in error for error in errors)


def test_audit_trade_intel_cli_fails_on_stale_payload(tmp_path):
    fixture = tmp_path / "tradar.js"
    fixture.write_text(
        "window.TRADAR_DATA = {\"P\":[]};\n"
        "window.TRADAR_TRADE_INTEL = {\"version\":1,\"generated\":\"2026-06-01T00:00:00\",\"products\":{},\"quality\":{\"status\":\"blocked\"}};\n",
        encoding="utf-8",
    )

    proc = subprocess.run(
        [
            sys.executable,
            "scripts/audit_trade_intel.py",
            "--tradar-js",
            str(fixture),
            "--now",
            "2026-07-03T12:00:00",
            "--max-age-hours",
            "48",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert proc.returncode == 1
    assert "stale" in proc.stdout
    assert "product count" in proc.stdout


def test_check_trade_intel_keys_cli_reports_without_leaking_values(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join([
            "DATA_GO_KR_KEY=secret-data-key",
            "TRADE_INTEL_PUBLIC_BL_CSV=server/data/public_bl_sample.csv",
            "IMPORTYETI_API_KEY=secret-importyeti-key",
        ]),
        encoding="utf-8",
    )

    proc = subprocess.run(
        [
            sys.executable,
            "scripts/check_trade_intel_keys.py",
            "--env-file",
            str(env_file),
            "--json",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    payload = json.loads(proc.stdout)
    assert payload["keys"]["DATA_GO_KR_KEY"]["status"] == "set"
    assert payload["sources"]["public_bl_csv"]["status"] == "set"
    assert payload["keys"]["IMPORTYETI_API_KEY"]["status"] == "set"
    assert "secret-data-key" not in proc.stdout
    assert "secret-importyeti-key" not in proc.stdout
