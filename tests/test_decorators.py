import os
import tempfile
import pytest
from src.decorators import log


@log()
def successful_function(x: int, y: int = 10) -> int:
    """Тестовая функция, которая всегда успешна."""
    return x + y


@log()
def failing_function(x: int) -> int:
    """Тестовая функция, которая всегда вызывает ошибку."""
    raise ValueError(f"Error with {x}")


class TestLogDecorator:
    """Тесты декоратора log."""

    def test_log_to_console_success(self, capsys):
        """Тест логирования успешной функции в консоль."""
        # Вызываем функцию
        result = successful_function(5, y=3)

        # Перехватываем вывод в консоль
        captured = capsys.readouterr()
        output = captured.out

        # Проверяем вывод
        assert "successful_function started" in output
        assert "successful_function finished" in output
        assert "result: 8" in output  # 5 + 3 = 8
        assert result == 8

    def test_log_to_console_error(self, capsys):
        """Тест логирования функции с ошибкой в консоль."""
        with pytest.raises(ValueError, match="Error with 5"):
            failing_function(5)

        # Перехватываем вывод в консоль
        captured = capsys.readouterr()
        output = captured.out

        # Проверяем вывод
        assert "failing_function started" in output
        assert "failing_function raised ValueError" in output
        assert "args: (5,)" in output

    def test_log_to_file_success(self):
        """Тест логирования успешной функции в файл."""
        # Создаем временный файл
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp:
            tmp_filename = tmp.name

        try:
            # Создаем декорированную функцию
            @log(filename=tmp_filename)
            def test_func(a: int, b: int) -> int:
                return a * b

            # Вызываем функцию
            result = test_func(4, 5)

            # Читаем файл
            with open(tmp_filename, 'r', encoding='utf-8') as f:
                content = f.read()

            # Проверяем
            assert "test_func started" in content
            assert "test_func finished" in content
            assert "result: 20" in content  # 4 * 5 = 20
            assert result == 20

        finally:
            # Удаляем временный файл
            if os.path.exists(tmp_filename):
                os.remove(tmp_filename)

    def test_log_to_file_error(self):
        """Тест логирования функции с ошибкой в файл."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp:
            tmp_filename = tmp.name

        try:
            # Создаем декорированную функцию
            @log(filename=tmp_filename)
            def test_func() -> None:
                raise TypeError("Test error")

            with pytest.raises(TypeError, match="Test error"):
                test_func()

            # Читаем файл
            with open(tmp_filename, 'r', encoding='utf-8') as f:
                content = f.read()

            # Проверяем
            assert "test_func started" in content
            assert "test_func raised TypeError" in content

        finally:
            # Удаляем временный файл
            if os.path.exists(tmp_filename):
                os.remove(tmp_filename)

    def test_log_with_default_args(self, capsys):
        """Тест декоратора без указания filename (по умолчанию в консоль)."""

        # Декоратор без аргументов
        @log()
        def test_func():
            return "test"

        test_func()

        captured = capsys.readouterr()
        assert "test_func started" in captured.out

    def test_function_metadata_preserved(self):
        """Тест сохранения метаданных оригинальной функции."""

        @log()
        def original_func(x: int) -> int:
            """Тестовая функция с документацией."""
            return x * 2

        # Проверяем, что метаданные сохранились
        assert original_func.__name__ == "original_func"
        assert original_func.__doc__ == "Тестовая функция с документацией."
        assert original_func(5) == 10


if __name__ == "__main__":
    pytest.main()
