# Tradar English Documentation

Tradar is an export-market analytics platform. It combines Korea Customs export/import statistics with AI scoring, forecasting, and risk signals so users can compare product and country export opportunities.

## Quick Start

```bash
python scripts/build_tradar_data.py
python scripts/serve.py
```

The static web app is served at `http://localhost:5183`. If `DATA_GO_KR_KEY` is set, the customs-data client can refresh data from data.go.kr; otherwise the demo dataset remains usable without external keys.

## API Interface

The FastAPI server exposes JSON endpoints under `/api/*`.

| Endpoint | Input | Output |
|---|---|---|
| `GET /api/health` | none | service status, data period, product count |
| `GET /api/catalog` | none | metadata, country list, product catalog |
| `GET /api/forecast?hs=1902.30&country=US&horizon=6` | HS code, country code, 1-12 month horizon | historical series, forecast mean/range, trend, market signal |
| `GET /api/radar?limit=24` | result limit | top export opportunities and risk alerts |
| `GET /api/radar/product/{hs}` | HS code | country-market radar for one product |
| `POST /api/advisor` | `{"question": "..."}` | detected intent, answer, evidence |

## Contribution And Feedback

Bug reports and enhancement requests are accepted through GitHub Issues. Code changes should be proposed as pull requests. Before opening a pull request, run:

```bash
pytest -q
ruff check server scripts
```

English bug reports, pull request comments, and code comments are welcome.

## Security Reporting

Please do not report exploitable vulnerabilities, credential leaks, authentication bypasses, or data exposure details in public issues. Use GitHub Security Advisories instead:

https://github.com/spcx0701/tradar/security/advisories/new
