import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'temp/ch-5.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('# 5.50')
print(text[idx:])
