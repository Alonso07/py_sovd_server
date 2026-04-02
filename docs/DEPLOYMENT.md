# Deployment Guide

This guide covers deployment and CI/CD for the SOVD Server.

## Quick Deployment

### Local Development (Poetry)
```bash
poetry install
poetry run sovd-server
# or: make install && make run-server
```

### Production (pip from PyPI or wheel)
```bash
pip install sovd-server
sovd-server
# Or from built wheel/sdist:
pip install dist/sovd_server-*.whl
sovd-server
```

Configuration is loaded from `src/sovd_server/config/` by default. Override or extend via environment or gateway YAML as needed.

## Configuration

- **Development**: Use `sovd_gateway.yaml` with host `127.0.0.1` and DEBUG logging if desired.
- **Production**: Use a dedicated gateway config with appropriate host/port and INFO (or WARNING) logging. Ensure config paths are correct for the deployment layout.

## Docker

Example Dockerfile (Poetry or exported requirements):

**Option A — Poetry in image:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry
COPY pyproject.toml poetry.lock ./
COPY src/ ./src/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --without dev

EXPOSE 8080

CMD ["sovd-server"]
```

**Option B — Export requirements (no Poetry in image):**
```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
COPY pyproject.toml README.md ./
COPY src/ ./src/

RUN pip install --no-cache-dir .
# Or if you keep a static requirements.txt: pip install -r requirements.txt && pip install .

EXPOSE 8080

