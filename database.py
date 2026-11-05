
import sqlite3
import pandas as pd

DB_NAME = "spendwise.db"


def create_table():
    connection = sqlite3.connect(DB_NAME)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_transaction(transaction_type, description, amount, category, date):
    connection = sqlite3.connect(DB_NAME)

    connection.execute("""
        INSERT INTO transactions
        (type, description, amount, category, date)
        VALUES (?, ?, ?, ?, ?)
    """, (transaction_type, description, amount, category, date))

    connection.commit()
    connection.close()


def get_transactions():
    connection = sqlite3.connect(DB_NAME)

    data = pd.read_sql_query(
        "SELECT * FROM transactions ORDER BY date DESC",
        connection
    )

    connection.close()
    return data

def create_budget_table():
    connection = sqlite3.connect(DB_NAME)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT NOT NULL UNIQUE,
            amount REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_budget(month, amount):
    connection = sqlite3.connect(DB_NAME)

    connection.execute("""
        INSERT INTO budgets (month, amount)
        VALUES (?, ?)
        ON CONFLICT(month)
        DO UPDATE SET amount = excluded.amount
    """, (month, amount))

    connection.commit()
    connection.close()


def get_budget(month):
    connection = sqlite3.connect(DB_NAME)

    result = connection.execute(
        "SELECT amount FROM budgets WHERE month = ?",
        (month,)
    ).fetchone()

    connection.close()

    return result[0] if result else 0
