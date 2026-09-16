import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'temp/ch-7.md', 'r', encoding='utf-8') as f:
    text = f.read().replace('\r\n', '\n')

blocks = re.findall(r'((?:###[^\n]*\n+)?)```text\n(.*?)```', text, flags=re.S)
print(f"Total text blocks: {len(blocks)}")
for i, (h, c) in enumerate(blocks):
    h_clean = h.strip() if h else "No heading"
    preview = c.strip().replace('\n', ' ')[:60]
    if any(ch in c for ch in ('↓', '→', '┌', '└', '│', '▼', '▲', 'TDZ', '|', '+')):
        print(f"Diagram {i+1}: {h_clean} -> {preview}")
