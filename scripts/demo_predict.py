import json
import os
import sys
from typing import Any, cast
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

REQUIRED_RESPONSE_FIELDS = {
    "transaction_id",
    "prediction",
    "label",
    "risk_score",
    "decision_threshold",
    "model_name",
    "model_version",
    "telemetry_event_id",
}


def demo_transactions() -> list[dict[str, Any]]:
    return [
        {
            "transaction_id": "demo_low_risk",
            "transaction_amount": 5.00,
            "transaction_hour": 10,
            "customer_age_days": 365,
            "num_previous_transactions": 10,
            "merchant_risk_score": 0.01,
            "device_risk_score": 0.01,
        },
        {
            "transaction_id": "demo_medium_risk",
            "transaction_amount": 280.00,
            "transaction_hour": 21,
            "customer_age_days": 120,
            "num_previous_transactions": 5,
            "merchant_risk_score": 0.52,
            "device_risk_score": 0.60,
        },
        {
            "transaction_id": "demo_high_risk",
            "transaction_amount": 1250.00,
            "transaction_hour": 2,
            "customer_age_days": 7,
            "num_previous_transactions": 0,
            "merchant_risk_score": 0.94,
            "device_risk_score": 0.91,
        },
    ]


def validate_prediction_response(payload: dict[str, Any]) -> None:
    missing = REQUIRED_RESPONSE_FIELDS - set(payload)
    if missing:
        raise ValueError(f"Prediction response missing fields: {sorted(missing)}")
    if payload["prediction"] not in {0, 1}:
        raise ValueError("Prediction must be 0 or 1.")
    if not 0 <= float(payload["risk_score"]) <= 1:
        raise ValueError("Risk score must be between 0 and 1.")


def post_prediction(base_url: str, transaction: dict[str, Any]) -> dict[str, Any]:
    parsed = urlparse(base_url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP(S) API URLs are supported.")
    request = Request(
        f"{base_url.rstrip('/')}/predict",
        data=json.dumps(transaction).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=5) as response:  # nosec B310
        payload = json.load(response)
    payload = cast(dict[str, Any], payload)
    validate_prediction_response(payload)
    return payload


def format_results(results: list[dict[str, Any]]) -> str:
    header = f"{'Transaction':<20} {'Label':<12} {'Risk':>7} {'Telemetry':<12}"
    rows = [
        f"{row['transaction_id']:<20} {row['label']:<12} "
        f"{float(row['risk_score']):>7.3f} "
        f"{'stored' if row['telemetry_event_id'] else 'fail-soft':<12}"
        for row in results
    ]
    return "\n".join([header, "-" * len(header), *rows])


def main() -> int:
    base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
    try:
        results = [
            post_prediction(f"{base_url.rstrip('/')}/v1", item)
            for item in demo_transactions()
        ]
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        print(f"Inference demo failed: {exc}", file=sys.stderr)
        return 1
    print(format_results(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
