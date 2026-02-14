import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Union


def read_json_file(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Читает транзакции из JSON файла.

    Возвращает пустой список если файл не найден, поврежден или содержит не список.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем что загруженные данные - список
        if isinstance(data, list):
            return data
        return []
    except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError):
        # Файла нет, невалидный JSON или проблемы с кодировкой
        return []
    except Exception:
        # Любая другая ошибка
        return []


def read_csv_file(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Читает транзакции из CSV файла.

    CSV должен использовать разделитель ';'.
    Возвращает пустой список при ошибках чтения.
    """
    try:
        # Читаем CSV с указанием разделителя
        df = pd.read_csv(file_path, delimiter=';')
        # Преобразуем DataFrame в список словарей
        return df.to_dict('records')
    except (FileNotFoundError, pd.errors.EmptyDataError):
        # Файла нет или он пустой
        return []
    except Exception:
        # Ошибки парсинга CSV, неверная структура и т.д.
        return []


def read_excel_file(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Читает транзакции из Excel файла (XLSX или XLS).

    Возвращает пустой список при ошибках чтения.
    """
    try:
        # Читаем Excel файл
        df = pd.read_excel(file_path)
        # Преобразуем DataFrame в список словарей
        return df.to_dict('records')
    except (FileNotFoundError, ValueError):
        # Файла нет или он поврежден
        return []
    except Exception:
        # Другие ошибки (например, нет openpyxl)
        return []


def read_transactions_file(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Универсальная функция для чтения файлов разных форматов.

    Определяет формат по расширению файла:
    - .json -> читает как JSON
    - .csv -> читает как CSV
    - .xlsx/.xls -> читает как Excel

    Выбрасывает ValueError если формат не поддерживается.
    """
    # Преобразуем в Path для удобства работы с расширением
    path = Path(file_path)

    # Получаем расширение файла в нижнем регистре
    extension = path.suffix.lower()

    if extension == '.json':
        return read_json_file(file_path)
    elif extension == '.csv':
        return read_csv_file(file_path)
    elif extension in ['.xlsx', '.xls']:
        return read_excel_file(file_path)
    else:
        # Формат не поддерживается
        raise ValueError(f"Формат файла '{extension}' не поддерживается. "
                         f"Используйте .json, .csv или .xlsx")