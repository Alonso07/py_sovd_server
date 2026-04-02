# Testing Guide

This guide covers testing for the SOVD Server.

## Running Tests

### All Tests
```bash
poetry run pytest tests/ -v
# or: make test
```

### With Coverage
```bash
poetry run pytest tests/ -v --cov=sovd_server --cov-report=term-missing
poetry run pytest tests/ --cov=sovd_server --cov-report=html
# or: make run-tests
```

### Specific test modules
```bash
poetry run pytest tests/test_config.py -v
poetry run pytest tests/test_endpoints.py -v
poetry run pytest tests/test_server.py -v
poetry run pytest tests/test_resource_response.py -v   # round-robin helpers (data, operations, faults, modes)
poetry run pytest tests/test_e2e_enhanced_round_robin.py -v  # Flask test_client against enhanced server
```

### Testing multiple Python versions

Use the Makefile targets (they create isolated venvs and run pytest):

```bash
make test-python310   # requires python3.10 on PATH
make test-python311   # requires python3.11 on PATH
make test-python312   # requires python3.12 on PATH
make test-versions    # runs tests for each installed 3.10/3.11/3.12
```

Install extra Python versions with [pyenv](https://github.com/pyenv/pyenv) or your OS packages (e.g. `deadsnakes` on Ubuntu).

### Security checks (bandit, safety)

```bash
poetry install   # includes dev deps (bandit, safety)
make security    # writes reports to reports/bandit-report.json, reports/safety-report.json
```

### Match CI locally

```bash
make ci-local     # lint, format-check, security, test
```

**Black:** GitHub Actions runs `black --check` only on the paths listed in `.github/workflows/ci.yml` (a subset of `src/` plus all of `tests/`). The Makefile’s `format` / `format-check` targets run Black on **all** of `src/` and `tests/`. For an exact match to CI before pushing, use the same file list as in the workflow, or rely on the `Check code formatting` step in CI.

**Commits that skip CI:** Pushes whose head commit message contains `[skip ci]` (for example automated version bumps) skip the lint/test jobs by design. See [VERSIONING.md](VERSIONING.md).

## Test layout

```
tests/
├── test_config.py                    # Configuration loading
├── test_endpoints.py                 # Smoke / import tests
├── test_server.py                    # Server behavior
├── test_server_config.py             # Server configuration
├── test_resource_response.py         # Round-robin response selection (unit)
├── test_e2e_enhanced_round_robin.py  # End-to-end: data, operations, faults, modes via Flask client
├── test_default_controller.py        # Optional; generated OpenAPI (often ignored in CI)
└── debug_*.py                        # Local debugging helpers (optional)
```

## CI/CD (GitHub Actions)

Workflow: `.github/workflows/ci.yml`.

Triggers:

- Push to `main` or `develop`
- Pull requests targeting `main` or `develop`

Jobs:

- **quick-checks** — flake8, Black (subset of files), bandit, safety; skipped when the pushed commit message contains `[skip ci]`
- **test** — pytest with coverage on Python 3.10–3.12 on Ubuntu, macOS, Windows; same `[skip ci]` rule
- **build** — on `main` only, builds wheel/sdist with `scripts/build_resolve_symlinks.sh` (skipped with `[skip ci]`)
- **semantic-release** — on `main` pushes only, after quick-checks and test succeed; runs **python-semantic-release** to bump version from conventional commits and push a tag (see [VERSIONING.md](VERSIONING.md))

Publishing to PyPI when a **version tag** `v*` is pushed: `.github/workflows/publish-pypi.yml` (requires `PYPI_TOKEN` secret). Documented in [DEPLOYMENT.md](DEPLOYMENT.md).

## Writing Tests

- Use pytest; place tests in `tests/` with names `test_*.py`.
- Use descriptive test names and docstrings.
- Prefer small, focused tests. Use fixtures for shared setup (e.g. client, config).

Example:
```python
def test_health_endpoint_returns_ok(client):
    """Health endpoint returns 200."""
    response = client.get("/health")
    assert response.status_code == 200
```

## Troubleshooting

- **Import errors**: Run tests from project root and ensure dependencies are installed (`poetry install`).
- **Config not found**: Tests that load config assume paths relative to `src/sovd_server/config/`; run from repo root.
- **Port in use**: Endpoint tests may start a server; use a free port or mock the server where possible.
