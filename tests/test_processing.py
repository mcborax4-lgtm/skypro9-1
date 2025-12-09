import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
        {"id": 2, "state": "PENDING", "date": "2024-02-10T12:30:00.000000"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-09T08:15:45.123456"},
        {"id": 4, "state": "CANCELED", "date": "2024-04-12T18:45:30.987654"},
        {"id": 5, "state": "EXECUTED", "date": "2023-12-31T23:59:59.999999"},
    ]


def test_filter_by_state_executed(sample_transactions):
    """Тест фильтрации по статусу EXECUTED"""
    result = filter_by_state(sample_transactions, "EXECUTED")
    result_ids = [t["id"] for t in result]
    assert result_ids == [1, 3, 5]


def test_filter_by_state_pending(sample_transactions):
    """Тест фильтрации по статусу PENDING"""
    result = filter_by_state(sample_transactions, "PENDING")
    result_ids = [t["id"] for t in result]
    assert result_ids == [2]


def test_filter_by_state_default(sample_transactions):
    """Тест фильтрации со статусом по умолчанию (EXECUTED)"""
    result = filter_by_state(sample_transactions)
    result_ids = [t["id"] for t in result]
    assert result_ids == [1, 3, 5]


def test_filter_by_state_empty_list():
    """Тест фильтрации пустого списка"""
    result = filter_by_state([], "EXECUTED")
    assert result == []


def test_filter_by_state_no_state_key():
    """Тест фильтрации транзакций без ключа state"""
    transactions = [
        {"id": 1, "date": "2024-03-11T02:26:18.671407"},
        {"id": 2, "state": "EXECUTED", "date": "2024-02-10T12:30:00.000000"},
    ]
    result = filter_by_state(transactions, "EXECUTED")
    result_ids = [t["id"] for t in result]
    assert result_ids == [2]


def test_sort_by_date_descending(sample_transactions):
    """Тест сортировки по убыванию даты (по умолчанию)"""
    result = sort_by_date(sample_transactions)
    result_ids = [t["id"] for t in result]
    assert result_ids == [4, 1, 2, 3, 5]


def test_sort_by_date_ascending(sample_transactions):
    """Тест сортировки по возрастанию даты"""
    result = sort_by_date(sample_transactions, reverse=False)
    result_ids = [t["id"] for t in result]
    assert result_ids == [5, 3, 2, 1, 4]


def test_sort_by_date_empty_list():
    """Тест сортировки пустого списка"""
    result = sort_by_date([], reverse=True)
    assert result == []


def test_sort_by_date_no_date_key():
    """Тест сортировки транзакций без даты"""
    transactions = [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
        {"id": 2, "state": "EXECUTED"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-01T00:00:00.000000"},
    ]
    result = sort_by_date(transactions)
    result_ids = [t["id"] for t in result]
    assert result_ids == [1, 3, 2]


def test_sort_by_date_invalid_date_format():
    """Тест сортировки с некорректным форматом даты"""
    transactions = [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
        {"id": 2, "state": "EXECUTED", "date": "not a date"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-01T00:00:00.000000"},
    ]
    result = sort_by_date(transactions)
    result_ids = [t["id"] for t in result]
    assert result_ids == [1, 3, 2]


def test_sort_by_date_z_timezone():
    """Тест сортировки с датами в формате с Z (UTC)"""
    transactions = [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407Z"},
        {"id": 2, "state": "EXECUTED", "date": "2024-01-01T00:00:00.000000Z"},
        {"id": 3, "state": "EXECUTED", "date": "2024-02-15T12:30:45.123456Z"},
    ]
    result = sort_by_date(transactions)
    result_ids = [t["id"] for t in result]
    assert result_ids == [1, 3, 2]


@pytest.mark.parametrize(
    "reverse, expected_ids",
    [
        (True, [1, 2, 3]),
        (False, [3, 2, 1]),
    ],
)
def test_sort_by_date_parametrized(reverse, expected_ids):
    """Параметризованный тест сортировки"""
    transactions = [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
        {"id": 2, "state": "EXECUTED", "date": "2024-02-10T12:30:00.000000"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-09T08:15:45.123456"},
    ]
    result = sort_by_date(transactions, reverse=reverse)
    result_ids = [t["id"] for t in result]
    assert result_ids == expected_ids
