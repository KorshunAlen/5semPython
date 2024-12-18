import functools
import itertools

# def fib_elem_gen():
#     """Генератор, возвращающий элементы ряда Фибоначчи"""
#     a = 0
#     b = 1
#
#     while True:
#         yield a
#         res = a + b
#         a = b
#         b = res
#
#
# g = fib_elem_gen()
#
# while True:
#     el = next(g)
#     print(el)
#     if el > 10:
#         break



def my_genn():
    """Сопрограмма"""

    while True:
        number_of_fib_elem = yield
        print(number_of_fib_elem)
        # Создаем список чисел Фибоначчи по указанному количеству
        a, b = 0, 1
        fib_list = [a, b]  # Начальные элементы
        for _ in range(2, number_of_fib_elem):  # Начинаем с третьего числа и так далее
            a, b = b, a + b
            fib_list.append(b)

        # Используем itertools.islice для получения первых N чисел из fib_list
        l = list(itertools.islice(fib_list, number_of_fib_elem))  # Ограничиваем количество чисел

        yield l


def fib_coroutine(g):
    @functools.wraps(g)
    def inner(*args, **kwargs):
        gen = g(*args, **kwargs)
        gen.send(None)
        return gen

    return inner


my_genn = fib_coroutine(my_genn)
gen = my_genn()
print(gen.send(5))
