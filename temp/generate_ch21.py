import re
import sys
import html
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

# 1. Read source markdown
with open(r'temp/ch-21.md', 'r', encoding='utf-8') as f:
    raw_md = f.read().replace('\r\n', '\n').replace('\r', '\n')

def inline_format(text):
    if not text:
        return ''
    text = html.escape(text)
    # Bold + Code
    text = re.sub(r'\*\*`([^`]+)`\*\*', r'<strong><code>\1</code></strong>', text)
    text = re.sub(r'`\*\*([^*]+)\*\*`', r'<strong><code>\1</code></strong>', text)
    # Bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Italic
    text = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', text)
    return text

def highlight_js(code_str):
    token_spec = [
        ('COMMENT_MULTI', r'/\*[\s\S]*?\*/'),
        ('COMMENT_LINE', r'//.*$'),
        ('REGEX_LIT', r'/(?:\\/|[^\n\r/])+/[gimsuy]*'),
        ('STRING_TMPL', r'`(?:\\.|[^`\\])*`'),
        ('STRING_DBL', r'"(?:\\.|[^"\\])*"'),
        ('STRING_SGL', r"'(?:\\.|[^'\\])*'"),
        ('KEYWORD', r'\b(?:for|while|do|break|continue|if|else|let|const|var|function|return|switch|case|default|of|in|new|typeof|delete|this|super|class|extends|static|instanceof|try|catch|finally|throw|await|async|yield|debugger|import|export|from|as|require|module|exports)\b'),
        ('BOOL_NULL', r'\b(?:true|false|null|undefined|NaN)\b'),
        ('DOM_BUILTIN', r'\b(?:console|window|document|Math|Object|Array|Date|JSON|Promise|Error|Response|Request|Headers)\b'),
        ('DOM_METHOD', r'\b(?:setTimeout|clearTimeout|setInterval|clearInterval|queueMicrotask|fetch|then|catch|finally|resolve|reject|all|allSettled|race|any|json|text|blob|log|error|warn|info|push|map|filter|reduce|addEventListener)\b'),
        ('NUMBER', r'\b\d+(?:\.\d+)?\b'),
        ('OTHER', r'[^\s\w]+|\w+|\s+'),
    ]
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
    
    out = []
    for mo in re.finditer(tok_regex, code_str, flags=re.MULTILINE):
        kind = mo.lastgroup
        val = mo.group()
        esc = html.escape(val)
        if kind in ('COMMENT_MULTI', 'COMMENT_LINE'):
            out.append(f'<span class="syn-com">{esc}</span>')
        elif kind == 'REGEX_LIT':
            out.append(f'<span class="syn-regex">{esc}</span>')
        elif kind in ('STRING_TMPL', 'STRING_DBL', 'STRING_SGL'):
            out.append(f'<span class="syn-str">{esc}</span>')
        elif kind == 'KEYWORD':
            out.append(f'<span class="syn-kw">{esc}</span>')
        elif kind == 'BOOL_NULL':
            out.append(f'<span class="syn-bool">{esc}</span>')
        elif kind == 'DOM_BUILTIN':
            out.append(f'<span class="syn-fn">{esc}</span>')
        elif kind == 'DOM_METHOD':
            out.append(f'<span class="syn-op">{esc}</span>')
        elif kind == 'NUMBER':
            out.append(f'<span class="syn-num">{esc}</span>')
        else:
            out.append(esc)
    return ''.join(out)

def render_table(table_str):
    lines = [l.strip() for l in table_str.strip().splitlines() if l.strip()]
    if len(lines) < 2:
        return ''
    headers = [c.strip() for c in lines[0].strip('|').split('|')]
    rows = []
    for line in lines[2:]:
        cols = [c.strip() for c in line.strip('|').split('|')]
        rows.append(cols)
    th_html = ''.join(f'<th>{inline_format(h)}</th>' for h in headers)
    tr_html = []
    for row in rows:
        td_html = ''.join(f'<td>{inline_format(c)}</td>' for c in row)
        tr_html.append(f'<tr>{td_html}</tr>')
    return f"""<div class="table-wrap">
  <table>
    <thead><tr>{th_html}</tr></thead>
    <tbody>
      {''.join(tr_html)}
    </tbody>
  </table>
</div>"""

