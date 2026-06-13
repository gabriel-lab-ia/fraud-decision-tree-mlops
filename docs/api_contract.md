# API Contract

The FastAPI service exposes `GET /health`, `GET /ready`, `POST /predict`, and
`GET /telemetry/recent`. Interactive OpenAPI documentation is served at `/docs`.

`POST /predict` accepts a transaction ID plus six non-negative/range-validated raw
features. It returns the binary prediction, human label, fraud probability, model
identity, and nullable telemetry event ID. Unknown request fields are rejected.

`GET /ready` reports whether the configured joblib artifact can be loaded.
`GET /telemetry/recent?limit=20` accepts limits from 1 to 100 and returns HTTP 503
with a useful detail when MongoDB is unavailable.
