from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    for transaction in transactions:
        # Проверяем наличие ключа и соответствие валюты
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    for transaction in transactions:
        description = transaction.get("description", "")
        yield description


def card_number_generator(start: int, end: int) -> Iterator[str]:
    # Проверка диапазона
    if start < 1 or end > 9999999999999999 or start > end:
        raise ValueError(
            f"Диапазон должен быть от 1 до 9999999999999999, start <= end. " f"Получено: start={start}, end={end}"
        )

    for number in range(start, end + 1):
        # Форматируем номер с ведущими нулями
        card_str = f"{number:016d}"  # 16 цифр с ведущими нулями
        # Разбиваем на группы по 4 цифры
        formatted = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"
        yield formatted
