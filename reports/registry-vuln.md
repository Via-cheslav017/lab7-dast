# Реєстр знахідок (автоматично з ZAP)

| Plugin | Знахідка | Ризик ZAP | CWE | CVSS (орієнт.) | Екз. | Пріоритет | Строк | Статус |
|---|---|---|---|---|---|---|---|---|
| 40012 | Cross Site Scripting (Reflected) | High | 79 | 6.1 AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N | 2 | P1 | негайно | Критична: усунути негайно |
| 20019 | External Redirect | High | 601 | 6.1 AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N | 1 | P1 | негайно | Критична: усунути негайно |
| 6 | Path Traversal | High | 22 | 7.5 AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N | 2 | P1 | негайно | Критична: усунути негайно |
| 90020 | Remote OS Command Injection | High | 78 | 9.8 AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H | 1 | P1 | негайно | Критична: усунути негайно |
| 40018 | SQL Injection - SQLite | High | 89 | 9.8 AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H | 1 | P1 | негайно | Критична: усунути негайно |
| 10202 | Absence of Anti-CSRF Tokens | Medium | 352 | 4.3 AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N | 2 | P2 | 30 днів | Технічний борг |
| 30001 | Buffer Overflow | Medium | 120 | оцінити вручну - | 1 | P2 | 30 днів | Технічний борг |
| 10038 | Content Security Policy (CSP) Header Not Set | Medium | 693 | 4.3 AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N | 5 | P2 | 30 днів | Технічний борг |
| 30002 | Format String Error | Medium | 134 | оцінити вручну - | 1 | P2 | 30 днів | Технічний борг |
| 10020 | Missing Anti-clickjacking Header | Medium | 1021 | 4.3 AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N | 4 | P2 | 30 днів | Технічний борг |
| 10010 | Cookie No HttpOnly Flag | Low | 1004 | 3.1 AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:N/A:N | 2 | P3 | 90 днів | Технічний борг |
| 10054 | Cookie without SameSite Attribute | Low | 1275 | оцінити вручну - | 2 | P3 | 90 днів | Технічний борг |
| 10036 | Server Leaks Version Information via "Server" HTTP Response Header Field | Low | 497 | оцінити вручну - | 5 | P3 | 90 днів | Технічний борг |
| 10096 | Timestamp Disclosure - Unix | Low | 497 | оцінити вручну - | 2 | - | - | Хибнопозитивна: Хибнопозитивне: число 1700000000 в тексті сторінки є ідентифікатором замовлення, а не часовою міткою сервера. Підтверджено ручним аналізом відповіді. |
| 10021 | X-Content-Type-Options Header Missing | Low | 693 | 4.3 AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N | 5 | P3 | 90 днів | Технічний борг |
| 10111 | Authentication Request Identified | Info | -1 | оцінити вручну - | 1 | P3 | 180 днів | Технічний борг |
| 10027 | Information Disclosure - Suspicious Comments | Info | 615 | оцінити вручну - | 2 | P3 | 180 днів | Технічний борг |
| 10112 | Session Management Response Identified | Info | -1 | оцінити вручну - | 3 | P3 | 180 днів | Технічний борг |
| 10104 | User Agent Fuzzer | Info | 0 | оцінити вручну - | 5 | P3 | 180 днів | Технічний борг |
