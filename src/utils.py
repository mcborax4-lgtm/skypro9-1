"""
Модуль utils для работы с файлами и данными.
"""

import json
import os
from typing import Any, Dict, List


def load_json_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает данные из JSON-файла.

    Args:
        file_path: Путь к JSON-файлу

    Returns:
        Список словарей с данными или пустой список в случае ошибки
    """
    # Проверяем существует ли файл
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем что данные  список
        if isinstance(data, list):
            return data
        else:
            return []

    except (json.JSONDecodeError, FileNotFoundError):
        # Файл пустой, невалидный JSON или другие ошибки
        return []
    except Exception:
        # Любые другие ошибки
        return []
