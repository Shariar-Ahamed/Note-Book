import re
import sys
import html
import subprocess
import os

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Read raw markdown
with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-27.md', 'r', encoding='utf-8') as f:
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
        ('DOM_BUILTIN', r'\b(?:console|window|document|Math|Object|Array|Date|JSON|Promise|Error|Map|Set|WeakMap|WeakSet|Symbol|performance|setTimeout|clearTimeout)\b'),
        ('GEN_METHOD', r'\b(?:next|return|throw|values|entries|keys|iterator)\b'),
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
        elif kind == 'GEN_METHOD':
            out.append(f'<span class="syn-gen" style="color: #38bdf8; font-weight: 600;">{esc}</span>')
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
        tag_label = '❌ Trap / Issue'
    elif is_correct:
        box_extra_cls = ' code-box-correct'
        tag_color = '#4ade80'
        tag_label = '✅ Standard Pattern'

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
pattern = r'\n(?=# (?:(?:🔥\s*)?27\.\d+|🧠\s*Quick Cheat Sheet|📝\s*Practice Set|🎯\s*Final Mental Map))'
raw_sections = re.split(pattern, raw_md)

print(f"Total raw sections split: {len(raw_sections)}")

# Build HTML with Classic 1-10 UI Styling + Brand JS Yellow + Prominent Chapter Title
html_parts = []
html_parts.append('''<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter 27 — Iterators &amp; Generators | JavaScript Master Study Documentation</title>
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
      #sec-27-1 {
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
          <span class="chapter-badge">Chapter 27</span>
        </div>
      </div>
      <div class="banner-sub">ITERATORS, GENERATORS &amp; CUSTOM ITERABLE ARCHITECTURE — PROTOCOLS, LAZY EVALUATION &amp; STREAMS</div>
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">Total Modules</div>
          <div class="meta-val">43 Modules + Practice Lab</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Curriculum Part</div>
          <div class="meta-val">Part 21 — Iteration Protocols &amp; Generators</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Core Mechanics</div>
          <div class="meta-val">Symbol.iterator, next(), yield &amp; Streams</div>
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
        <span>🎯</span> Iterators &amp; Generators — JavaScript Sequence &amp; Stream Architecture
      </div>
      <p class="text-p">
        JavaScript-এ ডেটা ক্রমান্বয়ে অ্যাক্সেস করার পেছনে একটি শক্তিশালী অন্তর্নিহিত মেকানিজম কাজ করে—যার নাম <strong>Iteration Protocols</strong>। এই চ্যাপ্টারে আমরা <strong>Iterable, Iterator, <code>Symbol.iterator</code>, Generator Functions (<code>function*</code>), <code>yield</code>, Lazy Evaluation</strong> এবং ইনফিনিট স্ট্রিম প্রসেসিংয়ের গভীরতম খুঁটিনাটি একদম বাস্তব উদাহরণসহ নিখুঁতভাবে শিখব।
      </p>
      <div class="roadmap-grid">
        <div class="roadmap-item"><span>📌</span> 1. Iterable Concept</div>
        <div class="roadmap-item"><span>📌</span> 2. Iterator Protocol</div>
        <div class="roadmap-item"><span>📌</span> 3. Symbol.iterator</div>
        <div class="roadmap-item"><span>📌</span> 4. next() Mechanics</div>
        <div class="roadmap-item"><span>📌</span> 5. { value, done }</div>
        <div class="roadmap-item"><span>📌</span> 6. for...of Loop Internal</div>
        <div class="roadmap-item"><span>📌</span> 7. Custom Iterators</div>
        <div class="roadmap-item"><span>📌</span> 8. Generator Function*</div>
        <div class="roadmap-item"><span>📌</span> 9. yield Operator</div>
        <div class="roadmap-item"><span>📌</span> 10. Pause &amp; Resume</div>
        <div class="roadmap-item"><span>📌</span> 11. Generator State Machine</div>
        <div class="roadmap-item"><span>📌</span> 12. Two-way next(val)</div>
        <div class="roadmap-item"><span>📌</span> 13. return() &amp; throw()</div>
        <div class="roadmap-item"><span>📌</span> 14. yield* Delegation</div>
        <div class="roadmap-item"><span>📌</span> 15. Infinite Streams</div>
        <div class="roadmap-item"><span>📌</span> 16. Lazy Evaluation</div>
        <div class="roadmap-item"><span>📌</span> 17. Fibonacci Generator</div>
        <div class="roadmap-item"><span>📌</span> 18. Range Generator</div>
        <div class="roadmap-item"><span>📌</span> 19. Custom Iterable Class</div>
        <div class="roadmap-item"><span>📌</span> 20. Object as Iterable</div>
        <div class="roadmap-item"><span>📌</span> 21. API Pagination Stream</div>
        <div class="roadmap-item"><span>📌</span> 22. Async Generators</div>
        <div class="roadmap-item"><span>📌</span> 23. Memory Optimization</div>
        <div class="roadmap-item"><span>📌</span> 24. 9 Production Challenges</div>
      </div>
    </div>
''')

