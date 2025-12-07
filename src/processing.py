from datetime import datetime
from typing import List, Dict, Any, Optional


def filter_by_state(
        transactions: List[Dict[str, Any]],
        state: str = "EXECUTED"
) -> List[Dict[str, Any]]:
    """
    Фильтрует список транзакций по статусу
    """
    return [t for t in transactions if t.get("state") == state]


def sort_by_date(
        transactions: List[Dict[str, Any]],
        reverse: bool = True
) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате
    """

    def get_date(transaction: Dict[str, Any]) -> datetime:
        date_str = transaction.get("date", "")
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return datetime.min

    return sorted(transactions, key=get_date, reverse=reverse)