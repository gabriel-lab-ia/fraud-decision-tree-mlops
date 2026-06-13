from pathlib import Path

import numpy as np
import pandas as pd


def generate_synthetic_fraud_data(
    output_path: str | Path,
    n_samples: int = 5000,
    random_state: int = 42,
) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)

    transaction_amount = rng.lognormal(mean=4.0, sigma=1.0, size=n_samples)
    transaction_hour = rng.integers(0, 24, size=n_samples)
    customer_age_days = rng.integers(1, 3650, size=n_samples)
    num_previous_transactions = rng.poisson(lam=8, size=n_samples)
    merchant_risk_score = rng.uniform(0, 1, size=n_samples)
    device_risk_score = rng.uniform(0, 1, size=n_samples)

    fraud_probability = (
        0.015
        + 0.22 * (transaction_amount > 500)
        + 0.18 * ((transaction_hour >= 0) & (transaction_hour <= 5))
        + 0.22 * (merchant_risk_score > 0.75)
        + 0.22 * (device_risk_score > 0.80)
        + 0.16 * (customer_age_days < 30)
        + 0.12 * (num_previous_transactions <= 1)
    )

    fraud_probability = np.clip(fraud_probability, 0, 0.95)
    is_fraud = rng.binomial(1, fraud_probability)

    data = pd.DataFrame(
        {
            "transaction_amount": transaction_amount.round(2),
            "transaction_hour": transaction_hour,
            "customer_age_days": customer_age_days,
            "num_previous_transactions": num_previous_transactions,
            "merchant_risk_score": merchant_risk_score.round(4),
            "device_risk_score": device_risk_score.round(4),
            "is_fraud": is_fraud,
        }
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path, index=False)

    return data


def load_dataset(path: str | Path) -> pd.DataFrame:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at: {path}")

    return pd.read_csv(path)
