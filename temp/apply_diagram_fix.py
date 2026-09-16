import sys

sys.stdout.reconfigure(encoding='utf-8')

new_diagram = """                         Program
                            │
                            ▼
                    ┌───────────────┐
                    │  Condition?   │
                    └───────┬───────┘
                            │
              ┌─────────────┴─────────────┐
          [ True ]                    [ False ]
              │                           │
              ▼                           ▼
       ┌──────────────┐         ┌───────────────────┐
       │   if Block   │         │ Another Condition?│
       │  (Executes)  │         │    (else if)      │
       └──────┬───────┘         └─────────┬─────────┘
              │                           │
              │             ┌─────────────┴─────────────┐
              │         [ True ]                    [ False ]
              │             │                           │
              │             ▼                           ▼
              │     ┌───────────────┐            ┌──────────────┐
              │     │ else if Block │            │  else Block  │
              │     │  (Executes)   │            │  (Fallback)  │
              │     └───────┬───────┘            └──────┬───────┘
              │             │                           │
              └─────────────┴─────────────┬─────────────┘
                                          │
                                          ▼
                                   Program Continues"""

# 1. Update temp/ch-4.md
with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-4.md', 'r', encoding='utf-8') as f:
    md_text = f.read()

old_md_diagram = """```text
                  Program
                     ↓
                 Condition?
                /          \\
             true          false
              ↓              ↓
            if            else
              ↓
       Another condition?
          /          \\
       true          false
        ↓              ↓
    else if          else
```"""

if old_md_diagram in md_text:
    md_text = md_text.replace(old_md_diagram, f"```text\n{new_diagram}\n```")
    print("Updated ch-4.md successfully!")
else:
    # Try flexible matching
    import re
    md_text = re.sub(
        r'```text\s+Program\s+↓\s+Condition\?.*?' + re.escape('else if          else') + r'\s+```',
        f"```text\n{new_diagram}\n```",
        md_text,
        flags=re.DOTALL
    )
    print("Updated ch-4.md via regex!")

with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-4.md', 'w', encoding='utf-8') as f:
    f.write(md_text)

# 2. Update Code/Chapter-04-Control-Flow-Decision-Making.html
with open(r'Code/Chapter-04-Control-Flow-Decision-Making.html', 'r', encoding='utf-8') as f:
    html_text = f.read()

# Find the ascii-tree-container under 4.42
old_html_pattern = r'<span class="tag-label cyan">IF - ELSE IF - ELSE FLOW</span>\s*<div class="ascii-tree-container">.*?</div>'
new_html_block = f'<span class="tag-label cyan">IF - ELSE IF - ELSE FLOW</span>\n      <div class="ascii-tree-container">{new_diagram}</div>'

import re
html_text = re.sub(old_html_pattern, new_html_block, html_text, flags=re.DOTALL)

with open(r'Code/Chapter-04-Control-Flow-Decision-Making.html', 'w', encoding='utf-8') as f:
    f.write(html_text)

print("Updated Chapter-04-Control-Flow-Decision-Making.html successfully!")
