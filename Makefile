.PHONY: help venv install lint format test train api validate docker-up docker-down mlflow clean

help:
	@echo "Available commands:"
	@echo "  make venv        - Create local .venv with uv"
	@echo "  make install     - Install project dependencies"
	@echo "  make lint        - Run ruff and black checks"
	@echo "  make format      - Auto-format code"
	@echo "  make test        - Run tests"
	@echo "  make train       - Train model"
	@echo "  make validate    - Validate model metrics"
	@echo "  make api         - Run FastAPI app"
	@echo "  make docker-up   - Start Docker Compose services"
	@echo "  make docker-down - Stop Docker Compose services"
	@echo "  make mlflow      - Run MLflow UI"

venv:
	uv venv .venv --python 3.11

install:
	uv pip install -e ".[dev]"

lint:
	uv run ruff check src tests
	uv run black --check src tests

format:
	uv run ruff check src tests --fix
	uv run black src tests

test:
	uv run pytest

train:
	uv run python scripts/run_training.py

api:
	uv run python scripts/run_api.py

validate:
	uv run python scripts/validate_model.py

docker-up:
	docker compose up --build

docker-down:
	docker compose down

mlflow:
	uv run mlflow ui --host 0.0.0.0 --port 5000

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
