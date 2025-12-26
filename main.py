from models import Transaction
from storage import save_transactions, load_transactions

def main():
    print("Загрузка операций: ")
    transactions = load_transactions()
    print(f"Загружено {len(transactions)} транзакций")

    if len(transactions) == 0:
        print("Добавляем тестовые транзакции")
        t1 = Transaction(200, "кофе", "23-12-2025", "Утренний кофе")
        t2 = Transaction(50000, "зарплата", "01-12-2025", "Аванс", 'income')
        save_transactions([t1, t2])
        print("ОК")
        transactions = [t1, t2]
    else:
        print("Операции уже есть")

    for t in transactions:
        print(t.to_dict())

if __name__ == "__main__":
    main()