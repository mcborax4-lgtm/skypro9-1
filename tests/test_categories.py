from src.categories import count_by_category, count_by_custom_categories


def test_count_by_category_basic():
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод с карты"},
    ]

    result = count_by_category(transactions)
    assert result["Перевод организации"] == 2
    assert result["Открытие вклада"] == 1
    assert result["Перевод с карты"] == 1


def test_count_by_category_with_filter():
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод с карты"},
    ]

    categories = ["Перевод организации", "Кредит"]
    result = count_by_category(transactions, categories)

    assert result == {"Перевод организации": 1, "Кредит": 0}


def test_count_by_custom_categories():
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод с карты"},
        {"description": "Снятие наличных"},
    ]

    category_map = {"Переводы": ["перевод"], "Вклады": ["вклад", "открытие"], "Наличные": ["снятие"]}

    result = count_by_custom_categories(transactions, category_map)
    assert result["Переводы"] == 2
    assert result["Вклады"] == 1
    assert result["Наличные"] == 1
