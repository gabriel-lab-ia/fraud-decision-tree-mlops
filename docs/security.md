# Security

## Runtime Controls

- Production mode requires API-key authentication.
- Production mode rejects wildcard CORS origins.
- Secrets are loaded from environment variables and redacted from safe config dumps.
- Container runtime uses a non-root user.
- Generated datasets, databases, model artifacts, reports, caches, and secrets are
  excluded from Git and Docker build context.

## Artifact Safety

The serving loader validates artifact schema and SHA-256 manifest before use.
Because sklearn/joblib artifacts rely on Python serialization, only artifacts
created by the governed training workflow should be deployed.

## Gates

Run these before commit or release:

```bash
make lint
make typecheck
make security
make test
git diff --check
```
