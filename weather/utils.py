import requests
from datetime import datetime

from app import settings
from users.models import User


def get_weather_data(
    city, api_key=settings.WEATHER_API_TOKEN, units="metric", request=None
):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}"
    owm_response = requests.get(url, timeout=10).json()

    try:
        responce_data = {
            "city": owm_response.get("name"),
            "temp": owm_response["main"].get("temp"),
            "temp_max": owm_response["main"].get("temp_max"),
            "temp_min": owm_response["main"].get("temp_min"),
            "humidity": owm_response["main"].get("humidity"),
            "wind_speed": owm_response["wind"].get("speed"),
            "wind_direction": owm_response["wind"].get("deg"),
            "weather": owm_response["weather"][0].get("main"),
            "weather_desc": owm_response["weather"][0].get("description"),
            "timestamp": datetime.fromtimestamp(owm_response.get("dt")),
            "sunrise": datetime.fromtimestamp(owm_response["sys"].get("sunrise")),
            "sunset": datetime.fromtimestamp(owm_response["sys"].get("sunset")),
        }

    except (KeyError, TypeError):
        responce_data = {
            "error": owm_response["cod"],
            "error_message": owm_response["message"],
        }

    return responce_data
