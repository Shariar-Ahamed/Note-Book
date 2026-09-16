import re
import sys
import html
import subprocess
import os

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Read raw markdown
with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-26.md', 'r', encoding='utf-8') as f:
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
        ('KEYWORD', r'\b(?:for|while|do|break|continue|if|else|let|const|var|function|return|switch|case|default|of|in|new|typeof|delete|this|super|class|extends|static|instanceof|try|catch|finally|throw|await|async|yield|debugger|import|export|from|as)\b'),
        ('BOOL_NULL', r'\b(?:true|false|null|undefined|NaN)\b'),
        ('DOM_BUILTIN', r'\b(?:console|window|document|Math|Object|Array|Date|JSON|Promise|Error|Map|Set|WeakMap|WeakSet|performance|setTimeout|clearTimeout|setInterval|clearInterval)\b'),
        ('FP_METHOD', r'\b(?:map|filter|reduce|reduceRight|find|some|every|flatMap|forEach|sort|concat|slice|push|pop|shift|unshift|reverse|apply|call|bind|pipe|compose|now|addEventListener|getElementById)\b'),
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
        elif kind == 'FP_METHOD':
            out.append(f'<span class="syn-fp" style="color: #38bdf8; font-weight: 600;">{esc}</span>')
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
        tag_label = '❌ Trap / Antipattern'
    elif is_correct:
        box_extra_cls = ' code-box-correct'
        tag_color = '#4ade80'
        tag_label = '✅ Best Practice'

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
pattern = r'\n(?=# (?:(?:🔥\s*)?26\.\d+|🔥\s*Must Know|🧠\s*Quick Cheat Sheet|📝\s*Practice Set|🎯\s*Chapter 26-এর মূল কথা))'
raw_sections = re.split(pattern, raw_md)

print(f"Total raw sections split: {len(raw_sections)}")

# Build HTML with Classic 1-10 UI Styling + Brand JS Yellow + Prominent Chapter Title
html_parts = []
html_parts.append('''<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter 26 — Closures, IIFE, Currying &amp; Function Composition | JavaScript Master Study Documentation</title>
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

    /* ASCII Diagrams */
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
      #sec-26-1 {
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
          <span class="chapter-badge">Chapter 26</span>
        </div>
      </div>
      <div class="banner-sub">CLOSURES, IIFE, CURRYING &amp; FUNCTION COMPOSITION — ADVANCED PATTERNS &amp; ARCHITECTURE</div>
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">Total Modules</div>
          <div class="meta-val">59 Modules + Practice Lab</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Curriculum Part</div>
          <div class="meta-val">Part 20 — Advanced Functions &amp; Closures</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Core Mechanics</div>
          <div class="meta-val">Closures, Lexical Scope, IIFE &amp; Currying</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Reference Standard</div>
          <div class="meta-val">ECMAScript 2026 / Modern V8 Internals</div>
        </div>
      </div>
    </header>

    <!-- Chapter Opening Statement (Page 1 Balance) -->
    <div class="opening-card">
      <div class="opening-title">
        <span>🎯</span> Advanced Functions — Closure থেকে Advanced Function Patterns
      </div>
      <p class="text-p">
        Chapter 6-এ আমরা Function-এর basic concept এবং Chapter 25-এ Functional JavaScript শিখেছি। এখন সেই foundation-এর ওপর দাঁড়িয়ে JavaScript-এর <strong>সবচেয়ে গুরুত্বপূর্ণ advanced function concepts</strong>—Scope Chain, Closures, IIFE, Currying, Function Composition, Pipelines, Memoization এবং Throttling/Debouncing—নিখুঁতভাবে শিখব।
      </p>
      <div class="roadmap-grid">
        <div class="roadmap-item"><span>📌</span> 1. Scope Recap</div>
        <div class="roadmap-item"><span>📌</span> 2. Lexical Scope</div>
        <div class="roadmap-item"><span>📌</span> 3. Scope Chain</div>
        <div class="roadmap-item"><span>📌</span> 4. Closure Mechanics</div>
        <div class="roadmap-item"><span>📌</span> 5. Private Variables</div>
        <div class="roadmap-item"><span>📌</span> 6. Data Encapsulation</div>
        <div class="roadmap-item"><span>📌</span> 7. Factory Functions</div>
        <div class="roadmap-item"><span>📌</span> 8. IIFE Patterns</div>
        <div class="roadmap-item"><span>📌</span> 9. Private State (IIFE)</div>
        <div class="roadmap-item"><span>📌</span> 10. Returning Functions</div>
        <div class="roadmap-item"><span>📌</span> 11. Currying (N-ary)</div>
        <div class="roadmap-item"><span>📌</span> 12. Partial Application</div>
        <div class="roadmap-item"><span>📌</span> 13. compose() Pipeline</div>
        <div class="roadmap-item"><span>📌</span> 14. pipe() Flow</div>
        <div class="roadmap-item"><span>📌</span> 15. Memoization Cache</div>
        <div class="roadmap-item"><span>📌</span> 16. Function Decorators</div>
        <div class="roadmap-item"><span>📌</span> 17. Execution Timing</div>
        <div class="roadmap-item"><span>📌</span> 18. Debounce Logic</div>
        <div class="roadmap-item"><span>📌</span> 19. Throttle Interval</div>
        <div class="roadmap-item"><span>📌</span> 20. Loop Binding (let/var)</div>
        <div class="roadmap-item"><span>📌</span> 21. Memory Management</div>
        <div class="roadmap-item"><span>📌</span> 22. Permission Factory</div>
        <div class="roadmap-item"><span>📌</span> 23. ID Generator</div>
        <div class="roadmap-item"><span>📌</span> 24. Mini Project (Counter)</div>
      </div>
    </div>
''')

