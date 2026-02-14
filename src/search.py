import re
from typing import Any, Dict, List


def filter_by_description(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    if not transactions or not search_string:
        return []

    # Создаем регулярное выражение с флагом игнорирования регистра
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    # Фильтруем транзакции
    filtered = []
    for transaction in transactions:
        description = transaction.get("description", "")
        if pattern.search(description):
            filtered.append(transaction)

    return filtered
