import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open(r'Code/Chapter-04-Control-Flow-Decision-Making.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("File size:", len(text))
print(r"Count of \n:", text.count(r'\n'))
print(r'Count of \":', text.count(r'\"'))

idx = text.find('@media print')
if idx != -1:
    print("--- Print CSS ---")
    print(text[idx:idx+600])

idx_page = text.find('@page')
if idx_page != -1:
    print("--- @page CSS ---")
    print(text[idx_page:idx_page+200])
else:
    print("No @page found!")