def parse_section_body(body_md, sec_num=""):
    lines = body_md.split('\n')
    blocks = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped or stripped == '---':
            i += 1
            continue

        if stripped.startswith('```'):
            fence_rest = stripped[3:].strip()
            lang = fence_rest.split()[0].lower() if fence_rest else ''
            code_lines = []
            i += 1
            while i < n and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1
            code_str = '\n'.join(code_lines)
            blocks.append(('code', lang, code_str))
            continue

        if stripped.startswith('|') and stripped.endswith('|'):
            table_lines = []
            while i < n and lines[i].strip().startswith('|') and lines[i].strip().endswith('|'):
                table_lines.append(lines[i].strip())
                i += 1
            blocks.append(('table', '\n'.join(table_lines)))
            continue

        if stripped.startswith('### ') or stripped.startswith('## '):
            level = 3 if stripped.startswith('### ') else 2
            h_text = stripped[4:] if level == 3 else stripped[3:]
            blocks.append(('subheading', h_text.strip()))
            i += 1
            continue

        if stripped.startswith('>'):
            quote_lines = []
            while i < n and lines[i].strip().startswith('>'):
                quote_lines.append(re.sub(r'^>\s*', '', lines[i].strip()))
                i += 1
            blocks.append(('quote', ' '.join(quote_lines)))
            continue

        if stripped.startswith('* ') or stripped.startswith('- ') or re.match(r'^\d+\.\s+', stripped):
            list_items = []
            while i < n and (lines[i].strip().startswith('* ') or lines[i].strip().startswith('- ') or re.match(r'^\d+\.\s+', lines[i].strip())):
                item_text = re.sub(r'^(?:[*+-]|\d+\.)\s+', '', lines[i].strip())
                list_items.append(item_text)
                i += 1
            blocks.append(('list', list_items))
            continue

        para_lines = []
        while i < n:
            l = lines[i]
            s = l.strip()
            if not s or s == '---' or s.startswith('```') or (s.startswith('|') and s.endswith('|')) or s.startswith('### ') or s.startswith('## ') or s.startswith('>') or s.startswith('* ') or s.startswith('- ') or re.match(r'^\d+\.\s+', s):
                break
            para_lines.append(s)
            i += 1
        if para_lines:
            blocks.append(('paragraph', ' '.join(para_lines)))

    out_html = []
    last_subheading = ""

    for b in blocks:
        b_type = b[0]

        if b_type == 'subheading':
            last_subheading = b[1]
            if "Real-Life" in last_subheading or "Real-life" in last_subheading or "Example" in last_subheading:
                out_html.append(f'<div class="sub-badge">💡 {inline_format(last_subheading)}</div>')
            elif "মনে রাখো" in last_subheading or "মনে রাখবে" in last_subheading or "গুরুত্বপূর্ণ" in last_subheading or "Important" in last_subheading or "কেন সমস্যা" in last_subheading:
                out_html.append(f'<div class="sub-badge" style="background:#fef9c3; color:#854d0e;">📌 {inline_format(last_subheading)}</div>')
            elif "Syntax" in last_subheading or "State" in last_subheading:
                out_html.append(f'<div class="sub-badge" style="background:#ede9fe; color:#6d28d9;">⚙️ {inline_format(last_subheading)}</div>')
            elif "Output" in last_subheading or "Expected" in last_subheading:
                pass
            elif last_subheading in ("❌ ভুল", "✅ সঠিক"):
                badge_bg = "#fee2e2" if "ভুল" in last_subheading else "#dcfce7"
                badge_color = "#991b1b" if "ভুল" in last_subheading else "#166534"
                out_html.append(f'<div class="sub-badge" style="background:{badge_bg}; color:{badge_color};">{inline_format(last_subheading)}</div>')
            else:
                out_html.append(f'<div class="section-subhead">{inline_format(last_subheading)}</div>')

        elif b_type == 'quote':
            out_html.append(f"""<div class="def-box">
  <div class="def-text">{inline_format(b[1])}</div>
</div>""")

        elif b_type == 'list':
            items = ''.join(f'<li>{inline_format(item)}</li>' for item in b[1])
            out_html.append(f'<ul class="bullet-list">{items}</ul>')

        elif b_type == 'paragraph':
            txt = b[1]
            if "Output:" in txt or txt.strip() == "Output:":
                continue
            if txt.startswith("⚠️") or "Warning" in txt or "সতর্কতা" in txt or "সমস্যা" in txt or "বিপদ" in txt or "Error" in txt or "ভুল" in txt:
                out_html.append(f'<div class="warn-box">{inline_format(txt)}</div>')
            elif "মনে রাখবে" in txt or "গুরুত্বপূর্ণ" in txt or "আয়ত্ত করবে" in txt or "মনে রাখো" in txt:
                out_html.append(f'<div class="memory-box">{inline_format(txt)}</div>')
            else:
                out_html.append(f'<p class="text-p">{inline_format(txt)}</p>')

        elif b_type == 'table':
            out_html.append(render_table(b[1]))

        elif b_type == 'code':
            lang = b[1].lower()
            raw_code = b[2]

            # Detect ASCII diagrams
            is_ascii = any(c in raw_code for c in ['├──', '└──', '│', '──', '┌', '└', '↓', '→', '▼', '▲', '┼', '---------------------']) or (lang == 'text' and any(k in raw_code.lower() for k in ["task 1", "order placed", "event loop", "call stack", "async javascript"]))
            
            if is_ascii:
                out_html.append(f"""<div class="ascii-tree-container">{html.escape(raw_code)}</div>""")
            elif last_subheading and ("Output" in last_subheading or "Expected" in last_subheading):
                out_html.append(f"""<div class="code-box output-box">
  <div class="code-top"><span class="out-label">CONSOLE OUTPUT</span></div>
  <pre>{html.escape(raw_code)}</pre>
</div>""")
                last_subheading = ""
            elif lang in ('javascript', 'js') or (not lang and any(k in raw_code for k in ['async ', 'await ', 'Promise', 'fetch(', 'setTimeout(', 'then(', 'catch(', 'console.log'])) or any(lang == m for m in ['settimeout', 'promise', 'async', 'await', 'try', 'queuemicrotask', 'setinterval', 'fetch', 'getdata', 'resolve', 'reject']):
                hl_code = highlight_js(raw_code)
                label = f"{last_subheading}" if (last_subheading and ".js" in last_subheading) else "JavaScript Async"
                code_title = f"{sec_num} {label}" if sec_num else label
                out_html.append(f"""<div class="code-box">
  <div class="code-top"><span>{code_title}</span><span>ES2026</span></div>
  <pre>{hl_code}</pre>
</div>""")
            else:
                out_html.append(f"""<div class="code-box output-box">
  <div class="code-top"><span class="out-label">OUTPUT / TEXT</span></div>
  <pre>{html.escape(raw_code)}</pre>
</div>""")

    return '\n'.join(out_html)

