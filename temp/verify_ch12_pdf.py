import pymupdf as fitz
import sys, os

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"c:\Users\User\Desktop\Note-Book\PDF\Chapter-12-Map-Set-WeakMap-WeakSet.pdf"
doc = fitz.open(pdf_path)

print("Total pages in Chapter 12 PDF:", len(doc))

full_text = ""
for p in doc:
    full_text += p.get_text() + "\n"

# Check all 60 sections 12.1 to 12.60
missing_secs = []
for i in range(1, 61):
    sec = f"12.{i}"
    if sec not in full_text:
        missing_secs.append(sec)

if missing_secs:
    print("MISSING SECTIONS:", missing_secs)
else:
    print("ALL 60 SECTIONS (12.1 - 12.60) PRESENT!")

# Check 5 practices
missing_prs = []
for i in range(1, 6):
    if f"Practice {i}" not in full_text:
        missing_prs.append(i)

if missing_prs:
    print("MISSING PRACTICES:", missing_prs)
else:
    print("ALL 5 PRACTICES PRESENT!")

print("Must Know present:", "Must Know" in full_text or "12.61" in full_text)
print("Cheat sheet present:", "Quick Cheat Sheet" in full_text)
print("Decision Guide present:", "কখন কোনটা ব্যবহার করব" in full_text)
print("Summary present:", "Chapter 12 Final Summary" in full_text)
print("Preview present:", "Chapter 13 Preview" in full_text)
