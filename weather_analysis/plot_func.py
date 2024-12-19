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