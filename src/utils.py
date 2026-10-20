import pandas as pd


def get_transactions(file_path: str) -> pd.DataFrame:
    """Читает Excel-файл с транзакциями и возвращает DataFrame."""
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception:
        return pd.DataFrame()
