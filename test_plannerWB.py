import unittest
from attestation.models import Transaction, calculate_balance

class TestTransaction(unittest.TestCase):

    def test_valid_transaction(self):
        transaction = Transaction(100.0, "Одежда", "25-12-2025")
        self.assertEqual(transaction.amount, 100.0)

    def test_invalid_transaction_type(self):
        with self.assertRaises(ValueError):
            Transaction(100.0, "Обувь", "25-12-2025", transaction_type="invalid")

    def test_invalid_amount(self):
        with self.assertRaises(ValueError):
            Transaction(-100.0, "Игрушки", "25-12-2025")

    def test_invalid_date_format(self):
        with self.assertRaises(ValueError):
            Transaction(100.0, "Прочее", "2025-12-25")

class TestCalculateBalance(unittest.TestCase):

    def test_calculate_balance(self):
        transactions = [
            Transaction(100.0, "", "25-12-2025", transaction_type="income"),
            Transaction(50.0, "Одежда", "26-12-2025", transaction_type="expense")
        ]
        balance = calculate_balance(transactions)
        self.assertEqual(balance, 50.0)


if __name__ == '__main__':
    unittest.main()