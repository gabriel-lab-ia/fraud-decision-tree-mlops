import json
import os
import sys
import time
from typing import Any, cast
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from scripts.demo_predict import demo_transactions, post_prediction


def get_json(url: str) -> dict[str, Any]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP(S) API URLs are supported.")
    with urlopen(url, timeout=5) as response:  # nosec B310
        return cast(dict[str, Any], json.load(response))


def post_json(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP(S) API URLs are supported.")
    request = Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "x-request-id": "e2e-smoke"},
        method="POST",
    )
    with urlopen(request, timeout=5) as response:  # nosec B310
        return cast(dict[str, Any], json.load(response))


def wait_ready(base_url: str, timeout_seconds: int = 30) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            payload = get_json(f"{base_url}/health/ready")
            if payload.get("model_loaded"):
                return
        except (HTTPError, URLError, TimeoutError):
            time.sleep(1)
    raise TimeoutError("API did not become ready before timeout.")


def main() -> int:
    base_url = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")
    try:
        wait_ready(base_url)
        predictions = [
            post_prediction(f"{base_url}/v1", item) for item in demo_transactions()
        ]
        batch = post_json(
            f"{base_url}/v1/predict/batch",
            {"transactions": demo_transactions()},
        )
        metrics_url = f"{base_url}/metrics"
        metrics_parsed = urlparse(metrics_url)
        if metrics_parsed.scheme not in {"http", "https"}:
            raise ValueError("Only HTTP(S) API URLs are supported.")
        metrics = (
            urlopen(  # nosec B310
                metrics_url,
                timeout=5,
            )
            .read()
            .decode()
        )
        if len(batch["predictions"]) != len(predictions):
            raise ValueError("Batch prediction count does not match demo count.")
        if "fraud_api_info" not in metrics:
            raise ValueError("Prometheus metrics output is missing fraud_api_info.")
    except Exception as exc:
        print(f"E2E smoke test failed: {exc}", file=sys.stderr)
        return 1
    print("E2E smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
