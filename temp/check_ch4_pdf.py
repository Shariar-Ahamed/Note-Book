import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')
pdf_path = r'c:\Users\User\Desktop\Note-Book\PDF\Chapter-04-Control-Flow-Decision-Making.pdf'
doc = fitz.open(pdf_path)
print(f"Total pages in Chapter 4 PDF: {len(doc)}")

for i, page in enumerate(doc):
    text = page.get_text().strip()
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    top = " // ".join(lines[:2]) if lines else "EMPTY"
    bottom = " // ".join(lines[-2:]) if lines else "EMPTY"
    print(f"P{i+1:02d}: [TOP] {top[:55]}  -->  [BOTTOM] {bottom[:55]}")
