# Versioning

This project follows [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH).

## Where the version is defined

- **Source of truth for packaging**: `pyproject.toml` → `[tool.poetry]` → `version`.
- **Runtime**: `src/sovd_server/__init__.py` → `__version__` (updated together with the above).

## Automated releases (GitHub Actions)

On every **push to `main`** that passes CI, the **Semantic release** job runs **after** lint and tests. It uses [python-semantic-release](https://python-semantic-release.readthedocs.io/) with [conventional commits](https://www.conventionalcommits.org/):

| Commit type | Example | Version bump |
|-------------|---------|--------------|
| Breaking change | `feat!: remove old API` or footer `BREAKING CHANGE:` | **major** |
| Feature | `feat: add round-robin modes` | **minor** |
| Fix / perf | `fix: handle empty body` or `perf: ...` | **patch** |
| Other | `chore:`, `docs:`, `ci:`, `style:`, … | **no** release* |

\*By default, `chore`/`docs`/etc. do not trigger a new version unless there are releasable commits since the last tag.

The job updates `pyproject.toml` and `__init__.py`, commits with `[skip ci]` (so the normal CI workflow does not loop), creates a tag like `v1.2.0`, and pushes. **Changelog file generation is disabled** in CI (`--no-changelog`); you can still maintain `docs/CHANGELOG.md` by hand if you want.

### PyPI

When a **version tag** is pushed (e.g. `v1.2.0`), [.github/workflows/publish-pypi.yml](../.github/workflows/publish-pypi.yml) builds the wheel/sdist and uploads to PyPI. Configure the repository secret **`PYPI_TOKEN`** (PyPI API token) under **Settings → Secrets and variables → Actions**.

## Manual release (without automation)

1. Decide the version (e.g. `1.1.0`).
2. Update version: `poetry version 1.1.0` (or edit `pyproject.toml` and `__init__.py`).
3. Optionally edit `docs/CHANGELOG.md`.
4. Commit and tag: `git tag -a v1.1.0 -m "Release 1.1.0"`, then `git push origin main && git push origin v1.1.0`.
5. Build and publish: `./scripts/publish/publish_to_pypi.sh` or `make build` + `twine upload dist/*`.

## Version numbering rules

- **MAJOR**: Incompatible API or config changes.
- **MINOR**: New features, backward compatible.
- **PATCH**: Bug fixes, backward compatible.

## Checking the current version locally

```bash
make version
```

Or:

```bash
poetry version -s
grep '^version = ' pyproject.toml
```

## Preview next version locally

```bash
poetry run semantic-release --noop version --print
```

Requires git history and tags; does not change files.
