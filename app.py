import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///reports.db")


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
    return render_template("index.html")


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    """Buy shares of stock"""
    return render_template("index.html")


@app.route("/report", methods=["GET", "POST"])
@login_required
def report():
    """Buy shares of stock"""

    if request.method == "POST":
        landmark = request.form.get("landmark")
        exactlocation = request.form.get("exactlocation")
        notes = request.form.get("notes")

        # Initialize photo_data as None
        photo_data = None

        # Check if a file was uploaded
        # get photo from form
        if "photo" in request.files:
            photo = request.files["photo"]
            # Check if the file is a photo
            if photo.filename != "" and photo.filename.endswith((".jpg", ".jpeg", ".png")):
                photo_data = photo.read()

        # Insert the data into the database
        db.execute("INSERT INTO reports (landmark, exactlocation, notes, photo) VALUES (?, ?, ?, ?)",
                   landmark, exactlocation, notes, photo_data)
    # Pass the entries to the template rendering function
    return render_template("report.html")


@app.route("/view", methods=["GET", "POST"])
@login_required
def view():
    """Buy shares of stock"""
    return render_template("view.html", reports=db.execute("SELECT * FROM reports"))


@app.route("/adopt", methods=["GET", "POST"])
@login_required
def adopt():
    """Buy shares of stock"""
    return render_template("adopt.html")


@app.route("/report-photo/<int:id>", methods=["GET"])
def image(id):
    """Return image"""
    row = db.execute("SELECT * FROM reports WHERE id = ?", id)
    # set the content type to the image type
    if row[0]["photo"] is None:
        return apology("No photo found", 404)

    return row[0]["photo"],200, {"Content-Type": "image/jpeg"}


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get(
                "username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

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
    num = 0
    num=num+1
    print(num)
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Ensure password was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation")

        # Ensure confirmation password is equal to password
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password dont match")
        try:
            # Add into db
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?,?)", request.form.get(
                "username"), generate_password_hash(request.form.get("password")))

        except:
            # Check if its unique
            return apology("username is already registered")

        # Remember the user
        session["user_id"] = new_user

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
