import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.file_handlers import read_transactions_file
from src.logger_config import setup_logger
from src.processing import filter_by_state, sort_by_date
from src.search import filter_by_description
from src.widget import get_date, mask_account_card

# Добавляем src в путь, если запускаем напрямую
sys.path.append(str(Path(__file__).parent))

# Настраиваем логгер
logger = setup_logger(__name__, "main.log")

# Доступные статусы
VALID_STATUSES = ["EXECUTED", "CANCELED", "PENDING"]


def print_welcome():
    """Выводит приветственное сообщение"""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")


def get_file_choice() -> Optional[str]:
    choice = input("> ").strip()

    file_map = {"1": "data/operations.json", "2": "data/transactions.csv", "3": "data/transactions_excel.xlsx"}

    if choice in file_map:
        file_path = file_map[choice]
        print(f"Для обработки выбран {Path(file_path).name}.")
        return file_path
    else:
        print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")
        return None


def get_status_filter() -> Optional[str]:
    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию")
        print(f"Доступные статусы: {', '.join(VALID_STATUSES)}")

        status = input("> ").strip().upper()

        if status in VALID_STATUSES:
            print(f'Операции отфильтрованы по статусу "{status}"')
            return status
        else:
            print(f'Статус операции "{status}" недоступен.')


def get_yes_no(question: str) -> bool:
    """
    Задает вопрос с ответом Да/Нет и возвращает булево значение
    """
    while True:
        answer = input(f"{question} Да/Нет\n> ").strip().lower()
        if answer in ["да", "lf", "yes", "y"]:  # поддерживаем разные варианты
            return True
        elif answer in ["нет", "ytn", "no", "n"]:
            return False
        else:
            print("Пожалуйста, ответьте 'Да' или 'Нет'.")


def get_sort_order() -> str:
    """
    Запрашивает порядок сортировки
    """
    while True:
        order = input("Отсортировать по возрастанию или по убыванию?\n> ").strip().lower()
        if order in ["возрастанию", "по возрастанию", "возрастание", "asc"]:
            return "asc"
        elif order in ["убыванию", "по убыванию", "убывание", "desc"]:
            return "desc"
        else:
            print("Пожалуйста, введите 'по возрастанию' или 'по убыванию'.")


def print_transactions(transactions: List[Dict[str, Any]]) -> None:
    """
    Красиво выводит список транзакций
    """
    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")

    for transaction in transactions:
        # Дата
        date = get_date(transaction.get("date", ""))
        description = transaction.get("description", "Неизвестная операция")
        print(f"{date} {description}")

        # Откуда и куда
        from_str = transaction.get("from", "")
        to_str = transaction.get("to", "")

        if from_str and to_str:
            print(f"{mask_account_card(from_str)} -> {mask_account_card(to_str)}")
        elif to_str:
            print(f"-> {mask_account_card(to_str)}")

        # Сумма
        amount = transaction.get("amount", 0)
        currency = transaction.get("currency_name", transaction.get("currency_code", "руб."))
        print(f"Сумма: {amount} {currency}\n")


def main() -> None:
    """
    Основная функция программы
    """
    logger.info("Запуск программы")

    # Приветствие и выбор файла
    print_welcome()

    file_path = None
    while file_path is None:
        file_path = get_file_choice()

    # Загрузка данных
    logger.info(f"Загрузка файла: {file_path}")
    transactions = read_transactions_file(file_path)

    if not transactions:
        print("Не удалось загрузить транзакции. Программа завершена.")
        logger.error("Не удалось загрузить транзакции")
        return

    # Фильтрация по статусу
    status = get_status_filter()
    if status is not None:
        filtered_by_status = filter_by_state(transactions, status)
    else:
        filtered_by_status = []
    # Дополнительные фильтры
    transactions_to_process = filtered_by_status.copy()

    # Сортировка по дате
    if get_yes_no("\nОтсортировать операции по дате?"):
        order = get_sort_order()
        transactions_to_process = sort_by_date(transactions_to_process, reverse=(order == "desc"))
        logger.info(f"Транзакции отсортированы по дате: {order}")

    # Фильтр по рублевым транзакциям
    if get_yes_no("\nВыводить только рублевые транзакции?"):
        rub_transactions = []
        for t in transactions_to_process:
            currency_code = t.get("currency_code", "").upper()
            currency_name = t.get("currency_name", "").upper()
            if currency_code == "RUB" or "РУБ" in currency_name or "RUB" in currency_name:
                rub_transactions.append(t)
        transactions_to_process = rub_transactions
        logger.info("Отфильтрованы только рублевые транзакции")

    # Поиск по описанию
    if get_yes_no("\nОтфильтровать список транзакций по определенному слову в описании?"):
        search_word = input("Введите слово для поиска:\n> ").strip()
        if search_word:
            transactions_to_process = filter_by_description(transactions_to_process, search_word)
            logger.info(f"Поиск по описанию: '{search_word}'")

    # Вывод результата
    print_transactions(transactions_to_process)
    logger.info(f"Программа завершена. Найдено транзакций: {len(transactions_to_process)}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        logger.error(f"Необработанная ошибка: {e}", exc_info=True)
