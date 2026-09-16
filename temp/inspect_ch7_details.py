import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'temp/ch-7.md', 'r', encoding='utf-8') as f:
    text = f.read().replace('\r\n', '\n').replace('\r', '\n')

tables = re.findall(r'(\|[^\n]+\|\n\|[-|\s]+\|\n(?:\|[^\n]+\|\n?)+)', text)
print(f"Found {len(tables)} tables:")
for i, t in enumerate(tables):
    rows = t.strip().splitlines()
    print(f"Table {i+1} has {len(rows)} lines. Header: {rows[0]}")

fences = re.findall(r'```([a-zA-Z0-9]*)', text)
from collections import Counter
print("\nCode fence types:", Counter(fences))
