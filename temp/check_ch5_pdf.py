import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'PDF/Chapter-05-Loops-Iteration.pdf'
doc = fitz.open(pdf_path)
print(f"Total pages in Chapter 5 PDF: {len(doc)}")

# Check Page 1 content
page1 = doc[0]
text_p1 = page1.get_text()
print("=== Page 1 Text Preview ===")
print(text_p1[:400])
print("...")
print(text_p1[-300:])

# Check what is on Page 1:
print("\nPage 1 checks:")
print("Master Banner title present:", "JavaScript Master Study Documentation" in text_p1)
print("Chapter Subtitle present:", "CHAPTER 05: LOOPS & ITERATION" in text_p1)
print("Opening Statement present:", "Loops & Iteration" in text_p1)
print("Part 01 Banner present:", "Part 01" in text_p1)
print("Section 5.1 present:", "5.1" in text_p1)
print("Section 5.2 present:", "5.2" in text_p1)

# Check Page 2 start
page2 = doc[1]
text_p2 = page2.get_text()
print("\n=== Page 2 Start Preview ===")
print(text_p2[:250])