CMD ["sovd-server"]
```

Build and run:
```bash
docker build -t sovd-server .
docker run -p 8080:8080 sovd-server
```

## Publishing to PyPI

### How this project pushes to PyPI

1. **Local publishing (recommended)**  
   - Run: **`./scripts/publish/publish_to_pypi.sh`** from the project root.  
   - The script cleans, runs tests, builds with **Poetry** (`poetry build`), runs `twine check`, then prompts you to publish to **TestPyPI**, **PyPI**, or **Both**.  
   - Alternatively run manually: `poetry build` then `twine upload dist/*` (or `twine upload --repository testpypi dist/*`).

2. **CI (GitHub Actions)**  
   - [.github/workflows/publish-pypi.yml](../.github/workflows/publish-pypi.yml) runs on **tag pushes** matching `v*` (e.g. `v1.2.0`), builds with `./scripts/build_resolve_symlinks.sh build`, and publishes with [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish).  
   - Set the repository secret **`PYPI_TOKEN`** to your PyPI API token (same value you would put in `TWINE_PASSWORD` locally).  
   - Version tags are created automatically on `main` when conventional commits warrant a release; see [VERSIONING.md](VERSIONING.md).

### Where your PyPI credentials are stored

**Credentials are not stored in this repo.** They live outside the project:

- **Local (twine)**  
  Twine looks for credentials in:
  - **`~/.pypirc`** (recommended for local publish), e.g.:
    ```ini
    [pypi]
    username = __token__
    password = pypi-AgE...
    ```
    For Test PyPI add:
    ```ini
    [testpypi]
    username = __token__
    password = pypi-...   # token from test.pypi.org
    ```
  - Or **environment variables**: `TWINE_USERNAME=__token__`, `TWINE_PASSWORD=pypi-...`  
  After you enter the token once, twine can also use the **system keyring** (e.g. macOS Keychain) to reuse it.

- **CI (if you add a publish workflow)**  
  - Store the PyPI API token in the repo’s **GitHub Secrets** as **`PYPI_TOKEN`**.  
  - In the workflow use: `TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}` (and `TWINE_USERNAME: __token__`). No username/password in the repo.

Create or manage tokens at [PyPI → Account → API tokens](https://pypi.org/manage/account/token/).

**One-time local setup (so you can push a new version from your machine):**  
Create or edit `~/.pypirc` with your PyPI token (no repo changes needed):

```ini
[pypi]
username = __token__
password = pypi-YourTokenFromPyPI
```

Then run `./scripts/publish/publish_to_pypi.sh` whenever you want to publish a new version; twine will read credentials from `~/.pypirc`.

### Prerequisites

1. **PyPI account**: [Register at pypi.org](https://pypi.org/account/register/) (and optionally [Test PyPI](https://test.pypi.org/account/register/) for testing).
2. **API token**: On PyPI go to **Account → API tokens → Add API token**. Create a token with scope “Entire account” or limit to the project (e.g. `sovd-server`). **Do not commit the token**; use `~/.pypirc`, env vars, or GitHub Secrets only.

### Configuring PyPI variables for CI (GitHub)

To publish from GitHub Actions (or use the same variable names locally), configure **one secret** in the repository:

| Where | Name | Value | Notes |
|-------|------|--------|--------|
| **GitHub** → Repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret** | `PYPI_TOKEN` | Your PyPI API token (starts with `pypi-`) | Used by the publish workflow as `TWINE_PASSWORD` |

- **Secret name**: `PYPI_TOKEN` (same as in the doip_server project).
- **Value**: The token from PyPI (Account → API tokens). Use “Entire account” or a token scoped to this project.
- For **Test PyPI** you can add a second secret, e.g. `TEST_PYPI_TOKEN`, and use it in a separate job or workflow.

Twine expects:
- `TWINE_USERNAME=__token__`
- `TWINE_PASSWORD=<your PyPI token>`

In CI you pass the token via the secret, e.g. `TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}` (see “Publish to PyPI via GitHub Actions” below).

### Steps to publish

1. **Set version** (see [VERSIONING.md](VERSIONING.md)):
   - Update `version` in `pyproject.toml` (e.g. `poetry version patch`).
   - Update `docs/CHANGELOG.md`.

2. **Install Poetry and twine** (one-time):
   ```bash
   # Poetry: https://python-poetry.org/docs/#installation
   pip install twine
   # or: poetry self add twine  (if you prefer)
   ```

3. **Build the package** (resolves symlinks so the wheel contains real files):
   ```bash
   make build
   # or: ./scripts/build_resolve_symlinks.sh build
   ```
   This creates `dist/sovd_server-<version>.tar.gz` and `dist/sovd_server-<version>-py3-none-any.whl`.

4. **Check the archives** (optional):
   ```bash
   twine check dist/*
   ```

5. **Upload to Test PyPI** (recommended first time):
   ```bash
   twine upload --repository testpypi dist/*
   ```
   When prompted, use your Test PyPI username and the token as the password (or set `TWINE_USERNAME=__token__` and `TWINE_PASSWORD=<token>`). Then try: `pip install -i https://test.pypi.org/simple/ sovd-server`.

6. **Upload to PyPI**:
   ```bash
   twine upload dist/*
   ```
   Use PyPI username and API token. Or:
   ```bash
   export TWINE_USERNAME=__token__
   export TWINE_PASSWORD=pypi-YourTokenHere
   twine upload dist/*
   ```

7. **Tag the release** (recommended):
   ```bash
   git tag -a v1.0.0 -m "Release 1.0.0"
   git push origin v1.0.0
   ```

### Notes

- **Package name**: The project uses the name `sovd-server` (with hyphen). On PyPI the name is normalized; users install with `pip install sovd-server`.
- **First release**: The name `sovd-server` must be free on PyPI. If it is taken, choose another name and set it in `pyproject.toml`.
- **Re-releases**: PyPI does not allow re-uploading the same version; bump the version for every release.

### Publish to PyPI via GitHub Actions

You can automate publishing so that pushing a version tag (e.g. `v1.0.0`) builds and uploads to PyPI. Configure the `PYPI_TOKEN` secret as above, then add a workflow like this (e.g. `.github/workflows/publish-pypi.yml`):

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]
  # Or trigger on tag push:
  # push:
  #   tags: [ 'v*' ]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v6

    - name: Set up Python
      uses: actions/setup-python@v6
      with:
        python-version: '3.11'

    - name: Install Poetry
      uses: snok/install-poetry@v1
      with:
        version: 1.8.5
        virtualenvs-create: true
        virtualenvs-in-project: true

    - name: Install twine
      run: pip install twine

    - name: Build package
      run: poetry build

    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
      run: twine upload dist/*
```

- **Secret**: The workflow uses `secrets.PYPI_TOKEN` (same variable name as in the doip_server project).
- **Trigger**: Either on **Release published** (create a release on the GitHub repo) or on **tag push** `v*`; adjust the `on:` block to match how you release.

## CI/CD (GitHub Actions)

The repository includes:

- **`.github/workflows/ci.yml`**: On push/PR to `main`/`develop`:
  - Lint (flake8), format check (black)
  - Security (bandit, safety)
  - Tests with coverage (pytest)
  - Optional: build package (on main)

The workflow uses **Poetry**: `poetry install` and `poetry run` for lint, test, and `poetry build` on main.

## System Service (systemd)

Example unit file:

```ini
[Unit]
Description=SOVD Server
After=network.target

[Service]
Type=simple
User=sovd
Group=sovd
WorkingDirectory=/opt/sovd-server
ExecStart=/opt/sovd-server/.venv/bin/sovd-server
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## Monitoring and Logging

- Configure logging level and output in `sovd_gateway.yaml`.
- Use a process manager or systemd for restarts and logging.
- Optionally put a reverse proxy (e.g. nginx) in front and restrict access to the SOVD port.

## Security

- Run as a non-root user.
- Restrict network access to the SOVD port.
- Keep dependencies updated (e.g. with Dependabot or `pip install -U`).
- Do not expose the server unnecessarily to the internet.
