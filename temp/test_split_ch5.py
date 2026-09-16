import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-5.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Split sections
# Headings like '# 5.1 ...'
section_splits = re.split(r'\n(?=#\s+5\.\d+\s+)', text)
print(f"Opening + Numbered sections count: {len(section_splits)}")
print("Section 0 title:", section_splits[0].splitlines()[:5])
for i in range(1, len(section_splits)):
    h = section_splits[i].splitlines()[0]
    print(f"Sec {i}: {h}")
