from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

db = SQL("sqlite:///shelfheng.db")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            errorcode = 400
            message = "must provide username"
            return render_template("apology.html", errorcode = errorcode, message = message)

        # Ensure password was submitted
        elif not request.form.get("password"):
            errorcode = 400
            message = "must provide password"
            return render_template("apology.html", errorcode = errorcode, message = message)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            errorcode = 400
            message = "invalid username/ password"
            return render_template("apology.html", errorcode = errorcode, message = message)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Checking the validity of user
        session.clear()
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if not username:
            errorcode = 400
            message = "Must provide username"
            return render_template("apology.html", errorcode = errorcode, message = message)
        elif not password:
            errorcode = 400
            message = "must provide password"
            return render_template("apology.html", errorcode = errorcode, message = message)
        elif not confirmation:
            errorcode = 400
            message = "must confirm your password"
            return render_template("apology.html", errorcode = errorcode, message = message)
        elif confirmation != password:
            errorcode = 400
            message = "confirmation not match"
            return render_template("apology.html", errorcode = errorcode, message = message)
        elif len(rows) != 0:
            errorcode = 400
            message = "username exist, try to login"
            return render_template("apology.html", errorcode = errorcode, message = message)
        else:
            # add new user into the database
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                       username, generate_password_hash(password))

        # login the new user
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]
        return redirect("/")

    return render_template("register.html")


@app.route("/item", methods=["GET", "POST"])
def item():
    if request.method == "GET":
        errorcode = 400
        message = "Please select a shelf and a place beforehand!"
        return render_template("apology.html", errorcode = errorcode, message = message)
    else:
        items = db.execute("SELECT * FROM items WHERE place = ?, shelf = ?")
        return render_template("add.html", items = items)
    

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        return render_template("add.html")
    return render_template("add.html")
