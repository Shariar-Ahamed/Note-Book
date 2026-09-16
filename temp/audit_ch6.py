import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'Code/Chapter-06-Functions.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Verify numbered sections 6.1 to 6.66
missing_secs = []
for i in range(1, 67):
    sec = f"6.{i}"
    if f">{sec}<" not in html and f">{sec} " not in html:
        missing_secs.append(sec)

print(f"Missing sections count: {len(missing_secs)}")
if missing_secs:
    print(f"Missing: {missing_secs}")
else:
    print("All sections 6.1 to 6.66 are present!")

# 2. Verify Part Banners
part_banners = re.findall(r'<div class="part-banner">(.*?)</div>', html)
print(f"\nPart banners found ({len(part_banners)}):")
for pb in part_banners:
    print(f"  - {pb}")

# 3. Verify Basic Questions 1 to 15
basic_qs = re.findall(r'<strong>(\d+)\.</strong>', html)
print(f"\nBasic practice questions found: {len(basic_qs)}")

# 4. Verify Coding Problems 1 to 10
coding_ps = re.findall(r'<h4[^>]*>(Problem \d+[^<]*)</h4>', html)
print(f"\nCoding problems found ({len(coding_ps)}):")
for cp in coding_ps:
    print(f"  - {cp}")

# 5. Verify Cheat Sheet, Must Remember, Summary
print("\nPost-section checks:")
print("Quick Cheat Sheet:", "Quick Cheat Sheet" in html)
print("Must Remember:", "Must Remember" in html)
print("Summary:", "Chapter 6 শেষ করার পর" in html)
print("Function ecosystem tree:", "├── Declaration" in html)

# 6. Check for literal \\n or unparsed artifacts
print(f"\nLiteral \\n count: {html.count('\\n')}")
print(f"Literal \\\" count: {html.count('\\\"')}")

# 7. Check print CSS rules
print(f"@page 8mm 10mm: {'margin: 8mm 10mm' in html}")
print(f"page-break-inside avoid: {'page-break-inside: avoid !important' in html}")
print(f"doc-page padding 0: {'padding: 0 !important' in html}")
