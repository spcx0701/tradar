"""거래 인텔리전스 자동수집/정규화 엔진.

무료로 확보 가능한 레이어를 분리한다.

- official: 관세청/Comtrade/Census 같은 HS x 국가 공식 금액/중량 통계
- public_bl: 공개 B/L 또는 공개 B/L에서 내려받은 CSV의 회사/바이어/선적 흐름
- estimate: public_bl 물량에 official 평균단가를 결합한 단가/거래액 추정
- upload: 사용자가 올린 내부 CSV의 확정값
"""
from __future__ import annotations

import csv
import io
import json
import urllib.parse
import urllib.request
from collections import defaultdict
from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime
from typing import Iterable


@dataclass(frozen=True)
class CompanyFlow:
    product_id: str
    seller: str
    buyer: str
    product: str
    market: str
    market_name: str
    volume_kg: float
    shipments: int
    port: str = ""
    channel: str = ""
    unit_price_usd: float | None = None
    value_usd: float | None = None
    source_tier: str = "public_bl"


@dataclass(frozen=True)
class ConnectorRun:
    id: str
    label: str
    status: str
    records: int = 0
    message: str = ""
    error: str = ""
    source_tier: str = ""


def parse_company_flow_csv(text: str) -> list[CompanyFlow]:
    """공개 B/L/업로드 CSV를 내부 흐름 스키마로 정규화한다."""
    rows: list[CompanyFlow] = []
    reader = csv.DictReader(io.StringIO(text))
    for raw in reader:
        row = {str(k or "").strip(): (v or "").strip() for k, v in raw.items()}
        market = (row.get("market") or row.get("country") or row.get("country_code") or "").upper()
        market_name = row.get("marketName") or row.get("market_name") or row.get("country_name") or market
        volume_kg = _to_float(row.get("volume_kg") or row.get("weight_kg"))
        if not volume_kg:
            volume_t = _to_float(row.get("volume_t") or row.get("volume"))
            volume_kg = volume_t * 1000
        rows.append(CompanyFlow(
            product_id=row.get("product_id") or row.get("productId") or "",
            seller=row.get("seller") or row.get("shipper") or row.get("exporter") or "Unknown seller",
            buyer=row.get("buyer") or row.get("consignee") or row.get("importer") or "Unknown buyer",
            product=row.get("product") or row.get("description") or row.get("goods") or "",
            market=market,
            market_name=market_name,
            volume_kg=volume_kg,
            shipments=int(_to_float(row.get("shipments") or row.get("shipment_count") or "1") or 1),
            port=row.get("port") or row.get("route") or "",
            channel=row.get("channel") or "",
            unit_price_usd=_maybe_float(row.get("unit_price_usd") or row.get("unitPriceUsd")),
            value_usd=_maybe_float(row.get("value_usd") or row.get("valueUsd")),
            source_tier=row.get("source_tier") or row.get("sourceTier") or "public_bl",
        ))
    return rows


def parse_company_flow_records(records: Iterable[dict], *, default_product_id: str = "") -> list[CompanyFlow]:
    """JSON API 레코드 배열을 CSV와 같은 내부 흐름 스키마로 정규화한다."""
    out: list[CompanyFlow] = []
    for record in records:
        text = io.StringIO()
        keys = sorted(record.keys())
        writer = csv.DictWriter(text, fieldnames=keys)
        writer.writeheader()
        writer.writerow(record)
        parsed = parse_company_flow_csv(text.getvalue())
        for flow in parsed:
            out.append(CompanyFlow(
                product_id=flow.product_id or default_product_id,
                seller=flow.seller,
                buyer=flow.buyer,
                product=flow.product,
                market=flow.market,
                market_name=flow.market_name,
                volume_kg=flow.volume_kg,
                shipments=flow.shipments,
                port=flow.port,
                channel=flow.channel,
                unit_price_usd=flow.unit_price_usd,
                value_usd=flow.value_usd,
                source_tier=flow.source_tier,
            ))
    return out


