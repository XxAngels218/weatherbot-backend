import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
    async def get_current_weather(self, city: str) -> Dict[str, Any]:
        """Get current weather for a city"""
        url = f"{self.base_url}/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
            "lang": "en"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    async def get_forecast(self, city: str) -> Dict[str, Any]:
        """Get 5-day weather forecast for a city"""
        url = f"{self.base_url}/forecast"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
            "lang": "en"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def format_weather_response(self, data: Dict[str, Any]) -> str:
        """Format weather data into a human-readable response"""
        if "main" in data:  # Current weather
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            description = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            
            return f"🌤️ Current Weather:\n" \
                   f"Temperature: {temp}°C\n" \
                   f"Feels like: {feels_like}°C\n" \
                   f"Conditions: {description}\n" \
                   f"Humidity: {humidity}%"
        
        elif "list" in data:  # Forecast
            forecast = data["list"][0]  # Get first forecast
            temp = forecast["main"]["temp"]
            description = forecast["weather"][0]["description"]
            dt_txt = forecast["dt_txt"]
            
            return f"📅 Forecast for {dt_txt}:\n" \
                   f"Temperature: {temp}°C\n" \
                   f"Conditions: {description}"
        
        return "Could not retrieve weather information." 