import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'Code/Chapter-04-Control-Flow-Decision-Making.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('4.45')
print("--- END OF HTML ---")
print(text[idx:])
