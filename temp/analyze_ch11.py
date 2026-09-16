import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'temp/ch-11.md', 'r', encoding='utf-8') as f:
    text = f.read()

print("File length:", len(text), "characters, lines:", len(text.splitlines()))

# Headings
headings = re.findall(r'^(#+)\s+(.+)$', text, re.MULTILINE)
print(f"Total headings: {len(headings)}")

h1_list = [h for h in headings if h[0] == '#']
print(f"Total H1: {len(h1_list)}")

numbered_secs = [h for h in h1_list if re.match(r'11\.\d+', h[1])]
print(f"Total numbered sections: {len(numbered_secs)}")
if numbered_secs:
    print(f"First numbered: {numbered_secs[0][1]}")
    print(f"Last numbered: {numbered_secs[-1][1]}")

non_numbered_h1 = [h for h in h1_list if not re.match(r'11\.\d+', h[1])]
print("\nNon-numbered H1s:")
for h in non_numbered_h1:
    print(" -", h[1])

# Practice items
practices = re.findall(r'^##+\s+(Practice\s+\d+.*)$', text, re.MULTILINE)
print(f"\nTotal Practice items: {len(practices)}")
for p in practices:
    print(" -", p)
