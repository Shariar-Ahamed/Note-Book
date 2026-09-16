import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-3.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('# 89.')
print(text[idx:])
