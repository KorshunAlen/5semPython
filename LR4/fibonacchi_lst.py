class FibonacchiLst:
    def __init__(self, lst):
        self.lst = lst
        self.idx = 0  # Инициализируем индекс для перебора элементов списка
        self.fib_set = set(self.generate_fib_up_to(max(lst)))  # Множество чисел Фибоначчи до максимального элемента из списка

    def generate_fib_up_to(self, n):
        """Генерирует числа Фибоначчи до n."""
        fib = [0, 1]
        while fib[-1] <= n:
            fib.append(fib[-1] + fib[-2])
        return fib

    def __iter__(self):
        return self  # Возвращаем экземпляр класса, чтобы поддерживать протокол итераторов

    def __next__(self):
        while self.idx < len(self.lst):  # Проверяем все элементы списка
            res = self.lst[self.idx]  # Получаем текущий элемент списка
            self.idx += 1  # Увеличиваем индекс для следующего элемента
            if res in self.fib_set:  # Проверяем, является ли элемент числом Фибоначчи
                return res  # Если да, возвращаем его
        raise StopIteration  # Если мы перебрали все элементы, выбрасываем исключение StopIteration


# Пример использования:
lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
fib_lst = FibonacchiLst(lst)

# Получаем все числа Фибоначчи из списка
print(list(fib_lst))  # [0, 1, 2, 3, 5, 8, 1]
