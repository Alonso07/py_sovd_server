# Testing Guide

This guide covers testing for the SOVD Server.

## Running Tests

### All Tests
```bash
pytest tests/ -v
# or
make test
```

### With Coverage
```bash
pytest tests/ -v --cov=sovd_server --cov-report=term-missing
pytest tests/ --cov=sovd_server --cov-report=html
```

### Specific Test Files
```bash
pytest tests/test_config.py -v
pytest tests/test_endpoints.py -v
pytest tests/test_server.py -v
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
make install-dev   # installs dev + bandit, safety
make security     # writes reports to reports/bandit-report.json, reports/safety-report.json
```

### Simulate CI locally

```bash
make ci-local     # lint, format-check, security, test
```

## Test Structure

```
tests/
├── test_config.py         # Configuration loading tests
├── test_endpoints.py      # API endpoint tests
├── test_server.py         # Server behavior tests
├── test_server_config.py  # Server configuration tests
├── test_default_controller.py
└── debug_*.py             # Debug utilities (optional)
```

## CI/CD

Tests run automatically on:
- Push to `main` and `develop`
- Pull requests targeting `main` and `develop`

The CI workflow runs:
- Linting (flake8)
- Format check (black)
- Security checks (bandit, safety)
- Full test suite with coverage

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

- **Import errors**: Run tests from project root and ensure the package is installed (`pip install -e .`).
- **Config not found**: Tests that load config assume paths relative to `src/sovd_server/config/`; run from repo root.
- **Port in use**: Endpoint tests may start a server; use a free port or mock the server where possible.
