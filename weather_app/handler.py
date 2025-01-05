from .weather_secrets import API_KEY
from django.conf import settings
import requests

DIRECTIONS = {
    "N": "North",
    "E": "East",
    "S": "South",
    "W": "West",

    }

class Formatter:
    @staticmethod
    def format_current_weather_response(data: dict) -> dict:
        formatted_data = {
            "location": data['location']['name'],
            "region": data['location']['region'],
            "time": data['location']['localtime'],
            "timezone": data['location']['tz_id'],
            "latitude": data['location']['lat'],
            "longitude": data['location']['lon'],
            "temperature_c": data['current']['temp_c'],
            "temperature_f": data['current']['temp_f'],
            "condition": data['current']['condition']['text'],
            "icon": data['current']['condition']['icon'],
            "feels_like_c": data['current']['feelslike_c'],
            "feels_like_f": data['current']['feelslike_f'],
            "wind_kph": data['current']['wind_kph'],
            "wind_mph": data['current']['wind_mph'],
            "wind_direction": " ".join([DIRECTIONS[direction] for direction in list((data['current']['wind_dir']))]),
            "humidity": data['current']['humidity'],    
            "cloud": data['current']['cloud'],
            "precip_mm": data['current']['precip_mm'],
            "pressure_mb": data['current']['pressure_mb'],
            "uv": data['current']['uv'],
            "visibility_km": data['current']['vis_km'],
            "visibility_miles": data['current']['vis_miles'],
            "last_updated": data['current']['last_updated'],
            "heat_index_c": data['current']['heatindex_c'],
            "heat_index_f": data['current']['heatindex_f'],
            "gust_kph": data['current']['gust_kph'],
            "gust_mph": data['current']['gust_mph'],

        }
        return formatted_data

    @staticmethod
    def format_forecast_response(data: dict, current: bool, hourly_forecast: bool) -> dict:
        forecast = []
        for day in data['forecast']['forecastday']:
            formatted_day = {
                "date": day['date'],
                "max_temp_c": day['day']['maxtemp_c'],
                "max_temp_f": day['day']['maxtemp_f'],
                "min_temp_c": day['day']['mintemp_c'],
                "min_temp_f": day['day']['mintemp_f'],
                "avg_temp_c": day['day']['avgtemp_c'],
                "avg_temp_f": day['day']['avgtemp_f'],
                "condition": day['day']['condition']['text'],
                "icon": day['day']['condition']['icon'],
                "max_wind_kph": day['day']['maxwind_kph'],
                "max_wind_mph": day['day']['maxwind_mph'],
                "total_precip_mm": day['day']['totalprecip_mm'],
                "total_precip_in": day['day']['totalprecip_in'],
                "daily_chance_of_rain": day['day']['daily_chance_of_rain'],
                "avg_visibility_km": day['day']['avgvis_km'],
                "avg_visibility_miles": day['day']['avgvis_miles'],
                "avg_humidity": day['day']['avghumidity'],
                "sunrise": day['astro']['sunrise'],
                "sunset": day['astro']['sunset'],
                "moonrise": day['astro']['moonrise'],
                "moonset": day['astro']['moonset'],
                "moon_phase": day['astro']['moon_phase'],
                "moon_illumination": day['astro']['moon_illumination'],
            }
            forecast.append(formatted_day)
        
        response = {"forecast": forecast}

        if current is True:
            current = Formatter.format_current_weather_response(data)
            response.update({"current": current})
        
        if hourly_forecast is True:
            hourly_forecast = []
            for hour in data['forecast']['forecastday'][0]['hour']:
                formatted_hour = {
                    "time": hour['time'],
                    "temp_c": hour['temp_c'],
                    "temp_f": hour['temp_f'],
                    "condition": hour['condition']['text'],
                    "icon": hour['condition']['icon'],
                    "wind_kph": hour['wind_kph'],
                    "wind_mph": hour['wind_mph'],
                    "wind_direction": " ".join([DIRECTIONS[direction] for direction in list((hour['wind_dir']))]),
                    "humidity": hour['humidity'],
                    "cloud": hour['cloud'],
                    "precip_mm": hour['precip_mm'],
                    "pressure_mb": hour['pressure_mb'],
                    "uv": hour['uv'],
                    "visibility_km": hour['vis_km'],
                    "visibility_miles": hour['vis_miles'],
                    "heat_index_c": hour['heatindex_c'],
                    "heat_index_f": hour['heatindex_f'],
                    "gust_kph": hour['gust_kph'],
                    "gust_mph": hour['gust_mph'],
                }
                hourly_forecast.append(formatted_hour)

            response.update({"hourly_forecast": hourly_forecast})
        
        
        return response

    def format_astronomy_response(data: dict) -> dict:
        formatted_data = {
            "location": data['location']['name'],
            "region": data['location']['region'],
            "time": data['location']['localtime'],
            "timezone": data['location']['tz_id'],
            "latitude": data['location']['lat'],
            "longitude": data['location']['lon'],
            "sunrise": data['astronomy']['astro']['sunrise'],
            "sunset": data['astronomy']['astro']['sunset'],
            "moonrise": data['astronomy']['astro']['moonrise'],
            "moonset": data['astronomy']['astro']['moonset'],
            "moon_phase": data['astronomy']['astro']['moon_phase'],
            "moon_illumination": data['astronomy']['astro']['moon_illumination'],
            "is_moon_up": bool(data['astronomy']['astro']['is_moon_up']),
            "is_sun_up": bool(data['astronomy']['astro']['is_sun_up'])
        }
        return formatted_data

class WeatherHandler:
    def __init__(self, city: str):
        self.city = city
    def get_weather(self) -> dict | None:
        url = f"{settings.WEATHER_BASE_URL}/current.json?key={API_KEY}&q={self.city}"
        response = requests.get(url)
        if response.status_code != 200:
            return None
        data = response.json()
        return Formatter.format_current_weather_response(data)

    def get_forecast(self, days: int, current: bool, hourly_forecast: bool) -> dict | None:
        url = f"{settings.WEATHER_BASE_URL}/forecast.json?key={API_KEY}&q={self.city}&days={days}"
        response = requests.get(url)
        if response.status_code != 200:
            return None
        data = response.json()
        return Formatter.format_forecast_response(data, current=current, hourly_forecast=hourly_forecast)

    def get_astronomy(self) -> dict | None:
        url = f"{settings.WEATHER_BASE_URL}/astronomy.json?key={API_KEY}&q={self.city}"
        response = requests.get(url)
        if response.status_code != 200:
            return None
        data = response.json()
        return Formatter.format_astronomy_response(data)

