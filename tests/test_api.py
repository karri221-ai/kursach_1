import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
alpha_key = os.getenv("ALPHA_VANTAGE_KEY")

# Тест валюты
url = "https://api.apilayer.com/exchangerates_data/convert"
params = {"from": "USD", "to": "RUB", "amount": 1}
headers = {"apikey": api_key}
r = requests.get(url, headers=headers, params=params)
print("Валюта:", r.status_code, r.json().get("result"))

# Тест акции Alpha Vantage
url2 = "https://www.alphavantage.co/query"
params2 = {"function": "GLOBAL_QUOTE", "symbol": "AAPL", "apikey": alpha_key}
r2 = requests.get(url2, params=params2)
print("Акции:", r2.status_code, r2.json())
