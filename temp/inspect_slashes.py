import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'Code/Chapter-03-Operators-Expressions.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Check all backslash sequences
backslashes = set(re.findall(r'\\.', text))
print("All backslash sequences found in text:", backslashes)