def get_part_banner(num):
    if num == 1:
        return '<div class="part-banner">Part 01 — Scope, Lexical Environment &amp; Scope Chain (26.1 – 26.3)</div>'
    elif num == 4:
        return '<div class="part-banner">Part 02 — Closures, Private State, Factories &amp; Loop Bindings (26.4 – 26.19)</div>'
    elif num == 20:
        return '<div class="part-banner">Part 03 — Immediately Invoked Function Expressions (IIFE) (26.20 – 26.26)</div>'
    elif num == 27:
        return '<div class="part-banner">Part 04 — Currying, Partial Application &amp; Function Transformation (26.27 – 26.33)</div>'
    elif num == 34:
        return '<div class="part-banner">Part 05 — Function Composition, Pipelines, Memoization &amp; Rate Limiting (26.34 – 26.53)</div>'
    elif num == 54:
        return '<div class="part-banner">Part 06 — Real-World Architectures, Mini-Project &amp; Mastery Lab (26.54 – 26.59 + Lab)</div>'
    return None

# Process all 59 sections
for idx in range(1, 60):
    sec_text = raw_sections[idx].strip()
    pb = get_part_banner(idx)
    if pb:
        html_parts.append(f'    {pb}\n')
        
    sec_lines = sec_text.split('\n')
    header_line = sec_lines[0]
    m_head = re.search(r'# (?:🔥\s*)?(26\.\d+)\s*(?:—|-)?\s*(.*)', header_line)
    if m_head:
        sec_num = m_head.group(1)
        sec_title = m_head.group(2)
    else:
        sec_num = f'26.{idx}'
        sec_title = header_line.replace('#', '').strip()
        
    card_extra = ''
    if idx == 1:
        card_extra = ' id="sec-26-1"'
        
    html_parts.append(f'''    <div class="study-card"{card_extra}>
      <div class="card-title"><span class="badge-num">{sec_num}</span> {inline_format(sec_title)}</div>
''')
    
    body_text = '\n'.join(sec_lines[1:]).strip()
    
    # Check for specific mistake highlights
    if idx == 18:
        # Loop with var trap
        html_parts.append('''      <p class="text-p">JavaScript-এ বহুল পরিচিত একটি ক্লাসিক ট্র্যাপ হলো লুপে <code>var</code> ব্যবহার করে Closure তৈরি করা:</p>
      <div class="warn-box">
        <strong>সতর্কতা:</strong> <code>var</code> কীওয়ার্ড ফাংশন-স্কোপড হওয়ায় সবকটি টাইমআউট কলব্যাক একই ভ্যারিয়েবল রেফারেন্স শেয়ার করে। ফলে লুপ শেষ হয়ে <code>i</code>-এর মান যখন 4 হয়, তখন সব কলব্যাক একই মান 4 প্রিন্ট করে।
      </div>
''')
        chunks = re.split(r'(```[\s\S]*?```|###[^\n]+|\|[^\n]+\|\n\|[\s:-|-]+\|\n(?:\|[^\n]+\|\n?)+)', body_text)
        for ch in chunks:
            ch_str = ch.strip()
            if not ch_str:
                continue
            if ch_str.startswith('```javascript'):
                cb_match = re.match(r'```javascript\n([\s\S]*?)```', ch_str)
                if cb_match:
                    html_parts.append(render_code_box(cb_match.group(1), is_invalid=True, invalid_token='var i = 1', title='❌ Loop with var (Shared Reference)'))
            elif ch_str.startswith('```text'):
                cb_match = re.match(r'```text\n([\s\S]*?)```', ch_str)
                if cb_match:
                    html_parts.append(render_output_box(cb_match.group(1)))
            elif ch_str.startswith('###'):
                pass
            else:
                for l in ch_str.split('\n'):
                    ls = l.strip()
                    if ls and ls != '---' and not ls.startswith('---'):
                        html_parts.append(f'      <p class="text-p">{inline_format(ls)}</p>\n')
    elif idx == 19:
        # Loop with let (correct solution)
        html_parts.append('''      <p class="text-p">Modern JavaScript-এ (ES6+) ব্লক-স্কোপড <code>let</code> ব্যবহার করলে প্রতি লুপ ইটারেশনে একটি করে নতুন লেক্সিক্যাল বাইন্ডিং তৈরি হয়:</p>
''')
        chunks = re.split(r'(```[\s\S]*?```|###[^\n]+|\|[^\n]+\|\n\|[\s:-|-]+\|\n(?:\|[^\n]+\|\n?)+)', body_text)
        for ch in chunks:
            ch_str = ch.strip()
            if not ch_str:
                continue
            if ch_str.startswith('```javascript'):
                cb_match = re.match(r'```javascript\n([\s\S]*?)```', ch_str)
                if cb_match:
                    html_parts.append(render_code_box(cb_match.group(1), is_correct=True, title='✅ Loop with let (Per-Iteration Lexical Binding)'))
            elif ch_str.startswith('```text'):
                cb_match = re.match(r'```text\n([\s\S]*?)```', ch_str)
                if cb_match:
                    html_parts.append(render_output_box(cb_match.group(1)))
            elif ch_str.startswith('###'):
                pass
            else:
                for l in ch_str.split('\n'):
                    ls = l.strip()
                    if ls and ls != '---' and not ls.startswith('---'):
                        html_parts.append(f'      <p class="text-p">{inline_format(ls)}</p>\n')
        html_parts.append('''      <div class="def-box">
        <div class="def-text">Key Takeaway: <code>let</code> প্রতিটি ইটারেশনের জন্য ক্লোজারের ভিতরে একটি স্বতন্ত্র মেমরি রেফারেন্স সংরক্ষণ করে, যা প্রত্যাশিত 1, 2, 3 আউটপুট নিশ্চিত করে।</div>
      </div>
''')
    elif idx == 53:
        # Common mistakes in closure
        html_parts.append('''      <p class="text-p">Closure ব্যবহারের সময় সচরাচর যেসব ভুল এবং ব্যাড-প্র্যাকটিস দেখা যায়:</p>
      <div class="section-subhead">🔹 Mistake 1 — গ্লোবাল স্টেট পরিবর্তন (Variable Mutation)</div>
''')
        code_m1 = "let count = 0; // ❌ Global variable leakage\n\nfunction increment() {\n    count++;\n}"
        code_c1 = "function createCounter() {\n    let count = 0; // ✅ Private lexical state\n    return () => ++count;\n}"
        html_parts.append(render_code_box(code_m1, is_invalid=True, invalid_token='let count = 0', title='❌ ভুল: গ্লোবাল ভ্যারিয়েবল মিউটেশন'))
        html_parts.append(f'''      <div class="warn-box">গ্লোবাল স্টেট বাইরের যেকোনো কোড দিয়ে অনিচ্ছাকৃতভাবে বদলে যেতে পারে।</div>
      <p class="text-p"><strong>সঠিক সমাধান:</strong> ফাংশন স্কোপের ভেতরে প্রাইভেট স্টেট হিসেবে রাখা:</p>
      {render_code_box(code_c1, is_correct=True, title='✅ সঠিক: Closure Encapsulated State')}
      <div class="section-subhead">🔹 Mistake 2 — লুপে <code>var</code> ব্যবহারের ফাঁদ</div>
''')
        code_m2 = "for (var i = 0; i < 3; i++) {\n    setTimeout(() => console.log(i), 100); // ❌ Output: 3, 3, 3\n}"
        code_c2 = "for (let i = 0; i < 3; i++) {\n    setTimeout(() => console.log(i), 100); // ✅ Output: 0, 1, 2\n}"
        html_parts.append(render_code_box(code_m2, is_invalid=True, invalid_token='var i = 0', title='❌ ভুল: var লুপ ট্র্যাপ'))
        html_parts.append(render_output_box("3\n3\n3"))
        html_parts.append(f'''      <p class="text-p"><strong>Modern JavaScript সমাধান:</strong> <code>let</code> দিয়ে পার-ইটারেশন ব্লক স্কোপিং নিশ্চিত করা:</p>
      {render_code_box(code_c2, is_correct=True, title='✅ সঠিক: let ব্লক স্কোপিং')}
      {render_output_box("0\n1\n2")}
''')
    else:
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
                    elif clang == 'html':
                        html_parts.append(render_code_box(code_val, lang='html', title='HTML Structure'))
                    elif clang == 'text':
                        if any(c in code_val for c in ['│', '┌', '└', '├', '──', '─', '↓', '→', '←', 'ATM', 'Advanced', 'Scope', 'process']):
                            html_parts.append(render_ascii_box(code_val))
                        else:
                            html_parts.append(render_output_box(code_val))
                    else:
                        html_parts.append(render_code_box(code_val, lang=clang, title=clang.upper()))
            elif ch_str.startswith('###'):
                sub_title = ch_str.replace('###', '').strip()
                if sub_title.lower() == 'output' or sub_title.lower() == 'calculation':
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

