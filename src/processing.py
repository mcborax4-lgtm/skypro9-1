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

