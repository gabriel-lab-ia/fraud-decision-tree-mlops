# Architecture

The project is organized as a small but complete MLOps system: data ingestion and
validation are separated from feature engineering, training, artifact governance,
serving, telemetry, and documentation.

![Fraud Decision Tree MLOps Architecture](diagrams/fraud-mlops-big-tech-architecture.svg)

## Runtime Flow

```text
Raw or synthetic transactions
  -> TransactionDataRepository
  -> cleaning and data contract validation
  -> shared feature engineering
  -> train / validation / test split
  -> Decision Tree training and sigmoid calibration
  -> validation threshold selection
  -> MLflow logging and governed model artifact
  -> FastAPI /v1 prediction API
  -> MongoDB telemetry and monitoring summaries
```

## Main Components

| Layer | Implementation | Purpose |
|---|---|---|
| Data access | `src/fraud_detection/data/repository.py` | Load or generate transaction data and persist processed data. |
| Data quality | `cleaning.py`, `contract.py`, `validation.py` | Clean data, enforce schema, reject malformed datasets, and fingerprint training data. |
| Features | `features/feature_engineering.py` | Build model features shared by training and inference. |
| Training | `models/train_decision_tree.py` | Train, calibrate, select threshold, evaluate, and log to MLflow. |
| Artifact governance | `models/artifact.py` | Build artifact metadata, save manifest, and validate artifact integrity. |
| Serving | `api/main.py`, `api/routes.py`, `models/predict.py` | Expose health, readiness, version, metrics, single prediction, and batch prediction. |
| Telemetry | `telemetry/` | Store prediction events and provide monitoring queries. |
| Monitoring | `monitoring/` | Provide data-quality, performance, and PSI drift helpers. |

## Diagrams

The repository keeps GitHub-renderable SVG diagrams under `docs/diagrams/` and a
Mermaid source file for the simpler flow diagram. The invalid empty Draw.io
placeholder was removed during repository renovation.

![Fraud MLOps System Graph](diagrams/fraud-mlops-underground-graph.svg)

## Design Constraints

- Runtime artifacts are generated locally and ignored by Git.
- API telemetry is fail-soft so MongoDB outages do not block predictions.
- Production mode requires API-key authentication and non-wildcard CORS.
- Joblib artifacts must be treated as trusted files because Python serialization is
  not safe for arbitrary untrusted input.
