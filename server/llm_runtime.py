"""Runtime owner for the server-side LLM provider selection."""
from __future__ import annotations

from typing import Any

from .advisor import llm_provider_status, normalize_llm_provider
from .config import Settings, settings

_selected_provider_override: str | None = None


def selected_llm_provider(config: Settings = settings) -> str:
    return _selected_provider_override or normalize_llm_provider(config.llm_provider)


def llm_provider_control_state(config: Settings = settings) -> dict[str, Any]:
    selected = selected_llm_provider(config)
    providers = llm_provider_status(config)
    return {
        "selected_provider": selected,
        "providers": providers,
    }


def set_selected_llm_provider(provider: str, config: Settings = settings) -> dict[str, Any]:
    global _selected_provider_override

    normalized = normalize_llm_provider(provider)
    providers = llm_provider_status(config)
    known = {item["provider"]: item for item in providers}
    if normalized not in known:
        raise ValueError(f"Unsupported LLM provider: {provider}")
    if not known[normalized]["configured"]:
        raise RuntimeError(f"LLM provider is not configured: {normalized}")
    _selected_provider_override = normalized
    return llm_provider_control_state(config)
