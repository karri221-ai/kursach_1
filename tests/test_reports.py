import pandas as pd
import pytest
from src.reports import spending_by_category


@pytest.fixture
def sample_df():
    return pd.DataFrame([
        {
            "Дата операции": "01.10.2021 12:00:00",
            "Категория": "Супермаркеты",
            "Статус": "OK",
            "Сумма платежа": -500.0
        },
        {
            "Дата операции": "15.11.2021 12:00:00",
            "Категория": "Супермаркеты",
            "Статус": "OK",
            "Сумма платежа": -300.0
        },
        {
            "Дата операции": "01.06.2021 12:00:00",
            "Категория": "Супермаркеты",
            "Статус": "OK",
            "Сумма платежа": -100.0
        },
        {
            "Дата операции": "15.11.2021 12:00:00",
            "Категория": "Кафе",
            "Статус": "OK",
            "Сумма платежа": -200.0
        },
    ])


def test_spending_by_category(sample_df):
    result = spending_by_category(sample_df, "Супермаркеты", "31.12.2021")
    assert len(result) == 2
    assert all(result["Категория"] == "Супермаркеты")


def test_spending_by_category_no_results(sample_df):
    result = spending_by_category(sample_df, "Аптеки", "31.12.2021")
    assert len(result) == 0


def test_spending_by_category_default_date(sample_df):
    result = spending_by_category(sample_df, "Супермаркеты")
    assert isinstance(result, pd.DataFrame)
