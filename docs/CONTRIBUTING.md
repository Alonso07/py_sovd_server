# Contributing to SOVD Server

Thank you for your interest in contributing to the SOVD Server project. This document provides guidelines for contributors.

## Quick start

### Prerequisites
- Python 3.9+
- [Poetry](https://python-poetry.org/docs/#installation)
- Git

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/sovd_server.git
   cd sovd_server
   ```

2. **Install dependencies** (Poetry creates the virtual environment)
   ```bash
   poetry install
   # or: make install
   ```

3. **Run tests to verify setup**
   ```bash
   poetry run pytest tests/ -v
   # or: make test
   ```

4. **Start the server for testing**
   ```bash
   poetry run sovd-server
   # or: make run-server
   ```

## Development workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 2. Make Your Changes
- Follow the coding standards (see below)
- Add tests for new functionality
- Update documentation if needed

### 3. Test your changes
```bash
poetry run pytest tests/ -v
poetry run pytest tests/ --cov=sovd_server --cov-report=term-missing
```

### 4. Code quality checks
```bash
poetry run flake8 src/ tests/
# Black: CI checks specific paths — see .github/workflows/ci.yml "Check code formatting"
poetry run black --check --diff \
  src/sovd_server/config_loader.py \
  src/sovd_server/enhanced_server.py \
  src/sovd_server/fault_builder.py \
  src/sovd_server/run_enhanced_server.py \
  src/sovd_server/__init__.py \
  src/sovd_server/parse_pdf.py \
  src/sovd_server/resource_response.py \
  tests/
# or: make format-check   (formats all of src/ + tests/ — broader than CI)
```

### 5. Commit and push

Use [Conventional Commits](https://www.conventionalcommits.org/) so automated releases can derive the next version on `main` (see [VERSIONING.md](VERSIONING.md)):

- `feat:` — new feature (typically minor version)
- `fix:` / `perf:` — fix or performance (typically patch)
- `feat!:` or `BREAKING CHANGE:` — incompatible change (major)

```bash
git add .
git commit -m "feat: add new feature description"
git push origin feature/your-feature-name
```

### 6. Create Pull Request
- Use the provided PR template
- Reference any related issues
- Ensure CI checks pass

## Coding standards

### Python style
- Follow PEP 8
- Use Black for formatting (`pyproject.toml`); align with CI’s checked paths when possible
- Use type hints where appropriate
- Write docstrings for public functions and classes

### Testing
- New features should include tests
- Use pytest; place tests in `tests/`
- Use descriptive test names

## Documentation

- Update README.md for user-facing changes
- Update docs/ for configuration or API changes
- Use docstrings for code (Google or NumPy style)

## Bug reports

When reporting bugs, please include:
1. Clear description and steps to reproduce
2. Expected vs actual behavior
3. Environment (OS, Python version)
4. Configuration/logs (with sensitive data removed)

Use the bug report template in `.github/ISSUE_TEMPLATE/bug_report.md`.

## Feature requests

Use the feature request template in `.github/ISSUE_TEMPLATE/feature_request.md`.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
