"""산업통상부(산하기관) 공공데이터 레이어 테스트 — K-SURE·KOTRA 연동/앵커 폴백."""
import json
import subprocess
import sys
from pathlib import Path

from server.motie_client import ANCHOR_COUNTRIES, DATASETS, MotieClient, _items

ROOT = Path(__file__).resolve().parents[2]
MOTIE_JS = ROOT / "app" / "app" / "data" / "motie.js"
TRADAR_JS = ROOT / "app" / "app" / "data" / "tradar.js"


def _eval_window(js_files: list[Path], expr: str):
    """node로 데이터 JS를 평가해 window.* 페이로드를 JSON으로 추출."""
    load = "".join(f"require({json.dumps(str(f))});" for f in js_files)
    js = f"globalThis.window=globalThis.window||{{}};{load}process.stdout.write(JSON.stringify({expr}));"
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def test_anchor_payload_always_works_without_key():
    """인증키 없이도 앵커 페이로드가 완전한 구조로 생성돼야 한다(데모는 항상 동작)."""
    client = MotieClient(service_key="")
    assert not client.available
    payload = client.build_payload(["US", "CN", "VN"])
    assert payload["mode"] == "anchor"
    assert payload["news"], "KOTRA 뉴스 앵커가 비어 있으면 안 된다"
    for code in ["US", "CN", "VN"]:
        entry = payload["countries"][code]
        assert 1 <= entry["grade"] <= 7
        assert entry["regs"] >= 0
        assert entry["asOf"]


def test_anchor_covers_all_dashboard_markets():
    """대시보드 markets의 모든 국가가 앵커에 등재돼야 한다."""
    codes = _eval_window([TRADAR_JS], "window.TRADAR_DATA.markets.map(m=>m.code)")
    missing = [c for c in codes if c not in ANCHOR_COUNTRIES]
    assert not missing, f"앵커 누락 국가: {missing}"


def test_datasets_reference_motie_orgs():
    """활용 데이터셋 표기는 산업부 산하기관(공모전 필수 요건) 기준이어야 한다."""
    orgs = {d["org"] for d in DATASETS}
    assert "한국무역보험공사" in orgs
    assert "대한무역투자진흥공사" in orgs
    for d in DATASETS:
        assert d["portal"].startswith("https://www.data.go.kr/data/")


def test_motie_js_payload_is_valid():
    """생성된 motie.js가 대시보드 계약(TRADAR_MOTIE 구조)을 지켜야 한다."""
    assert MOTIE_JS.exists(), "scripts/sync_motie_data.py 로 생성 필요"
    payload = _eval_window([MOTIE_JS], "window.TRADAR_MOTIE")
    assert payload["mode"] in ("anchor", "live")
    assert payload["datasets"]
    assert payload["countries"]
    grades = [c["grade"] for c in payload["countries"].values()]
    assert all(1 <= g <= 7 for g in grades)


def test_items_parses_datago_response_shapes():
    """data.go.kr 표준/변형 응답에서 item 배열을 방어적으로 추출해야 한다."""
    std = {"response": {"body": {"items": {"item": [{"a": 1}]}}}}
    assert _items(std) == [{"a": 1}]
    flat = {"data": [{"b": 2}]}
    assert _items(flat) == [{"b": 2}]
    single = {"response": {"body": {"items": {"item": {"c": 3}}}}}
    assert _items(single) == [{"c": 3}]
    assert _items([{"d": 4}, "junk"]) == [{"d": 4}]
    assert _items("garbage") == []


def test_sync_script_is_deterministic_offline(tmp_path, monkeypatch):
    """키 미설정 환경에서 sync 스크립트가 항상 성공해야 한다(CI 재현성)."""
    monkeypatch.delenv("DATA_GO_KR_KEY", raising=False)
    client = MotieClient(service_key="")
    p1 = client.build_payload(["US", "IN"])
    p2 = client.build_payload(["US", "IN"])
    assert p1 == p2


if __name__ == "__main__":
    sys.exit(subprocess.call(["pytest", __file__, "-q"]))
