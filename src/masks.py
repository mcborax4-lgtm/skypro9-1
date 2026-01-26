from src.logger_config import setup_logger

# Инициализируем логгер
logger = setup_logger(__name__, 'masks.log')


def get_mask_card_number(card_number: str | int) -> str:
    """
    Маскирует номер карты в формате XXXX XX** **** XXXX
    """
    logger.info(f"Начало маскировки карты: {card_number}")

    # Конвертируем в строку если пришло число
    card_str = str(card_number)

    # Убираем все пробелы и нецифровые символы
    cleaned_number = "".join(filter(str.isdigit, card_str))

    # Проверяем, что номер содержит 16 цифр
    if len(cleaned_number) != 16:
        logger.error(f"Ошибка: номер карты должен содержать 16 цифр, получено {len(cleaned_number)}")
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Форматируем номер
    result = f"{cleaned_number[:4]} {cleaned_number[4:6]}** **** {cleaned_number[-4:]}"

    logger.info(f"Карта замаскирована: {result}")
    return result


def get_mask_account(account_number: str) -> str:
    """
    маскируем счет
    """
    logger.info(f"Начало маскировки счета: {account_number}")

    # Убираем все пробелы и нецифровые символы
    cleaned_number = "".join(filter(str.isdigit, account_number))

    # проверяем, что строка из 20 цифр
    if len(cleaned_number) != 20:
        logger.error(f"Ошибка: номер счета должен содержать 20 цифр, получено {len(cleaned_number)}")
        raise ValueError("Номер счета должен содержать 20 цифр")

    # Форматируем (ОБРАТИТЕ ВНИМАНИЕ: пробел между ** и цифрами!)
    result = f"** {cleaned_number[-4:]}"

    logger.info(f"Счет замаскирован: {result}")
    return result