import unittest
from utils import is_valid_date, format_currency



class TestUtils(unittest.TestCase):

    def test_is_valid_date_valid_formats(self):
        """Проверяет корректные даты в правильном формате."""
        self.assertTrue(is_valid_date("2023-01-01"))
        self.assertTrue(is_valid_date("2024-12-31"))
        self.assertTrue(is_valid_date("1900-02-28"))

    def test_is_valid_date_invalid_format(self):
        """Проверяет строки с неверным форматом (не ГГГГ-ММ-ДД)."""
        self.assertFalse(is_valid_date("01-01-2023"))
        self.assertFalse(is_valid_date("2023/01/01"))
        self.assertFalse(is_valid_date("23-01-01"))
        self.assertFalse(is_valid_date("2023-1-01"))
        self.assertFalse(is_valid_date("2023-01-1"))


    def test_is_valid_date_invalid_dates(self):
        """Проверяет несуществующие даты (например, 30 февраля)."""
        self.assertFalse(is_valid_date("2023-02-30"))
        self.assertFalse(is_valid_date("2023-04-31"))
        self.assertFalse(is_valid_date("2023-13-01"))
        self.assertFalse(is_valid_date("2023-00-10"))

        self.assertFalse(is_valid_date("2023-06-31"))


    def test_format_currency_positive(self):
        """Форматирование положительной суммы."""
        self.assertEqual(format_currency(1000.50), "1,000.50 руб.")
        self.assertEqual(format_currency(0.99), "0.99 руб.")
        self.assertEqual(format_currency(1234567.89), "1,234,567.89 руб.")


    def test_format_currency_negative(self):
        """Форматирование отрицательной суммы (в скобках)."""
        self.assertEqual(format_currency(-1000.50), "(1,000.50) руб.")
        self.assertEqual(format_currency(-0.99), "(0.99) руб.")
        self.assertEqual(format_currency(-1234567.89), "(1,234,567.89) руб.")


    def test_format_currency_zero(self):
        """Форматирование нуля."""
        self.assertEqual(format_currency(0), "0.00 руб.")




if __name__ == '__main__':
    unittest.main()