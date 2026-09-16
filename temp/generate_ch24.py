import re
import sys
import html
import subprocess
import os

sys.stdout.reconfigure(encoding='utf-8')

# 1. Read source markdown
with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-24.md', 'r', encoding='utf-8') as f:
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
        ('PRIVATE_FIELD', r'#[a-zA-Z_$][a-zA-Z0-9_$]*'),
        ('KEYWORD', r'\b(?:for|while|do|break|continue|if|else|let|const|var|function|return|switch|case|default|of|in|new|typeof|delete|this|super|class|extends|static|instanceof|try|catch|finally|throw|await|async|yield|debugger|import|export|from|as|get|set)\b'),
        ('BOOL_NULL', r'\b(?:true|false|null|undefined|NaN)\b'),
        ('CLASS_NAME', r'\b[A-Z][a-zA-Z0-9_$]*\b'),
        ('DOM_BUILTIN', r'\b(?:console|window|document|Math|Object|Array|Date|JSON|Promise|Error|Map|Set|WeakMap|WeakSet|Reflect|Proxy)\b'),
        ('METHOD_CALL', r'\b[a-zA-Z_$][a-zA-Z0-9_$]*(?=\s*\()'),
        ('NUMBER', r'\b\d+(?:\.\d+)?\b'),
        ('OTHER', r'[^\s\w]+|\w+|\s+'),
    ]
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
    
    out = []
    for mo in re.finditer(tok_regex, code_str, flags=re.MULTILINE):
        kind = mo.lastgroup
        val = mo.group()
        esc = html.escape(val)
        
        # Check if token is marked as invalid
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
        elif kind == 'CLASS_NAME':
            out.append(f'<span class="syn-class" style="color: #fb923c; font-weight: 600;">{esc}</span>')
        elif kind == 'PRIVATE_FIELD':
            out.append(f'<span class="syn-priv" style="color: #f472b6; font-weight: 600;">{esc}</span>')
        elif kind == 'DOM_BUILTIN':
            out.append(f'<span class="syn-fn">{esc}</span>')
        elif kind == 'METHOD_CALL':
            out.append(f'<span class="syn-fn" style="color: #38bdf8;">{esc}</span>')
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
        tag_label = '❌ Error / Invalid'
    elif is_correct:
        box_extra_cls = ' code-box-correct'
        tag_color = '#4ade80'
        tag_label = '✅ Correct'

    display_title = title if title else "JavaScript"

    return f'''<div class="code-box{box_extra_cls}">
  <div class="code-top"><span style="color: {tag_color}; font-weight: 600;">{display_title}</span><span>{tag_label}</span></div>
  <pre><code>{highlighted}</code></pre>
</div>'''

def render_ascii_box(text, title="Concept Architecture"):
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
pattern = r'\n(?=# (?:(?:🔥\s*)?24\.\d+|🧠\s*Quick Cheat Sheet|📝\s*Practice Set|🎯\s*Final Mental Map))'
raw_sections = re.split(pattern, raw_md)

# Extract learning goals from section 0
sec0 = raw_sections[0].strip()
goals_match = re.search(r'# 🎯 Chapter 24 Learning Goals\s*([\s\S]*?)$', sec0)
learning_goals = []
if goals_match:
    for g in re.findall(r'^\*\s*(.*)$', goals_match.group(1), re.M):
        learning_goals.append(g.strip())

