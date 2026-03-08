import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path so we can import weather
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import weather


class TestWeatherFunctions(unittest.TestCase):
    
    def test_weather_codes_mapping(self):
        """Test that weather codes map correctly to conditions"""
        self.assertEqual(weather.WEATHER_CODES[0], "Clear sky")
        self.assertEqual(weather.WEATHER_CODES[45], "Fog")
        self.assertEqual(weather.WEATHER_CODES[95], "Thunderstorm")
        self.assertEqual(weather.WEATHER_CODES[99], "Thunderstorm with heavy hail")
        # Test edge cases
        self.assertEqual(weather.WEATHER_CODES.get(999, "Unknown"), "Unknown")
        self.assertEqual(weather.WEATHER_CODES.get(100, "Unknown"), "Unknown")
        
    def test_geocode_city_success(self):
        """Test successful geocoding of a city"""
        with patch('weather.urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = b'{"results": [{"latitude": 38.7223, "longitude": -9.1393}]}'  
            mock_urlopen.return_value = mock_response
            
            result = weather.geocode_city("Lisbon")
            self.assertEqual(result, (38.7223, -9.1393))
    
    def test_geocode_city_failure(self):
        """Test geocoding failure"""
        with patch('weather.urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = b'{"results": []}'  
            mock_urlopen.return_value = mock_response
            
            result = weather.geocode_city("InvalidCity")
            self.assertIsNone(result)
    
    @patch('weather.geocode_city')
    def test_fetch_weather_data_success(self, mock_geocode):
        """Test successful weather data fetch"""
        mock_geocode.return_value = (38.7223, -9.1393)
        
        with patch('weather.urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = b'{"current": {"temperature_2m": 22.5, "relative_humidity_2m": 65, "wind_speed_10m": 12.3, "wind_direction_10m": 180, "surface_pressure": 1013.25, "weather_code": 0}}'
            mock_urlopen.return_value = mock_response
            
            result = weather.fetch_weather_data(38.7223, -9.1393)
            expected = {
                'temperature_c': 22.5,
                'humidity_percent': 65,
                'wind_speed_kmh': 12.3,
                'wind_direction_deg': 180,
                'pressure_hpa': 1013.25,
                'conditions': "Clear sky"
            }
            self.assertEqual(result, expected)
    
    @patch('weather.geocode_city')
    def test_fetch_weather_data_failure(self, mock_geocode):
        """Test weather data fetch failure"""
        mock_geocode.return_value = (38.7223, -9.1393)
        
        with patch('weather.urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.side_effect = Exception("Connection error")
            
            result = weather.fetch_weather_data(38.7223, -9.1393)
            self.assertIsNone(result)
    
    def test_fetch_weather_data_invalid_coordinates(self):
        """Test weather data fetch with invalid coordinates"""
        with self.assertRaises(ValueError):
            weather.fetch_weather_data(100, 0)  # Invalid latitude
            
        with self.assertRaises(ValueError):
            weather.fetch_weather_data(0, 200)  # Invalid longitude
    
    @patch('weather.datetime')
    def test_save_to_csv(self, mock_datetime):
        """Test saving to CSV"""
        # Mock datetime to return a fixed timestamp
        mock_datetime.now.return_value.isoformat.return_value = "2023-01-01T12:00:00"
        
        # Create a temporary CSV file for testing
        test_filename = "test_weather_output.csv"
        
        try:
            data = {
                'temperature_c': 22.5,
                'humidity_percent': 65,
                'wind_speed_kmh': 12.3,
                'wind_direction_deg': 180,
                'pressure_hpa': 1013.25,
                'conditions': "Clear sky"
            }
            
            weather.save_to_csv(data, "Test City", 38.7223, -9.1393, test_filename)
            
            # Check that file was created and has content
            with open(test_filename, 'r') as f:
                content = f.read()
                self.assertIn("2023-01-01T12:00:00", content)
                self.assertIn("Test City", content)
                
        finally:
            # Clean up test file
            if os.path.exists(test_filename):
                os.remove(test_filename)


if __name__ == '__main__':
    unittest.main()