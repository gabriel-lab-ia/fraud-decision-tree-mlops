from __future__ import annotations

import pandas as pd

from fraud_detection.data.cleaning import clean_transaction_data
from fraud_detection.data.repository import TransactionDataRepository
from fraud_detection.features.feature_engineering import add_engineered_features


def build_training_dataset(
    repository: TransactionDataRepository,
    n_samples: int,
    random_state: int,
) -> pd.DataFrame:
    raw_data = repository.load_or_generate_raw(
        n_samples=n_samples,
        random_state=random_state,
    )

    cleaned_data = clean_transaction_data(raw_data)

    repository.validate_raw(cleaned_data)

    engineered_data = add_engineered_features(cleaned_data)

    repository.save_processed(engineered_data)

    return engineered_data
