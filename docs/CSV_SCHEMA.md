# CSV Schema Specification

Weather Logger stores weather data in CSV format with the following schema.

## File Format

- **Encoding:** UTF-8
- **Delimiter:** Comma (`,`)  
- **Line Ending:** System default (`\n` on Unix, `\r\n` on Windows)
- **Quote Character:** Double quote (`"`)
- **Header Row:** Included in new files only

## Column Specification

| #  | Column Name          | Type    | Unit    | Description                            | Example                    |
|----|----------------------|---------|---------|----------------------------------------|----------------------------|
| 1  | `timestamp`          | string  | ISO8601 | UTC timestamp when data was logged     | `2026-02-21T14:07:24`      |
| 2  | `location`           | string  | -       | City name or "Provided coordinates"    | `Lisbon`                   |
| 3  | `latitude`           | float   | degrees | Latitude (-90 to 90)                   | `38.71667`                 |
| 4  | `longitude`          | float   | degrees | Longitude (-180 to 180)                | `-9.13333`                 |
| 5  | `temperature_c`      | float   | °C      | Air temperature at 2m height           | `17.7`                     |
| 6  | `humidity_percent`   | int     | %       | Relative humidity (0-100)              | `57`                       |
| 7  | `wind_speed_kmh`     | float   | km/h    | Wind speed at 10m height               | `11.5`                     |
| 8  | `wind_direction_deg` | int     | degrees | Wind direction (0-360, 0 = North)      | `49`                       |
| 9  | `conditions`         | string  | -       | Human-readable weather condition       | `Mainly clear`             |
| 10 | `pressure_hpa`       | float   | hPa     | Atmospheric pressure                   | `1023.0`                   |

## Example Data

### Header Row
```csv
timestamp,location,latitude,longitude,temperature_c,humidity_percent,wind_speed_kmh,wind_direction_deg,conditions,pressure_hpa
```

### Sample Rows
```csv
2026-02-21T14:07:24.949823,Lisbon,38.71667,-9.13333,17.7,57,11.5,49,Mainly clear,1023.0
2026-02-21T15:07:24.123456,London,51.50853,-0.12574,12.3,72,18.2,235,Light rain,1012.5
2026-02-21T16:07:24.789012,Provided coordinates,40.7128,-74.006,22.5,45,8.3,120,Clear sky,1015.2
```

## Data Types

### timestamp
- **Format:** ISO 8601 with microseconds
- **Timezone:** Local system time
- **Example:** `2026-02-21T14:07:24.949823`

### location
- **Source:** Either city name from geocoding or "Provided coordinates"
- **Encoding:** UTF-8, properly escaped for CSV
- **Special characters:** Escaped with double quotes if contains comma

### Coordinates (latitude, longitude)
- **Precision:** Up to 5 decimal places
- **Range:** 
  - Latitude: -90.0 to 90.0
  - Longitude: -180.0 to 180.0

### Numeric Values
- **temperature_c:** Decimal with 1 decimal place
- **humidity_percent:** Integer, 0-100
- **wind_speed_kmh:** Decimal with 1 decimal place
- **wind_direction_deg:** Integer, 0-360
- **pressure_hpa:** Decimal with 1 decimal place

### conditions
- **Source:** WMO weather code mapping
- **Values:** See [API.md](API.md#weather-codes-wmo) for complete list
- **Common values:**
  - Clear sky
  - Mainly clear
  - Partly cloudy
  - Overcast
  - Light rain
  - Moderate rain
  - Heavy rain

## Appending Behavior

When logging to an existing file:
1. Check if file exists
2. If file exists → append new row without header
3. If file is new → write header row first, then data row

This allows for easy continuous logging over time.

## Analysis Examples

### Load with Pandas
```python
import pandas as pd

# Load CSV
df = pd.read_csv('weather_log.csv')

# Convert timestamp
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Basic stats
print(df['temperature_c'].describe())
```

### Load with Python CSV
```python
import csv

with open('weather_log.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['location']}: {row['temperature_c']}°C")
```

### Command Line
```bash
# View last 10 entries
tail -n 10 weather_log.csv

# Extract temperatures only
cut -d',' -f5 weather_log.csv

# Count entries per location
cut -d',' -f2 weather_log.csv | sort | uniq -c
```
