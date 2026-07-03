# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

무역풍 (Tradewind) / product name **Tradar** — a Korean Customs Service (관세청) export-data analytics platform. It scores and forecasts export markets by HS code × country using an in-house ("국산", domestic) AI stack (no external LLM required for the demo). Built for the 2026 관세청 공공데이터·AI 활용 창업경진대회 competition. Korean-first: code comments/docs are Korean, identifiers are English.

## Commands

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt        # installs requirements.txt + pytest/ruff/etc.

# Data pipeline (snapshot -> AI engine outputs -> static JSON, used by server/dataset.py + FastAPI)
python scripts/generate_snapshot.py        # (re)generate server/data/snapshot.json
python scripts/build_app_data.py           # run forecasting/radar/scoring -> app/data/*.json

# Static PWA dev server (no backend needed)
python scripts/serve.py                    # http://localhost:5183

# Live API server (FastAPI)
uvicorn server.main:app --reload

# Tests / lint (must pass before PR)
pytest -q
pytest server/tests/test_core.py -q                 # single file
pytest server/tests/test_core.py::test_dataset_loads -q  # single test
ruff check server scripts
```

CI (`.github/workflows/ci.yml`) runs `ruff check server scripts`, regenerates data deterministically (`generate_snapshot.py` + `build_app_data.py`), then `pytest -q --cov=server --cov=scripts`, plus an OWASP ZAP baseline scan against the running app and a GitHub Pages deploy job (main only).

### Second, separate data pipeline (Tradar dashboard)

`app/index.html` (the Tradar dashboard UI) does **not** read `server/dataset.py`'s snapshot — it consumes `app/data/tradar.js` (`window.TRADAR_DATA = {P, markets, news}`), rebuilt by:

```bash
python scripts/build_tradar_data.py        # refreshes app/data/tradar.js from data.go.kr (needs DATA_GO_KR_KEY) or keeps 2024 published anchors
```

Trade-intelligence enrichment (company/buyer/shipment flows, `window.TRADAR_TRADE_INTEL` in `app/data/tradar.js`) is a separate sync:

```bash
python scripts/check_trade_intel_keys.py   # check which optional keys/CSVs are configured
python scripts/sync_trade_intel.py --public-bl-csv server/data/public_bl_sample.csv
python scripts/audit_trade_intel.py --max-age-hours 72   # staleness gate, run before deploy
```

Env vars (`DATA_GO_KR_KEY`, `TRADE_INTEL_*`, `IMPORTYETI_API_KEY`, `TW_LLM_*`, `TW_CORS`) are documented in [.env.example](.env.example) and loaded automatically from `.env` by `server/env.py`. Nothing requires these to be set — every pipeline has a deterministic offline fallback ("데모는 항상 동작한다": the demo must always work without external keys).

## Architecture

Three layers, per [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): **data → AI engine → presentation**.

1. **Data**: 관세청 (Korean Customs) OpenAPI `nitemtrade` (HS code × country × month export stats), fetched by [server/customs_client.py](server/customs_client.py). Falls back to a seeded, reproducible snapshot anchored to 2024 published figures when `DATA_GO_KR_KEY` is unset.
2. **AI engine** (pure numpy, no external ML services):
   - [server/forecasting.py](server/forecasting.py) — multiplicative seasonal decomposition + damped log-linear trend extrapolation for demand forecasts (with 95% prediction intervals).
   - [server/radar.py](server/radar.py) — momentum/acceleration/volatility signals → opportunity & risk scores, early-warning states (급등/상승/안정/둔화/변동).
   - [server/scoring.py](server/scoring.py) — combines radar signals into the "Tradar Score" (0-100 market attractiveness + sub-scores), modeled after Chartmetric's CM Score/Career Stage concept.
   - [server/advisor.py](server/advisor.py) — Korean-language intent extraction (품목/국가/의도) + grounded NLG; can hand the same evidence pack to a domestic LLM adapter (Solar/HyperCLOVA X via `TW_LLM_*`) for phrasing only — numbers always come from the engine, never the LLM, to prevent hallucination.
   - [server/reportspec.py](server/reportspec.py) — natural language → **Report Spec DSL** (`tradar-report/1`) → JSON-schema validation → deterministic resolve against dataset/forecasting/radar/scoring → interactive report blocks. The LLM only ever designs the spec (data references: HS code, country, period); it never sees or emits numbers, so numeric hallucination is structurally blocked. Full research lineage/design rationale in [docs/GENERATIVE_REPORTS.md](docs/GENERATIVE_REPORTS.md); consumed by [app/report.html](app/report.html).
3. **Presentation**:
   - `server/main.py` (FastAPI) serves `/api/*` (see [server/routers/api.py](server/routers/api.py): `/api/health`, `/api/catalog`, `/api/forecast`, `/api/radar`, `/api/radar/product/{hs}`, `/api/advisor`, `/api/report`, `/api/report/render`, `/api/report/schema`) and mounts `app/` as static files in one process (deployable as-is on Render).
   - Static PWA in `app/` also works fully offline from pre-baked `app/data/*.json`/`tradar.js` with no server (deployed to GitHub Pages).
   - `packaging/android/` — native wrapper (Jetpack Compose + TWA) pointed at either the static PWA or a deployed API via `TRADEWIND_API_BASE`.

### Two independent data models — don't conflate them

- `server/dataset.py` loads `server/data/snapshot.json` (built by `generate_snapshot.py`) — this is what the FastAPI `/api/*` routes, `server/tests/test_core.py`, and `build_app_data.py` all use.
- `app/data/tradar.js` (`window.TRADAR_DATA`) is a separate, hand/pipeline-maintained payload for the dashboard UI in `app/index.html`, rebuilt by `scripts/build_tradar_data.py` (which evaluates the JS via `node -e` to round-trip it, so Node must be on PATH for that script). Changes to one do not propagate to the other — check which one an endpoint/screen actually reads before editing data.

### Frontend

`app/index.html` and `app/report.html` are vanilla JS (no build step, no framework) using locally vendored React 18 + ECharts 5 (`app/vendor/`) for offline capability. UI follows the Chartmetric-inspired design system in `app/_ds/` (dark sidebar + white canvas, blue accents, brand gradient, tabular numerals). `app/_ds/**` and `app/vendor/**` are generated/vendored — excluded from oxlint (see `.oxlintrc.json`) and not meant to be hand-edited like first-party code.

## Conventions

- Python comments/docstrings and docs are Korean; identifiers (functions, variables) are English.
- New features should include regression tests where practical; if not feasible, note why in the PR.
- API contract changes must update both the README.md API table and corresponding tests.
- Keep the offline/no-external-key path always working — every pipeline script must degrade gracefully (anchored snapshot / skipped connector) rather than fail when optional keys are absent.
