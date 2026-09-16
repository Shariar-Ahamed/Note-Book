import re
import sys
import html
import subprocess
import os

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Read raw markdown
with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-29.md', 'r', encoding='utf-8') as f:
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

def highlight_js(code_str, invalid_token=None):
    token_spec = [
        ('COMMENT_MULTI', r'/\*[\s\S]*?\*/'),
        ('COMMENT_LINE', r'//.*$'),
        ('REGEX_LIT', r'/(?:\\/|[^\n\r/])+/[gimsuy]*'),
        ('STRING_TMPL', r'`(?:\\.|[^`\\])*`'),
        ('STRING_DBL', r'"(?:\\.|[^"\\])*"'),
        ('STRING_SGL', r"'(?:\\.|[^'\\])*'"),
        ('KEYWORD', r'\b(?:for|while|do|break|continue|if|else|let|const|var|function|return|switch|case|default|of|in|new|typeof|delete|this|super|class|extends|static|instanceof|try|catch|finally|throw|await|async|yield)\b'),
        ('BOOL_NULL', r'\b(?:true|false|null|undefined|NaN)\b'),
        ('DOM_BUILTIN', r'\b(?:console|window|document|Math|Object|Array|Date|JSON|Promise|Error|Map|Set|WeakMap|WeakSet|setTimeout|clearTimeout|setInterval|clearInterval|queueMicrotask|fetch|performance)\b'),
        ('ASYNC_METHOD', r'\b(?:then|catch|finally|resolve|reject|addEventListener|removeEventListener|getElementById)\b'),
        ('NUMBER', r'\b\d+(?:\.\d+)?\b'),
        ('OTHER', r'[^\s\w]+|\w+|\s+'),
    ]
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
    
    out = []
    for mo in re.finditer(tok_regex, code_str, flags=re.MULTILINE):
        kind = mo.lastgroup
        val = mo.group()
        esc = html.escape(val)
        
        if invalid_token and (invalid_token in val or val == invalid_token):
            out.append(f'<span class="invalid-token">{esc}</span>')
            continue
            
        if kind in ('COMMENT_MULTI', 'COMMENT_LINE'):
            out.append(f'<span class="syn-com">{esc}</span>')
        elif kind in ('STRING_TMPL', 'STRING_DBL', 'STRING_SGL'):
            out.append(f'<span class="syn-str">{esc}</span>')
        elif kind == 'KEYWORD':
            out.append(f'<span class="syn-kw">{esc}</span>')
        elif kind == 'BOOL_NULL':
            out.append(f'<span class="syn-bool">{esc}</span>')
        elif kind == 'DOM_BUILTIN':
            out.append(f'<span class="syn-fn">{esc}</span>')
        elif kind == 'ASYNC_METHOD':
            out.append(f'<span class="syn-async" style="color: #38bdf8; font-weight: 600;">{esc}</span>')
        elif kind == 'NUMBER':
            out.append(f'<span class="syn-num">{esc}</span>')
        else:
            out.append(esc)
    return ''.join(out)

def render_code_box(code_text, lang='javascript', title=None, is_invalid=False, invalid_token=None, is_correct=False):
    code_text = code_text.strip()
    highlighted = highlight_js(code_text, invalid_token=invalid_token)
    
    box_extra_cls = ''
    tag_color = '#94a3b8'
    tag_label = 'JavaScript'
    
    if is_invalid:
        box_extra_cls = ' code-box-error'
        tag_color = '#f87171'
        tag_label = '❌ Blocking / Trap'
    elif is_correct:
        box_extra_cls = ' code-box-correct'
        tag_color = '#4ade80'
        tag_label = '✅ Non-Blocking / Optimal'

    display_title = title if title else "JavaScript Source"

    return f'''<div class="code-box{box_extra_cls}">
  <div class="code-top"><span style="color: {tag_color}; font-weight: 600;">{display_title}</span><span>{tag_label}</span></div>
  <pre><code>{highlighted}</code></pre>
</div>'''

def render_ascii_box(text, title="Architecture / Concept Flow"):
    text = html.escape(text.strip())
    return f'''<div class="ascii-tree-container">
  <div class="ascii-tree-header">🧭 {title}</div>
  <pre class="ascii-tree-content">{text}</pre>
</div>'''

def render_output_box(text):
    text = html.escape(text.strip())
    return f'''<div class="code-box output-box">
  <div class="code-top"><span class="out-label">▶ CONSOLE OUTPUT</span><span>Output</span></div>
  <pre>{text}</pre>
</div>'''

