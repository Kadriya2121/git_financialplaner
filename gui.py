"""
Графический интерфейс финансового планировщика.
Реализует: ввод транзакций, отображение списка, анализ и визуализацию.
"""
import tkinter as tk
from tkinter import messagebox, ttk
from models import Transaction, Category
from storage import load_transactions, save_transactions
from analysis import get_category_summary, plot_income_expense, plot_category_pie
from utils import is_valid_date, format_currency
from datetime import datetime, date
import pandas as pd
from visualization import plot_income_expense, plot_category_pie, plot_top_expenses



class FinanceApp:
    """
    Основной класс графического интерфейса.

    Attributes:
        root (tk.Tk): Главное окно приложения
        transactions (list): Список транзакций (объектов Transaction)
        tree (ttk.Treeview): Виджет таблицы для отображения транзакций
        balance_label (tk.Label): Метка для отображения баланса
    """

    def __init__(self, root):

        self.root = root
        self.root.title("Финансовый планировщик")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        # Загрузка данных
        try:
            self.transactions = load_transactions()
            print(f"[INFO] Загружено {len(self.transactions)} операций")
        except Exception as e:
            messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить транзакции: {e}")
            self.transactions = []

        # Создание интерфейса
        self.create_widgets()
        # Обновление таблицы и баланса
        self.refresh_transactions_list()
        self.update_balance()

    def create_widgets(self):
        """Создаёт все элементы интерфейса."""
        # Заголовок
        header = tk.Label(
            self.root,
            text="Финансовый планировщик",
            font=("Arial", 18, "bold"),
            bg="#4CAF50",
            fg="white",
            pady=15
        )
        header.grid(row=0, column=0, columnspan=6, sticky="ew", padx=10, pady=(10, 15))

        # Форма ввода
        tk.Label(self.root, text="Сумма (руб.):", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.amount_entry = tk.Entry(self.root, width=15, font=("Arial", 10))
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Категория:", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.category_entry = tk.Entry(self.root, width=15, font=("Arial", 10))
        self.category_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Дата (ГГГГ-ММ-ДД):", bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.date_entry = tk.Entry(self.root, width=15, font=("Arial", 10))
        self.date_entry.grid(row=3, column=1, padx=5, pady=5)


        tk.Label(self.root, text="Комментарий:", bg="#f0f0f0").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.comment_entry = tk.Entry(self.root, width=40, font=("Arial", 10))
        self.comment_entry.grid(row=4, column=1, columnspan=4, padx=5, pady=5, sticky="ew")

        # Кнопка добавления
        add_btn = tk.Button(
            self.root,
            text="Добавить операцию",
            command=self.add_transaction,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15
        )
        add_btn.grid(row=5, column=0, columnspan=2, pady=15, padx=10)

        # Кнопка анализа
        analysis_btn = tk.Button(
            self.root,
            text="Анализ данных",
            command=self.show_analysis,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15
        )
        analysis_btn.grid(row=5, column=2, columnspan=2, pady=15, padx=10)

        charts_btn = tk.Button(
            self.root,
            text="Графики анализа",
            command=self.show_charts,
            bg="#9C27B0",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15
        )
        charts_btn.grid(row=5, column=4, columnspan=2, pady=15, padx=10)

        # Таблица транзакций
        columns = ("Сумма", "Категория", "Тип", "Дата", "Комментарий")
        self.tree = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings",
            height=15
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        self.tree.grid(row=6, column=0, columnspan=6, padx=15, pady=10, sticky="nsew")

        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=6, column=6, sticky="ns", padx=(0, 10), pady=10)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Баланс
        self.balance_label = tk.Label(
            self.root,
            text="Баланс: 0 руб.",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            fg="#1976D2"
        )
        self.balance_label.grid(row=7, column=0, columnspan=6, pady=15)

        # Адаптивность
        self.root.grid_rowconfigure(6, weight=1)
        for i in range(6):
            self.root.grid_columnconfigure(i, weight=1)

    def add_transaction(self):
        """Добавляет новую транзакцию после валидации."""
        try:
            # 1. Получение и валидация данных
            amount_str = self.amount_entry.get().strip()
            if not amount_str:
                raise ValueError("Сумма не может быть пустой")
            amount = float(amount_str)
            if amount == 0:
                raise ValueError("Сумма должна быть отличной от нуля")

            category_name = self.category_entry.get().strip()
            if not category_name:
                raise ValueError("Категория не может быть пустой")

            date_str = self.date_entry.get().strip()
            if not is_valid_date(date_str):
                raise ValueError("Неверный формат даты. Используйте ГГГГ-ММ-ДД")
            transaction_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            comment = self.comment_entry.get().strip()

            # 2. Определение типа операции
            transaction_type = "income" if amount > 0 else "expense"

            # 3. Создание объектов
            category = Category(category_name, transaction_type)
            transaction = Transaction(amount, category, transaction_date, comment)

            # 4. Добавление в список
            self.transactions.append(transaction)

            # 5. Сохранение в файл
            save_transactions(self.transactions)

            # 6. Обновление интерфейса
            self.refresh_transactions_list()
            self.update_balance()

            # 7. Очистка полей ввода
            self.amount_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.comment_entry.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка: {e}")

    def show_analysis(self):
        """Отображает анализ транзакций."""
        if not self.transactions:
            messagebox.showinfo("Анализ", "Нет данных для анализа.")
            return

        income = sum(t.amount for t in self.transactions if t.amount > 0)
        expense = sum(abs(t.amount) for t in self.transactions if t.amount < 0)
        balance = income - expense

        report = (
            f"📊 АНАЛИЗ ФИНАНСОВ\n\n"
            f"Доходы: {income:,.2f} руб.\n"
            f"Расходы: {expense:,.2f} руб.\n"
            f"Баланс: {balance:,.2f} руб."
        )
        messagebox.showinfo("Анализ данных", report)

    def refresh_transactions_list(self):
        """Обновляет таблицу транзакций, отображая актуальные данные."""
        # Очищаем все строки таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполняем таблицу данными
        for transaction in self.transactions:
            amount_str = f"{transaction.amount:,.2f}"
            category_name = transaction.category.name
            transaction_type = transaction.category.category_type
            date_str = transaction.date.strftime("%Y-%m-%d")
            comment = transaction.comment or ""

            # Добавляем строку в таблицу
            self.tree.insert("", "end", values=(
                amount_str,
                category_name,
                transaction_type,
                date_str,
                comment
            ))

    def update_balance(self):
        """Обновляет отображение баланса в интерфейсе."""
        if not self.transactions:
            balance = 0.0
        else:
            income = sum(t.amount for t in self.transactions if t.amount > 0)
            expense = sum(abs(t.amount) for t in self.transactions if t.amount < 0)
            balance = income - expense

        balance_str = f"{balance:,.2f}"
        self.balance_label.config(text=f"Баланс: {balance_str} руб.")

    def show_charts(self):
        """Отображает меню выбора графиков."""
        if not self.transactions:
            messagebox.showinfo("Графики", "Нет данных для построения графиков.")
            return

        # Окно выбора
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Выбор графика")
        chart_window.geometry("400x300")
        chart_window.configure(bg="#f0f0f0")

        tk.Label(chart_window, text="Выберите график:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)

        options = [
            ("Доходы и расходы по времени", self.plot_income_expense),
            ("Круговая диаграмма расходов", self.plot_category_pie),
            ("Топ-5 расходов по категориям", self.plot_top_expenses),
        ]

        for text, cmd in options:
            btn = tk.Button(
                chart_window,
                text=text,
                command=cmd,
                bg="#4CAF50",
                fg="white",
                font=("Arial", 10),
                width=30
            )
            btn.pack(pady=5)

        # Кнопка сохранения
        save_btn = tk.Button(
            chart_window,
            text="Сохранить все графики в файлы",
            command=self.save_all_charts,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10),
            width=30
        )
        save_btn.pack(pady=10)

    def plot_income_expense(self):
        plot_income_expense(self.transactions)

    def plot_category_pie(self):
        plot_category_pie(self.transactions)

    def plot_top_expenses(self):
        plot_top_expenses(self.transactions, top_n=5)

    def save_all_charts(self):
        """Сохраняет все графики в файлы."""
        try:
            plot_income_expense(self.transactions, "income_expense.png")
            plot_category_pie(self.transactions, "category_pie.png")
            plot_top_expenses(self.transactions, "top_expenses.png", top_n=5)
            messagebox.showinfo("Сохранение", "Все графики успешно сохранены!")
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить графики: {e}")