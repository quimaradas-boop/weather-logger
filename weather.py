#!/usr/bin/env python3
"""
Weather script that fetches current weather data from Open-Meteo API
and saves it to a CSV file.
"""

import argparse
import csv
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime
from typing import Dict, Optional, Tuple


# Weather code mapping (WMO codes to readable conditions)
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}


def geocode_city(city: str, timeout: int = 10) -> Optional[Tuple[float, float]]:
    """
    Geocode a city name to latitude and longitude.
    
    Args:
        city (str): City name to geocode
        timeout (int): Timeout in seconds for the request
        
    Returns:
        Optional[Tuple[float, float]]: Tuple of (latitude, longitude) or None if failed
    """
    try:
        # Build the URL for geocoding
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city)}&count=1"
        
        # Make the request with timeout
        response = urllib.request.urlopen(url, timeout=timeout)
        data = json.loads(response.read().decode())
        
        if not data or 'results' not in data or len(data['results']) == 0:
            return None
            
        result = data['results'][0]
        return (result['latitude'], result['longitude'])
        
    except (urllib.error.URLError, json.JSONDecodeError, KeyError) as e:
        print(f"Error geocoding city '{city}': {e}", file=sys.stderr)
        return None


def fetch_weather_data(lat: float, lon: float, timeout: int = 10) -> Optional[Dict]:
    """
    Fetch current weather data for given coordinates.
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        timeout (int): Timeout in seconds for the request
        
    Returns:
        Optional[Dict]: Weather data dictionary or None if failed
    """
    # Validate coordinates
    if not (-90 <= lat <= 90):
        raise ValueError(f"Invalid latitude: {lat}. Must be between -90 and 90.")
    if not (-180 <= lon <= 180):
        raise ValueError(f"Invalid longitude: {lon}. Must be between -180 and 180.")
    
    try:
        # Build the URL for weather data
        url = (f"https://api.open-meteo.com/v1/forecast?"
               f"latitude={lat}&longitude={lon}&"
               f"current=temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,surface_pressure,weather_code")
        
        # Make the request with timeout
        response = urllib.request.urlopen(url, timeout=timeout)
        data = json.loads(response.read().decode())
        
        if not data or 'current' not in data:
            return None
            
        current = data['current']
        
        # Map weather code to readable condition
        weather_code = current.get('weather_code', 0)
        condition = WEATHER_CODES.get(weather_code, "Unknown")
        
        return {
            'temperature_c': current.get('temperature_2m', 0),
            'humidity_percent': current.get('relative_humidity_2m', 0),
            'wind_speed_kmh': current.get('wind_speed_10m', 0),
            'wind_direction_deg': current.get('wind_direction_10m', 0),
            'pressure_hpa': current.get('surface_pressure', 0),
            'conditions': condition
        }
        
    except (urllib.error.URLError, json.JSONDecodeError, KeyError) as e:
        print(f"Error fetching weather data for coordinates ({lat}, {lon}): {e}", file=sys.stderr)
        return None


def save_to_csv(data: Dict, location: str, lat: float, lon: float, filename: str):
    """
    Save weather data to CSV file.
    
    Args:
        data (Dict): Weather data dictionary
        location (str): Location name
        lat (float): Latitude
        lon (float): Longitude
        filename (str): Output CSV filename
    """
    # Prepare the row data
    row = {
        'timestamp': datetime.now().isoformat(),
        'location': location,
        'latitude': lat,
        'longitude': lon,
        'temperature_c': data['temperature_c'],
        'humidity_percent': data['humidity_percent'],
        'wind_speed_kmh': data['wind_speed_kmh'],
        'wind_direction_deg': data['wind_direction_deg'],
        'conditions': data['conditions'],
        'pressure_hpa': data['pressure_hpa']
    }
    
    # Check if file exists to determine if we need to write header
    file_exists = False
    try:
        with open(filename, 'r') as _:
            file_exists = True
    except FileNotFoundError:
        pass
    
    # Write to CSV
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['timestamp', 'location', 'latitude', 'longitude', 'temperature_c',
                     'humidity_percent', 'wind_speed_kmh', 'wind_direction_deg', 'conditions', 'pressure_hpa']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
            
        writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(description='Fetch current weather and save to CSV')
    parser.add_argument('--city', help='City name to geocode (default: Lisbon)')
    parser.add_argument('--lat', type=float, help='Latitude coordinate')
    parser.add_argument('--lon', type=float, help='Longitude coordinate')
    parser.add_argument('--output', default='weather_log.csv', help='Output CSV filename (default: weather_log.csv)')
    parser.add_argument('--timeout', type=int, default=10, help='HTTP timeout in seconds (default: 10)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.lat is not None and args.lon is None:
        print("Error: --lon is required when --lat is specified", file=sys.stderr)
        sys.exit(1)
    if args.lon is not None and args.lat is None:
        print("Error: --lat is required when --lon is specified", file=sys.stderr)
        sys.exit(1)
    
    # Determine location coordinates
    if args.lat is not None and args.lon is not None:
        # Use provided coordinates
        lat = args.lat
        lon = args.lon
        location = "Provided coordinates"
    elif args.city:
        # Geocode the city
        coords = geocode_city(args.city, args.timeout)
        if not coords:
            print(f"Error: Could not geocode city '{args.city}'", file=sys.stderr)
            sys.exit(1)
        lat, lon = coords
        location = args.city
    else:
        # Default to Lisbon
        coords = geocode_city("Lisbon", args.timeout)
        if not coords:
            print("Error: Could not geocode default city 'Lisbon'", file=sys.stderr)
            sys.exit(1)
        lat, lon = coords
        location = "Lisbon"
    
    # Fetch weather data
    weather_data = fetch_weather_data(lat, lon, args.timeout)
    if not weather_data:
        print("Error: Could not fetch weather data", file=sys.stderr)
        sys.exit(1)
    
    # Save to CSV
    save_to_csv(weather_data, location, lat, lon, args.output)
    
    # Print summary
    print(f"Weather data saved to {args.output}")
    print(f"Location: {location} ({lat}, {lon})")
    print(f"Temperature: {weather_data['temperature_c']}°C")
    print(f"Humidity: {weather_data['humidity_percent']}%")
    print(f"Wind Speed: {weather_data['wind_speed_kmh']} km/h")
    print(f"Wind Direction: {weather_data['wind_direction_deg']}°")
    print(f"Pressure: {weather_data['pressure_hpa']} hPa")
    print(f"Conditions: {weather_data['conditions']}")


if __name__ == "__main__":
    main()