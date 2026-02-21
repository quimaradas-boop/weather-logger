#!/bin/bash
# Basic Usage Examples for Weather Logger
# Run these commands in the project directory

# Example 1: Default settings (Lisbon)
echo "=== Example 1: Default (Lisbon) ==="
python weather.py

# Example 2: Specific city
echo ""
echo "=== Example 2: London ==="
python weather.py --city "London"

# Example 3: Custom output file
echo ""
echo "=== Example 3: Custom output file ==="
python weather.py --city "Paris" --output paris_weather.csv

# Example 4: Direct coordinates (New York)
echo ""
echo "=== Example 4: Direct coordinates ==="
python weather.py --lat 40.7128 --lon -74.0060

# Example 5: Tokyo with custom timeout
echo ""
echo "=== Example 5: Custom timeout ==="
python weather.py --city "Tokyo" --timeout 15

# Example 6: View the CSV output
echo ""
echo "=== Example 6: View CSV content ==="
if [ -f weather_log.csv ]; then
    echo "Contents of weather_log.csv:"
    cat weather_log.csv
else
    echo "No weather_log.csv found"
fi

# Example 7: Append to existing file
echo ""
echo "=== Example 7: Append more data ==="
python weather.py --city "Berlin"
python weather.py --city "Madrid"
echo "Current weather_log.csv:"
cat weather_log.csv