# Section 60: Must Know
sec60 = raw_sections[60].strip()
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">26.Must</span> 🔥 Must Know — Chapter 26 এর সবচেয়ে গুরুত্বপূর্ণ কনসেপ্টসমূহ</div>
      <p class="text-p">Chapter 26 থেকে ইন্টারভিউ ও প্রোডাকশন কোডিংয়ের জন্য অপরিহার্য মূল বিষয়গুলোর সারসংক্ষেপ:</p>
      
      <div class="section-subhead">🔹 Scope &amp; Lexical Environment</div>
      <ul style="margin: 2px 0 6px 16px; color: #334155; font-size: 10.5px;">
        <li><strong>Scope:</strong> ভ্যারিয়েবল ও ফাংশনের ভিজিবিলিটি বা এক্সেসিবিলিটি বাউন্ডারি।</li>
        <li><strong>Lexical Scope:</strong> কোড যেখানে লিখিত হয়েছে, সেই ফিজিক্যাল লোকেশনের ওপর স্কোপ নির্ধারিত হয়।</li>
        <li><strong>Scope Chain:</strong> কারেন্ট স্কোপ থেকে প্যারেন্ট স্কোপ হয়ে গ্লোবাল পর্যন্ত আইডেন্টিফায়ার খোঁজার চেইন।</li>
      </ul>

      <div class="section-subhead">🔹 Closure &amp; Encapsulation</div>
      <ul style="margin: 2px 0 6px 16px; color: #334155; font-size: 10.5px;">
        <li><strong>Closure:</strong> একটি ফাংশন ও তার লেক্সিক্যাল এনভায়রনমেন্টের রেফারেন্স সংরক্ষণ করে রাখার ক্ষমতা।</li>
        <li><strong>Private Variables:</strong> বাইরে থেকে অ্যাক্সেস অযোগ্য ডেটা এনক্যাপসুলেশন তৈরি।</li>
        <li><strong>Function Factory:</strong> প্যারামিটার পাস করে স্পেশালাইজড ডায়নামিক ফাংশন জেনারেশন।</li>
        <li><strong>Async Closure:</strong> <code>setTimeout</code>, ইভেন্ট লিসেনার ও ডিবাউন্সারে স্টেট ধরে রাখা।</li>
      </ul>

      <div class="section-subhead">🔹 Immediately Invoked Function Expressions (IIFE)</div>
      <ul style="margin: 2px 0 6px 16px; color: #334155; font-size: 10.5px;">
        <li><strong>IIFE Syntax:</strong> <code>(function() { ... })();</code> বা অ্যারো সিনট্যাক্স <code>(() => { ... })();</code></li>
        <li><strong>Private Scope:</strong> গ্লোবাল নেমস্পেসকে পলিউশন থেকে রক্ষা করা এবং ইনিশিয়ালাইজেশন কোড একবারে চালানো।</li>
      </ul>

      <div class="section-subhead">🔹 Advanced Function Patterns</div>
      <ul style="margin: 2px 0 6px 16px; color: #334155; font-size: 10.5px;">
        <li><strong>Currying:</strong> <code>f(a, b, c)</code>-কে রূপান্তর করে <code>f(a)(b)(c)</code> এ একবারে একটি আর্গুমেন্ট গ্রহণকারী ফাংশন চেইন বানানো।</li>
        <li><strong>Partial Application:</strong> কিছু আর্গুমেন্ট আগে বাইন্ড করে নতুন স্পেশালাইজড ফাংশন তৈরি করা।</li>
        <li><strong>Composition:</strong> <code>compose(f, g)(x) = f(g(x))</code> (Right to Left ডেটা ট্রান্সফরমেশন)।</li>
        <li><strong>Pipe:</strong> <code>pipe(f, g)(x) = g(f(x))</code> (Left to Right স্বাভাবিক পঠনযোগ্য ডেটা পাইপলাইন)।</li>
        <li><strong>Memoization:</strong> পূর্বের ইনপুট ও ফলাফলের ক্যাশ সংরক্ষণ করে কর্মক্ষমতা অপ্টিমাইজেশন।</li>
        <li><strong>Debounce &amp; Throttle:</strong> উচ্চ-ফ্রিকোয়েন্সি ইভেন্টকে রেট-লিমিট ও অপ্টিমাইজ করার ক্লোজার প্যাটার্ন।</li>
      </ul>
    </div>
