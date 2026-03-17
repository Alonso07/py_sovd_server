# SOVD Server - Poetry-based development
# Prerequisite: install Poetry (https://python-poetry.org/docs/#installation), then run 'make install'

POETRY ?= poetry

.PHONY: help install install-dev run-server test run-tests lint format format-check security
.PHONY: test-python310 test-python311 test-python312 test-versions ci-local version clean setup export-requirements build

help:  ## Show this help message
	@echo "SOVD Server (Poetry)"
	@echo "===================="
	@echo "  install          - Install dependencies (poetry install)"
	@echo "  install-dev      - Same as install (dev deps included by default)"
	@echo "  run-server       - Run the enhanced SOVD server"
	@echo "  test             - Run tests"
	@echo "  run-tests        - Run tests with coverage"
	@echo "  lint             - Run flake8 and mypy"
	@echo "  format           - Format code with black"
	@echo "  format-check     - Check formatting only"
	@echo "  security         - Run bandit and safety"
	@echo "  test-python310   - Run tests with Python 3.10"
	@echo "  test-python311   - Run tests with Python 3.11"
	@echo "  test-python312   - Run tests with Python 3.12"
	@echo "  test-versions    - Run tests on 3.10, 3.11, 3.12 (skips missing)"
	@echo "  ci-local         - Lint, format-check, security, test"
	@echo "  version          - Show package version"
	@echo "  export-requirements - Export requirements.txt (e.g. for Docker)"
	@echo "  build            - Build wheel and sdist (resolves symlinks for distribution)"
	@echo "  clean            - Remove build artifacts and caches"
	@echo "  setup            - Install and print next steps"

install:  ## Install dependencies with Poetry
	$(POETRY) install

install-dev: install  ## Alias for install (Poetry includes dev deps by default)

run-server:  ## Run the enhanced server
	$(POETRY) run sovd-server

test:  ## Run tests
	$(POETRY) run pytest tests/ -v

run-tests:  ## Run tests with coverage
	$(POETRY) run pytest tests/ -v --cov=sovd_server --cov-report=term-missing --cov-report=html

lint:  ## Run flake8 and mypy
	$(POETRY) run flake8 src/ tests/ --max-line-length=88
	$(POETRY) run mypy src/ || true

format:  ## Format code with black
	$(POETRY) run black src/ tests/

format-check:  ## Check formatting without changing files
	$(POETRY) run black --check --diff src/ tests/

security:  ## Run bandit and safety
	@mkdir -p reports
	$(POETRY) run bandit -r src/ -f json -o reports/bandit-report.json || true
	$(POETRY) run safety check --json > reports/safety-report.json 2>/dev/null || true
	@echo "Security reports: reports/bandit-report.json, reports/safety-report.json"

test-python310:  ## Run tests with Python 3.10
	@echo "Testing with Python 3.10..."
	$(POETRY) env use python3.10 2>/dev/null || true
	$(POETRY) install
	$(POETRY) run pytest tests/ -v

test-python311:  ## Run tests with Python 3.11
	@echo "Testing with Python 3.11..."
	$(POETRY) env use python3.11 2>/dev/null || true
	$(POETRY) install
	$(POETRY) run pytest tests/ -v

test-python312:  ## Run tests with Python 3.12
	@echo "Testing with Python 3.12..."
	$(POETRY) env use python3.12 2>/dev/null || true
	$(POETRY) install
	$(POETRY) run pytest tests/ -v

test-versions:  ## Run tests on multiple Python versions (skips missing)
	@for v in 3.10 3.11 3.12; do \
		if command -v python$$v >/dev/null 2>&1; then \
			echo "=== Python $$v ==="; \
			$(POETRY) env use python$$v 2>/dev/null || true; \
			$(POETRY) install --no-interaction && $(POETRY) run pytest tests/ -v || true; \
		else \
			echo "Skipping Python $$v (not installed)"; \
		fi; \
	done

ci-local:  ## Run full CI pipeline locally
	@echo "Running CI pipeline locally..."
	@$(MAKE) lint
	@$(MAKE) format-check
	@$(MAKE) security
	@$(MAKE) test
	@echo "CI pipeline completed."

version:  ## Show package version
	@$(POETRY) version -s

export-requirements:  ## Export requirements.txt (for Docker or non-Poetry CI)
	$(POETRY) export -f requirements.txt --output requirements.txt --without-hashes
	@echo "Exported requirements.txt"

build:  ## Build wheel and sdist (resolves symlinks so dist package has real files)
	./scripts/build_resolve_symlinks.sh build

clean:  ## Remove build artifacts and caches
	rm -rf build/ dist/ *.egg-info/ src/*.egg-info/
	rm -rf __pycache__/ .pytest_cache/ .mypy_cache/ htmlcov/
	rm -f .coverage coverage.xml
	rm -rf reports/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Clean done. To remove Poetry venv: $(POETRY) env remove --all"

setup: install  ## First-time setup
	@echo ""
	@echo "Next steps:"
	@echo "  make run-server   - start the SOVD server"
	@echo "  make test         - run tests"
	@echo "  make security     - run security checks"
