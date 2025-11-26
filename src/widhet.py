def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета в зависимости от типа

    Args:
        account_info (str): Строка с типом и номером

    Returns:
        str: Замаскированный номер
    """
    # Находим последние 4 цифры (номер)
    digits = ''.join(filter(str.isdigit, account_info))
    last_four = digits[-4:] if len(digits) >= 4 else digits

    # Определяем тип
    if "счет" in account_info.lower():
        # Маскировка счета: **4305
        masked_number = f"**{last_four}"
        # Сохраняем оригинальное написание "Счет"
        account_type = "Счет"
    else:
        # Маскировка карты: 700079******6361
        if len(digits) == 16:
            masked_number = f"{digits[:6]}******{last_four}"
        else:
            masked_number = f"******{last_four}"
        # Берем все слова кроме цифр как тип карты
        words = account_info.split()
        account_type = ' '.join([word for word in words if not word.isdigit()])

    return f"{account_type} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата "2024-03-11T02:26:18.671407" в "11.03.2024"
    """
    # Берем только часть до T (дату)
    date_part = date_string.split("T")[0]

    # Разбиваем на год, месяц, день
    year, month, day = date_part.split("-")

    return f"{day}.{month}.{year}"