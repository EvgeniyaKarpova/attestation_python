#models.py

import datetime

class Transaction:
    def __init__(
            self,
            amount: float,
            category: str,
            date: str,
            comment: str = '',
            transaction_type: str = 'expense'
            ):

        if transaction_type not in ('expense', 'income'):
            raise ValueError('Тип транзакции - только expense/income')
        if amount <= 0:
            raise ValueError("Сумма транзакции должна быть положительной")
        self.amount = amount
        self.category = category
        self.date = self._validate_date(date)
        self.comment = comment.strip()
        self.transaction_type = transaction_type

    @staticmethod
    def _validate_date(date_str: str) -> str:
        try:
            datetime.datetime.strptime(date_str, '%d-%m-%Y')
            return date_str
        except ValueError:
            raise ValueError('Дата записывается в формате DD-MM-YYYY')

    def to_dict(self):
        return {
            'amount': self.amount,
            'category': self.category,
            'date': self.date,
            'comment': self.comment,
            'transaction_type': self.transaction_type
        }

def calculate_balance(transactions: list[Transaction]) -> float:
    balance = 0.0
    for transaction in transactions:
        if transaction.transaction_type == 'income':
            balance += transaction.amount
        elif transaction.transaction_type == 'expense':
            balance -= transaction.amount
    return balance
