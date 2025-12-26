import datetime
import tkinter as tk
import analysis
from tkinter import ttk, messagebox
from models import Transaction
from storage import save_transactions, load_transactions
from utils import validate_amount, validate_date, validate_category

class PlannerWBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Планер Wildberries")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        self.root.configure(bg="honeydew")

        # Загружаем существующие операции
        self.transactions = load_transactions()

        # Создаём виджеты
        self.create_widgets()
        self.refresh_transaction_table()
    def create_widgets(self):
        # === Верхняя панель: форма ввода ===
        input_frame = ttk.LabelFrame(self.root, text=" ➕ Новая операция ", padding=(10, 10))
        input_frame.pack(fill="x", padx=10, pady=(10, 5))

        #Баланс
        self.balance_label = ttk.Label(self.root, text="Баланс: 0.00 RUB")
        self.balance_label.pack(pady=5)
        self.refresh_balance()

        # Сумма
        ttk.Label(input_frame, text='Сумма (RUB):').grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.amount_var = tk.StringVar()
        amount_entry = ttk.Entry(input_frame, textvariable=self.amount_var, width=15)
        amount_entry.grid(row=0, column=1, sticky='w')

        # Категории
        category = ['Обувь', 'Одежда', 'Дом', 'Мебель', 'Электроника', 'Игрушки', 'Продукты', 'Спорт', 'Зоотовары', 'Прочее']
        ttk.Label(input_frame, text='Категория:').grid(row=0, column=2, sticky="w", padx=(20, 10))
        self.category_var = tk.StringVar()
        # self.category_var.set(category[0])
        category_combo = ttk.Combobox(input_frame, textvariable=self.category_var, values=category, width=18, state='readonly')
        category_combo.grid(row=0, column=3, sticky="w")

        # Дата
        ttk.Label(input_frame, text="Дата (ДД-ММ-ГГГГ):").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(10, 0))
        today = datetime.date.today()
        formatted_date = today.strftime("%d-%m-%Y")
        self.date_var = tk.StringVar(value=formatted_date)  # подставим сегодняшнюю дату позже
        date_entry = ttk.Entry(input_frame, textvariable=self.date_var, width=15)
        date_entry.grid(row=1, column=1, sticky="w", pady=(10, 0))

        # Комментарий
        ttk.Label(input_frame, text="Комментарий:").grid(row=1, column=2, sticky="w", padx=(20, 10), pady=(10, 0))
        self.comm_var = tk.StringVar()
        comm_entry = ttk.Entry(input_frame, textvariable=self.comm_var, width=30)
        comm_entry.grid(row=1, column=3, sticky="w", pady=(10, 0))

        # Тип операции
        ttk.Label(input_frame, text="Тип:").grid(row=2, column=0, sticky="w", pady=(10, 0))
        self.type_var = tk.StringVar(value="expense")
        expense_rb = ttk.Radiobutton(input_frame, text="Покупка", variable=self.type_var, value="expense")
        income_rb = ttk.Radiobutton(input_frame, text="Пополнение", variable=self.type_var, value="income")
        expense_rb.grid(row=2, column=1, sticky="w", pady=(10, 0))
        income_rb.grid(row=2, column=1, sticky="w", padx=(80, 0), pady=(10, 0))

        # Кнопка "Добавить"
        add_btn = ttk.Button(input_frame, text=" Добавить операцию", command=self.add_transaction)
        add_btn.grid(row=3, column=0, columnspan=4, pady=(15, 0))

        # Кнопка анализа по категориям
        analysis_btn = ttk.Button(input_frame, text="Расходы по категориям", command=analysis.analyze_category)
        analysis_btn.grid(row=4, column=0, columnspan=1, pady=(15, 0))

        # Кнопка график покупок
        chart_btn = ttk.Button(input_frame, text="График покупок", command=analysis.time_chart)
        chart_btn.grid(row=4, column=0, columnspan=3, pady=(15, 0))

        # Кнопка диаграмма самых дорогих покупок
        diagram_btn = ttk.Button(input_frame, text="Топ-5 дорогих покупок", command=analysis.shopping_diagram)
        diagram_btn.grid(row=4, column=1, columnspan=3, pady=(15, 0))


        # === Таблица операций ===
        table_frame = ttk.LabelFrame(self.root, text=" 📜 История операций ", padding=(10, 10))
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Создаём Treeview (таблицу)
        columns = ("type", "amount", "category", "date", "comment")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        # Заголовки
        self.tree.heading("type", text="Тип")
        self.tree.heading("amount", text="Сумма (RUB)")
        self.tree.heading("category", text="Категория")
        self.tree.heading("date", text="Дата")
        self.tree.heading("comment", text="Комментарий")

        # Ширина колонок
        self.tree.column("type", width=80, anchor="center")
        self.tree.column("amount", width=100, anchor="e")
        self.tree.column("category", width=150)
        self.tree.column("date", width=100, anchor="center")
        self.tree.column("comment", width=250)

        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        # Размещение
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def refresh_balance(self):
       """Вычисляет и отображает текущий баланс."""
       balance = self.calculate_balance() # вызываем метод calculate_balance
       self.balance_label.config(text=f"Баланс: {balance:.2f} RUB") #Обновляем метку

    def calculate_balance(self):
        """Вычисляет баланс на основе сохраненных транзакций."""
        balance = 0.0
        for transaction in self.transactions: #Итерируемся по транзакциям
            if transaction.transaction_type == 'income':
                balance += transaction.amount
            elif transaction.transaction_type == 'expense':
                balance -= transaction.amount
        return balance

    def add_transaction(self):
        """Добавляет новую операцию после валидации."""
        try:
            # 1. Получаем и валидируем данные
            amount = validate_amount(self.amount_var.get())
            category = validate_category(self.category_var.get())
            date = validate_date(self.date_var.get())
            comment = self.comm_var.get().strip()
            trans_type = self.type_var.get()

        # 2. Создаём объект
            transaction = Transaction(
            amount=amount,
            category=category,
            date=date,
            comment=comment,
            transaction_type=trans_type
            )

        # 3. Сохраняем
            save_transactions([transaction])
            self.transactions.append(transaction)

        # 4. Обновляем интерфейс
            self.refresh_transaction_table()
            self.clear_input_fields()
            self.refresh_transaction_table()
            self.clear_input_fields()
            self.refresh_balance()

            messagebox.showinfo("Успех", f"Операция добавлена:\n{transaction}")

        except Exception as e:
            messagebox.showerror("Ошибка ввода", f"Не удалось добавить операцию:\n{e}")

    def clear_input_fields(self):
        """Очищает поля ввода."""
        self.amount_var.set("")
        self.category_var.set("")
        self.comm_var.set("")
        # Дату можно оставить или сбросить — оставим как есть

    def refresh_transaction_table(self):
        """Обновляет таблицу операций."""
        # Очищаем текущие строки
        for item in self.tree.get_children():
            self.tree.delete(item)


        # Добавляем все операции
        for t in self.transactions:
            row_type = "Пополнение" if t.transaction_type == "income" else "Покупка"
            self.tree.insert("", "end", values=(
                row_type,
                f"{t.amount:.2f}",
                t.category,
                t.date,
                t.comment
            ))

        # Скролл вниз (к новой операции)
        self.tree.yview_moveto(1.0)
        self.refresh_balance()

# === Точка входа для запуска GUI ===
if __name__ == "__main__":
    root = tk.Tk()
    app = PlannerWBApp(root)
    root.mainloop()