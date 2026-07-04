/* Tradar 데이터 — 관세청 품목별 국가별 수출입실적(HS코드 기준) 연동.
   생성: 2026-07-01T15:46:53 · scripts/build_tradar_data.py 로 재생성. */
window.TRADAR_DATA = {
 "P": [
  {
   "id": "ramen",
   "ko": "라면",
   "en": "Instant Noodles",
   "hs": "1902.30",
   "cat": "food",
   "stage": "breakout",
   "score": 94,
   "ann": 1540,
   "yoy": 23.4,
   "ytd": 18.2,
   "risk": "med",
   "mom": 7.9,
   "rchg": 2,
   "mk": [
    [
     "US",
     22,
     28
    ],
    [
     "CN",
     18,
     9
    ],
    [
     "NL",
     9,
     33
    ],
    [
     "JP",
     8,
     12
    ]
   ],
   "tags": [
    "한류",
    "급상승",
    "관세리스크"
   ],
   "nv": "high",
   "sent": "pos",
   "seed": 9210
  },
  {
   "id": "skincare",
   "ko": "기초화장품",
   "en": "Skincare",
   "hs": "3304.99",
   "cat": "beauty",
   "stage": "flagship",
   "score": 96,
   "ann": 8530,
   "yoy": 12.1,
   "ytd": 13.5,
   "risk": "low",
   "mom": 4.2,
   "rchg": 1,
   "mk": [
    [
     "US",
     19,
     18
    ],
    [
     "CN",
     18,
     -19
    ],
    [
     "JP",
     10,
     5
    ],
    [
     "HK",
     6,
     27
    ]
   ],
   "tags": [
    "K뷰티",
    "시장다변화"
   ],
   "nv": "high",
   "sent": "pos",
   "seed": 4821
  },
  {
   "id": "colorcos",
   "ko": "색조화장품",
   "en": "Color Cosmetics",
   "hs": "3304.20",
   "cat": "beauty",
   "stage": "scaling",
   "score": 88,
   "ann": 1505,
   "yoy": 19.2,
   "ytd": 16,
   "risk": "low",
   "mom": 5.1,
   "rchg": 1,
   "mk": [
    [
     "US",
     21,
     19
    ],
    [
     "JP",
     16,
     17
    ],
    [
     "VN",
     8,
     22
    ]
   ],
   "tags": [
    "K뷰티",
    "신흥시장"
   ],
   "nv": "med",
   "sent": "pos",
   "seed": 3344
  },
  {
   "id": "laver",
   "ko": "김(조미김)",
   "en": "Laver / Seaweed",
   "hs": "1212.21",
   "cat": "food",
   "stage": "breakout",
   "score": 90,
   "ann": 1000,
   "yoy": 14,
   "ytd": 12.2,
   "risk": "low",
   "mom": 6,
   "rchg": 3,
   "mk": [
    [
     "US",
     18,
     16
    ],
    [
     "JP",
     17,
     8
    ],
    [
     "CN",
     12,
     10
    ],
    [
     "TH",
     7,
     21
    ]
   ],
   "tags": [
    "수산",
    "프리미엄"
   ],
   "nv": "med",
   "sent": "pos",
   "seed": 7782
  },
  {
   "id": "memory",
   "ko": "메모리반도체",
   "en": "Memory Chips",
   "hs": "8542.32",
   "cat": "semi",
   "stage": "flagship",
   "score": 92,
   "ann": 138000,
   "yoy": 9,
   "ytd": 5.4,
   "risk": "med",
   "mom": 1.8,
   "rchg": 0,
   "mk": [
    [
     "CN",
     33,
     4
    ],
    [
     "HK",
     20,
     3
    ],
    [
     "TW",
     12,
     18
    ],
    [
     "VN",
     9,
     7
    ]
   ],
   "tags": [
    "주력",
    "사이클"
   ],
   "nv": "low",
   "sent": "neu",
   "seed": 1201
  },
  {
   "id": "battery",
   "ko": "2차전지",
   "en": "Li-ion Batteries",
   "hs": "8507.60",
   "cat": "battery",
   "stage": "scaling",
   "score": 64,
   "ann": 12000,
   "yoy": -8,
   "ytd": -4.2,
   "risk": "high",
   "mom": -3.1,
   "rchg": -6,
   "mk": [
    [
     "US",
     38,
     -6
    ],
    [
     "DE",
     12,
     -9
    ],
    [
     "HU",
     9,
     -3
    ]
   ],
   "tags": [
    "캐즘",
    "정책리스크"
   ],
   "nv": "med",
   "sent": "neg",
   "seed": 5562
  },
  {
   "id": "ev",
   "ko": "전기차",
   "en": "Electric Vehicles",
   "hs": "8703.80",
   "cat": "auto",
   "stage": "scaling",
   "score": 70,
   "ann": 9800,
   "yoy": 3,
   "ytd": -2.1,
   "risk": "med",
   "mom": -1.2,
   "rchg": -2,
   "mk": [
    [
     "US",
     34,
     -4
    ],
    [
     "DE",
     11,
     2
    ],
    [
     "GB",
     8,
     5
    ]
   ],
   "tags": [
    "친환경",
    "정책"
   ],
   "nv": "med",
   "sent": "neu",
   "seed": 6101
  },
  {
   "id": "autoparts",
   "ko": "자동차부품",
   "en": "Auto Parts",
   "hs": "8708.99",
   "cat": "auto",
   "stage": "flagship",
   "score": 84,
   "ann": 28000,
   "yoy": 6.4,
   "ytd": 4.1,
   "risk": "low",
   "mom": 1.5,
   "rchg": 1,
   "mk": [
    [
     "US",
     33,
     7
    ],
    [
     "MX",
     10,
     9
    ],
    [
     "CN",
     8,
     2
    ]
   ],
   "tags": [
    "주력"
   ],
   "nv": "low",
   "sent": "neu",
   "seed": 2290
  },
  {
   "id": "ships",
   "ko": "선박",
   "en": "Ships",
   "hs": "8901.20",
   "cat": "ship",
   "stage": "flagship",
   "score": 86,
   "ann": 24000,
   "yoy": 18,
   "ytd": 22.4,
   "risk": "low",
   "mom": 3.8,
   "rchg": 4,
   "mk": [
    [
     "LR",
     20,
     30
    ],
    [
     "PA",
     14,
     12
    ],
    [
     "SG",
     9,
     18
    ]
   ],
   "tags": [
    "친환경선박",
    "수주호황"
   ],
   "nv": "med",
   "sent": "pos",
   "seed": 8841
  },
  {
   "id": "dumpling",
   "ko": "만두",
   "en": "Dumplings",
   "hs": "1902.20",
   "cat": "food",
   "stage": "scaling",
   "score": 82,
   "ann": 320,
   "yoy": 16,
   "ytd": 14.2,
   "risk": "low",
   "mom": 5.5,
   "rchg": 2,
   "mk": [
    [
     "US",
     40,
     18
    ],
    [
     "JP",
     12,
     9
    ],
    [
     "AU",
     7,
     14
    ]
   ],
   "tags": [
    "한류"
   ],
   "nv": "med",
   "sent": "pos",
   "seed": 3912
  },
  {
   "id": "kimchi",
   "ko": "김치",
   "en": "Kimchi",
   "hs": "2005.99",
   "cat": "food",
   "stage": "scaling",
   "score": 80,
   "ann": 165,
   "yoy": 9.4,
   "ytd": 11,
   "risk": "low",
   "mom": 4.6,
   "rchg": 1,
   "mk": [
    [
     "JP",
     38,
     7
    ],
    [
     "US",
     22,
     15
    ],
    [
     "NL",
     6,
     20
    ]
   ],
   "tags": [
    "전통",
    "프리미엄"
   ],
   "nv": "med",
   "sent": "pos",
   "seed": 4410
  },
  {
   "id": "coffeemix",
   "ko": "커피조제품",
   "en": "Coffee Mix",
   "hs": "2101.12",
   "cat": "food",
   "stage": "scaling",
   "score": 81,
   "ann": 280,
   "yoy": 15.8,
   "ytd": 13,
   "risk": "low",
   "mom": 4.9,
   "rchg": 2,
   "mk": [
    [
     "CN",
     17,
     8
    ],
    [
     "RU",
     14,
     3
    ],
    [
     "US",
     12,
     22
    ]
   ],
   "tags": [
    "한류"
   ],
   "nv": "med",
   "sent": "pos",
   "seed": 5120
  },
  {
   "id": "snacks",
   "ko": "과자류",
   "en": "Snacks",
   "hs": "1905.31",
   "cat": "food",
   "stage": "scaling",
   "score": 79,
   "ann": 720,
   "yoy": 12,
   "ytd": 10.4,
   "risk": "low",
   "mom": 3.6,
   "rchg": 0,
   "mk": [
    [
     "US",
     21,
     15
    ],
    [
     "CN",
     16,
     4
    ],
    [
     "VN",
     10,
     18
    ]
   ],
   "tags": [
    "한류"
   ],
   "nv": "med",
   "sent": "pos",
   "seed": 6633
  },
  {
   "id": "sauce",
   "ko": "소스·고추장",
   "en": "Sauces",
   "hs": "2103.90",
   "cat": "food",
   "stage": "scaling",
   "score": 83,
   "ann": 420,
   "yoy": 14,
   "ytd": 15.2,
   "risk": "low",
   "mom": 5.8,
   "rchg": 2,
   "mk": [
    [
     "US",
     28,
     19
    ],
    [
     "JP",
     14,
     8
    ],
    [
     "VN",
     9,
     25
    ]
   ],
   "tags": [
    "한류",
    "급상승"
   ],
   "nv": "med",
   "sent": "pos",
   "seed": 7150
  },
  {
   "id": "rice",
   "ko": "즉석밥",
   "en": "Instant Rice",
   "hs": "1904.90",
   "cat": "food",
   "stage": "scaling",
   "score": 84,
   "ann": 180,
   "yoy": 20,
   "ytd": 18,
   "risk": "low",
   "mom": 6.4,
   "rchg": 3,
   "mk": [
    [
     "US",
     35,
     22
    ],
    [
     "HK",
     9,
     12
    ],
    [
     "AU",
     8,
     16
    ]
   ],
   "tags": [
    "한류",
    "급상승"
   ],
   "nv": "med",
   "sent": "pos",
   "seed": 8120
  },
  {
   "id": "tteok",
   "ko": "떡볶이",
   "en": "Tteokbokki",
   "hs": "1902.19",
   "cat": "food",
   "stage": "breakout",
   "score": 85,
   "ann": 95,
   "yoy": 25,
   "ytd": 22,
   "risk": "med",
   "mom": 8.5,
   "rchg": 5,
   "mk": [
    [
     "US",
     33,
     28
    ],
    [
     "JP",
     15,
     18
    ],
    [
     "TW",
     9,
     24
    ]
   ],
   "tags": [
    "한류",
    "급상승"
   ],
   "nv": "high",
   "sent": "pos",
   "seed": 9901
  },
  {
   "id": "ginseng",
   "ko": "인삼류",
   "en": "Ginseng",
   "hs": "1211.20",
   "cat": "bio",
   "stage": "emerging",
   "score": 72,
   "ann": 250,
   "yoy": 5,
   "ytd": 6.1,
   "risk": "low",
   "mom": 1.9,
   "rchg": 0,
   "mk": [
    [
     "CN",
     30,
     2
    ],
    [
     "HK",
     16,
     4
    ],
    [
     "JP",
     11,
     7
    ]
   ],
   "tags": [
    "건강기능"
   ],
   "nv": "low",
   "sent": "neu",
   "seed": 2740
  },
  {
   "id": "soju",
   "ko": "소주",
   "en": "Soju",
   "hs": "2208.90",
   "cat": "food",
   "stage": "scaling",
   "score": 78,
   "ann": 140,
   "yoy": 11,
   "ytd": 13.4,
   "risk": "low",
   "mom": 4.4,
   "rchg": 2,
   "mk": [
    [
     "JP",
     26,
     6
    ],
    [
     "US",
     16,
     18
    ],
    [
     "CN",
     12,
     5
    ]
   ],
   "tags": [
    "한류"
   ],
   "nv": "med",
   "sent": "pos",
   "seed": 3360
  },
  {
   "id": "album",
   "ko": "음반·K-pop",
   "en": "K-pop Albums",
   "hs": "8523.49",
   "cat": "culture",
   "stage": "breakout",
   "score": 86,
   "ann": 320,
   "yoy": 18,
   "ytd": 16.3,
   "risk": "low",
   "mom": 6.8,
   "rchg": 3,
   "mk": [
    [
     "US",
     24,
     22
    ],
    [
     "JP",
     22,
     9
    ],
    [
     "CN",
     9,
     4
    ]
   ],
   "tags": [
    "한류",
    "케데헌"
   ],
   "nv": "high",
   "sent": "pos",
   "seed": 1450
  },
  {
   "id": "toy",
   "ko": "완구·피규어",
   "en": "Toys & Figures",
   "hs": "9503.00",
   "cat": "culture",
   "stage": "scaling",
   "score": 83,
   "ann": 410,
   "yoy": 14,
   "ytd": 17.1,
   "risk": "low",
   "mom": 5.9,
   "rchg": 3,
   "mk": [
    [
     "US",
     30,
     20
    ],
    [
     "JP",
     14,
     12
    ],
    [
     "GB",
     7,
     16
    ]
   ],
   "tags": [
    "한류"
   ],
   "nv": "med",
   "sent": "pos",
   "seed": 1990
  },
  {
   "id": "bio",
   "ko": "바이오·의약",
   "en": "Bio & Pharma",
   "hs": "3002.15",
   "cat": "bio",
   "stage": "breakout",
   "score": 87,
   "ann": 9500,
   "yoy": 16,
   "ytd": 14,
   "risk": "med",
   "mom": 3.3,
   "rchg": 2,
   "mk": [
    [
     "US",
     26,
     18
    ],
    [
     "DE",
     12,
     9
    ],
    [
     "NL",
     9,
     14
    ]
   ],
   "tags": [
    "바이오시밀러"
   ],
   "nv": "med",
   "sent": "pos",
   "seed": 5210
  },
  {
   "id": "oled",
   "ko": "디스플레이",
   "en": "OLED Display",
   "hs": "8524.91",
   "cat": "display",
   "stage": "flagship",
   "score": 80,
   "ann": 30000,
   "yoy": 7,
   "ytd": 5,
   "risk": "med",
   "mom": 1.2,
   "rchg": 0,
   "mk": [
    [
     "CN",
     28,
     3
    ],
    [
     "VN",
     18,
     9
    ],
    [
     "US",
     10,
     6
    ]
   ],
   "tags": [
    "주력"
   ],
   "nv": "low",
   "sent": "neu",
   "seed": 3070
  },
  {
   "id": "robot",
   "ko": "로봇",
   "en": "Robotics",
   "hs": "8479.50",
   "cat": "machine",
   "stage": "breakout",
   "score": 85,
   "ann": 1800,
   "yoy": 22,
   "ytd": 19.4,
   "risk": "low",
   "mom": 4.7,
   "rchg": 4,
   "mk": [
    [
     "US",
     24,
     26
    ],
    [
     "CN",
     15,
     12
    ],
    [
     "DE",
     11,
     18
    ]
   ],
   "tags": [
    "신산업"
   ],
   "nv": "med",
   "sent": "pos",
   "seed": 6720
  },
  {
   "id": "eyewear",
   "ko": "안경·선글라스",
   "en": "Eyewear",
   "hs": "9004.10",
   "cat": "fashion",
   "stage": "emerging",
   "score": 77,
   "ann": 600,
   "yoy": 13,
   "ytd": 12,
   "risk": "low",
   "mom": 3.1,
   "rchg": 1,
   "mk": [
    [
     "US",
     22,
     14
    ],
    [
     "JP",
     17,
     9
    ],
    [
     "HK",
     8,
     11
    ]
   ],
   "tags": [
    "라이프"
   ],
   "nv": "low",
   "sent": "neu",
   "seed": 4150
  },
  {
   "id": "fruit",
   "ko": "신선과일",
   "en": "Fresh Fruit",
   "hs": "0810.10",
   "cat": "food",
   "stage": "emerging",
   "score": 81,
   "ann": 380,
   "yoy": 17,
   "ytd": 15,
   "risk": "med",
   "mom": 4,
   "rchg": 2,
   "mk": [
    [
     "VN",
     21,
     24
    ],
    [
     "HK",
     16,
     12
    ],
    [
     "SG",
     11,
     18
    ]
   ],
   "tags": [
    "프리미엄",
    "신흥"
   ],
   "nv": "med",
   "sent": "pos",
   "seed": 2510
  },
  {
   "id": "petfood",
   "ko": "펫푸드",
   "en": "Pet Food",
   "hs": "2309.10",
   "cat": "food",
   "stage": "emerging",
   "score": 82,
   "ann": 210,
   "yoy": 19,
   "ytd": 18,
   "risk": "low",
   "mom": 5.2,
   "rchg": 3,
   "mk": [
    [
     "JP",
     28,
     16
    ],
    [
     "US",
     15,
     22
    ],
    [
     "TH",
     9,
     20
    ]
   ],
   "tags": [
    "신산업"
   ],
   "nv": "med",
   "sent": "pos",
   "seed": 8330
  },
  {
   "id": "solar",
   "ko": "태양광모듈",
   "en": "Solar Modules",
   "hs": "8541.43",
   "cat": "green",
   "stage": "scaling",
   "score": 66,
   "ann": 2200,
   "yoy": -5,
   "ytd": 2,
   "risk": "med",
   "mom": -1.5,
   "rchg": -3,
   "mk": [
    [
     "US",
     52,
     -8
    ],
    [
     "JP",
     9,
     4
    ]
   ],
   "tags": [
    "정책",
    "IRA"
   ],
   "nv": "med",
   "sent": "neu",
   "seed": 7410
  },
  {
   "id": "apparel",
   "ko": "패션의류",
   "en": "Apparel",
   "hs": "6109.10",
   "cat": "fashion",
   "stage": "scaling",
   "score": 74,
   "ann": 2600,
   "yoy": 8,
   "ytd": 7,
   "risk": "low",
   "mom": 2.4,
   "rchg": 0,
   "mk": [
    [
     "US",
     24,
     9
    ],
    [
     "JP",
     16,
     6
    ],
    [
     "CN",
     12,
     3
    ]
   ],
   "tags": [
    "라이프"
   ],
   "nv": "low",
   "sent": "neu",
   "seed": 5840
  }
 ],
 "markets": [
  {
   "code": "US",
   "ko": "미국",
   "region": "북미",
   "exp": 130,
   "yoy": 5,
   "top": [
    "semi",
    "auto",
    "beauty"
   ],
   "risk": "med",
   "score": 88,
   "seed": 1101
  },
  {
   "code": "CN",
   "ko": "중국",
   "region": "아시아",
   "exp": 133,
   "yoy": -2,
   "top": [
    "semi",
    "display",
    "beauty"
   ],
   "risk": "med",
   "score": 74,
   "seed": 1102
  },
  {
   "code": "VN",
   "ko": "베트남",
   "region": "아시아",
   "exp": 62,
   "yoy": 8,
   "top": [
    "semi",
    "display",
    "food"
   ],
   "risk": "low",
   "score": 82,
   "seed": 1103
  },
  {
   "code": "JP",
   "ko": "일본",
   "region": "아시아",
   "exp": 30,
   "yoy": 3,
   "top": [
    "food",
    "beauty",
    "ship"
   ],
   "risk": "low",
   "score": 80,
   "seed": 1104
  },
  {
   "code": "HK",
   "ko": "홍콩",
   "region": "아시아",
   "exp": 30,
   "yoy": 6,
   "top": [
    "semi",
    "beauty"
   ],
   "risk": "med",
   "score": 79,
   "seed": 1105
  },
  {
   "code": "TW",
   "ko": "대만",
   "region": "아시아",
   "exp": 30,
   "yoy": 20,
   "top": [
    "semi"
   ],
   "risk": "med",
   "score": 86,
   "seed": 1106
  },
  {
   "code": "SG",
   "ko": "싱가포르",
   "region": "아시아",
   "exp": 18,
   "yoy": 7,
   "top": [
    "semi",
    "ship"
   ],
   "risk": "low",
   "score": 78,
   "seed": 1107
  },
  {
   "code": "IN",
   "ko": "인도",
   "region": "아시아",
   "exp": 19,
   "yoy": 12,
   "top": [
    "auto",
    "beauty",
    "semi"
   ],
   "risk": "low",
   "score": 84,
   "seed": 1108
  },
  {
   "code": "MX",
   "ko": "멕시코",
   "region": "북미",
   "exp": 18,
   "yoy": 4,
   "top": [
    "auto",
    "display"
   ],
   "risk": "med",
   "score": 73,
   "seed": 1109
  },
  {
   "code": "DE",
   "ko": "독일",
   "region": "유럽",
   "exp": 11,
   "yoy": 5,
   "top": [
    "auto",
    "bio",
    "battery"
   ],
   "risk": "med",
   "score": 76,
   "seed": 1110
  },
  {
   "code": "NL",
   "ko": "네덜란드",
   "region": "유럽",
   "exp": 9,
   "yoy": 12,
   "top": [
    "bio",
    "food",
    "beauty"
   ],
   "risk": "low",
   "score": 83,
   "seed": 1111
  },
  {
   "code": "PL",
   "ko": "폴란드",
   "region": "유럽",
   "exp": 6,
   "yoy": 30,
   "top": [
    "beauty",
    "battery"
   ],
   "risk": "low",
   "score": 90,
   "seed": 1112
  },
  {
   "code": "AE",
   "ko": "UAE",
   "region": "중동",
   "exp": 6,
   "yoy": 25,
   "top": [
    "beauty",
    "auto",
    "food"
   ],
   "risk": "low",
   "score": 88,
   "seed": 1113
  },
  {
   "code": "ID",
   "ko": "인도네시아",
   "region": "아시아",
   "exp": 9,
   "yoy": 9,
   "top": [
    "semi",
    "beauty"
   ],
   "risk": "low",
   "score": 81,
   "seed": 1114
  },
  {
   "code": "TH",
   "ko": "태국",
   "region": "아시아",
   "exp": 9,
   "yoy": 11,
   "top": [
    "food",
    "beauty"
   ],
   "risk": "low",
   "score": 80,
   "seed": 1115
  },
  {
   "code": "GB",
   "ko": "영국",
   "region": "유럽",
   "exp": 8,
   "yoy": 14,
   "top": [
    "beauty",
    "bio",
    "culture"
   ],
   "risk": "low",
   "score": 82,
   "seed": 1116
  }
 ],
 "news": [
  {
   "id": "n1",
   "head": "K-라면 수출 상반기 8억 달러 돌파…‘케데헌’ 효과로 미국·EU 동반 급증",
   "src": "관세청·연합뉴스",
   "time": "2시간 전",
   "country": "US",
   "related": [
    "ramen"
   ],
   "sent": "pos",
   "sev": "opp",
   "rel": 96,
   "topic": "한류 소비재",
   "sum": "넷플릭스 ‘케데헌’ 흥행과 현지화 라인업 확대로 대미·대EU 라면 수출이 동반 급증. 상반기 누계 사상 최대.",
   "mv": "라면 대미 수출 +28%"
  },
  {
   "id": "n2",
   "head": "美, 가공식품·화장품 대상 상호관세 인상 검토…수출기업 변수",
   "src": "Reuters·관세청",
   "time": "5시간 전",
   "country": "US",
   "related": [
    "ramen",
    "skincare",
    "colorcos"
   ],
   "sent": "neg",
   "sev": "high",
   "rel": 94,
   "topic": "통상·관세",
   "sum": "미 행정부의 상호관세 인상 검토로 대미 의존도가 높은 가공식품·화장품 품목의 채산성 리스크 확대 전망.",
   "mv": "대미 노출 품목 리스크 ↑"
  },
  {
   "id": "n3",
   "head": "K-뷰티 화장품 수출 사상 첫 세계 2위…미국, 중국 제치고 1위 시장 등극",
   "src": "식약처",
   "time": "8시간 전",
   "country": "US",
   "related": [
    "skincare",
    "colorcos"
   ],
   "sent": "pos",
   "sev": "info",
   "rel": 92,
   "topic": "K-뷰티",
   "sum": "2025년 화장품 수출 114억 달러로 프랑스에 이은 세계 2위. 미국이 중국을 제치고 최대 수출시장으로.",
   "mv": "화장품 대미 +18%"
  },
  {
   "id": "n4",
   "head": "‘검은 반도체’ 김 수출 사상 최대 10억 달러…K-푸드 수산 견인",
   "src": "해양수산부",
   "time": "어제",
   "country": "JP",
   "related": [
    "laver"
   ],
   "sent": "pos",
   "sev": "opp",
   "rel": 88,
   "topic": "K-푸드 수산",
   "sum": "조미김·맨김 수요 확대로 김 단일품목 수출 첫 10억 달러. K·FISH 브랜드 수출 다변화 가속.",
   "mv": "김 수출 +14%"
  },
  {
   "id": "n5",
   "head": "원/달러 환율 1,450원 돌파…수출 채산성·결제 리스크 확대",
   "src": "한국은행",
   "time": "어제",
   "country": null,
   "related": [
    "battery",
    "ev",
    "solar"
   ],
   "sent": "neg",
   "sev": "med",
   "rel": 85,
   "topic": "환율·거시",
   "sum": "고환율 장기화로 원자재 수입 비중이 높은 품목의 마진 압박. 결제·헤지 전략 점검 필요.",
   "mv": "고환율 채산성 리스크"
  },
  {
   "id": "n6",
   "head": "中 화장품 수요 둔화 지속…대중 수출 19% 감소, 시장 다변화 가속",
   "src": "한국무역협회",
   "time": "2일 전",
   "country": "CN",
   "related": [
    "skincare"
   ],
   "sent": "neu",
   "sev": "med",
   "rel": 83,
   "topic": "K-뷰티",
   "sum": "내수 침체로 대중 화장품 수출 감소세. 미국·중동·유럽 신흥시장 전환으로 전체 성장세는 유지.",
   "mv": "화장품 대중 -19%"
  },
  {
   "id": "n7",
   "head": "폴란드·UAE 등 신흥시장 K-뷰티 수출 100%+ 폭증",
   "src": "식약처",
   "time": "3일 전",
   "country": "PL",
   "related": [
    "skincare",
    "colorcos"
   ],
   "sent": "pos",
   "sev": "opp",
   "rel": 81,
   "topic": "신흥시장",
   "sum": "폴란드 +115%, UAE +71% 등 유럽·중동 신흥시장이 중국 공백을 메우며 수출 다변화 견인.",
   "mv": "폴란드 +115%"
  },
  {
   "id": "n8",
   "head": "2차전지 수출 둔화…‘캐즘’ 속 美 IRA 정책 불확실성 부담",
   "src": "산업통상부",
   "time": "3일 전",
   "country": "US",
   "related": [
    "battery"
   ],
   "sent": "neg",
   "sev": "high",
   "rel": 80,
   "topic": "2차전지",
   "sum": "전기차 수요 둔화(캐즘)와 미 IRA 보조금 정책 변동성으로 2차전지 대미 수출 감소.",
   "mv": "2차전지 -8%"
  },
  {
   "id": "n9",
   "head": "K-콘텐츠 굿즈·완구 수출 두 자릿수 성장…‘굿즈도 한류 상품’",
   "src": "관세청",
   "time": "4일 전",
   "country": "US",
   "related": [
    "toy",
    "album"
   ],
   "sent": "pos",
   "sev": "info",
   "rel": 77,
   "topic": "한류 소비재",
   "sum": "음반·완구·피규어 등 K-콘텐츠 연계 상품 수출 호조. 미국·일본 중심 수요 확대.",
   "mv": "완구 +17%"
  },
  {
   "id": "n10",
   "head": "APEC 경주 정상회의 계기 K-푸드 글로벌 노출 확대",
   "src": "aT 한국농수산식품유통공사",
   "time": "5일 전",
   "country": null,
   "related": [
    "ramen",
    "sauce",
    "kimchi"
   ],
   "sent": "pos",
   "sev": "info",
   "rel": 74,
   "topic": "K-푸드",
   "sum": "국제행사 연계 마케팅으로 라면·소스·김치 등 K-푸드 신규시장 진입 기회 확대.",
   "mv": "K-푸드 노출 ↑"
  },
  {
   "id": "n11",
   "head": "EU CBAM 본격 적용 확대…탄소국경세 대응 시급",
   "src": "한국무역협회",
   "time": "6일 전",
   "country": "DE",
   "related": [
    "battery",
    "solar"
   ],
   "sent": "neg",
   "sev": "med",
   "rel": 71,
   "topic": "통상·규제",
   "sum": "EU 탄소국경조정제도(CBAM) 적용 품목 확대로 대EU 수출기업의 탄소데이터 대응 부담 증가.",
   "mv": "대EU 규제 리스크"
  },
  {
   "id": "n12",
   "head": "선박 수주 호황 지속…친환경 선박 중심 수출 18% 증가",
   "src": "산업통상부",
   "time": "1주 전",
   "country": "SG",
   "related": [
    "ships"
   ],
   "sent": "pos",
   "sev": "info",
   "rel": 70,
   "topic": "조선",
   "sum": "LNG·메탄올 추진 등 친환경 선박 수요로 수주잔량 확대, 수출 두 자릿수 성장.",
   "mv": "선박 +18%"
  },
  {
   "id": "n13",
   "head": "관세청, 수출입무역통계 실시간 Open API 고도화…AI 분석 지원",
   "src": "관세청 데이터담당관",
   "time": "1주 전",
   "country": null,
   "related": [],
   "sent": "pos",
   "sev": "info",
   "rel": 68,
   "topic": "공공데이터",
   "sum": "UNI-PASS·수출입무역통계 Open API 항목 확대 및 실시간성 강화로 민간 AI 분석 활용도 제고.",
   "mv": "데이터 인프라 ↑"
  },
  {
   "id": "n14",
   "head": "‘불닭’ 단일품목 의존 우려…라면 포트폴리오 다변화 과제",
   "src": "업계·KITA",
   "time": "1주 전",
   "country": null,
   "related": [
    "ramen"
   ],
   "sent": "neu",
   "sev": "med",
   "rel": 66,
   "topic": "리스크",
   "sum": "특정 브랜드·품목 의존도가 높아 수요 변동 시 변동성 확대 우려. 라인업·시장 다변화 필요.",
   "mv": "집중도 리스크"
  }
 ]
};
