# Fraud Decision Tree MLOps

<p align="center">
  <img src="docs/diagrams/fraud-mlops-big-tech-architecture.svg" alt="Fraud Decision Tree MLOps Architecture" width="100%">
</p>

A production-oriented fraud detection baseline that separates data access, cleaning,
validation, feature engineering, model training, serving, and telemetry. It uses a
scikit-learn Decision Tree, MLflow, FastAPI, MongoDB, Docker, GitHub Actions, and uv.
Version 0.3 adds governed artifacts, manifest validation, API-key production mode,
versioned inference endpoints, batch prediction, drift helpers, and security docs.

## Architecture

```text
Raw data -> Repository/DAO -> Cleaning -> Validation -> Feature engineering
         -> Decision Tree -> Evaluation -> MLflow + joblib artifact
         -> FastAPI -> MongoDB telemetry -> Monitoring queries
```

Training calls `build_training_dataset()` rather than embedding CSV and preparation
logic. Inference reuses the same feature-engineering function used by training.
Telemetry is fail-soft: MongoDB outages never block a prediction response.

<p align="center">
  <img src="docs/diagrams/fraud-mlops-underground-graph.svg" alt="Fraud MLOps underground graph" width="100%">
</p>

## Quick Start

Requires Python 3.11 and [uv](https://docs.astral.sh/uv/).

```bash
cp .env.example .env
uv venv --python 3.11
uv pip install -e ".[dev]"
make train
make validate
make test
make api
```

API docs are available at `http://localhost:8000/docs`.

```bash
curl -X POST http://localhost:8000/v1/predict \
  -H 'Content-Type: application/json' \
  -d '{"transaction_id":"txn_001","transaction_amount":750.0,"transaction_hour":2,"customer_age_days":14,"num_previous_transactions":1,"merchant_risk_score":0.82,"device_risk_score":0.74}'
```

## API And Telemetry

| Endpoint | Purpose |
|---|---|
| `GET /health/live` | Process liveness |
| `GET /health/ready` | Model artifact and manifest readiness |
| `GET /version` | Application, model, schema, and Git metadata |
| `GET /metrics` | Prometheus-compatible API metadata metric |
| `POST /v1/predict` | Validate, engineer features, score, and log telemetry |
| `POST /v1/predict/batch` | Batch prediction with configured size limit |
| `GET /v1/telemetry/recent` | Return recent MongoDB events or HTTP 503 |
| `GET /v1/monitoring/summary` | Operational prediction summary |

Legacy `/health`, `/ready`, `/predict`, and `/telemetry/recent` aliases remain
available but are marked deprecated.

Each telemetry event stores request features, prediction, risk score, model identity,
and a UTC timestamp. Start the complete local stack with `make docker-up`.

## v0.2.0 Observability and Demo Workflow

Train and validate the model, then start the API:

```bash
make train
make validate
make api
```

In another terminal, exercise inference and observability:

```bash
make demo
make telemetry-smoke
make monitoring-summary
make explain
```

`make demo` sends low-, medium-, and high-risk transactions and validates every API
response. `make telemetry-smoke` confirms recent events when MongoDB is available and
exits cleanly when telemetry is unavailable. `make monitoring-summary` reports total
predictions, fraud rate, and average risk. `make explain` prints Decision Tree feature
importances and requires `make train` first.

For API plus MongoDB, use `docker compose up --build`, then run the demo commands in a
second terminal. Prediction telemetry remains fail-soft: MongoDB downtime never blocks
inference. Generated datasets, models, metrics, and MLflow state remain ignored.

## v0.3.0 Production Hardening

The training pipeline now writes a governed model artifact plus a SHA-256 manifest.
The API refuses artifacts with incompatible schema or hash mismatches. Prediction
responses include `decision_threshold`, `request_id`, and artifact schema metadata.

Production settings require API-key authentication and reject wildcard CORS. Set:

```bash
APP_ENV=production
ENABLE_API_KEY_AUTH=true
API_KEY=<strong-secret>
CORS_ALLOW_ORIGINS=https://your-app.example
```

## Model Lifecycle

`make train` generates synthetic raw data when needed, persists a processed dataset,
logs parameters and metrics to MLflow, and writes a joblib serving artifact plus a
manifest and data-quality reports. `make validate` enforces model gates.

| Metric | Validation floor |
|---|---:|
| Recall | 0.50 |
| F1 score | 0.35 |
| ROC-AUC | 0.60 |
| PR-AUC | 0.25 |

Generated datasets, model files, MLflow state, and `reports/metrics.json` are ignored.
Source, tests, configs, docs, diagrams, workflows, and `uv.lock` remain tracked.

## Development Commands

| Command | Action |
|---|---|
| `make install` | Install project and development dependencies |
| `make format` | Apply Ruff fixes and Black formatting |
| `make lint` / `make typecheck` | Check style and typing |
| `make security` | Run Bandit scan |
| `make test` | Run unit, integration, and contract tests |
| `make coverage` | Run tests with coverage gate |
| `make train` / `make train-ci` | Train and validate the baseline |
| `make api` / `make mlflow` | Run API or MLflow UI |
| `make demo` / `make e2e` | Exercise inference and live API smoke tests |
| `make monitoring-summary` / `make explain` | Inspect operations and model importance |
| `make docker-up` / `make docker-down` | Manage the local service stack |

## Project Layout

```text
src/fraud_detection/
├── data/          # DAO, cleaning, validation, preprocessing, pipeline
├── features/      # Shared feature engineering
├── models/        # Training, evaluation, prediction, explainability
├── api/           # FastAPI schemas, dependencies, and routes
├── telemetry/     # MongoDB client, event logging, monitoring queries
└── monitoring/    # Extension points for quality, drift, and performance
```

## Documentation

- [Data architecture](docs/data_architecture.md)
- [ML lifecycle](docs/ml_lifecycle.md)
- [Model governance](docs/model_governance.md)
- [Responsible AI](docs/responsible_ai.md)
- [Data sheet](docs/data_sheet.md)
- [API contract](docs/api_contract.md)
- [Telemetry](docs/telemetry.md)
- [Model card](docs/model_card.md)
- [Security](docs/security.md)
- [Threat model](docs/threat_model.md)
- [Runbook](docs/runbook.md)
- [Limitations](docs/limitations.md)
- [Demo workflow](docs/demo_workflow.md)
- [Monitoring](docs/monitoring.md)
- [Model explainability](docs/model_explainability.md)

Licensed under the [MIT License](LICENSE).
