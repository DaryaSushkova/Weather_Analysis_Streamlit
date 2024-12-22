import aiohttp
import asyncio
import json
import time
import pandas as pd
from datetime import datetime
from analyzer import analyze_city, open_weather_api, check_anomaly
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor, as_completed


def compare_analyze_city_func(df):
    '''
    Функция сравнения выполнения анализа с распараллеливанием и без него.
    '''

    cities_list = df['city'].unique()

    # Последовательное выполнение
    start_time = time.time()
    results = [analyze_city(df, city) for city in cities_list]
    res_time = time.time() - start_time

    print(f"Последовательный анализ занял {res_time:.2f} секунд.")

    # Многопроцессорность (параллельное выполнение)
    start_time = time.time()
    with Pool(processes=4) as pool:
        results_par = pool.starmap(analyze_city, [(df, city) for city in cities_list])
    res_time = time.time() - start_time

    print(f"Параллельный анализ занял {res_time:.2f} секунд.")

    # Многопоточность (параллельное выполнение)
    results = []
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_city = {executor.submit(analyze_city, df, city): city for city in cities_list}

        for future in as_completed(future_to_city):
            city = future_to_city[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                print(f'Город {city} вызвал ошибку: {exc}')

    res_time = time.time() - start_time

    print(f"Параллельный анализ занял {res_time:.2f} секунд.")


async def get_weather_async(city, api_key):
    """
    Получение температуры из OpenWeatherMap API (aсинхронный).
    """

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
    'q': city,
    'appid': api_key,
    'units': 'metric',
    'lang': 'ru'
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                temperature = data['main']['temp']
                print(f"Асинхронный метод: текущая температура в городе {city}: {temperature} °C")
                return temperature

    except aiohttp.ClientError as e:
        print(f"Ошибка при асинхронном запросе: {e}")
        return None


async def async_main(cities, api_key):
  '''
  Асинхронный запуск получения текущих температур.
  '''

  # Список асинхронных задач
  tasks = [get_weather_async(city, api_key) for city in cities]
  results = await asyncio.gather(*tasks)
  return results


def test_open_weather_api(cities_list):
    '''
    Тестирование разных подходов получения текущей температуры.
    '''

    with open("optional/key.json") as json_file:
        data = json.load(json_file)
    api_key = data['api_key']

    print(f"Текущее время: {datetime.now()}\n")

    # Синхронное получение текущих температур
    start_time = time.time()
    for city in cities_list:
        print(f"Cинхронный метод: текущая температура в городе {city}: {open_weather_api(city, api_key)[0]}°C")
    res_time = time.time() - start_time
    print(f"Синхронное выполнение заняло {res_time:.2f} секунд.")

    print()

    # Асинхронное получение текущих температур
    start_time = time.time()
    results = asyncio.run(async_main(cities_list, api_key))
    res_time = time.time() - start_time
    print(f"Асинхронное выполнение заняло {res_time:.2f} секунд.")


def check_temp_cities(df, cities_list):
    '''
    Функция проверки аномальности текущей температуры для нескольких городов.
    '''

    with open("optional/key.json") as json_file:
        data = json.load(json_file)
    api_key = data['api_key']

    for city in cities_list:
        curr_temp = open_weather_api(city, api_key)[0]
        curr_season_profile = analyze_city(df, city)['season_profile']
        check_anomaly(curr_temp, curr_season_profile, st_flag=False)
        print()


if __name__ == "__main__":
   df = pd.read_csv('optional/temperature_data.csv')
   df['timestamp'] = pd.to_datetime(df['timestamp'])
   cities_list = df['city'].unique()

   # Ниже - вызовы дополнительных функций из задания

   #check_temp_cities(df, cities_list)
   #test_open_weather_api(cities_list)
   #compare_analyze_city_func(df)