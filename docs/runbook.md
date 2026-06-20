# Runbook

## Model Not Ready

1. Check `GET /health/ready`.
2. Confirm `MODEL_PATH` and `MODEL_MANIFEST_PATH`.
3. Re-run `make train && make validate`.
4. Confirm the manifest SHA-256 matches the artifact.
5. Restart the API.

## Telemetry Unavailable

Prediction remains fail-soft. Check MongoDB health, `MONGO_URI`, network access,
and recent `/v1/telemetry/recent` responses.

## Bad Metrics

Inspect `reports/metrics.json`, `reports/data_quality_report.json`, MLflow runs,
threshold strategy, class balance, and dataset fingerprint changes. Do not promote
a model that fails validation gates.

## Rollback

Restore the previous approved model artifact and manifest together, then restart
the API and verify `/health/ready`, `/version`, and a known prediction request.
