import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = fitz.open(r'c:\Users\User\Desktop\Note-Book\PDF\Chapter-02-Variables-DataTypes-TypeSystem.pdf')

for i, page in enumerate(doc):
    text = page.get_text().strip()
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    top = " // ".join(lines[:2]) if lines else "EMPTY"
    bottom = " // ".join(lines[-2:]) if lines else "EMPTY"
    print(f"P{i+1:02d}: [TOP] {top[:60]}  -->  [BOTTOM] {bottom[:60]}")
