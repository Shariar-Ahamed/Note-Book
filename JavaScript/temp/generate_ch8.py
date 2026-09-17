import re
import sys
import html

sys.stdout.reconfigure(encoding='utf-8')

# 1. Read source markdown
with open(r'temp/ch-8.md', 'r', encoding='utf-8') as f:
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
            sub = b[1]
            if sub.lower() in ('output', 'output:', '**output**', 'result', 'result:'):
                out_html.append('<span class="tag-label amber">Output</span>')
            elif sub.lower() in ('code', 'code:'):
                out_html.append('<span class="tag-label purple">Code</span>')
            elif sub.lower() in ('syntax', 'syntax:'):
                out_html.append('<span class="tag-label purple">Syntax</span>')
            elif sub.lower() in ('example', 'example:'):
                out_html.append('<span class="tag-label green">Example</span>')
            elif 'real-life' in sub.lower():
                out_html.append('<span class="tag-label cyan">Real-Life Example</span>')
            elif 'সহজভাবে' in sub:
                out_html.append('<span class="tag-label cyan">সহজভাবে</span>')
            elif 'মনে রাখ' in sub:
                out_html.append('<span class="tag-label amber">🧠 মনে রাখার নিয়ম</span>')
            elif 'summary' in sub.lower():
                out_html.append('<span class="tag-label cyan">Summary</span>')
            else:
                out_html.append(f'<h4 style="font-size: 12px; font-weight: 700; color: var(--navy-mid); margin: 8px 0 4px 0;">{inline_format(sub)}</h4>')

        elif b_type == 'code':
            lang, code_str = b[1], b[2]
            if lang == 'javascript' or (not lang and ('let ' in code_str or 'const ' in code_str or 'console.log' in code_str or 'function ' in code_str or 'return ' in code_str or '["' in code_str)):
                top_label = "JavaScript"
                sub_title = "Code"
                if last_subheading and last_subheading.lower() not in ('output', 'output:', 'code', 'result', 'result:'):
                    sub_title = inline_format(last_subheading.replace('`', ''))
                out_html.append(f"""<div class="code-box">
  <div class="code-top"><span>{top_label}</span><span>{sub_title}</span></div>
  <pre>{highlight_js(code_str)}</pre>
</div>""")
            elif lang == 'text' or not lang:
                is_output = ('output' in last_subheading.lower()) or ('result' in last_subheading.lower()) or (code_str.strip() in ('true', 'false', '-1', '10', 'Java', 'Script', 'shariar', 'Hello', '75000'))
                has_diagram_chars = any(c in code_str for c in ('↓', '→', '┌', '└', '├', '│', '┴', '┬', '├──', '└──', '▲', '▼')) or ('Name:' in code_str and 'Email:' in code_str) or ('Product:' in code_str) or ('✅' in code_str)
                
                if is_output and not has_diagram_chars:
                    out_html.append(f'<div class="output-box">{html.escape(code_str.strip())}</div>')
                else:
                    out_html.append(f'<div class="ascii-tree-container">{html.escape(code_str.rstrip())}</div>')
            else:
                out_html.append(f"""<div class="code-box">
  <div class="code-top"><span>{lang.upper()}</span><span>Snippet</span></div>
  <pre>{html.escape(code_str)}</pre>
</div>""")

        elif b_type == 'table':
            out_html.append(render_table(b[1]))

        elif b_type == 'quote':
            out_html.append(f'<div class="def-box english" style="margin: 6px 0;"><strong>Core Definition:</strong> {inline_format(b[1])}</div>')

        elif b_type == 'list':
            items = ''.join(f'<li>{inline_format(item)}</li>' for item in b[1])
            out_html.append(f'<ul class="clean-list">{items}</ul>')

        elif b_type == 'paragraph':
            p_text = b[1]
            if p_text.startswith('**String** হলো') or p_text.startswith('**String Immutability** হলো') or p_text.startswith('**Template Literals** হলো'):
                out_html.append(f'<div class="def-box bangla">{inline_format(p_text)}</div>')
            elif p_text.startswith('**মনে রেখো:**') or p_text.startswith('**Note:**') or p_text.startswith('**Rule:**'):
                out_html.append(f'<div class="memory-box">{inline_format(p_text)}</div>')
            elif p_text.startswith('**ভুল:**') or p_text.startswith('**সতর্কতা:**') or p_text.startswith('**Warning:**') or p_text.startswith('⚠️') or p_text.startswith('Important —'):
                out_html.append(f'<div class="warn-box">{inline_format(p_text)}</div>')
            else:
                out_html.append(f'<p class="text-p">{inline_format(p_text)}</p>')

    return '\n'.join(out_html)

