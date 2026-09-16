import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')
pdf_path = r'c:\Users\User\Desktop\Note-Book\PDF\Chapter-03-Operators-Expressions.pdf'
doc = fitz.open(pdf_path)
print(f"Total pages in Chapter 3 PDF: {len(doc)}")

# Check text for literal \n or /n
has_slash_n = False
for i, page in enumerate(doc):
    text = page.get_text()
    if r'\n' in text:
        print(f"Page {i+1} has literal \\n!")
        has_slash_n = True

if not has_slash_n:
    print("SUCCESS: Zero literal \\n found in any page of the PDF!")

for i, page in enumerate(doc):
    text = page.get_text().strip()
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    top = " // ".join(lines[:2]) if lines else "EMPTY"
    bottom = " // ".join(lines[-2:]) if lines else "EMPTY"
    print(f"P{i+1:02d}: [TOP] {top[:60]}  -->  [BOTTOM] {bottom[:60]}")