CSS = """
    :root {
      --navy-deep: #0f172a;
      --navy-mid: #1e293b;
      --navy-light: #334155;
      --blue-accent: #0284c7;
      --blue-light: #e0f2fe;
      --blue-dark: #0369a1;
      --emerald: #059669;
      --amber: #d97706;
      --rose: #e11d48;
      --purple: #7c3aed;
      --bg-page: #f8fafc;
      --bg-card: #ffffff;
      --border-card: #e2e8f0;
      --text-main: #0f172a;
      --text-muted: #475569;
      --font-code: 'Fira Code', monospace;
      --font-body: 'Hind Siliguri', sans-serif;
      --font-heading: 'Plus Jakarta Sans', sans-serif;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-page);
      font-family: var(--font-body);
      color: var(--text-main);
      line-height: 1.45;
      font-size: 11px;
      -webkit-font-smoothing: antialiased;
    }

    /* Top Sticky Action Bar */
    .action-bar {
      position: sticky;
      top: 0;
      z-index: 999;
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(8px);
      padding: 10px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #334155;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .brand-title {
      font-family: var(--font-heading);
      font-weight: 700;
      font-size: 13px;
      color: #f8fafc;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .print-btn {
      background: linear-gradient(135deg, #0284c7, #0369a1);
      color: #ffffff;
      border: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-family: var(--font-heading);
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
      box-shadow: 0 2px 6px rgba(2, 132, 199, 0.3);
    }
    .print-btn:hover {
      background: linear-gradient(135deg, #0369a1, #075985);
      transform: translateY(-1px);
    }

    /* Container */
    .doc-page {
      max-width: 860px;
      margin: 16px auto;
      background: white;
      padding: 24px 28px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.06);
      border-radius: 8px;
    }

    /* Master Banner */
    .master-banner {
      background: linear-gradient(135deg, #075985 0%, #0369a1 50%, #0284c7 100%);
      color: white;
      padding: 14px 18px;
      border-radius: 8px;
      margin-bottom: 10px;
      box-shadow: 0 4px 12px rgba(3, 105, 161, 0.2);
    }
    .banner-top {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 4px;
    }
    .banner-icon {
      background: rgba(255,255,255,0.18);
      border: 1px solid rgba(255,255,255,0.3);
      width: 26px;
      height: 26px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: var(--font-code);
      font-weight: 700;
      font-size: 11px;
    }
    .banner-title {
      font-family: var(--font-heading);
      font-size: 15px;
      font-weight: 800;
      letter-spacing: 0.3px;
    }
    .banner-sub {
      font-size: 10px;
      font-weight: 600;
      opacity: 0.95;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 8px;
    }
    .meta-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      background: rgba(15, 23, 42, 0.25);
      padding: 6px 10px;
      border-radius: 6px;
      border: 1px solid rgba(255,255,255,0.12);
    }
    .meta-item {
      display: flex;
      flex-direction: column;
    }
    .meta-label {
      font-size: 8px;
      text-transform: uppercase;
      opacity: 0.8;
      letter-spacing: 0.5px;
    }
    .meta-val {
      font-size: 9.5px;
      font-weight: 700;
    }

    /* Part Banner */
    .part-banner {
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
      color: #f8fafc;
      padding: 7px 12px;
      font-family: var(--font-heading);
      font-size: 11px;
      font-weight: 700;
      border-radius: 5px;
      margin-top: 10px;
      margin-bottom: 6px;
      border-left: 4px solid #0284c7;
      display: flex;
      align-items: center;
      justify-content: space-between;
      page-break-after: avoid !important;
      break-after: avoid !important;
    }

    /* Study Cards */
    .study-card {
      background: var(--bg-card);
      border: 1px solid var(--border-card);
      border-radius: 6px;
      padding: 8px 12px;
      margin-bottom: 6px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }
    .card-title {
      font-family: var(--font-heading);
      font-size: 12px;
      font-weight: 700;
      color: var(--navy-mid);
      margin-bottom: 5px;
      display: flex;
      align-items: center;
      gap: 6px;
      border-bottom: 1px solid #f1f5f9;
      padding-bottom: 3px;
    }
    .badge-num {
      background: var(--blue-accent);
      color: white;
      font-family: var(--font-code);
      font-size: 9px;
      padding: 1px 5px;
      border-radius: 4px;
      font-weight: 600;
    }

    /* Typography inside cards */
    .text-p {
      margin-bottom: 4px;
      color: #334155;
      font-size: 10.5px;
      line-height: 1.45;
    }
    .section-subhead {
      font-family: var(--font-heading);
      font-size: 10.5px;
      font-weight: 700;
      color: var(--navy-light);
      margin-top: 4px;
      margin-bottom: 3px;
      border-left: 2px solid var(--blue-accent);
      padding-left: 5px;
    }
    .sub-badge {
      display: inline-block;
      font-family: var(--font-heading);
      font-size: 9.5px;
      font-weight: 700;
      background: #e0f2fe;
      color: #0369a1;
      padding: 1px 6px;
      border-radius: 4px;
      margin-top: 4px;
      margin-bottom: 3px;
    }

    /* Definition / Note Boxes */
    .def-box {
      background: #f0fdf4;
      border-left: 3px solid #10b981;
      padding: 5px 8px;
      border-radius: 4px;
      margin: 4px 0;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }
    .def-text {
      font-size: 10px;
      font-weight: 600;
      color: #065f46;
    }
    .memory-box {
      background: #eff6ff;
      border-left: 3px solid #3b82f6;
      padding: 5px 8px;
      border-radius: 4px;
      margin: 4px 0;
      font-size: 10px;
      color: #1e40af;
      font-weight: 500;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }
    .warn-box {
      background: #fef2f2;
      border-left: 3px solid #ef4444;
      padding: 5px 8px;
      border-radius: 4px;
      margin: 4px 0;
      font-size: 10px;
      color: #991b1b;
      font-weight: 500;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }

    /* Lists */
    .bullet-list {
      margin: 3px 0 5px 14px;
      font-size: 10.5px;
      color: #334155;
      line-height: 1.4;
    }
    .bullet-list li {
      margin-bottom: 2px;
    }

    /* Tables */
    .table-wrap {
      overflow-x: auto;
      margin: 4px 0;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 9.5px;
      background: white;
    }
    th, td {
      border: 1px solid #cbd5e1;
      padding: 4px 6px;
      text-align: left;
    }
    th {
      background: #f1f5f9;
      color: #0f172a;
      font-weight: 700;
    }

    /* Code Blocks */
    .code-box {
      background: #0f172a;
      border-radius: 5px;
      margin: 4px 0;
      overflow: hidden;
      border: 1px solid #1e293b;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }
    .code-top {
      background: #1e293b;
      padding: 2px 8px;
      display: flex;
      justify-content: space-between;
      color: #94a3b8;
      font-family: var(--font-code);
      font-size: 8.5px;
      text-transform: uppercase;
      border-bottom: 1px solid #334155;
    }
    pre {
      font-family: var(--font-code);
      font-size: 9.5px;
      line-height: 1.35;
      padding: 6px 10px;
      color: #f8fafc;
      overflow-x: hidden !important;
      white-space: pre-wrap !important;
      word-break: break-word !important;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }
    code {
      font-family: var(--font-code);
      font-size: 9.5px;
      background: #f1f5f9;
      color: #0369a1;
      padding: 1px 3px;
      border-radius: 3px;
    }
    .output-box {
      background: #182234;
      border-left: 3px solid #10b981;
    }
    .out-label {
      color: #34d399;
      font-weight: 700;
    }

    /* Syntax Highlighting */
    .syn-kw { color: #f43f5e; font-weight: 600; }
    .syn-fn { color: #38bdf8; }
    .syn-str { color: #a3e635; }
    .syn-num { color: #fb923c; }
    .syn-com { color: #64748b; font-style: italic; }
    .syn-op { color: #38bdf8; }
    .syn-bool { color: #c084fc; font-weight: 600; }
    .syn-regex { color: #facc15; }

    /* ASCII Diagrams */
    .ascii-tree-container {
      background: #0f172a;
      color: #38bdf8;
      font-family: var(--font-code);
      font-size: 9px;
      line-height: 1.25;
      padding: 6px 10px;
      border-radius: 5px;
      margin: 4px 0;
      white-space: pre;
      overflow-x: auto;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
      border: 1px solid #1e293b;
    }

    /* Practice Items */
    .practice-item {
      page-break-inside: avoid !important;
      break-inside: avoid !important;
      margin-bottom: 6px;
      padding: 6px 10px;
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
        color: #0f172a;
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
        page-break-after: avoid !important;
        break-after: avoid !important;
      }
      .code-box, pre, .ascii-tree-container, .table-wrap, .def-box, .memory-box, .warn-box {
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      pre {
        overflow-x: hidden !important;
        white-space: pre-wrap !important;
        word-break: break-word !important;
      }
    }
"""

