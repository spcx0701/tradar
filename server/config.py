"""환경 설정 (12-factor). 모든 비밀값은 환경변수로 주입."""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from .env import load_env_file

load_env_file()


def _first_env(*names: str) -> str:
    for name in names:
        value = os.environ.get(name, "").strip()
        if value:
            return value
    return ""


@dataclass
class Settings:
    # 관세청 data.go.kr 인증키 — 없으면 데모 스냅샷 사용
    data_go_kr_key: str = field(default_factory=lambda: os.environ.get("DATA_GO_KR_KEY", ""))
    # 운영자 선택 LLM(Solar/OpenRouter/Gemini/Groq) — 없으면 데모 NLG 사용
    llm_provider: str = field(default_factory=lambda: os.environ.get("TW_LLM_PROVIDER", ""))
    llm_api_key: str = field(default_factory=lambda: os.environ.get("TW_LLM_KEY", ""))
    llm_base_url: str = field(default_factory=lambda: os.environ.get("TW_LLM_BASE_URL", ""))
    llm_model: str = field(default_factory=lambda: os.environ.get("TW_LLM_MODEL", ""))
    llm_timeout: float = field(default_factory=lambda: float(os.environ.get("TW_LLM_TIMEOUT", "12")))
    openrouter_api_key: str = field(
        default_factory=lambda: _first_env("TW_OPENROUTER_KEY", "OPENROUTER_API_KEY")
    )
    openrouter_base_url: str = field(
        default_factory=lambda: os.environ.get("TW_OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    )
    openrouter_model: str = field(
        default_factory=lambda: os.environ.get("TW_OPENROUTER_MODEL", "upstage/solar-pro-3:free")
    )
    groq_api_key: str = field(
        default_factory=lambda: _first_env("TW_GROQ_KEY", "GROQ_API_KEY")
    )
    groq_base_url: str = field(
        default_factory=lambda: os.environ.get("TW_GROQ_BASE_URL", "https://api.groq.com/openai/v1")
    )
    groq_model: str = field(
        default_factory=lambda: os.environ.get("TW_GROQ_MODEL", "llama-3.3-70b-versatile")
    )
    gemini_api_key: str = field(
        default_factory=lambda: _first_env("TW_GEMINI_KEY", "GEMINI_API_KEY")
    )
    gemini_base_url: str = field(
        default_factory=lambda: os.environ.get(
            "TW_GEMINI_BASE_URL",
            "https://generativelanguage.googleapis.com/v1beta/openai",
        )
    )
    gemini_model: str = field(default_factory=lambda: os.environ.get("TW_GEMINI_MODEL", "gemini-3.5-flash"))
    llm_admin_token: str = field(default_factory=lambda: os.environ.get("TW_ADMIN_TOKEN", ""))
    cors_origins: str = field(default_factory=lambda: os.environ.get("TW_CORS", "*"))
    app_name: str = "무역풍 Tradewind API"
    version: str = "0.1.0"

    @property
    def live_data(self) -> bool:
        return bool(self.data_go_kr_key)


settings = Settings()
