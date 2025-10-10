.PHONY: help install install-dev test lint format clean run-server run-tests

help:  ## Show this help message
	@echo "SOVD Server Development Commands"
	@echo "================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install the package in development mode
	poetry install

install-dev:  ## Install development dependencies
	poetry install --with dev

test:  ## Run all tests
	poetry run pytest tests/ -v

lint:  ## Run linting checks
	poetry run flake8 src/ tests/
	poetry run mypy src/

format:  ## Format code with black
	poetry run black src/ tests/

clean:  ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	poetry cache clear --all pypi

run-server:  ## Run the enhanced server
	poetry run python src/sovd_server/enhanced_server.py

run-tests:  ## Run tests with coverage
	poetry run pytest tests/ -v --cov=src/sovd_server --cov-report=html

setup: install-dev  ## Set up development environment
	@echo "Development environment set up successfully!"
	@echo "Run 'make run-server' to start the server"
	@echo "Run 'make test' to run tests"
