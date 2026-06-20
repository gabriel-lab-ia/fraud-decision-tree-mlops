# Contributing

Thanks for taking a look at this project. This repository is maintained as a
production-oriented MLOps portfolio project, so changes should keep the system
coherent, testable, and easy to review.

## Local Setup

```bash
uv venv --python 3.11
uv pip install -e ".[dev]"
```

## Quality Gates

Before opening a pull request, run the gates that match your change:

```bash
make lint
make typecheck
make security
make test
make docs
git diff --check
```

For model or training changes, also run:

```bash
make train-ci
```

For container changes, also run:

```bash
make docker-build
```

## Repository Hygiene

- Keep generated datasets, reports, model artifacts, MLflow state, caches, and local
  databases out of Git.
- Prefer small, intentional pull requests.
- Update tests when behavior changes.
- Update documentation when public workflows, API contracts, model governance, or
  operational behavior changes.
- Do not commit secrets or real transaction data.

## Commit Style

Use conventional commit prefixes such as:

- `feat:`
- `fix:`
- `docs:`
- `test:`
- `refactor:`
- `chore:`
