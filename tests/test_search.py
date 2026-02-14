from src.search import filter_by_description


def test_filter_by_description_basic():
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод с карты на карту"},
    ]

    result = filter_by_description(transactions, "перевод")
    assert len(result) == 2
    assert all("перевод" in t["description"].lower() for t in result)


def test_filter_by_description_case_insensitive():
    transactions = [
        {"description": "ПЕРЕВОД ОРГАНИЗАЦИИ"},
        {"description": "перевод с карты"},
        {"description": "Открытие вклада"},
    ]

    result = filter_by_description(transactions, "Перевод")
    assert len(result) == 2


def test_filter_by_description_empty_result():
    transactions = [{"description": "Перевод организации"}, {"description": "Открытие вклада"}]

    result = filter_by_description(transactions, "кредит")
    assert result == []


def test_filter_by_description_empty_input():
    assert filter_by_description([], "перевод") == []
    assert filter_by_description([{"description": "test"}], "") == []
