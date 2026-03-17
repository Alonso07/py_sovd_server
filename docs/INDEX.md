# Documentation Index

This is the main index for all SOVD Server documentation.

## 📚 Core Documentation

### [README.md](../README.md)
Main project overview with quick start guide, features, and basic usage.

### [CONFIGURATION.md](CONFIGURATION.md)
Configuration guide covering:
- Gateway configuration (sovd_gateway.yaml)
- Entity configurations (areas, components, apps)
- Resource configurations (data, operations, faults, modes)
- Troubleshooting and best practices

### [TESTING.md](TESTING.md)
Testing guide covering:
- Test suite overview
- Running tests (unit, config, endpoints)
- Test structure and CI

### [DEPLOYMENT.md](DEPLOYMENT.md)
Deployment and CI/CD guide including:
- Local and production deployment
- Docker deployment
- GitHub Actions CI
- Development workflow

## 🤝 Community & Project Management

### [CONTRIBUTING.md](CONTRIBUTING.md)
Contributor guide including:
- Development setup and workflow
- Coding standards and testing requirements
- Pull request process
- Issue reporting guidelines

### [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
Community standards and guidelines.

### [CHANGELOG.md](CHANGELOG.md)
Project changelog and release notes.

### [SECURITY.md](SECURITY.md)
Security policy and vulnerability reporting.

### [VERSIONING.md](VERSIONING.md)
How we version the project and cut releases (semver, pyproject.toml, tags).

## 🏗️ Configuration Structure

```
src/sovd_server/config/
├── sovd_gateway.yaml    # Gateway configuration
├── entities/            # Entity configurations
│   ├── areas.yaml
│   ├── components.yaml
│   └── apps.yaml
└── resources/           # Resource configurations
    ├── data/
    ├── operations/
    ├── faults/
    └── modes/
```

## 🚀 Quick Start

### Installation (Poetry)
```bash
poetry install
# or: make install
```

### Start Server
```bash
poetry run sovd-server
# or: make run-server
```

### Run Tests
```bash
poetry run pytest tests/ -v
# or: make test
```

### Test multiple Python versions locally
```bash
make test-python310   # Python 3.10 only
make test-python311   # Python 3.11 only
make test-python312   # Python 3.12 only
make test-versions    # all installed 3.10/3.11/3.12
```
Install extra Python versions with [pyenv](https://github.com/pyenv/pyenv) or your OS package manager (e.g. `deadsnakes` on Ubuntu).

### Run security checks
```bash
make install-dev      # installs bandit, safety
make security         # writes reports to reports/
```

### Full CI pipeline locally
```bash
make ci-local         # lint, format-check, security, test
```

### Show current version
```bash
make version
```

## 📖 Documentation Navigation

- **Users**: Start with [README.md](../README.md) → [CONFIGURATION.md](CONFIGURATION.md)
- **Developers**: [CONTRIBUTING.md](CONTRIBUTING.md) → [TESTING.md](TESTING.md)
- **DevOps**: [DEPLOYMENT.md](DEPLOYMENT.md)
