import pytest
from src.widhet import mask_account_card, get_date


class TestWidget:
    """Тесты для модуля widhet.py (с опечаткой)"""

    # Тесты для mask_account_card
    @pytest.mark.parametrize("account_info, expected", [
        ("Visa Platinum 7000792289606361", "Visa Platinum 700079******6361"),
        ("Maestro 1596837868705199", "Maestro 159683******5199"),
        ("MasterCard 7158300734726758", "MasterCard 715830******6758"),
        ("Visa Classic 6831982476737658", "Visa Classic 683198******7658"),
        ("Visa Gold 5999414228426353", "Visa Gold 599941******6353"),
        ("МИР 1234567890123456", "МИР 123456******3456"),
    ])
    def test_mask_account_card_for_cards(self, account_info, expected):
        """Тест маскировки банковских карт"""
        result = mask_account_card(account_info)
        assert result == expected

    @pytest.mark.parametrize("account_info, expected", [
        ("Счет 73654108430135874305", "Счет **4305"),
        ("счет 64686473678894779589", "счет **9589"),
        ("Cчет 35383033474447895560", "Cчет **5560"),
        ("СЧЕТ 89992000333344445555", "СЧЕТ **5555"),
        ("Account 12345678901234567890", "Account **7890"),
    ])
    def test_mask_account_card_for_accounts(self, account_info, expected):
        """Тест маскировки счетов (разные написания)"""
        result = mask_account_card(account_info)
        assert result == expected

    @pytest.mark.parametrize("account_info", [
        "Карта 123",  # слишком мало цифр
        "Счет 123",  # слишком мало цифр
        "",  # пустая строка
        "Только текст без цифр",
    ])
    def test_mask_account_card_edge_cases(self, account_info):
        """Тест пограничных случаев"""
        result = mask_account_card(account_info)
        assert isinstance(result, str)  # Должен вернуть строку

    # Тесты для get_date
    @pytest.mark.parametrize("date_string, expected", [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2025-01-01T00:00:00.000000", "01.01.2025"),
        ("2000-02-29T12:30:45.123456", "29.02.2000"),
        ("1999-09-09T09:09:09.090909", "09.09.1999"),
    ])
    def test_get_date_valid(self, date_string, expected):
        """Тест форматирования валидных дат"""
        result = get_date(date_string)
        assert result == expected

    @pytest.mark.parametrize("invalid_date, expected", [
        ("2024-03-11", "11.03.2024"),  # работает и без T
        ("11.03.2024", "11.03.2024"),  # возвращает как есть
        ("not a date", "not a date"),  # возвращает как есть
        ("", ""),  # возвращает как есть
    ])
    def test_get_date_invalid(self, invalid_date, expected):
        """Тест с некорректными датами"""
        result = get_date(invalid_date)
        assert result == expected