from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)

deadlines = []

@app.route("/")
def home():
    today = datetime.today().date()

    updated_deadlines = []

    for d in deadlines:
        deadline_date = datetime.strptime(d["date"], "%Y-%m-%d").date()
        days_left = (deadline_date - today).days

        updated_deadlines.append({
            "subject": d["subject"],
            "task": d["task"],
            "date": d["date"],
            "days_left": days_left
        })

    return render_template("index.html", deadlines=updated_deadlines)


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
def delete_deadline(index):
    deadlines.pop(index)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