# CSS Template
CSS = """
    :root {
      --navy-dark: #0b2545;
      --navy-mid: #134074;
      --blue-accent: #0284c7;
      --blue-light: #e0f2fe;
      --blue-subtle: #f0f9ff;
      --teal-accent: #0d9488;
      --green-accent: #059669;
      --green-light: #ecfdf5;
      --amber-accent: #d97706;
      --amber-light: #fefce8;
      --amber-border: #fef08a;
      --red-accent: #dc2626;
      --red-light: #fef2f2;
      --purple-accent: #7c3aed;
      --purple-light: #f5f3ff;
      --text-dark: #0f172a;
      --text-body: #1e293b;
      --text-muted: #475569;
      --text-sub: #64748b;
      --card-bg: #ffffff;
      --page-bg: #f1f5f9;
      --border-card: #e2e8f0;
      --border-subtle: #cbd5e1;
      --code-bg: #0f172a;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Hind Siliguri', 'Plus Jakarta Sans', sans-serif;
      background-color: var(--page-bg);
      color: var(--text-body);
      font-size: 12px;
      line-height: 1.55;
      -webkit-font-smoothing: antialiased;
    }

    /* Print Sticky Action Bar */
    .action-bar {
      position: sticky;
      top: 0;
      z-index: 1000;
      background: rgba(255, 255, 255, 0.96);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid var(--border-card);
      padding: 10px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .action-bar .brand-title {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 13px;
      font-weight: 700;
      color: var(--navy-mid);
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .print-btn {
      background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
      color: white;
      border: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-weight: 600;
      font-size: 12px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 2px 4px rgba(2, 132, 199, 0.25);
    }
    .print-btn:hover {
      background: #0284c7;
    }

    /* Document Sheet */
    .doc-page {
      max-width: 820px;
      margin: 20px auto;
      background: var(--card-bg);
      padding: 32px 36px;
      border-radius: 8px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.04);
      border: 1px solid var(--border-card);
    }

    /* Header Master Banner */
    .master-banner {
      background: linear-gradient(135deg, #0b2545 0%, #0d3b66 55%, #0284c7 100%);
      border-radius: 8px;
      padding: 14px 20px;
      color: white;
      margin-bottom: 8px;
    }
    .banner-top {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 4px;
    }
    .banner-icon {
      width: 28px;
      height: 28px;
      background: rgba(255,255,255,0.15);
      border: 2px solid #38bdf8;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
      font-weight: 800;
    }
    .banner-title {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 20px;
      font-weight: 800;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }
    .banner-sub {
      font-size: 12px;
      color: #93c5fd;
      margin-bottom: 10px;
      margin-left: 40px;
    }
    .meta-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      border-top: 1px solid rgba(255,255,255,0.15);
      padding-top: 8px;
    }
    .meta-item .meta-label {
      font-size: 10px;
      color: #7dd3fc;
      text-transform: uppercase;
      font-weight: 600;
      letter-spacing: 0.5px;
      margin-bottom: 2px;
    }
    .meta-item .meta-val {
      font-size: 11px;
      color: #ffffff;
      font-weight: 600;
    }

    /* Part Banners */
    .part-banner {
      background: var(--blue-light);
      border-left: 4px solid var(--blue-accent);
      color: #0369a1;
      padding: 5px 10px;
      border-radius: 4px;
      font-family: 'Plus Jakarta Sans', 'Hind Siliguri', sans-serif;
      font-size: 11.5px;
      font-weight: 800;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      margin: 12px 0 8px 0;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    /* Study Cards */
    .study-card {
      background: var(--card-bg);
      border: 1px solid var(--border-card);
      border-radius: 6px;
      padding: 9px 13px;
      margin-bottom: 8px;
      box-shadow: 0 1px 2px rgba(0,0,0,0.015);
    }
    .card-title {
      font-size: 12.5px;
      font-weight: 700;
      color: var(--text-dark);
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 6px;
    }
    .badge-num {
      background: var(--blue-accent);
      color: white;
      font-family: 'Plus Jakarta Sans', monospace;
      font-size: 10px;
      font-weight: 700;
      padding: 1px 6px;
      border-radius: 4px;
      letter-spacing: 0.5px;
      display: inline-block;
    }

    /* Section Sub-labels */
    .tag-label {
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin: 5px 0 2px 0;
      display: block;
    }
    .tag-label.cyan { color: #0284c7; }
    .tag-label.green { color: #059669; }
    .tag-label.amber { color: #d97706; }
    .tag-label.purple { color: #6366f1; }
    .tag-label.red { color: #dc2626; }

    p.text-p {
      margin-bottom: 3px;
      font-size: 11.5px;
      color: var(--text-body);
      line-height: 1.5;
    }

    ul.clean-list {
      margin-left: 18px;
      margin-bottom: 4px;
    }
    ul.clean-list li {
      margin-bottom: 2px;
      font-size: 11.5px;
    }

    /* Definition Alert inside card */
    .def-box {
      border-radius: 4px;
      padding: 5px 9px;
      margin: 4px 0;
      font-size: 11px;
      line-height: 1.45;
    }
    .def-box.english {
      background: var(--blue-subtle);
      border-left: 3px solid var(--blue-accent);
      color: #0c4a6e;
    }
    .def-box.bangla {
      background: #faf5ff;
      border-left: 3px solid #9333ea;
      color: #581c87;
    }

    /* Memory / Rule box */
    .memory-box {
      background: var(--amber-light);
      border: 1px solid var(--amber-border);
      border-left: 4px solid #eab308;
      padding: 6px 10px;
      border-radius: 4px;
      font-size: 11px;
      color: #713f12;
      margin: 5px 0 4px 0;
    }

    /* Error / Warning box */
    .warn-box {
      background: var(--red-light);
      border: 1px solid #fecaca;
      border-left: 4px solid var(--red-accent);
      padding: 6px 10px;
      border-radius: 4px;
      font-size: 11px;
      color: #7f1d1d;
      margin: 5px 0 4px 0;
    }

    /* Tables */
    .table-wrap {
      margin: 6px 0 8px 0;
      border: 1px solid var(--border-card);
      border-radius: 5px;
      overflow: hidden;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 11px;
      text-align: left;
    }
    thead th {
      background: #f8fafc;
      color: var(--text-dark);
      font-weight: 700;
      padding: 6px 8px;
      border-bottom: 1px solid var(--border-card);
    }
    tbody tr {
      border-bottom: 1px solid var(--border-card);
    }
    tbody tr:last-child {
      border-bottom: none;
    }
    tbody tr:nth-child(even) {
      background: #fbfcfe;
    }
    tbody td {
      padding: 5px 8px;
      color: var(--text-body);
    }

    /* Code & Terminal */
    .code-box {
      background: #0f172a;
      border: 1px solid #1e293b;
      border-radius: 5px;
      margin: 4px 0;
      overflow: hidden;
    }
    .code-top {
      background: #1e293b;
      color: #94a3b8;
      font-family: 'Plus Jakarta Sans', monospace;
      font-size: 9px;
      font-weight: 600;
      padding: 2px 8px;
      display: flex;
      justify-content: space-between;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }
    pre {
      margin: 0;
      padding: 6px 10px;
      font-family: 'Fira Code', monospace;
      font-size: 10.5px;
      line-height: 1.4;
      color: #e2e8f0;
      overflow-x: auto;
    }
    code {
      font-family: 'Fira Code', monospace;
      background: #f1f5f9;
      color: #0369a1;
      padding: 1px 4px;
      border-radius: 3px;
      font-size: 10.5px;
    }
    pre code {
      background: transparent;
      color: inherit;
      padding: 0;
    }

    .output-box {
      background: #f8fafc;
      border: 1px dashed #cbd5e1;
      border-left: 3px solid #64748b;
      border-radius: 4px;
      padding: 5px 8px;
      font-family: 'Fira Code', monospace;
      font-size: 10.5px;
      color: #334155;
      margin: 3px 0 6px 0;
    }

    /* Syntax Highlighting */
    .syn-kw { color: #f43f5e; font-weight: 600; }
    .syn-fn { color: #38bdf8; }
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
splits = re.split(r'\n(?=#\s+8\.\d+\s+)', raw_md)
opening_md = splits[0]
numbered_secs = splits[1:75]

sec75_and_after = splits[75]
post_parts = re.split(r'\n(?=#{1,2}\s+[🔥🧠📝🎯])', sec75_and_after)
sec75_md = post_parts[0]
post_tree_md = post_parts[1]
post_concept_md = post_parts[2]
post_practice_md = post_parts[3]
post_summary_md = post_parts[4]

all_secs = numbered_secs + [sec75_md]

# Part definitions: (trigger_sec_num, banner_text)
PART_TRIGGERS = {
    1: "Part 01 — String Creation, Quotes & Escape Characters (8.1 – 8.9)",
    10: "Part 02 — Length, Indexing & Character Access (8.10 – 8.20)",
    21: "Part 03 — Template Literals & Case Transformation (8.21 – 8.31)",
    32: "Part 04 — Searching, Checking & Substring Extraction (8.32 – 8.45)",
    46: "Part 05 — Replacing, Splitting, Padding & Immutability (8.46 – 8.58)",
    59: "Part 06 — Unicode, Objects, Conversion & Real-Life Projects (8.59 – 8.75)",
}

# Start building HTML
html_parts = []
html_parts.append(f"""<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>JS Master Study Documentation — Chapter 08: Strings</title>
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
      <div class="banner-sub">CHAPTER 08: STRINGS &amp; TEXT PROCESSING</div>
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">Total Sections</div>
          <div class="meta-val">75 Modules + Projects</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Curriculum Part</div>
          <div class="meta-val">Part 04 — Core Data Structures (1/3)</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Core Mechanics</div>
          <div class="meta-val">Immutability, Unicode &amp; Text Parsing</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Reference Standard</div>
          <div class="meta-val">ECMAScript 2026 / V8 Runtime</div>
        </div>
      </div>
    </header>

    <!-- Chapter Opening Statement (Page 1 Balance) -->
    <div class="study-card" style="border-left: 4px solid var(--blue-accent); background: #f8fafc; padding: 10px 14px; margin-bottom: 8px;">
      <h2 style="font-size: 13px; color: var(--navy-mid); margin-bottom: 4px;">Strings — String / টেক্সট নিয়ে কাজ</h2>
      <p class="text-p">JavaScript-এ <strong>String</strong> হলো text বা character-এর sequence। যেমন:</p>
      <div class="code-box" style="margin: 4px 0;">
        <div class="code-top"><span>JavaScript</span><span>Examples</span></div>
        <pre><span class="syn-kw">let</span> name = <span class="syn-str">"Shariar"</span>;
