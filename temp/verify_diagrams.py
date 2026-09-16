import pymupdf
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = pymupdf.open('PDF/Chapter-05-Loops-Iteration.pdf')
full_text = "".join(p.get_text() for p in doc)

diagram_checks = [
    "একবার code লিখবে",
    "Condition false হলে থামবে",
    "Student 50",
    "initialization",
    "update",
    "1 <= 5",
    "Choose Loop",
    "values",
    "keys",
    "break",
    "continue",
    "Nested Loop",
]

all_ok = True
for check in diagram_checks:
    found = check in full_text
    if not found:
        print(f"Missing diagram token: {check}")
        all_ok = False

if all_ok:
    print("All diagram elements and tokens verified perfectly in PDF!")
