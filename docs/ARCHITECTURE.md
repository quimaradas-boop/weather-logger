# Architecture & Implementation Details

This document describes the design principles and architecture of Weather Logger.

## Design Principles

1. **Zero Dependencies**: Uses only Python standard library
   - No external packages to install
   - Works on any system with Python 3.7+
   - No version conflicts or security concerns from dependencies

2. **Fail Gracefully**: Network errors don't crash the program
   - All network operations have timeouts
   - Errors are reported to stderr
   - Appropriate exit codes for scripting

3. **Data Integrity**: Atomic CSV writes with proper escaping
   - Uses Python's `csv.DictWriter` for correct escaping
   - UTF-8 encoding for international city names
   - Conditional headers prevent duplicate columns

4. **Extensibility**: Modular design for easy feature addition
   - Clean separation of concerns
   - Functions are testable in isolation
   - Easy to add new data sources or output formats

## Module Breakdown

### Main Script Structure

```python
weather.py
├── WEATHER_CODES          # Dictionary mapping WMO codes to descriptions
├── geocode_city()         # City name → coordinates
├── fetch_weather_data()   # Coordinates → weather data
├── save_to_csv()          # Data → CSV file
└── main()                 # CLI parsing and orchestration
```

### Function Details

#### `geocode_city(city, timeout=10)`
**Purpose:** Convert city name to latitude/longitude

**API:** Open-Meteo Geocoding API

**Returns:** `Tuple[float, float]` or `None`

**Error Handling:**
- Returns `None` on network errors
- Returns `None` if city not found
- Prints error to stderr

#### `fetch_weather_data(lat, lon, timeout=10)`
**Purpose:** Fetch current weather for given coordinates

**API:** Open-Meteo Weather Forecast API

**Returns:** `Dict[str, Any]` or `None`

**Validation:**
- Latitude: -90 to 90
- Longitude: -180 to 180

**Data Transformation:**
- Maps WMO weather codes to human-readable strings
- Extracts relevant fields from API response

#### `save_to_csv(data, location, lat, lon, filename)`
**Purpose:** Append weather data to CSV file

**CSV Strategy:**
- Check file existence to determine header needs
- Use `csv.DictWriter` for proper escaping
- Append mode with newline handling

#### `main()`
**Purpose:** CLI entry point and orchestration

**Argument Parsing:**
```
--city CITY        City name to geocode
--lat LAT          Latitude coordinate
--lon LON          Longitude coordinate
--output FILE      Output CSV filename (default: weather_log.csv)
--timeout SECONDS  HTTP timeout (default: 10)
```

**Logic Flow:**
1. Parse arguments
2. Validate argument combinations
3. Resolve location (coordinates or geocode city)
4. Fetch weather data
5. Save to CSV
6. Print summary
7. Exit with appropriate code

## Error Handling Strategy

| Error Type          | Handling                                  | Exit Code |
|---------------------|-------------------------------------------|-----------|
| Network timeout     | Print to stderr, exit                     | 1         |
| HTTP 4xx            | Print to stderr, exit                     | 1         |
| City not found      | Print to stderr, exit                     | 1         |
| Invalid coordinates | Print to stderr, exit                     | 1         |
| CSV write error     | Print to stderr, exit                     | 1         |
| Generic error       | Print to stderr, exit                     | 1         |

## Exit Codes

| Code | Meaning          |
|------|------------------|
| 0    | Success          |
| 1    | Error occurred   |

(Note: Currently uses simplified exit codes; could be expanded)

## Data Flow

```
┌─────────────────┐
│  CLI Arguments  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Parse & Validate│
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│  City provided? │────▶│  Geocode API    │
└─────────────────┘     └────────┬────────┘
         │ No                    │
         ▼                       │
┌─────────────────┐              │
│  Use coordinates│◀─────────────┘
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Weather API    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Transform Data │ (WMO codes → text)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Write CSV      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Print Summary  │
└─────────────────┘
```

## API Integration Details

### Geocoding
- Uses `urllib.request` for HTTP
- JSON parsing with `json` module
- URL encoding with `urllib.parse.quote`

### Weather Data
- Same HTTP stack as geocoding
- Timeout of 10 seconds on all requests
- Validates coordinate ranges before API call

### CSV Writing
- Uses `csv.DictWriter` for proper escaping
- Checks file existence via exception handling
- UTF-8 encoding for international support

## Security Considerations

1. **No API keys stored** - Uses public Open-Meteo API
2. **Input validation** - Validates coordinates before API calls
3. **URL encoding** - Properly escapes city names in URLs
4. **No shell execution** - All arguments passed safely
5. **File permissions** - Uses standard Python file I/O

## Performance Characteristics

- **Memory usage:** Minimal (~KB)
- **Network requests:** 1-2 HTTP requests per run
- **Disk I/O:** Single append operation
- **CPU usage:** Negligible

## Potential Enhancements

Future versions could include:

1. **Caching layer** - Cache geocoding results locally
2. **Configuration file** - Default location, output path
3. **Multiple formats** - JSON, XML output options
4. **Forecast support** - Log future weather predictions
5. **Batch mode** - Process multiple locations
6. **Data validation** - Schema validation on write
7. **Compression** - Gzip old log files

## Testing Strategy

Recommended test coverage:

1. **Unit tests** - Mock API responses
2. **Integration tests** - Real API calls
3. **Edge cases** - Invalid inputs, network failures
4. **CSV validation** - Output format verification

## Compatibility

- **Python 3.7+** - Uses dataclasses (3.7+), type hints
- **Cross-platform** - Works on Linux, macOS, Windows
- **No external deps** - Pure standard library
