from fraud_detection.data.load_data import generate_synthetic_fraud_data
from fraud_detection.data.schemas import TARGET_COLUMN
from fraud_detection.data.validation import validate_training_data


def test_generate_synthetic_fraud_data_creates_valid_dataset(tmp_path):
    output_path = tmp_path / "synthetic_fraud.csv"

    data = generate_synthetic_fraud_data(
        output_path=output_path,
        n_samples=200,
        random_state=42,
    )

    assert output_path.exists()
    assert TARGET_COLUMN in data.columns
    assert set(data[TARGET_COLUMN].unique()).issubset({0, 1})

    validate_training_data(data)