def render_table(table_md):
    lines = [l.strip() for l in table_md.strip().split('\n') if l.strip()]
    if len(lines) < 2:
        return ''
    
    headers = [c.strip() for c in lines[0].strip('|').split('|')]
    rows = []
    for l in lines[2:]:
        cols = [c.strip() for c in l.strip('|').split('|')]
        rows.append(cols)
        
    html_out = ['<div class="table-wrap"><table><thead><tr>']
    for h in headers:
        html_out.append(f'<th>{inline_format(h)}</th>')
    html_out.append('</tr></thead><tbody>')
    for r in rows:
        html_out.append('<tr>')
        for c in r:
            html_out.append(f'<td>{inline_format(c)}</td>')
        html_out.append('</tr>')
    html_out.append('</tbody></table></div>')
    return ''.join(html_out)

# Split sections
pattern = r'\n(?=# (?:(?:🔥\s*)?29\.\d+|🧠\s*Quick Cheat Sheet|🎯\s*Output Question Shortcut|🧠\s*Final Mental Map|📝\s*Practice Set))'
raw_sections = re.split(pattern, raw_md)

print(f"Total raw sections split: {len(raw_sections)}")

# Build HTML with Classic 1-10 UI Styling + Brand JS Yellow + Prominent Chapter Title
html_parts = []
html_parts.append('''<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter 29 — JavaScript Execution Model &amp; Event Loop | JavaScript Master Study Documentation</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Hind+Siliguri:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
  <style>
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
      --bg-page: #f8fafc;
      --bg-card: #ffffff;
      --border-card: #e2e8f0;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --font-bengali: 'Hind Siliguri', sans-serif;
      --font-heading: 'Plus Jakarta Sans', sans-serif;
      --font-code: 'Fira Code', monospace;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-page);
      color: var(--text-main);
      font-family: var(--font-bengali);
      font-size: 11px;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
    }

    /* Print Controls */
    .action-bar {
      position: sticky;
      top: 0;
      z-index: 1000;
      background: #0f172a;
      padding: 8px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #334155;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .brand-title {
      font-family: var(--font-heading);
      font-weight: 700;
      font-size: 12px;
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
      padding: 5px 12px;
      border-radius: 5px;
      font-family: var(--font-heading);
      font-size: 10px;
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
      margin: 14px auto;
      background: white;
      padding: 20px 26px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.06);
      border-radius: 8px;
    }

    /* Master Banner (Classic 1-10 Blue Gradient + Official JS Yellow Badge & Prominent Chapter Title) */
    .master-banner {
      background: linear-gradient(135deg, #075985 0%, #0369a1 50%, #0284c7 100%);
      color: white;
      padding: 12px 16px;
      border-radius: 8px;
      margin-bottom: 8px;
      box-shadow: 0 4px 12px rgba(3, 105, 161, 0.2);
    }
    .banner-top {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 4px;
    }
    .banner-icon {
      background: #f7df1e;
      color: #000000;
      font-weight: 900;
      font-size: 13px;
      width: 28px;
      height: 28px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: var(--font-code);
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.25);
      flex-shrink: 0;
    }
    .banner-title-group {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }
    .banner-title {
      font-family: var(--font-heading);
      font-size: 15.5px;
      font-weight: 800;
      letter-spacing: 0.3px;
      color: #ffffff;
    }
    .chapter-badge {
      background: #f7df1e;
      color: #000000;
      font-family: var(--font-heading);
      font-size: 13.5px;
      font-weight: 800;
      padding: 2px 10px;
      border-radius: 6px;
      letter-spacing: 0.4px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.25);
      display: inline-flex;
      align-items: center;
      border: 1px solid rgba(0, 0, 0, 0.15);
    }
    .banner-sub {
      font-size: 9.5px;
      font-weight: 600;
      opacity: 0.95;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      margin-bottom: 6px;
    }
    .meta-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
      background: rgba(15, 23, 42, 0.25);
      padding: 5px 8px;
      border-radius: 6px;
      border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .meta-item {
      display: flex;
      flex-direction: column;
    }
    .meta-label {
      font-size: 7.5px;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      color: #bae6fd;
      font-family: var(--font-heading);
      font-weight: 600;
    }
    .meta-val {
      font-size: 9.5px;
      font-weight: 700;
      color: #ffffff;
      margin-top: 1px;
    }

    /* Chapter Opening Card */
    .opening-card {
      background: #f0f9ff;
      border: 1px solid #bae6fd;
      border-left: 4px solid var(--blue-accent);
      border-radius: 6px;
      padding: 8px 12px;
      margin-bottom: 8px;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }
    .opening-title {
      font-family: var(--font-heading);
      font-size: 11.5px;
      font-weight: 700;
      color: var(--blue-dark);
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .roadmap-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 2px 8px;
      margin-top: 5px;
      background: rgba(255, 255, 255, 0.7);
      padding: 5px 8px;
      border-radius: 5px;
      border: 1px solid #e0f2fe;
    }
    .roadmap-item {
      font-size: 8.5px;
      color: #0369a1;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 4px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    /* Part Banner */
    .part-banner {
      background: linear-gradient(135deg, #1e293b, #0f172a);
      color: #38bdf8;
      font-family: var(--font-heading);
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.6px;
      padding: 5px 10px;
      border-radius: 5px;
      margin: 8px 0 6px 0;
      border-left: 3px solid #38bdf8;
      box-shadow: 0 1px 4px rgba(0,0,0,0.08);
      page-break-after: avoid !important;
      break-after: avoid !important;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }

    /* Study Cards */
    .study-card {
      background: #ffffff;
      border: 1px solid var(--border-card);
      border-radius: 6px;
      padding: 8px 11px;
      margin-bottom: 7px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }
    .card-title {
      font-family: var(--font-heading);
      font-size: 11px;
      font-weight: 700;
      color: var(--navy-deep);
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
      font-size: 9px;
      font-weight: 700;
      padding: 1px 5px;
      border-radius: 3px;
      font-family: var(--font-code);
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
    }
    th {
      background: #0f172a;
      color: #38bdf8;
      font-family: var(--font-heading);
      font-weight: 700;
      padding: 5px 8px;
      border: 1px solid #334155;
      text-align: left;
    }
    td {
      padding: 4px 8px;
      border: 1px solid #e2e8f0;
      color: #334155;
      line-height: 1.35;
    }
    tr:nth-child(even) {
      background: #f8fafc;
    }

    /* Code Boxes */
    .code-box {
      background: #0f172a;
      border-radius: 5px;
      margin: 4px 0;
      overflow: hidden;
      border: 1px solid #1e293b;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }
    .code-box-error {
      border: 1px solid #ef4444 !important;
    }
    .code-box-correct {
      border: 1px solid #10b981 !important;
    }
    .code-top {
      background: #1e293b;
      padding: 3px 8px;
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
      line-height: 1.32;
      padding: 5px 8px;
      color: #f8fafc;
      overflow-x: hidden !important;
      white-space: pre-wrap !important;
      word-break: break-word !important;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }
    code {
      font-family: var(--font-code);
    }
    p code, li code {
      font-family: var(--font-code);
      font-size: 9.5px;
      background: #f1f5f9;
      color: #0369a1;
      padding: 1px 3px;
      border-radius: 3px;
    }

    /* Syntax Highlighting */
    .syn-kw { color: #f43f5e; font-weight: 600; }
    .syn-fn { color: #38bdf8; }
    .syn-str { color: #a3e635; }
    .syn-num { color: #fb923c; }
    .syn-com { color: #64748b; font-style: italic; }
    .syn-bool { color: #c084fc; font-weight: 600; }

    /* Invalid Token Wave Highlight */
    .invalid-token {
      text-decoration: underline wavy #ef4444 !important;
      text-decoration-skip-ink: none !important;
      color: #fca5a5 !important;
      font-weight: 700 !important;
      background: rgba(239, 68, 68, 0.25) !important;
      padding: 0 3px !important;
      border-radius: 3px !important;
    }

    /* Output Box */
    .output-box {
      background: #182234;
      border-left: 3px solid #10b981;
    }
    .out-label {
      color: #34d399;
      font-weight: 700;
    }

    /* ASCII Diagrams with Pre & White-space: Pre */
    .ascii-tree-container {
      background: #0f172a;
      border: 1px solid #1e293b;
      border-radius: 5px;
      margin: 4px 0;
      overflow: hidden;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }
    .ascii-tree-header {
      background: #1e293b;
      color: #94a3b8;
      font-family: var(--font-code);
      font-size: 8.5px;
      padding: 3px 8px;
      text-transform: uppercase;
      border-bottom: 1px solid #334155;
    }
    .ascii-tree-content {
      color: #38bdf8 !important;
      font-family: var(--font-code) !important;
      font-size: 9px !important;
      line-height: 1.28 !important;
      padding: 6px 10px !important;
      background: transparent !important;
      border: none !important;
      white-space: pre !important;
      overflow-x: hidden !important;
      word-break: normal !important;
      margin: 0 !important;
    }

    /* Practice Lab Items */
    .practice-item {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-left: 3px solid var(--blue-accent);
      border-radius: 5px;
      padding: 6px 9px;
      margin-bottom: 6px;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }

    /* Print Optimization Rules */
    @page {
      size: A4;
      margin: 8mm 10mm;
    }

    @media print {
      body {
        background: white !important;
        font-size: 10px !important;
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
      #sec-29-1 {
        page-break-after: always !important;
        break-after: page !important;
        margin-bottom: 0 !important;
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
      .code-box, pre, .ascii-tree-container, .table-wrap, .def-box, .output-box, .warn-box {
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      pre {
        overflow-x: hidden !important;
        white-space: pre-wrap !important;
        word-break: break-word !important;
      }
    }
  </style>
</head>
<body>

  <!-- Sticky Top Print Nav -->
  <div class="action-bar">
    <div class="brand-title">
      <span style="color:#f7df1e; font-weight:800; font-family:var(--font-code); background:#000; padding:1px 4px; border-radius:3px;">JS</span> MASTER STUDY DOCUMENTATION
    </div>
    <button class="print-btn" onclick="window.print()">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
      Print / Save as PDF
    </button>
  </div>

  <div class="doc-page">

    <!-- Header Master Banner (Classic 1-10 Style + JS Yellow & Prominent Chapter Title) -->
    <header class="master-banner">
      <div class="banner-top">
        <div class="banner-icon">JS</div>
        <div class="banner-title-group">
          <span class="banner-title">JavaScript Master Study Documentation</span>
          <span class="chapter-badge">Chapter 29</span>
        </div>
      </div>
      <div class="banner-sub">JAVASCRIPT EXECUTION MODEL, EVENT LOOP &amp; ASYNCHRONOUS RUNTIME ARCHITECTURE</div>
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">Total Modules</div>
          <div class="meta-val">55 Modules + Practice Lab</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Curriculum Part</div>
          <div class="meta-val">Part 23 — Execution Model &amp; Event Loop</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Core Mechanics</div>
          <div class="meta-val">Call Stack, Microtasks, Task Queue &amp; V8</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Reference Standard</div>
          <div class="meta-val">HTML5 Event Loop Spec / ECMAScript 2026</div>
        </div>
      </div>
    </header>

    <!-- Chapter Opening Statement (Page 1 Balance) -->
    <div class="opening-card">
      <div class="opening-title">
        <span>🎯</span> JavaScript Execution Model &amp; Event Loop — অ্যাসিঙ্ক আর্কিটেকচার শেখার মূল উদ্দেশ্য
      </div>
      <p class="text-p">
        JavaScript সিঙ্গেল-থ্রেডেড হয়েও কীভাবে বিলিয়ন রিকোয়েস্ট, নেটওয়ার্ক আই/ও এবং নন-ব্লকিং ইউআই পরিচালনা করে—তার পেছনের চালিকাশক্তি হলো <strong>Event Loop ও Execution Context</strong>। এই চ্যাপ্টারে আমরা <strong>Call Stack (LIFO), Memory Heap, Web APIs, Microtask Queue (Promises), Macrotask Queue (Timers)</strong> এবং ব্রাউজার রেন্ডারিং পাইপলাইন গভীরভাবে শিখব।
      </p>
      <div class="roadmap-grid">
        <div class="roadmap-item"><span>📌</span> 1. Execution Model</div>
        <div class="roadmap-item"><span>📌</span> 2. Single-Threaded Nature</div>
        <div class="roadmap-item"><span>📌</span> 3. Runtime Components</div>
        <div class="roadmap-item"><span>📌</span> 4. V8 Engine Architecture</div>
        <div class="roadmap-item"><span>📌</span> 5. Call Stack (LIFO)</div>
        <div class="roadmap-item"><span>📌</span> 6. Stack Overflow Trap</div>
        <div class="roadmap-item"><span>📌</span> 7. Memory Heap Allocations</div>
        <div class="roadmap-item"><span>📌</span> 8. Execution Context (GEC/FEC)</div>
        <div class="roadmap-item"><span>📌</span> 9. Creation &amp; Execution Phase</div>
        <div class="roadmap-item"><span>📌</span> 10. Lexical Scope Chain</div>
        <div class="roadmap-item"><span>📌</span> 11. Browser Host Web APIs</div>
        <div class="roadmap-item"><span>📌</span> 12. Event Loop Core Algorithm</div>
        <div class="roadmap-item"><span>📌</span> 13. Task / Macrotask Queue</div>
        <div class="roadmap-item"><span>📌</span> 14. Microtask Queue Priority</div>
        <div class="roadmap-item"><span>📌</span> 15. setTimeout(fn, 0) Reality</div>
        <div class="roadmap-item"><span>📌</span> 16. Promise Microtask Drain</div>
        <div class="roadmap-item"><span>📌</span> 17. Async/Await Execution Order</div>
        <div class="roadmap-item"><span>📌</span> 18. fetch() &amp; DOM Queues</div>
        <div class="roadmap-item"><span>📌</span> 19. Microtask Starvation</div>
        <div class="roadmap-item"><span>📌</span> 20. Rendering Frame Sync</div>
        <div class="roadmap-item"><span>📌</span> 21. queueMicrotask() API</div>
        <div class="roadmap-item"><span>📌</span> 22. React Concurrent Mode</div>
        <div class="roadmap-item"><span>📌</span> 23. Node.js Event Loop Phases</div>
        <div class="roadmap-item"><span>📌</span> 24. 4 Execution Trace Labs</div>
      </div>
    </div>
''')

