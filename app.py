from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import time

app = Flask(__name__)

# ==========================================
# SECRET KEY
# ==========================================

app.secret_key = "eventease_secret_key"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db_connection():

    conn = sqlite3.connect(
        "eventease.db",
        timeout=30,
        check_same_thread=False
    )

    # Wait up to 30 seconds if database is busy
    conn.execute("PRAGMA busy_timeout = 30000")

    # Helps reduce SQLite locking problems
    conn.execute("PRAGMA journal_mode = WAL")

    return conn


# ==========================================
# INITIALIZE DATABASE
# ==========================================

def init_db():

    conn = get_db_connection()

    cursor = conn.cursor()

    # ======================================
    # USERS TABLE
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        )
    """)

    # ======================================
    # REVIEWS TABLE
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            venue_name TEXT NOT NULL,

            username TEXT NOT NULL,

            rating INTEGER NOT NULL,

            review TEXT NOT NULL

        )
    """)

    conn.commit()
    conn.close()


# ==========================================
# LOGIN
# ==========================================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        conn = None

        try:

            conn = get_db_connection()

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM users
                WHERE username = ?
                AND password = ?
                """,
                (username, password)
            )

            user = cursor.fetchone()

            if user:

                session["username"] = username

                return redirect(url_for("home"))

            return render_template(
                "login.html",
                error="Invalid username or password."
            )

        finally:

            if conn:
                conn.close()

    return render_template("login.html")


# ==========================================
# REGISTER
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    # ======================================
    # SHOW REGISTER PAGE
    # ======================================

    if request.method == "GET":

        return render_template("register.html")


    # ======================================
    # GET FORM DATA
    # ======================================

    username = request.form.get("username", "").strip()

    email = request.form.get("email", "").strip()

    password = request.form.get("password", "")


    # ======================================
    # BASIC VALIDATION
    # ======================================

    if not username or not email or not password:

        return render_template(
            "register.html",
            error="Please fill all fields."
        )


    conn = None


    # ======================================
    # SAVE USER
    # ======================================

    try:

        conn = get_db_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users
            (username, email, password)
            VALUES (?, ?, ?)
            """,
            (
                username,
                email,
                password
            )
        )

        conn.commit()

        return redirect(url_for("login"))


    except sqlite3.IntegrityError:

        return render_template(
            "register.html",
            error="Username or Email already exists."
        )


    except sqlite3.OperationalError as e:

        if "locked" in str(e).lower():

            return render_template(
                "register.html",
                error="Database is busy. Please wait a few seconds and try again."
            )

        return render_template(
            "register.html",
            error="Registration failed: " + str(e)
        )


    finally:

        if conn:

            conn.close()


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/home")
def home():

    if "username" not in session:

        return redirect(
            url_for("login")
        )

    return render_template(
        "index.html",
        username=session["username"]
    )


# ==========================================
# VENUE DETAILS PAGE
# ==========================================

@app.route("/venue/<venue_name>")
def venue_details(venue_name):

    if "username" not in session:

        return redirect(
            url_for("login")
        )

    conn = None

    try:

        conn = get_db_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM reviews
            WHERE venue_name = ?
            ORDER BY id DESC
            """,
            (venue_name,)
        )

        reviews = cursor.fetchall()

        return render_template(
            "venue_details.html",
            venue_name=venue_name,
            username=session["username"],
            reviews=reviews
        )

    finally:

        if conn:

            conn.close()


# ==========================================
# ADD REVIEW
# ==========================================

@app.route("/add-review", methods=["POST"])
def add_review():

    # ======================================
    # CHECK LOGIN
    # ======================================

    if "username" not in session:

        return redirect(
            url_for("login")
        )


    # ======================================
    # GET FORM DATA
    # ======================================

    venue_name = request.form.get("venue_name", "")

    rating = request.form.get("rating", "")

    review = request.form.get("review", "").strip()

    username = session["username"]


    # ======================================
    # CONVERT RATING
    # ======================================

    try:

        rating = int(rating)

    except ValueError:

        return redirect(
            url_for(
                "venue_details",
                venue_name=venue_name
            )
        )


    # ======================================
    # CHECK RATING
    # ======================================

    if rating < 1 or rating > 5:

        return redirect(
            url_for(
                "venue_details",
                venue_name=venue_name
            )
        )


    # ======================================
    # SAVE REVIEW
    # ======================================

    conn = None

    try:

        conn = get_db_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO reviews
            (
                venue_name,
                username,
                rating,
                review
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                venue_name,
                username,
                rating,
                review
            )
        )

        conn.commit()

    finally:

        if conn:

            conn.close()


    # ======================================
    # BACK TO VENUE
    # ======================================

    return redirect(
        url_for(
            "venue_details",
            venue_name=venue_name
        )
    )


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# ==========================================
# INITIALIZE DATABASE
# ==========================================

# IMPORTANT:
# Gunicorn/Render imports this file,
# so database initialization must happen
# outside __main__.

init_db()


# ==========================================
# RUN APPLICATION LOCALLY
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
