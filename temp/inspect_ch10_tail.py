import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'temp/ch-10.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('# 10.68')
print(text[idx:])