def get_part_banner(num):
    if num == 1:
        return '<div class="part-banner">Part 01 — JavaScript Engine, Call Stack &amp; Memory Heap (29.1 – 29.10)</div>'
    elif num == 11:
        return '<div class="part-banner">Part 02 — Execution Context, Lifecycle Phases &amp; Scope Chain (29.11 – 29.17)</div>'
    elif num == 18:
        return '<div class="part-banner">Part 03 — Asynchronous Mechanics, Web APIs &amp; Event Loop Architecture (29.18 – 29.26)</div>'
    elif num == 27:
        return '<div class="part-banner">Part 04 — Microtasks vs Macrotasks: Promises &amp; Execution Order (29.27 – 29.36)</div>'
    elif num == 37:
        return '<div class="part-banner">Part 05 — Advanced Runtime Internals, Starvation &amp; Node.js (29.37 – 29.54)</div>'
    elif num == 55:
        return '<div class="part-banner">Part 06 — Production Mastery, Practice Lab &amp; Mental Map (29.55 – 29.59)</div>'
    return None

# Process all 55 numbered sections (1 to 55)
for idx in range(1, 56):
    sec_text = raw_sections[idx].strip()
    pb = get_part_banner(idx)
    if pb:
        html_parts.append(f'    {pb}\n')
        
    sec_lines = sec_text.split('\n')
    header_line = sec_lines[0]
    m_head = re.search(r'# (?:🔥\s*)?(29\.\d+)\s*(?:—|-)?\s*(.*)', header_line)
    if m_head:
        sec_num = m_head.group(1)
        sec_title = m_head.group(2)
    else:
        sec_num = f'29.{idx}'
        sec_title = header_line.replace('#', '').strip()
        
    card_extra = ''
    if idx == 1:
        card_extra = ' id="sec-29-1"'
        
    html_parts.append(f'''    <div class="study-card"{card_extra}>
      <div class="card-title"><span class="badge-num">{sec_num}</span> {inline_format(sec_title)}</div>
''')
    
    body_text = '\n'.join(sec_lines[1:]).strip()
    
    # Standard parsing with markdown table extraction and separator filtering
    chunks = re.split(r'(```[\s\S]*?```|###[^\n]+|\|[^\n]+\|\n\|[\s:-|-]+\|\n(?:\|[^\n]+\|\n?)+)', body_text)
    for ch in chunks:
        ch_str = ch.strip()
        if not ch_str:
            continue
        if ch_str.startswith('|') and '\n|' in ch_str:
            html_parts.append(f'      {render_table(ch_str)}\n')
        elif ch_str.startswith('```'):
            cb_match = re.match(r'```([a-zA-Z0-9_-]*)\n([\s\S]*?)```', ch_str)
            if cb_match:
                clang = cb_match.group(1).lower()
                code_val = cb_match.group(2)
                if clang in ('javascript', 'js'):
                    html_parts.append(render_code_box(code_val))
                elif clang == 'text':
                    if any(c in code_val for c in ['│', '┌', '└', '├', '──', '─', '↓', '→', '←', 'Stack', 'Queue', 'Engine', 'Runtime', 'Loop', 'Context', 'Call', 'Phase']):
                        html_parts.append(render_ascii_box(code_val))
                    else:
                        html_parts.append(render_output_box(code_val))
                else:
                    html_parts.append(render_code_box(code_val, lang=clang, title=clang.upper()))
        elif ch_str.startswith('###'):
            sub_title = ch_str.replace('###', '').strip()
            if sub_title.lower() == 'output':
                pass
            else:
                html_parts.append(f'      <div class="section-subhead">🔹 {inline_format(sub_title)}</div>\n')
        else:
            lines = ch_str.split('\n')
            p_acc = []
            in_list = False
            for l in lines:
                ls = l.strip()
                if not ls:
                    continue
                if ls == '---' or ls.startswith('---') or ls == '***':
                    continue
                if ls.endswith('---'):
                    ls = ls[:-3].strip()
                if not ls:
                    continue
                if ls.startswith('* ') or ls.startswith('- '):
                    if not in_list:
                        if p_acc:
                            p_text = " ".join(p_acc).strip()
                            if p_text and p_text != '---':
                                html_parts.append(f'      <p class="text-p">{inline_format(p_text)}</p>\n')
                            p_acc = []
                        html_parts.append('      <ul style="margin: 2px 0 5px 16px; color: #334155; font-size: 10.5px;">\n')
                        in_list = True
                    html_parts.append(f'        <li>{inline_format(ls[2:])}</li>\n')
                else:
                    if in_list:
                        html_parts.append('      </ul>\n')
                        in_list = False
                    p_acc.append(ls)
            if in_list:
                html_parts.append('      </ul>\n')
            if p_acc:
                p_text = " ".join(p_acc).strip()
                if p_text and p_text != '---':
                    html_parts.append(f'      <p class="text-p">{inline_format(p_text)}</p>\n')
                
    html_parts.append('    </div>\n')

