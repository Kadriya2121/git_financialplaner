from datetime import date
import re

class Category:
    """Категория расходов/доходов."""
    
    def __init__(self, name: str, category_type: str = "expense"):
        if not self._is_valid_name(name):
            raise ValueError("Название категории должно содержать буквы/цифры")
        self.name = name.strip()
        self.category_type = category_type  # "expense" или "income"

    def _is_valid_name(self, name: str) -> bool:
        """Проверка имени через регулярное выражение."""
        return bool(re.match(r"^[\w\s]+$", name))

    def __str__(self):
        return self.name



class Transaction:
    """Финансовая операция."""

    def __init__(self, amount: float, category: Category, date: date, comment: str = ""):
        self._validate_amount(amount)
        self.amount = float(amount)
        self.category = category
        self.date = date
        self.comment = comment.strip()

    def _validate_amount(self, amount):
        """Валидация суммы."""
        if not isinstance(amount, (int, float)):
            raise TypeError("Сумма должна быть числом")
        if amount == 0:
            raise ValueError("Сумма не может быть нулевой")

    def to_dict(self) -> dict:
        """Преобразование в словарь для сохранения."""
        return {
            "amount": self.amount,
            "category": self.category.name,
            "category_type": self.category.category_type,
            "date": self.date.isoformat(),
            "comment": self.comment
        }