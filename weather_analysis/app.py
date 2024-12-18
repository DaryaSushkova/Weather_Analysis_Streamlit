import streamlit as st
import pandas as pd


def main():
    st.title("Анализ временных рядов температуры")

    # 1. Интерфейс для загрузки файла
    st.header("Загрузка файла с историческими данными")
    uploaded_file = st.file_uploader("Загрузите CSV файл с историческими данными", type=["csv"])
    
    if uploaded_file is not None:
        # Загрузка данных
        df = pd.read_csv(uploaded_file)

        # Проверка структуры данных
        required_columns = {"city", "timestamp", "temperature", "season"}
        if required_columns.issubset(df.columns):
            st.success("Файл успешно загружен!")
            
            # Отображение первых строк данных
            st.subheader("Первые строки загруженных данных")
            st.dataframe(df.head())
            
            # 2. Интерфейс для выбора города
            st.header("Выбор города")
            unique_cities = df['city'].unique()
            selected_city = st.selectbox("Выберите город", unique_cities)
            
            # Отображение данных для выбранного города
            st.subheader(f"Данные для города {selected_city}")
            city_df = df[df['city'] == selected_city]
            st.dataframe(city_df)

        else:
            st.error(f"Файл должен содержать столбцы: {', '.join(required_columns)}")

if __name__ == "__main__":
    main()