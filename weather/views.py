from datetime import datetime
import os
from dotenv import find_dotenv, load_dotenv

from rest_framework.views import APIView
from rest_framework.response import Response


from app import settings
from history.models import UserHistory
from weather.utils import get_weather_data
# Create your views here.
class WeatherView(APIView):
    def get(self, request,  *args, **kwargs):
        weather_data = get_weather_data(kwargs.get('city'), settings.WEATHER_API_TOKEN)

        try:
            responce_data = {
                'user': request.user.id,
                'city': weather_data.get('name'),

                'temp': weather_data["main"].get('temp'),
                'temp_max': weather_data["main"].get('temp_max'),
                'temp_min': weather_data["main"].get('temp_min'),
                'humidity': weather_data["main"].get('humidity'),
                'wind_speed': weather_data["wind"].get('speed'),
                'wind_direction': weather_data["wind"].get('deg'),

                'weather': weather_data["weather"][0].get('main'),
                'weather_desc': weather_data["weather"][0].get('description'),

                # 'timestamp': datetime.fromtimestamp(weather_data.get('dt')).utcoffset(),
                'timestamp': datetime.fromtimestamp(weather_data.get('dt')),
                'sunrise': datetime.fromtimestamp(weather_data["sys"].get('sunrise')),
                'sunset': datetime.fromtimestamp(weather_data["sys"].get('sunset')),

            }

            if request.user.is_authenticated:
                responce_data['user'] = request.user
                UserHistory.objects.create(**responce_data)

            responce_data['user'] = request.user.id
        except KeyError:
            responce_data = {
                "error": weather_data["cod"],
                "error_message": weather_data["message"] 
            }

        return Response(responce_data)
