import pandas as pd
import numpy as np
import requests
import streamlit as st
from sklearn.linear_model import LinearRegression
from datetime import datetime


def analyze_city(df: pd.DataFrame, city: str):
    '''
    Анализ данных о температуре для заданного города
    '''

    # Текущие данные для конкретного города
    current_df = df[df['city'] == city].copy()
    current_df = current_df.sort_values('timestamp')

    window = 30  # Значение окна для скользящего
    # Скользящее среднее и отклонение
    current_df['rolling_mean'] = current_df['temperature'].rolling(window=window).mean()
    current_df['rolling_std'] = current_df['temperature'].rolling(window=window).std()
    # Определение аномальных данных
    current_df['is_anomaly'] = np.abs(current_df['temperature'] - current_df['rolling_mean']) > 2 * current_df['rolling_std']
    anomalies = current_df[current_df['is_anomaly']]

    # Профиль сезона
    season_profile = current_df.groupby('season')['temperature'].agg(['mean', 'std']).reset_index()

    # Добавляем числовую фичу для регрессии - кол-во дней от начала замеров
    current_df['days'] = (current_df['timestamp'] - current_df['timestamp'].min()).dt.days
    X = current_df['days'].values.reshape(-1, 1)
    y = current_df['temperature'].values

    # Обучение линейной регрессии
    model = LinearRegression()
    model.fit(X, y)
    reg_coeff = model.coef_[0]
    trend = 'positive' if reg_coeff > 0 else 'negative'

    # Вычисление основных статистик за все время
    avg_temp = current_df['temperature'].mean()
    min_temp = current_df['temperature'].min()
    max_temp = current_df['temperature'].max()

    return {
        'city': city,
        'average_temperature': avg_temp,
        'min_temperature': min_temp,
        'max_temperature': max_temp,
        'season_profile': season_profile,
        'reg_coeff': reg_coeff,
        'trend': trend,
        'anomalies_cnt': len(anomalies),
        'anomalies': anomalies[['timestamp', 'temperature']]
    }


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
  

def get_current_season():
    """
    Вспомогательная функция определения сезона.
    """

    month = datetime.now().month  # Номер текущего месяца

    if month in [1, 2, 12]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    else:
        return 'autumn'


def check_anomaly(temp: float, season_profile: pd.DataFrame):
    '''
    Функция проверки текущей погоды на аномальность.
    '''

    season = get_current_season()
    # Профиль сезона для заданного города
    season_data = season_profile[season_profile['season'] == season]

    if not season_data.empty:
        # Вычисление статистик на профиле сезонов
        mean_temp = season_data['mean'].values[0]
        std_temp = season_data['std'].values[0]

        # Проверка аномальности температуры
        if mean_temp - 2 * std_temp <= temp <= mean_temp + 2 * std_temp:
            st.success(f"Текущая температура {temp} градусов является нормальной для сезона {season}.")
        else:
            message = f"""
            Текущая температура {temp} градусов является аномальной для сезона {season}.\n
            Допустимый диапазон: [{round(mean_temp - 2 * std_temp, 2)}; {round(mean_temp + 2 * std_temp, 2)}]
            """
            st.warning(message)
    else:
        st.error(f"Отсутствуют данные по городу за сезон {season} для определения аномальности.")
    
    return None