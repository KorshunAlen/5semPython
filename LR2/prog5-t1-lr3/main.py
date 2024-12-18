from owm_key import owm_api_key
import json
from urllib import request
from getweatherdata import get_weather_data

# TODO 1
def get_weather_data(place, api_key=None):

    # Все данные идут в строке запроса
    # в f лежит тело ответа.
    with request.urlopen(
            f'https://api.openweathermap.org/data/2.5/weather?q={place}&appid={api_key}'
    ) as f:
        # закодированный текст (строка)
        res = f.read().decode('utf-8')  # для обычной(unicode) строки, вместо байтовой
        # преобразование в json в объект питона
        res_obj = json.loads(res)

    # print(res_json)

    print((res_obj))
    # запись результата в json
    # with open('data.json', 'w') as f:
    #     json.dump(res_json, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    get_weather_data('Moscow', api_key=owm_api_key)
