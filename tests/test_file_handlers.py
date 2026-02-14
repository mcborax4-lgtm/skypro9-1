import pytest
import pandas as pd
from pathlib import Path
import tempfile
import json
import os
from src.file_handlers import (
    read_json_file,
    read_csv_file,
    read_excel_file,
    read_transactions_file
)


@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 650703,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210,
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации"
        }
    ]


@pytest.fixture
def temp_json_file(sample_transactions):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_transactions, f)
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)


@pytest.fixture
def temp_csv_file(sample_transactions):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df = pd.DataFrame(sample_transactions)
        df.to_csv(f, index=False, sep=';')
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)


@pytest.fixture
def temp_excel_file(sample_transactions):
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.xlsx', delete=False) as f:
        df = pd.DataFrame(sample_transactions)
        df.to_excel(f, index=False)
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)


def test_read_json_file(temp_json_file, sample_transactions):
    result = read_json_file(temp_json_file)
    assert len(result) == len(sample_transactions)


def test_read_excel_file(temp_excel_file, sample_transactions):
    result = read_excel_file(temp_excel_file)
    assert len(result) == len(sample_transactions)


def test_read_transactions_file_json(temp_json_file):
    result = read_transactions_file(temp_json_file)
    assert len(result) == 1


def test_read_transactions_file_excel(temp_excel_file):
    result = read_transactions_file(temp_excel_file)
    assert len(result) == 1


def test_read_transactions_file_unsupported_format():
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
        temp_path = f.name
    try:
        with pytest.raises(ValueError):
            read_transactions_file(temp_path)
    finally:
        os.unlink(temp_path)