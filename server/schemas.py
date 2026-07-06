"""API 요청·응답 스키마(OpenAPI 문서화용)."""
from __future__ import annotations

from pydantic import BaseModel, Field


class AdvisorRequest(BaseModel):
    question: str = Field(..., examples=["라면 어디에 수출하면 좋을까?"], min_length=1)


class Evidence(BaseModel):
    label: str
    value: str


class AdvisorResponse(BaseModel):
    question: str
    intent: dict
    answer: str
    evidence: list[Evidence]
    suggestions: list[str]
    chart: dict | None = None
    engine: str = "demo-grounded"
    llm_error: str | None = None


class LLMProviderSelectionRequest(BaseModel):
    provider: str = Field(..., examples=["openrouter-solar-free"], min_length=1)


class ForecastPoint(BaseModel):
    months: list[str]
    fc_months: list[str]
    hist: list[float]
    mean: list[float]
    lo: list[float]
    hi: list[float]
    yoy: float
    status: str
    opportunity: float
    mape: float
    trend: float
