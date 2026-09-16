import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'Code/Chapter-07-Scope-Hoisting.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Verify numbered sections 7.1 to 7.47
missing_secs = []
for i in range(1, 48):
    sec = f"7.{i}"
    if f">{sec}<" not in html and f">{sec} " not in html:
        missing_secs.append(sec)

print(f"Missing sections count: {len(missing_secs)}")
if missing_secs:
    print(f"Missing: {missing_secs}")
else:
    print("All sections 7.1 to 7.47 are present!")

# 2. Verify Part Banners
part_banners = re.findall(r'<div class="part-banner">(.*?)</div>', html)
print(f"\nPart banners found ({len(part_banners)}):")
for pb in part_banners:
    print(f"  - {pb}")

# 3. Verify Practice Problems 1 to 8
prac_ps = re.findall(r'<h4[^>]*>(Practice \d+[^<]*)</h4>', html)
print(f"\nPractice problems found ({len(prac_ps)}):")
for pp in prac_ps:
    print(f"  - {pp}")

# 4. Verify Cheat Sheet, Must Know, Summary, Next Chapter
print("\nPost-section checks:")
print("Quick Cheat Sheet:", "Quick Cheat Sheet" in html)
print("Must Know:", "Must Know" in html)
print("Summary:", "Chapter 7-এর মূল ধারণা" in html)
print("Next Chapter Preview:", "Chapter 8 Preview" in html)

# 5. Check for literal \\n or unparsed artifacts
print(f"\nLiteral \\n count: {html.count('\\n')}")
print(f"Literal \\\" count: {html.count('\\\"')}")

# 6. Check print CSS rules
print(f"@page 8mm 10mm: {'margin: 8mm 10mm' in html}")
print(f"page-break-inside avoid: {'page-break-inside: avoid !important' in html}")
print(f"doc-page padding 0: {'padding: 0 !important' in html}")
