# Data Sheet

## Source

The repository uses a deterministic synthetic transaction dataset when no raw CSV
is present. This is useful for repeatable engineering tests but is not
representative of real fraud behavior.

## Contract

Required raw columns are:

- `transaction_amount`
- `transaction_hour`
- `customer_age_days`
- `num_previous_transactions`
- `merchant_risk_score`
- `device_risk_score`
- `is_fraud`

Validation rejects missing required columns, unexpected columns, duplicate rows,
missing values, non-finite values, invalid ranges, non-binary targets, one-class
targets, and class counts below the configured minimum.

## Fingerprint

Training records a deterministic dataset fingerprint using sorted columns,
normalized records, and the data schema version. This supports model lineage and
artifact review.
