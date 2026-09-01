from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)

DB_NAME = "expenses.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/")
def index():
    conn = get_db_connection()

    category_filter = request.args.get("category")

    if category_filter and category_filter != "All":
        expenses = conn.execute(
            "SELECT * FROM expenses WHERE category = ? ORDER BY date DESC",
            (category_filter,)
        ).fetchall()
    else:
        expenses = conn.execute(
            "SELECT * FROM expenses ORDER BY date DESC"
        ).fetchall()

    total_row = conn.execute(
        "SELECT SUM(amount) AS total FROM expenses"
    ).fetchone()

    total = total_row["total"] if total_row["total"] is not None else 0

    categories = conn.execute(
        "SELECT DISTINCT category FROM expenses ORDER BY category"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        categories=categories,
        selected_category=category_filter or "All",
        today=date.today().isoformat()
    )


@app.route("/add", methods=["POST"])
def add():
    description = request.form.get("description")
    amount = request.form.get("amount")
    category = request.form.get("category")
    expense_date = request.form.get("date")

    if not description or not amount or not category or not expense_date:
        return redirect(url_for("index"))

    try:
        amount = float(amount)
    except ValueError:
        return redirect(url_for("index"))

    conn = get_db_connection()

    conn.execute(
        """
        INSERT INTO expenses
        (description, amount, category, date)
        VALUES (?, ?, ?, ?)
        """,
        (description, amount, category, expense_date)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):
    conn = get_db_connection()

    conn.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
