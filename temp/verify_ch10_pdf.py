import pymupdf as fitz
import sys, os

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"c:\Users\User\Desktop\Note-Book\PDF\Chapter-10-Objects.pdf"

if not os.path.exists(pdf_path):
    print("PDF not found yet:", pdf_path)
    sys.exit(1)

doc = fitz.open(pdf_path)
print("Total pages in PDF:", len(doc))

# Check Page 1
page1_text = doc[0].get_text()
print("\n--- PAGE 1 TEXT SNIPPET ---")
print(page1_text[:600])

print("\n--- PAGE 1 BALANCE CHECK ---")
has_banner = "CHAPTER 10: OBJECTS" in page1_text or "JavaScript Master Study" in page1_text
has_intro = "Objects — Object / Key-Value Data" in page1_text or "MongoDB" in page1_text
has_part1 = "PART 01" in page1_text or "Part 01" in page1_text
has_sec1 = "10.1" in page1_text

print(f"Has Master Banner: {has_banner}")
print(f"Has Intro Card: {has_intro}")
print(f"Has Part 1 Banner: {has_part1}")
print(f"Has Section 10.1: {has_sec1}")

# Check Section 10.2 on Page 1
print(f"Has Section 10.2 on Page 1: {'10.2' in page1_text}")

# Extract all text from PDF
full_text = ""
for p in doc:
    full_text += p.get_text() + "\n"

missing = []
for i in range(1, 69):
    sec_num = f"10.{i}"
    if sec_num not in full_text:
        missing.append(sec_num)

if missing:
    print("\nMISSING SECTIONS IN PDF:", missing)
else:
    print("\nALL 68 SECTIONS VERIFIED IN PDF!")

missing_pr = []
for i in range(1, 11):
    if f"Practice {i}" not in full_text:
        missing_pr.append(i)

if missing_pr:
    print("MISSING PRACTICES IN PDF:", missing_pr)
else:
    print("ALL 10 PRACTICES VERIFIED IN PDF!")

# Render preview of page 1 and last page
pix1 = doc[0].get_pixmap(dpi=150)
pix1.save(r"temp/ch10_page1_preview.png")
print("\nSaved temp/ch10_page1_preview.png")

pix_last = doc[-1].get_pixmap(dpi=150)
pix_last.save(r"temp/ch10_page_last_preview.png")
print("Saved temp/ch10_page_last_preview.png")
