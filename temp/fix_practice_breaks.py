import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'Code/Chapter-03-Operators-Expressions.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Add .practice-item style
practice_css = """    .practice-item {
      page-break-inside: avoid !important;
      break-inside: avoid !important;
      margin-bottom: 8px;
      padding: 8px 12px;
      background: #f8fafc;
      border-left: 3px solid #0284c7;
      border-radius: 4px;
    }"""

if '.practice-item {' not in text:
    text = text.replace('.study-card {', practice_css + '\n\n    .study-card {')

# Replace the inline styled divs in practice set with .practice-item
text = text.replace('<div style="margin-bottom: 8px; padding: 8px 12px; background: #f8fafc; border-left: 3px solid #0284c7; border-radius: 4px;">', '<div class="practice-item">')
text = text.replace('<div style="margin-bottom: 6px; padding: 8px 12px; background: #f8fafc; border-left: 3px solid #0284c7; border-radius: 4px;">', '<div class="practice-item">')

# Also ensure .practice-item is added to @media print
text = text.replace('.study-card {', '.study-card, .practice-item {')

with open(r'Code/Chapter-03-Operators-Expressions.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Practice items updated with page-break-inside: avoid!")
