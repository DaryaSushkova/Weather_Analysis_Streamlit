import streamlit as st
import pandas as pd
from analyzer import analyze_city, open_weather_api, check_anomaly
from plot_func import anomaly_pie_chart, seasonal_profile, weather_time_series


CURRENT_DATA = {}

def main():
    st.title("Анализ временных рядов температуры")

    # Интерфейс для загрузки файла
    st.header("Загрузка файла с историческими данными")
    uploaded_file = st.file_uploader("Загрузите CSV файл с историческими данными", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Проверка структуры данных
        required_columns = {"city", "timestamp", "temperature", "season"}
        if required_columns.issubset(df.columns):
            st.success("Файл успешно загружен!")
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Отображение первых строк данных
            st.subheader("Начальные строки загруженного файла:")
            st.dataframe(df.head())
            
            # Интерфейс для выбора города
            st.header("Город для анализа")
            cities_list = df['city'].unique()
            current_city = st.selectbox("Выберите город из списка ниже", cities_list)

            if current_city:
                if current_city not in CURRENT_DATA:
                    CURRENT_DATA[current_city] = analyze_city(df, current_city)

                # Вывод описательной статистики
                st.subheader(f"Историческая статистика для города {current_city}")
                st.write(f"Средняя температура: {CURRENT_DATA[current_city]['average_temperature']:.2f} °C")
                st.write(f"Минимальная температура: {CURRENT_DATA[current_city]['min_temperature']:.2f} °C")
                st.write(f"Максимальная температура: {CURRENT_DATA[current_city]['max_temperature']:.2f} °C")
                st.write(f"Тренд: {CURRENT_DATA[current_city]['trend']}")
                anomaly_pie_chart(CURRENT_DATA[current_city]['total_cnt'], CURRENT_DATA[current_city]['anomalies_cnt'])

                # Интерфейс для ввода API-ключа OpenWeatherMap
                st.subheader("Получение текущей погоды")
                api_key = st.text_input("Введите ваш API-ключ OpenWeatherMap", type="password")
                
                if api_key:
                    try:
                        result = open_weather_api(current_city, api_key)
                        if result:
                            temperature, description = result
                            st.success(f"Текущая температура в городе {current_city} успешно получена отображена ниже")
                            st.info(f"Температура: {temperature} °C, облачность: {description}")
                            check_anomaly(temperature, CURRENT_DATA[current_city]['season_profile'])
                    except Exception as e:
                        st.error(f"Ошибка: {e}")
                else:
                    st.warning("API-ключ не введен.")

                st.header(f"Временной ряд для города {current_city}")
                weather_time_series(CURRENT_DATA[current_city]['city_df'], CURRENT_DATA[current_city]['anomalies'])

                st.header(f"Сезонный профиль для города {current_city}")
                seasonal_profile(CURRENT_DATA[current_city]['season_profile'])
                
                # Отображение данных для выбранного города
                # st.subheader(f"Данные для города {selected_city}")
                # city_df = df[df['city'] == selected_city]
                # st.dataframe(city_df)

        else:
            st.error(f"Файл должен содержать столбцы: {', '.join(required_columns)}")

if __name__ == "__main__":
    main()