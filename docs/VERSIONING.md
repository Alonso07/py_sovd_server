# Versioning

This project follows [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH) and [Keep a Changelog](https://keepachangelog.com/).

## Where the version is defined

- **Single source of truth**: `pyproject.toml` → `[project]` → `version = "1.0.0"`.
- **Keep in sync** (if you still ship with setuptools): `setup.py` → `version="1.0.0"` in the `setup()` call.

When releasing, update the version in both places so that `pip install .` and built wheels report the same version.

## How to release a new version

1. **Decide the version** (e.g. `1.1.0` for a new feature, `1.0.1` for a fix).
2. **Update version**:
   - In `pyproject.toml`: `version = "1.1.0"`.
   - In `setup.py`: `version="1.1.0"`.
3. **Update changelog**: Edit `docs/CHANGELOG.md` (move items from `[Unreleased]` to `[1.1.0]`, add date).
4. **Commit**: e.g. `git commit -am "chore: release 1.1.0"`.
5. **Tag**: `git tag -a v1.1.0 -m "Release 1.1.0"`.
6. **Push**: `git push origin main && git push origin v1.1.0`.
7. **Build and publish** (if you use PyPI):
   - `python -m build`
   - `twine upload dist/*`

## Version numbering rules

- **MAJOR**: Incompatible API or config changes.
- **MINOR**: New features, backward compatible.
- **PATCH**: Bug fixes, backward compatible.

## Checking the current version locally

```bash
make version
```

Or read from `pyproject.toml`:

```bash
grep '^version = ' pyproject.toml
```

## CI and tags

The GitHub Actions workflow can use tags (e.g. `v*`) to build and attach artifacts to a GitHub Release. Pushing a tag like `v1.1.0` is the usual trigger for a release build.
