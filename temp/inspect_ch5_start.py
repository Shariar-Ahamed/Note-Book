import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'temp/ch-5.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(50, min(110, len(lines))):
    print(f"L{i+1}: {lines[i].rstrip()}")
