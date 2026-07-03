<p align="center">
  <img src="assets/readme/tradar-readme-banner.png" alt="Tradar README banner" width="100%">
</p>

# Tradar

<p align="center"><strong>An export-market analytics platform that scores and forecasts product-by-country opportunities across Korea's export industries with Korea Customs HS-code data and AI.</strong></p>

<p align="center">
  <a href="https://github.com/spcx0701/tradar/releases/latest"><img alt="Latest release" src="https://img.shields.io/github/v/release/spcx0701/tradar?display_name=tag&color=1D68F0&logo=github&cacheSeconds=60"></a>
  <a href="https://github.com/spcx0701/tradar/actions/workflows/ci.yml"><img alt="Build" src="https://img.shields.io/github/actions/workflow/status/spcx0701/tradar/ci.yml?branch=main&logo=github"></a>
  <a href="https://github.com/spcx0701/tradar/actions/workflows/codeql.yml"><img alt="CodeQL" src="https://github.com/spcx0701/tradar/actions/workflows/codeql.yml/badge.svg?branch=main"></a>
  <a href="https://www.codefactor.io/repository/github/spcx0701/tradar"><img alt="Code quality" src="https://img.shields.io/codefactor/grade/github/spcx0701/tradar?label=code%20quality&logo=codefactor"></a>
  <a href="https://codecov.io/gh/spcx0701/tradar"><img alt="Coverage" src="https://img.shields.io/codecov/c/github/spcx0701/tradar?label=coverage&logo=codecov"></a>
  <a href="https://scorecard.dev/viewer/?uri=github.com/spcx0701/tradar"><img alt="OpenSSF Scorecard" src="https://api.scorecard.dev/projects/github.com/spcx0701/tradar/badge"></a>
  <a href="https://www.bestpractices.dev/en/projects/13452"><img alt="OpenSSF Best Practices" src="https://www.bestpractices.dev/projects/13452/badge"></a>
  <a href="https://sonarcloud.io/summary/overall?id=spcx0701_tradewind&branch=main"><img alt="Bugs" src="https://sonarcloud.io/api/project_badges/measure?project=spcx0701_tradewind&metric=bugs"></a>
  <a href="https://sonarcloud.io/summary/overall?id=spcx0701_tradewind&branch=main"><img alt="Security Rating" src="https://sonarcloud.io/api/project_badges/measure?project=spcx0701_tradewind&metric=security_rating"></a>
  <a href="https://sonarcloud.io/summary/overall?id=spcx0701_tradewind&branch=main"><img alt="Maintainability Rating" src="https://sonarcloud.io/api/project_badges/measure?project=spcx0701_tradewind&metric=sqale_rating"></a>
  <a href="https://sonarcloud.io/summary/overall?id=spcx0701_tradewind&branch=main"><img alt="Technical Debt" src="https://sonarcloud.io/api/project_badges/measure?project=spcx0701_tradewind&metric=sqale_index"></a>
</p>

<p align="center">
  <a href="https://tradar.onrender.com/"><strong>Open platform -></strong></a> &middot;
  <a href="https://www.data.go.kr/data/15100475/openapi.do"><strong>Korea Customs data</strong></a>
</p>

<p align="center">
  <a href="README.md">Korean</a> &middot; <strong>English</strong>
</p>

> Submission for the **2026 Korea Customs Public Data and AI Startup Competition**, Product and Service Development track.
> Tradar covers **28 product groups x major destination countries** across export industries from semiconductors, automobiles, batteries, and shipbuilding to K-Food and K-Beauty.

<p align="center">
  <img src="assets/screens/01-command.png" width="49%" alt="Command Center">
  <img src="assets/screens/02-map.png" width="49%" alt="Market Map">
</p>
<p align="center">
  <img src="assets/screens/03-score.png" width="49%" alt="Score Profile">
  <img src="assets/screens/05-discovery.png" width="49%" alt="Discovery">
</p>

---

## Screens

