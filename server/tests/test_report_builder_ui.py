"""Static regression checks for the homepage report-builder workspace."""
from __future__ import annotations

from pathlib import Path


APP_HTML = Path(__file__).resolve().parents[2] / "app" / "index.html"


def test_report_builder_sections_use_rich_section_models():
    html = APP_HTML.read_text(encoding="utf-8")

    required_bindings = [
        "coverStats",
        "summaryBullets",
        "trendSignals",
        "marketRows",
        "riskFactors",
        "sourceRows",
        "appendixChecks",
    ]
    for binding in required_bindings:
        assert f"rd.{binding}" in html
        assert f"{binding}:{binding}" in html


def test_report_builder_copy_names_decision_oriented_blocks():
    html = APP_HTML.read_text(encoding="utf-8")

    for phrase in [
        "핵심 판단",
        "실행 메모",
        "시장별 액션",
        "완화 플레이북",
        "검증 상태",
    ]:
        assert phrase in html
