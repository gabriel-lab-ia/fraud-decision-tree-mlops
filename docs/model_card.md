# Model Card

## Intended Use

This Decision Tree is an educational and portfolio baseline for fraud-risk scoring
and MLOps workflow demonstration. It is not approved for autonomous financial action.

## Inputs And Output

The model uses amount, hour, customer age, transaction history, merchant/device risk,
and five engineered features. It outputs a binary label and class probability.

## Evaluation

Training records accuracy, precision, recall, F1, and ROC-AUC on a stratified holdout.
Promotion floors are recall 0.50, F1 0.35, and ROC-AUC 0.60.

## Risks

Synthetic data is not representative of real fraud patterns. Decision Trees can
overfit, probabilities may be poorly calibrated, and outcomes may vary across groups.
Human review, real-data validation, calibration, bias analysis, and drift monitoring
are required before any consequential use.
