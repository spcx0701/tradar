#!/usr/bin/env python3
"""거래 인텔리전스 자동수집 동기화.

실행 예:

    DATA_GO_KR_KEY=... python scripts/sync_trade_intel.py --public-bl-csv data/public_bl.csv

동작:
1. app/data/tradar.js 에서 현재 제품 카탈로그(window.TRADAR_DATA)를 읽는다.
2. 관세청 품목별 국가별 수출입실적 API로 HS x 국가 공식 금액/중량을 갱신한다.
3. 공개 B/L 또는 사용자 CSV의 회사/바이어/선적 흐름을 정규화한다.
4. window.TRADAR_TRADE_INTEL 섹션을 재생성한다.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from server.customs_client import DEFAULT_COUNTRY_CODES, CustomsClient  # noqa: E402
from server.trade_intelligence import (  # noqa: E402
    ConnectorRun,
    ImportYetiClient,
    PublicBLJsonClient,
    build_quality_summary,
    build_trade_intel_payload,
    parse_company_flow_csv,
)

ROOT = Path(__file__).resolve().parents[1]
TRADAR_JS = str(ROOT / "app" / "app" / "data" / "tradar.js")
RUN_REPORT_JSON = str(ROOT / "server" / "data" / "trade_intel_last_run.json")


def load_tradar_data() -> dict:
    """node로 tradar.js를 평가해 window.TRADAR_DATA를 추출한다."""
    js = (
        "globalThis.window=globalThis.window||{};"
        f"require({json.dumps(os.path.abspath(TRADAR_JS))});"
        "process.stdout.write(JSON.stringify(window.TRADAR_DATA));"
    )
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def load_trade_intel() -> dict:
    js = (
        "globalThis.window=globalThis.window||{};"
        f"require({json.dumps(os.path.abspath(TRADAR_JS))});"
        "process.stdout.write(JSON.stringify(window.TRADAR_TRADE_INTEL||{version:1,sources:[],products:{}}));"
    )
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def sync_trade_intelligence(
    *,
    public_bl_csv: str = "",
    public_bl_api_url: str = "",
    importyeti_companies: list[str] | None = None,
    customs_client: CustomsClient | None = None,
    customs_timeout: int = 8,
    customs_market_limit: int = 3,
    product_ids: list[str] | None = None,
    report_out: str = "",
    strict: bool = False,
    stale_after_hours: int = 48,
) -> dict:
    data = load_tradar_data()
    products = data.get("P", [])
    if product_ids:
        wanted = set(product_ids)
        products = [p for p in products if p.get("id") in wanted]
    public_flows = []
    connectors: list[ConnectorRun] = []
    if public_bl_csv:
        try:
            csv_text = Path(public_bl_csv).read_text(encoding="utf-8")
            csv_flows = parse_company_flow_csv(csv_text)
            public_flows.extend(csv_flows)
            connectors.append(ConnectorRun(
                id="public_bl_csv",
                label="공개 B/L CSV",
                status="success",
                records=len(csv_flows),
                message=os.path.relpath(public_bl_csv, ROOT) if os.path.exists(public_bl_csv) else public_bl_csv,
                source_tier="public_bl",
            ))
        except Exception as exc:  # noqa: BLE001
            connectors.append(ConnectorRun(
                id="public_bl_csv",
                label="공개 B/L CSV",
                status="failed",
                error=str(exc),
                source_tier="public_bl",
            ))
            if strict:
                raise
    if public_bl_api_url:
        client_api = PublicBLJsonClient(public_bl_api_url, api_key=os.environ.get("TRADE_INTEL_PUBLIC_BL_API_KEY", ""))
        api_count = 0
        api_errors = []
        for p in products:
            try:
                fetched = client_api.fetch(product_id=p.get("id", ""), hs=p.get("hs", ""), q=p.get("ko", ""))
                api_count += len(fetched)
                public_flows.extend(fetched)
            except Exception as exc:  # noqa: BLE001
                api_errors.append(f"{p.get('id')}: {exc}")
                if strict:
                    raise
        connectors.append(ConnectorRun(
            id="public_bl_api",
            label="공개 B/L API",
            status="failed" if api_errors and api_count == 0 else "degraded" if api_errors else "success",
            records=api_count,
            error="; ".join(api_errors[:3]),
            message=public_bl_api_url,
            source_tier="public_bl",
        ))
    if importyeti_companies:
        iy = ImportYetiClient(api_key=os.environ.get("IMPORTYETI_API_KEY", ""))
        import_count = 0
        import_errors = []
        for p in products:
            for company in importyeti_companies:
                try:
                    fetched = iy.fetch_company(company, product_id=p.get("id", ""), product_name=p.get("ko", ""))
                    import_count += len(fetched)
                    public_flows.extend(fetched)
                except Exception as exc:  # noqa: BLE001
                    import_errors.append(f"{company}/{p.get('id')}: {exc}")
                    if strict:
                        raise
        connectors.append(ConnectorRun(
            id="importyeti",
            label="ImportYeti",
            status="failed" if import_errors and import_count == 0 else "degraded" if import_errors else "success",
            records=import_count,
            error="; ".join(import_errors[:3]),
            message=", ".join(importyeti_companies),
            source_tier="public_bl",
        ))
    if not public_flows:
        connectors.append(ConnectorRun(
            id="public_bl",
            label="공개 B/L 통합",
            status="failed",
            error="CSV, JSON API, ImportYeti 중 수집된 거래 흐름이 없습니다.",
            source_tier="public_bl",
        ))
        if strict:
            raise RuntimeError("공개 B/L 입력이 없습니다. CSV, JSON API URL, ImportYeti company 중 하나가 필요합니다.")
    client = customs_client or CustomsClient(timeout=customs_timeout)
    official: dict[str, list[dict]] = {}
    start, end = _sync_window()
    if client.available:
        official_count = 0
        official_errors = []
        official_products = _official_products(products, public_flows, product_ids)
        skipped = max(0, len(products) - len(official_products))
        for p in official_products:
            hs = p.get("hs")
            if not hs:
                continue
            markets = _markets_for_product(
                public_flows,
                p.get("id", ""),
                limit=customs_market_limit,
                fallback_to_default=bool(product_ids),
            )
            try:
                rows = client.fetch_item_country(
                    hs,
                    start,
                    end,
                    country_codes=markets,
                )
                official[p["id"]] = rows
                official_count += len(rows)
            except Exception as exc:  # noqa: BLE001
                official_errors.append(f"{p['id']} {hs}: {exc}")
                official[p["id"]] = []
                if strict:
                    raise
        connectors.append(ConnectorRun(
            id="official_customs",
            label="관세청 공식 HS 통계",
            status="failed" if official_errors and official_count == 0 else "degraded" if official_errors else "success",
            records=official_count,
            error="; ".join(official_errors[:3]),
            message=f"{start}-{end} · products={len(official_products)} · skipped={skipped} · marketLimit={customs_market_limit}",
            source_tier="official",
        ))
    else:
        connectors.append(ConnectorRun(
            id="official_customs",
            label="관세청 공식 HS 통계",
            status="skipped",
            message="DATA_GO_KR_KEY가 없어 공개 B/L 입력 단가 또는 기존 값만 사용",
            source_tier="official",
        ))
    payload = build_trade_intel_payload(products, public_flows, official)
    payload["generated"] = datetime.now().isoformat(timespec="seconds")
    payload["quality"] = build_quality_summary(
        payload,
        connectors,
        generated_at=payload["generated"],
        stale_after_hours=stale_after_hours,
    )
    if product_ids:
        existing = load_trade_intel()
        merged = existing.get("products", {}).copy()
        merged.update(payload["products"])
        payload["products"] = merged
        if existing.get("sources") and not payload.get("sources"):
            payload["sources"] = existing["sources"]
        payload["quality"] = build_quality_summary(
            payload,
            connectors,
            generated_at=payload["generated"],
            stale_after_hours=stale_after_hours,
        )
    _emit(data, payload)
    result = {
        "updated": payload["updated"],
        "products": sorted(payload["products"]),
        "status": payload["quality"]["status"],
        "quality": payload["quality"],
        "connectors": [c.__dict__ for c in connectors],
        "generated": payload["generated"],
    }
    if report_out:
        _write_report(report_out, result)
    return result


def _emit(data: dict, trade_intel: dict) -> None:
    header = (
        "/* Tradar 데이터 — 관세청 품목별 국가별 수출입실적 + 거래 인텔리전스 자동수집.\n"
        f"   생성: {datetime.now().isoformat(timespec='seconds')} · "
        "scripts/sync_trade_intel.py 로 재생성. */\n"
    )
    body = (
        "window.TRADAR_DATA = "
        + json.dumps(data, ensure_ascii=False, indent=1)
        + ";\n\nwindow.TRADAR_TRADE_INTEL = "
        + json.dumps(trade_intel, ensure_ascii=False, indent=1)
        + ";\n"
    )
    Path(TRADAR_JS).write_text(header + body, encoding="utf-8")


def _sync_window() -> tuple[str, str]:
    now = datetime.now()
    return f"{now.year - 2:04d}{now.month:02d}", f"{now.year:04d}{now.month:02d}"


def _official_products(products: list[dict], public_flows: list, product_ids: list[str] | None = None) -> list[dict]:
    """공식 HS 보강 대상 품목을 실제 거래 흐름이 있는 범위로 제한한다.

    전체 카탈로그를 기본 국가 20개로 조회하면 외부 API 지연 하나에 동기화가 오래 묶인다.
    명시적 --product가 있으면 사용자의 선택을 존중하고, 없으면 수집된 flow가 있는 품목만 조회한다.
    """
    if product_ids:
        return products
    flow_products = {
        getattr(flow, "product_id", "")
        for flow in public_flows
        if getattr(flow, "product_id", "")
    }
    if not flow_products:
        return products
    return [p for p in products if p.get("id") in flow_products]


def _markets_for_product(
    public_flows: list,
    product_id: str,
    *,
    limit: int = 3,
    fallback_to_default: bool = False,
) -> list[str]:
    totals: dict[str, float] = {}
    for flow in public_flows:
        if getattr(flow, "product_id", "") and getattr(flow, "product_id", "") != product_id:
            continue
        market = getattr(flow, "market", "")
        if not market:
            continue
        totals[market] = totals.get(market, 0.0) + float(getattr(flow, "volume_kg", 0.0) or 0.0)
    markets = [
        market
        for market, _volume in sorted(totals.items(), key=lambda item: item[1], reverse=True)
    ]
    if not markets and fallback_to_default:
        markets = DEFAULT_COUNTRY_CODES
    if limit > 0:
        markets = markets[:limit]
    return markets


def _write_report(path: str, result: dict) -> None:
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync Tradar trade intelligence from official stats + public B/L CSV")
    parser.add_argument("--public-bl-csv", default=os.environ.get("TRADE_INTEL_PUBLIC_BL_CSV", ""),
                        help="공개 B/L/업로드 CSV 경로. env TRADE_INTEL_PUBLIC_BL_CSV도 지원")
    parser.add_argument("--public-bl-api-url", default=os.environ.get("TRADE_INTEL_PUBLIC_BL_API_URL", ""),
                        help="records/results/data 배열을 반환하는 공개 B/L JSON API URL")
    parser.add_argument("--importyeti-company", action="append", default=[],
                        help="ImportYeti company slug. 예: wal-mart. 여러 번 지정 가능")
    parser.add_argument("--product", action="append", dest="products", help="동기화할 product id. 여러 번 지정 가능")
    parser.add_argument("--report-out", default=os.environ.get("TRADE_INTEL_REPORT_OUT", RUN_REPORT_JSON),
                        help="수집 실행 리포트 JSON 경로")
    parser.add_argument("--strict", action="store_true", help="커넥터 하나라도 실패하면 즉시 실패")
    parser.add_argument("--stale-after-hours", type=int, default=int(os.environ.get("TRADE_INTEL_STALE_AFTER_HOURS", "48")),
                        help="UI/감사에서 stale로 볼 시간")
    parser.add_argument("--customs-timeout", type=int, default=int(os.environ.get("TRADE_INTEL_CUSTOMS_TIMEOUT", "8")),
                        help="관세청 API 단일 요청 타임아웃(초)")
    parser.add_argument("--customs-market-limit", type=int,
                        default=int(os.environ.get("TRADE_INTEL_CUSTOMS_MARKET_LIMIT", "3")),
                        help="품목별 공식 HS 통계를 조회할 상위 시장 수. 0이면 제한 없음")
    args = parser.parse_args()
    if not (args.public_bl_csv or args.public_bl_api_url or args.importyeti_company):
        raise SystemExit("공개 B/L 입력이 필요합니다: --public-bl-csv, --public-bl-api-url, --importyeti-company 중 하나")
    result = sync_trade_intelligence(
        public_bl_csv=args.public_bl_csv,
        public_bl_api_url=args.public_bl_api_url,
        importyeti_companies=args.importyeti_company,
        product_ids=args.products,
        customs_timeout=args.customs_timeout,
        customs_market_limit=args.customs_market_limit,
        report_out=args.report_out,
        strict=args.strict,
        stale_after_hours=args.stale_after_hours,
    )
    print(
        f"✓ 거래 인텔리전스 {result['updated']}개 품목 갱신 · "
        f"status={result['status']} · report={os.path.relpath(args.report_out)} → {os.path.relpath(TRADAR_JS)}"
    )


if __name__ == "__main__":
    main()
