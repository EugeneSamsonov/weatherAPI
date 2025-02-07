from django.test import SimpleTestCase
from django.urls import resolve, reverse

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# from history.views import UserHistoryViewSet
from users.views import UserRegisterAPIView
from weather.views import WeatherView


class UrlsTestCase(SimpleTestCase):

    def test_weather_url(self):
        url = reverse('weather_api', args=['city'])
        self.assertEqual(resolve(url).func.view_class, WeatherView)

    def test_url_history_list(self):
        # url = '/api/v1/history/'
        url = reverse('history-list')
        from history.views import UserHistoryViewSet
        self.assertEqual(resolve(url).func, UserHistoryViewSet)
    
    # def test_url_history_detail(self):
    #     url = '/api/v1/history/1/'
    #     self.assertEqual(resolve(url).func, UserHistoryViewSet)

    def test_register_url(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func.view_class, UserRegisterAPIView)
    
    def test_jwt_auth_url(self):
        url = reverse('token_obtain_pair')
        self.assertEqual(resolve(url).func.view_class, TokenObtainPairView)
    
    def test_jwt_refresh_token_url(self):
        url = reverse('token_refresh')
        self.assertEqual(resolve(url).func.view_class, TokenRefreshView)

