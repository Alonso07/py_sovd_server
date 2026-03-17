# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2025-03-16

### Changed
- Migrated project to Poetry (pyproject.toml, poetry.lock; removed setup.py)
- CI: use Poetry for install/build; fixed Windows (bash shell for poetry steps)
- Build: resolve symlinks before packaging for wheel/sdist
- Docs and README updated for Poetry workflow

### Added
- `make build` and `scripts/build_resolve_symlinks.sh` for distribution builds
- Documentation (INDEX, CONFIGURATION, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, TESTING, DEPLOYMENT)
- GitHub Actions CI workflow (lint, test, security checks)
- Dependabot configuration, issue/PR templates

## [1.0.0] - (initial release)

### Added
- SOVD server implementation based on ISO/DIS 17978-3:2025
- Hierarchical YAML configuration (gateway, entities, resources)
- RESTful API with areas, components, apps, data, operations, faults, modes
- Flask/Connexion server with OpenAPI
- Configuration loader and enhanced server with YAML support

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security: [SECURITY.md](SECURITY.md).
