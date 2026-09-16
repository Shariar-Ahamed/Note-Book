import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'Code/Chapter-03-Operators-Expressions.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(r'\n', '\n').replace(r'\"', '"')

# Split by card
cards = text.split('<div class="study-card"')
print(f"Total cards: {len(cards)-1}")

for i, card in enumerate(cards[1:], 1):
    # check for ``` or ### or ---
    if '```' in card or '###' in card:
        m = re.search(r'<span class="badge-num">(\d+)</span>', card)
        badge = m.group(1) if m else f"Card {i}"
        print(f"Section {badge} has raw markdown!")
