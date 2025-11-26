def get_mask_card_number(card_number: str) -> str:
    """
    Маскируем номер карты
    """
    # Убираем все пробелы и нецифровые символы
    cleaned_number = "".join(filter(str.isdigit, card_number))

    # Проверяем, что номер содержит 16 цифр
    if len(cleaned_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Разбиваем на части и маскируем
    part1 = cleaned_number[:4]  # первые 4 цифры
    part2 = cleaned_number[4:6] + "**"  # следующие 2 цифры + **
    part3 = "****"  # полностью скрытая часть
    part4 = cleaned_number[-4:]  # последние 4 цифры

    # Собираем вместе с пробелами
    return f"{part1} {part2} {part3} {part4}"


def get_mask_account(account_number: str) -> str:
    """
    маскируем счет
    """
    # Убираем все пробелы и нецифровые символы
    cleaned_number = "".join(filter(str.isdigit, account_number))
    # проверяем, что строка из 20 цифр
    if len(cleaned_number) != 20:
        raise ValueError("Номер счета должен содержать 20 цифр")
    # разбиваем на части
    part1 = "**"
    part2 = cleaned_number[-4:]
    return f"{part1} {part2}"
