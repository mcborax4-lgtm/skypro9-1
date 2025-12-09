import pytest

from src.masks import get_mask_card_number


def test_valid_card_numbers():
    """Тест маскировки валидных номеров карт"""
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"
    assert get_mask_card_number("5555444433332222") == "5555 44** **** 2222"


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("7000 7922 8960 6361", "7000 79** **** 6361"),
        ("1234-5678-9012-3456", "1234 56** **** 3456"),
        ("5555 4444 3333 2222", "5555 44** **** 2222"),
    ],
)
def test_card_numbers_with_separators(card_number, expected):
    """Тест маскировки номеров с разделителями"""
    result = get_mask_card_number(card_number)
    assert result == expected


@pytest.mark.parametrize(
    "invalid_card",
    [
        "123",
        "12345678901234567",
        "abcdefghijklmnop",
        "",
        "1234 5678 9012",
    ],
)
def test_invalid_card_numbers(invalid_card):
    """Тест маскировки невалидных номеров карт"""
    with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
        get_mask_card_number(invalid_card)


def test_int_input():
    """Тест с числовым вводом"""
    assert get_mask_card_number(1234567890123456) == "1234 56** **** 3456"
    assert get_mask_card_number(7000792289606361) == "7000 79** **** 6361"


def test_mixed_characters():
    """Тест с смешанными символами"""
    assert get_mask_card_number("7000a7922b8960c6361") == "7000 79** **** 6361"
    assert get_mask_card_number("7000-7922-8960-6361") == "7000 79** **** 6361"
    assert get_mask_card_number("7000 7922 8960 6361") == "7000 79** **** 6361"


def test_special_formats():
    """Тест со специальными форматами"""
    assert get_mask_card_number("1234-5678-9012-3456") == "1234 56** **** 3456"
    assert get_mask_card_number("  1234  5678  9012  3456  ") == "1234 56** **** 3456"
    assert get_mask_card_number("1234_5678_9012_3456") == "1234 56** **** 3456"
