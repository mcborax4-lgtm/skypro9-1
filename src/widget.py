from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str | int | float) -> str:
    # Гарантированно преобразуем в строку
    account_info = str(account_info).strip()

    if not account_info:
        return account_info

    # Разделяем на части
    parts = account_info.split()

    if len(parts) < 2:
        return account_info

    # Определяем тип (счет или карта)
    if "счет" in account_info.lower():
        # Для счета
        account_number = parts[-1]
        masked = get_mask_account(account_number)
        return f"{' '.join(parts[:-1])} {masked}"
    else:
        # Для карты
        card_number = parts[-1]
        # Убираем все нецифровые символы из номера карты
        clean_number = "".join(filter(str.isdigit, card_number))
        if clean_number:
            masked = get_mask_card_number(clean_number)
            return f"{' '.join(parts[:-1])} {masked}"

    return account_info


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