# Section 56: Quick Cheat Sheet
sec56 = raw_sections[56].strip()
m_table56 = re.search(r'(\|[\s\S]*\|)', sec56)
html_parts.append(f'''    <div class="study-card">
      <div class="card-title"><span class="badge-num">29.Cheat</span> 🧠 Quick Cheat Sheet — Event Loop &amp; Execution Components</div>
      <p class="text-p">JavaScript রানটাইমের প্রতিটি মেকানিজম এবং তার প্রধান ভূমিকার দ্রুত রেফারেন্স টেবিল:</p>
      {render_table(m_table56.group(1)) if m_table56 else ""}
    </div>
''')

# Section 57: Output Question Shortcut
sec57 = raw_sections[57].strip()
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">29.Formula</span> 🎯 Output Question Shortcut — ৩ ধাপের গোল্ডেন রুল</div>
      <p class="text-p">যেকোনো জটিল ইন্টারভিউ কোডের এক্সিকিউশন অর্ডার তাৎক্ষণিকভাবে বের করার শর্টকাট ফর্মুলা:</p>
      <div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 8px;">
        <div>
''')
code_shortcut = """console.log("A");

setTimeout(() => {
    console.log("B");
}, 0);

Promise.resolve().then(() => {
    console.log("C");
});

console.log("D");"""
html_parts.append(render_code_box(code_shortcut, title="Sample Execution Problem"))
html_parts.append('''        </div>
        <div>
