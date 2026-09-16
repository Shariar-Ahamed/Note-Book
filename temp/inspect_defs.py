import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'Code/Chapter-03-Operators-Expressions.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(r'\n', '\n').replace(r'\"', '"')

idx = text.find('<span class="badge-num">89</span>')
print(text[idx:])