def get_part_banner(num):
    if num == 1:
        return '<div class="part-banner">Part 01 — Iterables, Iteration Protocols &amp; Symbol.iterator (27.1 – 27.8)</div>'
    elif num == 9:
        return '<div class="part-banner">Part 02 — Custom Iterators &amp; Practical Sequences (27.9 – 27.13)</div>'
    elif num == 14:
        return '<div class="part-banner">Part 03 — Generators, yield Mechanics &amp; Execution Control (27.14 – 27.25)</div>'
    elif num == 26:
        return '<div class="part-banner">Part 04 — Lazy Evaluation, Streams &amp; Infinite Sequences (27.26 – 27.33)</div>'
    elif num == 34:
        return '<div class="part-banner">Part 05 — Architectural Comparisons &amp; Async Streaming (27.34 – 27.42)</div>'
    elif num == 43:
        return '<div class="part-banner">Part 06 — Production Mastery, Practice Lab &amp; Mental Map (27.43 – 27.46)</div>'
    return None

# Process all 43 numbered sections (1 to 43)
for idx in range(1, 44):
    sec_text = raw_sections[idx].strip()
    pb = get_part_banner(idx)
    if pb:
        html_parts.append(f'    {pb}\n')
        
    sec_lines = sec_text.split('\n')
    header_line = sec_lines[0]
    m_head = re.search(r'# (?:🔥\s*)?(27\.\d+)\s*(?:—|-)?\s*(.*)', header_line)
    if m_head:
        sec_num = m_head.group(1)
        sec_title = m_head.group(2)
    else:
        sec_num = f'27.{idx}'
        sec_title = header_line.replace('#', '').strip()
        
    card_extra = ''
    if idx == 1:
        card_extra = ' id="sec-27-1"'
        
    html_parts.append(f'''    <div class="study-card"{card_extra}>
      <div class="card-title"><span class="badge-num">{sec_num}</span> {inline_format(sec_title)}</div>
''')
    
    body_text = '\n'.join(sec_lines[1:]).strip()
    
    # Standard parsing with markdown table extraction and separator filtering
    chunks = re.split(r'(```[\s\S]*?```|###[^\n]+|# 🧠[^\n]+|\|[^\n]+\|\n\|[\s:-|-]+\|\n(?:\|[^\n]+\|\n?)+)', body_text)
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
                    if any(c in code_val for c in ['│', '┌', '└', '├', '──', '─', '↓', '→', '←', 'Mental', 'Iteration', 'pause', 'resume', 'generator']):
                        html_parts.append(render_ascii_box(code_val))
                    else:
                        html_parts.append(render_output_box(code_val))
                else:
                    html_parts.append(render_code_box(code_val, lang=clang, title=clang.upper()))
        elif ch_str.startswith('# 🧠'):
            sub_head = ch_str.replace('# 🧠', '').strip()
            html_parts.append(f'      <div class="section-subhead" style="color: #0369a1; border-color: #0284c7;">🧠 {inline_format(sub_head)}</div>\n')
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

# Section 44: Quick Cheat Sheet
sec44 = raw_sections[44].strip()
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">27.Cheat</span> 🧠 Quick Cheat Sheet — Iterators &amp; Generators Syntax Matrix</div>
      <p class="text-p">Iteration Protocols এবং Generator স্টেট মেশিনের দ্রুত রেফারেন্সের জন্য সম্পূর্ণ ফ্লো ও সিনট্যাক্স সামারি:</p>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px;">
        <div>
''')
ascii_cheat = """Iterable
   ↓
Symbol.iterator
   ↓
Iterator
   ↓
next()
   ↓
{ value, done }"""
html_parts.append(render_ascii_box(ascii_cheat, title="Iteration Flow"))
html_parts.append('''        </div>
        <div>
