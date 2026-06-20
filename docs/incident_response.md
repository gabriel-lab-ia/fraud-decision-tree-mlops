# Incident Response

## Severity Examples

- Sev 1: API unavailable or producing invalid decisions.
- Sev 2: Telemetry outage, model readiness failures, or suspected artifact tamper.
- Sev 3: Documentation, dashboard, or non-blocking workflow failure.

## Response

1. Preserve logs, artifact manifest, model version, Git commit, and config.
2. Disable promotion or deployment automation for the affected model.
3. Roll back to the previous approved artifact when predictions are impacted.
4. Run `make quality-gates` and `make train-ci` before restoring normal release.
5. Document impact, root cause, corrective action, and prevention.
