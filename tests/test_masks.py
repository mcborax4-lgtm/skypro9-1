import pytest

from src.masks import get_mask_card_number, get_mask_account


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

def test_get_mask_account_valid():
    """Тест маскировки валидного номера счета"""
    assert get_mask_account("73654108430135874305") == "** 4305"
    assert get_mask_account("12345678901234567890") == "** 7890"
    assert get_mask_account("00000000000000000001") == "** 0001"


def test_get_mask_account_with_spaces():
    """Тест маскировки номера счета с пробелами"""
    assert get_mask_account("7365 4108 4301 3587 4305") == "** 4305"
    assert get_mask_account("1234 5678 9012 3456 7890") == "** 7890"


def test_get_mask_account_with_dashes():
    """Тест маскировки номера счета с дефисами"""
    assert get_mask_account("7365-4108-4301-3587-4305") == "** 4305"
    assert get_mask_account("1234-5678-9012-3456-7890") == "** 7890"


@pytest.mark.parametrize(
    "invalid_account",
    [
        "123",
        "123456789012345678901",
        "abcdefghijklmnopqrst",
        "",
        "1234 5678 9012 3456",
    ]
)
def test_get_mask_account_invalid(invalid_account):
    """Тест маскировки невалидных номеров счетов"""
    with pytest.raises(ValueError, match="Номер счета должен содержать 20 цифр"):
        get_mask_account(invalid_account)


def test_get_mask_account_mixed_characters():
    """Тест с смешанными символами"""
    assert get_mask_account("7365a4108b4301c3587d4305") == "** 4305"
    assert get_mask_account("1234-5678-9012-3456-7890") == "** 7890"
    assert get_mask_account("1234 5678 9012 3456 7890") == "** 7890"


def test_get_mask_account_special_formats():
    """Тест со специальными форматами"""
    assert get_mask_account("1234.5678.9012.3456.7890") == "** 7890"
    assert get_mask_account("  1234  5678  9012  3456  7890  ") == "** 7890"
    assert get_mask_account("1234_5678_9012_3456_7890") == "** 7890"