# Build HTML
html_parts = []
html_parts.append('''<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter 24 — OOP &amp; JavaScript Classes | JavaScript Master Study Documentation</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Hind+Siliguri:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --navy-deep: #0f172a;
      --navy-mid: #1e293b;
      --navy-light: #334155;
      --blue-accent: #0284c7;
      --blue-light: #e0f2fe;
      --blue-dark: #0369a1;
      --purple-accent: #6366f1;
      --purple-light: #ede9fe;
      --emerald: #059669;
      --amber: #d97706;
      --rose: #e11d48;
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

    /* Master Banner */
    .master-banner {
      background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%);
      color: white;
      padding: 12px 16px;
      border-radius: 8px;
      margin-bottom: 8px;
      box-shadow: 0 4px 12px rgba(49, 46, 129, 0.25);
    }
    .banner-top {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 3px;
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
      border-left: 4px solid var(--purple-accent);
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
    .goals-flex {
      display: flex;
      flex-wrap: wrap;
      gap: 4px 6px;
      margin-top: 6px;
    }
    .goal-tag {
      background: #ede9fe;
      border: 1px solid #ddd6fe;
      color: #5b21b6;
      padding: 1px 6px;
      border-radius: 4px;
      font-size: 9.5px;
      font-weight: 600;
      white-space: nowrap;
    }
    .goal-tag::before {
      content: "✓ ";
      color: #059669;
      font-weight: 700;
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
      border-left: 4px solid #6366f1;
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
      background: var(--purple-accent);
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
      border-left: 2px solid var(--purple-accent);
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
      border-left: 3px solid var(--purple-accent);
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
      #sec-24-1 {
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
      .code-box, pre, .ascii-tree-container, .table-wrap, .def-box, .output-box {
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
      <span style="color:#6366f1;">⚡</span> JS MASTER STUDY DOCUMENTATION
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
      <div class="banner-sub">CHAPTER 24: OOP &amp; JAVASCRIPT CLASSES — OBJECT MODELING, INHERITANCE &amp; ARCHITECTURE</div>
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">Total Modules</div>
          <div class="meta-val">50 Modules + Practice Lab</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Curriculum Part</div>
          <div class="meta-val">Part 18 — Object-Oriented Architecture</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Core Mechanics</div>
          <div class="meta-val">Classes, Encapsulation, Extends &amp; Super</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Reference Standard</div>
          <div class="meta-val">ECMAScript 2026 / OOP Class Fields</div>
        </div>
      </div>
    </header>

    <!-- Chapter Opening Statement (Page 1 Balance) -->
    <div class="opening-card">
      <div class="opening-title">
        <span>🎯</span> Chapter 24 — OOP Architecture &amp; Core Learning Roadmap
      </div>
      <p class="text-p">
        OOP (Object-Oriented Programming) হলো আধুনিক সফটওয়্যার ইঞ্জিনিয়ারিংয়ের মূল ভিত্তি। বিশেষ করে <strong>React, Node.js, Express, NestJS, এবং large-scale enterprise application</strong> ডেভেলপমেন্টে পরিষ্কার ডেটা মডেলিং এবং মডুলার কোড স্ট্রাকচার সাজাতে ক্লাস এবং অবজেক্টের কনসেপ্ট অপরিহার্য। এই চ্যাপ্টারে আমরা একদম গ্রাউন্ড লেভেল থেকে ইন্টারনাল প্রোটোটাইপ মেকানিজম পর্যন্ত নিখুঁতভাবে শিখব।
      </p>
      <div class="goals-flex">
''')

for g in learning_goals:
    html_parts.append(f'        <span class="goal-tag">{inline_format(g)}</span>\n')

html_parts.append('''      </div>
    </div>
''')

def get_part_banner(num):
    if num == 1:
        return '<div class="part-banner">Part 01 — OOP Fundamentals, Objects &amp; Class Syntax (24.1 – 24.10)</div>'
    elif num == 11:
        return '<div class="part-banner">Part 02 — Methods, Properties, Accessors &amp; Encapsulation (24.11 – 24.23)</div>'
    elif num == 24:
        return '<div class="part-banner">Part 03 — Inheritance, Polymorphism, Abstraction &amp; Composition (24.24 – 24.33)</div>'
    elif num == 34:
        return '<div class="part-banner">Part 04 — Under the Hood: Prototypes, Class Fields &amp; Practical Architecture (24.34 – 24.43)</div>'
    elif num == 44:
        return '<div class="part-banner">Part 05 — Common Mistakes, Edge Cases &amp; Mental Models (24.44 – 24.49)</div>'
    elif num == 50:
        return '<div class="part-banner">Part 06 — OOP Mastery: Must Know, Quick Cheat Sheet, Practice Lab &amp; Mental Map</div>'
    return None

