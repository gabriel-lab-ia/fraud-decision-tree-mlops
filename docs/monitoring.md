# Monitoring

Prediction events capture transaction features, prediction, label, risk score, model
identity, and UTC timestamp. The monitoring summary reports total predictions, fraud
prediction count/rate, average risk score, and recent event count.

Data-quality utilities count missing values, flag invalid numeric ranges, and summarize
transaction amounts. Performance utilities summarize risk scores and predicted-class
distribution. These functions are pure and suitable for scheduled jobs or dashboards.

The v0.3 drift helper computes PSI against a reference distribution. Production
monitoring should still add scheduled windows, alert delivery, latency/error
telemetry, and labeled-outcome performance monitoring.
