# Publishing sovd-server to PyPI

## First-time setup: store your PyPI token

Credentials are **not** in this repo. Use one of these (once per machine):

### Option A: `~/.pypirc` (recommended)

1. Create a token at [pypi.org/manage/account/token/](https://pypi.org/manage/account/token/).
   - For the **first release**, use scope **"Entire account"** (or create a token and choose "Create new project" when you create the project on PyPI).
   - Copy the token (starts with `pypi-`).

2. Create the file (replace `pypi-YourTokenHere` with your real token):

   ```bash
   cat > ~/.pypirc << 'EOF'
   [pypi]
   username = __token__
   password = pypi-YourTokenHere
   EOF
   chmod 600 ~/.pypirc
   ```

   Or edit manually: `nano ~/.pypirc` or `open -e ~/.pypirc` and paste:

   ```ini
   [pypi]
   username = __token__
   password = pypi-YourActualToken
   ```

   Then: `chmod 600 ~/.pypirc`

### Option B: environment variables

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YourTokenHere
```

Then run the upload command in the same shell.

---

## Push the first version (or a new version)

From the **project root** (requires [Poetry](https://python-poetry.org/)):

```bash
# Interactive: cleans, tests, builds with Poetry, then asks TestPyPI / PyPI / Both
./scripts/publish/publish_to_pypi.sh
```

Or do it manually:

```bash
poetry build
twine check dist/*
twine upload dist/*                    # production PyPI
# twine upload --repository testpypi dist/*   # Test PyPI only
```

If you get **403 Forbidden**: your token may not have permission to create a new project. Create a token with scope **"Entire account"** or create the project name on PyPI first, then use a token scoped to that project.
