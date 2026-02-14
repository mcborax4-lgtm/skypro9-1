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
```python
from src.masks import get_mask_card_number

masked = get_mask_card_number("7000792289606361")
print(masked)  # 7000 79** **** 6361
```
2. Модуль ```widget``` - работа со счетами и датами
```python
from src.widget import mask_account_card, get_date

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
```python
from src.processing import filter_by_state, sort_by_date

transactions = [
    {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
    {"id": 2, "state": "PENDING", "date": "2024-03-10T01:00:00.000000"},
]

# Фильтрация
executed = filter_by_state(transactions, "EXECUTED")

# Сортировка
sorted_transactions = sort_by_date(transactions)
```

## Тестирование

Проект покрыт тестами с использованием pytest. Покрытие кода составляет более 80%.

### Запуск тестов
   ``` bash
poetry run pytest tests/ -v
   ```
## Модуль generators.py

Новый модуль для работы с генераторами транзакций.

### Функции:

#### 1. `filter_by_currency(transactions, currency)`
Фильтрует транзакции по валюте и возвращает итератор.

```python
from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")
for transaction in usd_transactions:
    print(f"ID: {transaction['id']}, Amount: {transaction['operationAmount']['amount']}")
```

#### 2. `transaction_descriptions(transactions)`
Возвращает генератор описаний транзакций.
```python
from src.generators import transaction_descriptions
descriptions = transaction_descriptions(transactions)
for description in descriptions:
    print(description)    
 ```
#### 2. `card_number_generator(start, end)` 
Генерирует номера банковских карт в заданном диапазоне.
```python
from src.generators import card_number_generator

# Генерация первых 5 номеров карт
card_numbers = card_number_generator(1, 5)
for card in card_numbers:
    print(card)
# Вывод:
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
# 0000 0000 0000 0004
# 0000 0000 0000 0005
```
#### Особенности:
Все функции возвращают генераторы (ленивые вычисления)

card_number_generator автоматически форматирует номера карт

Функции работают с любой структурой транзакций, соответствующей ожидаемому формату
## Поддержка CSV и Excel форматов

### Новый модуль: `file_handlers.py`

Модуль предоставляет функции для чтения финансовых транзакций из разных форматов файлов.

#### Функции:

1. **`read_json_file(file_path)`**
   - Чтение данных из JSON файла
   - Возвращает список словарей с транзакциями
   - При ошибках возвращает пустой список

2. **`read_csv_file(file_path)`**  
   - Чтение данных из CSV файла с разделителем `;`
   - Использует библиотеку pandas для парсинга
   - Возвращает список словарей

3. **`read_excel_file(file_path)`**
   - Чтение данных из Excel файлов (XLSX/XLS)
   - Поддерживает форматы через библиотеку openpyxl
   - Возвращает список словарей

4. **`read_transactions_file(file_path)`** - **УНИВЕРСАЛЬНАЯ ФУНКЦИЯ**
   - Автоматически определяет формат файла по расширению:
     - `.json` → вызывает `read_json_file()`
     - `.csv` → вызывает `read_csv_file()`
     - `.xlsx` или `.xls` → вызывает `read_excel_file()`
   - Выбрасывает `ValueError` для неподдерживаемых форматов

#### Пример использования:
```python
from src.file_handlers import read_transactions_file

# Чтение разных форматов одной функцией
json_data = read_transactions_file("data/operations.json")
csv_data = read_transactions_file("data/transactions.csv")
excel_data = read_transactions_file("data/transactions_excel.xlsx")

print(f"JSON: {len(json_data)} записей")
print(f"CSV: {len(csv_data)} записей")
print(f"Excel: {len(excel_data)} записей")