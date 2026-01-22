"""
Модуль с декораторами для логирования.
"""

import functools
from typing import Any, Callable


def log(filename: str | None = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Формируем сообщение о начале
            start_message = f"{func.__name__} started with args: {args}, kwargs: {kwargs}"

            try:
                # Выводим или записываем начало
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(start_message + "\n")
                else:
                    print(start_message)

                # Выполняем функцию
                result = func(*args, **kwargs)

                # Формируем сообщение об успешном завершении
                success_message = f"{func.__name__} finished with result: {result}"

            except Exception as e:
                # Формируем сообщение об ошибке
                error_message = f"{func.__name__} raised {type(e).__name__}: {e} with args: {args}, kwargs: {kwargs}"

                # Выводим или записываем ошибку
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(error_message + "\n")
                else:
                    print(error_message)

                # Пробрасываем исключение дальше
                raise

            else:
                # Выводим или записываем успешное завершение
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(success_message + "\n")
                else:
                    print(success_message)

                return result

        return wrapper

    return decorator
