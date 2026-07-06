/* Tradar 산업통상부 공공데이터 레이어 — K-SURE 국별신용등급·위험지수, KOTRA 해외시장뉴스·수입규제.
   생성: 2026-07-05T05:16:17 · scripts/sync_motie_data.py 로 재생성. */
window.TRADAR_MOTIE = {
 "mode": "anchor",
 "datasets": [
  {
   "org": "한국무역보험공사",
   "name": "국별신용등급",
   "portal": "https://www.data.go.kr/data/15140201/openapi.do"
  },
  {
   "org": "한국무역보험공사",
   "name": "국가별 업종별 위험지수",
   "portal": "https://www.data.go.kr/data/15132755/openapi.do"
  },
  {
   "org": "대한무역투자진흥공사",
   "name": "해외시장뉴스",
   "portal": "https://www.data.go.kr/data/15034831/openapi.do"
  },
  {
   "org": "대한무역투자진흥공사",
   "name": "수입규제품목(지역본부별) 정보",
   "portal": "https://www.data.go.kr/data/15088467/openapi.do"
  }
 ],
 "countries": {
  "US": {
   "grade": 1,
   "ri": 2,
   "regs": 53,
   "regsNote": "반덤핑·상계관세 중심(철강·화학 다수)",
   "asOf": "2026-06"
  },
  "CN": {
   "grade": 2,
   "ri": 3,
   "regs": 15,
   "regsNote": "반덤핑 중심(석유화학·소재)",
   "asOf": "2026-06"
  },
  "VN": {
   "grade": 4,
   "ri": 3,
   "regs": 6,
   "regsNote": "세이프가드·반덤핑(철강 등)",
   "asOf": "2026-06"
  },
  "JP": {
   "grade": 1,
   "ri": 1,
   "regs": 0,
   "regsNote": "현행 규제 없음",
   "asOf": "2026-06"
  },
  "HK": {
   "grade": 2,
   "ri": 2,
   "regs": 0,
   "regsNote": "현행 규제 없음",
   "asOf": "2026-06"
  },
  "TW": {
   "grade": 1,
   "ri": 2,
   "regs": 2,
   "regsNote": "반덤핑(일부 소재)",
   "asOf": "2026-06"
  },
  "SG": {
   "grade": 1,
   "ri": 1,
   "regs": 0,
   "regsNote": "현행 규제 없음",
   "asOf": "2026-06"
  },
  "IN": {
   "grade": 3,
   "ri": 3,
   "regs": 19,
   "regsNote": "반덤핑 최다 축(화학·철강·섬유)",
   "asOf": "2026-06"
  },
  "MX": {
   "grade": 3,
   "ri": 3,
   "regs": 4,
   "regsNote": "반덤핑(철강 등)",
   "asOf": "2026-06"
  },
  "DE": {
   "grade": 1,
   "ri": 1,
   "regs": 6,
   "regsNote": "EU 공동 규제(철강 세이프가드 등)",
   "asOf": "2026-06"
  },
  "NL": {
   "grade": 1,
   "ri": 1,
   "regs": 6,
   "regsNote": "EU 공동 규제(철강 세이프가드 등)",
   "asOf": "2026-06"
  },
  "PL": {
   "grade": 2,
   "ri": 2,
   "regs": 6,
   "regsNote": "EU 공동 규제(철강 세이프가드 등)",
   "asOf": "2026-06"
  },
  "AE": {
   "grade": 2,
   "ri": 2,
   "regs": 1,
   "regsNote": "GCC 세이프가드(일부)",
   "asOf": "2026-06"
  },
  "ID": {
   "grade": 3,
   "ri": 3,
   "regs": 8,
   "regsNote": "세이프가드·반덤핑(섬유·철강)",
   "asOf": "2026-06"
  },
  "TH": {
   "grade": 3,
   "ri": 2,
   "regs": 9,
   "regsNote": "반덤핑(철강 중심)",
   "asOf": "2026-06"
  },
  "GB": {
   "grade": 1,
   "ri": 1,
   "regs": 3,
   "regsNote": "철강 세이프가드 등",
   "asOf": "2026-06"
  }
 },
 "news": [
  {
   "head": "미국, 화장품규제현대화법(MoCRA) 집행 본격화 — 시설등록·성분신고 의무 확대",
   "country": "US",
   "related": [
    "skincare",
    "colorcos"
   ],
   "sent": "neg",
   "sev": "med",
   "topic": "규제·인증",
   "office": "워싱턴무역관",
   "sum": "FDA가 MoCRA 시설등록·제품리스팅 미이행 업체 단속을 예고. 대미 K-뷰티 수출기업은 등록 대행·라벨링 점검 필요."
  },
  {
   "head": "베트남, 한-베 FTA 활용 가공식품 수입 급증 — 유통망 콜드체인 투자 확대",
   "country": "VN",
   "related": [
    "ramen",
    "sauce"
   ],
   "sent": "pos",
   "sev": "opp",
   "topic": "시장 동향",
   "office": "호치민무역관",
   "sum": "현지 대형유통 3사가 한국식품 전용 매대를 확대. FTA 관세 인하 품목 중심으로 진입 기회."
  },
  {
   "head": "인도, 전자·화학 반덤핑 조사 확대 — 對韓 조사 개시 품목 추가",
   "country": "IN",
   "related": [
    "semi",
    "battery"
   ],
   "sent": "neg",
   "sev": "high",
   "topic": "통상·관세",
   "office": "뉴델리무역관",
   "sum": "인도 상공부가 화학·소재 신규 반덤핑 조사에 착수. 인도향 수출 비중이 큰 기업은 대응 필요."
  },
  {
   "head": "UAE, K-푸드 할랄 인증 수요 급증 — 두바이 유통망 입점 상담 2배",
   "country": "AE",
   "related": [
    "ramen",
    "tteok"
   ],
   "sent": "pos",
   "sev": "opp",
   "topic": "시장 동향",
   "office": "두바이무역관",
   "sum": "할랄 인증 취득 한국 식품의 현지 입점 문의가 전년比 2배. 중동 시장 다변화의 실질 창구."
  }
 ],
 "generated": "2026-07-05T05:16:17"
};
