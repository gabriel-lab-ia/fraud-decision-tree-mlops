OBSERVABILITY_SCRIPTS = scripts/demo_predict.py scripts/telemetry_smoke_check.py scripts/run_monitoring_summary.py scripts/export_model_explainability.py scripts/e2e_smoke_test.py
PYTHON_TARGETS = src tests scripts/run_training.py scripts/run_api.py scripts/validate_model.py $(OBSERVABILITY_SCRIPTS)

.PHONY: help venv install lint format typecheck security test test-unit test-integration test-contract coverage train train-ci validate evaluate drift-check api demo e2e telemetry-smoke monitoring-summary explain docker-build docker-up docker-down docker-smoke mlflow docs docs-serve clean all quality-gates

help:
	@echo "Available commands:"
	@echo "  make install        - Install project dependencies"
	@echo "  make lint           - Run Ruff and Black checks"
	@echo "  make format         - Auto-format code"
	@echo "  make typecheck      - Run mypy"
	@echo "  make security       - Run Bandit security scan"
	@echo "  make test           - Run all tests"
	@echo "  make coverage       - Run tests with coverage"
	@echo "  make train          - Train model and write governed artifacts"
	@echo "  make validate       - Validate model metrics against gates"
	@echo "  make drift-check    - Run PSI drift example check"
	@echo "  make api            - Run FastAPI app"
	@echo "  make demo           - Send demo transactions to the API"
	@echo "  make e2e            - Run API smoke test against a live service"
	@echo "  make docker-build   - Build production container"
	@echo "  make docker-up      - Start Docker Compose services"
	@echo "  make docker-smoke   - Smoke test the Compose API"
	@echo "  make docs           - Build documentation"

venv:
	uv venv .venv --python 3.11

install:
	uv pip install -e ".[dev]"

lint:
	uv run ruff check .
	uv run ruff format --check .
	uv run black --check $(PYTHON_TARGETS)

format:
	uv run ruff check . --fix
	uv run ruff format .
	uv run black $(PYTHON_TARGETS)

typecheck:
	uv run mypy src scripts

security:
	uv run bandit -q -r src scripts -x tests

test:
	uv run pytest

test-unit:
	uv run pytest tests/unit

test-integration:
	uv run pytest tests/integration

test-contract:
	uv run pytest tests/contract

coverage:
	uv run pytest --cov=fraud_detection --cov-report=term-missing --cov-fail-under=85

train:
	uv run python scripts/run_training.py

train-ci: train validate

validate:
	uv run python scripts/validate_model.py

evaluate: validate

drift-check:
	uv run python -m fraud_detection.monitoring.drift

api:
	uv run python scripts/run_api.py

demo:
	uv run python scripts/demo_predict.py

e2e:
	uv run python scripts/e2e_smoke_test.py

telemetry-smoke:
	uv run python scripts/telemetry_smoke_check.py

monitoring-summary:
	uv run python scripts/run_monitoring_summary.py

explain:
	uv run python scripts/export_model_explainability.py

docker-build:
	docker build -t fraud-decision-tree-mlops:local .

docker-up:
	docker compose up --build

docker-down:
	docker compose down

docker-smoke:
	BASE_URL=http://localhost:8000 uv run python scripts/e2e_smoke_test.py

mlflow:
	uv run mlflow ui --host 0.0.0.0 --port 5000

docs:
	uv run mkdocs build --strict

docs-serve:
	uv run mkdocs serve

quality-gates: lint typecheck security test

all: quality-gates train-ci

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
