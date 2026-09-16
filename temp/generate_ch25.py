import re
import sys
import html
import subprocess
import os

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Read raw markdown
with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-25.md', 'r', encoding='utf-8') as f:
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
        ('DOM_BUILTIN', r'\b(?:console|window|document|Math|Object|Array|Date|JSON|Promise|Error|Map|Set|WeakMap|WeakSet)\b'),
        ('FP_METHOD', r'\b(?:map|filter|reduce|find|some|every|flatMap|forEach|toSorted|sort|concat|slice|push|pop|shift|unshift|reverse|apply|call|bind|pipe|compose)\b'),
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
        tag_label = '❌ Mutation / Impure'
    elif is_correct:
        box_extra_cls = ' code-box-correct'
        tag_color = '#4ade80'
        tag_label = '✅ Pure / Immutable'

    display_title = title if title else "JavaScript FP"

    return f'''<div class="code-box{box_extra_cls}">
  <div class="code-top"><span style="color: {tag_color}; font-weight: 600;">{display_title}</span><span>{tag_label}</span></div>
  <pre><code>{highlighted}</code></pre>
</div>'''

def render_ascii_box(text, title="Functional Architecture"):
    text = html.escape(text.strip())
    return f'''<div class="ascii-tree-container">
<div style="color: #94a3b8; font-size: 8.5px; border-bottom: 1px solid #334155; padding-bottom: 2px; margin-bottom: 4px; text-transform: uppercase;">🧭 {title}</div>
{text}</div>'''

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
pattern = r'\n(?=# (?:(?:🔥\s*)?25\.\d+|🧠\s*Quick Cheat Sheet|📝\s*Practice Set|🎯\s*Chapter 25 Final Mental Map))'
raw_sections = re.split(pattern, raw_md)

print(f"Total raw sections split: {len(raw_sections)}")

# Build HTML with Classic 1-10 UI Styling
html_parts = []
html_parts.append('''<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter 25 — Functional JavaScript | JavaScript Master Study Documentation</title>
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

    /* Master Banner (Classic 1-10 Blue Gradient) */
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
      gap: 10px;
      margin-bottom: 3px;
    }
    .banner-icon {
      background: #ffffff;
      color: #0369a1;
      font-weight: 800;
      font-size: 12px;
      width: 26px;
      height: 26px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: var(--font-code);
    }
    .banner-title {
      font-family: var(--font-heading);
      font-size: 15px;
      font-weight: 800;
      letter-spacing: 0.3px;
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

    /* Opening Statement Card */
    .opening-card {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-left: 4px solid var(--blue-accent);
      border-radius: 6px;
      padding: 8px 12px;
      margin-bottom: 6px;
    }
    .opening-title {
      font-family: var(--font-heading);
      font-size: 11.5px;
      font-weight: 700;
      color: var(--navy-deep);
      margin-bottom: 3px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    /* Part Banner */
    .part-banner {
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
      color: #f8fafc;
      padding: 6px 12px;
      font-family: var(--font-heading);
      font-size: 11px;
      font-weight: 700;
      border-radius: 5px;
      margin-top: 8px;
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
      margin: 3px 0;
      overflow: hidden;
      border: 1px solid #1e293b;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }
    .code-box-error {
      border: 1px solid #f87171 !important;
    }
    .code-box-correct {
      border: 1px solid #4ade80 !important;
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
      color: #38bdf8;
      font-family: var(--font-code);
      font-size: 9px;
      line-height: 1.25;
      padding: 6px 10px;
      border-radius: 5px;
      margin: 4px 0;
      white-space: pre;
      overflow-x: hidden !important;
      border: 1px solid #1e293b;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }

    /* Practice Items */
    .practice-item {
      page-break-inside: avoid !important;
      break-inside: avoid !important;
      margin-bottom: 6px;
      padding: 7px 10px;
      background: #f8fafc;
      border-left: 3px solid var(--blue-accent);
      border-radius: 5px;
    }

    @page {
      size: A4;
      margin: 8mm 10mm;
    }

    @media print {
      body {
        background: white !important;
        font-size: 11px;
        color: #0f172a !important;
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
      #sec-25-1 {
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
      <span style="color:#0284c7;">⚡</span> JS MASTER STUDY DOCUMENTATION
    </div>
    <button class="print-btn" onclick="window.print()">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
      Print / Save as PDF
    </button>
  </div>

  <div class="doc-page">

    <!-- Header Master Banner (Classic 1-10 Style) -->
    <header class="master-banner">
      <div class="banner-top">
        <div class="banner-icon">JS</div>
        <div class="banner-title">JavaScript Master Study Documentation</div>
      </div>
      <div class="banner-sub">CHAPTER 25: FUNCTIONAL JAVASCRIPT — PURE FUNCTIONS, IMMUTABILITY &amp; DATA PIPELINES</div>
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">Total Modules</div>
          <div class="meta-val">50 Modules + Practice Lab</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Curriculum Part</div>
          <div class="meta-val">Part 19 — Functional Paradigm &amp; Patterns</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Core Mechanics</div>
          <div class="meta-val">Pure Functions, Immutability &amp; HOFs</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Reference Standard</div>
          <div class="meta-val">ECMAScript 2026 / Modern Functional JS</div>
        </div>
      </div>
    </header>

    <!-- Chapter Opening Statement (Page 1 Balance) -->
    <div class="opening-card">
      <div class="opening-title">
        <span>🎯</span> Functional Programming (FP) — Functional JavaScript শেখার মূল উদ্দেশ্য
      </div>
      <p class="text-p">
        JavaScript-এ <strong>Functional Programming</strong> অত্যন্ত গুরুত্বপূর্ণ—বিশেষ করে তুমি যখন <strong>React, Redux, Node.js এবং Modern Full-Stack</strong> ইকোসিস্টেমে কাজ করবে। এই চ্যাপ্টারে আমরা শুধুমাত্র <code>map()</code> বা <code>filter()</code> নয়, বরং Functional JavaScript-এর গভীরতম ভিত্তিগুলো—Pure Functions, Immutability, Composition, Currying এবং Declarative Data Pipelines—নিখুঁতভাবে শিখব।
      </p>
      <div class="def-box" style="margin: 3px 0; padding: 4px 8px;">
        <div class="def-text">Core Formula: Input Data &nbsp;→&nbsp; Pure Function (No Side Effect) &nbsp;→&nbsp; New Immutable Output Data</div>
      </div>
    </div>
''')

