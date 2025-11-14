# Makefile for PDF Extract and Translate
# Windows Git Bash compatible

.PHONY: help setup install install-dev test test-cov test-watch clean run lint format init-git

# Detect Python command (python or python3)
PYTHON := python
PIP := $(PYTHON) -m pip
VENV := venv
VENV_BIN := $(VENV)/Scripts

# Default target - show help
help:
	@echo ""
	@echo "make setup        - Create virtual environment and install all dependencies"
	@echo "make install      - Install production dependencies only"
	@echo "make install-dev  - Install development dependencies (pytest, etc.)"
	@echo ""
	@echo "make test         - Run all tests with verbose output"
	@echo "make test-cov     - Run tests with coverage report"
	@echo "make test-watch   - Run tests in watch mode (re-run on file changes)"
	@echo "make test-fast    - Run tests, stop at first failure"
	@echo ""
	@echo "make run          - Run the interactive application"
	@echo ""
	@echo "make lint         - Run code linting (flake8)"
	@echo ""
	@echo "make clean        - Remove virtual environment and cache files"
	@echo "make clean-cache  - Remove only cache files (keep venv)"
	@echo ""

# Setup: Create venv and install everything
setup: clean
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)
	@echo "Upgrading pip..."
	$(VENV_BIN)/$(PIP) install --upgrade pip
	@echo "Installing production dependencies..."
	$(VENV_BIN)/$(PIP) install -r requirements.txt
	@echo "Installing development dependencies..."
	$(VENV_BIN)/$(PIP) install -r requirements-dev.txt
	@echo ""
	@echo " Setup complete!"
	@echo ""
	@echo "To activate the virtual environment:"
	@echo "  source venv/Scripts/activate    (Git Bash)"
	@echo "  venv\\Scripts\\activate          (Windows CMD)"
	@echo ""

# Install production dependencies only
install:
	@echo "Installing production dependencies..."
	$(VENV_BIN)/$(PIP) install -r requirements.txt
	@echo " Production dependencies installed"

# Install development dependencies
install-dev:
	@echo "Installing development dependencies..."
	$(VENV_BIN)/$(PIP) install -r requirements-dev.txt
	@echo " Development dependencies installed"

# Run all tests with verbose output
test:
	@echo "Running tests..."
	$(VENV_BIN)/pytest -v

# Run tests with coverage report
test-cov:
	@echo "Running tests with coverage..."
	$(VENV_BIN)/pytest -v --cov=src --cov-report=term-missing --cov-report=html
	@echo ""
	@echo "=� Coverage report generated in htmlcov/index.html"

# Run tests in watch mode (requires pytest-watch)
test-watch:
	@echo "Running tests in watch mode (Ctrl+C to stop)..."
	$(VENV_BIN)/ptw -- -v

# Run tests, stop at first failure (useful for TDD)
test-fast:
	@echo "Running tests (stop at first failure)..."
	$(VENV_BIN)/pytest -x -v

# Run the application
run:
	@echo "Starting PDF Extract and Translate..."
	$(VENV_BIN)/$(PYTHON) main.py

# Lint code with flake8
lint:
	@echo "Linting code..."
	$(VENV_BIN)/flake8 src tests --max-line-length=100 --exclude=venv,__pycache__
	@echo " Linting complete"

# Clean up everything
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV)
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -rf dist
	rm -rf build
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.egg" -delete 2>/dev/null || true
	@echo " Cleanup complete"

# Clean only cache files (keep venv)
clean-cache:
	@echo "Cleaning cache files..."
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo " Cache cleaned"