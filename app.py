from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta

app = Flask(__name__)

deadlines = []

@app.route("/")
def home():

    today = datetime.today().date()   # FIX: remove time part

    global deadlines

    # Remove tasks older than 14 days
    deadlines = [
        d for d in deadlines
        if datetime.strptime(d["date"], "%Y-%m-%d").date() > today - timedelta(days=14)
    ]

    for d in deadlines:
        deadline_date = datetime.strptime(d["date"], "%Y-%m-%d").date()  # FIX
        d["days_left"] = (deadline_date - today).days  # correct calculation

    deadlines_sorted = sorted(deadlines, key=lambda x: x["date"])

    # Create UNIQUE subject list
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

    deadlines.append({
        "subject": subject,
        "task": task,
        "date": date
    })

    return redirect("/")


@app.route("/delete/<int:index>")
def delete(index):

    if index < len(deadlines):
        deadlines.pop(index)

    return redirect("/")


if __name__ == "__main__":
    app.run()