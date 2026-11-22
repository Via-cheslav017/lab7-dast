import json
import sys
from pathlib import Path

CVSS = {
    "89": ("9.8", "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"),
    "78": ("9.8", "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"),
    "22": ("7.5", "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N"),
    "79": ("6.1", "AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N"),
    "601": ("6.1", "AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N"),
    "352": ("4.3", "AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N"),
    "693": ("4.3", "AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N"),
    "1021": ("4.3", "AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N"),
    "200": ("5.3", "AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N"),
    "209": ("5.3", "AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N"),
    "1004": ("3.1", "AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:N/A:N"),
}
RISK = {3: "High", 2: "Medium", 1: "Low", 0: "Info"}
DEADLINE = {3: "негайно", 2: "30 днів", 1: "90 днів", 0: "180 днів"}

def main():
    src, dst = sys.argv[1], sys.argv[2]
    gate = "--gate" in sys.argv
    data = json.loads(Path(src).read_text(encoding="utf-8"))
    sup = json.loads(Path("zap/suppressions.json").read_text(encoding="utf-8"))

    rows, blocking = [], 0
    for site in data.get("site", []):
        for a in site.get("alerts", []):
            risk = int(a.get("riskcode", 0))
            cwe = str(a.get("cweid", "-"))
            score, vec = CVSS.get(cwe, ("оцінити вручну", "-"))
            pid = str(a.get("pluginid"))
            if pid in sup:
                status = "Хибнопозитивна: " + sup[pid]
                prio, term = "-", "-"
            elif risk == 3:
                status, prio, term = "Критична: усунути негайно", "P1", DEADLINE[3]
                blocking += 1
            else:
                status, prio, term = "Технічний борг", "P2" if risk == 2 else "P3", DEADLINE[risk]
            rows.append((pid, a.get("name", ""), RISK[risk], cwe, f"{score} {vec}",
                         a.get("count", "?"), prio, term, status))

    rows.sort(key=lambda r: ("High", "Medium", "Low", "Info").index(r[2]))
    md = ["# Реєстр знахідок (автоматично з ZAP)\n",
          "| Plugin | Знахідка | Ризик ZAP | CWE | CVSS (орієнт.) | Екз. | Пріоритет | Строк | Статус |",
          "|---|---|---|---|---|---|---|---|---|"]
    md += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    Path(dst).write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Знахідок: {len(rows)}, блокувальних (High, без придушення): {blocking}. Реєстр: {dst}")

    if gate and blocking:
        print("GATE: є критичні знахідки, складання зупинено")
        sys.exit(1)

if __name__ == "__main__":
    main()