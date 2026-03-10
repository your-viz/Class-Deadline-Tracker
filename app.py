from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)

DB = "deadlines.db"


def get_db():
    return sqlite3.connect(DB)


# create table if not exists
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS deadlines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        task TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():

    today = datetime.today().date()

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM deadlines")
    rows = cursor.fetchall()

    deadlines = []

    for r in rows:
        deadline_date = datetime.strptime(r[3], "%Y-%m-%d").date()

        # remove tasks older than 14 days
        if deadline_date > today - timedelta(days=14):

            deadlines.append({
                "id": r[0],
                "subject": r[1],
                "task": r[2],
                "date": r[3],
                "days_left": (deadline_date - today).days
            })

        else:
            cursor.execute("DELETE FROM deadlines WHERE id=?", (r[0],))

    conn.commit()
    conn.close()

    deadlines_sorted = sorted(deadlines, key=lambda x: x["date"])

    subjects = sorted(list(set(d["subject"] for d in deadlines_sorted)))

    return render_template(
        "index.html",
        deadlines=deadlines_sorted,
        subjects=subjects
    )


@app.route("/add", methods=["POST"])
def add_deadline():

    subject = request.form["subject"]
    task = request.form["task"]
    date = request.form["date"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO deadlines (subject,task,date) VALUES (?,?,?)",
        (subject, task, date)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM deadlines WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run()