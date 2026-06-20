import pandas as pd

from fraud_detection.data.contract import validate_dataset_contract
from fraud_detection.data.schemas import FEATURE_COLUMNS, TARGET_COLUMN


def validate_training_data(data: pd.DataFrame) -> None:
    validate_dataset_contract(data[[*FEATURE_COLUMNS, TARGET_COLUMN]])
