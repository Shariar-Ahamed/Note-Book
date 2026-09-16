import re
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-2.md', 'r', encoding='utf-8') as f:
    md_text = f.read()

with open(r'c:\Users\User\Desktop\Note-Book\Code\Chapter-02-Variables-DataTypes-TypeSystem.html', 'r', encoding='utf-8') as f:
    html_text = f.read()

# Find headers in markdown
h2_list = re.findall(r'^##\s+(.+)$', md_text, flags=re.MULTILINE)
h3_list = re.findall(r'^###\s+(.+)$', md_text, flags=re.MULTILINE)
h4_list = re.findall(r'^####\s+(.+)$', md_text, flags=re.MULTILINE)

print(f"MD Header Counts -> H2: {len(h2_list)}, H3: {len(h3_list)}, H4: {len(h4_list)}")

# Numbered sections like "### 1.", "### 2.", etc. or "## Part"
numbered_sections = re.findall(r'^###\s+(\d+[\.\)].+)$', md_text, flags=re.MULTILINE)
print(f"Total numbered sections in MD: {len(numbered_sections)}")

missing = []
for sec in numbered_sections:
    # extract title number and key phrase
    num_match = re.match(r'^(\d+)[\.\)]\s*(.+)', sec)
    if num_match:
        num, title = num_match.groups()
        # search in html
        # Check if number + some title words are in html
        words = [w for w in re.findall(r'[A-Za-z0-9\u0980-\u09FF]+', title) if len(w) > 2]
        found = False
        if f">{num}." in html_text or f">{num} " in html_text or f" {num}. " in html_text:
            found = True
        elif any(w in html_text for w in words[:2]):
            found = True
        if not found:
            missing.append(sec)

print(f"Missing numbered sections: {len(missing)}")
for m in missing:
    print(" - ", m)

# Also check parts
parts = re.findall(r'PART\s+\d+|Part\s+\d+', md_text, flags=re.IGNORECASE)
print(f"Part occurrences in MD: {set(parts)}")
