import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'Code/Chapter-03-Operators-Expressions.html', 'r', encoding='utf-8') as f:
    text = f.read()

clean_text = text.replace(r'\n', '\n').replace(r'\"', '"')

raw_md = re.findall(r'(?:\n|^)(?:#{1,4}\s+[^\n]+|```[^\n]*)', clean_text)
print(f"Raw MD elements in unescaped text: {len(raw_md)}")
for r in raw_md:
    print("  ", repr(r))

# Check where these raw markdown elements occur
for r in raw_md:
    pos = clean_text.find(r.strip())
    print("Around:", repr(clean_text[max(0, pos-40):min(len(clean_text), pos+100)]))
