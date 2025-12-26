import pandas as pd
import matplotlib.pyplot as plt
from storage import load_transactions

# Расходы по категориям
def analyze_category():
    transactions = load_transactions()
    df = pd.DataFrame([t.__dict__ for t in transactions])

    df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0) #или .astype(float)

    category_expenses = df[df['transaction_type'] == 'expense'].groupby('category')['amount'].sum()
    plt.figure(figsize=(8,6))
    category_expenses.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Расходы по категориям')
    plt.ylabel('')
    plt.show()

# График покупок
def time_chart(transactions):
    transactions = load_transactions()

    df = pd.DataFrame([t.__dict__ for t in transactions])

    df['amount'] = pd.to_numeric(df['amount'])
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')

    time_group = df[df['transaction_type'] == 'expense'].groupby('date')['amount'].sum()
    plt.figure(figsize=(10, 5))
    plt.plot(time_group.index, time_group.values, marker='o')  # Строим график
    plt.title('График покупок')
    plt.xlabel('Дата')
    plt.ylabel('Сумма')
    plt.grid(True)
    plt.show()

# Диаграмма самых дорогих покупок
def shopping_diagram(num_expenses=5):
    transactions = load_transactions()
    df = pd.DataFrame([t.__dict__ for t in transactions])
    df['amount'] = pd.to_numeric(df['amount'])
    expenses_df = df[df['transaction_type'] == 'expense']
    top_expenses = expenses_df.nlargest(num_expenses, 'amount')
    plt.figure(figsize=(10, 6))
    bars = plt.bar(top_expenses['category'], top_expenses['amount'], color='moccasin') #Сохраняем бары в переменную
    for bar in bars:  # Iterate over the bars
        yval = bar.get_height()  # Получаем высоту текущего бара
        plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom')
    plt.xlabel('Категория')
    plt.ylabel('Сумма')
    plt.title(f'Топ {num_expenses} расходов')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(axis='y', alpha=0.5)
    plt.show()
