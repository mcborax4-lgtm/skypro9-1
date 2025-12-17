from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми транзакциями."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2024-01-01T12:00:00.000000",
            "operationAmount": {"amount": "100.00", "currency": {"code": "USD", "name": "US Dollar"}},
            "description": "Payment 1",
            "from": "Card 1234 5678 9012 3456",
            "to": "Account 12345678901234567890",
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2024-01-02T12:00:00.000000",
            "operationAmount": {"amount": "200.00", "currency": {"code": "EUR", "name": "Euro"}},
            "description": "Payment 2",
            "from": "Card 2345 6789 0123 4567",
            "to": "Account 23456789012345678901",
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2024-01-03T12:00:00.000000",
            "operationAmount": {"amount": "300.00", "currency": {"code": "USD", "name": "US Dollar"}},
            "description": "Payment 3",
            "from": "Card 3456 7890 1234 5678",
            "to": "Account 34567890123456789012",
        },
    ]


class TestFilterByCurrency:
    """Тесты для функции filter_by_currency."""

    def test_filter_usd_transactions(self, sample_transactions):
        """Тест фильтрации транзакций в USD."""
        usd_transactions = list(filter_by_currency(sample_transactions, "USD"))

        assert len(usd_transactions) == 2
        assert usd_transactions[0]["id"] == 1
        assert usd_transactions[1]["id"] == 3

    def test_filter_eur_transactions(self, sample_transactions):
        """Тест фильтрации транзакций в EUR."""
        eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))

        assert len(eur_transactions) == 1
        assert eur_transactions[0]["id"] == 2

    def test_filter_no_matches(self, sample_transactions):
        """Тест фильтрации при отсутствии совпадений."""
        rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))

        assert len(rub_transactions) == 0

    def test_empty_transactions_list(self):
        """Тест с пустым списком транзакций."""
        empty_result = list(filter_by_currency([], "USD"))

        assert len(empty_result) == 0

    def test_transaction_without_currency(self):
        """Тест обработки транзакции без информации о валюте."""
        transactions = [{"id": 1, "operationAmount": {"amount": "100.00"}}]

        result = list(filter_by_currency(transactions, "USD"))

        assert len(result) == 0

    def test_generator_behavior(self, sample_transactions):
        """Тест ленивого поведения генератора."""
        generator = filter_by_currency(sample_transactions, "USD")

        # Генератор не должен сразу возвращать все значения
        assert next(generator)["id"] == 1
        assert next(generator)["id"] == 3

        with pytest.raises(StopIteration):
            next(generator)


class TestTransactionDescriptions:
    """Тесты для функции transaction_descriptions."""

    def test_get_all_descriptions(self, sample_transactions):
        """Тест получения всех описаний."""
        descriptions = list(transaction_descriptions(sample_transactions))

        expected = ["Payment 1", "Payment 2", "Payment 3"]
        assert descriptions == expected

    def test_empty_transactions_list(self):
        """Тест с пустым списком транзакций."""
        descriptions = list(transaction_descriptions([]))

        assert descriptions == []

    def test_transaction_without_description(self):
        """Тест обработки транзакции без описания."""

        transactions: List[Dict[str, Any]] = [{"id": 1}, {"description": "Test"}]

        descriptions = list(transaction_descriptions(transactions))

        assert descriptions == ["", "Test"]

    def test_generator_behavior(self, sample_transactions):
        """Тест ленивого поведения генератора."""
        generator = transaction_descriptions(sample_transactions)

        assert next(generator) == "Payment 1"
        assert next(generator) == "Payment 2"
        assert next(generator) == "Payment 3"


class TestCardNumberGenerator:
    """Тесты для функции card_number_generator."""

    @pytest.mark.parametrize(
        "start,end,expected_count,expected_first,expected_last",
        [
            (1, 5, 5, "0000 0000 0000 0001", "0000 0000 0000 0005"),
            (9999999999999995, 9999999999999999, 5, "9999 9999 9999 9995", "9999 9999 9999 9999"),
            (1234567890123456, 1234567890123456, 1, "1234 5678 9012 3456", "1234 5678 9012 3456"),
            (100, 105, 6, "0000 0000 0000 0100", "0000 0000 0000 0105"),
        ],
    )
    def test_valid_ranges(self, start, end, expected_count, expected_first, expected_last):
        """Тест генератора с различными валидными диапазонами."""
        generator = card_number_generator(start, end)
        numbers = list(generator)

        assert len(numbers) == expected_count
        assert numbers[0] == expected_first
        assert numbers[-1] == expected_last

    def test_single_number(self):
        """Тест генерации одного номера."""
        generator = card_number_generator(42, 42)
        numbers = list(generator)

        assert len(numbers) == 1
        assert numbers[0] == "0000 0000 0000 0042"

    @pytest.mark.parametrize(
        "start,end",
        [
            (0, 10),  # start < 1
            (10, 5),  # start > end
            (1, 10000000000000000),  # end > 9999999999999999
            (-5, 10),  # start отрицательный
        ],
    )
    def test_invalid_ranges(self, start, end):
        """Тест невалидных диапазонов."""
        with pytest.raises(ValueError, match="Диапазон должен быть"):
            list(card_number_generator(start, end))

    def test_generator_behavior(self):
        """Тест ленивого поведения генератора."""
        generator = card_number_generator(1, 3)

        assert next(generator) == "0000 0000 0000 0001"
        assert next(generator) == "0000 0000 0000 0002"
        assert next(generator) == "0000 0000 0000 0003"

        with pytest.raises(StopIteration):
            next(generator)

    def test_format_correctness(self):
        """Тест правильности форматирования номера карты."""
        generator = card_number_generator(1234567890123456, 1234567890123456)
        number = next(generator)

        # Проверяем формат: 4 группы по 4 цифры, разделенные пробелами
        parts = number.split()
        assert len(parts) == 4
        assert all(len(part) == 4 for part in parts)
        assert all(part.isdigit() for part in parts)

        # Проверяем, что число восстановилось правильно
        combined = "".join(parts)
        assert int(combined) == 1234567890123456

    def test_leading_zeros(self):
        """Тест генерации номеров с ведущими нулями."""
        generator = card_number_generator(1, 1)
        number = next(generator)

        assert number == "0000 0000 0000 0001"
        assert number.startswith("0000 0000 0000")


if __name__ == "__main__":
    pytest.main()
