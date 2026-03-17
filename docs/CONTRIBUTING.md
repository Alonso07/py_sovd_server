# Contributing to SOVD Server

Thank you for your interest in contributing to the SOVD Server project. This document provides guidelines for contributors.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip and venv
- Git

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/sovd_server.git
   cd sovd_server
   ```

2. **Create virtual environment and install dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. **Run tests to verify setup**
   ```bash
   pytest tests/ -v
   ```

4. **Start the server for testing**
   ```bash
   python -m sovd_server.run_enhanced_server
   ```

## 📋 Development Workflow

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

### 3. Test Your Changes
```bash
pytest tests/ -v
pytest tests/ --cov=sovd_server --cov-report=term-missing
```

### 4. Code Quality Checks
```bash
black src/ tests/
flake8 src/ tests/
# Optional: bandit -r src/
```

### 5. Commit and Push
```bash
git add .
git commit -m "feat: add new feature description"
git push origin feature/your-feature-name
```

### 6. Create Pull Request
- Use the provided PR template
- Reference any related issues
- Ensure CI checks pass

## 🎨 Coding Standards

### Python Style
- Follow PEP 8
- Use Black for formatting (see pyproject.toml)
- Use type hints where appropriate
- Write docstrings for public functions/classes

### Testing
- New features should include tests
- Use pytest; place tests in `tests/`
- Use descriptive test names

## 📝 Documentation

- Update README.md for user-facing changes
- Update docs/ for configuration or API changes
- Use docstrings for code (Google or NumPy style)

## 🐛 Bug Reports

When reporting bugs, please include:
1. Clear description and steps to reproduce
2. Expected vs actual behavior
3. Environment (OS, Python version)
4. Configuration/logs (with sensitive data removed)

Use the bug report template in `.github/ISSUE_TEMPLATE/bug_report.md`.

## ✨ Feature Requests

Use the feature request template in `.github/ISSUE_TEMPLATE/feature_request.md`.

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.
