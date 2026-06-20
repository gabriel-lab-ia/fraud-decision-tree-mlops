# Responsible AI

This system produces fraud-risk scores and binary labels for demonstration
purposes. It is not approved for automated account blocking, transaction denial,
credit decisions, or law-enforcement escalation.

Required controls before consequential use:

- Human review for adverse actions.
- Real-world validation with representative data.
- Fairness analysis across legally and ethically relevant groups.
- Calibration checks and threshold review.
- Monitoring for drift, false negatives, false positives, and appeal outcomes.
- Clear customer-impact policy and audit logging.

The API intentionally returns model identity and decision threshold so downstream
systems can preserve decision context.
