import re
import sys
import html

sys.stdout.reconfigure(encoding='utf-8')

# 1. Read source markdown
with open(r'temp/ch-19.md', 'r', encoding='utf-8') as f:
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

def highlight_json(code_str):
    token_spec = [
        ('STRING_KEY', r'"(?:\\.|[^"\\])*"(?=\s*:)'),
        ('UNQUOTED_KEY', r'\b[a-zA-Z_]\w*(?=\s*:)'),
        ('STRING_SGL_KEY', r"'(?:\\.|[^'\\])*'(?=\s*:)"),
        ('STRING_SGL', r"'(?:\\.|[^'\\])*'"),
        ('STRING_VAL', r'"(?:\\.|[^"\\])*"'),
        ('BOOL_NULL', r'\b(?:true|false|null)\b'),
        ('NUMBER', r'-?\b\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\b'),
        ('COLON', r':'),
        ('COMMA', r','),
        ('BRACKET', r'[{}\[\]]'),
        ('OTHER', r'[^\s]+|\s+'),
    ]
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
    out = []
    for mo in re.finditer(tok_regex, code_str):
        kind = mo.lastgroup
        val = mo.group()
        esc = html.escape(val)
        if kind == 'STRING_KEY':
            out.append(f'<span class="syn-kw" style="color:#38bdf8;">{esc}</span>')
        elif kind in ('UNQUOTED_KEY', 'STRING_SGL_KEY'):
            out.append(f'<span class="syn-kw" style="color:#f87171; text-decoration: underline wavy #ef4444;" title="Invalid JSON Key">{esc}</span>')
        elif kind == 'STRING_SGL':
            out.append(f'<span class="syn-str" style="color:#f87171; text-decoration: underline wavy #ef4444;" title="Invalid: Single quotes not allowed in JSON">{esc}</span>')
        elif kind == 'STRING_VAL':
            out.append(f'<span class="syn-str">{esc}</span>')
        elif kind == 'BOOL_NULL':
            out.append(f'<span class="syn-bool">{esc}</span>')
        elif kind == 'NUMBER':
            out.append(f'<span class="syn-num">{esc}</span>')
        elif kind == 'COLON':
            out.append(f'<span class="syn-op">:</span>')
        elif kind == 'COMMA':
            out.append(f'<span class="syn-op">,</span>')
        elif kind == 'BRACKET':
            out.append(f'<span style="color:#94a3b8;">{esc}</span>')
        else:
            out.append(esc)
    return ''.join(out)

