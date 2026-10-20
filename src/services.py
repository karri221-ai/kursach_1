import json
import re


def search_by_phone(transactions: list) -> str:
    """Возвращает JSON со всеми транзакциями, содержащими номера в описании."""
    pattern = r'(?:\+7|8)[\s-]?\d{3}[\s-]?\d{2,3}[\s-]?\d{2}[\s-]?\d{2}'
    result = [
        t for t in transactions
        if re.search(pattern, str(t.get("Описание", "")))
    ]
    return json.dumps(result, ensure_ascii=False, indent=2)
