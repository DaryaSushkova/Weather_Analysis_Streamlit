import requests


def open_weather_api(city, api_key):
  '''
  Получение температуры из OpenWeatherMap API (синхронный).
  '''

  base_url = "http://api.openweathermap.org/data/2.5/weather"
  params = {
      'q': city,
      'appid': api_key,
      'units': 'metric',
      'lang': 'ru'
  }

  try:
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()

    # Парсинг ответа сервиса OpenWeatherMap
    temperature = data['main']['temp']
    description = data['weather'][0]['description']

    print(f"Текущая температура в городе {city}: {temperature} градусов")
    print(f"Облачность: {description.capitalize()}")

    return temperature

  except Exception as e:
    print(f"Ошибка при запросе: {e}")