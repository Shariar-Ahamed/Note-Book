import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'temp/ch-11.md', 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()

fences = []
for i, line in enumerate(lines):
    if line.startswith('```'):
        fences.append((i+1, line))

print("Total fence lines:", len(fences))
print("Opening fences:", len(fences) // 2)

langs = set()
for line_num, line in fences:
    content = line[3:].strip()
    if content:
        lang = content.split()[0].lower()
        langs.add(lang)

print("Unique fence languages:", langs)
