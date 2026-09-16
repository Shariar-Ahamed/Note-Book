import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'temp/ch-11.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('# 11.54')
print(text[idx:])
