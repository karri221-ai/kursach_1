import json
import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


def get_greeting(date_str: str) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    hour = int(date_str[11:13])
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_cards_info(df: pd.DataFrame) -> list:
    """Возвращает информацию по каждой карте."""
    result = []
    expenses = df[(df["Статус"] == "OK") & (df["Сумма платежа"] < 0)]
    for card, group in expenses.groupby("Номер карты"):
        total_spent = round(abs(group["Сумма платежа"].sum()), 2)
        result.append({
            "last_digits": str(card)[-4:],
            "total_spent": total_spent,
            "cashback": round(total_spent / 100, 2)
        })
    return result


def get_top_transactions(df: pd.DataFrame) -> list:
    """Возвращает топ-5 транзакций по сумме платежа."""
    top = df.nlargest(5, "Сумма платежа")
    result = []
    for _, row in top.iterrows():
        date = pd.to_datetime(row["Дата платежа"], dayfirst=True)
        result.append({
            "date": date.strftime("%d.%m.%Y"),
            "amount": round(row["Сумма платежа"], 2),
            "category": row["Категория"],
            "description": row["Описание"]
        })
    return result


def get_currency_rates(currencies: list) -> list:
    """Возвращает курсы валют к рублю."""
    api_key = os.getenv("API_KEY")
    result = []
    for currency in currencies:
        try:
            url = "https://api.apilayer.com/exchangerates_data/convert"
            params = {"from": currency, "to": "RUB", "amount": 1}
            headers = {"apikey": api_key}
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            result.append({
                "currency": currency,
                "rate": round(float(data["result"]), 2)
            })
        except Exception:
            result.append({"currency": currency, "rate": 0.0})
    return result


def get_stock_prices(stocks: list) -> list:
    """Возвращает цены акций."""
    alpha_key = os.getenv("ALPHA_VANTAGE_KEY")
    result = []
    for stock in stocks:
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": stock,
                "apikey": alpha_key
            }
            response = requests.get(url, params=params)
            data = response.json()
            price = float(data["Global Quote"]["05. price"])
            result.append({"stock": stock, "price": round(price, 2)})
        except Exception:
            result.append({"stock": stock, "price": 0.0})
    return result


def get_main_page(date_str: str, df: pd.DataFrame) -> str:
    """Возвращает JSON для главной страницы."""
    with open("user_settings.json", encoding="utf-8") as f:
        settings = json.load(f)

    date = pd.to_datetime(date_str)
    start = date.replace(day=1)
    mask = (pd.to_datetime(df["Дата операции"], dayfirst=True) >= start) & \
           (pd.to_datetime(df["Дата операции"], dayfirst=True) <= date)
    filtered_df = df[mask]

    result = {
        "greeting": get_greeting(date_str),
        "cards": get_cards_info(filtered_df),
        "top_transactions": get_top_transactions(filtered_df),
        "currency_rates": get_currency_rates(settings["user_currencies"]),
        "stock_prices": get_stock_prices(settings["user_stocks"])
    }
    return json.dumps(result, ensure_ascii=False, indent=2)