<span class="syn-kw">let</span> university = <span class="syn-str">"Daffodil International University"</span>;
<span class="syn-kw">let</span> message = <span class="syn-str">"Hello JavaScript!"</span>;</pre>
      </div>
      <p class="text-p" style="font-weight: 600; color: #0369a1; margin-top: 4px;">এগুলো সবই <strong>String</strong>।</p>
    </div>
""")

# Render all 75 numbered sections
for idx, sec_text in enumerate(all_secs, start=1):
    if idx in PART_TRIGGERS:
        html_parts.append(f'    <div class="part-banner">{PART_TRIGGERS[idx]}</div>\n')

    lines = sec_text.strip().split('\n')
    header_line = lines[0].strip()
    body_lines = lines[1:]

    m = re.match(r'^#\s+(8\.\d+)\s+(.*)$', header_line)
    if m:
        sec_num, sec_title = m.group(1), m.group(2)
    else:
        sec_num, sec_title = f"8.{idx}", header_line.lstrip('#').strip()

    card_style = ""
    badge_style = ""
    if "Project" in sec_title or "Cheat Sheet" in sec_title:
        card_style = ' style="border-left: 4px solid #10b981; background: #f0fdf4;"'
        badge_style = ' style="background: #059669;"'

    rendered_body = parse_section_body('\n'.join(body_lines), sec_num)

    html_parts.append(f"""    <!-- {sec_num} -->
    <div class="study-card"{card_style}>
      <div class="card-title"><span class="badge-num"{badge_style}>{sec_num}</span> {inline_format(sec_title)}</div>
{rendered_body}
    </div>
