"""환경 설정 (12-factor). 모든 비밀값은 환경변수로 주입."""
from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class Settings:
    # 관세청 data.go.kr 인증키 — 없으면 데모 스냅샷 사용
    data_go_kr_key: str = field(default_factory=lambda: os.environ.get("DATA_GO_KR_KEY", ""))
    # 국산 LLM(Solar/HyperCLOVA X) — 없으면 데모 NLG 사용
    llm_provider: str = field(default_factory=lambda: os.environ.get("TW_LLM_PROVIDER", ""))
    llm_api_key: str = field(default_factory=lambda: os.environ.get("TW_LLM_KEY", ""))
    cors_origins: str = field(default_factory=lambda: os.environ.get("TW_CORS", "*"))
    app_name: str = "무역풍 Tradewind API"
    version: str = "0.1.0"

    @property
    def live_data(self) -> bool:
        return bool(self.data_go_kr_key)


settings = Settings()
