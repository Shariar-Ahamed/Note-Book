import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-4.md', 'r', encoding='utf-8') as f:
    md_text = f.read()

with open(r'c:\Users\User\Desktop\Note-Book\Code\Chapter-04-Control-Flow-Decision-Making.html', 'r', encoding='utf-8') as f:
    html_text = f.read()

# Find all numbered sections in ch-4.md
sections_md = re.findall(r'^#\s+(\d+\..+)$', md_text, flags=re.MULTILINE)
print(f"Total numbered sections in ch-4.md: {len(sections_md)}")
for s in sections_md[:5]:
    print("  First 5:", s)
for s in sections_md[-5:]:
    print("  Last 5 :", s)

# Find cards in HTML
badges = re.findall(r'<span class="badge-num">(\d+)</span>', html_text)
print(f"Found badges in HTML: {len(badges)}")

# Check missing sections
missing = []
for s in sections_md:
    num = s.split('.')[0].strip()
    if num not in badges:
        missing.append(s)

print(f"Missing numbered sections: {len(missing)}")
if missing:
    for m in missing:
        print("  Missing:", m)

# Check what is after the last section in ch-4.md
last_sec_header = sections_md[-1]
idx = md_text.find(last_sec_header)
print("\n--- After last section in ch-4.md ---")
print(md_text[idx:idx+1500])
