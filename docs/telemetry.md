# Prediction Telemetry

Successful predictions attempt to write an event to MongoDB containing request ID,
transaction identity, raw request features, prediction, label, risk score, decision
threshold, model name/version, and UTC timestamp. In production, transaction IDs are
hashed before storage. Insert failures are logged as warnings and return a null event
ID; they do not fail inference.

`monitoring_queries.py` provides recent predictions, total prediction count, fraud
rate summary, and average risk score. The public recent-events endpoint returns HTTP
503 when the store is unavailable. Production deployments should add retention/index
policies, encryption, and access review for regulated transaction data.
