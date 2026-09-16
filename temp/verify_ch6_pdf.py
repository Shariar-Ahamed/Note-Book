import pymupdf
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'PDF/Chapter-06-Functions.pdf'
doc = pymupdf.open(pdf_path)
print(f"Total pages in Chapter 6 PDF: {len(doc)}")

# Check Page 1
page1 = doc[0]
text_p1 = page1.get_text()
print("\n=== Page 1 Full Text ===")
print(text_p1.strip())

print("\n=== Page 1 Verification ===")
print("Master Banner title present:", "JAVASCRIPT MASTER STUDY DOCUMENTATION" in text_p1)
print("Chapter Subtitle present:", "CHAPTER 06: FUNCTIONS & EXECUTION ENGINE" in text_p1)
print("Opening Statement present:", "Functions — Code একবার লিখে বারবার ব্যবহার করার উপায়" in text_p1)
print("Part 01 Banner present:", "Part 01" in text_p1)
print("Section 6.1 present:", "6.1" in text_p1)
print("Section 6.2 present on Page 1:", "6.2" in text_p1)

# Check Page 2 start
page2 = doc[1]
text_p2 = page2.get_text()
print("\n=== Page 2 Start Preview ===")
print(text_p2[:250].strip())

# Check all 66 sections across the PDF
full_text = "".join(p.get_text() for p in doc)
missing = [f"6.{i}" for i in range(1, 67) if f"6.{i}" not in full_text]
print(f"\nMissing sections in PDF: {missing if missing else 'None! All 66 present!'}")

# Check Practice Set
print("Basic questions all present:", all(f"{i}." in full_text for i in range(1, 16)))
print("Coding problems all present:", all(f"Problem {i}" in full_text for i in range(1, 11)))
print("Quick Cheat Sheet:", "Quick Cheat Sheet" in full_text)
print("Must Remember:", "Must Remember" in full_text)
print("Ecosystem Tree:", "Ecosystem" in full_text or "Declaration" in full_text)
