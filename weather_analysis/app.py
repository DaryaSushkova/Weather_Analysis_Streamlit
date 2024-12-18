import streamlit as st
import pandas as pd
from analyzer import open_weather_api


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
            
            # Отображение первых строк данных
            st.subheader("Начальные строки загруженного файла:")
            st.dataframe(df.head())
            
            # Интерфейс для выбора города
            st.header("Город для анализа")
            cities_list = df['city'].unique()
            current_city = st.selectbox("Выберите город из списка ниже", cities_list)

            # Интерфейс для ввода API-ключа OpenWeatherMap
            st.header("Получение текущей погоды")
            api_key = st.text_input("Введите ваш API-ключ OpenWeatherMap", type="password")
            
            if api_key:
                result = open_weather_api(current_city, api_key)
                if result:
                    temperature, description = result
                    st.success(f"Текущая температура в городе {current_city}: {temperature} градусов Цельсия")
                    st.info(f"Облачность: {description}")
            else:
                st.warning("Введите API-ключ для получения данных о текущей погоде.")
            
            # Отображение данных для выбранного города
            # st.subheader(f"Данные для города {selected_city}")
            # city_df = df[df['city'] == selected_city]
            # st.dataframe(city_df)

        else:
            st.error(f"Файл должен содержать столбцы: {', '.join(required_columns)}")

if __name__ == "__main__":
    main()