| Screen | What it does |
|------|------|
| **Command Center** | Top export opportunities, heating markets, risk alerts, and news signals in one operating view |
| **Market Map** | FINVIZ-style treemap: tile size = export value, color = momentum, grouped by sector and country |
| **Score Profile** | Product-level Tradar Score, sub-scores, export trend, country mix, event timeline, and risk index |
| **Discovery** | Sorts 28 product groups by Tradar Score with category filters such as K-Food, semiconductors, and batteries |
| **News Intelligence** | Automatically connects real-time news signals to products and markets with sentiment, impact, and related-item hints |
| **AI Analyst** | Answers product, market, and news questions with numeric evidence, plus a command palette |
| **Report Studio** | Turns a natural-language request into a declarative Report Spec DSL, resolves Korea Customs data, and assembles an interactive report in [app/report.html](app/report.html). The LLM designs the spec only; the engine calculates the numbers to block numeric hallucination. See the [design note](docs/GENERATIVE_REPORTS.md). |

## Data

- **Required public data** - Korea Customs Service [product-by-country export/import results](https://www.data.go.kr/data/15100475/openapi.do) from data.go.kr (`apis.data.go.kr/1220000/nitemtrade`), connected by HS code.
- **Pipeline** - [scripts/build_tradar_data.py](scripts/build_tradar_data.py) fetches HS-code results, computes annual exports, YoY change, and country share, then builds `app/data/tradar.js`.
  - With `DATA_GO_KR_KEY`, the pipeline syncs live data through [server/customs_client.py](server/customs_client.py).
  - Without the key, the app falls back to 2024 Korea Customs published-value anchors so the demo remains usable.
- **AI and analytics** - Tradar Score, demand trend, forecasting, anomaly detection, and evidence-based advising are implemented in [server/](server/) and can be connected to the pipeline.

Korea Customs public data plus Korean AI directly supports the competition rubric, including the domestic-AI bonus.

## How It Works

```text
Korea Customs product-by-country export/import results (HS code)
        |  scripts/build_tradar_data.py  (live with API key / 2024 anchor without key)
        v
app/data/tradar.js  -->  Tradar SPA (React + ECharts, Chartmetric-style design system)
```

## Quick Start

```bash
python scripts/build_tradar_data.py     # Korea Customs data -> app/data/tradar.js
python scripts/serve.py                 # Platform: http://localhost:5183
```

## Contribution And Feedback

- Report bugs and enhancement requests through [GitHub Issues](https://github.com/spcx0701/tradar/issues).
- Propose code changes with a pull request. Before opening a PR, run the tests and lint commands in [CONTRIBUTING.md](CONTRIBUTING.md).
- Please report exploitable vulnerabilities, secret exposure, authentication bypasses, or possible data exposure through a private [GitHub Security Advisory](https://github.com/spcx0701/tradar/security/advisories/new), not a public issue.

## API Interface

The FastAPI server exposes JSON endpoints under `/api/*` alongside the static PWA.

| Endpoint | Input | Output |
|---|---|---|
| `GET /api/health` | none | service status, data period, product count |
| `GET /api/catalog` | none | metadata, country list, product catalog |
| `GET /api/forecast?hs=1902.30&country=US&horizon=6` | HS code, country code, 1-12 month horizon | historical series, forecast mean/range, trend, market signal |
| `GET /api/radar?limit=24` | result limit | top export opportunities and risk alerts |
| `GET /api/radar/product/{hs}` | HS code | country-market radar for one product |
| `POST /api/advisor` | `{"question": "..."}` | detected intent, answer, numeric evidence |
| `POST /api/report` | `{"question": "..."}` | natural language -> Report Spec plan -> data-resolved report |
| `POST /api/report/render` | `{"spec": {...}}` | direct spec resolution for UI round-trips |
| `GET /api/report/schema` | none | JSON schema contract for the Report Spec DSL |

## Repository Structure

```text
app/
  index.html         Tradar platform and PWA metadata
  vendor/generated/ generated design runtime and design-system bundle
  _ds/               Chartmetric-style design system tokens, styles, and components
  data/tradar.js     Korea Customs-linked data built by build_tradar_data.py
  vendor/            local React 18 and ECharts 5 bundles for offline use
server/              Korea Customs API client and AI engines for forecasting, scoring, and advising
scripts/             data pipeline, server helper, and capture scripts
packaging/android/   Android app with Jetpack Compose and TWA packaging
deliverables/        competition submission materials
design/              source design artifacts
```

## Design System

Tradar follows a light, data-dense Chartmetric-style interface in [app/_ds](app/_ds): dark sidebar, white canvas, restrained blue accents, a cyan-to-blue-to-violet brand gradient, tabular numbers, and ECharts visualizations.

## License

[MIT](LICENSE). Demo data is anchored to public Korea Customs statistics and does not include personally identifiable or company-identifiable information.