# Split sections
splits = re.split(r'\n(?=#\s+(?:.*?\b21\.\d+\b|🧠\s+Quick|📝\s+Practice|🎯\s+Chapter))', raw_md)

opening_md = splits[0]
numbered_secs = splits[1:56] # 21.1 to 21.55 (55 sections)
must_know_md = splits[56]    # 21.56
quick_cheat_md = splits[57]  # Quick Cheat Sheet
practice_set_md = splits[58] # Practice Set
final_mental_md = splits[59] # 🎯 Chapter 21 Final Mental Map

# Part definitions: (trigger_sec_num, banner_text)
PART_TRIGGERS = {
    1: "Part 01 — Asynchronous Foundations, Browser Runtime, Call Stack &amp; Event Loop (21.1 – 21.10)",
    11: "Part 02 — Promises Architecture: Creation, Lifecycle, Chaining &amp; Error Handling (21.11 – 21.23)",
    24: "Part 03 — Promise Combinators: Concurrency &amp; Parallel Execution (21.24 – 21.28)",
    29: "Part 04 — Modern Async/Await: Syntactic Sugar, Flow Control &amp; Loop Patterns (21.29 – 21.38)",
    39: "Part 05 — Engine Internals, Microtasks, Fetch API &amp; Production Architecture (21.39 – 21.55)",
}

