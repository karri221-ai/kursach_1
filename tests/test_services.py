from src.services import search_by_phone
import json


def test_search_by_phone_found():
    transactions = [
        {"Описание": "МТС +7 921 11-22-33", "Категория": "Связь"},
        {"Описание": "Перевод Ивану", "Категория": "Переводы"},
        {"Описание": "Тинькофф +7 995 555-55-55", "Категория": "Связь"},
    ]
    result = json.loads(search_by_phone(transactions))
    assert len(result) == 2


def test_search_by_phone_not_found():
    transactions = [
        {"Описание": "Супермаркет Лента", "Категория": "Еда"},
        {"Описание": "Кофейня", "Категория": "Кафе"},
    ]
    result = json.loads(search_by_phone(transactions))
    assert result == []


def test_search_by_phone_format_89():
    transactions = [
        {"Описание": "Оплата 89001234567", "Категория": "Связь"},
    ]
    result = json.loads(search_by_phone(transactions))
    assert len(result) == 1
