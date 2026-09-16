import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'temp/ch-5.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all # 5.*
sections = re.findall(r'^#\s+(5\.\d+\s+.*)$', text, flags=re.MULTILINE)
print(f"Total numbered sections found: {len(sections)}")
for s in sections:
    print(" ", s)

# Find remaining H1 headers after 5.52
after_552 = text[text.find('# 5.52'):]
h1_after = re.findall(r'^#\s+(.*)$', after_552, flags=re.MULTILINE)
print("\nHeaders after 5.52:")
for h in h1_after:
    print(" ", h)
