import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'temp/ch-8.md', 'r', encoding='utf-8') as f:
    text = f.read().replace('\r\n', '\n').replace('\r', '\n')

splits = re.split(r'\n(?=#\s+8\.\d+\s+)', text)
print(f"Total splits: {len(splits)}")
print("Section 0 lines:", len(splits[0].splitlines()))

sec75_and_after = splits[75]
post_parts = re.split(r'\n(?=#{1,2}\s+[🔥🧠📝🎯])', sec75_and_after)
print(f"Post parts count: {len(post_parts)}")
for i, p in enumerate(post_parts):
    h = [l for l in p.strip().splitlines() if l.strip()][0]
    print(f"  Post part {i}: {h}")
