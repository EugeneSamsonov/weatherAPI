import requests

def get_weather_data(city, api_key, units='metric'):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}'
    response = requests.get(url, timeout=10)
    return response.json()
