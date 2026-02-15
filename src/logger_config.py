import logging
from pathlib import Path


def setup_logger(name: str, log_file: str, level: int = logging.INFO) -> logging.Logger:
    """
    Настройка логгера
    """
    # создаем папку logs если её нет
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # очищаем предыдущие обработчики
    if logger.handlers:
        logger.handlers.clear()

    # формат сообщения
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # файловый обработчик
    file_handler = logging.FileHandler(log_dir / log_file, mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
