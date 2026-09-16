import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'Code/Chapter-05-Loops-Iteration.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Verify numbered sections 5.1 to 5.52
missing_secs = []
for i in range(1, 53):
    sec = f"5.{i}"
    if f">{sec}<" not in html and f">{sec} " not in html:
        missing_secs.append(sec)

print(f"Missing sections count: {len(missing_secs)}")
if missing_secs:
    print(f"Missing: {missing_secs}")
else:
    print("All sections 5.1 to 5.52 are present!")

# 2. Verify Part Banners
part_banners = re.findall(r'<div class="part-banner">(.*?)</div>', html)
print(f"Part banners found ({len(part_banners)}):")
for pb in part_banners:
    print(f"  - {pb}")

# 3. Verify Basic Practice Questions
basic_qs = re.findall(r'<strong>(\d+)\.</strong>', html)
print(f"Basic practice questions found: {len(basic_qs)}")

# 4. Verify Coding Practice Problems
coding_ps = re.findall(r'<h4[^>]*>(Problem \d+[^<]*)</h4>', html)
print(f"Coding problems found ({len(coding_ps)}):")
for cp in coding_ps:
    print(f"  - {cp}")

# 5. Verify Cheat sheet, Comparison, Summary, Next Chapter
print("Cheat Sheet present:", "🧠 Chapter 5 Cheat Sheet" in html)
print("Comparison present:", "🔥 সবচেয়ে গুরুত্বপূর্ণ পার্থক্য" in html)
print("Summary present:", "🎯 Chapter 5-এর মূল শিক্ষা" in html)
print("Next Chapter present:", "Chapter 6 Preview" in html)

# 6. Check for literal \\n or unparsed artifacts
literal_n = html.count('\\n')
print(f"Literal \\n count: {literal_n}")
literal_quote = html.count('\\"')
print(f"Literal \\\" count: {literal_quote}")

# 7. Check print CSS rules
print("@page 8mm 10mm present:", "margin: 8mm 10mm" in html)
print("page-break-inside avoid present:", "page-break-inside: avoid !important" in html)
print("doc-page padding 0 in print:", "padding: 0 !important" in html)
