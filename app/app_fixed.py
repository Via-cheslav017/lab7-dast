import hmac
import os
import re
import secrets
import sqlite3
import subprocess
import uuid
from flask import Flask, Response, abort, make_response, redirect, request
from markupsafe import escape

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES_DIR = os.path.realpath(os.path.join(BASE_DIR, "files"))
DB_PATH = "/tmp/lab7.db"
CSRF = {}
HOST_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.-]{0,63}$")
NAME_RE = re.compile(r"^[A-Za-z0-9_.-]{1,64}$")
ID_RE = re.compile(r"^[0-9]{1,9}$")

PAGE = """<!doctype html>
<html lang="uk">
<head><meta charset="utf-8"><title>Lab7 Shop</title></head>
<body>
<h1>Lab7 Shop</h1>
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
  <input type="hidden" name="csrf_token" value="__CSRF__">
  <input type="text" name="username">
  <input type="password" name="password">
  <input type="submit" value="Увійти">
</form>
</body>
</html>"""

@app.after_request
def secure_headers(resp):
    resp.headers["Server"] = "lab7"
    resp.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none'; form-action 'self'"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Referrer-Policy"] = "no-referrer"
    resp.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
    resp.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    resp.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    resp.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    resp.headers["Cache-Control"] = "no-store"
    return resp

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
    sid = request.cookies.get("sid") or uuid.uuid4().hex
    token = secrets.token_hex(16)
    CSRF[sid] = token
    resp = make_response(PAGE.replace("__CSRF__", token))
    resp.set_cookie("sid", sid, httponly=True, samesite="Strict")
    return resp

@app.route("/search")
def search():
    q = str(escape(request.args.get("q", "")[:100]))
    return f"<html><body><h2>Результати пошуку: {q}</h2><p>Нічого не знайдено.</p><a href='/'>Назад</a></body></html>"

@app.route("/user")
def user():
    raw = request.args.get("id", "1")
    if not ID_RE.fullmatch(raw):
        return "Некоректний id", 400
    rows = db().execute("SELECT id, username, email FROM users WHERE id = ?", (int(raw),)).fetchall()
    return "<br>".join(f"{r[0]}: {escape(r[1])} ({escape(r[2])})" for r in rows) or "Not found"

@app.route("/file")
def file():
    name = request.args.get("name", "readme.txt")
    if not NAME_RE.fullmatch(name):
        abort(400)
    path = os.path.realpath(os.path.join(FILES_DIR, name))
    if os.path.commonpath([FILES_DIR, path]) != FILES_DIR or not os.path.isfile(path):
        abort(404)
    with open(path, "r", encoding="utf-8") as f:
        return Response(f.read(), mimetype="text/plain")

@app.route("/diag")
def diag():
    host = request.args.get("host", "localhost")
    if not HOST_RE.fullmatch(host):
        return Response("Некоректне ім'я хоста", status=400, mimetype="text/plain")
    out = subprocess.run(["echo", "checking", host], capture_output=True, text=True, timeout=5, check=False)
    return Response(out.stdout, mimetype="text/plain")

@app.route("/go")
def go():
    url = request.args.get("url", "/")
    if not url.startswith("/") or url.startswith("//") or "\\" in url:
        url = "/"
    return redirect(url)

@app.route("/login", methods=["POST"])
def login():
    sid = request.cookies.get("sid", "")
    token = request.form.get("csrf_token", "")
    if not sid or not hmac.compare_digest(CSRF.get(sid, ""), token):
        return "Недійсний CSRF-токен", 403
    u = request.form.get("username", "")
    p = request.form.get("password", "")
    row = db().execute("SELECT id FROM users WHERE username=? AND password=?", (u, p)).fetchone()
    if row:
        return "Вхід виконано", 200
    return "Невірний логін або пароль", 401

@app.errorhandler(Exception)
def handle_error(e):
    code = getattr(e, "code", 500)
    return f"Помилка {code}", code

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)