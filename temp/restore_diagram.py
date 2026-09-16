import sys

sys.stdout.reconfigure(encoding='utf-8')

exact_diagram = """                  Program
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
    else if          else"""

# 1. Update temp/ch-4.md
with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-4.md', 'r', encoding='utf-8') as f:
    md_text = f.read()

# Replace between '# 4.42 Control Flow-এর Complete Picture' and 'আর specific values হলে:'
idx_md_start = md_text.find('# 4.42 Control Flow-এর Complete Picture')
idx_md_end = md_text.find('আর specific values হলে:')

if idx_md_start != -1 and idx_md_end != -1:
    section_part = md_text[idx_md_start:idx_md_end]
    new_section_part = f"""# 4.42 Control Flow-এর Complete Picture

এখন পুরো Chapter-এর concept একসাথে:

```text
{exact_diagram}
```

"""
    md_text = md_text[:idx_md_start] + new_section_part + md_text[idx_md_end:]
    with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-4.md', 'w', encoding='utf-8') as f:
        f.write(md_text)
    print("Restored exact diagram in temp/ch-4.md!")
else:
    print("Could not find section in ch-4.md!")

# 2. Update Code/Chapter-04-Control-Flow-Decision-Making.html
with open(r'Code/Chapter-04-Control-Flow-Decision-Making.html', 'r', encoding='utf-8') as f:
    html_text = f.read()

idx_html_start = html_text.find('<span class="badge-num">4.42</span>')
idx_html_end = html_text.find('<span class="tag-label purple">SWITCH - CASE FLOW</span>')

if idx_html_start != -1 and idx_html_end != -1:
    card_part = html_text[idx_html_start:idx_html_end]
    new_card_part = f"""<span class="badge-num">4.42</span> Control Flow-এর Complete Picture</div>
      <p class="text-p">এখন পুরো Chapter-এর concept একসাথে:</p>
      <span class="tag-label cyan">IF - ELSE IF - ELSE FLOW</span>
      <div class="ascii-tree-container">{exact_diagram}</div>

      """
    html_text = html_text[:idx_html_start] + new_card_part + html_text[idx_html_end:]
    with open(r'Code/Chapter-04-Control-Flow-Decision-Making.html', 'w', encoding='utf-8') as f:
        f.write(html_text)
    print("Restored exact diagram in Chapter-04-Control-Flow-Decision-Making.html!")
else:
    print("Could not find section in HTML!")
