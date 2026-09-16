import pymupdf
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'PDF/Chapter-07-Scope-Hoisting.pdf'
doc = pymupdf.open(pdf_path)
print(f"Total pages in Chapter 7 PDF: {len(doc)}")

# Check Page 1
page1 = doc[0]
text_p1 = page1.get_text()
print("\n=== Page 1 Full Text ===")
print(text_p1.strip())

print("\n=== Page 1 Verification ===")
print("Master Banner title present:", "JAVASCRIPT MASTER STUDY DOCUMENTATION" in text_p1)
print("Chapter Subtitle present:", "CHAPTER 07: SCOPE & HOISTING" in text_p1)
print("Opening Statement present:", "Scope & Hoisting" in text_p1)
print("Part 01 Banner present:", "Part 01" in text_p1)
print("Section 7.1 present:", "7.1" in text_p1)

# Check Page 2 start
page2 = doc[1]
text_p2 = page2.get_text()
print("\n=== Page 2 Start Preview ===")
print(text_p2[:250].strip())

# Check all 47 sections across the PDF
full_text = "".join(p.get_text() for p in doc)
missing = [f"7.{i}" for i in range(1, 48) if f"7.{i}" not in full_text]
print(f"\nMissing sections in PDF: {missing if missing else 'None! All 47 present!'}")

# Check Practice Set
print("Practice problems all present:", all(f"Practice {i}" in full_text for i in range(1, 9)))
print("Quick Cheat Sheet:", "Quick Cheat Sheet" in full_text)
print("Must Know:", "Must Know" in full_text)
print("Next Chapter Preview:", "Chapter 8 Preview" in full_text or "Strings" in full_text)
