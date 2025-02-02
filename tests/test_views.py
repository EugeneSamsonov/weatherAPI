import pdb
from django.urls import reverse
from rest_framework.test import APITestCase

from users.models import User

class ViewsTests(APITestCase):

    def setUp(self) -> None:
        self.user_data = {
            'username': 'testuser',
            'email': 'test.user@email.com',
            'password': 'testuser132',
            'password2': 'testuser132'
        }
        return super().setUp()
    

    def test_get_weather_view(self):
        url = reverse('weather_api', args=['Moscow'])
        result = self.client.get(url)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data['city'], 'Moscow')
    
    
    def test_get_weather_view_with_uncorrect_city(self):
        url = reverse('weather_api', args=['uncorrect_city'])
        result = self.client.get(url)

        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data.get('error', None), '404')


    def test_register_view(self):
        url = reverse('register')
        result = self.client.post(url, data=self.user_data, format='json')

        self.assertEqual(result.status_code, 201)
        user = User.objects.get(username=self.user_data['username'])

        self.assertEqual(user.username, self.user_data['username'])
    
    
    def test_register_view_with_uncorrect_email(self):
        url = reverse('register')
        user_data = self.user_data
        user_data['email'] = 'email@'

        result = self.client.post(url, data=user_data, format='json')

        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data.get('email', None)[0], 'Введите правильный адрес электронной почты.')
    
    
    def test_register_view_with_different_passwords(self):
        url = reverse('register')
        user_data = self.user_data
        user_data['password2'] = 'password2'

        result = self.client.post(url, data=user_data, format='json')

        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.data.get('password', None)[0], 'Пароли не совпадают')


    def test_token_obtain_pair(self):
        token_obtain_pair_url = reverse('token_obtain_pair')
        register_url = reverse('register')

        self.client.post(register_url, data=self.user_data, format='json')
        result = self.client.post(token_obtain_pair_url, data=self.user_data, format='json')

        self.assertEqual(result.status_code, 200)
        self.assertContains(result, 'refresh')
        self.assertContains(result, 'access')
        self.assertContains(result, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9')


    def test_token_obtain_pair_with_uncorrect_data(self):
        token_obtain_pair_url = reverse('token_obtain_pair')
        register_url = reverse('register')

        uncorrect_data = self.user_data
        uncorrect_data['username'] = 'username'
        uncorrect_data['password'] = '123'

        self.client.post(register_url, data=self.user_data, format='json')
        result = self.client.post(token_obtain_pair_url, data=uncorrect_data, format='json')

        self.assertEqual(result.status_code, 401)
        self.assertEqual(result.data.get('detail', None), 'Не найдено активной учетной записи с указанными данными')


    def test_refresh_token(self):
        register_url = reverse('register')
        token_obtain_pair_url = reverse('token_obtain_pair')
        token_refresh_url = reverse('token_refresh')

        self.client.post(register_url, data=self.user_data, format='json')
        tokens = self.client.post(token_obtain_pair_url, data=self.user_data, format='json').data

        result = self.client.post(token_refresh_url, data=tokens, format='json')

        self.assertEqual(result.status_code, 200)
        self.assertContains(result, 'access')
        self.assertContains(result, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9')


    def test_refresh_token_with_uncorrect_data(self):
        token_refresh_url = reverse('token_refresh')
        token = {
            'refresh': 'invalid_token'
        }

        result = self.client.post(token_refresh_url, data=token, format='json')

        self.assertEqual(result.status_code, 401)
        self.assertEqual(result.data.get('code', None), 'token_not_valid')

    
    def test_user_history(self):
        register_url = reverse('register')
        token_obtain_pair_url = reverse('token_obtain_pair')
        get_user_history_url = f'/api/v1/history/'

        self.client.post(register_url, data=self.user_data, format='json')
        access_token = self.client.post(token_obtain_pair_url, data=self.user_data, format='json').data['access']

        for num, city in enumerate(('Moscow', 'London')):
            get_weather_url = reverse('weather_api', args=[f'{city}'])
            get_weather = self.client.get(get_weather_url, headers={'Authorization': f'Bearer {access_token}'})

            get_user_history = self.client.get(get_user_history_url, headers={'Authorization': f'Bearer {access_token}'})

            self.assertEqual(get_user_history.status_code, 200)

            for key in get_weather.data.keys():
                if key in ('timestamp', 'sunrise', 'sunset'):
                    continue
                
                if key in ('temp', 'temp_max', 'temp_min', 'humidity', 'wind_speed'):
                    self.assertEqual(
                    # Get user history detail and take data from key
                    float(get_user_history.data['results'][num][key]),
                    float(get_weather.data[key]))

                    continue

                self.assertEqual(
                    # Get user history detail and take data from key
                    str(get_user_history.data['results'][num][key]), 
                    str(get_weather.data[key]))
            

    def test_user_history_with_not_auth(self):
        get_user_history_url = '/api/v1/history/'
        get_user_history = self.client.get(get_user_history_url)

        self.assertEqual(get_user_history.status_code, 401)
        self.assertEqual(get_user_history.data['detail'], 'Учетные данные не были предоставлены.')


    def tearDown(self) -> None:
        return super().tearDown()