for idx in range(1, 51):
    sec_text = raw_sections[idx].strip()
    pb = get_part_banner(idx)
    if pb:
        html_parts.append(f'    {pb}\n')
        
    sec_lines = sec_text.split('\n')
    header_line = sec_lines[0]
    m_head = re.search(r'# (?:🔥\s*)?(24\.\d+)\s*—\s*(.*)', header_line)
    if m_head:
        sec_num = m_head.group(1)
        sec_title = m_head.group(2)
    else:
        sec_num = f'24.{idx}'
        sec_title = header_line.replace('#', '').strip()
        
    card_extra = ''
    if idx == 1:
        card_extra = ' id="sec-24-1"'
        
    html_parts.append(f'''    <div class="study-card"{card_extra}>
      <div class="card-title"><span class="badge-num">{sec_num}</span> {inline_format(sec_title)}</div>
''')
    
    body_text = '\n'.join(sec_lines[1:]).strip()
    
    if idx in [44, 45, 46, 47, 48]:
        if idx == 44:
            invalid_c = "class Student {}\n\nconst student = Student();"
            correct_c = "class Student {}\n\nconst student = new Student();"
            html_parts.append(f'''      <p class="text-p">Class constructor কখনো <code>new</code> কীওয়ার্ড ছাড়া সরাসরি ফাংশনের মতো কল করা যায় না। এভাবে কল করলে <code>TypeError</code> ছুঁড়ে দেয়।</p>
      {render_code_box(invalid_c, is_invalid=True, invalid_token='Student()', title='ভুল পদ্ধতি: new কীওয়ার্ড ছাড়া কল')}
      <div class="code-box output-box" style="border-left-color: #ef4444;">
        <div class="code-top"><span style="color: #f87171;">✖ RUNTIME ERROR</span><span>TypeError</span></div>
        <pre>TypeError: Class constructor Student cannot be invoked without 'new'</pre>
      </div>
      <p class="text-p"><strong>সঠিক সমাধান:</strong> অবজেক্ট ইনস্ট্যান্স তৈরি করতে সর্বদা <code>new</code> ব্যবহার করুন।</p>
      {render_code_box(correct_c, is_correct=True, title='সঠিক পদ্ধতি: new ব্যবহার')}
''')
        elif idx == 45:
            invalid_c = "class Animal {\n    constructor(name) {\n        this.name = name;\n    }\n}\n\nclass Dog extends Animal {\n    constructor(name, breed) {\n        this.breed = breed;\n    }\n}"
            correct_c = "class Animal {\n    constructor(name) {\n        this.name = name;\n    }\n}\n\nclass Dog extends Animal {\n    constructor(name, breed) {\n        super(name);\n        this.breed = breed;\n    }\n}"
            html_parts.append(f'''      <p class="text-p">Inheritance ব্যবহার করার সময় চাইল্ড ক্লাসের <code>constructor</code>-এ <code>this</code> অ্যাক্সেস করার পূর্বে অবশ্যই প্যারেন্ট ক্লাসের <code>super()</code> কল করতে হবে।</p>
      {render_code_box(invalid_c, is_invalid=True, invalid_token='this.breed = breed;', title='ভুল পদ্ধতি: super() না ডেকে this অ্যাক্সেস')}
      <div class="code-box output-box" style="border-left-color: #ef4444;">
        <div class="code-top"><span style="color: #f87171;">✖ REFERENCE ERROR</span><span>ReferenceError</span></div>
        <pre>ReferenceError: Must call super constructor in derived class before accessing 'this'</pre>
      </div>
      <p class="text-p"><strong>সঠিক সমাধান:</strong> প্যারেন্ট কনস্ট্রাক্টরে প্যারামিটার পাস করতে প্রথমে <code>super(...)</code> কল করুন।</p>
      {render_code_box(correct_c, is_correct=True, title='সঠিক পদ্ধতি: super(name) কল')}
''')
        elif idx == 46:
            invalid_c = "class User {\n    #password = \"12345\";\n}\n\nconst user = new User();\nconsole.log(user.#password);"
            correct_c = "class User {\n    #password = \"12345\";\n\n    verifyPassword(input) {\n        return this.#password === input;\n    }\n}\n\nconst user = new User();\nconsole.log(user.verifyPassword(\"12345\")); // true"
            html_parts.append(f'''      <p class="text-p">Private field (<code>#field</code>) ক্লাসের বাইরে থেকে সরাসরি ডট নোটেশনে অ্যাক্সেস করা যায় না। এটি করলে সিনট্যাক্স এরর দেয়।</p>
      {render_code_box(invalid_c, is_invalid=True, invalid_token='user.#password', title='ভুল পদ্ধতি: ক্লাসের বাইরে Private Field অ্যাক্সেস')}
      <div class="code-box output-box" style="border-left-color: #ef4444;">
        <div class="code-top"><span style="color: #f87171;">✖ SYNTAX ERROR</span><span>SyntaxError</span></div>
        <pre>SyntaxError: Private field '#password' must be declared in an enclosing class</pre>
      </div>
      <p class="text-p"><strong>সঠিক সমাধান:</strong> ক্লাসের নিজস্ব মেথড বা গেটারের মাধ্যমে প্রাইভেট ডেটা ভ্যালিডেট বা এক্সেস করুন।</p>
      {render_code_box(correct_c, is_correct=True, title='সঠিক পদ্ধতি: মেথডের মাধ্যমে এক্সেস')}
''')
        elif idx == 47:
            invalid_c = "class Test {\n    static hello() {\n        console.log(\"Hello\");\n    }\n}\n\nconst test = new Test();\ntest.hello();"
            correct_c = "class Test {\n    static hello() {\n        console.log(\"Hello\");\n    }\n}\n\nTest.hello(); // Hello"
            html_parts.append(f'''      <p class="text-p">Static method সরাসরি ক্লাসের প্রপার্টি, এটি ইনস্ট্যান্স অবজেক্টে উত্তরাধিকারসূত্রে থাকে না। অবজেক্ট ইনস্ট্যান্স দিয়ে কল করলে TypeError দেয়।</p>
      {render_code_box(invalid_c, is_invalid=True, invalid_token='test.hello()', title='ভুল পদ্ধতি: অবজেক্ট দিয়ে Static মেথড কল')}
      <div class="code-box output-box" style="border-left-color: #ef4444;">
        <div class="code-top"><span style="color: #f87171;">✖ TYPE ERROR</span><span>TypeError</span></div>
        <pre>TypeError: test.hello is not a function</pre>
      </div>
      <p class="text-p"><strong>সঠিক সমাধান:</strong> সরাসরি ক্লাসের নাম ধরে কল করুন: <code>Test.hello()</code></p>
      {render_code_box(correct_c, is_correct=True, title='সঠিক পদ্ধতি: ক্লাসের নাম ধরে কল')}
''')
        elif idx == 48:
            invalid_c = "class Student {\n    constructor(name) {\n        name = name; // প্যারামিটার নিজের উপর অ্যাসাইন হচ্ছে, ইনস্ট্যান্সে নয়!\n    }\n}\n\nconst s = new Student(\"Shariar\");\nconsole.log(s.name); // undefined"
            correct_c = "class Student {\n    constructor(name) {\n        this.name = name; // ইনস্ট্যান্স অবজেক্টে প্রপার্টি সেট হলো\n    }\n}\n\nconst s = new Student(\"Shariar\");\nconsole.log(s.name); // 'Shariar'"
            html_parts.append(f'''      <p class="text-p">কনস্ট্রাক্টরের ভেতর <code>this.property = value</code> না লিখলে অবজেক্টের প্রপার্টি ইনিশিয়ালাইজ হয় না; শুধু লোকাল ভেরিয়েবল অ্যাসাইন হয়।</p>
      {render_code_box(invalid_c, is_invalid=True, invalid_token='name = name;', title='ভুল পদ্ধতি: this ছাড়া নাম অ্যাসাইন')}
      <div class="code-box output-box" style="border-left-color: #ef4444;">
        <div class="code-top"><span style="color: #f87171;">▶ OUTPUT MISMATCH</span><span>Undefined</span></div>
        <pre>undefined</pre>
      </div>
      <p class="text-p"><strong>সঠিক সমাধান:</strong> অবজেক্টের প্রপার্টি সেট করতে সর্বদা <code>this.name</code> ব্যবহার করুন।</p>
      {render_code_box(correct_c, is_correct=True, title='সঠিক পদ্ধতি: this.name ব্যবহার')}
''')
    else:
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
                        if any(c in code_val for c in ['│', '┌', '└', '├', '──', '─', '↓', '→', 'OOP']):
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
      <div class="card-title"><span class="badge-num">24.Quick</span> 🧠 Quick Cheat Sheet — Class &amp; OOP Syntax Reference</div>
      <p class="text-p">JavaScript Class এবং Object-Oriented Programming এর দ্রুত রেফারেন্সের জন্য সম্পূর্ণ সিনট্যাক্স টেবিল:</p>
      {render_table(m_table.group(1))}
    </div>
