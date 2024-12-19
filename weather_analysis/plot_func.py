import matplotlib.pyplot as plt
import streamlit as st


def anomaly_pie_chart(total_count, anomaly_count):
    '''
    Построение pie chart для отображения соотношения общего числа данных и числа аномалий.
    '''

    labels = ['Нормальные данные', 'Аномалии']
    sizes = [total_count - anomaly_count, anomaly_count]
    colors = ['#66b3ff', '#ff6666']
    explode = (0, 0.1)

    plt.figure(figsize=(6, 6))

    plt.pie(sizes, labels=labels, colors=colors, explode=explode, autopct='%1.1f%%', startangle=140)
    plt.title('Соотношение нормальных данных и аномалий')

    st.pyplot(plt)


def weather_time_series(city_df, anomalies):
    '''
    Построение временного ряда температур с выделением аномалий.
    '''

    plt.figure(figsize=(12, 6))

    plt.plot(city_df['timestamp'], city_df['temperature'], label='Температура', color='blue')
    plt.scatter(anomalies['timestamp'], anomalies['temperature'], color='red', label='Аномалии')
    plt.xlabel('Дата')
    plt.ylabel('Температура (°C)')
    plt.title('Временной ряд температур с аномалиями')

    plt.legend()
    st.pyplot(plt)


def seasonal_profile(season_profile):
    '''
    Построение сезонного профиля со средним и стандартным отклонением.
    '''

    plt.figure(figsize=(8, 5))

    plt.bar(season_profile['season'], season_profile['mean'], yerr=season_profile['std'], capsize=5)
    plt.xlabel('Сезон')
    plt.ylabel('Средняя температура (°C)')
    plt.title('Сезонный профиль температуры')

    plt.grid(True)
    st.pyplot(plt)
    st.info(season_profile)