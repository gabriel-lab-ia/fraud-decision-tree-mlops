import io
from urllib.error import HTTPError

import pytest

from scripts.demo_predict import (
    REQUIRED_RESPONSE_FIELDS,
    demo_transactions,
    validate_prediction_response,
)
from scripts.run_monitoring_summary import build_monitoring_summary
from scripts.telemetry_smoke_check import check_recent_telemetry


class EmptyCursor:
    def sort(self, *_args):
        return self

    def limit(self, *_args):
        return self

    def __iter__(self):
        return iter([])


class EmptyCollection:
    def count_documents(self, query):
        return 0

    def aggregate(self, pipeline):
        return []

    def find(self, *_args):
        return EmptyCursor()


class EmptyClient:
    def get_collection(self):
        return EmptyCollection()


def test_demo_transactions_are_realistic_and_valid():
    transactions = demo_transactions()
    assert len(transactions) == 3
    assert {item["transaction_id"] for item in transactions} == {
        "demo_low_risk",
        "demo_medium_risk",
        "demo_high_risk",
    }
    assert all(0 <= item["transaction_hour"] <= 23 for item in transactions)


def test_prediction_response_validation_catches_missing_fields():
    with pytest.raises(ValueError, match="missing fields"):
        validate_prediction_response({"transaction_id": "txn"})

    valid = dict.fromkeys(REQUIRED_RESPONSE_FIELDS)
    valid.update({"prediction": 0, "risk_score": 0.2})
    validate_prediction_response(valid)


def test_telemetry_smoke_treats_503_as_expected(monkeypatch):
    def unavailable(*_args, **_kwargs):
        raise HTTPError("url", 503, "offline", {}, io.BytesIO())

    monkeypatch.setattr("scripts.telemetry_smoke_check.urlopen", unavailable)
    assert check_recent_telemetry("http://test") == (False, [])


def test_monitoring_summary_handles_empty_store():
    assert build_monitoring_summary(EmptyClient()) == {
        "total_predictions": 0,
        "fraud_predictions": 0,
        "fraud_prediction_rate": 0.0,
        "average_risk_score": 0.0,
        "recent_predictions_count": 0,
    }
