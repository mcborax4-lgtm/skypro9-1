def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета в зависимости от типа
    """
    # Разделяем на слова
    words = account_info.split()
    if len(words) < 2:
        return account_info

    # Последнее слово - номер
    number = words[-1]

    # Все остальное - тип
    account_type = " ".join(words[:-1])

    # Очищаем номер от нецифровых символов
    digits = "".join(filter(str.isdigit, number))
    if not digits:
        return account_info

    last_four = digits[-4:]

    # Приводим тип к нижнему регистру для проверки
    type_lower = account_type.lower()

    # Проверяем является ли это счетом
    is_account = any(keyword in type_lower for keyword in ["счет", "account"])

    # Также проверяем вариант с латинской C
    if not is_account:
        # Заменяем латинскую c на кириллическую
        type_with_cyrillic_c = type_lower.replace("c", "с")
        is_account = "счет" in type_with_cyrillic_c

    if is_account:
        return f"{account_type} **{last_four}"
    else:
        # Для карт
        if len(digits) >= 16:
            masked_number = f"{digits[:6]}******{last_four}"
        else:
            masked_number = f"******{last_four}"
        return f"{account_type} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата "2024-03-11T02:26:18.671407" в "11.03.2024"
    """
    try:
        # Берем только часть до T (дату)
        if "T" in date_string:
            date_part = date_string.split("T")[0]
        else:
            date_part = date_string

        # Разбиваем на год, месяц, день
        parts = date_part.split("-")
        if len(parts) != 3:
            return date_string  # Если формат неправильный, возвращаем как есть

        year, month, day = parts
        return f"{day}.{month}.{year}"
    except (ValueError, IndexError):
        # Если что-то пошло не так, возвращаем оригинальную строку
        return date_string
