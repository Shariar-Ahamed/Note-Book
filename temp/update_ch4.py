import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'Code/Chapter-04-Control-Flow-Decision-Making.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update print styles to match Chapter 1, 2, 3
old_print_css = """    @media print {
      body {
        background: white;
        font-size: 11.5px;
      }
      .action-bar { display: none !important; }
      .doc-page {
        max-width: 100% !important;
        margin: 0 !important;
        padding: 14mm 16mm !important;
        border: none !important;
        box-shadow: none !important;
      }
      .study-card {
        page-break-inside: avoid;
        break-inside: avoid;
        border: 1px solid #cbd5e1;
      }
      .part-banner {
        page-break-after: avoid;
        break-after: avoid;
      }
      .code-box, pre, .ascii-tree-container {
        page-break-inside: avoid;
        break-inside: avoid;
      }
    }"""

new_print_css = """    .practice-item {
      page-break-inside: avoid !important;
      break-inside: avoid !important;
      margin-bottom: 8px;
      padding: 8px 12px;
      background: #f8fafc;
      border-left: 3px solid #0284c7;
      border-radius: 4px;
    }

    @page {
      size: A4;
      margin: 8mm 10mm;
    }

    @media print {
      body {
        background: white;
        font-size: 11px;
      }
      .action-bar {
        display: none !important;
      }
      .doc-page {
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        box-shadow: none !important;
      }
      .study-card, .practice-item {
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        border: 1px solid #cbd5e1;
      }
      .part-banner {
        page-break-after: avoid;
        break-after: avoid;
      }
      .code-box, pre, .ascii-tree-container, .table-wrap, .def-box, .memory-box, .warn-box {
        page-break-inside: avoid;
        break-inside: avoid;
      }
      pre {
        overflow-x: hidden !important;
        white-space: pre-wrap !important;
        word-break: break-word !important;
      }
    }"""

if old_print_css in html:
    html = html.replace(old_print_css, new_print_css)
    print("Replaced print CSS cleanly!")
else:
    print("Exact match not found, replacing with regex...")
    html = re.sub(r'@media print\s*\{.*?\}\s*\}', new_print_css.strip(), html, flags=re.DOTALL)
    print("Replaced print CSS via regex!")

# 2. Add .practice-item class to coding practice problem divs
html = html.replace('<div style="margin-bottom: 10px; padding: 8px 12px; background: #f8fafc; border-left: 3px solid #0284c7; border-radius: 4px;">', '<div class="practice-item">')
html = html.replace('<div style="margin-bottom: 6px; padding: 8px 12px; background: #f8fafc; border-left: 3px solid #0284c7; border-radius: 4px;">', '<div class="practice-item">')

with open(r'Code/Chapter-04-Control-Flow-Decision-Making.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved updated Chapter 4 HTML file successfully!")
