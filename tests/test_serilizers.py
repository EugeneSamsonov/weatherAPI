from django.test import TestCase

from users.models import User
from history.models import UserHistory
from history.serializers import UserHistorySerializer
from users.serializers import UserRegisterSerializer


class SerializersTestCase(TestCase):
    def test_history_serializer(self):
        testuser = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        history1 = UserHistory.objects.create(
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
            user=testuser,
        )
        history2 = UserHistory.objects.create(
            city="London",
            temp=4.13,
            temp_max=4.86,
            temp_min=3.12,
            humidity=85,
            wind_speed=8.75,
            wind_direction=70,
            weather="Clouds",
            weather_desc="overcast clouds",
            timestamp="2025-02-07T16:13:49",
            sunrise="2025-02-07T06:58:20",
            sunset="2025-02-07T17:09:59",
            user=testuser,
        )

        excepted_data = [
            {
                "id": history1.id,
                "city": "Makhachkala",
                "temp": "0.99",
                "temp_max": "0.99",
                "temp_min": "0.99",
                "humidity": 70,
                "wind_speed": "4.48",
                "wind_direction": 349,
                "weather": "Clouds",
                "weather_desc": "overcast clouds",
                "timestamp": "2025-02-07T16:13:49",
                "sunrise": "2025-02-07T06:58:20",
                "sunset": "2025-02-07T17:09:59",
                "user": testuser.id,
            },
            {
                "id": history2.id,
                "city": "London",
                "temp": "4.13",
                "temp_max": "4.86",
                "temp_min": "3.12",
                "humidity": 85,
                "wind_speed": "8.75",
                "wind_direction": 70,
                "weather": "Clouds",
                "weather_desc": "overcast clouds",
                "timestamp": "2025-02-07T16:13:49",
                "sunrise": "2025-02-07T06:58:20",
                "sunset": "2025-02-07T17:09:59",
                "user": testuser.id,
            },
        ]
        
        history_serializer = UserHistorySerializer(instance=[history1, history2], many=True)

        self.assertEqual(history_serializer.data, excepted_data)

    def test_user_serializer(self):
        testuser1 = User.objects.create(
            username="testuser1", email="test.user1@email.com", password="testuser132"
        )
        testuser2 = User.objects.create(
            username="testuser2", email="test.user2@email.com", password="testuser132"
        )

        excepted_data = [
            {
                "username": "testuser1",
                "email": "test.user1@email.com",
                "password": "testuser132",
            },
            {
                "username": "testuser2",
                "email": "test.user2@email.com",
                "password": "testuser132",
            },
        ]

        user_serializer = UserRegisterSerializer([testuser1, testuser2], many=True)
        self.assertEqual(user_serializer.data, excepted_data)
    
    def test_user_serializer_create(self):
        user_data = {"username": "testuser", "email": "test.user@email.com", "password": "testuser132", "password2": "testuser132"}
        user_serializer = UserRegisterSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            self.assertEqual(user.username, "testuser")
            self.assertEqual(user.email, "test.user@email.com")
            self.assertTrue(user.check_password("testuser132"))
    
    def test_user_serializer_validate(self):
        user_data = {"username": "testuser", "email": "test.user@email.com", "password": "testuser132", "password2": "testuser132"}
        user_serializer = UserRegisterSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            self.assertEqual(user.username, "testuser")
            self.assertEqual(user.email, "test.user@email.com")
            self.assertTrue(user.check_password("testuser132"))