''')

# Section 61: Quick Cheat Sheet
sec61 = raw_sections[61].strip()
cheat_codes = re.findall(r'```javascript\n([\s\S]*?)```', sec61)
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">26.Cheat</span> 🧠 Quick Cheat Sheet — Code Pattern Reference</div>
      <p class="text-p">Chapter 26-এর ৯টি প্রধান ফাংশনাল প্যাটার্নের আল্ট্রা-কম্প্যাক্ট প্রোডাকশন রেফারেন্স:</p>
      <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px;">
''')
cheat_titles = [
    "1. Closure (State Retention)",
    "2. IIFE (Immediate Execution)",
    "3. Currying (Unary Chaining)",
    "4. Function Factory",
    "5. compose() (Right to Left)",
    "6. pipe() (Left to Right)",
    "7. Memoization (Cache Store)",
    "8. Debounce Pattern",
    "9. Throttle Pattern"
]
for i, code in enumerate(cheat_codes):
    t = cheat_titles[i] if i < len(cheat_titles) else f"Pattern {i+1}"
    html_parts.append(f'''        <div>
          {render_code_box(code, title=t)}
        </div>
''')
html_parts.append('''      </div>
    </div>
''')

# Section 62: Practice Set (7 Practical Challenges with Full Production Solutions)
practice_solutions = [
    {
        "id": "Practice 1",
        "title": "Counter Closure — Private State Management",
        "req": "এমন <code>createCounter()</code> ফাংশন তৈরি করো যাতে প্রতিবার কল করলে 1, 2, 3 রিটার্ন করে এবং ভেতরের কাউন্ট বাইরে থেকে মডিফাই করা না যায়।",
        "code": """function createCounter() {
    let count = 0; // Private state
    return function() {
        count++;
        return count;
    };
}

const counter = createCounter();
console.log(counter()); // 1
console.log(counter()); // 2
console.log(counter()); // 3""",
        "output": "1\n2\n3"
    },
    {
        "id": "Practice 2",
        "title": "Private Balance — Encapsulated Bank Account",
        "req": "<code>createAccount(5000)</code> ফাংশন তৈরি করো যার মধ্যে <code>deposit(amount)</code>, <code>withdraw(amount)</code> এবং <code>getBalance()</code> মেথড থাকবে।",
        "code": """function createAccount(initialBalance) {
    let balance = initialBalance; // Encapsulated private balance

    return {
        deposit(amount) {
            balance += amount;
            return balance;
        },
        withdraw(amount) {
            if (amount <= balance) {
                balance -= amount;
            } else {
                console.log("Insufficient funds");
            }
            return balance;
        },
        getBalance() {
            return balance;
        }
    };
}

const account = createAccount(5000);
account.deposit(1000);
account.withdraw(500);
console.log("Final Balance:", account.getBalance());""",
        "output": "Final Balance: 5500"
    },
    {
        "id": "Practice 3",
        "title": "Multiplier Factory — Higher-Order Function",
        "req": "একটি <code>createMultiplier(multiplier)</code> ফাংশন ফ্যাক্টরি তৈরি করো যা নতুন মাল্টিপ্লায়ার ফাংশন জেনারেট করে।",
        "code": """const createMultiplier = multiplier => number => number * multiplier;

const triple = createMultiplier(3);
const quadruple = createMultiplier(4);

console.log("Triple 10:", triple(10));
console.log("Quadruple 5:", quadruple(5));""",
        "output": "Triple 10: 30\nQuadruple 5: 20"
    },
    {
        "id": "Practice 4",
        "title": "Currying Function — Unary Parameter Pipeline",
        "req": "কারিং স্টাইলে <code>add(10)(20)(30)</code> কল করে 60 আউটপুট পাওয়ার মতো ফাংশন তৈরি করো।",
        "code": """const add = a => b => c => a + b + c;

const result = add(10)(20)(30);
console.log("Curried Add Result:", result);

// Partial utilization
const add10 = add(10);
const add10And20 = add10(20);
console.log("Partially Applied Result:", add10And20(30));""",
        "output": "Curried Add Result: 60\nPartially Applied Result: 60"
    },
    {
        "id": "Practice 5",
        "title": "Pipeline Composition — Left-to-Right Data Flow",
        "req": "<code>double</code>, <code>add10</code>, <code>square</code> তিনটি ফাংশনকে <code>pipe()</code> দিয়ে যুক্ত করে 5 থেকে 400 ফলাফল তৈরি করো (5 → 10 → 20 → 400)।",
        "code": """const pipe = (...fns) => initialVal =>
    fns.reduce((val, fn) => fn(val), initialVal);

const double = x => x * 2;
const add10 = x => x + 10;
const square = x => x * x;

const compute = pipe(double, add10, square);

console.log("Pipeline Output (5 -> 10 -> 20 -> 400):", compute(5));""",
        "output": "Pipeline Output (5 -> 10 -> 20 -> 400): 400"
    },
    {
        "id": "Practice 6",
        "title": "Memoization Function — Cache Optimization",
        "req": "এমন <code>memoize(fn)</code> ফাংশন তৈরি করো যাতে একই আর্গুমেন্ট দিলে পূর্বে ক্যাশ করা মান ফেরত আসে এবং পুনরায় ক্যালকুলেশন না হয়।",
        "code": """function memoize(fn) {
    const cache = new Map();
    return function(...args) {
        const key = JSON.stringify(args);
        if (cache.has(key)) {
            console.log("[Cache Hit] Returning cached result for:", key);
            return cache.get(key);
        }
        console.log("[Computing] Calculating fresh result for:", key);
        const result = fn(...args);
        cache.set(key, result);
        return result;
    };
}

const slowSquare = n => n * n;
const memoizedSquare = memoize(slowSquare);

console.log(memoizedSquare(12)); // Computing
console.log(memoizedSquare(12)); // Cache Hit""",
        "output": "[Computing] Calculating fresh result for: [12]\n144\n[Cache Hit] Returning cached result for: [12]\n144"
    },
    {
        "id": "Practice 7",
        "title": "Debounce Function — Rate Limiting Keystrokes",
        "req": "একটি <code>debounce(fn, delay)</code> ফাংশন তৈরি করো যা ইউজার টাইপিং থামানোর 500ms পর এক্সিকিউট হবে।",
        "code": """function debounce(fn, delay) {
    let timer;
    return function(...args) {
        clearTimeout(timer); // Cancel previous timer
        timer = setTimeout(() => {
            fn.apply(this, args);
        }, delay);
    };
}

const performSearch = debounce(query => {
    console.log("Searching:", query);
}, 500);

// Simulating rapid user typing
performSearch("R");
performSearch("Ri");
performSearch("Rip");
performSearch("Ripon"); // Only this triggers after 500ms""",
        "output": "Searching: Ripon"
    }
]

