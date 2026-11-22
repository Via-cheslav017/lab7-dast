import os
import sqlite3
import subprocess
import uuid
from flask import Flask, Response, make_response, redirect, request

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES_DIR = os.path.join(BASE_DIR, "files")
DB_PATH = "/tmp/lab7.db"

PAGE = """<!doctype html>
<html lang="uk">
<head><meta charset="utf-8"><title>Lab7 Shop</title></head>
<body>
<h1>Lab7 Shop</h1>
<!-- TODO: прибрати debug-посилання /user?id=1 перед релізом -->
<p>ID останнього замовлення: 1700000000</p>
<ul>
  <li><a href="/search?q=test">Пошук</a></li>
  <li><a href="/user?id=1">Профіль користувача</a></li>
  <li><a href="/file?name=readme.txt">Документ: readme</a></li>
  <li><a href="/file?name=about.txt">Документ: about</a></li>
  <li><a href="/diag?host=localhost">Діагностика хоста</a></li>
  <li><a href="/go?url=/">Перехід</a></li>
</ul>
<form action="/search" method="get">
  <input type="text" name="q"><input type="submit" value="Шукати">
</form>
<form action="/login" method="post">
  <input type="text" name="username">
  <input type="password" name="password">
  <input type="submit" value="Увійти">
</form>
</body>
</html>"""

def db():
    return sqlite3.connect(DB_PATH)

def init_db():
    con = db()
    con.executescript(
        """
        DROP TABLE IF EXISTS users;
        CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT);
        INSERT INTO users VALUES (1, 'alice', 'alice@example.test', 'alice-pass');
        INSERT INTO users VALUES (2, 'bob', 'bob@example.test', 'bob-pass');
        INSERT INTO users VALUES (3, 'admin', 'admin@example.test', 'S3cr3t-admin');
        """
    )
    con.commit()
    con.close()

@app.route("/")
def index():
    resp = make_response(PAGE)
    if "sid" not in request.cookies:
        resp.set_cookie("sid", uuid.uuid4().hex)
    return resp

@app.route("/search")
def search():
    q = request.args.get("q", "")
    return f"<html><body><h2>Результати пошуку: {q}</h2><p>Нічого не знайдено.</p><a href='/'>Назад</a></body></html>"

@app.route("/user")
def user():
    uid = request.args.get("id", "1")
    query = "SELECT id, username, email FROM users WHERE id = " + uid
    try:
        rows = db().execute(query).fetchall()
    except Exception as e:
        return f"SQL error: {e}<br>Query: {query}", 500
    return "<br>".join(f"{r[0]}: {r[1]} ({r[2]})" for r in rows) or "Not found"

@app.route("/file")
def file():
    name = request.args.get("name", "readme.txt")
    path = os.path.join(FILES_DIR, name)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return Response(f.read(), mimetype="text/plain")
    except Exception:
        return Response("Файл не знайдено", status=404, mimetype="text/plain")

@app.route("/diag")
def diag():
    host = request.args.get("host", "localhost")
    out = subprocess.run("echo checking " + host, shell=True, capture_output=True, text=True, timeout=10)
    return Response(out.stdout + out.stderr, mimetype="text/plain")

@app.route("/go")
def go():
    return redirect(request.args.get("url", "/"))

@app.route("/login", methods=["POST"])
def login():
    u = request.form.get("username", "")
    p = request.form.get("password", "")
    row = db().execute("SELECT id FROM users WHERE username=? AND password=?", (u, p)).fetchone()
    if row:
        return "Вхід виконано", 200
    return "Невірний логін або пароль", 401

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)