# Start building HTML
html_parts = []
html_parts.append(f"""<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>JS Master Study Documentation — Chapter 21: Asynchronous JavaScript</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Hind+Siliguri:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
  <style>{CSS}</style>
</head>
<body>

  <!-- Sticky Top Print Nav -->
  <div class="action-bar">
    <div class="brand-title">
      <span style="color:#0284c7;">⚡</span> JS MASTER STUDY DOCUMENTATION
    </div>
    <button class="print-btn" onclick="window.print()">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
      Print / Save as PDF
    </button>
  </div>

  <div class="doc-page">

    <!-- Header Master Banner -->
    <header class="master-banner">
      <div class="banner-top">
        <div class="banner-icon">JS</div>
        <div class="banner-title">JavaScript Master Study Documentation</div>
      </div>
      <div class="banner-sub">CHAPTER 21: ASYNCHRONOUS JAVASCRIPT — EVENT LOOP, PROMISES, ASYNC/AWAIT &amp; FETCH API</div>
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">Total Sections</div>
          <div class="meta-val">56 Modules + Practice</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Curriculum Part</div>
          <div class="meta-val">Part 15 — Asynchronous Programming &amp; Concurrency</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Core Mechanics</div>
          <div class="meta-val">Event Loop, Microtasks, Promise &amp; async/await</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Reference Standard</div>
          <div class="meta-val">ECMAScript 2026 / WHATWG HTML Living Standard</div>
        </div>
      </div>
    </header>

    <!-- Chapter Opening Statement (Page 1 Balance) -->
    <div class="study-card" style="border-left: 4px solid var(--blue-accent); background: #f8fafc; padding: 8px 12px; margin-bottom: 6px;">
      <h2 style="font-size: 12px; color: var(--navy-mid); margin-bottom: 3px;">Asynchronous JavaScript — নন-ব্লকিং মডেল ও অ্যাসিনক্রোনাস আর্কিটেকচার</h2>
      <p class="text-p" style="font-size: 10px; margin-bottom: 3px;">JavaScript হলো একটি <strong>Single-Threaded</strong> ল্যাঙ্গুয়েজ, অর্থাৎ এটি একসাথে একটিমাত্র কাজ করতে পারে। কিন্তু বাস্তব অ্যাপ্লিকেশনে নেটওয়ার্ক রিকোয়েস্ট, সার্ভার থেকে ডাটা লোড, টাইমার বা ডেটাবেজ এক্সেসের মতো দীর্ঘস্থায়ী কাজের সময় ব্রাউজার যেন জমে (Freeze) না যায়, সেজন্য জাভাস্ক্রিপ্ট <strong>Non-blocking Asynchronous</strong> মডেল ব্যবহার করে।</p>
      <div class="def-box" style="margin: 2px 0; padding: 4px 6px;">
        <div class="def-text" style="font-size: 9px;">Call Stack (JS Engine) &nbsp;→&nbsp; Web APIs (Timer/Network) &nbsp;→&nbsp; Callback / Microtask Queue &nbsp;→&nbsp; Event Loop</div>
      </div>
      <p class="text-p" style="font-weight: 600; color: #0369a1; margin-top: 2px; font-size: 9.5px;">React, Next.js, Node.js কিংবা Express-এ API Integration ও Backend Communication-এর মূল চালিকাশক্তিই হলো Asynchronous JavaScript। 🔥</p>
    </div>
""")