''')
code_gen_cheat = """function* numbers() {
    yield 1;
    yield 2;
    yield 3;
}

const generator = numbers();
generator.next(); // { value: 1, done: false }
generator.next(); // { value: 2, done: false }
generator.next(); // { value: 3, done: false }
generator.next(); // { value: undefined, done: true }"""
html_parts.append(render_code_box(code_gen_cheat, title="Generator Pattern"))
html_parts.append('''        </div>
      </div>
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin-top: 5px;">
        <div class="def-box" style="margin: 0;">
          <div style="font-weight: 700; font-size: 9.5px; color: #065f46;">yield</div>
          <div style="font-size: 8.5px; color: #047857;">বর্তমান মান রিটার্ন করে এবং ফাংশনের এক্সিকিউশন স্টেট সাময়িকভাবে পজ (Pause) করে।</div>
        </div>
        <div class="def-box" style="margin: 0;">
          <div style="font-weight: 700; font-size: 9.5px; color: #065f46;">next()</div>
          <div style="font-size: 8.5px; color: #047857;">পজ হওয়া জেনারেটর এক্সিকিউশনকে পুনরায় শুরু (Resume) করে পরবর্তী yield পর্যন্ত চালায়।</div>
        </div>
        <div class="def-box" style="margin: 0;">
          <div style="font-weight: 700; font-size: 9.5px; color: #065f46;">yield*</div>
          <div style="font-size: 8.5px; color: #047857;">অন্য কোনো Iterable বা Generator-এ ডেলিগেট করে তার প্রতিটি মান ধারাবাহিকভাবে yield করে।</div>
        </div>
      </div>
    </div>
