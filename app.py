from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)

# DATABASE PATH (persistent storage in Azure)

DB_PATH = "/home/deadlines.db"

# ---------- DATABASE INITIALIZATION ----------

def init_db():
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

```
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
```

init_db()

# ---------- HOME PAGE ----------

@app.route("/")
def home():

```
today = datetime.today().date()
tomorrow = today + timedelta(days=1)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT id, subject, task, date FROM deadlines")
rows = cursor.fetchall()

conn.close()

updated_deadlines = []
tomorrow_tasks = []

for r in rows:

    deadline_date = datetime.strptime(r[3], "%Y-%m-%d").date()
    days_left = (deadline_date - today).days

    deadline_data = {
        "id": r[0],
        "subject": r[1],
        "task": r[2],
        "date": r[3],
        "days_left": days_left
    }

    updated_deadlines.append(deadline_data)

    # Check if task is due tomorrow
    if deadline_date == tomorrow:
        tomorrow_tasks.append(deadline_data)

# Create subject list for dropdown
subjects = sorted(list(set([d["subject"] for d in updated_deadlines])))

return render_template(
    "index.html",
    deadlines=updated_deadlines,
    subjects=subjects,
    tomorrow_tasks=tomorrow_tasks
)
```

# ---------- ADD DEADLINE ----------

@app.route("/add", methods=["POST"])
def add_deadline():

```
subject = request.form["subject"]
task = request.form["task"]
date = request.form["date"]

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute(
    "INSERT INTO deadlines (subject, task, date) VALUES (?, ?, ?)",
    (subject, task, date)
)

conn.commit()
conn.close()

return redirect("/")
```

# ---------- DELETE DEADLINE ----------

@app.route("/delete/[int:id](int:id)")
def delete_deadline(id):

```
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("DELETE FROM deadlines WHERE id=?", (id,))

conn.commit()
conn.close()

return redirect("/")
```

# ---------- RUN APP ----------

if **name** == "**main**":
app.run(debug=True)
