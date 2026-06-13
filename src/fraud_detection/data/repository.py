from __future__ import annotations

from pathlib import Path

import pandas as pd

from fraud_detection.data.load_data import generate_synthetic_fraud_data
from fraud_detection.data.validation import validate_training_data


class TransactionDataRepository:
    def __init__(self, raw_path: str | Path, processed_path: str | Path) -> None:
        self.raw_path = Path(raw_path)
        self.processed_path = Path(processed_path)

    def load_raw(self) -> pd.DataFrame:
        if not self.raw_path.exists():
            raise FileNotFoundError(f"Raw dataset not found at: {self.raw_path}")

        return pd.read_csv(self.raw_path)

    def load_or_generate_raw(self, n_samples: int, random_state: int) -> pd.DataFrame:
        if not self.raw_path.exists():
            self.raw_path.parent.mkdir(parents=True, exist_ok=True)

            return generate_synthetic_fraud_data(
                output_path=self.raw_path,
                n_samples=n_samples,
                random_state=random_state,
            )

        return self.load_raw()

    def save_processed(self, data: pd.DataFrame) -> None:
        self.processed_path.parent.mkdir(parents=True, exist_ok=True)
        data.to_csv(self.processed_path, index=False)

    def load_processed(self) -> pd.DataFrame:
        if not self.processed_path.exists():
            raise FileNotFoundError(
                f"Processed dataset not found at: {self.processed_path}"
            )

        return pd.read_csv(self.processed_path)

    def validate_raw(self, data: pd.DataFrame) -> None:
        validate_training_data(data)