''')

# Section 45: Practice Set (9 Practical Challenges with Full Production Solutions)
practice_solutions = [
    {
        "id": "Practice 1",
        "level": "Beginner",
        "title": "Static Numeric Generator",
        "req": "একটি জেনারেটর ফাংশন <code>generateTenToFifty()</code> তৈরি করো যা ক্রমান্বয়ে 10, 20, 30, 40, 50 মানগুলো <code>yield</code> দিয়ে প্রদান করবে।",
        "code": """function* generateTenToFifty() {
    yield 10;
    yield 20;
    yield 30;
    yield 40;
    yield 50;
}

const gen = generateTenToFifty();
for (const val of gen) {
    console.log(val);
}""",
        "output": "10\n20\n30\n40\n50"
    },
    {
        "id": "Practice 2",
        "level": "Beginner",
        "title": "Loop-Driven Sequence Generator",
        "req": "লুপের সাহায্যে একটি জেনারেটর ফাংশন <code>countToOneTen()</code> তৈরি করো যা 1 থেকে 10 পর্যন্ত সংখ্যা জেনারেট করবে।",
        "code": """function* countToOneTen() {
    for (let i = 1; i <= 10; i++) {
        yield i;
    }
}

const sequence = [...countToOneTen()];
console.log("Generated Sequence:", sequence);""",
        "output": "Generated Sequence: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
    },
    {
        "id": "Practice 3",
        "level": "Beginner",
        "title": "Manual Iterator Traversal",
        "req": "একটি সাধারণ অ্যারের <code>[Symbol.iterator]()</code> মেথড কল করে <code>while</code> লুপ ও <code>next()</code> দিয়ে ম্যানুয়ালি সব উপাদান প্রিন্ট করো।",
        "code": """const fruits = ["Apple", "Mango", "Banana"];

// Manually extract iterator from array
const iterator = fruits[Symbol.iterator]();

let result = iterator.next();
while (!result.done) {
    console.log(result.value);
    result = iterator.next();
}""",
        "output": "Apple\nMango\nBanana"
    },
    {
        "id": "Practice 4",
        "level": "Intermediate",
        "title": "Custom range(start, end) Generator",
        "req": "Python-এর মতো একটি <code>range(start, end)</code> জেনারেটর ফাংশন বানাও যা <code>range(5, 10)</code> কল করলে 5 থেকে 10 রিটার্ন করবে।",
        "code": """function* range(start, end) {
    for (let current = start; current <= end; current++) {
        yield current;
    }
}

for (const num of range(5, 10)) {
    console.log(num);
}""",
        "output": "5\n6\n7\n8\n9\n10"
    },
    {
        "id": "Practice 5",
        "level": "Intermediate",
        "title": "Zero-Padded User ID Generator",
        "req": "একটি ইনফিনিট আইডি জেনারেটর তৈরি করো যা কল করলে <code>USER-001</code>, <code>USER-002</code>, <code>USER-003</code> ফরম্যাটে প্যাডেড আইডি তৈরি করবে।",
        "code": """function* createUserIdGenerator(prefix = "USER") {
    let id = 1;
    while (true) {
        const formatted = String(id).padStart(3, "0");
        yield `${prefix}-${formatted}`;
        id++;
    }
}

const idGen = createUserIdGenerator();
console.log(idGen.next().value); // USER-001
console.log(idGen.next().value); // USER-002
console.log(idGen.next().value); // USER-003
console.log(idGen.next().value); // USER-004""",
        "output": "USER-001\nUSER-002\nUSER-003\nUSER-004"
    },
    {
        "id": "Practice 6",
        "level": "Intermediate",
        "title": "Fibonacci Infinite Generator",
        "req": "একটি ইনফিনিট ফিবোনাচ্চি জেনারেটর তৈরি করে তা থেকে প্রথম 10টি ফিবোনাচ্চি সংখ্যা সংগ্রহ করে প্রিন্ট করো।",
        "code": """function* fibonacci() {
    let current = 0;
    let next = 1;
    while (true) {
        yield current;
        [current, next] = [next, current + next];
    }
}

const fib = fibonacci();
const firstTen = [];
for (let i = 0; i < 10; i++) {
    firstTen.push(fib.next().value);
}

console.log("First 10 Fibonacci:", firstTen);""",
        "output": "First 10 Fibonacci: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]"
    },
    {
        "id": "Practice 7",
        "level": "Advanced",
        "title": "Dynamic Pagination Generator",
        "req": "একটি <code>paginate(items, pageSize)</code> জেনারেটর ফাংশন তৈরি করো যা বড় অ্যারে থেকে পেজ অনুযায়ী চাঙ্ক (chunks) <code>yield</code> করবে।",
        "code": """function* paginate(items, pageSize = 3) {
    for (let i = 0; i < items.length; i += pageSize) {
        yield items.slice(i, i + pageSize);
    }
}

const dataset = [101, 102, 103, 104, 105, 106, 107];
const pager = paginate(dataset, 3);

console.log("Page 1:", pager.next().value);
console.log("Page 2:", pager.next().value);
console.log("Page 3:", pager.next().value);
console.log("End:", pager.next().done);""",
        "output": "Page 1: [101, 102, 103]\nPage 2: [104, 105, 106]\nPage 3: [107]\nEnd: true"
    },
    {
        "id": "Practice 8",
        "level": "Advanced",
        "title": "Custom Iterable Class Implementation",
        "req": "একটি <code>NumberRange</code> ক্লাস তৈরি করো যা <code>[Symbol.iterator]()</code> মেথড ইমপ্লিমেন্ট করবে যাতে ক্লাসের ইন্সট্যান্স সরাসরি <code>for...of</code> সমর্থন করে।",
        "code": """class NumberRange {
    constructor(from, to) {
        this.from = from;
        this.to = to;
    }

    *[Symbol.iterator]() {
        for (let current = this.from; current <= this.to; current++) {
            yield current;
        }
    }
}

const myRange = new NumberRange(1, 5);
const collected = [...myRange];
console.log("Spread from class:", collected);""",
        "output": "Spread from class: [1, 2, 3, 4, 5]"
    },
    {
        "id": "Practice 9",
        "level": "Advanced",
        "title": "Async Generator for Streamed API Paging",
        "req": "একটি <code>async function* fetchPages(totalPages)</code> জেনারেটর তৈরি করো যা অ্যাসিঙ্ক নেটওয়ার্ক রিকোয়েস্ট সিমুলেট করে <code>for await (const page of ...)</code> দিয়ে প্রসেস হবে।",
        "code": """// Simulating asynchronous API page delay
const wait = ms => new Promise(res => setTimeout(res, ms));

async function* fetchPages(totalPages = 3) {
    for (let p = 1; p <= totalPages; p++) {
        await wait(50); // Simulated network latency
        yield { page: p, data: [`Item ${p}A`, `Item ${p}B`] };
    }
}

async function runStream() {
    for await (const pageData of fetchPages(3)) {
        console.log(`Received Page ${pageData.page}:`, pageData.data);
    }
}

runStream();""",
        "output": "Received Page 1: ['Item 1A', 'Item 1B']\nReceived Page 2: ['Item 2A', 'Item 2B']\nReceived Page 3: ['Item 3A', 'Item 3B']"
    }
]

html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">27.Lab</span> 📝 Hands-On Practice Lab — 9 Production Mastery Challenges</div>
      <p class="text-p">Iterators, Custom Iterables এবং Generators কনসেপ্টগুলোকে সম্পূর্ণ আয়ত্তে আনতে নিচে ৩টি লেভেলের ৯টি প্র্যাকটিক্যাল চ্যালেঞ্জের সম্পূর্ণ মডেল সলিউশন দেওয়া হলো:</p>
''')

