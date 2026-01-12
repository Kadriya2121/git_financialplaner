from datetime import datetime
from typing import Optional
import re

class Category:
    def __init__(self, name: str):
        if not self._is_valid_name(name):
            raise ValueError("Некорректное название категории")
        self.name = name.strip()

    @staticmethod
    def _is_valid_name(name: str) -> bool:
        return bool(re.match(r'^[a-zA-Za-яА-Я\s]+$', name))

    def __str__(self):
        return self.name



class Transaction:
    def __init__(
        self,
        amount: float,
        category: Category,
        date: Optional[datetime] = None,
        comment: str = ""
    ):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        self.amount = amount
        self.category = category
        self.date = date or datetime.now()
        self.comment = comment.strip()

    def __repr__(self):
        return (f"Transaction(amount={self.amount}, category={self.category}, "
            f"date={self.date.strftime('%Y-%m-%d')}, comment='{self.comment}')")