''')
ascii_rule = """1️⃣ Synchronous (Immediate)
       ↓
2️⃣ Microtask Queue (Promises)
       ↓
3️⃣ Macrotask Queue (Timers)"""
html_parts.append(render_ascii_box(ascii_rule, title="Golden Execution Priority"))
html_parts.append(render_output_box("A\nD\nC\nB"))
html_parts.append('''        </div>
      </div>
    </div>
''')

# Section 58: Final Mental Map
sec58 = raw_sections[58].strip()
ascii_map_match = re.search(r'```text([\s\S]*?)```', sec58)
ascii_map = ascii_map_match.group(1).strip() if ascii_map_match else ""

html_parts.append(f'''    <div class="study-card">
      <div class="card-title"><span class="badge-num">29.Map</span> 🎯 Final Mental Map &amp; Event Loop Architecture</div>
      <p class="text-p">JavaScript সিংক্রোনাস ও অ্যাসিনক্রোনাস কোঅর্ডিনেশনের পূর্ণাঙ্গ আর্কিটেকচারাল ফ্লো ম্যাপ:</p>
      {render_ascii_box(ascii_map, title="Event Loop Global Coordination Tree")}
      
      <div class="def-box" style="margin-top: 6px; padding: 6px 10px; background: #f0fdf4; border-left: 3px solid #10b981;">
        <div style="font-weight: 700; font-size: 10px; color: #065f46; margin-bottom: 2px;">⭐ এক নজরে মূল কথা (Key Takeaway):</div>
        <div style="font-size: 9.5px; color: #047857; line-height: 1.45;">
          JavaScript code প্রথমে Call Stack-এ synchronous-ভাবে execute হয়; asynchronous কাজ host environment-এর মাধ্যমে schedule হয়; Call Stack খালি হলে microtasks আগে process হয়, তারপর tasks-এর সুযোগ আসে—এই coordination-ই Event Loop-এর মূল ভিত্তি।
        </div>
      </div>
    </div>
