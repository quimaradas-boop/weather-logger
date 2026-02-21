.PHONY: help run test lint clean install

help:
	@echo "Available commands:"
	@echo "  make run      - Run the weather logger with default settings"
	@echo "  make test     - Run basic tests (if available)"
	@echo "  make lint     - Check code style with flake8 (if installed)"
	@echo "  make clean    - Remove generated files"
	@echo "  make install  - Install to /usr/local/bin (requires sudo)"

run:
	python3 weather.py

test:
	@echo "Testing weather logger..."
	python3 weather.py --city "Lisbon" --output test_output.csv
	@echo "Test output:"
	cat test_output.csv
	@rm -f test_output.csv

lint:
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 weather.py; \
	else \
		echo "flake8 not installed. Install with: pip install flake8"; \
	fi

clean:
	rm -f weather_log.csv test_output.csv
	rm -rf __pycache__ *.pyc
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

install:
	@echo "Installing weather-logger to /usr/local/bin..."
	@cp weather.py /usr/local/bin/weather-logger
	@chmod +x /usr/local/bin/weather-logger
	@echo "Installed! Run: weather-logger --help"
