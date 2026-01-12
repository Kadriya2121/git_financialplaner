import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def get_category_summary(transactions: list) -> pd.DataFrame:
    """Сумма по категориям."""
    df = pd.DataFrame([t.to_dict() for t in transactions])
    summary = df.groupby("category")["amount"].sum().reset_index()
    return summary

def plot_income_expense(transactions: list):
    """График доходов/расходов по времени."""
    df = pd.DataFrame([t.to_dict() for t in transactions])
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    
    income = df[df["category_type"] == "income"].resample("M").sum()
    expense = df[df["category_type"] == "expense"].resample("M").sum()

    plt.figure(figsize=(10, 6))
    plt.plot(income.index, income["amount"], label="Доходы", marker="o")
    plt.plot(expense.index, expense["amount"], label="Расходы", marker="s")
    plt.title("Доходы и расходы по месяцам")
    plt.xlabel("Месяц")
    plt.ylabel("Сумма (руб.)")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_category_pie(transactions: list):
    """Круговая диаграмма расходов по категориям."""
    df = pd.DataFrame([t.to_dict() for t in transactions])
    expenses = df[df["category_type"] == "expense"]
    category_sum = expenses.groupby("category")["amount"].sum()

    plt.figure(figsize=(8, 8))
    plt.pie(category_sum, labels=category_sum.index, autopct="%1.1f%%")
    plt.title("Распределение расходов по категориям")
    plt.show()