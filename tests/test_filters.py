from django.urls import reverse
from rest_framework.test import APITestCase

from history.models import UserHistory
from history.serializers import UserHistorySerializer
from users.models import User


class FiltersTestCase(APITestCase):
    def setUp(self):
        self.testuser = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.history1 = UserHistory.objects.create(
            city="Makhachkala",
            temp=0.99,
            temp_max=0.99,
            temp_min=0.99,
            humidity=70,
            wind_speed=4.48,
            wind_direction=349,
            weather="Clouds",
            weather_desc="overcast clouds",
            timestamp="2025-02-07T16:13:49",
            sunrise="2025-02-07T06:58:20",
            sunset="2025-02-07T17:09:59",
            user=self.testuser,
        )
        self.history2 = UserHistory.objects.create(
            city="London",
            temp=4.13,
            temp_max=4.86,
            temp_min=3.12,
            humidity=85,
            wind_speed=8.75,
            wind_direction=70,
            weather="Clear",
            weather_desc="clear sky",
            timestamp="2025-02-07T16:13:49",
            sunrise="2025-02-07T06:58:20",
            sunset="2025-02-07T17:09:59",
            user=self.testuser,
        )
        self.history3 = UserHistory.objects.create(
            city="Paris",
            temp=6.98,
            temp_max=7.43,
            temp_min=6.7,
            humidity=72,
            wind_speed=5.66,
            wind_direction=150,
            weather="Clouds",
            weather_desc="overcast clouds",
            timestamp="2025-02-08T19:09:38",
            sunrise="2025-02-08T10:10:28",
            sunset="2025-02-08T19:59:12",
            user=self.testuser,
        )
        self.history_serializer = UserHistorySerializer(
            instance=[self.history1, self.history2, self.history3], many=True
        )

        token_obtain_pair_url = reverse("token_obtain_pair")
        register_url = reverse("register")

        self.access_token = self.client.post(
            token_obtain_pair_url,
            data={"username": self.testuser.username, "password": "testpassword"},
            format="json",
        ).data["access"]

    def test_filter_by_city(self):
        url = reverse("history-list")
        response = self.client.get(
            url,
            {"city": "London"},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0], self.history_serializer.data[1])

    def test_filter_by_date(self):
        url = reverse("history-list")
        response = self.client.get(
            url,
            {"timestamp": "2025-02-08T19:09:38"},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0], self.history_serializer.data[2])

    def test_search(self):
        url = reverse("history-list")
        response = self.client.get(
            url,
            {"search": "London"},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0], self.history_serializer.data[1])

    def test_search_by_timestamp(self):
        url = reverse("history-list")
        response = self.client.get(
            url,
            {"search": "2025-02-08"},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0], self.history_serializer.data[2])

    def test_search_by_weather(self):
        url = reverse("history-list")
        response = self.client.get(
            url,
            {"search": "Clear"},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0], self.history_serializer.data[1])

    def test_ordering(self):
        url = reverse("history-list")
        response = self.client.get(
            url,
            {"ordering": "-temp"},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0], self.history_serializer.data[2])

        response = self.client.get(
            url,
            {"ordering": "city"},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0], self.history_serializer.data[1])

        response = self.client.get(
            url,
            {"ordering": "-sunset"},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0], self.history_serializer.data[2])

