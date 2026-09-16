import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'temp/ch-5.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Normalize \r\n to \n
text = text.replace('\r\n', '\n')

blocks = re.findall(r'((?:###[^\n]*\n+)?)```text\n(.*?)```', text, flags=re.S)
print(f"Total text blocks: {len(blocks)}")
for i, (heading, content) in enumerate(blocks):
    h_clean = heading.strip() if heading else "No heading"
    preview = content.strip().replace('\n', ' ')[:50]
    print(f"{i+1}: {h_clean} -> {preview}")