# Render all 55 numbered sections (21.1 to 21.55)
for idx, sec_text in enumerate(numbered_secs, start=1):
    if idx in PART_TRIGGERS:
        html_parts.append(f'    <div class="part-banner">{PART_TRIGGERS[idx]}</div>\n')

    lines = sec_text.strip().split('\n')
    header_line = lines[0].strip()
    body_lines = lines[1:]

    m = re.search(r'\b(21\.\d+)\b\s*(.*)$', header_line)
    if m:
        sec_num, sec_title = m.group(1), m.group(2)
        sec_title = sec_title.strip('`* ')
    else:
        sec_num, sec_title = f"21.{idx}", header_line.lstrip('#').strip()

    card_style = ""
    badge_style = ""
    if "⚠️" in header_line or "ভুল" in sec_title or "Error" in sec_title or "Hell" in sec_title or "Mistake" in sec_title:
        card_style = ' style="border-left: 4px solid #ef4444; background: #ffffff;"'
        badge_style = ' style="background: #dc2626;"'
    elif "Mental Model" in sec_title or "Flow" in sec_title or "vs" in sec_title or "Mini Project" in sec_title or "Login" in sec_title or "Microtask" in sec_title or "Event Loop" in sec_title:
        card_style = ' style="border-left: 4px solid #0284c7; background: #ffffff;"'
        badge_style = ' style="background: #0284c7;"'

    # Strict Page 1 Balance: Section 21.1 Card must break cleanly before Section 21.2
    if idx == 1:
        if card_style:
            card_style = card_style[:-1] + ' page-break-after: always !important; break-after: page !important;"'
        else:
            card_style = ' style="page-break-after: always !important; break-after: page !important;"'

    rendered_body = parse_section_body('\n'.join(body_lines), sec_num)

    html_parts.append(f"""    <!-- {sec_num} -->
    <div class="study-card"{card_style}>
      <div class="card-title"><span class="badge-num"{badge_style}>{sec_num}</span> {inline_format(sec_title)}</div>
{rendered_body}
    </div>
""")

