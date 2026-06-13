# Prediction Telemetry

Successful predictions attempt to write an event to MongoDB containing transaction
ID, raw request features, prediction, label, risk score, model name/version, and UTC
timestamp. Insert failures are logged as warnings and return a null event ID; they do
not fail inference.

`monitoring_queries.py` provides recent predictions, total prediction count, fraud
rate summary, and average risk score. The public recent-events endpoint returns HTTP
503 when the store is unavailable. Production deployments should add authentication,
retention/index policies, encryption, and redaction for regulated transaction data.