''')

# Section 52: Practice Set
practice_solutions = [
    {
        "id": "Practice 1",
        "level": "Beginner",
        "title": "Car Class — Brand, Model, Year & showInfo() Method",
        "req": "<code>Car</code> নামে একটি ক্লাস বানান যাতে <code>brand</code>, <code>model</code>, <code>year</code> প্রোপার্টি থাকবে এবং <code>showInfo()</code> মেথড গাড়ির সম্পূর্ণ বিবরণ প্রিন্ট করবে।",
        "code": """class Car {
    constructor(brand, model, year) {
        this.brand = brand;
        this.model = model;
        this.year = year;
    }

    showInfo() {
        console.log(`Car Info: ${this.brand} ${this.model} (${this.year})`);
    }
}

// Verification
const myCar = new Car("Toyota", "Camry", 2024);
myCar.showInfo();""",
        "output": "Car Info: Toyota Camry (2024)"
    },
    {
        "id": "Practice 2",
        "level": "Beginner",
        "title": "Student Class — Name, ID, Department & introduce() Method",
        "req": "<code>Student</code> নামে একটি ক্লাস বানান যাতে <code>name</code>, <code>id</code>, <code>department</code> প্রোপার্টি থাকবে এবং <code>introduce()</code> মেথড শিক্ষার্থীর পরিচয় প্রিন্ট করবে।",
        "code": """class Student {
    constructor(name, id, department) {
        this.name = name;
        this.id = id;
        this.department = department;
    }

    introduce() {
        console.log(`Hello, I am ${this.name}, ID: ${this.id}, Department of ${this.department}.`);
    }
}

// Verification
const s1 = new Student("Rahim Ahmed", "CSE-1024", "Computer Science");
s1.introduce();""",
        "output": "Hello, I am Rahim Ahmed, ID: CSE-1024, Department of Computer Science."
    },
    {
        "id": "Practice 3",
        "level": "Beginner",
        "title": "Rectangle Class — Width, Height, area() & perimeter() Calculation",
        "req": "<code>Rectangle</code> নামে একটি ক্লাস বানান যার <code>width</code> ও <code>height</code> প্রোপার্টি থাকবে এবং আয়তক্ষেত্রের ক্ষেত্রফল ও পরিসীমা নির্ণয়ের জন্য <code>area()</code> ও <code>perimeter()</code> মেথড থাকবে।",
        "code": """class Rectangle {
    constructor(width, height) {
        this.width = width;
        this.height = height;
    }

    area() {
        return this.width * this.height;
    }

    perimeter() {
        return 2 * (this.width + this.height);
    }
}

// Verification
const rect = new Rectangle(10, 5);
console.log("Area:", rect.area());
console.log("Perimeter:", rect.perimeter());""",
        "output": "Area: 50\nPerimeter: 30"
    },
    {
        "id": "Practice 4",
        "level": "Intermediate",
        "title": "BankAccount with Private #balance, Deposit & Withdraw Validations",
        "req": "<code>BankAccount</code> ক্লাস বানান যাতে ব্যালেন্স প্রাইভেট (<code>#balance</code>) থাকবে এবং <code>deposit(amount)</code>, <code>withdraw(amount)</code>, ও <code>getBalance()</code> মেথডের মাধ্যমে সুরক্ষিতভাবে লেনদেন করা যাবে।",
        "code": """class BankAccount {
    #balance;

    constructor(initialBalance = 0) {
        this.#balance = initialBalance >= 0 ? initialBalance : 0;
    }

    deposit(amount) {
        if (amount > 0) {
            this.#balance += amount;
            console.log(`Deposited $${amount}. New balance: $${this.#balance}`);
        } else {
            console.log("Deposit amount must be positive.");
        }
    }

    withdraw(amount) {
        if (amount <= 0) {
            console.log("Invalid withdrawal amount.");
        } else if (amount > this.#balance) {
            console.log("Insufficient funds!");
        } else {
            this.#balance -= amount;
            console.log(`Withdrawn $${amount}. Remaining balance: $${this.#balance}`);
        }
    }

    getBalance() {
        return this.#balance;
    }
}

// Verification
const account = new BankAccount(500);
account.deposit(200);
account.withdraw(150);
console.log("Final Balance:", account.getBalance());""",
        "output": "Deposited $200. New balance: $700\nWithdrawn $150. Remaining balance: $550\nFinal Balance: 550"
    },
    {
        "id": "Practice 5",
        "level": "Intermediate",
        "title": "Inheritance Architecture: Employee Base Class to Developer Derived Class",
        "req": "<code>Employee</code> (name, salary) বেস ক্লাস থেকে <code>Developer</code> (language, code()) চাইল্ড ক্লাস তৈরি করুন এবং <code>super()</code> এর মাধ্যমে প্যারেন্ট প্রোপার্টি ইনিশিয়ালাইজ করুন।",
        "code": """class Employee {
    constructor(name, salary) {
        this.name = name;
        this.salary = salary;
    }

    getDetails() {
        return `${this.name} earns $${this.salary}/year`;
    }
}

class Developer extends Employee {
    constructor(name, salary, language) {
        super(name, salary); // Call parent constructor
        this.language = language;
    }

    code() {
        console.log(`${this.name} is writing code in ${this.language}.`);
    }
}

// Verification
const dev = new Developer("Shariar", 95000, "JavaScript");
console.log(dev.getDetails());
dev.code();""",
        "output": "Shariar earns $95000/year\nShariar is writing code in JavaScript."
    },
    {
        "id": "Practice 6",
        "level": "Advanced",
        "title": "Mini E-commerce Architecture: Product, Cart, Order & User Interaction",
        "req": "একটি পূর্ণাঙ্গ অবজেক্ট-ওরিয়েন্টেড মিনি ই-কমার্স আর্কিটেকচার তৈরি করুন যাতে <code>Product</code>, <code>Cart</code>, <code>Order</code>, এবং <code>User</code> ক্লাসগুলো একে অপরের সাথে ইন্টারঅ্যাক্ট করে মোট মূল্য ও কার্ট প্রসেসিং সম্পন্ন করবে।",
        "code": """class Product {
    constructor(id, name, price) {
        this.id = id;
        this.name = name;
        this.price = price;
    }
}

class Cart {
    constructor() {
        this.items = [];
    }

    addProduct(product, quantity = 1) {
        this.items.push({ product, quantity });
        console.log(`Added ${quantity}x ${product.name} to cart.`);
    }

    getTotal() {
        return this.items.reduce((sum, item) => sum + item.product.price * item.quantity, 0);
    }
}

class Order {
    constructor(user, cart) {
        this.user = user;
        this.items = [...cart.items];
        this.totalAmount = cart.getTotal();
        this.orderDate = new Date();
    }

    printReceipt() {
        console.log(`=== RECEIPT FOR ${this.user.name} ===`);
        this.items.forEach(i => console.log(`- ${i.product.name} x${i.quantity}: $${i.product.price * i.quantity}`));
        console.log(`Total: $${this.totalAmount}`);
    }
}

class User {
    constructor(name, email) {
        this.name = name;
        this.email = email;
    }
}

// Complete System Simulation
const user = new User("Tanjim", "tanjim@example.com");
const laptop = new Product(101, "MacBook Pro", 1999);
const mouse = new Product(102, "Magic Mouse", 79);

const cart = new Cart();
cart.addProduct(laptop, 1);
cart.addProduct(mouse, 2);

const order = new Order(user, cart);
order.printReceipt();""",
        "output": "Added 1x MacBook Pro to cart.\nAdded 2x Magic Mouse to cart.\n=== RECEIPT FOR Tanjim ===\n- MacBook Pro x1: $1999\n- Magic Mouse x2: $158\nTotal: $2157"
    }
]

html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">24.Lab</span> 📝 Hands-On Practice Lab — 6 Real-World OOP Challenges</div>
      <p class="text-p">থিওরি এবং কনসেপ্ট আয়ত্ত করার পর বাস্তব প্রজেক্টে ক্লাস ব্যবহারের দক্ষতা যাচাই করার জন্য নিচে ৬টি প্র্যাকটিস প্রবলেমের বিস্তারিত সমাধান দেওয়া হলো:</p>
''')

