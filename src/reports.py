from datetime import datetime
from typing import Optional
import pandas as pd


def spending_by_category(
    transactions: pd.DataFrame,
    category: str,
    date: Optional[str] = None
) -> pd.DataFrame:
    """Возвращает траты по заданной категории за последние 3 месяца."""
    if date is None:
        end_date = datetime.now()
    else:
        end_date = pd.to_datetime(date, dayfirst=True)

    start_date = end_date - pd.DateOffset(months=3)

    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"], dayfirst=True
    )

    filtered = transactions[
        (transactions["Категория"] == category) &
        (transactions["Дата операции"] >= start_date) &
        (transactions["Дата операции"] <= end_date) &
        (transactions["Статус"] == "OK")
    ]

    return filtered
