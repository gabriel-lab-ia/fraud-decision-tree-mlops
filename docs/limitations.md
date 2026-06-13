# Limitations

- The default dataset is synthetic and encodes simplified fraud rules.
- There is no production identity/authentication layer or rate limiting.
- MongoDB telemetry has no configured retention, redaction, or schema migration.
- Monitoring modules are extension points; automated drift alerts are not implemented.
- The local artifact is not a governed model registry promotion mechanism.
- The Decision Tree probability is not calibrated.
- Docker Compose is intended for local development, not resilient production hosting.

Before production use, validate on representative labeled data, define costs and
decision thresholds, add security controls, perform fairness analysis, and establish
retraining, rollback, and incident-response procedures.
