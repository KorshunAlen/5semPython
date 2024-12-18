
from gen_fib import my_genn


def test_fib_1():
    gen = my_genn()
    assert gen.send(3) == [0, 1, 1], "Тривиальный случай n = 3, список [0, 1, 1]"


def test_fib_2():
    gen = my_genn()
    assert gen.send(5) == [0, 1, 1, 2, 3], "Пять первых членов ряда"

## Тест для получения первых 10 чисел Фибоначчи
def test_fib_3():
    gen = my_genn()
    result = gen.send(10)
    assert result == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34], "Первые 10 чисел ряда Фибоначчи"

# Тест для получения первых 1 числа Фибоначчи
def test_fib_4():
    gen = my_genn()
    result = gen.send(1)
    assert result == [0], "Тривиальный случай n = 1, список [0]"

# Тест для получения 0 чисел Фибоначчи
def test_fib_5():
    gen = my_genn()
    result = gen.send(0)
    assert result == [], "Случай n = 0, пустой список"
