import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'temp/ch-8.md', 'r', encoding='utf-8') as f:
    text = f.read().replace('\r\n', '\n').replace('\r', '\n')

sections = re.findall(r'^#\s+(8\.\d+\s+.*)$', text, flags=re.MULTILINE)
print(f"Total numbered sections found: {len(sections)}")
for s in sections:
    print(" ", s)

last_sec_num = sections[-1].split()[0] if sections else ""
print(f"\nLast section: {last_sec_num}")

if last_sec_num:
    after_last = text[text.find(f"# {last_sec_num}"):]
    h_after = re.findall(r'^#{1,2}\s+(.*)$', after_last, flags=re.MULTILINE)
    print("\nHeaders after last section:")
    for h in h_after:
        print(" ", h)
