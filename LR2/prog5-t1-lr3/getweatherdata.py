import requests
from owm_key import owm_api_key


def get_weather_data(place, api_key=None):
    # URL и параметры запроса
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": place,
        "appid": api_key,
        "units": "metric",  # Используем градусы Цельсия
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Проверка на ошибки HTTP

    data = response.json()  # преобразовать JSON-ответ от сервера в словарь Python

    # print(data)
    # Обработка данных и формирование результата
    result = {
        "name": data["name"],
        "coord": {
            "lon": data["coord"]["lon"],
            "lat": data["coord"]["lat"]
        },
        "country": data["sys"]["country"],
        "feels_like": data["main"]["feels_like"],
        "timezone": convert_timezone(data["timezone"])
    }
    return result


# Конвертирует временной сдвиг в формат UTC±N.
def convert_timezone(offset):
    hours = offset // 3600  # Сдвиг времени в часах
    sign = "+" if hours >= 0 else "-"
    return f"UTC{sign}{abs(hours)}"


if __name__ == "__main__":

    cities = ["Chicago", "Saint Petersburg", "Dhaka"]

    for city in cities:
        weather_data = get_weather_data(city, api_key=owm_api_key)
        if weather_data:
            print(weather_data)
