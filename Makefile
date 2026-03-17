# SOVD Server - use a virtual environment (recommended on macOS/Homebrew: run "make venv" first)
# If ./venv exists we use it; otherwise we use PYTHON / python -m pip (requires active venv or --break-system-packages)
ifneq (,$(wildcard venv/bin/python))
  PYTHON := venv/bin/python
  PIP := venv/bin/pip
else
  PYTHON ?= python
  PIP ?= $(PYTHON) -m pip
endif

.PHONY: help venv install install-dev test lint format format-check security clean run-server run-tests
.PHONY: test-python310 test-python311 test-python312 test-versions ci-local version setup

help:  ## Show this help message
	@echo "SOVD Server Development Commands"
	@echo "================================"
	@echo "  venv             - Create venv and install dev deps (run this first on macOS/Homebrew)"
	@echo "  install          - Install package in development mode (uses venv if present)"
	@echo "  install-dev      - Install with dev dependencies (uses venv if present)"
	@echo "  run-server       - Run the enhanced server"
	@echo "  test             - Run all tests"
	@echo "  run-tests        - Run tests with coverage report"
	@echo "  lint             - Run flake8 and mypy"
	@echo "  format           - Format code with black"
	@echo "  format-check     - Check formatting only (no write)"
	@echo "  security         - Run security checks (bandit, safety)"
	@echo "  test-python310   - Run tests with Python 3.10 (isolated venv)"
	@echo "  test-python311   - Run tests with Python 3.11 (isolated venv)"
	@echo "  test-python312   - Run tests with Python 3.12 (isolated venv)"
	@echo "  test-versions    - Run tests with 3.10, 3.11, 3.12 (skips missing)"
	@echo "  ci-local         - Run full CI pipeline locally (lint, format-check, security, test)"
	@echo "  version          - Show current package version"
	@echo "  clean            - Remove build artifacts, caches, reports, versioned venvs"
	@echo "  setup            - venv + print next steps"

# Create venv and install (avoids externally-managed-environment on macOS/Homebrew)
venv:  ## Create venv and install dev deps; other make targets will use this venv
	@if [ ! -d venv ]; then python3 -m venv venv; fi
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -e ".[dev]"
	@echo "Done. Use: source venv/bin/activate  (or run make targets; they will use venv automatically)"

# Installation (uses venv if present, else current PYTHON/PIP)
install:  ## Install the package in development mode
	$(PIP) install -e .

install-dev:  ## Install with dev dependencies (includes bandit, safety)
	$(PIP) install -e ".[dev]"

# Running
run-server:  ## Run the enhanced server
	$(PYTHON) -m sovd_server.run_enhanced_server

# Testing
test:  ## Run all tests
	$(PYTHON) -m pytest tests/ -v

run-tests:  ## Run tests with coverage
	$(PYTHON) -m pytest tests/ -v --cov=sovd_server --cov-report=term-missing --cov-report=html

# Linting and formatting
lint:  ## Run flake8 and mypy
	$(PYTHON) -m flake8 src/ tests/ --max-line-length=88
	$(PYTHON) -m mypy src/ || true

format:  ## Format code with black
	$(PYTHON) -m black src/ tests/

format-check:  ## Check formatting without changing files
	$(PYTHON) -m black --check --diff src/ tests/

# Security checks (bandit, safety) - install with: make install-dev
security:  ## Run bandit and safety
	@mkdir -p reports
	$(PYTHON) -m bandit -r src/ -f json -o reports/bandit-report.json || true
	$(PYTHON) -m safety check --json > reports/safety-report.json 2>/dev/null || true
	@echo "Security reports: reports/bandit-report.json, reports/safety-report.json"

# Multi-version testing (creates .venv-310, .venv-311, .venv-312)
test-python310:  ## Run tests with Python 3.10
	@echo "Testing with Python 3.10..."
	@if command -v python3.10 >/dev/null 2>&1; then \
		python3.10 -m venv .venv-310 && \
		.venv-310/bin/pip install --upgrade pip && \
		.venv-310/bin/pip install -e ".[dev]" && \
		.venv-310/bin/pip install bandit safety && \
		.venv-310/bin/python -m pytest tests/ -v; \
	else \
		echo "Python 3.10 not found. Install it (e.g. pyenv, deadsnakes) and retry."; \
		exit 1; \
	fi

test-python311:  ## Run tests with Python 3.11
	@echo "Testing with Python 3.11..."
	@if command -v python3.11 >/dev/null 2>&1; then \
		python3.11 -m venv .venv-311 && \
		.venv-311/bin/pip install --upgrade pip && \
		.venv-311/bin/pip install -e ".[dev]" && \
		.venv-311/bin/pip install bandit safety && \
		.venv-311/bin/python -m pytest tests/ -v; \
	else \
		echo "Python 3.11 not found. Install it (e.g. pyenv, deadsnakes) and retry."; \
		exit 1; \
	fi

test-python312:  ## Run tests with Python 3.12
	@echo "Testing with Python 3.12..."
	@if command -v python3.12 >/dev/null 2>&1; then \
		python3.12 -m venv .venv-312 && \
		.venv-312/bin/pip install --upgrade pip && \
		.venv-312/bin/pip install -e ".[dev]" && \
		.venv-312/bin/pip install bandit safety && \
		.venv-312/bin/python -m pytest tests/ -v; \
	else \
		echo "Python 3.12 not found. Install it (e.g. pyenv, deadsnakes) and retry."; \
		exit 1; \
	fi

test-versions:  ## Run tests with 3.10, 3.11, 3.12 (skips missing)
	@for v in 310 311 312; do \
		if command -v python3.$$v >/dev/null 2>&1; then \
			echo "=== Python 3.$$v ==="; \
			$(MAKE) test-python3$$v || true; \
		else \
			echo "Skipping Python 3.$$v (not installed)"; \
		fi; \
	done

# Full CI pipeline locally
ci-local:  ## Lint, format-check, security, test (simulate CI)
	@echo "Running CI pipeline locally..."
	@$(MAKE) lint
	@$(MAKE) format-check
	@$(MAKE) security
	@$(MAKE) test
	@echo "CI pipeline completed."

# Version (single source: pyproject.toml)
version:  ## Show current package version
	@$(PYTHON) -c "import re; m=re.search(r'version\s*=\s*[\"']([^\"']+)[\"']', open('pyproject.toml').read()); print(m.group(1) if m else 'unknown')"

# Cleanup
clean:  ## Remove build artifacts, caches, reports, versioned venvs
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf src/*.egg-info/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -f .coverage coverage.xml
	rm -rf reports/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .venv-310 .venv-311 .venv-312
	@echo "Tip: to remove project venv too: rm -rf venv"
	@echo "Clean done."

setup: venv  ## Set up development environment (create venv + install)
	@echo "  make run-server   - start server"
	@echo "  make test         - run tests"
	@echo "  make security     - run security checks"
	@echo "  make test-versions - test with Python 3.10/3.11/3.12"
