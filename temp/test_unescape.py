import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'Code/Chapter-03-Operators-Expressions.html', 'r', encoding='utf-8') as f:
    text = f.read()

clean_text = text.replace(r'\n', '\n').replace(r'\"', '"')
print("First 600 chars of cleaned text:")
print(clean_text[:600])

print("\n...\nLast 600 chars of cleaned text:")
print(clean_text[-600:])
