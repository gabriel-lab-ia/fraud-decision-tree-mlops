# Fraud Decision Tree MLOps

<p align="center">
  <img src="docs/diagrams/fraud-mlops-big-tech-architecture.svg" alt="Fraud Decision Tree MLOps Architecture" width="100%">
</p>

Production-oriented fraud detection baseline for MLOps practice and portfolio use.
The project separates data access, cleaning, contract validation, feature
engineering, model training, model governance, FastAPI serving, MongoDB telemetry,
MLflow tracking, Docker runtime, documentation, and CI quality gates.

Version 0.3 focuses on production hardening. It adds governed model artifacts,
manifest validation, data fingerprints, train/validation/test splitting, richer
metrics, threshold selection, calibrated probabilities, versioned API endpoints,
batch prediction, production security settings, PSI drift helpers, and public
operational documentation.

This is not approved for autonomous financial decisions. It uses synthetic data by
default and requires real-data validation, fairness review, monitoring, and human
approval controls before consequential use.

## v0.3 Status

Implemented and validated on branch `feat/v0.3-production-hardening`:

- Governed artifact schema `fraud-model-artifact-v1`.
- SHA-256 sidecar manifest for model artifact integrity.
- Dataset contract `transaction-dataset-v1` and deterministic dataset fingerprint.
- Stratified train, validation, and test split.
- Decision Tree training with sigmoid calibration through scikit-learn.
- Threshold selection using validation data, default strategy `max_f1`.
- Validation gates for recall, F1, ROC-AUC, PR-AUC, false-negative rate, and Brier
  score.
- FastAPI `/v1` inference API with batch prediction and request IDs.
- Readiness, version, metrics, telemetry, and monitoring summary endpoints.
- Production security posture checks for API key and CORS.
- Production telemetry hashing for transaction IDs.
- PSI helper for drift detection.
- MkDocs documentation, runbook, threat model, release notes, and governance docs.

Not implemented in v0.3:

- Automated hyperparameter search, despite the config placeholder.
- Automated scheduled drift jobs or alert delivery.
- Model registry promotion workflow beyond MLflow logging and local artifacts.
- Git tag or GitHub Release. Those are intentionally post-merge tasks.

## Architecture

```text
Raw/synthetic data
  -> repository / DAO
  -> cleaning
  -> data contract validation
  -> shared feature engineering
  -> train / validation / test split
  -> Decision Tree training + optional calibration
  -> validation threshold selection
  -> metrics, baselines, MLflow logging
  -> joblib model artifact + SHA-256 manifest
  -> FastAPI /v1 serving
  -> MongoDB telemetry
  -> monitoring queries + PSI drift helper
```

Training calls `build_training_dataset()` and the API reuses the same feature
engineering path used during training. Telemetry is fail-soft: MongoDB insert
failures are logged and do not block prediction responses.

<p align="center">
  <img src="docs/diagrams/fraud-mlops-underground-graph.svg" alt="Fraud MLOps underground graph" width="100%">
</p>

## Local Execution

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

Example single prediction:

```bash
curl -X POST http://localhost:8000/v1/predict \
  -H 'Content-Type: application/json' \
  -d '{"transaction_id":"txn_001","transaction_amount":750.0,"transaction_hour":2,"customer_age_days":14,"num_previous_transactions":1,"merchant_risk_score":0.82,"device_risk_score":0.74}'
```

Demo and smoke checks:

```bash
make demo
make telemetry-smoke
make monitoring-summary
make explain
```

## Model Artifact Governance

Training writes:

- `artifacts/models/decision_tree_model.joblib`
- `artifacts/models/decision_tree_model.manifest.json`
- `reports/metrics.json`
- `reports/data_quality_report.json`
- `reports/reference_profile.json`
- `reports/evaluation_summary.md`

Generated artifacts and reports are ignored by Git.

The serving artifact includes model metadata, feature order, model version,
project version, decision threshold, calibration method, dataset fingerprint, data
schema version, training timestamp, training run ID, Git commit, metrics summary,
Python version, and scikit-learn version.

The manifest records artifact schema, path, size, SHA-256 hash, creation time, and
metadata. The API loader validates artifact schema and refuses hash mismatches when
the manifest is present. The artifact is still a joblib/sklearn artifact, so it
must only be loaded from trusted training output.

## Data Contract And Fingerprint

Required raw columns:

- `transaction_amount`
- `transaction_hour`
- `customer_age_days`
- `num_previous_transactions`
- `merchant_risk_score`
- `device_risk_score`
- `is_fraud`

The contract rejects missing columns, unexpected columns, duplicate rows, missing
values, non-numeric values, infinite values, invalid ranges, non-binary targets,
one-class targets, and class counts below the configured minimum.

The dataset fingerprint is a SHA-256 hash over the schema version, sorted columns,
and normalized data payload. It is recorded in model metadata and data-quality
reports for lineage checks.

## Training, Metrics, And Gates

`make train` builds or loads the dataset, validates the contract, creates
stratified train/validation/test splits, trains the Decision Tree, calibrates
probabilities with sigmoid calibration, selects a threshold on the validation
split, evaluates on the test split, logs MLflow metadata, and writes governed
artifacts.

Current gates from `configs/train_config.yaml`:

| Gate | Threshold |
|---|---:|
| Recall | >= 0.50 |
| F1 score | >= 0.35 |
| ROC-AUC | >= 0.60 |
| PR-AUC | >= 0.25 |
| False-negative rate | <= 0.50 |
| Brier score | <= 0.30 |

