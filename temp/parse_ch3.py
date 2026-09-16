import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'Code/Chapter-03-Operators-Expressions.html', 'r', encoding='utf-8') as f:
    text = f.read()

# unescape first
text = text.replace(r'\n', '\n').replace(r'\"', '"')

parts = re.findall(r'<div class="part-banner">(.*?)</div>', text)
print(f"Total parts in HTML: {len(parts)}")
for p in parts:
    print("  PART:", p)

cards = re.findall(r'<div class="card-title"><span class="badge-num">(\d+)</span>\s*(.*?)</div>', text)
print(f"Total cards in HTML: {len(cards)}")
print(f"First 5: {cards[:5]}")
print(f"Last 5: {cards[-5:]}")
