import json
import os
from typing import Any, Dict, List

from src.logger_config import setup_logger

# Инициализируем логгер
logger = setup_logger(__name__, "utils.log")


def load_json_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает данные из JSON-файла.
    """
    logger.info(f"Попытка загрузить JSON файл: {file_path}")

    # Проверяем существует ли файл
    if not os.path.exists(file_path):
        logger.error(f"Файл не найден: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем что данные - список
        if isinstance(data, list):
            logger.info(f"Файл успешно загружен, записей: {len(data)}")
            return data
        else:
            logger.warning(f"Данные в файле не являются списком: {file_path}")
            return []

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка JSON в файле {file_path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Неизвестная ошибка при загрузке {file_path}: {e}")
        return []
