# SkyPro9 - Проект для домашних заданий

Проект содержит набор утилит для обработки банковских транзакций.

## Установка

1. Убедитесь, что у вас установлен Python 3.13+
2. Установите Poetry:
   ``` bash
   pip install poetry 
   ```
3. Установите зависимости
   ``` bash
   poetry install
   ```
## Использование 
1. Модуль ```masks``` - маскировка номеров карт
```
from skypro9.masks import get_mask_card_number

masked = get_mask_card_number("7000792289606361")
print(masked)  # 7000 79** **** 6361
```
2. Модуль ```widget``` - работа со счетами и датами
```
from skypro9.widget import mask_account_card, get_date

# Маскировка карты
print(mask_account_card("Visa Platinum 7000792289606361"))
# Результат: Visa Platinum 700079******6361

# Маскировка счета
print(mask_account_card("Счет 73654108430135874305"))
# Результат: Счет **4305

# Форматирование даты
print(get_date("2024-03-11T02:26:18.671407"))
# Результат: 11.03.2024
```
3. Модуль ```processing``` - обработка транзакций
```
from skypro9.processing import filter_by_state, sort_by_date

transactions = [
    {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
    {"id": 2, "state": "PENDING", "date": "2024-03-10T01:00:00.000000"},
]

# Фильтрация
executed = filter_by_state(transactions, "EXECUTED")

# Сортировка
sorted_transactions = sort_by_date(transactions)
```

