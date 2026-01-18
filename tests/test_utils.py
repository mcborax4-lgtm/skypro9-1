import json
import tempfile
import pytest
from src.utils import load_json_data


class TestUtils:
    def test_load_valid_json(self):
        """Тест загрузки валидного JSON файла."""
        # Создаем временный файл с JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            json.dump([{"id": 1, "name": "test"}], tmp)
            tmp_path = tmp.name

        try:
            result = load_json_data(tmp_path)
            assert result == [{"id": 1, "name": "test"}]
        finally:
            import os
            os.unlink(tmp_path)

    def test_load_empty_file(self):
        """Тест загрузки пустого файла."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            tmp_path = tmp.name  # Создаем пустой файл

        try:
            result = load_json_data(tmp_path)
            assert result == []
        finally:
            import os
            os.unlink(tmp_path)

    def test_load_non_list_json(self):
        """Тест загрузки JSON который не является списком."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            json.dump({"id": 1}, tmp)  # Словарь, не список
            tmp_path = tmp.name

        try:
            result = load_json_data(tmp_path)
            assert result == []
        finally:
            import os
            os.unlink(tmp_path)

    def test_file_not_found(self):
        """Тест когда файл не найден."""
        result = load_json_data("/несуществующий/путь/file.json")
        assert result == []

    def test_invalid_json(self):
        """Тест загрузки невалидного JSON."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            tmp.write("{это не json}")  # Невалидный JSON
            tmp_path = tmp.name

        try:
            result = load_json_data(tmp_path)
            assert result == []
        finally:
            import os
            os.unlink(tmp_path)

    def test_with_real_data(self):
        """Тест с реальными данными из operations.json."""
        # Предполагаем что файл operations.json существует в data/
        result = load_json_data("data/operations.json")

        # Проверяем что результат - список
        assert isinstance(result, list)

        # Если файл существует и не пустой, проверяем структуру
        if result:
            sample_transaction = result[0]
            assert "id" in sample_transaction
            assert "operationAmount" in sample_transaction