# API Contract

The FastAPI service exposes versioned endpoints:

- `GET /health/live`
- `GET /health/ready`
- `GET /version`
- `GET /metrics`
- `POST /v1/predict`
- `POST /v1/predict/batch`
- `GET /v1/telemetry/recent`
- `GET /v1/monitoring/summary`

Interactive OpenAPI documentation is served at `/docs`.

`POST /predict` accepts a transaction ID plus six non-negative/range-validated raw
features. It returns the binary prediction, human label, fraud probability,
decision threshold, model identity, request ID, artifact schema version, and
nullable telemetry event ID. Unknown request fields are rejected.

`GET /health/ready` reports whether the configured joblib artifact and manifest can
be loaded. `GET /v1/telemetry/recent?limit=20` accepts limits from 1 to 100 and
returns HTTP 503 with a useful detail when MongoDB is unavailable.
