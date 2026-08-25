from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "subham_ev.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            vehicle TEXT,
            preferred_date TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit-enquiry", methods=["POST"])
def submit_enquiry():

    name = request.form.get("name")
    phone = request.form.get("phone")
    vehicle = request.form.get("vehicle")
    preferred_date = request.form.get("date")
    message = request.form.get("message")

    connection = get_db_connection()

    connection.execute("""
        INSERT INTO enquiries
        (name, phone, vehicle, preferred_date, message)
        VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        phone,
        vehicle,
        preferred_date,
        message
    ))

    connection.commit()
    connection.close()

    return redirect(url_for("home") + "?success=1")


# ==============================
# ADMIN DASHBOARD
# ==============================

@app.route("/admin")
def admin():

    connection = get_db_connection()

    enquiries = connection.execute("""
        SELECT * FROM enquiries
        ORDER BY id DESC
    """).fetchall()

    total = connection.execute("""
        SELECT COUNT(*) FROM enquiries
    """).fetchone()[0]

    connection.close()

    return render_template(
        "admin.html",
        enquiries=enquiries,
        total=total
    )


# ==============================
# DELETE ENQUIRY
# ==============================

@app.route("/admin/delete/<int:enquiry_id>", methods=["POST"])
def delete_enquiry(enquiry_id):

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM enquiries WHERE id = ?",
        (enquiry_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("admin"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)