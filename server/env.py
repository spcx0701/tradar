"""Local .env loader for development and single-process deployments."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_env_file(path: str | Path | None = None, *, override: bool = False) -> dict[str, str]:
    """Load KEY=VALUE pairs from `.env` without printing or overwriting secrets."""
    env_path = Path(path) if path else ROOT / ".env"
    if not env_path.exists():
        return {}
    loaded: dict[str, str] = {}
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = _clean_value(value.strip())
        if not key:
            continue
        loaded[key] = value
        if override or key not in os.environ:
            os.environ[key] = value
    return loaded


def _clean_value(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value
