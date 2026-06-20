# Deployment

## Local

```bash
make train
make validate
make api
```

## Docker Compose

```bash
make train
docker compose up --build
```

The API expects:

- `MODEL_PATH`
- `MODEL_MANIFEST_PATH`
- `MONGO_URI`
- `APP_ENV`
- `ENABLE_API_KEY_AUTH`
- `API_KEY` when auth is enabled

Use `APP_ENV=production`, `ENABLE_API_KEY_AUTH=true`, a strong `API_KEY`, and
specific `CORS_ALLOW_ORIGINS` for production deployments.