# Part 06: Must Know, Quick Cheat Sheet, Practice Lab & Mental Map
html_parts.append('    <div class="part-banner">Part 06 — Asynchronous Mastery: Must Know, Cheat Sheet, Practice Lab &amp; Mental Map</div>\n')

# 1. Must Know (21.56)
must_know_body = parse_section_body(re.sub(r'^#\s+🔥\s+21\.56\s+Must Know', '', must_know_md).strip())
html_parts.append(f"""    <!-- 21.56 Must Know -->
    <div class="study-card" style="border-left: 4px solid #ef4444; background: #ffffff;">
      <div class="card-title"><span class="badge-num" style="background: #dc2626;">MUST KNOW</span> 🔥 21.56 Must Know — Asynchronous JavaScript Core Pillars</div>
{must_know_body}
    </div>
""")

# 2. Quick Cheat Sheet
cheat_body = parse_section_body(re.sub(r'^#\s+🧠\s+Quick Cheat Sheet', '', quick_cheat_md).strip())
html_parts.append(f"""    <!-- Quick Cheat Sheet -->
    <div class="study-card" style="border-left: 4px solid #10b981; background: #f0fdf4;">
      <div class="card-title"><span class="badge-num" style="background: #059669;">CHEAT SHEET</span> 🧠 Quick Cheat Sheet — Callback, Promise &amp; Async/Await Syntax</div>
{cheat_body}
    </div>
""")

