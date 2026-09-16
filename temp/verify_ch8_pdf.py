import fitz # PyMuPDF
import os, sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"c:\Users\User\Desktop\Note-Book\PDF\Chapter-08-Strings.pdf"
doc = fitz.open(pdf_path)

print("Total pages in PDF:", len(doc))

# Page 1 text inspection
page1 = doc[0]
page1_text = page1.get_text()
print("\n--- PAGE 1 TEXT SNIPPET ---")
print(page1_text[:600])

print("\n--- PAGE 1 BALANCE CHECK ---")
has_banner = "CHAPTER 08: STRINGS" in page1_text or "JavaScript Master Study" in page1_text
has_intro = "String / টেক্সট নিয়ে কাজ" in page1_text or "Shariar" in page1_text
has_part1 = "Part 01" in page1_text
has_sec1 = "8.1" in page1_text

print(f"Has Master Banner: {has_banner}")
print(f"Has Intro Card: {has_intro}")
print(f"Has Part 1 Banner: {has_part1}")
print(f"Has Section 8.1: {has_sec1}")

# Check Section 8.2 on Page 1 or 2
has_sec2 = "8.2" in page1_text
print(f"Has Section 8.2 on Page 1: {has_sec2}")

# Check all sections in the entire document
full_text = ""
for p in doc:
    full_text += p.get_text() + "\n"

missing = []
for i in range(1, 76):
    sec_num = f"8.{i}"
    if sec_num not in full_text:
        missing.append(sec_num)

if missing:
    print("\nMISSING SECTIONS IN PDF:", missing)
else:
    print("\nALL 75 SECTIONS VERIFIED IN PDF!")

missing_pr = []
for i in range(1, 10):
    if f"Practice {i}" not in full_text:
        missing_pr.append(i)

if missing_pr:
    print("MISSING PRACTICES IN PDF:", missing_pr)
else:
    print("ALL 9 PRACTICES VERIFIED IN PDF!")

# Render preview image of page 1 to verify layout visually
pix1 = doc[0].get_pixmap(dpi=150)
pix1.save(r"temp/ch8_page1_preview.png")
print("\nSaved temp/ch8_page1_preview.png")

pix_last = doc[-1].get_pixmap(dpi=150)
pix_last.save(r"temp/ch8_page_last_preview.png")
print("Saved temp/ch8_page_last_preview.png")
