# Model Card

## Intended Use

This Decision Tree is an educational and portfolio baseline for fraud-risk scoring
and MLOps workflow demonstration. It is not approved for autonomous financial action.

## Inputs And Output

The model uses amount, hour, customer age, transaction history, merchant/device risk,
and five engineered features. It outputs a binary label, class probability, and the
decision threshold used for classification.

## Evaluation

Training records accuracy, balanced accuracy, precision, recall, specificity, F1,
F-beta, ROC-AUC, PR-AUC, MCC, false-positive rate, false-negative rate, Brier score,
log loss, confusion matrix, and baseline metrics. Promotion floors are configured in
`configs/train_config.yaml`.

## Risks

Synthetic data is not representative of real fraud patterns. Decision Trees can
overfit, probabilities may be poorly calibrated, and outcomes may vary across groups.
Human review, real-data validation, calibration, bias analysis, and drift monitoring
are required before any consequential use.
