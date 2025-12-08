import pytest
from src.masks import get_mask_card_number


class TestMasks:
    """Тесты для модуля masks.py"""

    @pytest.mark.parametrize("card_number, expected", [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("5555444433332222", "5555 44** **** 2222"),
        ("0000111122223333", "0000 11** **** 3333"),
    ])
    def test_valid_card_numbers(self, card_number, expected):
        """Тест маскировки валидных номеров карт"""
        result = get_mask_card_number(card_number)
        assert result == expected

    @pytest.mark.parametrize("card_number, expected", [
        ("7000 7922 8960 6361", "7000 79** **** 6361"),
        ("1234-5678-9012-3456", "1234 56** **** 3456"),
        ("5555 4444 3333 2222", "5555 44** **** 2222"),
    ])
    def test_card_numbers_with_separators(self, card_number, expected):
        """Тест маскировки номеров с разделителями"""
        result = get_mask_card_number(card_number)
        assert result == expected

    @pytest.mark.parametrize("invalid_card", [
        "123",
        "12345678901234567",
        "abcdefghijklmnop",
        "",
        "1234 5678 9012",  # только 12 цифр с пробелами
    ])
    def test_invalid_card_numbers(self, invalid_card):
        """Тест маскировки невалидных номеров карт"""
        with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
            get_mask_card_number(invalid_card)

    def test_type_error(self):
        """Тест передачи числа вместо строки"""
        # Теперь функция должна работать с числами
        result = get_mask_card_number(1234567890123456)
        assert result == "1234 56** **** 3456"


# Добавьте в tests/test_masks.py:

def test_get_mask_card_number_edge_cases():
    """Тест пограничных случаев"""
    # Тест с очень большим числом
    with pytest.raises(ValueError):
        get_mask_card_number("12345678901234567890")

    # Тест с невалидными символами
    assert get_mask_card_number("7000-7922-8960-6361") == "7000 79** **** 6361"

    # Тест с пробелами в разных местах
    assert get_mask_card_number("  7000  7922  8960  6361  ") == "7000 79** **** 6361"


def test_get_mask_card_number_special_characters():
    """Тест со специальными символами"""
    assert get_mask_card_number("7000a7922b8960c6361") == "7000 79** **** 6361"
    assert get_mask_card_number("7_0_0_0_7_9_2_2_8_9_6_0_6_3_6_1") == "7000 79** **** 6361"