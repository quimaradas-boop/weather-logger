# Open-Meteo API Reference

Weather Logger uses the [Open-Meteo API](https://open-meteo.com/) for weather data retrieval. This API is free, requires no API key, and provides global coverage.

## API Endpoints

### 1. Geocoding API

Converts city names to geographic coordinates.

**Endpoint:** `https://geocoding-api.open-meteo.com/v1/search`

**Parameters:**
| Parameter | Type   | Description                          | Required |
|-----------|--------|--------------------------------------|----------|
| `name`    | string | City name to search for              | Yes      |
| `count`   | int    | Number of results to return (1-100)  | No       |
| `language`| string | Language for results (e.g., "en")  | No       |

**Example Request:**
```
https://geocoding-api.open-meteo.com/v1/search?name=Lisbon&count=1
```

**Example Response:**
```json
{
  "results": [
    {
      "id": 2267057,
      "name": "Lisbon",
      "latitude": 38.71667,
      "longitude": -9.13333,
      "elevation": 45.0,
      "feature_code": "PPLC",
      "country_code": "PT",
      "timezone": "Europe/Lisbon",
      "population": 517802,
      "country": "Portugal",
      "admin1": "Lisbon"
    }
  ]
}
```

### 2. Weather Forecast API

Retrieves current weather conditions.

**Endpoint:** `https://api.open-meteo.com/v1/forecast`

**Parameters:**
| Parameter     | Type   | Description                          | Required |
|---------------|--------|--------------------------------------|----------|
| `latitude`    | float  | Latitude (-90 to 90)                 | Yes      |
| `longitude`   | float  | Longitude (-180 to 180)            | Yes      |
| `current`     | string | Comma-separated weather variables    | Yes      |
| `timezone`    | string | Timezone (e.g., "auto")              | No       |

**Current Weather Variables Used:**
| Variable                | Unit    | Description                     |
|-------------------------|---------|---------------------------------|
| `temperature_2m`        | °C      | Air temperature at 2m height    |
| `relative_humidity_2m`  | %       | Relative humidity at 2m         |
| `wind_speed_10m`        | km/h    | Wind speed at 10m height        |
| `wind_direction_10m`    | degrees | Wind direction (0-360°)         |
| `surface_pressure`      | hPa     | Atmospheric pressure            |
| `weather_code`          | code    | WMO Weather interpretation code |

**Example Request:**
```
https://api.open-meteo.com/v1/forecast?latitude=38.71667&longitude=-9.13333&current=temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,surface_pressure,weather_code
```

**Example Response:**
```json
{
  "latitude": 38.71667,
  "longitude": -9.13333,
  "current": {
    "time": "2026-02-21T14:00",
    "interval": 900,
    "temperature_2m": 17.7,
    "relative_humidity_2m": 57,
    "wind_speed_10m": 11.5,
    "wind_direction_10m": 49,
    "surface_pressure": 1023.0,
    "weather_code": 1
  }
}
```

## Weather Codes (WMO)

The API returns numeric weather codes defined by the World Meteorological Organization:

| Code | Description                        |
|------|-------------------------------------|
| 0    | Clear sky                          |
| 1    | Mainly clear                       |
| 2    | Partly cloudy                      |
| 3    | Overcast                           |
| 45   | Fog                                |
| 48   | Depositing rime fog                |
| 51   | Light drizzle                      |
| 53   | Moderate drizzle                   |
| 55   | Dense drizzle                      |
| 61   | Slight rain                        |
| 63   | Moderate rain                      |
| 65   | Heavy rain                         |
| 71   | Slight snow fall                   |
| 73   | Moderate snow fall                 |
| 75   | Heavy snow fall                    |
| 95   | Thunderstorm                       |
| 96   | Thunderstorm with slight hail      |
| 99   | Thunderstorm with heavy hail       |

For a complete list, see [weather_codes.py](../weather.py#L15-L52).

## Rate Limits

Open-Meteo API has the following limits:
- **Anonymous requests:** 10,000 calls/day per IP
- **No authentication required**
- **Fair use policy:** Please be considerate of server resources

For production use with high volumes, consider:
- Caching geocoding results
- Batching requests when possible
- Self-hosting Open-Meteo (open source)

## Official Documentation

For complete API documentation, visit:
- [Open-Meteo Documentation](https://open-meteo.com/en/docs)
- [Geocoding API](https://open-meteo.com/en/docs/geocoding-api)
- [GitHub Repository](https://github.com/open-meteo/open-meteo)

## Error Handling

The API returns standard HTTP status codes:

| Status | Meaning                           |
|--------|-----------------------------------|
| 200    | Success                           |
| 400    | Bad request (invalid parameters)  |
| 404    | Location not found                |
| 429    | Rate limit exceeded               |
| 500    | Server error                      |
