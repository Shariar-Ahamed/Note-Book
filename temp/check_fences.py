import re

with open(r'temp/ch-9.md', 'r', encoding='utf-8') as f:
    text = f.read()

fences = re.findall(r'^```(.*)$', text, re.MULTILINE)
langs = set(f.strip() for f in fences if f.strip())
print("Real fence languages:", langs)
