
import csv
import os
from models import Transaction, Category
from datetime import datetime

# Путь к файлу данных
DATA_FILE = "data/finances.csv"



def load_transactions() -> list:
    """
    Загружает транзакции из CSV-файла.
    
    Returns:
        Список объектов Transaction.
    """
    transactions = []
    
    if not os.path.exists(DATA_FILE):
        print(f"[INFO] Файл {DATA_FILE} не найден. Будет создан при сохранении.")
        return transactions

    try:
        with open(DATA_FILE, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            
            # Проверяем, есть ли заголовки
            if reader.fieldnames is None:
                print(f"[WARNING] Файл {DATA_FILE} пуст или не содержит заголовков.")
                return transactions
            
            for row in reader:
                try:
                    # Преобразуем поля
                    amount = float(row["amount"])
                    category_name = row["category"]
                    category_type = row["type"]  # в CSV поле называется "type"
                    date = datetime.strptime(row["date"], "%Y-%m-%d").date()
                    comment = row.get("comment", "")  # если нет — пустая строка

                    # Создаём объекты
                    category = Category(category_name, category_type)
                    transaction = Transaction(amount, category, date, comment)
                    transactions.append(transaction)

                except (ValueError, KeyError) as e:
                    print(f"[WARNING] Пропущена строка: {row} | Ошибка: {e}")
                except Exception as e:
                    print(f"[ERROR] Неожиданная ошибка при обработке строки: {row} | {e}")

    except FileNotFoundError:
        print(f"[ERROR] Файл {DATA_FILE} не найден.")
    except PermissionError:
        print(f"[ERROR] Нет прав на чтение файла {DATA_FILE}.")
    except Exception as e:
        print(f"[ERROR] Неизвестная ошибка при чтении файла: {e}")

    return transactions



def save_transactions(transactions: list):
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8", newline="") as f:
            fieldnames = ["amount", "category", "type", "date", "comment"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for t in transactions:  # ← проходим по ВСЕМ транзакциям
                writer.writerow({
                    "amount": t.amount,
                    "category": t.category.name,
                    "type": t.category.category_type,
                    "date": t.date.strftime("%Y-%m-%d"),
                    "comment": t.comment or ""
                })
        print(f"[INFO] Сохранено {len(transactions)} записей в {DATA_FILE}")
    except Exception as e:
        print(f"[ERROR] Не удалось сохранить: {e}")

    except PermissionError:
        print(f"[ERROR] Нет прав на запись в файл {DATA_FILE}.")
    except OSError as e:
        print(f"[ERROR] Ошибка файловой системы: {e}")
    except Exception as e:
        print(f"[ERROR] Неизвестная ошибка при сохранении: {e}")