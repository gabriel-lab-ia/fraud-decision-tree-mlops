# Drift Detection

The v0.3 monitoring module includes Population Stability Index (PSI) helpers.
PSI compares a reference distribution from training with a new production window.

Default interpretation:

- `< 0.10`: stable
- `0.10` to `< 0.25`: moderate drift
- `>= 0.25`: significant drift

Recommended production workflow:

1. Store reference feature profiles after model approval.
2. Compute PSI for each feature on a scheduled cadence.
3. Alert on significant drift for high-impact features.
4. Review telemetry volume, data-quality errors, and model metrics together.
5. Retrain only after data and label quality are understood.
