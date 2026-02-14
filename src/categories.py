from collections import Counter
from typing import Any, Dict, List, Optional


def count_by_category(transactions: List[Dict[str, Any]], categories: Optional[List[str]] = None) -> Dict[str, int]:
    if not transactions:
        return {}

    # Собираем все описания
    descriptions = [t.get("description", "") for t in transactions if t.get("description")]

    if categories:
        # Подсчитываем только указанные категории
        counter = Counter(descriptions)
        return {cat: counter.get(cat, 0) for cat in categories}
    else:
        # Подсчитываем все категории
        return dict(Counter(descriptions))


def count_by_custom_categories(
    transactions: List[Dict[str, Any]], category_map: Dict[str, List[str]]
) -> Dict[str, int]:
    result = {category: 0 for category in category_map}

    for transaction in transactions:
        description = transaction.get("description", "").lower()

        for category, keywords in category_map.items():
            for keyword in keywords:
                if keyword.lower() in description:
                    result[category] += 1
                    break

    return result