for p in practice_solutions:
    lvl_color = "#059669" if p["level"] == "Beginner" else ("#d97706" if p["level"] == "Intermediate" else "#dc2626")
    html_parts.append(f'''      <div class="practice-item">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 3px;">
          <span style="font-weight: 700; font-size: 11px; color: var(--navy-deep);">{p["id"]}: {p["title"]}</span>
          <span style="background: {lvl_color}; color: white; font-size: 8px; font-weight: 700; padding: 1px 6px; border-radius: 3px; text-transform: uppercase;">{p["level"]}</span>
        </div>
        <p class="text-p" style="margin-bottom: 3px;"><strong>Problem Requirement:</strong> {p["req"]}</p>
        {render_code_box(p["code"], is_correct=True, title=f'{p["id"]} Model Solution')}
        {render_output_box(p["output"])}
      </div>
''')

html_parts.append('    </div>\n')

# Section 46: Final Mental Map
sec46 = raw_sections[46].strip()
ascii_map_match = re.search(r'```text([\s\S]*?)```', sec46)
ascii_map = ascii_map_match.group(1).strip() if ascii_map_match else ""

html_parts.append(f'''    <div class="study-card">
      <div class="card-title"><span class="badge-num">27.Map</span> 🎯 Final Mental Map &amp; Iteration Protocol Architecture</div>
      <p class="text-p">JavaScript Iteration Ecosystem-এর সম্পূর্ণ মেমরি ও কনসেপ্ট কাঠামোর চূড়ান্ত চিত্র:</p>
      {render_ascii_box(ascii_map, title="Iterators & Generators Ecosystem Map")}
      
      <div class="section-subhead">⭐ সবচেয়ে গুরুত্বপূর্ণ ৫টি Concept</div>
      <p class="text-p">যদি Chapter 27 থেকে শুধু ৫টা জিনিস মনে রাখতে চাও:</p>
      <div class="code-box output-box" style="margin: 4px 0;">
        <div class="code-top"><span class="out-label">🎯 CORE CONCEPTS TAKEAWAY</span><span>Quick Recall</span></div>
        <pre style="color: #38bdf8; font-size: 10px; line-height: 1.45; white-space: pre !important;">1️⃣ Iterable → Symbol.iterator
2️⃣ Iterator → next()
3️⃣ next() → &#123; value, done &#125;
4️⃣ Generator → function*
5️⃣ yield → value দেয় + execution pause করে</pre>
      </div>

      <div class="def-box" style="margin-top: 6px; padding: 6px 10px; background: #f0fdf4; border-left: 3px solid #10b981;">
        <div style="font-weight: 700; font-size: 10px; color: #065f46; margin-bottom: 2px;">📌 সবচেয়ে গুরুত্বপূর্ণ Relationship:</div>
        <div style="font-family: var(--font-code); font-size: 11px; font-weight: 700; color: #047857; margin: 3px 0;">
          <code>for...of</code> &nbsp;→&nbsp; Iterable &nbsp;→&nbsp; Iterator &nbsp;→&nbsp; <code>next()</code>
        </div>
        <div style="font-size: 9.5px; color: #065f46;">এটা বুঝে ফেললে Chapter 27-এর মূল concept তোমার পরিষ্কার হয়ে যাবে।</div>
      </div>
    </div>

  </div>

</body>
</html>
''')

full_html = ''.join(html_parts)

out_file = r'c:\Users\User\Desktop\Note-Book\Code\Chapter-27-Iterators-Generators.html'
with open(out_file, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f'Successfully generated {out_file} ({len(full_html)} chars, {len(full_html.splitlines())} lines)')
