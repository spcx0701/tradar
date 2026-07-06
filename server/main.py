"""무역풍 Tradewind — FastAPI 진입점.

REST API(/api/*) + 정적 PWA(app/) 동시 서빙. 단일 프로세스로 배포 가능(Render 등).
실행: ``uvicorn server.main:app --reload`` (개발) / ``uvicorn server.main:app`` (운영).
"""
from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .config import settings
from .routers.api import router as api_router

app = FastAPI(title=settings.app_name, version=settings.version,
              description="관세청·산업부 공공데이터와 AI 기반 수출 수요예측·조기경보 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(api_router)

_APP_DIR = os.path.join(os.path.dirname(__file__), "..", "app")


@app.get("/")
def index():
    return FileResponse(os.path.join(_APP_DIR, "index.html"))


# 정적 자산(앱 화면·데이터·아이콘) 서빙
if os.path.isdir(_APP_DIR):
    app.mount("/", StaticFiles(directory=_APP_DIR, html=True), name="app")
