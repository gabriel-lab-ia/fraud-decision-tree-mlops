# Threat Model

## Assets

- API availability.
- Model artifact integrity.
- Telemetry data.
- MLflow training metadata.
- Configuration and API keys.

## Primary Risks

- Unauthorized prediction requests.
- Tampered or stale model artifacts.
- Leakage of transaction identifiers in production telemetry.
- Poisoned training data.
- Overly broad CORS policy.
- Accidental commit of datasets, model files, databases, reports, or secrets.

## Mitigations

- API-key gate for production.
- Manifest hash validation for artifacts.
- Production hashing of transaction IDs in telemetry.
- Dataset contract validation and deterministic fingerprints.
- `.gitignore` and `.dockerignore` exclusions for generated artifacts.
- CI lint, tests, type checks, Bandit scan, docs build, and model validation.
