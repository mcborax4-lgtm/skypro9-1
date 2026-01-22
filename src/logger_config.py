import logging
import os
from pathlib import Path


def setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:
    """
    Настройка логгера для модуля

    Args:
        name: Имя логгера (обычно __name__)
        log_file: Имя файла для логов (например, 'masks.log')
        level: Уровень логирования

    Returns:
        logging.Logger: Настроенный логгер
    """
    # Создаём папку logs, если её нет
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Полный путь к файлу лога
    full_log_path = log_dir / log_file

    # Создаём логгер
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Очищаем предыдущие обработчики (чтобы не дублировались)
    logger.handlers.clear()

    # Формат сообщения: время, имя модуля, уровень, сообщение
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Файловый обработчик с перезаписью при каждом запуске
    file_handler = logging.FileHandler(
        full_log_path,
        mode='w',  # 'w' - перезапись файла при каждом запуске
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)

    return logger