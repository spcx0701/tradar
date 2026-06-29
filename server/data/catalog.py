"""한류 수출 품목·시장 카탈로그.

무역풍(Tradewind) 데모 스냅샷의 기준이 되는 품목/국가 정의.

- ``anchor_2024_musd`` : 2024년 한국 수출 실적(백만 USD) 근사치. 관세청 수출입무역통계·
  보도자료에 공표된 값에 앵커링한 대표치(데모용). 실 서비스는 관세청
  ``품목별 국가별 수출입실적`` 오픈API로 실시간 동기화한다(see customs_client.py).
- ``markets`` : 주요 수출 대상국과 (점유율, 모멘텀) — 모멘텀은 최근 추세 태그로
  스냅샷 생성 시 성장률·계절성에 반영된다.

HS코드는 대표 세번(품목분류) 기준. 모든 수치 단위는 미화(USD).
"""

# 국가 코드 → 한글명 (관세청 통계 표기 기준)
COUNTRIES = {
    "US": "미국", "JP": "일본", "CN": "중국", "VN": "베트남", "TH": "태국",
    "ID": "인도네시아", "MY": "말레이시아", "PH": "필리핀", "TW": "대만",
    "HK": "홍콩", "SG": "싱가포르", "AU": "호주", "AE": "아랍에미리트",
    "SA": "사우디아라비아", "FR": "프랑스", "DE": "독일", "GB": "영국",
    "NL": "네덜란드", "CA": "캐나다", "MX": "멕시코", "IN": "인도",
    "MN": "몽골", "RU": "러시아", "BR": "브라질",
}

# 모멘텀 태그 → (연 성장률 중앙값, 변동성)
MOMENTUM = {
    "surge": (0.42, 0.18),     # 급등
    "rising": (0.18, 0.10),    # 상승
    "stable": (0.04, 0.06),    # 안정
    "cooling": (-0.10, 0.12),  # 둔화
    "volatile": (0.12, 0.30),  # 변동성 높음
}

# 계절성 프로파일(12개월, 평균 1.0 정규화). 식품 명절·계절 수요 반영.
SEASON = {
    "lunar_newyear": [1.25, 1.15, 0.95, 0.9, 0.9, 0.9, 0.95, 0.95, 1.0, 1.05, 1.1, 1.15],
    "summer": [0.85, 0.85, 0.95, 1.05, 1.15, 1.25, 1.25, 1.15, 1.0, 0.9, 0.85, 0.85],
    "yearend": [0.9, 0.9, 0.95, 0.95, 1.0, 1.0, 1.05, 1.05, 1.1, 1.15, 1.2, 1.2],
    "flat": [1.0] * 12,
    "harvest": [0.8, 0.8, 0.85, 0.95, 1.1, 1.2, 1.2, 1.15, 1.15, 1.05, 0.9, 0.85],
}