""")

# Part 07: Architecture Tree, Key Concepts, Practice Lab & Summary
html_parts.append('    <div class="part-banner">Part 07 — Comprehensive Mental Map, Key Concepts &amp; Practice Lab</div>\n')

# 1. Architecture Tree
tree_body = parse_section_body(post_tree_md.replace('# 🔥 String-এর সবচেয়ে গুরুত্বপূর্ণ বিষয়', '').strip())
html_parts.append(f"""    <!-- String Architecture Tree -->
    <div class="study-card" style="border-left: 4px solid #f59e0b;">
      <div class="card-title"><span class="badge-num" style="background: #d97706;">MENTAL MAP</span> 🔥 String-এর সবচেয়ে গুরুত্বপূর্ণ বিষয় (Architecture Tree)</div>
{tree_body}
    </div>
""")

# 2. Critical Concepts
concept_body = parse_section_body(post_concept_md.replace('# 🧠 খুব গুরুত্বপূর্ণ Concept', '').strip())
html_parts.append(f"""    <!-- Critical Concepts -->
    <div class="study-card" style="border-left: 4px solid #ef4444;">
      <div class="card-title"><span class="badge-num" style="background: #dc2626;">CORE CONCEPTS</span> 🧠 খুব গুরুত্বপূর্ণ Concept</div>
{concept_body}
    </div>
