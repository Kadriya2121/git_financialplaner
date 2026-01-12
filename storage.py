import pandas as pd
from models import Transaction, Category
from typing import List
import os

CSV_PATH = "data/finances.csv"

def save_transactions(transactions: List[Transaction]):
    data = []
    for t in transactions:
        data.append({
            "amount": t.amount,
            "category": t.category.name,
            "date": t.date.strftime("%Y-%m-%d"),
            "comment": t.comment
        })
    df = pd.DataFrame(data)
    df.to_csv(CSV_PATH, index=False, encoding="utf-8")
    print(f"[INFO] Данные сохранены в {CSV_PATH}")

def load_transactions() -> List[Transaction]:
    if not os.path.exists(CSV_PATH):
        return []
    try:
        df = pd.read_csv(CSV_PATH, encoding="utf-8")
        transactions = []
        for _, row in df.iterrows():
            category = Category(row["category"])
            date = datetime.strptime(row["date"], "%Y-%m-%d")
            t = Transaction(
                amount=row["amount"],
                category=category,
                date=date,
                comment=row["comment"]
            )
            transactions.append(t)
        print(f"[INFO] Загружено {len(transactions)} операций")
        return transactions
    except Exception as e:
        print(f"[ERROR] Ошибка при загрузке данных: {e}")
        return []