import pandas as pd
from src.utils import get_transactions


def test_get_transactions_success():
    result = get_transactions("data/operations.xlsx")
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0


def test_get_transactions_file_not_found():
    result = get_transactions("nonexistent.xlsx")
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0