def get_part_banner(num):
    if num == 1:
        return '<div class="part-banner">Part 01 — Functional Programming Fundamentals &amp; Pure Functions (25.1 – 25.9)</div>'
    elif num == 10:
        return '<div class="part-banner">Part 02 — Immutability, First-Class &amp; Higher-Order Functions (25.10 – 25.16)</div>'
    elif num == 17:
        return '<div class="part-banner">Part 03 — Core Array Transformations: map, filter &amp; reduce (25.17 – 25.24)</div>'
    elif num == 25:
        return '<div class="part-banner">Part 04 — Advanced FP: Composition, Pipe, Currying &amp; Closures (25.25 – 25.35)</div>'
    elif num == 36:
        return '<div class="part-banner">Part 05 — Mutation Prevention, Search Methods &amp; Real Pipelines (25.36 – 25.49)</div>'
    elif num == 50:
        return '<div class="part-banner">Part 06 — FP Mastery: Must Know, Quick Cheat Sheet, Practice Lab &amp; Mental Map</div>'
    return None

for idx in range(1, 51):
    sec_text = raw_sections[idx].strip()
    pb = get_part_banner(idx)
    if pb:
        html_parts.append(f'    {pb}\n')
        
    sec_lines = sec_text.split('\n')
    header_line = sec_lines[0]
    m_head = re.search(r'# (?:🔥\s*)?(25\.\d+)\s*(?:—|-)?\s*(.*)', header_line)
    if m_head:
        sec_num = m_head.group(1)
        sec_title = m_head.group(2)
    else:
        sec_num = f'25.{idx}'
        sec_title = header_line.replace('#', '').strip()
        
    card_extra = ''
    if idx == 1:
        card_extra = ' id="sec-25-1"'
        
    html_parts.append(f'''    <div class="study-card"{card_extra}>
      <div class="card-title"><span class="badge-num">{sec_num}</span> {inline_format(sec_title)}</div>
''')
    
    body_text = '\n'.join(sec_lines[1:]).strip()
    
    # Check for mutation comparison in 25.36
    if idx == 36 and '❌ Mutation' in body_text:
        invalid_c = "const numbers = [1, 2, 3];\nnumbers.push(4); // ❌ Original array সরাসরি mutate হয়ে গেছে!"
        correct_c = "const numbers = [1, 2, 3];\nconst newNumbers = [...numbers, 4]; // ✅ মূল array অক্ষত রেখে নতুন array রিটার্ন"
        html_parts.append(f'''      <p class="text-p">Functional Programming-এর প্রধান শর্ত হলো বিদ্যমান ডেটা সরাসরি পরিবর্তন (mutate) না করা।</p>
      {render_code_box(invalid_c, is_invalid=True, invalid_token='numbers.push(4)', title='❌ ভুল পদ্ধতি: Mutation (Side Effect)')}
      <div class="warn-box">
        <strong>সতর্কতা:</strong> <code>push()</code> মেথড মূল অ্যারে পরিবর্তন করে ফেলে, যার ফলে অ্যাপ্লিকেশনের স্টেট অপ্রত্যাশিতভাবে বদলে যেতে পারে।
      </div>
      <p class="text-p"><strong>সঠিক সমাধান (Immutable Style):</strong> Spread operator (<code>...</code>) ব্যবহার করে নতুন কপি তৈরি করুন।</p>
      {render_code_box(correct_c, is_correct=True, title='✅ সঠিক পদ্ধতি: Immutability (Pure Pattern)')}
''')
    elif idx == 37:
        mut_sort = "const numbers = [3, 1, 2];\nconst sorted = numbers.sort(); // ❌ মূল numbers অ্যারেও sort হয়ে যাবে!"
        pure_sort1 = "const numbers = [3, 1, 2];\nconst sorted = [...numbers].sort((a, b) => a - b); // ✅ Spread কপি করে sort\nconsole.log(numbers); // [3, 1, 2]\nconsole.log(sorted);  // [1, 2, 3]"
        pure_sort2 = "// Modern ES2023+ Native Immutable Method:\nconst sortedNative = numbers.toSorted((a, b) => a - b); // ✅ মূল অ্যারে অক্ষত থাকে"
        html_parts.append(f'''      <p class="text-p">একটি বহুল পরিচিত ট্রিকি বিষয় হলো জাভাস্ক্রিপ্টের বিল্ট-ইন <code>sort()</code> মেথড মূল অ্যারে মিউটেট করে।</p>
      {render_code_box(mut_sort, is_invalid=True, invalid_token='numbers.sort()', title='❌ Mutating Sort: মূল অ্যারে নষ্ট করে')}
      <p class="text-p"><strong>Functional সমাধান ১:</strong> স্প্রেড অপারেটর দিয়ে কপি বানিয়ে সর্ট করা:</p>
      {render_code_box(pure_sort1, is_correct=True, title='✅ Safe Pattern: [...numbers].sort()')}
      <p class="text-p"><strong>Functional সমাধান ২ (ES2023+ Standard):</strong> আধুনিক <code>toSorted()</code> মেথড ব্যবহার করা:</p>
      {render_code_box(pure_sort2, is_correct=True, title='✅ Modern Pattern: toSorted()')}
''')
    else:
        # Standard parsing with markdown table extraction and dash filtering
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
                        if any(c in code_val for c in ['│', '┌', '└', '├', '──', '─', '↓', '→', 'Functional']):
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