Metrics include accuracy, balanced accuracy, precision, recall, specificity, F1,
F-beta, ROC-AUC, PR-AUC, MCC, false-positive rate, false-negative rate, Brier score,
log loss, prediction rate, support counts, confusion matrix, validation metrics,
DummyClassifier baseline, and LogisticRegression baseline.

MLflow logs parameters, metrics, model metadata, data-quality report, artifact
manifest, and the sklearn model.

## API Contract

Versioned endpoints:

| Endpoint | Purpose |
|---|---|
| `GET /health/live` | Process liveness |
| `GET /health/ready` | Model artifact readiness |
| `GET /version` | Application, model, artifact schema, and Git metadata |
| `GET /metrics` | Prometheus-compatible API metadata metric |
| `POST /v1/predict` | Single transaction prediction |
| `POST /v1/predict/batch` | Batch prediction |
| `GET /v1/telemetry/recent` | Recent MongoDB telemetry events or HTTP 503 |
| `GET /v1/monitoring/summary` | Prediction count, fraud rate, and average risk |

Deprecated aliases remain available for compatibility:

- `GET /health`
- `GET /ready`
- `POST /predict`
- `GET /telemetry/recent`

Prediction responses include transaction ID, prediction, label, risk score,
decision threshold, model name, model version, artifact schema version, telemetry
event ID, and request ID.

Batch prediction accepts a non-empty list of transaction requests. The runtime limit
is configured with `MAX_BATCH_SIZE`, default `100`, with settings validation between
1 and 1000.

## Security

Production settings enforce:

- `APP_ENV=production`
- `ENABLE_API_KEY_AUTH=true`
- non-empty `API_KEY`
- no wildcard `CORS_ALLOW_ORIGINS`

Example:

```bash
APP_ENV=production
ENABLE_API_KEY_AUTH=true
API_KEY=<strong-secret>
CORS_ALLOW_ORIGINS=https://your-app.example
```

When `ENABLE_API_KEY_AUTH` is enabled, prediction routes require `x-api-key`.
Telemetry hashes transaction IDs in production and stores raw transaction IDs only
outside production. Settings expose a redacted `safe_dict()` for debugging.

Security limitations still apply: this is not a full auth platform, no rate limiting
is implemented, and joblib artifacts must be treated as trusted files only.

## Drift Detection

`fraud_detection.monitoring.drift` provides a Population Stability Index helper and
classification thresholds:

- `< 0.10`: stable
- `0.10` to `< 0.25`: moderate drift
- `>= 0.25`: significant drift

This is a library helper, not a scheduled monitoring service. Alerting, production
windows, labeled-outcome monitoring, and dashboard automation remain future work.

## Docker

Build the container:

```bash
make docker-build
```

Run API, MongoDB, and MLflow with Docker Compose:

```bash
make train
docker compose up --build
```

The API container runs as a non-root user and includes a liveness healthcheck.
Generated artifacts are mounted read-only into the API service.

## Quality Gates

Main gates:

```bash
make lint
make typecheck
make security
make test
make coverage
make train-ci
make docs
make docker-build
git diff --check
```

The v0.3 implementation was validated with:

- `make quality-gates`
- `make coverage` with 90.14% total coverage and an 85% threshold
- `make train-ci`
- `make docs`
- `make docker-build`
- `git diff --check`

## Documentation

MkDocs is configured in `mkdocs.yml`.

```bash
make docs
make docs-serve
```

Public docs include:

- [Release notes v0.3.0](docs/releases/v0.3.0.md)
- [Architecture](docs/architecture.md)
- [Data architecture](docs/data_architecture.md)
- [ML lifecycle](docs/ml_lifecycle.md)
- [Model governance](docs/model_governance.md)
- [Responsible AI](docs/responsible_ai.md)
- [Data sheet](docs/data_sheet.md)
- [API contract](docs/api_contract.md)
- [Telemetry](docs/telemetry.md)
- [Monitoring](docs/monitoring.md)
- [Drift detection](docs/drift_detection.md)
- [Security](docs/security.md)
- [Threat model](docs/threat_model.md)
- [Deployment](docs/deployment.md)
- [Runbook](docs/runbook.md)
- [Incident response](docs/incident_response.md)
- [Model card](docs/model_card.md)
- [Limitations](docs/limitations.md)

## Repository Structure

```text
.
├── configs/                 # Training configuration and validation gates
├── docs/                    # MkDocs public documentation
├── scripts/                 # Training, API, validation, demo, and smoke scripts
├── src/fraud_detection/
│   ├── api/                 # FastAPI schemas, dependencies, and routes
│   ├── data/                # DAO, cleaning, contract, splitting, preprocessing
│   ├── features/            # Shared feature engineering
│   ├── models/              # Artifact, training, evaluation, prediction
│   ├── monitoring/          # Data quality, performance, drift helpers
│   └── telemetry/           # MongoDB client, event logging, monitoring queries
├── tests/                   # Unit, integration, and contract tests
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── pyproject.toml
```

Generated datasets, model artifacts, reports, MLflow state, local databases, caches,
and secrets are intentionally ignored.

## Roadmap

Post-v0.3 candidates:

- Open PR, review, merge to `main`, then create tag and GitHub Release.
- Add scheduled drift jobs and alert routing.
- Add rate limiting and stronger authentication for production deployments.
- Add model registry promotion workflow.
- Add real-data validation, calibration review, and fairness analysis.
- Add CI publishing of docs after merge.

Licensed under the [MIT License](LICENSE).
