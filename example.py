from src.decorators import log


# Логирование в консоль
@log()
def add_numbers(a: int, b: int) -> int:
    """Складывает два числа."""
    return a + b


#  Логирование в файл
@log(filename="operations.log")
def multiply_numbers(a: int, b: int) -> int:
    """Умножает два числа."""
    return a * b


#  Функция, которая может вызвать ошибку
@log()
def divide_numbers(a: int, b: int) -> float:
    """Делит два числа."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


if __name__ == "__main__":
    print("=== Тест 1: Сложение (логи в консоль) ===")
    result = add_numbers(5, 3)
    print(f"Результат: {result}")

    print("\n=== Тест 2: Умножение (логи в файл) ===")
    result = multiply_numbers(4, 6)
    print(f"Результат: {result}")

    print("\n=== Тест 3: Деление с ошибкой ===")
    try:
        result = divide_numbers(10, 0)
    except ValueError as e:
        print(f"Поймали ошибку: {e}")

    print("\n=== Тест 4: Успешное деление ===")
    result = divide_numbers(10, 2)
    print(f"Результат: {result}")
