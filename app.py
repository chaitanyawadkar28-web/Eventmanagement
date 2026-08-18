from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)

# ==========================================
# SECRET KEY
# ==========================================

app.secret_key = "eventease_secret_key"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db_connection():

    conn = sqlite3.connect("eventease.db")

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

        username = request.form["username"]

        password = request.form["password"]


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

        conn.close()


        if user:

            session["username"] = username

            return redirect(
                url_for("home")
            )


        else:

            return render_template(
                "login.html",

                error="Invalid username or password."
            )


    return render_template("login.html")


# ==========================================
# REGISTER
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        email = request.form["email"]

        password = request.form["password"]


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

            conn.close()


            return redirect(
                url_for("login")
            )


        except sqlite3.IntegrityError:

            return render_template(
                "register.html",

                error="Username or Email already exists."
            )


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


    conn = get_db_connection()

    cursor = conn.cursor()


    # Get reviews for selected venue

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


    conn.close()


    return render_template(

        "venue_details.html",

        venue_name=venue_name,

        username=session["username"],

        reviews=reviews

    )


# ==========================================
# ADD REVIEW
# ==========================================

@app.route("/add-review", methods=["POST"])
def add_review():

    # Check login

    if "username" not in session:

        return redirect(
            url_for("login")
        )


    # Get form data

    venue_name = request.form["venue_name"]

    rating = request.form["rating"]

    review = request.form["review"]

    username = session["username"]


    # Convert rating to integer

    rating = int(rating)


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
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    init_db()

   
    app.run(host="0.0.0.0", port=5000, debug=True)