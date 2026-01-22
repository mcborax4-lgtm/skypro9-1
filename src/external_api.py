import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()


def get_exchange_rate(from_currency: str, to_currency: str = "RUB") -> Optional[float]:
    """
    Получает текущий курс валюты через API.
    """
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")

    if not api_key:
        print("Ошибка: API ключ не найден в переменных окружения")
        return None

    url = "https://api.apilayer.com/exchangerates_data/latest"

    try:
        response = requests.get(
            url, params={"base": from_currency, "symbols": to_currency}, headers={"apikey": api_key}, timeout=10
        )

        if response.status_code == 200:
            data: Dict[str, Any] = response.json()
            rates = data.get("rates", {})
            rate = rates.get(to_currency)

            # Преобразуем в float если возможно
            if isinstance(rate, (int, float)):
                return float(rate)
            return None
        else:
            print(f"Ошибка API: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка подключения: {e}")
        return None
    except (KeyError, ValueError, TypeError) as e:
        print(f"Ошибка обработки ответа: {e}")
        return None


def convert_amount_to_rub(transaction: Dict[str, Any]) -> Optional[float]:
    """
    Конвертирует сумму транзакции в рубли.
    """
    try:
        # Получаем сумму и валюту
        operation_amount = transaction["operationAmount"]
        amount_str = operation_amount["amount"]
        currency_code = operation_amount["currency"]["code"]

        # Преобразуем сумму в float
        amount = float(amount_str)

        # Если уже рубли - возвращаем как есть
        if currency_code == "RUB":
            return amount

        # Если USD или EUR - конвертируем
        if currency_code in ["USD", "EUR"]:
            rate = get_exchange_rate(currency_code, "RUB")
            if rate is not None:
                return round(amount * rate, 2)
            else:
                print(f"Не удалось получить курс {currency_code} -> RUB")
                return None

        # Если другая валюта
        print(f"Валюта {currency_code} не поддерживается для конвертации")
        return None

    except (KeyError, ValueError, TypeError) as e:
        print(f"Ошибка обработки транзакции: {e}")
        return None
