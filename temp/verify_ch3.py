import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-3.md', 'r', encoding='utf-8') as f:
    md_text = f.read()

with open(r'c:\Users\User\Desktop\Note-Book\Code\Chapter-03-Operators-Expressions.html', 'r', encoding='utf-8') as f:
    html_text = f.read()

clean_html = html_text.replace(r'\n', '\n').replace(r'\"', '"')

# Find all 89 sections in MD
sections = re.findall(r'^#\s+(\d+\..+)$', md_text, flags=re.MULTILINE)
print(f"Total numbered sections in ch-3.md: {len(sections)}")

missing_sections = []
for sec in sections:
    num = sec.split('.')[0].strip()
    title = sec.split('.', 1)[1].strip()
    if f'<span class="badge-num">{num}</span>' not in clean_html:
        missing_sections.append(sec)

print(f"Missing sections count: {len(missing_sections)}")
if missing_sections:
    for m in missing_sections:
        print("  Missing:", m)
