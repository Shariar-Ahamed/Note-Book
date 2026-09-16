import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'Code/Chapter-03-Operators-Expressions.html', 'r', encoding='utf-8') as f:
    text = f.read()

clean_text = text.replace(r'\n', '\n').replace(r'\"', '"')
idx = clean_text.find('@media print')
print(clean_text[idx:idx+800])
