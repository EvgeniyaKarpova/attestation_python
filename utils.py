import re


def validate_amount(amount_str: str) -> float:

    if not isinstance(amount_str, str):
        raise ValueError("Сумма должна быть строкой")

    amount_str = amount_str.strip()
    if not amount_str:
        raise ValueError("Сумма не может быть пустой")

    amount_str = amount_str.replace(',', '.')

    if not re.fullmatch(r"^\d+(\.\d+)?$", amount_str):
        raise ValueError("Неверный формат суммы. Используйте цифры и, при необходимости, точку или запятую.")

    amount = float(amount_str)
    if amount <= 0:
        raise ValueError("Сумма должна быть больше нуля")
    return amount


def validate_date(date_str: str) -> str:

    if not isinstance(date_str, str):
        raise ValueError("Дата должна быть строкой")

    date_str = date_str.strip()
    if not date_str:
        raise ValueError("Дата не может быть пустой")

    if not re.fullmatch(r"^\d{2}-\d{2}-\d{4}$", date_str):
        raise ValueError("Дата должна быть в формате ДД-ММ-ГГГГ (например, 23-12-2025)")

    from datetime import datetime
    try:
        datetime.strptime(date_str, "%d-%m-%Y")
    except ValueError:
        raise ValueError("Дата некорректна (например, 31 февраля)")

    return date_str


def validate_category(category_str: str) -> str:

    if not isinstance(category_str, str):
        raise ValueError("Категория должна быть строкой")

    # category_str = category_str.strip()
    # if not category_str:
    #     raise ValueError("Категория не может быть пустой")

    # Опционально: запретить спецсимволы (оставить только буквы, цифры, пробелы, дефисы)
    if re.search(r"[^а-яА-Яa-zA-Z0-9\s\-]", category_str):
        raise ValueError("Категория может содержать только буквы, цифры, пробелы и дефисы")

    return category_str