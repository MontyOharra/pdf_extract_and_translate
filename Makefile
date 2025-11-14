# Makefile for PDF Extract and Translate
# Using Conda with local environment (conda_env/ directory)

.PHONY: help setup install install-dev test test-cov test-watch clean run check-deps

# Conda environment settings
CONDA_ENV := conda_env
CONDA_ENV_BIN := $(CONDA_ENV)/Scripts
CONDA_PYTHON := $(CONDA_ENV_BIN)/python.exe
CONDA_PYTEST := $(CONDA_ENV_BIN)/pytest.exe
CONDA_PIP := $(CONDA_ENV_BIN)/pip.exe

# Conda command
CONDA := conda

# Default target - show help
help:
	@echo ""
	@echo "PDF Extract and Translate - Makefile Commands"
	@echo "=============================================="
	@echo ""
	@echo "Setup:"
	@echo "  make setup        - Create conda environment and install all dependencies"
	@echo "  make check-deps   - Check if conda is installed"
	@echo ""
	@echo "Installation:"
	@echo "  make install      - Install production dependencies only"
	@echo "  make install-dev  - Install development dependencies (pytest, etc.)"
	@echo ""
	@echo "Testing:"
	@echo "  make test         - Run all tests with verbose output"
	@echo "  make test-cov     - Run tests with coverage report"
	@echo "  make test-watch   - Run tests in watch mode (re-run on file changes)"
	@echo "  make test-fast    - Run tests, stop at first failure"
	@echo ""
	@echo "Running:"
	@echo "  make run          - Run the interactive application"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        - Remove conda environment and cache files"
	@echo "  make clean-cache  - Remove only cache files (keep conda_env)"
	@echo ""

# Check if conda is installed
check-deps:
	@echo "Checking dependencies..."
	@which conda > /dev/null || (echo "ERROR: conda not found. Please install Anaconda or Miniconda from:" && echo "  https://docs.conda.io/en/latest/miniconda.html" && exit 1)
	@echo " Conda is installed: $$(conda --version)"
	@echo " All system dependencies OK!"

# Setup: Create conda environment and install everything
setup: check-deps clean
	@echo "Creating conda environment in ./$(CONDA_ENV)..."
	$(CONDA) create -p ./$(CONDA_ENV) python=3.9 -y
	@echo ""
	@echo "Installing system dependencies (Tesseract, Poppler)..."
	$(CONDA) install -p ./$(CONDA_ENV) -c conda-forge tesseract poppler -y
	@echo ""
	@echo "Upgrading pip in conda environment..."
	$(CONDA_PIP) install --upgrade pip
	@echo ""
	@echo "Installing production dependencies..."
	$(CONDA_PIP) install -r requirements.txt
	@echo ""
	@echo "Installing development dependencies..."
	$(CONDA_PIP) install -r requirements-dev.txt
	@echo ""
	@echo "========================================"
	@echo " Setup complete!"
	@echo "========================================"
	@echo ""
	@echo "To activate the conda environment:"
	@echo "  conda activate ./$(CONDA_ENV)    (All platforms)"
	@echo ""
	@echo "System dependencies installed:"
	@echo "  - Tesseract OCR (for text extraction)"
	@echo "  - Poppler (for PDF processing)"
	@echo ""

# Install production dependencies only
install:
	@echo "Installing production dependencies..."
	@$(CONDA_PIP) install -r requirements.txt
	@echo " Production dependencies installed"

# Install development dependencies
install-dev:
	@echo "Installing development dependencies..."
	@$(CONDA_PIP) install -r requirements-dev.txt
	@echo " Development dependencies installed"

# Run all tests with verbose output
test:
	@echo "Running tests..."
	@PATH="$(CONDA_ENV)/Library/bin:$$PATH" TESSDATA_PREFIX="$(CONDA_ENV)/share/tessdata" $(CONDA_PYTEST) -v

# Run tests with coverage report
test-cov:
	@echo "Running tests with coverage..."
	@PATH="$(CONDA_ENV)/Library/bin:$$PATH" TESSDATA_PREFIX="$(CONDA_ENV)/share/tessdata" $(CONDA_PYTEST) -v --cov=src --cov-report=term-missing --cov-report=html
	@echo ""
	@echo "Coverage report generated in htmlcov/index.html"

# Run tests in watch mode (requires pytest-watch)
test-watch:
	@echo "Running tests in watch mode (Ctrl+C to stop)..."
	@PATH="$(CONDA_ENV)/Library/bin:$$PATH" TESSDATA_PREFIX="$(CONDA_ENV)/share/tessdata" $(CONDA_ENV_BIN)/ptw -- -v

# Run tests, stop at first failure (useful for TDD)
test-fast:
	@echo "Running tests (stop at first failure)..."
	@PATH="$(CONDA_ENV)/Library/bin:$$PATH" TESSDATA_PREFIX="$(CONDA_ENV)/share/tessdata" $(CONDA_PYTEST) -x -v

# Run the application
run:
	@echo "Starting PDF Extract and Translate..."
	@$(CONDA_PYTHON) main.py

# Clean up everything
clean:
	@echo "Cleaning up..."
	rm -rf $(CONDA_ENV)
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -rf dist
	rm -rf build
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo " Cleanup complete"

# Clean only cache files (keep conda environment)
clean-cache:
	@echo "Cleaning cache files..."
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo " Cache cleaned"
