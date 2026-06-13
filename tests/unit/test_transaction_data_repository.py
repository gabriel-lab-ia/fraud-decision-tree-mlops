import pandas as pd
import pytest

from fraud_detection.data.repository import TransactionDataRepository


def test_repository_load_raw_raises_when_file_does_not_exist(tmp_path):
    repository = TransactionDataRepository(
        raw_path=tmp_path / "missing.csv",
        processed_path=tmp_path / "processed.csv",
    )

    with pytest.raises(FileNotFoundError):
        repository.load_raw()


def test_repository_save_and_load_processed_dataset(tmp_path):
    repository = TransactionDataRepository(
        raw_path=tmp_path / "raw.csv",
        processed_path=tmp_path / "processed.csv",
    )

    data = pd.DataFrame(
        {
            "transaction_amount": [100, 200],
            "transaction_hour": [10, 20],
            "is_fraud": [0, 1],
        }
    )

    repository.save_processed(data)
    loaded = repository.load_processed()

    assert loaded.shape == data.shape
    assert list(loaded.columns) == list(data.columns)
    assert loaded["transaction_amount"].tolist() == [100, 200]


def test_repository_generates_raw_dataset_when_missing(tmp_path):
    repository = TransactionDataRepository(
        raw_path=tmp_path / "sample" / "synthetic_fraud.csv",
        processed_path=tmp_path / "processed" / "fraud_processed.csv",
    )

    data = repository.load_or_generate_raw(n_samples=100, random_state=42)

    assert repository.raw_path.exists()
    assert len(data) == 100
    assert "is_fraud" in data.columns
    assert "transaction_amount" in data.columns
