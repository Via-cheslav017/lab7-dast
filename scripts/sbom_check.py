import json
import sys

sbom = json.load(open(sys.argv[1], encoding="utf-8"))
name = sys.argv[2].lower()
found = [c for c in sbom.get("components", []) if c.get("name", "").lower() == name]
for c in found:
    print(f"ЗНАЙДЕНО: {c['name']} {c.get('version')}")
if not found:
    print("Компонент відсутній у продукті")
sys.exit(0 if found else 1)