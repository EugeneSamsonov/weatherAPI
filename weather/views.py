from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


from history.models import UserHistory
from weather.utils import get_weather_data


# Create your views here.
class WeatherView(APIView):
    def get(self, request, *args, **kwargs):
        cache_name = f"{kwargs.get('city')}"
        if cache_name in cache:
            responce_data = cache.get(cache_name)

            if request.user.is_authenticated:
                UserHistory.objects.get_or_create(
                    **responce_data, user_id=request.user.id
                )

            return Response(responce_data, status=status.HTTP_200_OK)

        responce_data = get_weather_data(kwargs.get("city"), request=request)

        if "error" in responce_data:
            return Response(responce_data, status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_authenticated:
            UserHistory.objects.get_or_create(**responce_data, user_id=request.user.id)

        cache.set(cache_name, responce_data, 10 * 60)  # on 10 min

        return Response(responce_data, status=status.HTTP_200_OK)
