import re
from datetime import datetime

def is_valid_date(date_str: str) -> bool:
    """Проверка формата и корректности даты (ГГГГ-ММ-ДД)."""
    # Проверка формата через регулярное выражение
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(pattern, date_str):
        return False

    # Проверка, что дата существует (например, не 30.02)
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
def format_currency(amount):
    """Форматирует сумму в денежный формат (рубли)."""
    return f"{amount:,.2f} ₽"