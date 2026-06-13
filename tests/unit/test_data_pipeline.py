from fraud_detection.data.pipeline import build_training_dataset
from fraud_detection.data.repository import TransactionDataRepository
from fraud_detection.data.schemas import ENGINEERED_FEATURE_COLUMNS, TARGET_COLUMN


def test_build_training_dataset_creates_processed_dataset_with_engineered_features(
    tmp_path,
):
    repository = TransactionDataRepository(
        raw_path=tmp_path / "sample" / "synthetic_fraud.csv",
        processed_path=tmp_path / "processed" / "fraud_processed.csv",
    )

    data = build_training_dataset(
        repository=repository,
        n_samples=100,
        random_state=42,
    )

    assert repository.raw_path.exists()
    assert repository.processed_path.exists()
    assert TARGET_COLUMN in data.columns

    for column in ENGINEERED_FEATURE_COLUMNS:
        assert column in data.columns
