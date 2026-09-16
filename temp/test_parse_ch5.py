import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'temp/ch-5.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Normalize line endings to \n
text = text.replace('\r\n', '\n').replace('\r', '\n')

# Check section splitting
splits = re.split(r'\n(?=#\s+5\.\d+\s+)', text)
print(f"Total splits: {len(splits)}")

# Post 5.52 splitting
post_parts = re.split(r'\n(?=#\s+[🧠🔥📝🎯])', splits[52])
print(f"Post parts count: {len(post_parts)}")
for i, p in enumerate(post_parts):
    h = [l for l in p.strip().splitlines() if l.strip()][0]
    print(f"  Post part {i}: {h}")
