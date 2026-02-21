# Weather Logger

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple, zero-dependency Python script that fetches current weather data from Open-Meteo API and logs it to a CSV file.

## Features

- **Zero Dependencies**: Uses only Python standard library
- **CSV Logging**: Saves weather data to timestamped CSV files
- **Flexible Input**: Accepts city names, coordinates, or defaults to Lisbon
- **Robust Error Handling**: With timeouts and validation
- **Open-Meteo API**: No API key required
- **Cross-platform**: Works on any system with Python 3.7+

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/weather-logger.git
cd weather-logger

# Run with default settings (logs to weather_log.csv for Lisbon)
python weather.py

# Log weather for a specific city
python weather.py --city "London"

# Log weather for specific coordinates
python weather.py --lat 40.7128 --lon -74.0060

# Save to a custom file
python weather.py --city "Tokyo" --output "tokyo_weather.csv"
```

## Installation

### Method 1: Direct Download
Download `weather.py` directly from the repository and run it:
```bash
curl -O https://raw.githubusercontent.com/yourusername/weather-logger/main/weather.py
python weather.py
```

### Method 2: Clone Repository
```bash
git clone https://github.com/yourusername/weather-logger.git
cd weather-logger
python weather.py
```

### Method 3: Python Package (Coming Soon)
```bash
pip install weather-logger
```

## Usage Examples

### Basic Usage
```bash
# Default: Lisbon, weather_log.csv
python weather.py

# Specific city
python weather.py --city "Paris"

# Specific coordinates
python weather.py --lat 35.6895 --lon 139.6917

# Custom output file
python weather.py --city "New York" --output "nyc_weather.csv"
```

### Cron Automation
Set up a cron job to log weather every hour:
```bash
# Edit crontab
crontab -e

# Add this line to run every hour at 15 minutes past the hour
15 * * * * /usr/bin/python3 /path/to/weather.py --city "London" --output "/path/to/weather_log.csv"
```

## CSV Format

The script saves data in the following CSV format:

| Field | Description |
|-------|-------------|
| `timestamp` | ISO 8601 timestamp of when data was collected |
| `location` | Name of the location (city name or "Provided coordinates") |
| `latitude` | Latitude coordinate |
| `longitude` | Longitude coordinate |
| `temperature_c` | Temperature in Celsius |
| `humidity_percent` | Relative humidity in percent |
| `wind_speed_kmh` | Wind speed in kilometers per hour |
| `wind_direction_deg` | Wind direction in degrees (0-360) |
| `conditions` | Human-readable weather condition |
| `pressure_hpa` | Atmospheric pressure in hectopascals |

## API Documentation

This tool uses the [Open-Meteo API](https://open-meteo.com/), which provides free weather data without requiring an API key. The following endpoints are used:

- **Geocoding**: `https://geocoding-api.open-meteo.com/v1/search?name=CITY&count=1`
- **Weather Data**: `https://api.open-meteo.com/v1/forecast?latitude=LAT&longitude=LON&current=temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,surface_pressure,weather_code`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.