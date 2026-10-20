import pandas as pd
import pytest
from unittest.mock import patch
from src.views import get_greeting, get_cards_info, get_top_transactions


def test_get_greeting_morning():
    assert get_greeting("2021-12-31 06:00:00") == "Доброе утро"


def test_get_greeting_day():
    assert get_greeting("2021-12-31 12:00:00") == "Добрый день"


def test_get_greeting_evening():
    assert get_greeting("2021-12-31 18:00:00") == "Добрый вечер"


def test_get_greeting_night():
    assert get_greeting("2021-12-31 23:00:00") == "Доброй ночи"


@pytest.fixture
def sample_df():
    return pd.DataFrame([
        {
            "Номер карты": "*1234",
            "Статус": "OK",
            "Сумма платежа": -100.0,
            "Дата платежа": "31.12.2021",
            "Категория": "Супермаркеты",
            "Описание": "Лента"
        },
        {
            "Номер карты": "*1234",
            "Статус": "OK",
            "Сумма платежа": -200.0,
            "Дата платежа": "30.12.2021",
            "Категория": "Кафе",
            "Описание": "Кофейня"
        },
        {
            "Номер карты": "*5678",
            "Статус": "FAILED",
            "Сумма платежа": -50.0,
            "Дата платежа": "29.12.2021",
            "Категория": "Аптеки",
            "Описание": "Аптека"
        }
    ])


def test_get_cards_info(sample_df):
    result = get_cards_info(sample_df)
    assert len(result) == 1
    assert result[0]["last_digits"] == "1234"
    assert result[0]["total_spent"] == 300.0
    assert result[0]["cashback"] == 3.0


def test_get_top_transactions(sample_df):
    result = get_top_transactions(sample_df)
    assert len(result) <= 5
    assert result[0]["amount"] == -50.0


def test_get_currency_rates():
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"result": 84.5}
        from src.views import get_currency_rates
        result = get_currency_rates(["USD"])
        assert result[0]["currency"] == "USD"
        assert result[0]["rate"] == 84.5


def test_get_stock_prices():
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {
            "Global Quote": {"05. price": "150.00"}
        }
        from src.views import get_stock_prices
        result = get_stock_prices(["AAPL"])
        assert result[0]["stock"] == "AAPL"
        assert result[0]["price"] == 150.0