# Section 51: Quick Cheat Sheet
sec51 = raw_sections[51].strip()
m_table = re.search(r'(\|[\s\S]*\|)', sec51)
if m_table:
    html_parts.append(f'''    <div class="study-card">
      <div class="card-title"><span class="badge-num">25.Quick</span> 🧠 Quick Cheat Sheet — Functional JavaScript Reference</div>
      <p class="text-p">Functional JavaScript এবং ডেটা রূপান্তরের দ্রুত রেফারেন্সের জন্য সম্পূর্ণ সিনট্যাক্স টেবিল:</p>
      {render_table(m_table.group(1))}
    </div>
''')

# Section 52: Practice Set
practice_solutions = [
    {
        "id": "Practice 1",
        "title": "Double with map() — Immutable Numeric Transformation",
        "req": "<code>numbers = [2, 4, 6, 8]</code> অ্যারে থেকে <code>map()</code> ব্যবহার করে প্রতিটি সংখ্যাকে দ্বিগুণ করে <code>[4, 8, 12, 16]</code> নতুন অ্যারে তৈরি করুন।",
        "code": """const numbers = [2, 4, 6, 8];

// Pure transformation using map()
const doubled = numbers.map(num => num * 2);

console.log("Original:", numbers);
console.log("Doubled:", doubled);""",
        "output": "Original: [2, 4, 6, 8]\nDoubled: [4, 8, 12, 16]"
    },
    {
        "id": "Practice 2",
        "title": "Filter Condition — Selecting Elements >= 20",
        "req": "<code>numbers = [10, 15, 20, 25, 30, 35]</code> থেকে <code>filter()</code> ব্যবহার করে শুধুমাত্র ২০ বা তার বেশি সংখ্যাগুলো ফিল্টার করে বের করুন।",
        "code": """const numbers = [10, 15, 20, 25, 30, 35];

// Declarative filtering with pure predicate
const filtered = numbers.filter(num => num >= 20);

console.log("Result:", filtered);""",
        "output": "Result: [20, 25, 30, 35]"
    },
    {
        "id": "Practice 3",
        "title": "Reduce Accumulation — Calculating Array Total",
        "req": "<code>numbers = [10, 20, 30, 40]</code> থেকে <code>reduce()</code> ব্যবহার করে মোট যোগফল <code>100</code> বের করুন।",
        "code": """const numbers = [10, 20, 30, 40];

// Sum accumulation with initial value 0
const total = numbers.reduce((accumulator, current) => accumulator + current, 0);

console.log("Total Sum:", total);""",
        "output": "Total Sum: 100"
    },
    {
        "id": "Practice 4",
        "title": "Passed Students Filter — Object Array Query",
        "req": "শিক্ষার্থীদের তালিকা থেকে <code>filter()</code> ব্যবহার করে শুধুমাত্র পাস করা শিক্ষার্থীদের (<code>marks >= 40</code>) আলাদা করুন।",
        "code": """const students = [
  { name: "A", marks: 80 },
  { name: "B", marks: 35 },
  { name: "C", marks: 70 },
  { name: "D", marks: 45 },
];

const passedStudents = students.filter(student => student.marks >= 40);

console.log("Passed Students:", passedStudents);""",
        "output": "Passed Students: [\n  { name: 'A', marks: 80 },\n  { name: 'C', marks: 70 },\n  { name: 'D', marks: 45 }\n]"
    },
    {
        "id": "Practice 5",
        "title": "Functional Pipeline — filter() + map() + reduce() Chain",
        "req": "পণ্য তালিকা থেকে: ১. স্টকে থাকা পণ্য নির্বাচন করুন (<code>stock > 0</code>), ২. তাদের মূল্য বের করুন, এবং ৩. মোট স্টক পণ্যের মূল্য বের করতে মেথড চেইনিং পাইপলাইন তৈরি করুন।",
        "code": """const products = [
  { name: "Laptop", price: 80000, stock: 5 },
  { name: "Mouse", price: 1000, stock: 0 },
  { name: "Monitor", price: 20000, stock: 3 },
];

// Clean functional data pipeline
const totalInStockPrice = products
  .filter(item => item.stock > 0)
  .map(item => item.price * item.stock)
  .reduce((sum, currentVal) => sum + currentVal, 0);

console.log("Total In-Stock Value: ৳", totalInStockPrice);""",
        "output": "Total In-Stock Value: ৳ 460000"
    }
]

