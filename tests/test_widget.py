import pytest

from src.widget import get_date, mask_account_card


class TestWidget:
    """Тесты для функций виджета."""

    # Тесты для mask_account_card с картами
    @pytest.mark.parametrize(
        "input_str, expected",
        [
            ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
            ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
            ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
            ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
            ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
            ("МИР 1234567890123456", "МИР 1234 56** **** 3456"),
        ],
    )
    def test_mask_account_card_for_cards(self, input_str, expected):
        """Тест маскировки карт."""
        assert mask_account_card(input_str) == expected

    # Тесты для mask_account_card со счетами
    @pytest.mark.parametrize(
        "input_str, expected",
        [
            ("Счет 73654108430135874305", "Счет ** 4305"),
            ("счет 64686473678894779589", "счет ** 9589"),
            ("СЧЕТ 89992000333344445555", "СЧЕТ ** 5555"),
        ],
    )
    def test_mask_account_card_for_accounts(self, input_str, expected):
        """Тест маскировки счетов."""
        assert mask_account_card(input_str) == expected

    # Тесты с нестандартными случаями
    @pytest.mark.parametrize(
        "input_str, expected",
        [
            ("Счет 12345678901234567890", "Счет ** 7890"),
            ("Карта 1234567890123456", "Карта 1234 56** **** 3456"),
        ],
    )
    def test_mask_account_card_edge_cases(self, input_str, expected):
        """Тест маскировки с нестандартными форматами."""
        assert mask_account_card(input_str) == expected

    # Тесты для get_date
    @pytest.mark.parametrize(
        "input_str, expected",
        [
            ("2024-03-11T02:26:18.671407", "11.03.2024"),
            ("2023-12-31T23:59:59", "31.12.2023"),
            ("2024-01-01T00:00:00", "01.01.2024"),
        ],
    )
    def test_get_date(self, input_str, expected):
        """Тест форматирования даты."""
        assert get_date(input_str) == expected

    def test_get_date_invalid_format(self):
        """Тест с некорректным форматом даты."""
        assert get_date("не дата") == "не дата"
