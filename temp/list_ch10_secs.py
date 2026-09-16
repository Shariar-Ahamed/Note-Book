import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'temp/ch-10.md', 'r', encoding='utf-8') as f:
    text = f.read()

secs = re.findall(r'^#\s+(10\.\d+.*)$', text, re.MULTILINE)
for i, s in enumerate(secs):
    print(f"{i+1}: {s}")
