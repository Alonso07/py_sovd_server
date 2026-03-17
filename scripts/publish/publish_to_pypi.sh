#!/bin/bash

# SOVD Server PyPI Publishing Script
# Publish the sovd-server package to PyPI (or Test PyPI).
# Uses Poetry to build. Credentials: ~/.pypirc or TWINE_USERNAME/TWINE_PASSWORD (never in this repo).

set -e

echo "🚀 SOVD Server PyPI Publishing Script"
echo "====================================="

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/../.."

if [ ! -f "pyproject.toml" ]; then
    print_error "pyproject.toml not found. Run this script from the project root."
    exit 1
fi

if ! command -v poetry >/dev/null 2>&1; then
    print_error "Poetry is required. Install from https://python-poetry.org/docs/#installation"
    exit 1
fi

if ! command -v twine >/dev/null 2>&1; then
    print_status "Installing twine..."
    pip install twine
fi

# Clean previous builds
print_status "Cleaning previous builds..."
rm -rf dist/ build/

# Run tests
print_status "Running tests..."
poetry run pytest tests/ --tb=no -q || { print_error "Tests failed. Fix tests before publishing."; exit 1; }
print_success "All tests passed!"

# Build with Poetry (resolve symlinks first so wheel contains real files)
print_status "Building package (resolving symlinks for wheel)..."
./scripts/build_resolve_symlinks.sh build || { print_error "Build failed."; exit 1; }
print_success "Package built successfully!"

# Check
print_status "Checking package..."
twine check dist/* || { print_error "Package check failed."; exit 1; }
print_success "Package check passed!"

# Publish target
echo ""
echo "Where would you like to publish?"
echo "1) TestPyPI (recommended for testing)"
echo "2) PyPI (production)"
echo "3) Both (TestPyPI first, then PyPI)"
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        print_status "Publishing to TestPyPI..."
        twine upload --repository testpypi dist/*
        print_success "Published to TestPyPI! Test with: pip install -i https://test.pypi.org/simple/ sovd-server"
        ;;
    2)
        print_warning "Publishing to PyPI (production)..."
        read -p "Are you sure? (y/N): " confirm
        if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
            twine upload dist/*
            print_success "Published to PyPI! Install with: pip install sovd-server"
        else
            print_status "Publishing cancelled."
        fi
        ;;
    3)
        print_status "Publishing to TestPyPI first..."
        twine upload --repository testpypi dist/*
        print_success "Published to TestPyPI!"
        read -p "Test from TestPyPI, then press Enter to publish to PyPI..."
        print_warning "Publishing to PyPI..."
        twine upload dist/*
        print_success "Published to PyPI! Install with: pip install sovd-server"
        ;;
    *)
        print_error "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
print_success "Publishing complete! 🎉"
echo "Next steps:"
echo "  1. Test: pip install sovd-server"
echo "  2. PyPI: https://pypi.org/project/sovd-server/"
echo "  3. Bump version: poetry version patch|minor|major"
echo "  4. Create a GitHub release / tag"
