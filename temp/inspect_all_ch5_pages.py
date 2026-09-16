import pymupdf
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

doc = pymupdf.open('PDF/Chapter-05-Loops-Iteration.pdf')
print(f"Total pages: {len(doc)}")

sections_found = {}

for page_idx in range(len(doc)):
    page = doc[page_idx]
    text = page.get_text()
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    
    # Find any section headers like '5.X'
    found_in_page = re.findall(r'\b(5\.\d+)\b', text)
    for s in found_in_page:
        if s not in sections_found:
            sections_found[s] = page_idx + 1
            
    first_few = " | ".join(lines[:2]) if lines else "EMPTY"
    last_few = " | ".join(lines[-2:]) if lines else "EMPTY"
    # print brief summary
    # print(f"Page {page_idx+1:02d}: Starts with '{first_few[:40]}' ... Ends with '{last_few[:40]}'")

print(f"\nTotal numbered sections found in PDF: {len(sections_found)} / 52")
missing = [f"5.{i}" for i in range(1, 53) if f"5.{i}" not in sections_found]
if missing:
    print(f"Missing from PDF: {missing}")
else:
    print("ALL 52 sections confirmed present in PDF!")

# Check Practice Set, Cheat Sheet, Summary
full_text = "".join(p.get_text() for p in doc)
print("\nPost-section checks in PDF:")
print("Cheat Sheet:", "Chapter 5 Cheat Sheet" in full_text)
print("Differences:", "সবচেয়ে গুরুত্বপূর্ণ পার্থক্য" in full_text)
print("Practice Set:", "Practice Set" in full_text)
print("Coding Practice:", "Coding Practice" in full_text)
print("Summary:", "Chapter 5-এর মূল শিক্ষা" in full_text)
print("Next Chapter Preview:", "Chapter 6 Preview" in full_text or "Functions" in full_text)

# Check Basic 1-10
basic_ok = all(f"{i}." in full_text for i in range(1, 11))
print("Basic Questions 1-10 all present:", basic_ok)

# Check Problem 1-10
probs_ok = all(f"Problem {i}" in full_text for i in range(1, 11))
print("Coding Problems 1-10 all present:", probs_ok)
