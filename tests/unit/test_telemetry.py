from fraud_detection.telemetry.event_logger import (
    build_prediction_event,
    log_prediction_event,
)


class BrokenClient:
    def get_collection(self):
        raise ConnectionError("offline")


def test_build_prediction_event_contains_monitoring_fields():
    event = build_prediction_event(
        "txn_1",
        {"transaction_amount": 100.0},
        {
            "prediction": 1,
            "label": "fraud",
            "risk_score": 0.9,
            "model_name": "tree",
            "model_version": "0.1.0",
        },
    )
    assert event["transaction_id"] == "txn_1"
    assert event["request_features"]["transaction_amount"] == 100.0
    assert event["timestamp"].tzinfo is not None


def test_log_prediction_event_fails_softly():
    assert log_prediction_event(BrokenClient(), {}) is None