""")

# 3. Practice Set
html_parts.append("""    <!-- Practice Set -->
    <div class="study-card" style="border-left: 4px solid #0284c7;">
      <div class="card-title"><span class="badge-num">PRACTICE LAB</span> 📝 Practice Set — Chapter 8</div>
""")

# Parse Practice Problems
probs = re.split(r'\n(?=###\s+Practice\s+\d+)', post_practice_md.replace('# 📝 Practice Set — Chapter 8', ''))
for p in probs:
    if not p.strip():
        continue
    p_lines = p.strip().split('\n')
    prob_title = p_lines[0].replace('###', '').strip()
    prob_body = '\n'.join(p_lines[1:])
    rendered_prob = parse_section_body(prob_body)
    html_parts.append(f"""      <div class="practice-item" style="background: white; border: 1px solid var(--border-card); border-left: 4px solid var(--blue-accent); margin-bottom: 8px;">
        <h4 style="font-size: 12px; font-weight: 700; color: var(--navy-mid); margin-bottom: 3px;">{inline_format(prob_title)}</h4>
{rendered_prob}
      </div>""")

html_parts.append("    </div>\n")

# 4. Final Summary & Next Chapter Preview
summary_lines = post_summary_md.replace('# 🎯 Chapter 8 Final Summary', '').strip().split('\n')
summary_text = '\n'.join(summary_lines)
parts_sum = re.split(r'\n(?=পরবর্তী অধ্যায় হবে)', summary_text)
core_summary_md = parts_sum[0]
next_preview_md = parts_sum[1] if len(parts_sum) > 1 else ""

rendered_summary = parse_section_body(core_summary_md)

html_parts.append(f"""    <!-- Chapter 8 Final Summary -->
    <div class="study-card" style="border-left: 4px solid #8b5cf6; background: #faf5ff;">
      <div class="card-title"><span class="badge-num" style="background: #7c3aed;">SUMMARY</span> 🎯 Chapter 8 Final Summary</div>
{rendered_summary}
    </div>
""")

if next_preview_md.strip():
    html_parts.append(f"""    <!-- Next Chapter Preview -->
    <div class="study-card" style="border-left: 4px solid #0284c7; background: #f0f9ff;">
      <div class="card-title"><span class="badge-num">NEXT CHAPTER</span> 🚀 Chapter 9 Preview — Arrays</div>
      <p class="text-p" style="font-size: 12px; line-height: 1.6; color: #0c4a6e;">
        {inline_format(next_preview_md.strip())}
      </p>
    </div>
""")

html_parts.append("""  </div>
</body>
</html>
""")

output_html = '\n'.join(html_parts)

# Write HTML file
target_file = r'Code/Chapter-08-Strings.html'
with open(target_file, 'w', encoding='utf-8') as f:
    f.write(output_html)

print(f"Generated {target_file} successfully! Total lines: {len(output_html.splitlines())}")