''')

# Section 59: Practice Set (4 Real-World Execution Trace Labs with Full Step-by-Step Solutions)
practice_solutions = [
    {
        "id": "Practice 1",
        "level": "Beginner",
        "title": "Timer vs Synchronous Code",
        "desc": "setTimeout(fn, 0) বনাম সাধারণ console.log এর এক্সিকিউশন অর্ডার যাচাই:",
        "code": """console.log("A");

setTimeout(() => {
    console.log("B");
}, 0);

console.log("C");""",
        "output": "A\nC\nB",
        "explanation": "১. 'A' কল স্ট্যাকে তাৎক্ষণিকভাবে এক্সিকিউট হয়ে প্রিন্ট হয়।\n২. setTimeout কল হয়ে টাইমার হোস্ট APIs-এ হ্যান্ডল হয় এবং ০ms পর Macrotask Queue-তে যুক্ত হয়।\n৩. 'C' কল স্ট্যাকে এক্সিকিউট হয়ে প্রিন্ট হয়।\n৪. কল স্ট্যাক খালি হলে ইভেন্ট লুপ Macrotask Queue থেকে 'B' এনে এক্সিকিউট করে।"
    },
    {
        "id": "Practice 2",
        "level": "Beginner",
        "title": "Promise Microtask vs Synchronous Code",
        "desc": "Promise.resolve().then() বনাম সাধারণ console.log এর এক্সিকিউশন অর্ডার:",
        "code": """console.log("A");

Promise.resolve().then(() => {
    console.log("B");
});

console.log("C");""",
        "output": "A\nC\nB",
        "explanation": "১. 'A' সিঙ্ক্রোনাসভাবে প্রিন্ট হয়।\n২. Promise.resolve() এর .then() কলব্যাক Microtask Queue-তে শিডিউল হয়।\n৩. 'C' সিঙ্ক্রোনাসভাবে প্রিন্ট হয়।\n৪. সিনক্রোনাস স্ক্রিপ্ট শেষ হওয়ামাত্রই কল স্ট্যাক খালি পেয়ে Microtask Queue থেকে 'B' এক্সিকিউট হয়।"
    },
    {
        "id": "Practice 3",
        "level": "Intermediate",
        "title": "Combined Multi-Priority Execution Trace",
        "desc": "Synchronous, Timer ও একাধিক Promise-এর সম্মিলিত এক্সিকিউশন ট্রেস:",
        "code": """console.log("1");

setTimeout(() => {
    console.log("2");
}, 0);

Promise.resolve().then(() => {
    console.log("3");
});

Promise.resolve().then(() => {
    console.log("4");
});

console.log("5");""",
        "output": "1\n5\n3\n4\n2",
        "explanation": "১. সিনক্রোনাস কোড: '1' এবং '5' আগে প্রিন্ট হবে।\n২. মাইক্রোটাস্ক ড্রেন: '3' এবং '4' মাইক্রোটাস্ক কিউতে থাকায় টাইমার টাস্কের আগে পরপর প্রিন্ট হবে।\n৩. ম্যাক্রোটাস্ক এক্সিকিউশন: সব মাইক্রোটাস্ক শেষ হলে ইভেন্ট লুপ টাস্ক কিউ থেকে '2' এক্সিকিউট করবে।"
    },
    {
        "id": "Practice 4",
        "level": "Advanced",
        "title": "Interleaved Nested Microtasks & Macrotasks",
        "desc": "টাইমারের ভেতর প্রমিজ এবং প্রমিজের ভেতর টাইমারের জটিল ইন্টারলিভড এক্সিকিউশন:",
        "code": """console.log("A");

setTimeout(() => {
    console.log("B");

    Promise.resolve().then(() => {
        console.log("C");
    });
}, 0);

Promise.resolve().then(() => {
    console.log("D");

    setTimeout(() => {
        console.log("E");
    }, 0);
});

console.log("F");""",
        "output": "A\nF\nD\nB\nC\nE",
        "explanation": "১. সিনক্রোনাস ফেজ: 'A' প্রিন্ট হয়, Macrotask Q-তে ঢোকে Timer-B, Microtask Q-তে ঢোকে Promise-D, 'F' প্রিন্ট হয়। [Output: A, F]\n২. মাইক্রোটাস্ক ফেজ: Promise-D চলে, 'D' প্রিন্ট করে Macrotask Q-তে Timer-E পাঠায়। [Output: D]\n৩. প্রথম ম্যাক্রোটাস্ক: Timer-B চলে, 'B' প্রিন্ট করে Microtask Q-তে Promise-C পাঠায়। [Output: B]\n৪. মাইক্রোটাস্ক চেক: পরবর্তী ম্যাক্রোটাস্কে যাওয়ার আগে ইভেন্ট লুপ মাইক্রোটাস্ক Promise-C রান করে। [Output: C]\n৫. দ্বিতীয় ম্যাক্রোটাস্ক: Timer-E চলে 'E' প্রিন্ট করে। [Output: E]\nচূড়ান্ত রেজাল্ট: A → F → D → B → C → E"
    }
]

html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">29.Lab</span> 📝 Hands-On Practice Lab — 4 Event Loop Execution Trace Challenges</div>
      <p class="text-p">ইভেন্ট লুপের বিভিন্ন ফেজের অগ্রাধিকার নিখুঁতভাবে যাচাই করতে নিচে ৪টি বহুল জিজ্ঞাসিত চ্যালেঞ্জের সম্পূর্ণ স্টেপ-বাই-স্টেপ ট্রেস সলিউশন দেওয়া হলো:</p>
''')

