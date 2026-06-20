## Summary

- Add a concise description of the change.

## Change Type

- [ ] Feature
- [ ] Fix
- [ ] Refactor
- [ ] Documentation
- [ ] Tests
- [ ] CI/CD
- [ ] Model or data pipeline

## Validation

- [ ] `make lint`
- [ ] `make typecheck`
- [ ] `make security`
- [ ] `make test`
- [ ] `make docs`
- [ ] `make train-ci` if training, model, or data behavior changed
- [ ] `make docker-build` if Docker/runtime behavior changed
- [ ] `git diff --check`

## Data, Artifact, And Secret Hygiene

- [ ] No datasets, model artifacts, reports, MLflow state, caches, local databases, or
      secrets are included.
- [ ] Any generated output is ignored or intentionally documented.

## Notes

- Add reviewer notes, screenshots, or operational context when useful.