html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">26.Lab</span> 📝 Hands-On Practice Lab — 7 Production Mastery Challenges</div>
      <p class="text-p">Closure, Currying, Composition এবং Rate Limiting কনসেপ্টগুলোকে সম্পূর্ণ আয়ত্তে আনতে নিচে ৭টি প্র্যাকটিক্যাল চ্যালেঞ্জের সম্পূর্ণ মডেল সলিউশন দেওয়া হলো:</p>
''')

for p in practice_solutions:
    html_parts.append(f'''      <div class="practice-item">
        <div style="font-weight: 700; font-size: 11px; color: var(--navy-deep); margin-bottom: 3px;">{p["id"]}: {p["title"]}</div>
        <p class="text-p" style="margin-bottom: 3px;"><strong>Problem Requirement:</strong> {p["req"]}</p>
        {render_code_box(p["code"], is_correct=True, title=f'{p["id"]} Solution')}
        {render_output_box(p["output"])}
      </div>
''')

html_parts.append('    </div>\n')

# Section 63: Final Concept Flow & Takeaway
sec63 = raw_sections[63].strip()
ascii_map_match = re.search(r'```text([\s\S]*?)```', sec63)
ascii_map = ascii_map_match.group(1).strip() if ascii_map_match else ""

html_parts.append(f'''    <div class="study-card">
      <div class="card-title"><span class="badge-num">26.Map</span> 🎯 Final Mental Map &amp; Core Architecture Flow</div>
      <p class="text-p">JavaScript Advanced Functions-এর মানসিক মডেল এবং কনসেপ্টসমূহের প্রাকৃতিক সংযোগ প্রবাহ:</p>
      {render_ascii_box(ascii_map, title="Advanced Functions Architecture & Paradigm Map")}
      
      <div class="section-subhead">⭐ এক নজরে Chapter 26 এর মূল টেক-অ্যাওয়ে</div>
      <div class="def-box" style="margin-top: 6px;">
        <div class="def-text">Key Takeaway: JavaScript-এ ফাংশন কেবল কোড এক্সিকিউট করার ব্লক নয়—ফাংশন নিজেই প্রথম-শ্রেণীর ডেটা (First-Class Citizen), যা অন্য ফাংশন তৈরি করতে পারে (Higher-Order), নিজের আশপাশের স্টেট সারাজীবন মনে রাখতে পারে (Closure), ডেটাকে সুরক্ষিত এনক্যাপসুলেশনে আবদ্ধ রাখতে পারে (Private State), এবং একাধিক স্বাধীন ফাংশনকে যুক্ত করে শক্তিশালী ও টেস্টেবল প্রসেসিং পাইপলাইন তৈরি করতে পারে।</div>
      </div>
    </div>

  </div>

</body>
</html>
''')

full_html = ''.join(html_parts)

out_file = r'c:\Users\User\Desktop\Note-Book\Code\Chapter-26-Closures-IIFE-Currying.html'
with open(out_file, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f'Successfully generated {out_file} ({len(full_html)} chars, {len(full_html.splitlines())} lines)')