for p in practice_solutions:
    lvl_color = "#059669" if p["level"] == "Beginner" else ("#d97706" if p["level"] == "Intermediate" else "#dc2626")
    html_parts.append(f'''      <div class="practice-item">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 3px;">
          <span style="font-weight: 700; font-size: 11px; color: var(--navy-deep);">{p["id"]}: {p["title"]}</span>
          <span style="background: {lvl_color}; color: white; font-size: 8px; font-weight: 700; padding: 1px 6px; border-radius: 3px; text-transform: uppercase;">{p["level"]}</span>
        </div>
        <p class="text-p" style="margin-bottom: 3px;">{p["desc"]}</p>
        {render_code_box(p["code"], title=f'{p["id"]} Code Challenge')}
        {render_output_box(p["output"])}
        <div class="def-box" style="margin-top: 3px; background: #f8fafc; border-left: 3px solid var(--blue-accent);">
          <div style="font-weight: 700; font-size: 9px; color: var(--blue-dark); margin-bottom: 2px;">🔍 Step-by-Step Execution Trace:</div>
          <div style="font-size: 8.5px; color: #334155; line-height: 1.35; white-space: pre-wrap;">{p["explanation"]}</div>
        </div>
      </div>
''')

html_parts.append('''      <div class="def-box" style="margin-top: 6px; padding: 6px 10px; background: #f0fdf4; border-left: 3px solid #10b981;">
        <div style="font-weight: 700; font-size: 10px; color: #065f46; margin-bottom: 2px;">🚀 Next Chapter Preview:</div>
        <div style="font-family: var(--font-heading); font-size: 10px; font-weight: 700; color: #0369a1;">
          Chapter 30 — JavaScript Memory Management &amp; Garbage Collection
        </div>
        <div style="font-size: 9px; color: #334155; margin-top: 2px;">পরবর্তী চ্যাপ্টারে আমরা শিখব Memory Lifecycle, Memory Allocation, Stack vs Heap, Reference Counting, Mark-and-Sweep Garbage Collection এবং Memory Leak প্রতিকার।</div>
      </div>
    </div>

  </div>

</body>
</html>
''')

full_html = ''.join(html_parts)

out_file = r'c:\Users\User\Desktop\Note-Book\Code\Chapter-29-Execution-Model-Event-Loop.html'
with open(out_file, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f'Successfully generated {out_file} ({len(full_html)} chars, {len(full_html.splitlines())} lines)')