html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">25.Lab</span> 📝 Hands-On Practice Lab — 5 Real-World Functional Challenges</div>
      <p class="text-p">Functional Programming-এর কনসেপ্টগুলোকে আত্মস্থ করার জন্য নিচে বাস্তবভিত্তিক ৫টি চ্যালেঞ্জের সম্পূর্ণ প্রোডাকশন সলিউশন দেওয়া হলো:</p>
''')

for p in practice_solutions:
    html_parts.append(f'''      <div class="practice-item">
        <div style="font-weight: 700; font-size: 11px; color: var(--navy-deep); margin-bottom: 3px;">{p["id"]}: {p["title"]}</div>
        <p class="text-p" style="margin-bottom: 3px;"><strong>Problem Requirement:</strong> {p["req"]}</p>
        {render_code_box(p["code"], is_correct=True, title=f'{p["id"]} Model Solution')}
        {render_output_box(p["output"])}
      </div>
''')

html_parts.append('    </div>\n')

# Section 53: Final Mental Map
sec53 = raw_sections[53].strip()
ascii_map_match = re.search(r'```text([\s\S]*?)```', sec53)
ascii_map = ascii_map_match.group(1).strip() if ascii_map_match else ""

html_parts.append(f'''    <div class="study-card">
      <div class="card-title"><span class="badge-num">25.Map</span> 🎯 Final Mental Map &amp; Functional Ecosystem</div>
      <p class="text-p">JavaScript Functional Programming-এর সামগ্রিক আর্কিটেকচার এবং মেথড প্রবাহের চূড়ান্ত চিত্র:</p>
      {render_ascii_box(ascii_map, title="Functional JavaScript Master Architecture Tree")}
      
      <div class="section-subhead">⭐ এক নজরে Chapter 25 এর সারসংক্ষেপ</div>
      <div class="def-box" style="margin-top: 6px;">
        <div class="def-text">Key Takeaway: Functional JavaScript হলো ডেটাকে ছোট, রিইউজেবল ও প্রেডিক্টেবল ফাংশনের পাইপলাইনে রূপান্তর করার শিল্প—যেখানে Pure Functions, Immutability এবং map/filter/reduce-এর মতো হায়ার-অর্ডার ফাংশনগুলো কোডকে বাগ-মুক্ত, টেস্টেবল এবং সহজে মেইনটেনেবল করে তোলে।</div>
      </div>
    </div>

  </div>

</body>
</html>
''')

full_html = ''.join(html_parts)

out_file = r'c:\Users\User\Desktop\Note-Book\Code\Chapter-25-Functional-JavaScript.html'
with open(out_file, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f'Successfully generated {out_file} ({len(full_html)} chars, {len(full_html.splitlines())} lines)')