def highlight_js(code_str):
    token_spec = [
        ('COMMENT_MULTI', r'/\*[\s\S]*?\*/'),
        ('COMMENT_LINE', r'//.*$'),
        ('REGEX_LIT', r'/(?:\\/|[^\n\r/])+/[gimsuy]*'),
        ('STRING_TMPL', r'`(?:\\.|[^`\\])*`'),
        ('STRING_DBL', r'"(?:\\.|[^"\\])*"'),
        ('STRING_SGL', r"'(?:\\.|[^'\\])*'"),
        ('KEYWORD', r'\b(?:for|while|do|break|continue|if|else|let|const|var|function|return|switch|case|default|of|in|new|typeof|delete|this|super|class|extends|static|instanceof|try|catch|finally|throw|await|async|yield|debugger)\b'),
        ('BOOL_NULL', r'\b(?:true|false|null|undefined|NaN|Infinity)\b'),
        ('DOM_BUILTIN', r'\b(?:JSON|localStorage|sessionStorage|window|document|console|fetch|Response|Headers|Request|Object|Array|Math|Date|Number|Boolean|String|Error|SyntaxError|Map|Set)\b'),
        ('DOM_METHOD', r'\b(?:stringify|parse|setItem|getItem|removeItem|clear|then|catch|json|text|map|filter|find|push|includes|toISOString|getTime|keys|values|entries)\b'),
        ('JSON_PROP', r'\b(?:headers|method|body|status|ok|name|age|email|role|skills|city|address|user|student|products)\b'),
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
        elif kind == 'JSON_PROP':
            out.append(f'<span class="syn-kw" style="color:#fdba74;">{esc}</span>')
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
            elif "মনে রাখো" in last_subheading or "মনে রাখবে" in last_subheading or "গুরুত্বপূর্ণ" in last_subheading or "Important" in last_subheading:
                out_html.append(f'<div class="sub-badge" style="background:#fef9c3; color:#854d0e;">📌 {inline_format(last_subheading)}</div>')
            elif "Syntax" in last_subheading or "Formula" in last_subheading or "Workflow" in last_subheading:
                out_html.append(f'<div class="sub-badge" style="background:#ede9fe; color:#6d28d9;">⚙️ {inline_format(last_subheading)}</div>')
            elif "Output" in last_subheading or "Expected" in last_subheading:
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
            if txt.startswith("⚠️") or "Warning" in txt or "সতর্কতা" in txt or "সমস্যা" in txt or "বিপদ" in txt or "Security" in txt or "Error" in txt:
                out_html.append(f'<div class="warn-box">{inline_format(txt)}</div>')
            elif txt.startswith("✅") or txt.startswith("❌"):
                badge_bg = "#fee2e2" if txt.startswith("❌") else "#dcfce7"
                badge_color = "#991b1b" if txt.startswith("❌") else "#166534"
                out_html.append(f'<div class="sub-badge" style="background:{badge_bg}; color:{badge_color};">{inline_format(txt)}</div>')
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
            is_ascii = any(c in raw_code for c in ['├──', '└──', '│', '──', '┌', '└', '↓', '→', '▼', '▲', '┼', '---------------------']) or (lang == 'text' and any(k in raw_code.lower() for k in ["javascript", "json", "frontend", "backend", "client", "server", "stringify", "parse", "object", "api", "database"]))
            
            if is_ascii:
                out_html.append(f"""<div class="ascii-tree-container">{html.escape(raw_code)}</div>""")
            elif last_subheading and ("Output" in last_subheading or "Expected" in last_subheading):
                out_html.append(f"""<div class="code-box output-box">
  <div class="code-top"><span class="out-label">CONSOLE OUTPUT</span></div>
  <pre>{html.escape(raw_code)}</pre>
</div>""")
                last_subheading = ""
            elif lang == 'json':
                hl_code = highlight_json(raw_code)
                code_title = f"{sec_num} JSON" if sec_num else "JSON"
                out_html.append(f"""<div class="code-box">
  <div class="code-top"><span style="color:#38bdf8;">{code_title}</span><span>Data Format</span></div>
  <pre>{hl_code}</pre>
</div>""")
            elif lang in ('javascript', 'js') or (not lang and any(k in raw_code for k in ['JSON.', 'fetch(', 'console.', 'let ', 'const ', 'localStorage.', 'JSON.stringify', 'JSON.parse'])) or any(lang == m for m in ['json', 'undefined', 'date', 'fetch', 'localstorage', 'null', 'replacer', 'sessionstorage', 'typeof', 'map', 'filter', 'find', 'response', 'try', 'http']):
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
      font-size: 10px;
      line-height: 1.38;
      padding: 6px 10px;
      color: #e2e8f0;
      white-space: pre-wrap !important;
      word-break: break-word !important;
      overflow-x: hidden !important;
      margin: 0;
    }
    code {
      font-family: var(--font-code) !important;
      font-size: 9.5px;
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
    .syn-regex { color: #38bdf8; font-style: italic; }

    .ascii-tree-container {
      background: #0f172a;
      border: 1px solid #1e293b;
      border-radius: 6px;
      padding: 6px 10px;
      color: #38bdf8;
      font-family: 'Courier New', Consolas, monospace !important;
      font-size: 10px;
      line-height: 1.32;
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
splits = re.split(r'\n(?=#\s+(?:.*?\b19\.\d+\b|🎯))', raw_md)

opening_md = splits[0]
numbered_secs = splits[1:53] # 19.1 to 19.52 (52 sections)
must_know_md = splits[53]    # 19.53
quick_cheat_md = splits[54]  # 19.54
practice_set_md = splits[55] # 19.55
final_mental_md = splits[56] # 🎯 19.56 Final Mental Map

# Part definitions: (trigger_sec_num, banner_text)
PART_TRIGGERS = {
    1: "Part 01 — JSON Fundamentals, Syntax &amp; Data Types (19.1 – 19.14)",
    15: "Part 02 — Serialization &amp; Parsing: stringify, parse &amp; The Core Formula (19.15 – 19.23)",
    24: "Part 03 — Advanced Serialization: Replacer, Reviver &amp; Serialization Quirks (19.24 – 19.36)",
    37: "Part 04 — Modern Web APIs, Fetch &amp; Network Communication (19.37 – 19.43)",
    44: "Part 05 — Deep Cloning, Security, Schema &amp; Array Operations (19.44 – 19.52)",
}

# Start building HTML
html_parts = []
html_parts.append(f"""<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>JS Master Study Documentation — Chapter 19: JSON (JavaScript Object Notation)</title>
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
      <div class="banner-sub">CHAPTER 19: JSON (JAVASCRIPT OBJECT NOTATION) — SERIALIZATION, API DATA &amp; PROTOCOLS</div>
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">Total Sections</div>
          <div class="meta-val">56 Modules + Practice</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Curriculum Part</div>
          <div class="meta-val">Part 13 — Data Formats &amp; Network Serialization</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Core Mechanics</div>
          <div class="meta-val">JSON.stringify(), JSON.parse(), Replacer &amp; Reviver</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Reference Standard</div>
          <div class="meta-val">RFC 8259 / ECMA-404 / ECMAScript 2026</div>
        </div>
      </div>
    </header>

    <!-- Chapter Opening Statement (Page 1 Balance) -->
    <div class="study-card" style="border-left: 4px solid var(--blue-accent); background: #f8fafc; padding: 10px 14px; margin-bottom: 8px;">
      <h2 style="font-size: 13px; color: var(--navy-mid); margin-bottom: 4px;">JSON — Data আদান-প্রদান ও API Communication-এর সবচেয়ে গুরুত্বপূর্ণ Format</h2>
      <p class="text-p">আধুনিক ওয়েব ডেভেলপমেন্টে ফ্রন্টএন্ড ও ব্যাকএন্ডের মধ্যে ডেটা আদান-প্রদান, ক্লায়েন্ট-সাইড স্টোরেজে অবজেক্ট পারসিস্ট করা এবং বিভিন্ন সিস্টেমের মধ্যে যোগাযোগ স্থাপনের জন্য <strong>JSON (JavaScript Object Notation)</strong> হলো সবচেয়ে হালকা, দ্রুত এবং বিশ্বজনীন মানদণ্ড।</p>
      <div class="def-box" style="margin: 4px 0;">
        <div class="def-text">JS Object &nbsp;→&nbsp; JSON.stringify() &nbsp;→&nbsp; JSON String (Payload) &nbsp;→&nbsp; Network / Storage &nbsp;→&nbsp; JSON.parse() &nbsp;→&nbsp; JS Object</div>
      </div>
      <p class="text-p" style="font-weight: 600; color: #0369a1; margin-top: 4px;">ফুলস্ট্যাক ও আধুনিক ফ্রন্টএন্ড ইঞ্জিনিয়ারিংয়ে এপিআই কমিউনিকেশনের ভিত্তিই হলো এই JSON আর্কিটেকচার। 🔥</p>
    </div>
""")

# Render all 52 numbered sections (19.1 to 19.52)
for idx, sec_text in enumerate(numbered_secs, start=1):
    if idx in PART_TRIGGERS:
        html_parts.append(f'    <div class="part-banner">{PART_TRIGGERS[idx]}</div>\n')

    lines = sec_text.strip().split('\n')
    header_line = lines[0].strip()
    body_lines = lines[1:]

    m = re.search(r'\b(19\.\d+)\b\s*(.*)$', header_line)
    if m:
        sec_num, sec_title = m.group(1), m.group(2)
        sec_title = sec_title.strip('`* ')
    else:
        sec_num, sec_title = f"19.{idx}", header_line.lstrip('#').strip()

    card_style = ""
    badge_style = ""
    if "⚠️" in header_line or "সতর্কতা" in sec_title or "Security" in sec_title or "Circular" in sec_title or "Error" in sec_title:
        card_style = ' style="border-left: 4px solid #ef4444; background: #ffffff;"'
        badge_style = ' style="background: #dc2626;"'
    elif "API" in sec_title or "বনাম" in sec_title or "vs" in sec_title or "Real-life" in sec_title or "Workflow" in sec_title:
        card_style = ' style="border-left: 4px solid #0284c7; background: #ffffff;"'
        badge_style = ' style="background: #0284c7;"'

    # Strict Page 1 Balance: Section 19.1 Card must break cleanly before Section 19.2
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
html_parts.append('    <div class="part-banner">Part 06 — JSON Mastery: Must Know, Cheat Sheet, Practice Lab &amp; Mental Map</div>\n')

# 1. Must Know (19.53)
must_know_body = parse_section_body(re.sub(r'^#\s+🔥\s+19\.53\s+Must Know', '', must_know_md).strip())
html_parts.append(f"""    <!-- 19.53 Must Know -->
    <div class="study-card" style="border-left: 4px solid #ef4444; background: #ffffff;">
      <div class="card-title"><span class="badge-num" style="background: #dc2626;">MUST KNOW</span> 🔥 19.53 Must Know — JSON Syntax, Types &amp; Limitations</div>
{must_know_body}
    </div>
""")

# 2. Quick Cheat Sheet (19.54)
cheat_body = parse_section_body(re.sub(r'^#\s+🧠\s+19\.54\s+Quick Cheat Sheet', '', quick_cheat_md).strip())
html_parts.append(f"""    <!-- 19.54 Quick Cheat Sheet -->
    <div class="study-card" style="border-left: 4px solid #10b981; background: #f0fdf4;">
      <div class="card-title"><span class="badge-num" style="background: #059669;">CHEAT SHEET</span> 🧠 19.54 Quick Cheat Sheet — stringify, parse &amp; Methods</div>
{cheat_body}
    </div>
""")

# 3. Practice Set (19.55)
html_parts.append("""    <!-- 19.55 Practice Set -->
    <div class="study-card" style="border-left: 4px solid #0284c7;">
      <div class="card-title"><span class="badge-num">PRACTICE LAB</span> 📝 19.55 Practice Set — 6 Hands-on Production Problems</div>
""")

prob_blocks = re.split(r'\n(?=###\s+Practice\s+\d+)', practice_set_md.replace('# 📝 19.55 Practice Set', ''))
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

# 4. Final Mental Map & Summary (19.56)
summary_text = re.sub(r'^#\s+🎯\s+19\.56\s+Final Mental Map', '', final_mental_md).strip()
rendered_summary = parse_section_body(summary_text)

html_parts.append(f"""    <!-- 19.56 Final Mental Map -->
    <div class="study-card" style="border-left: 4px solid #8b5cf6; background: #faf5ff;">
      <div class="card-title"><span class="badge-num" style="background: #7c3aed;">SUMMARY</span> 🎯 19.56 Final Mental Map — Full-Stack JSON Workflow</div>
{rendered_summary}
    </div>
""")

# Next Chapter Preview
html_parts.append("""    <!-- Next Chapter Preview -->
    <div class="study-card" style="border-left: 4px solid #0284c7; background: #f0f9ff;">
      <div class="card-title"><span class="badge-num">NEXT CHAPTER</span> 📘 Chapter 20 Preview — ES Modules (ESM)</div>
      <p class="text-p" style="font-size: 12px; line-height: 1.6; color: #0c4a6e;">
        পরবর্তী অধ্যায়ে আমরা আধুনিক মডুলার জাভাস্ক্রিপ্ট আর্কিটেকচার <strong>ES Modules (ESM)</strong> নিয়ে বিস্তারিত শিখব—<code>import</code>, <code>export</code>, Named Export, Default Export, Dynamic Import (<code>import()</code>), <code>import.meta</code>, এবং CommonJS বনাম ES Modules-এর পার্থক্য।
      </p>
    </div>
""")

html_parts.append("""  </div>
</body>
</html>
""")

output_html = '\n'.join(html_parts)

# Write HTML file
target_file = r'Code/Chapter-19-JSON.html'
with open(target_file, 'w', encoding='utf-8') as f:
    f.write(output_html)

print(f"Generated {target_file} successfully! Total lines: {len(output_html.splitlines())}, characters: {len(output_html)}")
