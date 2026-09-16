import re
import sys
import html

sys.stdout.reconfigure(encoding='utf-8')

# 1. Read source markdown
with open(r'temp/ch-9.md', 'r', encoding='utf-8') as f:
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
        ('STRING_TMPL', r'`(?:\\.|[^`\\])*`'),
        ('STRING_DBL', r'"(?:\\.|[^"\\])*"'),
        ('STRING_SGL', r"'(?:\\.|[^'\\])*'"),
        ('KEYWORD', r'\b(?:for|while|do|break|continue|if|else|let|const|var|function|return|switch|case|default|of|in|new|typeof|try|catch|finally|throw|class|extends|await|async|yield)\b'),
        ('BOOL_NULL', r'\b(?:true|false|null|undefined|NaN)\b'),
        ('BUILTIN', r'\b(?:console|Math|Array|Object|String|Number|Boolean|parseInt|parseFloat|prompt|alert)\b'),
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
        elif kind in ('STRING_TMPL', 'STRING_DBL', 'STRING_SGL'):
            out.append(f'<span class="syn-str">{esc}</span>')
        elif kind == 'KEYWORD':
            out.append(f'<span class="syn-kw">{esc}</span>')
        elif kind == 'BOOL_NULL':
            out.append(f'<span class="syn-bool">{esc}</span>')
        elif kind == 'BUILTIN':
            out.append(f'<span class="syn-fn">{esc}</span>')
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
            lang = stripped[3:].strip()
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
            if "Real-life" in last_subheading or "Example" in last_subheading:
                out_html.append(f'<div class="sub-badge">💡 {inline_format(last_subheading)}</div>')
            elif "Output" in last_subheading:
                # Handled together with next code block
                pass
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
            if txt.startswith("⚠️") or "Warning" in txt or "সতর্কতা" in txt:
                out_html.append(f'<div class="warn-box">{inline_format(txt)}</div>')
            elif "মনে রাখবে" in txt or "গুরুত্বপূর্ণ" in txt:
                out_html.append(f'<div class="memory-box">{inline_format(txt)}</div>')
            else:
                out_html.append(f'<p class="text-p">{inline_format(txt)}</p>')

        elif b_type == 'table':
            out_html.append(render_table(b[1]))

        elif b_type == 'code':
            lang = b[1].lower()
            raw_code = b[2]

            # Detect ASCII trees / text diagrams
            is_ascii = any(c in raw_code for c in ['├──', '└──', '│', '──', '┌', '└', '↓', '→', '▲']) or (lang == 'text' and not last_subheading.startswith("Output") and ("🛒" in raw_code or "Index:" in raw_code or "Shopping Cart" in raw_code))
            
            if is_ascii:
                out_html.append(f"""<div class="ascii-tree-container">{html.escape(raw_code)}</div>""")
            elif last_subheading and "Output" in last_subheading:
                out_html.append(f"""<div class="code-box output-box">
  <div class="code-top"><span class="out-label">CONSOLE OUTPUT</span></div>
  <pre>{html.escape(raw_code)}</pre>
</div>""")
                last_subheading = ""
            elif lang in ('javascript', 'js'):
                hl_code = highlight_js(raw_code)
                code_title = f"{sec_num} JavaScript" if sec_num else "JavaScript"
                out_html.append(f"""<div class="code-box">
  <div class="code-top"><span>{code_title}</span><span>Run</span></div>
  <pre>{hl_code}</pre>
</div>""")
            else:
                out_html.append(f"""<div class="code-box">
  <div class="code-top"><span>Text</span></div>
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
      background: #ffffff;
      color: #0369a1;
      font-weight: 800;
      font-size: 13px;
      padding: 2px 8px;
      border-radius: 5px;
      font-family: var(--font-heading);
    }
    .banner-title {
      font-family: var(--font-heading);
      font-size: 17px;
      font-weight: 800;
      letter-spacing: -0.3px;
      text-transform: uppercase;
    }
    .banner-sub {
      font-size: 11.5px;
      font-weight: 600;
      color: #e0f2fe;
      margin-bottom: 8px;
      letter-spacing: 0.5px;
    }
    .meta-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      background: rgba(15, 23, 42, 0.3);
      padding: 6px 10px;
      border-radius: 6px;
      border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .meta-item {
      display: flex;
      flex-direction: column;
    }
    .meta-label {
      font-size: 8.5px;
      text-transform: uppercase;
      color: #93c5fd;
      font-weight: 700;
      letter-spacing: 0.5px;
    }
    .meta-val {
      font-size: 10.5px;
      font-weight: 600;
      color: #ffffff;
    }

    /* Part Banner */
    .part-banner {
      background: #e0f2fe;
      color: #0369a1;
      font-family: var(--font-heading);
      font-size: 12px;
      font-weight: 800;
      padding: 6px 12px;
      border-radius: 6px;
      margin: 12px 0 8px 0;
      border-left: 4px solid #0284c7;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      page-break-after: avoid !important;
      break-after: avoid !important;
    }

    /* Study Cards */
    .study-card {
      background: var(--bg-card);
      border: 1px solid var(--border-card);
      border-left: 4px solid #0284c7;
      border-radius: 6px;
      padding: 10px 14px;
      margin-bottom: 8px;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .card-title {
      font-family: var(--font-heading);
      font-size: 12.5px;
      font-weight: 700;
      color: var(--navy-deep);
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .badge-num {
      background: #0284c7;
      color: white;
      font-size: 10px;
      font-weight: 700;
      padding: 1px 7px;
      border-radius: 4px;
      font-family: var(--font-code);
    }
    .section-subhead {
      font-family: var(--font-heading);
      font-size: 11.5px;
      font-weight: 700;
      color: #1e293b;
      margin: 6px 0 3px 0;
    }
    .sub-badge {
      display: inline-block;
      font-size: 9.5px;
      font-weight: 700;
      color: #0369a1;
      background: #e0f2fe;
      padding: 1px 6px;
      border-radius: 4px;
      margin: 4px 0 2px 0;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }
    .text-p {
      font-size: 11px;
      color: #334155;
      margin-bottom: 4px;
      line-height: 1.5;
    }
    .bullet-list {
      margin: 3px 0 6px 18px;
      color: #334155;
      font-size: 11px;
      line-height: 1.45;
    }
    .bullet-list li {
      margin-bottom: 2px;
    }

    /* Highlight Callouts */
    .def-box {
      background: #f0f9ff;
      border-left: 3px solid #0284c7;
      padding: 5px 10px;
      border-radius: 4px;
      margin: 4px 0 6px 0;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }
    .def-text {
      font-size: 11px;
      font-weight: 600;
      color: #0369a1;
      line-height: 1.4;
    }
    .memory-box {
      background: #fefce8;
      border-left: 3px solid #eab308;
      padding: 5px 10px;
      border-radius: 4px;
      margin: 4px 0 6px 0;
      font-size: 11px;
      font-weight: 600;
      color: #854d0e;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }
    .warn-box {
      background: #fff1f2;
      border-left: 3px solid #f43f5e;
      padding: 5px 10px;
      border-radius: 4px;
      margin: 4px 0 6px 0;
      font-size: 11px;
      font-weight: 600;
      color: #9f1239;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }

    /* Tables */
    .table-wrap {
      margin: 5px 0 6px 0;
      overflow-x: auto;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 10px;
      text-align: left;
    }
    th {
      background: #0f172a;
      color: #ffffff;
      padding: 4px 8px;
      font-weight: 600;
      font-family: var(--font-heading);
      border: 1px solid #1e293b;
    }
    td {
      padding: 4px 8px;
      border: 1px solid #e2e8f0;
      color: #334155;
    }
    tr:nth-child(even) {
      background: #f8fafc;
    }

    /* Code Blocks */
    .code-box {
      background: #0f172a;
      border: 1px solid #1e293b;
      border-radius: 6px;
      margin: 4px 0 6px 0;
      overflow: hidden;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }
    .code-top {
      background: #1e293b;
      color: #94a3b8;
      font-size: 9px;
      font-weight: 600;
      padding: 2px 10px;
      display: flex;
      justify-content: space-between;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      font-family: var(--font-heading);
    }
    .output-box {
      border: 1px solid #334155;
    }
    .output-box .code-top {
      background: #0f172a;
      border-bottom: 1px solid #1e293b;
    }
    .out-label {
      color: #38bdf8;
      font-weight: 700;
    }
    pre {
      font-family: var(--font-code) !important;
      font-size: 10.5px;
      line-height: 1.4;
      padding: 6px 10px;
      color: #e2e8f0;
      white-space: pre-wrap !important;
      word-break: break-word !important;
      overflow-x: hidden !important;
      margin: 0;
    }
    code {
      font-family: var(--font-code) !important;
      font-size: 10px;
      background: #f1f5f9;
      color: #0284c7;
      padding: 1px 4px;
      border-radius: 3px;
      border: 1px solid #e2e8f0;
    }
    pre code {
      background: transparent;
      color: inherit;
      padding: 0;
      border: none;
      font-size: inherit;
    }

    /* Syntax Highlighting */
    .syn-kw { color: #38bdf8; font-weight: 600; }
    .syn-fn { color: #f472b6; }
    .syn-str { color: #34d399; }
    .syn-num { color: #fbbf24; }
    .syn-com { color: #64748b; font-style: italic; }
    .syn-op { color: #a78bfa; }
    .syn-bool { color: #f59e0b; font-weight: 600; }

    .ascii-tree-container {
      background: #0f172a;
      border: 1px solid #1e293b;
      border-radius: 6px;
      padding: 6px 10px;
      color: #38bdf8;
      font-family: 'Courier New', Consolas, monospace !important;
      font-size: 10.5px;
      line-height: 1.35;
      white-space: pre !important;
      overflow-x: auto;
      margin: 4px 0;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
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
splits = re.split(r'\n(?=#\s+9\.\d+\s+)', raw_md)
opening_md = splits[0]
numbered_secs = splits[1:89] # 9.1 to 9.88

sec89_and_after = splits[89] # 9.89 and post sections
post_splits = re.split(r'\n(?=#\s+[🔥🧠📝🎯])', sec89_and_after)
sec89_md = post_splits[0]
project_cart_md = post_splits[1]
project_result_md = post_splits[2]
project_search_md = post_splits[3]
core_concepts_md = post_splits[4]
practice_set_md = post_splits[5]
final_summary_md = post_splits[6]

all_secs = numbered_secs + [sec89_md]

# Part definitions: (trigger_sec_num, banner_text)
PART_TRIGGERS = {
    1: "Part 01 — Array Fundamentals, Creation, Indexing & Basic Mutation (9.1 – 9.17)",
    18: "Part 02 — Looping, Searching & Slicing vs Splicing (9.18 – 9.35)",
    36: "Part 03 — Reversal, Sorting & Functional Iteration — forEach, map, filter (9.36 – 9.48)",
    49: "Part 04 — Advanced Search & Aggregation — find, some, every, reduce (9.49 – 9.57)",
    58: "Part 05 — Modern Syntax — Destructuring, Spread, Rest & Memory References (9.58 – 9.74)",
    75: "Part 06 — Advanced Methods, Constructors & Ecosystem Reference (9.75 – 9.89)",
}

# Start building HTML
html_parts = []
html_parts.append(f"""<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>JS Master Study Documentation — Chapter 09: Arrays &amp; Modern Collections</title>
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
      <div class="banner-sub">CHAPTER 09: ARRAYS &amp; MODERN COLLECTIONS</div>
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">Total Sections</div>
          <div class="meta-val">89 Modules + 3 Projects</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Curriculum Part</div>
          <div class="meta-val">Part 04 — Core Data Structures (2/3)</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Core Mechanics</div>
          <div class="meta-val">Indexing, Mutability, Iteration &amp; FP</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Reference Standard</div>
          <div class="meta-val">ECMAScript 2026 / V8 Runtime</div>
        </div>
      </div>
    </header>

    <!-- Chapter Opening Statement (Page 1 Balance) -->
    <div class="study-card" style="border-left: 4px solid var(--blue-accent); background: #f8fafc; padding: 10px 14px; margin-bottom: 8px;">
      <h2 style="font-size: 13px; color: var(--navy-mid); margin-bottom: 4px;">Arrays — একসাথে অনেক Data সংরক্ষণ</h2>
      <p class="text-p">JavaScript-এর সবচেয়ে গুরুত্বপূর্ণ data structures-এর একটি হলো <strong>Array</strong>। এতদিন আমরা একটি variable-এ একটি value রাখতাম:</p>
      <div class="code-box" style="margin: 4px 0;">
        <div class="code-top"><span>JavaScript</span><span>Single Value</span></div>
        <pre><span class="syn-kw">let</span> name = <span class="syn-str">"Shariar"</span>;</pre>
      </div>
      <p class="text-p">কিন্তু ধরো ১০০ জন student-এর নাম রাখতে হবে। আলাদা ১০০টা variable বানানো practical নয়। তখন আমরা Array ব্যবহার করব:</p>
      <div class="code-box" style="margin: 4px 0;">
        <div class="code-top"><span>JavaScript</span><span>Multiple Values Array</span></div>
        <pre><span class="syn-kw">let</span> students = [
    <span class="syn-str">"Shariar"</span>,
    <span class="syn-str">"Rahim"</span>,
    <span class="syn-str">"Karim"</span>,
    <span class="syn-str">"Sakib"</span>
];</pre>
      </div>
    </div>
""")

# Render all 89 numbered sections
for idx, sec_text in enumerate(all_secs, start=1):
    if idx in PART_TRIGGERS:
        html_parts.append(f'    <div class="part-banner">{PART_TRIGGERS[idx]}</div>\n')

    lines = sec_text.strip().split('\n')
    header_line = lines[0].strip()
    body_lines = lines[1:]

    m = re.match(r'^#\s+(9\.\d+)\s+(.*)$', header_line)
    if m:
        sec_num, sec_title = m.group(1), m.group(2)
    else:
        sec_num, sec_title = f"9.{idx}", header_line.lstrip('#').strip()

    card_style = ""
    badge_style = ""
    if "Table" in sec_title or "গুরুত্বপূর্ণ" in sec_title or "Real-life" in sec_title:
        card_style = ' style="border-left: 4px solid #0284c7; background: #ffffff;"'
        badge_style = ' style="background: #0284c7;"'

    rendered_body = parse_section_body('\n'.join(body_lines), sec_num)

    html_parts.append(f"""    <!-- {sec_num} -->
    <div class="study-card"{card_style}>
      <div class="card-title"><span class="badge-num"{badge_style}>{sec_num}</span> {inline_format(sec_title)}</div>
{rendered_body}
    </div>
""")

# Part 07: Real-Life Mini Projects, Core Concepts, Practice Lab & Summary
html_parts.append('    <div class="part-banner">Part 07 — Real-Life Mini Projects, Core Concepts, Practice Lab &amp; Summary</div>\n')

# 1. Mini Project: Shopping Cart
cart_body = parse_section_body(re.sub(r'^#\s+🔥\s+Real-life Mini Project\s+—\s+Shopping Cart', '', project_cart_md).strip())
html_parts.append(f"""    <!-- Mini Project: Shopping Cart -->
    <div class="study-card" style="border-left: 4px solid #10b981; background: #f0fdf4;">
      <div class="card-title"><span class="badge-num" style="background: #059669;">PROJECT 1</span> 🔥 Real-life Mini Project — Shopping Cart</div>
{cart_body}
    </div>
""")

# 2. Mini Project: Student Result
result_body = parse_section_body(re.sub(r'^#\s+🔥\s+Real-life Mini Project\s+—\s+Student Result', '', project_result_md).strip())
html_parts.append(f"""    <!-- Mini Project: Student Result -->
    <div class="study-card" style="border-left: 4px solid #10b981; background: #f0fdf4;">
      <div class="card-title"><span class="badge-num" style="background: #059669;">PROJECT 2</span> 🔥 Real-life Mini Project — Student Result</div>
{result_body}
    </div>
""")

# 3. Mini Project: Search Products
search_body = parse_section_body(re.sub(r'^#\s+🔥\s+Real-life Mini Project\s+—\s+Search Products', '', project_search_md).strip())
html_parts.append(f"""    <!-- Mini Project: Search Products -->
    <div class="study-card" style="border-left: 4px solid #10b981; background: #f0fdf4;">
      <div class="card-title"><span class="badge-num" style="background: #059669;">PROJECT 3</span> 🔥 Real-life Mini Project — Search Products</div>
{search_body}
    </div>
""")

# 4. Critical Concepts
concept_body = parse_section_body(re.sub(r'^#\s+🧠\s+Chapter 9\s+—\s+সবচেয়ে গুরুত্বপূর্ণ Concepts', '', core_concepts_md).strip())
html_parts.append(f"""    <!-- Chapter 9 Core Concepts -->
    <div class="study-card" style="border-left: 4px solid #ef4444;">
      <div class="card-title"><span class="badge-num" style="background: #dc2626;">CORE CONCEPTS</span> 🧠 Chapter 9 — সবচেয়ে গুরুত্বপূর্ণ Concepts</div>
{concept_body}
    </div>
""")

# 5. Practice Set
html_parts.append("""    <!-- Practice Set -->
    <div class="study-card" style="border-left: 4px solid #0284c7;">
      <div class="card-title"><span class="badge-num">PRACTICE LAB</span> 📝 Chapter 9 — Practice Set</div>
""")

# Parse Practice Problems
probs = re.split(r'\n(?=##\s+Practice\s+\d+)', practice_set_md.replace('# 📝 Chapter 9 — Practice Set', ''))
for p in probs:
    if not p.strip():
        continue
    p_lines = p.strip().split('\n')
    prob_title = p_lines[0].replace('##', '').strip()
    prob_body = '\n'.join(p_lines[1:])
    rendered_prob = parse_section_body(prob_body)
    html_parts.append(f"""      <div class="practice-item" style="background: white; border: 1px solid var(--border-card); border-left: 4px solid var(--blue-accent); margin-bottom: 8px;">
        <h4 style="font-size: 12px; font-weight: 700; color: var(--navy-mid); margin-bottom: 3px;">{inline_format(prob_title)}</h4>
{rendered_prob}
      </div>""")

html_parts.append("    </div>\n")

# 6. Final Summary, Top 8 Methods & Next Chapter Preview
summary_text = re.sub(r'^#\s+🎯\s+Chapter 9 Final Summary', '', final_summary_md).strip()
parts_p1 = re.split(r'\n(?=##\s+🚀\s+Chapter 9)', summary_text)
summary_overview_md = parts_p1[0].strip()

parts_p2 = re.split(r'\n(?=এরপর\s+\*\*Chapter 10|\*\*Chapter 10)', parts_p1[1]) if len(parts_p1) > 1 else ["", ""]
top8_md = parts_p2[0].strip()
next_preview_md = parts_p2[1].strip() if len(parts_p2) > 1 else ""

rendered_overview = parse_section_body(summary_overview_md)
html_parts.append(f"""    <!-- Chapter 9 Final Summary Overview -->
    <div class="study-card" style="border-left: 4px solid #8b5cf6; background: #faf5ff;">
      <div class="card-title"><span class="badge-num" style="background: #7c3aed;">SUMMARY</span> 🎯 Chapter 9 Final Summary — এক নজরে Array</div>
{rendered_overview}
    </div>
""")

if top8_md:
    rendered_top8 = parse_section_body(re.sub(r'^##\s+🚀\s+Chapter 9-এর সবচেয়ে গুরুত্বপূর্ণ ৮টি', '', top8_md).strip())
    html_parts.append(f"""    <!-- Chapter 9 Top 8 Methods -->
    <div class="study-card" style="border-left: 4px solid #f59e0b; background: #fffbeb;">
      <div class="card-title"><span class="badge-num" style="background: #d97706;">TOP 8</span> 🚀 Chapter 9-এর সবচেয়ে গুরুত্বপূর্ণ ৮টি Method</div>
{rendered_top8}
    </div>
""")

if next_preview_md:
    html_parts.append(f"""    <!-- Next Chapter Preview -->
    <div class="study-card" style="border-left: 4px solid #0284c7; background: #f0f9ff;">
      <div class="card-title"><span class="badge-num">NEXT CHAPTER</span> 🚀 Chapter 10 Preview — Objects</div>
      <p class="text-p" style="font-size: 12px; line-height: 1.6; color: #0c4a6e;">
        {inline_format(next_preview_md)}
      </p>
    </div>
""")

html_parts.append("""  </div>
</body>
</html>
""")

output_html = '\n'.join(html_parts)

# Write HTML file
target_file = r'Code/Chapter-09-Arrays.html'
with open(target_file, 'w', encoding='utf-8') as f:
    f.write(output_html)

print(f"Generated {target_file} successfully! Total lines: {len(output_html.splitlines())}")
