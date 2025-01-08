import requests
import matplotlib.pyplot as plt
from xml.etree import ElementTree as ET
from datetime import datetime, timedelta
import threading


class SingletonMeta(type):
    """Метакласс для реализации шаблона Одиночка."""
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class CurrencyFetcher(metaclass=SingletonMeta):
    """Класс для работы с курсами валют."""

    def __init__(self, min_request_interval=1):
        self._last_request_time = datetime.min
        self.min_request_interval = timedelta(seconds=min_request_interval)
        self._currencies = []
        self._nominals = {}

    def fetch_currencies(self, currency_ids):
        """Получить курсы валют по списку идентификаторов."""
        if datetime.now() - self._last_request_time < self.min_request_interval:
            raise Exception("Слишком частый запрос. Подождите немного.")

        response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
        root = ET.fromstring(response.content)
        valutes = root.findall("Valute")

        self._currencies.clear()
        for valute in valutes:
            valute_id = valute.get('ID')
            if valute_id in currency_ids:
                name = valute.find('Name').text
                char_code = valute.find('CharCode').text
                value = valute.find('Value').text.replace(',', '.')
                nominal = int(valute.find('Nominal').text)
                whole, fraction = value.split('.')
                self._currencies.append({char_code: (name, (whole, fraction))})
                self._nominals[char_code] = nominal

        self._last_request_time = datetime.now()
        return self._currencies

    def get_nominal(self, currency_code):
        """Получить номинал валюты."""
        return self._nominals.get(currency_code)

    def visualize_currencies(self, filename='currencies.jpg'):
        """Создать визуализацию курсов валют."""
        if not self._currencies:
            raise ValueError("Нет данных для визуализации. Сначала вызовите fetch_currencies.")

        labels = []
        values = []
        for currency in self._currencies:
            for code, (name, (whole, fraction)) in currency.items():
                labels.append(name)
                values.append(float(f"{whole}.{fraction}"))

        fig, ax = plt.subplots()
        ax.bar(labels, values, color='skyblue')
        ax.set_ylabel('Курс валют (в рублях)')
        ax.set_title('Курсы валют ЦБ РФ')

        # Устанавливаем фиксированные позиции меток
        ax.set_xticks(range(len(labels)))  # Устанавливаем позиции меток
        ax.set_xticklabels(labels, rotation=45, ha='right')  # Указываем метки

        plt.tight_layout()
        plt.savefig(filename)
        plt.show()


# Класс для тестирования с примерными значениями
class CurrenciesLst:
    def __init__(self):
        self.__cur_lst = [
            {'GBP': ('Фунт стерлингов Соединенного королевства', '113,2069')},
            {'KZT': ('Казахстанских тенге', '19,8264')},
            {'TRY': ('Турецких лир', '33,1224')}
        ]

    def visualize_currencies(self):
        """Визуализировать сохраненные данные."""
        fig, ax = plt.subplots()
        currencies = []
        values = []
        for el in self.__cur_lst:
            for key, (name, value) in el.items():
                currencies.append(name)
                values.append(float(value.replace(',', '.')))

        ax.bar(currencies, values, color='skyblue')
        ax.set_ylabel('Курс валют (в рублях)')
        ax.set_title('Пример визуализации валют')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    fetcher = CurrencyFetcher(min_request_interval=1)

    try:
        # Запрос данных о курсах валют
        currencies = fetcher.fetch_currencies(['R01035', 'R01335', 'R01700J'])
        print(currencies)

        # Получение номинала
        for currency in currencies:
            for code in currency:
                nominal = fetcher.get_nominal(code)
                print(f"Номинал {code}: {nominal}")

        # Визуализация
        fetcher.visualize_currencies()

    except Exception as e:
        print(f"Ошибка: {e}")