# 3. Practice Set
html_parts.append("""    <!-- Practice Set -->
    <div class="study-card" style="border-left: 4px solid #0284c7;">
      <div class="card-title"><span class="badge-num">PRACTICE LAB</span> 📝 Practice Set — 5 Asynchronous Coding Challenges</div>
""")

prob_blocks = re.split(r'\n(?=###\s+Practice\s+\d+)', practice_set_md.replace('# 📝 Practice Set', ''))
for pb in prob_blocks:
    if not pb.strip():
        continue
    pb_lines = pb.strip().split('\n')
    p_title = pb_lines[0].replace('###', '').strip()
    p_body = '\n'.join(pb_lines[1:])
    rendered_p = parse_section_body(p_body)
    html_parts.append(f"""      <div class="practice-item" style="background: white; border: 1px solid var(--border-card); border-left: 4px solid var(--blue-accent); margin-bottom: 8px;">
        <h4 style="font-size: 12px; font-weight: 700; color: var(--navy-mid); margin-bottom: 4px;">{inline_format(p_title)}</h4>
{rendered_p}
      </div>""")

html_parts.append("    </div>\n")

# 4. Final Mental Map & Summary
summary_text = re.sub(r'^#\s+🎯\s+Chapter 21 Final Mental Map', '', final_mental_md).strip()
rendered_summary = parse_section_body(summary_text)

html_parts.append(f"""    <!-- Final Mental Map -->
    <div class="study-card" style="border-left: 4px solid #8b5cf6; background: #faf5ff;">
      <div class="card-title"><span class="badge-num" style="background: #7c3aed;">SUMMARY</span> 🎯 Chapter 21 Final Mental Map — Asynchronous JavaScript Architecture</div>
{rendered_summary}
    </div>
""")

# Next Chapter Preview
html_parts.append("""    <!-- Next Chapter Preview -->
    <div class="study-card" style="border-left: 4px solid #0284c7; background: #f0f9ff;">
      <div class="card-title"><span class="badge-num">NEXT CHAPTER</span> 📘 Chapter 22 Preview — HTTP, API &amp; Fetch</div>
      <p class="text-p" style="font-size: 12px; line-height: 1.6; color: #0c4a6e;">
        পরবর্তী অধ্যায়ে আমরা শিখব <strong>HTTP Protocols, REST APIs, Request Headers, Status Codes (200, 201, 400, 401, 404, 500)</strong> এবং ব্রাউজারের আধুনিক <code>fetch()</code> API দিয়ে ফুল-স্ট্যাক নেটওয়ার্ক ইন্টারঅ্যাকশন ও এরর হ্যান্ডলিং কৌশল।
      </p>
    </div>
""")

html_parts.append("""  </div>
</body>
</html>
""")

output_html = '\n'.join(html_parts)

# Write HTML file
target_file = r'Code/Chapter-21-Asynchronous-JavaScript.html'
with open(target_file, 'w', encoding='utf-8') as f:
    f.write(output_html)

print(f"Generated {target_file} successfully! Total lines: {len(output_html.splitlines())}, characters: {len(output_html)}")
