import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

app = Flask(__name__)

app.jinja_env.filters["usd"] = usd

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    rows = db.execute(
        """
        SELECT symbol, SUM(shares) AS shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING SUM(shares) > 0
        """,
        session["user_id"],
    )

    holdings = []
    total = 0

    for row in rows:
        stock = lookup(row["symbol"])
        price = stock["price"]
        value = row["shares"] * price
        total += value

        holdings.append(
            {
                "symbol": row["symbol"],
                "shares": row["shares"],
                "price": price,
                "value": value,
            }
        )

    cash = db.execute(
        "SELECT cash FROM users WHERE id = ?", session["user_id"]
    )[0]["cash"]

    total += cash

    return render_template(
        "index.html",
        holdings=holdings,
        cash=cash,
        total=total,
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide symbol")

        stock = lookup(symbol)

        if stock is None:
            return apology("invalid symbol")

        shares = request.form.get("shares")

        if not shares:
            return apology("must provide shares")

        try:
            shares = int(shares)
        except ValueError:
            return apology("shares must be a positive integer")

        if shares <= 0:
            return apology("shares must be a positive integer")

        price = stock["price"]
        cost = shares * price

        user = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"]
        )[0]

        if cost > user["cash"]:
            return apology("can't afford")

        db.execute(
            "UPDATE users SET cash = cash - ? WHERE id = ?",
            cost,
            session["user_id"],
        )

        db.execute(
            """
            INSERT INTO transactions (user_id, symbol, shares, price)
            VALUES (?, ?, ?, ?)
            """,
            session["user_id"],
            stock["symbol"],
            shares,
            price,
        )

        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute(
        """
        SELECT symbol, shares, price, transacted
        FROM transactions
        WHERE user_id = ?
        ORDER BY transacted DESC
        """,
        session["user_id"],
    )

    return render_template("history.html", transactions=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            request.form.get("username"),
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    session.clear()

    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide symbol")

        stock = lookup(symbol)

        if stock is None:
            return apology("invalid symbol")

        return render_template("quoted.html", stock=stock)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username")

        if not password:
            return apology("must provide password")

        if not confirmation:
            return apology("must confirm password")

        if password != confirmation:
            return apology("passwords do not match")

        try:
            user_id = db.execute(
                """
                INSERT INTO users (username, hash)
                VALUES (?, ?)
                """,
                username,
                generate_password_hash(password),
            )
        except ValueError:
            return apology("username already exists")

        session["user_id"] = user_id

        return redirect("/")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must select a stock")

        try:
            shares = int(request.form.get("shares"))
        except (ValueError, TypeError):
            return apology("shares must be a positive integer")

        if shares <= 0:
            return apology("shares must be a positive integer")

        owned = db.execute(
            """
            SELECT COALESCE(SUM(shares), 0) AS shares
            FROM transactions
            WHERE user_id = ? AND symbol = ?
            """,
            session["user_id"],
            symbol,
        )[0]["shares"]

        if owned < shares:
            return apology("not enough shares")

        stock = lookup(symbol)

        if stock is None:
            return apology("invalid symbol")

        price = stock["price"]
        proceeds = shares * price

        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?",
            proceeds,
            session["user_id"],
        )

        db.execute(
            """
            INSERT INTO transactions (user_id, symbol, shares, price)
            VALUES (?, ?, ?, ?)
            """,
            session["user_id"],
            symbol,
            -shares,
            price,
        )

        return redirect("/")

    stocks = db.execute(
        """
        SELECT symbol
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING SUM(shares) > 0
        """,
        session["user_id"],
    )

    return render_template("sell.html", stocks=stocks)

@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add cash to account."""
    if request.method == "POST":
        try:
            amount = float(request.form.get("amount"))
        except (ValueError, TypeError):
            return apology("invalid amount")

        if amount <= 0:
            return apology("amount must be positive")

        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?",
            amount,
            session["user_id"],
        )

        flash("Cash added successfully!")
        return redirect("/")

    return render_template("add_cash.html")
