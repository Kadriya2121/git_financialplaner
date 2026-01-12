import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import date
from models import Transaction

# Настройка стиля
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'  # Для кириллицы



def plot_income_expense(transactions, save_path=None):
    """
    График доходов и расходов по времени (линейный график).
    
    Параметры:
        transactions: список объектов Transaction
        save_path: путь для сохранения файла (если None — показывает график)
    """
    if not transactions:
        print("Нет транзакций для отображения.")
        return

    # Подготовка данных
    data = []
    for t in transactions:
        data.append({
            'date': t.date,
            'income': t.amount if t.amount > 0 else 0,
            'expense': abs(t.amount) if t.amount < 0 else 0
        })
    df = pd.DataFrame(data)
    df = df.groupby('date').sum().reset_index()

    # Построение
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['income'], label='Доходы', marker='o', color='green')
    plt.plot(df['date'], df['expense'], label='Расходы', marker='s', color='red')


    plt.title("Доходы и расходы по времени", fontsize=16, fontweight='bold')
    plt.xlabel("Дата", fontsize=12)
    plt.ylabel("Сумма (руб.)", fontsize=12)
    plt.legend(fontsize=11)
    plt.xticks(rotation=45)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"График сохранён: {save_path}")
    else:
        plt.show()
    plt.close()



def plot_category_pie(transactions, save_path=None):
    """
    Круговая диаграмма расходов по категориям.
    """
    expenses = [t for t in transactions if t.amount < 0]
    if not expenses:
        print("Нет расходов для отображения.")
        return

    # Группировка по категориям
    data = {}
    for t in expenses:
        cat_name = t.category.name
        data[cat_name] = data.get(cat_name, 0) + abs(t.amount)

    labels = list(data.keys())
    sizes = list(data.values())

    plt.figure(figsize=(8, 8))
    wedges, texts, autotexts = plt.pie(
        sizes, labels=labels, autopct='%1.1f%%',
        startangle=90, textprops={'fontsize': 11}
    )
    plt.setp(autotexts, size=10, weight="bold")
    plt.title("Распределение расходов по категориям", fontsize=16, fontweight='bold')


    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"График сохранён: {save_path}")
    else:
        plt.show()
    plt.close()



def plot_top_expenses(transactions, top_n=5, save_path=None):
    """
    Столбчатая диаграмма топ-N самых больших расходов.
    Параметры:
        top_n: количество категорий для отображения
    """
    expenses = [t for t in transactions if t.amount < 0]
    if not expenses:
        print("Нет расходов для отображения.")
        return

    # Топ-N по сумме
    data = {}
    for t in expenses:
        cat_name = t.category.name
        data[cat_name] = data.get(cat_name, 0) + abs(t.amount)


    df = pd.DataFrame(list(data.items()), columns=['Категория', 'Сумма'])
    df = df.sort_values('Сумма', ascending=False).head(top_n)


    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='Сумма', y='Категория', palette='viridis')
    plt.title(f"Топ-{top_n} самых больших расходов", fontsize=16, fontweight='bold')
    plt.xlabel("Сумма (руб.)", fontsize=12)
    plt.ylabel("Категория", fontsize=12)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"График сохранён: {save_path}")
    else:
        plt.show()
    plt.close()