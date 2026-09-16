import re
import sys
from html.parser import HTMLParser

sys.stdout.reconfigure(encoding='utf-8')

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []
    def handle_data(self, d):
        self.text.append(d)
    def get_data(self):
        return ''.join(self.text)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

with open(r'c:\Users\User\Desktop\Note-Book\Code\Chapter-02-Variables-DataTypes-TypeSystem.html', 'r', encoding='utf-8') as f:
    raw_html = f.read()

plain_text = strip_tags(raw_html)
plain_norm = re.sub(r'\s+', ' ', plain_text)

with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-2.md', 'r', encoding='utf-8') as f:
    md_text = f.read()

sections = re.split(r'\n(?=#\s+\d+\.)', md_text)
print(f'Total sections found in MD: {len(sections)-1}')

missing_count = 0
for sec in sections[1:]:
    header = sec.splitlines()[0]
    num = re.search(r'#\s+(\d+)\.', header).group(1)
    
    code_blocks = re.findall(r'```(?:javascript|text|bash)?\n(.*?)```', sec, flags=re.DOTALL)
    for i, cb in enumerate(code_blocks):
        clean_lines = [l.strip() for l in cb.splitlines() if l.strip() and not l.strip().startswith('//')]
        if clean_lines:
            sample = clean_lines[0]
            sample_norm = re.sub(r'\s+', ' ', sample)
            if sample_norm not in plain_norm:
                print(f'Section {num} - snippet {i+1} NOT found: "{sample}"')
                missing_count += 1

print(f"Audit completed. Missing snippets: {missing_count}")