class PublicBLJsonClient:
    """공개 B/L JSON API 어댑터.

    API가 `records`, `results`, `data` 중 하나로 배열을 반환하면 CompanyFlow로 정규화한다.
    """

    def __init__(self, url: str, api_key: str = "", timeout: int = 20):
        self.url = url
        self.api_key = api_key
        self.timeout = timeout

    def fetch(self, **params: str) -> list[CompanyFlow]:
        query = urllib.parse.urlencode({k: v for k, v in params.items() if v})
        url = self.url + (("&" if "?" in self.url else "?") + query if query else "")
        headers = {"User-Agent": "tradewind/1.0"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:  # noqa: S310
            payload = json.loads(resp.read().decode("utf-8"))
        records = payload.get("records") or payload.get("results") or payload.get("data") or []
        if isinstance(records, dict):
            records = [records]
        return parse_company_flow_records(records, default_product_id=params.get("product_id", ""))


class ImportYetiClient:
    """ImportYeti 회사 endpoint 어댑터.

    ImportYeti의 공개 예시는 `https://data.importyeti.com/v1.0/company/<company>` 형태다.
    이 어댑터는 회사 payload의 `top_suppliers` 관계를 공개 B/L 흐름으로 정규화한다.
    """

    def __init__(self, api_key: str = "", base_url: str = "https://data.importyeti.com/v1.0", timeout: int = 20):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def fetch_company(self, company_slug: str, *, product_id: str = "", product_name: str = "") -> list[CompanyFlow]:
        slug = urllib.parse.quote(company_slug.strip("/"))
        url = f"{self.base_url}/company/{slug}"
        headers = {"User-Agent": "tradewind/1.0"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:  # noqa: S310
            payload = json.loads(resp.read().decode("utf-8"))
        return self.flows_from_company_payload(
            company_slug=company_slug,
            payload=payload,
            product_id=product_id,
            product_name=product_name,
        )

    @staticmethod
    def flows_from_company_payload(*, company_slug: str, payload: dict, product_id: str = "",
                                   product_name: str = "") -> list[CompanyFlow]:
        buyer = payload.get("name") or payload.get("company_name") or company_slug
        suppliers = (
            payload.get("top_suppliers")
            or payload.get("suppliers")
            or payload.get("topSuppliers")
            or []
        )
        flows: list[CompanyFlow] = []
        for supplier in suppliers:
            seller = supplier.get("name") or supplier.get("supplier_name") or supplier.get("company") or "Unknown supplier"
            shipments = int(_to_float(supplier.get("total_shipments") or supplier.get("shipments") or "1") or 1)
            flows.append(CompanyFlow(
                product_id=product_id,
                seller=seller,
                buyer=buyer,
                product=product_name or supplier.get("product") or supplier.get("top_product") or "",
                market="US",
                market_name="미국",
                volume_kg=_to_float(supplier.get("volume_kg") or supplier.get("weight_kg")),
                shipments=shipments,
                port=supplier.get("port") or "",
                channel="ImportYeti company supplier relationship",
                source_tier="public_bl",
            ))
        return flows


def official_unit_prices(official_rows: Iterable[dict]) -> dict[str, float]:
    """공식 통계 행에서 국가별 USD/kg 평균단가를 계산한다."""
    totals: dict[str, dict[str, float]] = defaultdict(lambda: {"usd": 0.0, "kg": 0.0})
    for row in official_rows:
        code = country_code(str(row.get("country") or row.get("country_name") or ""))
        usd = _to_float(row.get("exp_usd") or row.get("trade_value") or row.get("value_usd"))
        kg = _to_float(row.get("exp_kg") or row.get("quantity_kg") or row.get("weight_kg"))
        if not code or kg <= 0:
            continue
        totals[code]["usd"] += usd
        totals[code]["kg"] += kg
    return {code: round(v["usd"] / v["kg"], 4) for code, v in totals.items() if v["kg"] > 0}


def build_trade_intel_product(
    *,
    product_id: str,
    product_name: str,
    hs: str,
    public_flows: Iterable[CompanyFlow],
    official_rows: Iterable[dict],
) -> dict:
    """한 품목의 회사/상품/시장/바이어 흐름 payload를 만든다."""
    prices = official_unit_prices(official_rows)
    flows: list[dict] = []
    for idx, flow in enumerate(public_flows, start=1):
        if flow.product_id and flow.product_id != product_id:
            continue
        unit_price = flow.unit_price_usd
        price_status = "uploaded_exact" if flow.source_tier == "upload" and unit_price else "estimated"
        if unit_price is None:
            unit_price = prices.get(flow.market)
            price_status = "estimated" if unit_price is not None else "not_available"
        value_usd = flow.value_usd
        if value_usd is None and unit_price is not None:
            value_usd = unit_price * flow.volume_kg
        evidence_bits = []
        if flow.source_tier == "public_bl":
            evidence_bits.append("공개 B/L/CSV 자동수집")
        elif flow.source_tier == "upload":
            evidence_bits.append("사용자 업로드")
        else:
            evidence_bits.append(flow.source_tier)
        if unit_price is not None and flow.unit_price_usd is None:
            evidence_bits.append(f"공식 HS {hs} {flow.market} 평균단가")
        confidence = 84 if price_status == "uploaded_exact" else 72 if unit_price is not None else 45
        flows.append({
            "id": f"{product_id}-auto-{idx}",
            "seller": flow.seller,
            "buyer": flow.buyer,
            "product": flow.product or product_name,
            "market": flow.market,
            "marketName": flow.market_name,
            "port": flow.port,
            "channel": flow.channel or "바이어 후보",
            "unitPriceUsd": round(unit_price, 4) if unit_price is not None else 0,
            "unit": "kg",
            "volume": round(flow.volume_kg / 1000, 3),
            "volumeUnit": "t",
            "valueUsd": round(value_usd or 0),
            "shipments": flow.shipments,
            "share": 0,
            "growth": 0,
            "sourceTier": flow.source_tier,
            "priceStatus": price_status,
            "confidence": confidence,
            "evidence": " + ".join(evidence_bits),
            "action": "가격/물량/바이어 후보를 검토하고 내부 견적·ERP 업로드로 확정값 보강",
        })
    _assign_share(flows)
    return {
        "productId": product_id,
        "product": product_name,
        "hs": hs,
        "coverage": [
            "어떤 기업이 어떤 상품을 팔고 있는가",
            "어디에 얼마로 팔고 있는가",
            "얼마나 팔고 어떤 바이어 후보가 있는가",
            "공식/공개 B/L/추정/업로드 값이 어떻게 구분되는가",
        ],
        "flows": flows,
    }


def build_trade_intel_payload(products: Iterable[dict], public_flows: Iterable[CompanyFlow],
                              official_rows_by_product: dict[str, list[dict]]) -> dict:
    product_payloads = {}
    public_list = list(public_flows)
    updated = 0
    for p in products:
        pid = p.get("id")
        if not pid:
            continue
        payload = build_trade_intel_product(
            product_id=pid,
            product_name=p.get("ko") or p.get("name_ko") or pid,
            hs=p.get("hs") or "",
            public_flows=public_list,
            official_rows=official_rows_by_product.get(pid, []),
        )
        if payload["flows"]:
            product_payloads[pid] = payload
            updated += 1
    return {
        "version": 1,
        "generated": "",
        "note": "자동수집 커넥터가 공식 HS 통계와 공개 B/L/CSV 흐름을 결합해 생성.",
        "sources": _sources(),
        "products": product_payloads,
        "updated": updated,
    }


def build_quality_summary(
    payload: dict,
    connector_runs: Iterable[dict | ConnectorRun],
    *,
    generated_at: str = "",
    stale_after_hours: int = 48,
) -> dict:
    """운영 화면과 CI 감사에서 함께 쓰는 거래 인텔리전스 품질 요약."""
    products = payload.get("products", {}) or {}
    flows = [
        flow
        for product in products.values()
        for flow in (product.get("flows") or [])
    ]
    connectors = [_connector_to_dict(run) for run in connector_runs]
    flow_count = len(flows)
    product_count = len(products)
    sellers = {f.get("seller") for f in flows if f.get("seller")}
    buyers = {f.get("buyer") for f in flows if f.get("buyer")}
    markets = {f.get("market") for f in flows if f.get("market")}
    avg_conf = round(sum(_to_float(f.get("confidence")) for f in flows) / flow_count) if flow_count else 0
    exact_count = sum(1 for f in flows if f.get("priceStatus") == "uploaded_exact")
    estimated_count = sum(1 for f in flows if f.get("priceStatus") == "estimated")
    missing_price_count = sum(1 for f in flows if f.get("priceStatus") == "not_available" or not f.get("unitPriceUsd"))
    failed = [c for c in connectors if c.get("status") == "failed"]
    degraded = [c for c in connectors if c.get("status") == "degraded"]
    skipped = [c for c in connectors if c.get("status") == "skipped"]
    warnings: list[str] = []
    if not flow_count:
        warnings.append("거래 흐름이 없습니다. 공개 B/L/API/업로드 입력을 확인하세요.")
    for connector in failed:
        reason = connector.get("error") or connector.get("message") or "원인 미상"
        warnings.append(f"{connector.get('label') or connector.get('id')} 커넥터 실패: {reason}")
    for connector in degraded:
        reason = connector.get("error") or connector.get("message") or "부분 실패"
        warnings.append(f"{connector.get('label') or connector.get('id')} 커넥터 부분 실패: {reason}")
    for connector in skipped:
        reason = connector.get("message") or "실행 조건 미충족"
        warnings.append(f"{connector.get('label') or connector.get('id')} 커넥터 건너뜀: {reason}")
    if flow_count and not exact_count:
        warnings.append("실거래 업로드 단가가 없어 단가는 공식 평균단가 또는 공개 입력값 기반 추정입니다.")
    if missing_price_count:
        warnings.append(f"단가가 없는 거래 흐름 {missing_price_count}건은 가격 비교에서 보수적으로 표시됩니다.")
    if avg_conf and avg_conf < 60:
        warnings.append("평균 신뢰도가 60점 미만입니다. 내부 CSV 또는 추가 공개 B/L 소스를 보강하세요.")

    score = 0
    if flow_count:
        score += 35
    if product_count:
        score += min(15, product_count * 5)
    if sellers:
        score += min(12, len(sellers) * 3)
    if buyers:
        score += min(12, len(buyers) * 3)
    if markets:
        score += min(10, len(markets) * 3)
    if avg_conf >= 70:
        score += 10
    elif avg_conf >= 60:
        score += 6
    if exact_count:
        score += 6
    score -= len(failed) * 12
    score -= len(degraded) * 6
    score -= len(skipped) * 4
    score = max(0, min(100, score))

    status = "operational"
    if not flow_count:
        status = "blocked"
    elif failed or degraded or skipped or missing_price_count:
        status = "degraded"

    return {
        "status": status,
        "coverageScore": score,
        "generatedAt": generated_at,
        "staleAfterHours": stale_after_hours,
        "productCount": product_count,
        "flowCount": flow_count,
        "sellerCount": len(sellers),
        "buyerCount": len(buyers),
        "marketCount": len(markets),
        "averageConfidence": avg_conf,
        "exactPriceShare": _pct(exact_count, flow_count),
        "estimatedPriceShare": _pct(estimated_count, flow_count),
        "missingPriceShare": _pct(missing_price_count, flow_count),
        "warnings": warnings,
        "connectors": connectors,
    }


def validate_trade_intel_payload(
    payload: dict,
    *,
    now: str | None = None,
    max_age_hours: int = 72,
    min_products: int = 1,
    min_flows: int = 1,
) -> list[str]:
    """배포/PR 전 `window.TRADAR_TRADE_INTEL`의 운영 가능성을 감사한다."""
    errors: list[str] = []
    if payload.get("version") != 1:
        errors.append("version must be 1")
    products = payload.get("products") or {}
    if len(products) < min_products:
        errors.append(f"product count below minimum: {len(products)} < {min_products}")
    flows = [
        flow
        for product in products.values()
        for flow in (product.get("flows") or [])
    ]
    if len(flows) < min_flows:
        errors.append(f"flow count below minimum: {len(flows)} < {min_flows}")
    allowed_tiers = {"official", "public_bl", "estimate", "upload"}
    allowed_prices = {"market_average", "estimated", "uploaded_exact", "not_available"}
    for flow in flows:
        if flow.get("sourceTier") not in allowed_tiers:
            errors.append(f"invalid source tier: {flow.get('sourceTier')}")
        if flow.get("priceStatus") not in allowed_prices:
            errors.append(f"invalid price status: {flow.get('priceStatus')}")
        confidence = _to_float(flow.get("confidence"))
        if confidence < 0 or confidence > 100:
            errors.append(f"confidence out of range: {confidence}")
    quality = payload.get("quality") or {}
    if quality.get("status") == "blocked":
        errors.append("quality status is blocked")
    generated = payload.get("generated") or quality.get("generatedAt")
    if generated:
        age = _age_hours(generated, now)
        if age is not None and age > max_age_hours:
            errors.append(f"trade intelligence payload is stale: {round(age, 1)}h > {max_age_hours}h")
    else:
        errors.append("generated timestamp is missing")
    return errors


def country_code(name_or_code: str) -> str:
    val = (name_or_code or "").strip()
    for ko, code in _C2CODE.items():
        if ko in val:
            return code
    if len(val) == 2 and val.isascii() and val.isalpha():
        return val.upper()
    return val[:2].upper()


def _assign_share(flows: list[dict]) -> None:
    total = sum(f.get("valueUsd", 0) for f in flows) or 1
    for flow in flows:
        flow["share"] = round(flow.get("valueUsd", 0) / total * 100)


def _sources() -> list[dict]:
    return [
        {"tier": "official", "label": "공식 HS 통계", "detail": "관세청/Comtrade/Census 금액·중량", "use": "시장 평균단가"},
        {"tier": "public_bl", "label": "공개 B/L", "detail": "공개 선하증권/CSV 회사 흐름", "use": "기업·바이어·선적 흐름"},
        {"tier": "estimate", "label": "추정", "detail": "공식 평균단가 x 공개 물량", "use": "회사별 단가/거래액 추정"},
        {"tier": "upload", "label": "업로드", "detail": "사용자 내부 CSV", "use": "확정 단가/바이어 보강"},
    ]


def _to_float(value) -> float:
    try:
        return float(str(value or "0").replace(",", ""))
    except ValueError:
        return 0.0


def _maybe_float(value) -> float | None:
    if value in (None, ""):
        return None
    return _to_float(value)


def _connector_to_dict(run: dict | ConnectorRun) -> dict:
    if is_dataclass(run):
        return asdict(run)
    return dict(run)


def _pct(count: int, total: int) -> int:
    if total <= 0:
        return 0
    return round(count / total * 100)


def _age_hours(generated: str, now: str | None) -> float | None:
    try:
        generated_at = datetime.fromisoformat(generated)
        now_at = datetime.fromisoformat(now) if now else datetime.now()
    except ValueError:
        return None
    return (now_at - generated_at).total_seconds() / 3600


_C2CODE = {
    "미국": "US", "중국": "CN", "베트남": "VN", "일본": "JP", "홍콩": "HK", "대만": "TW",
    "싱가포르": "SG", "인도": "IN", "멕시코": "MX", "독일": "DE", "네덜란드": "NL",
    "폴란드": "PL", "아랍에미리트": "AE", "인도네시아": "ID", "태국": "TH", "영국": "GB",
    "라이베리아": "LR", "파나마": "PA", "헝가리": "HU", "호주": "AU",
}