for p in practice_solutions:
    html_parts.append(f'''      <div class="practice-item">
        <div style="font-weight: 700; font-size: 11px; color: var(--navy-deep); margin-bottom: 3px;">{p["id"]}: {p["title"]} <span style="font-size: 9px; color: #6366f1; background: #ede9fe; padding: 1px 5px; border-radius: 3px; margin-left: 6px;">{p["level"]}</span></div>
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
      <div class="card-title"><span class="badge-num">24.Map</span> 🎯 Final Mental Map &amp; Prototype Connection</div>
      <p class="text-p">JavaScript-এর সম্পূর্ণ Object-Oriented Programming ইকোসিস্টেম, ক্লাস ফিল্ডস, ইনহেরিট্যান্স এবং মেথড স্ট্রাকচারের সামগ্রিক ভিজ্যুয়াল আর্কিটেকচার:</p>
      {render_ascii_box(ascii_map, title="JavaScript OOP Master Architecture Tree")}
      
      <div class="section-subhead">⭐ সবচেয়ে গুরুত্বপূর্ণ Connection</div>
      <p class="text-p">তুমি <strong>Chapter 10-এ Objects</strong>, <strong>Chapter 11-এ Prototypes</strong>, এবং <strong>Chapter 24-এ Classes/OOP</strong> পড়ার পর এই তিনটির পারস্পরিক যোগসূত্র এভাবে মনে রাখবে:</p>
      {render_ascii_box("Object\\n  ↓\\nPrototype\\n  ↓\\nClass syntax\\n  ↓\\nInheritance\\n  ↓\\nOOP architecture", title="Evolution of JavaScript Object System")}
      
      <div class="def-box" style="margin-top: 6px;">
        <div class="def-text">Key Takeaway: JavaScript-এ class কোনো সম্পূর্ণ নতুন অবজেক্ট মডেল নয়; এটি আসলে JavaScript-এর বিদ্যমান Prototypal Inheritance সিস্টেমের ওপর নির্মিত অত্যন্ত মার্জিত এবং আধুনিক সিনট্যাকটিক সুগার (Syntactic Sugar)। এই কনসেপ্টটি আয়ত্ত করলে React এর ক্লাস কম্পোনেন্ট, TypeScript এর ক্লাস মডেলিং এবং Node.js/NestJS আর্কিটেকচার বোঝা অত্যন্ত সহজ হয়ে যাবে।</div>
      </div>
    </div>

  </div>

</body>
</html>
''')

full_html = ''.join(html_parts)

out_file = r'c:\Users\User\Desktop\Note-Book\Code\Chapter-24-OOP-Classes.html'
with open(out_file, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f'Successfully generated {out_file} ({len(full_html)} chars, {len(full_html.splitlines())} lines)')
