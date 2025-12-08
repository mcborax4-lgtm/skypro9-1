def get_mask_card_number(card_number: str | int) -> str:
    """
    Маскирует номер карты в формате XXXX XX** **** XXXX
    """
    # Конвертируем в строку если пришло число
    card_str = str(card_number)

    # Убираем все пробелы и нецифровые символы
    cleaned_number = "".join(filter(str.isdigit, card_str))

    # Проверяем, что номер содержит 16 цифр
    if len(cleaned_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Форматируем номер
    return f"{cleaned_number[:4]} {cleaned_number[4:6]}** **** {cleaned_number[-4:]}"

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
