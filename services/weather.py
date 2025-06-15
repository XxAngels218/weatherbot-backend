import os
import aiohttp
import logging
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY environment variable is not set")
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
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"Successfully retrieved weather for {city}")
                        return data
                    elif response.status == 401:
                        logger.error("Invalid API key for OpenWeather")
                        raise ValueError("Invalid OpenWeather API key")
                    elif response.status == 404:
                        logger.error(f"City not found: {city}")
                        raise ValueError(f"City not found: {city}")
                    else:
                        error_text = await response.text()
                        logger.error(f"OpenWeather API error: {error_text}")
                        raise Exception(f"OpenWeather API error: {error_text}")
        except aiohttp.ClientError as e:
            logger.error(f"Network error while fetching weather: {str(e)}")
            raise Exception(f"Network error while fetching weather: {str(e)}")
    
    async def get_forecast(self, city: str) -> Dict[str, Any]:
        """Get 5-day weather forecast for a city"""
        url = f"{self.base_url}/forecast"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
            "lang": "en"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"Successfully retrieved forecast for {city}")
                        return data
                    elif response.status == 401:
                        logger.error("Invalid API key for OpenWeather")
                        raise ValueError("Invalid OpenWeather API key")
                    elif response.status == 404:
                        logger.error(f"City not found: {city}")
                        raise ValueError(f"City not found: {city}")
                    else:
                        error_text = await response.text()
                        logger.error(f"OpenWeather API error: {error_text}")
                        raise Exception(f"OpenWeather API error: {error_text}")
        except aiohttp.ClientError as e:
            logger.error(f"Network error while fetching forecast: {str(e)}")
            raise Exception(f"Network error while fetching forecast: {str(e)}")
    
    def format_weather_response(self, data: Dict[str, Any]) -> str:
        """Format weather data into a human-readable response"""
        try:
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
        except KeyError as e:
            logger.error(f"Error formatting weather response: {str(e)}")
            return "Error formatting weather information." 