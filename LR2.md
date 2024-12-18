# Описание задачи

Написать реализацию функции get_weather_data(place, api_key=None) (в модуле getweatherdata), в которой необходимо получить данные о погоде с сайта https://openweathermap.org/.

Функция должна возвращать объект в формате JSON, включающий:

информацию о названии города (в контексте openweathermap),
код страны (2 символа),
широту и долготу, на которой он находится,
его временной зоне,
а также о значении температуры (как она ощущается).
Значение временной зоны выводить в формате UTC±N, где N - цифра временного сдвига. Протестировать выполнение программы со следующими городами: Чикаго, СПб, Дакка.

Пример вызова функции и получаемого результата.

>>> get_weather_data('Kiev', api_key=key)
{"name": "Kyiv", "coord": {"lon": 30.52, "lat": 50.43}, "country": "UA", "feels_like": 21.96, "timezone": "UTC+3"}
>>>

При реализации программы, не публикуйте свой ключ для осуществления запросов. Сразу же после создания борда в реплите, используйте вкладку слева "secrets"), а при публикации кода в гитхабе — исключите из коммитов подключаемый файл, где разместите ключ, с помощью .gitignore. Для организации запросов используйте модуль requests. Для кодирования и декодирования json - одноименный модуль.

# Решение


1. Функция get_weather_data(place, api_key=None)

Описание:
Эта функция отправляет запрос к API OpenWeatherMap, получает данные о погоде для указанного города и обрабатывает их. После обработки функция сохраняет полученные данные в файл формата JSON с помощью вспомогательной функции.

Что делает:

Формирует URL для запроса и параметры, включая название города и API-ключ.
Использует библиотеку requests для отправки GET-запроса на сервер OpenWeatherMap.
Обрабатывает ответ и выбирает из него нужные данные:
-Название города (data["name"]);
-Широта и долгота (data["coord"]);
-Код страны (data["sys"]["country"]);
-Температура, ощущаемая как (data["main"]["feels_like"]);
-Временная зона (data["timezone"]), которая конвертируется в формат UTC±N.
Возвращает словарь с обработанными данными.


    def get_weather_data(place, api_key=None):
        # URL и параметры запроса
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": place,
            "appid": api_key,
            "units": "metric",  # Используем градусы Цельсия
        }
    
        response = requests.get(base_url, params=params) # выполняет запрос 
        response.raise_for_status()  # Проверка на ошибки HTTP
    
        data = response.json()  # преобразовать JSON-ответ от сервера в словарь Python
    
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


2. Функция convert_timezone(offset)

Описание:
Эта функция конвертирует сдвиг времени в секундах (значение timezone из ответа OpenWeatherMap) в формат UTC±N, где N — это количество часов сдвига.

Что делает функция:

Делит сдвиг времени offset на 3600 (количество секунд в одном часе), чтобы получить часы.
Определяет знак (+ или -) в зависимости от положительного или отрицательного значения сдвига.
Возвращает строку вида UTC±N.

      def convert_timezone(offset):
          hours = offset // 3600  # Сдвиг времени в часах
          sign = "+" if hours >= 0 else "-"
          return f"UTC{sign}{abs(hours)}"

3. Блок if __name__ == "__main__":

Описание:
Это блок кода, который выполняется только при запуске данного файла как основной программы.

Что делает блок:

Импортирует API-ключ из файла owm_key.py (предполагается, что ключ хранится в переменной owm_api_key).
Создаёт список городов для тестирования: "Chicago", "Saint Petersburg", "Dhaka".
Для каждого города вызывает функцию get_weather_data с передачей названия города и API-ключа.
Выводит полученные данные в консоль.

    if __name__ == "__main__":
    
        cities = ["Chicago", "Saint Petersburg", "Dhaka"]
    
        for city in cities:
            weather_data = get_weather_data(city, api_key=owm_api_key)
            if weather_data:
                print(weather_data)

Вывод программы:

![image](https://github.com/user-attachments/assets/5f3103b6-768c-443a-b742-2afc87d44de2)