# 품목 카탈로그
PRODUCTS = [
    {
        "hs": "1902.30", "name_ko": "라면(즉석면)", "category": "K-Food",
        "anchor_2024_musd": 1240, "season": "yearend",
        "markets": {
            "CN": (0.22, "rising"), "US": (0.17, "surge"), "JP": (0.09, "stable"),
            "NL": (0.07, "rising"), "MY": (0.05, "rising"), "PH": (0.05, "stable"),
            "TH": (0.04, "rising"), "ID": (0.04, "surge"), "AU": (0.04, "rising"),
            "GB": (0.03, "surge"), "VN": (0.03, "stable"), "DE": (0.03, "rising"),
            "MX": (0.03, "surge"), "CA": (0.03, "rising"), "FR": (0.02, "rising"),
            "AE": (0.02, "rising"), "IN": (0.02, "surge"), "RU": (0.02, "volatile"),
        },
    },
    {
        "hs": "1212.21", "name_ko": "김(조미김·마른김)", "category": "K-Food",
        "anchor_2024_musd": 1000, "season": "lunar_newyear",
        "markets": {
            "US": (0.18, "surge"), "JP": (0.16, "stable"), "CN": (0.14, "rising"),
            "TH": (0.09, "surge"), "RU": (0.05, "volatile"), "TW": (0.05, "rising"),
            "CA": (0.04, "rising"), "GB": (0.04, "surge"), "DE": (0.03, "rising"),
            "AU": (0.03, "rising"), "NL": (0.03, "rising"), "VN": (0.03, "stable"),
            "FR": (0.03, "rising"), "SG": (0.02, "stable"), "ID": (0.02, "rising"),
            "MY": (0.02, "rising"),
        },
    },
    {
        "hs": "3304.99", "name_ko": "화장품(기초·색조)", "category": "K-Beauty",
        "anchor_2024_musd": 10200, "season": "flat",
        "markets": {
            "CN": (0.27, "cooling"), "US": (0.18, "surge"), "JP": (0.12, "rising"),
            "HK": (0.06, "stable"), "VN": (0.05, "rising"), "RU": (0.03, "volatile"),
            "TW": (0.03, "stable"), "SG": (0.03, "rising"), "TH": (0.03, "rising"),
            "MY": (0.02, "rising"), "ID": (0.02, "surge"), "AE": (0.02, "rising"),
            "GB": (0.02, "surge"), "NL": (0.02, "rising"), "CA": (0.02, "rising"),
            "AU": (0.02, "rising"), "FR": (0.02, "rising"), "IN": (0.02, "surge"),
        },
    },
    {
        "hs": "2005.99", "name_ko": "김치", "category": "K-Food",
        "anchor_2024_musd": 163, "season": "lunar_newyear",
        "markets": {
            "JP": (0.40, "stable"), "US": (0.24, "surge"), "NL": (0.06, "rising"),
            "HK": (0.05, "stable"), "GB": (0.04, "rising"), "AU": (0.04, "rising"),
            "TW": (0.03, "stable"), "CA": (0.03, "rising"), "DE": (0.02, "rising"),
            "SG": (0.02, "stable"), "FR": (0.02, "rising"), "TH": (0.02, "rising"),
        },
    },
    {
        "hs": "2103.90", "name_ko": "장류·소스(고추장 등)", "category": "K-Food",
        "anchor_2024_musd": 400, "season": "summer",
        "markets": {
            "US": (0.20, "surge"), "CN": (0.16, "stable"), "JP": (0.12, "stable"),
            "RU": (0.06, "volatile"), "PH": (0.05, "rising"), "VN": (0.05, "rising"),
            "NL": (0.05, "rising"), "MY": (0.04, "rising"), "AU": (0.04, "rising"),
            "TH": (0.03, "rising"), "GB": (0.03, "surge"), "CA": (0.03, "rising"),
            "TW": (0.03, "stable"), "DE": (0.03, "rising"),
        },
    },
    {
        "hs": "1905.31", "name_ko": "과자·제과", "category": "K-Food",
        "anchor_2024_musd": 700, "season": "yearend",
        "markets": {
            "US": (0.19, "surge"), "CN": (0.17, "stable"), "VN": (0.10, "rising"),
            "JP": (0.07, "stable"), "TH": (0.05, "rising"), "MY": (0.05, "rising"),
            "PH": (0.04, "rising"), "ID": (0.04, "surge"), "TW": (0.04, "stable"),
            "AU": (0.03, "rising"), "GB": (0.03, "rising"), "CA": (0.03, "rising"),
            "AE": (0.03, "rising"), "NL": (0.03, "rising"),
        },
    },
    {
        "hs": "2202.99", "name_ko": "음료(과채·기능성)", "category": "K-Food",
        "anchor_2024_musd": 600, "season": "summer",
        "markets": {
            "CN": (0.18, "stable"), "US": (0.16, "rising"), "VN": (0.10, "rising"),
            "PH": (0.07, "rising"), "JP": (0.06, "stable"),
            "TH": (0.05, "rising"), "MY": (0.05, "rising"), "ID": (0.05, "surge"),
            "MN": (0.04, "rising"), "TW": (0.04, "stable"), "AU": (0.03, "rising"),
            "GB": (0.03, "rising"), "AE": (0.03, "rising"),
        },
    },
    {
        "hs": "2208.90", "name_ko": "소주·증류주", "category": "K-Culture",
        "anchor_2024_musd": 200, "season": "yearend",
        "markets": {
            "JP": (0.22, "stable"), "US": (0.20, "surge"), "CN": (0.12, "stable"),
            "VN": (0.08, "rising"), "PH": (0.06, "rising"), "GB": (0.05, "surge"),
            "TW": (0.04, "stable"), "AU": (0.04, "rising"), "TH": (0.04, "rising"),
            "DE": (0.03, "rising"), "NL": (0.03, "rising"), "SG": (0.03, "stable"),
        },
    },
    {
        "hs": "0810.10", "name_ko": "신선딸기", "category": "K-Fruit",
        "anchor_2024_musd": 75, "season": "harvest",
        "markets": {
            "HK": (0.26, "stable"), "SG": (0.18, "rising"), "VN": (0.14, "surge"),
            "TH": (0.12, "rising"), "TW": (0.08, "stable"), "MY": (0.07, "rising"),
            "ID": (0.05, "surge"), "PH": (0.04, "rising"), "AE": (0.03, "rising"),
        },
    },
    {
        "hs": "0806.10", "name_ko": "포도(샤인머스캣)", "category": "K-Fruit",
        "anchor_2024_musd": 45, "season": "harvest",
        "markets": {
            "VN": (0.24, "surge"), "CN": (0.18, "rising"), "HK": (0.14, "stable"),
            "TW": (0.10, "stable"), "SG": (0.08, "rising"), "TH": (0.07, "rising"),
            "ID": (0.06, "surge"), "MY": (0.05, "rising"), "PH": (0.04, "rising"),
        },
    },
    {
        "hs": "1211.20", "name_ko": "인삼류", "category": "K-Food",
        "anchor_2024_musd": 280, "season": "yearend",
        "markets": {
            "CN": (0.22, "stable"), "JP": (0.16, "stable"), "HK": (0.12, "stable"),
            "TW": (0.10, "rising"), "US": (0.09, "rising"), "VN": (0.08, "surge"),
            "SG": (0.05, "rising"), "TH": (0.04, "rising"), "MY": (0.04, "rising"),
        },
    },
    {
        "hs": "1901.90", "name_ko": "쌀가공식품(즉석밥·떡)", "category": "K-Food",
        "anchor_2024_musd": 300, "season": "lunar_newyear",
        "markets": {
            "US": (0.30, "surge"), "JP": (0.10, "stable"), "AU": (0.07, "rising"),
            "VN": (0.06, "rising"), "CA": (0.06, "rising"), "GB": (0.05, "surge"),
            "NL": (0.05, "rising"), "DE": (0.04, "rising"), "HK": (0.04, "stable"),
            "TW": (0.04, "stable"), "SG": (0.03, "rising"), "MY": (0.03, "rising"),
        },
    },
]

# 데이터 기간(월). 최근 5년치 월별 시계열을 생성/동기화한다.
START_YEAR = 2021
START_MONTH = 1
N_MONTHS = 60  # 2021-01 ~ 2025-12
