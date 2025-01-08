import requests
from xml.etree import ElementTree as ET
import json
import csv
from io import StringIO

class Component:
    """
    Базовый интерфейс компонента для получения данных о валютах.
    """
    def operation(self):
        pass

class CurrenciesList(Component):
    """
    Базовый класс для получения данных о валютах в формате словаря.
    """
    def __init__(self, currencies_ids):
        self.currencies_ids = currencies_ids

    def fetch_currencies(self):
        response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
        root = ET.fromstring(response.content)
        currencies = []

        for valute in root.findall('Valute'):
            valute_id = valute.get('ID')
            if valute_id in self.currencies_ids:
                code = valute.find('CharCode').text
                name = valute.find('Name').text
                value = valute.find('Value').text.replace(',', '.')
                nominal = int(valute.find('Nominal').text)
                currencies.append({code: (name, value, nominal)})

        return currencies

    def operation(self):
        return self.fetch_currencies()

class Decorator(Component):
    """
    Базовый класс декоратора.
    """
    def __init__(self, component):
        self._component = component

    def operation(self):
        return self._component.operation()

class ConcreteDecoratorJSON(Decorator):
    """
    Декоратор для преобразования данных в формат JSON.
    """
    def operation(self):
        data = self._component.operation()
        return json.dumps(data, ensure_ascii=False, indent=4)

class ConcreteDecoratorCSV(Decorator):
    """
    Декоратор для преобразования данных в формат CSV.
    """
    def operation(self):
        data = self._component.operation()

        # Если данные в формате JSON, преобразуем их обратно в список словарей
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                raise ValueError("Невозможно преобразовать данные из JSON в список для CSV.")

        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["Код валюты", "Название", "Курс", "Номинал"])
        for item in data:
            for code, (name, value, nominal) in item.items():
                writer.writerow([code, name, value, nominal])
        output.seek(0)
        return output.getvalue()

if __name__ == '__main__':
    # Базовый компонент
    currencies = CurrenciesList(['R01035', 'R01335', 'R01700J'])

    # Данные в формате словаря
    print("Данные в формате словаря:")
    print(currencies.operation())
    print()

    # Декоратор JSON
    json_decorator = ConcreteDecoratorJSON(currencies)
    print("Данные в формате JSON:")
    print(json_decorator.operation())
    print()

    # Декоратор CSV
    csv_decorator = ConcreteDecoratorCSV(json_decorator)
    print("Данные в формате CSV:")
    print(csv_decorator.operation())

