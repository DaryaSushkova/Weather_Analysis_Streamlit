import requests
import streamlit as st


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

    # Проверка на ошибочный статус
    if response.status_code != 200:
        error_message = response.json().get('message', 'Произошла неизвестная ошибка')
        raise Exception(f"Ошибка {response.status_code}: {error_message}")
    
    response.raise_for_status()
    data = response.json()

    # Парсинг ответа сервиса OpenWeatherMap
    temperature = data['main']['temp']
    description = data['weather'][0]['description']

    return temperature, description.capitalize()

  except Exception as e:
    st.error(str(e))
    return None