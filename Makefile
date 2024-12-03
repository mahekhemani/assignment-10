# Variables
PYTHON = python3
APP = src/app.py
VENV = venv

# Default rule: Run the Flask app
run:
	$(PYTHON) $(APP)

# Create a virtual environment and install dependencies
setup:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

# Install required Python packages
install:
	pip install -r requirements.txt

# Clean up cache files and temporary files
clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf $(VENV)
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.pyc" -exec rm -rf {} +

# Run debug-static-path route for testing
debug-static:
	$(PYTHON) -c "from src.app import debug_static_path; print(debug_static_path())"

# Lint code with flake8
lint:
	flake8 src/ --ignore=E501

# Help message
help:
	@echo "Usage:"
	@echo "  make run         - Run the Flask app"
	@echo "  make setup       - Create a virtual environment and install dependencies"
	@echo "  make install     - Install required dependencies"
	@echo "  make clean       - Remove temporary and cache files"
	@echo "  make debug-static - Run debug-static-path for testing"
	@echo "  make lint        - Lint code with flake8"

