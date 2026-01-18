from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_amount_to_rub, get_exchange_rate


class TestExternalAPI:
    """Тесты с использованием Mock для изоляции от реального API."""

    @patch("src.external_api.requests.get")
    @patch("src.external_api.os.getenv")
    def test_get_exchange_rate_success(self, mock_getenv, mock_requests_get):
        """Тест успешного получения курса валют."""
        # Мокаем переменные окружения
        mock_getenv.return_value = "test_api_key"

        # Мокаем ответ API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"rates": {"RUB": 75.5}, "base": "USD"}
        mock_requests_get.return_value = mock_response

        # Вызываем функцию
        result = get_exchange_rate("USD", "RUB")

        # Проверяем
        assert result == 75.5

        # Проверяем что запрос был с правильными параметрами
        mock_requests_get.assert_called_once()
        call_args = mock_requests_get.call_args
        assert call_args[1]["params"]["base"] == "USD"
        assert call_args[1]["params"]["symbols"] == "RUB"
        assert call_args[1]["headers"]["apikey"] == "test_api_key"

    @patch("src.external_api.requests.get")
    @patch("src.external_api.os.getenv")
    def test_get_exchange_rate_api_error(self, mock_getenv, mock_requests_get):
        """Тест ошибки API."""
        mock_getenv.return_value = "test_api_key"

        mock_response = Mock()
        mock_response.status_code = 401  # Ошибка авторизации
        mock_requests_get.return_value = mock_response

        result = get_exchange_rate("USD", "RUB")

        assert result is None

    @patch("src.external_api.get_exchange_rate")
    def test_convert_amount_to_rub_usd(self, mock_get_rate):
        """Тест конвертации USD в RUB."""
        # Мокаем курс
        mock_get_rate.return_value = 75.5

        transaction = {"operationAmount": {"amount": "100.50", "currency": {"code": "USD", "name": "US Dollar"}}}

        result = convert_amount_to_rub(transaction)

        assert result == 7587.75
        mock_get_rate.assert_called_once_with("USD", "RUB")

    def test_convert_amount_to_rub_rub(self):
        """Тест когда валюта уже в RUB."""
        transaction = {"operationAmount": {"amount": "5000.00", "currency": {"code": "RUB", "name": "руб."}}}

        result = convert_amount_to_rub(transaction)

        assert result == 5000.0

    @patch("src.external_api.get_exchange_rate")
    def test_convert_amount_to_rub_api_failure(self, mock_get_rate):
        """Тест когда API не отвечает."""
        mock_get_rate.return_value = None

        transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD", "name": "US Dollar"}}}

        result = convert_amount_to_rub(transaction)

        assert result is None

    def test_convert_amount_invalid_transaction(self):
        """Тест с некорректной транзакцией."""
        # Транзакция без operationAmount
        transaction = {"id": 1}

        result = convert_amount_to_rub(transaction)

        assert result is None


if __name__ == "__main__":
    pytest.main()
