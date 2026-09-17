import re
import sys
import html
import subprocess
import os

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Read raw markdown
with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-28.md', 'r', encoding='utf-8') as f:
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
        ('DOM_BUILTIN', r'\b(?:console|window|document|Math|Object|Array|Date|JSON|Promise|Error|Map|Set|WeakMap|WeakSet|Symbol|Proxy|Reflect)\b'),
        ('PROXY_REFLECT', r'\b(?:get|set|has|deleteProperty|ownKeys|apply|construct|revocable|revoke|iterator|toStringTag|toPrimitive|hasInstance|for|keyFor)\b'),
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
        elif kind == 'PROXY_REFLECT':
            out.append(f'<span class="syn-proxy" style="color: #38bdf8; font-weight: 600;">{esc}</span>')
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
        tag_label = '❌ Trap / Anti-pattern'
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
pattern = r'\n(?=# (?:(?:🔥\s*)?28\.\d+|🧠\s*Quick Cheat Sheet|📝\s*Practice Set|🎯\s*Final Mental Map))'
raw_sections = re.split(pattern, raw_md)

print(f"Total raw sections split: {len(raw_sections)}")

# Build HTML with Classic 1-10 UI Styling + Brand JS Yellow + Prominent Chapter Title
html_parts = []
html_parts.append('''<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter 28 — Symbols, Proxy &amp; Reflect | JavaScript Master Study Documentation</title>
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
      #sec-28-1 {
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
          <span class="chapter-badge">Chapter 28</span>
        </div>
      </div>
      <div class="banner-sub">SYMBOLS, PROXY &amp; REFLECT — METAPROGRAMMING, INTERCEPTION &amp; OBJECT ARCHITECTURE</div>
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">Total Modules</div>
          <div class="meta-val">56 Modules + Practice Lab</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Curriculum Part</div>
          <div class="meta-val">Part 22 — JavaScript Metaprogramming</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Core Mechanics</div>
          <div class="meta-val">Symbol, Proxy Handlers &amp; Reflect API</div>
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
        <span>🎯</span> JavaScript Metaprogramming — Symbols, Proxy &amp; Reflect শেখার মূল উদ্দেশ্য
      </div>
      <p class="text-p">
        JavaScript-এ অবজেক্টের স্বাভাবিক আচরণ পরিবর্তন, অপারেশন ইন্টারসেপ্ট ও কাস্টম লজিক যুক্ত করার আর্কিটেকচারাল মেকানিজমের নাম হলো <strong>Metaprogramming</strong>। এই চ্যাপ্টারে আমরা <strong>Unique Symbol Keys, Global Symbol Registry, Proxy Handler Traps (get, set, has, deleteProperty), Reflect API</strong> এবং রিঅ্যাক্টিভ ফ্রেমওয়ার্ক আর্কিটেকচার নিখুঁতভাবে শিখব।
      </p>
      <div class="roadmap-grid">
        <div class="roadmap-item"><span>📌</span> 1. Primitive Symbol</div>
        <div class="roadmap-item"><span>📌</span> 2. Unique Property Keys</div>
        <div class="roadmap-item"><span>📌</span> 3. Symbol.for() Registry</div>
        <div class="roadmap-item"><span>📌</span> 4. Symbol.keyFor()</div>
        <div class="roadmap-item"><span>📌</span> 5. Well-Known Symbols</div>
        <div class="roadmap-item"><span>📌</span> 6. Symbol.iterator</div>
        <div class="roadmap-item"><span>📌</span> 7. Symbol.toPrimitive</div>
        <div class="roadmap-item"><span>📌</span> 8. Proxy Target &amp; Handler</div>
        <div class="roadmap-item"><span>📌</span> 9. get &amp; set Traps</div>
        <div class="roadmap-item"><span>📌</span> 10. Schema Validation</div>
        <div class="roadmap-item"><span>📌</span> 11. has &amp; deleteProperty</div>
        <div class="roadmap-item"><span>📌</span> 12. apply &amp; construct</div>
        <div class="roadmap-item"><span>📌</span> 13. Proxy.revocable</div>
        <div class="roadmap-item"><span>📌</span> 14. Reflect Static API</div>
        <div class="roadmap-item"><span>📌</span> 15. Reflect.get/set</div>
        <div class="roadmap-item"><span>📌</span> 16. Reflect.ownKeys</div>
        <div class="roadmap-item"><span>📌</span> 17. Proxy + Reflect Pair</div>
        <div class="roadmap-item"><span>📌</span> 18. Read-Only Objects</div>
        <div class="roadmap-item"><span>📌</span> 19. Access Control System</div>
        <div class="roadmap-item"><span>📌</span> 20. Vue Reactivity Engine</div>
        <div class="roadmap-item"><span>📌</span> 21. 5 Common Traps</div>
        <div class="roadmap-item"><span>📌</span> 22. 9 Practice Challenges</div>
      </div>
    </div>
''')

def get_part_banner(num):
    if num == 1:
        return '<div class="part-banner">Part 01 — Symbols &amp; Unique Property Keys (28.1 – 28.12)</div>'
    elif num == 13:
        return '<div class="part-banner">Part 02 — Global Symbol Registry &amp; Well-Known Symbols (28.13 – 28.21)</div>'
    elif num == 22:
        return '<div class="part-banner">Part 03 — Proxy Fundamentals &amp; Core Traps (28.22 – 28.36)</div>'
    elif num == 37:
        return '<div class="part-banner">Part 04 — Reflect API &amp; Metaprogramming (28.37 – 28.45)</div>'
    elif num == 46:
        return '<div class="part-banner">Part 05 — Production Architectures, Reactivity &amp; Common Mistakes (28.46 – 28.55)</div>'
    elif num == 56:
        return '<div class="part-banner">Part 06 — Production Mastery, Practice Lab &amp; Mental Map (28.56 – 28.59)</div>'
    return None

# Process all 56 numbered sections (1 to 56)
for idx in range(1, 57):
    sec_text = raw_sections[idx].strip()
    pb = get_part_banner(idx)
    if pb:
        html_parts.append(f'    {pb}\n')
        
    sec_lines = sec_text.split('\n')
    header_line = sec_lines[0]
    m_head = re.search(r'# (?:🔥\s*)?(28\.\d+)\s*(?:—|-)?\s*(.*)', header_line)
    if m_head:
        sec_num = m_head.group(1)
        sec_title = m_head.group(2)
    else:
        sec_num = f'28.{idx}'
        sec_title = header_line.replace('#', '').strip()
        
    card_extra = ''
    if idx == 1:
        card_extra = ' id="sec-28-1"'
        
    html_parts.append(f'''    <div class="study-card"{card_extra}>
      <div class="card-title"><span class="badge-num">{sec_num}</span> {inline_format(sec_title)}</div>
''')
    
    body_text = '\n'.join(sec_lines[1:]).strip()
    
    # Standard parsing with markdown table extraction and separator filtering
    chunks = re.split(r'(```[\s\S]*?```|###[^\n]+|# 🔥[^\n]+|# 🧠[^\n]+|\|[^\n]+\|\n\|[\s:-|-]+\|\n(?:\|[^\n]+\|\n?)+)', body_text)
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
                    if any(c in code_val for c in ['│', '┌', '└', '├', '──', '─', '↓', '→', '←', 'Mental', 'Proxy', 'Reflect', 'Target']):
                        html_parts.append(render_ascii_box(code_val))
                    else:
                        html_parts.append(render_output_box(code_val))
                else:
                    html_parts.append(render_code_box(code_val, lang=clang, title=clang.upper()))
        elif ch_str.startswith('# 🧠'):
            sub_head = ch_str.replace('# 🧠', '').strip()
            html_parts.append(f'      <div class="section-subhead" style="color: #0369a1; border-color: #0284c7;">🧠 {inline_format(sub_head)}</div>\n')
        elif ch_str.startswith('# 🔥'):
            sub_head = ch_str.replace('# 🔥', '').strip()
            html_parts.append(f'      <div class="section-subhead" style="color: #d97706; border-color: #f59e0b;">🔥 {inline_format(sub_head)}</div>\n')
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

# Section 57: Quick Cheat Sheet
sec57 = raw_sections[57].strip()
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">28.Cheat</span> 🧠 Quick Cheat Sheet — Symbol, Proxy &amp; Reflect Matrix</div>
      <p class="text-p">Metaprogramming-এর ৩টি মূল স্তম্ভের সংক্ষিপ্ত ব্যবহারিক সিনট্যাক্স সামারি:</p>
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px;">
        <div>
          <div style="font-weight: 700; font-size: 10px; color: #0369a1; margin-bottom: 2px;">1. Symbol Syntax</div>
''')
code_sym_cheat = """const s = Symbol("desc");
const g = Symbol.for("app.id");
Symbol.keyFor(g); // 'app.id'
obj[Symbol.iterator] = ...;"""
html_parts.append(render_code_box(code_sym_cheat, title="Symbol Reference"))
html_parts.append('''        </div>
        <div>
          <div style="font-weight: 700; font-size: 10px; color: #0369a1; margin-bottom: 2px;">2. Proxy Syntax</div>
''')
code_proxy_cheat = """const proxy = new Proxy(target, {
  get(target, prop, receiver) {
    return Reflect.get(...arguments);
  },
  set(target, prop, val, receiver) {
    return Reflect.set(...arguments);
  }
});"""
html_parts.append(render_code_box(code_proxy_cheat, title="Proxy Pattern"))
html_parts.append('''        </div>
        <div>
          <div style="font-weight: 700; font-size: 10px; color: #0369a1; margin-bottom: 2px;">3. Reflect Syntax</div>
''')
code_reflect_cheat = """Reflect.get(target, prop);
Reflect.set(target, prop, val);
Reflect.has(target, prop);
Reflect.deleteProperty(target, p);
Reflect.ownKeys(target);"""
html_parts.append(render_code_box(code_reflect_cheat, title="Reflect Methods"))
html_parts.append('''        </div>
      </div>
    </div>
''')

# Section 58: Practice Set (9 Practical Challenges with Full Production Solutions)
practice_solutions = [
    {
        "id": "Practice 1",
        "level": "Beginner",
        "title": "Symbol as Object Property Key",
        "req": "একটি <code>userId</code> সিম্বল তৈরি করো এবং অবজেক্টের প্রোপার্টি হিসেবে ব্যবহার করে তা কনসোলে অ্যাক্সেস করো।",
        "code": """const userId = Symbol("userId");

const user = {
    name: "Ripon",
    [userId]: 1001
};

console.log("Name:", user.name);
console.log("Symbol ID:", user[userId]);
console.log("Object Keys:", Object.keys(user)); // Symbol excluded""",
        "output": "Name: Ripon\nSymbol ID: 1001\nObject Keys: ['name']"
    },
    {
        "id": "Practice 2",
        "level": "Beginner",
        "title": "Symbol Uniqueness Verification",
        "req": "একই বিবরণ (description) দিয়ে দুটি পৃথক <code>Symbol('id')</code> তৈরি করে প্রমাণ করো যে তারা কখনো সমান হয় না।",
        "code": """const id1 = Symbol("id");
const id2 = Symbol("id");

console.log("id1 === id2:", id1 === id2);
console.log("id1 description:", id1.description);
console.log("id2 description:", id2.description);""",
        "output": "id1 === id2: false\nid1 description: id\nid2 description: id"
    },
    {
        "id": "Practice 3",
        "level": "Beginner",
        "title": "Global Symbol Registry with Symbol.for()",
        "req": "<code>Symbol.for('app.user')</code> দিয়ে একটি গ্লোবাল সিম্বল তৈরি করে <code>Symbol.keyFor()</code> দিয়ে তার রেজিস্ট্রি কি রিট্রিভ করো।",
        "code": """const globalSym1 = Symbol.for("app.user");
const globalSym2 = Symbol.for("app.user");

console.log("Global Symbols Same?", globalSym1 === globalSym2);
console.log("Registry Key:", Symbol.keyFor(globalSym1));""",
        "output": "Global Symbols Same? true\nRegistry Key: app.user"
    },
    {
        "id": "Practice 4",
        "level": "Intermediate",
        "title": "Custom Iterable with Symbol.iterator",
        "req": "একটি অবজেক্ট তৈরি করো যাতে <code>[Symbol.iterator]</code> মেথড ইমপ্লিমেন্ট করে সরাসরি <code>for...of</code> দিয়ে উপাদান পাওয়া যায়।",
        "code": """const collection = {
    items: ["JavaScript", "TypeScript", "Node.js"],
    *[Symbol.iterator]() {
        for (const item of this.items) {
            yield item;
        }
    }
};

for (const tech of collection) {
    console.log(tech);
}""",
        "output": "JavaScript\nTypeScript\nNode.js"
    },
    {
        "id": "Practice 5",
        "level": "Intermediate",
        "title": "Proxy Age Validation",
        "req": "একটি প্রক্সি তৈরি করো যা <code>age</code> প্রোপার্টিতে শুধু পজিটিভ সংখ্যা লিখতে দেবে, অন্যথায় <code>TypeError</code> থ্রো করবে।",
        "code": """const person = {};

const validator = new Proxy(person, {
    set(target, prop, value) {
        if (prop === "age") {
            if (typeof value !== "number" || value < 0) {
                throw new TypeError("Age must be a positive number!");
            }
        }
        target[prop] = value;
        return true;
    }
});

validator.age = 25;
console.log("Valid Age:", validator.age);
// validator.age = -5; // Throws TypeError""",
        "output": "Valid Age: 25"
    },
    {
        "id": "Practice 6",
        "level": "Intermediate",
        "title": "Proxy Property Access Logger",
        "req": "একটি প্রক্সি তৈরি করো যা প্রতিটি প্রোপার্টি পড়া (GET) এবং লেখার (SET) সময় কনসোলে স্বয়ংক্রিয়ভাবে লগ তৈরি করবে।",
        "code": """const user = { name: "Ripon" };

const loggedUser = new Proxy(user, {
    get(target, prop) {
        console.log(`GET → ${String(prop)}`);
        return Reflect.get(target, prop);
    },
    set(target, prop, value) {
        console.log(`SET → ${String(prop)} = ${value}`);
        return Reflect.set(target, prop, value);
    }
});

const currentName = loggedUser.name;
loggedUser.age = 28;""",
        "output": "GET → name\nSET → age = 28"
    },
    {
        "id": "Practice 7",
        "level": "Advanced",
        "title": "Read-Only Object Proxy with Reflect",
        "req": "একটি <code>createReadOnly(target)</code> হেল্পার বানাও যা অবজেক্টের কোনো প্রোপার্টি পরিবর্তন বা ডিলিট করতে দেবে না।",
        "code": """function createReadOnly(target) {
    return new Proxy(target, {
        set(t, prop) {
            console.warn(`Cannot set '${String(prop)}': Object is read-only!`);
            return false;
        },
        deleteProperty(t, prop) {
            console.warn(`Cannot delete '${String(prop)}': Object is read-only!`);
            return false;
        }
    });
}

const config = createReadOnly({ apiEndpoint: "https://api.example.com" });
config.apiEndpoint = "https://hacked.com"; // Warning logged
console.log("Safe Config:", config.apiEndpoint);""",
        "output": "Cannot set 'apiEndpoint': Object is read-only!\nSafe Config: https://api.example.com"
    },
    {
        "id": "Practice 8",
        "level": "Advanced",
        "title": "Role-Based Access Control (RBAC) Proxy",
        "req": "এমন একটি প্রক্সি তৈরি করো যেখানে <code>user</code> রোল শুধু <code>name</code> এবং <code>admin</code> রোল <code>salary</code> দেখতে পারবে।",
        "code": """function createSecureAccount(data, role) {
    return new Proxy(data, {
        get(target, prop) {
            if (prop === "salary" && role !== "admin") {
                return "⛔ Access Denied: Admin role required";
            }
            return Reflect.get(target, prop);
        }
    });
}

const employee = { name: "Anisur Rahman", salary: 85000 };
const userView = createSecureAccount(employee, "user");
const adminView = createSecureAccount(employee, "admin");

console.log("User views name:", userView.name);
console.log("User views salary:", userView.salary);
console.log("Admin views salary:", adminView.salary);""",
        "output": "User views name: Anisur Rahman\nUser views salary: ⛔ Access Denied: Admin role required\nAdmin views salary: 85000"
    },
    {
        "id": "Practice 9",
        "level": "Advanced",
        "title": "Integrated Metaprogramming Architecture",
        "req": "একটি কাস্টম ক্লাস তৈরি করো যাতে <code>Symbol.iterator</code>, <code>Proxy</code> এবং <code>Reflect</code> তিনটি কনসেপ্ট একসাথে যুক্ত থাকবে।",
        "code": """class ObservableStore {
    constructor(initialData = {}) {
        this.data = initialData;

        // Wrap internal data in proxy using Reflect
        return new Proxy(this, {
            set(target, prop, value) {
                console.log(`[Store Event] Mutated '${String(prop)}' to:`, value);
                return Reflect.set(target, prop, value);
            }
        });
    }

    *[Symbol.iterator]() {
        for (const [key, val] of Object.entries(this.data)) {
            yield { key, val };
        }
    }
}

const store = new ObservableStore({ theme: "dark", lang: "bn" });
store.version = "1.0.0";

for (const entry of store) {
    console.log(`Iterated: ${entry.key} = ${entry.val}`);
}""",
        "output": "[Store Event] Mutated 'version' to: 1.0.0\nIterated: theme = dark\nIterated: lang = bn"
    }
]

html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">28.Lab</span> 📝 Hands-On Practice Lab — 9 Production Metaprogramming Challenges</div>
      <p class="text-p">Symbol, Proxy Traps এবং Reflect API সম্পূর্ণ আয়ত্তে আনতে নিচে ৩টি লেভেলের ৯টি প্র্যাকটিক্যাল চ্যালেঞ্জের সম্পূর্ণ মডেল সলিউশন দেওয়া হলো:</p>
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

# Section 59: Final Mental Map
sec59 = raw_sections[59].strip()
ascii_map_match = re.search(r'```text([\s\S]*?)```', sec59)
ascii_map = ascii_map_match.group(1).strip() if ascii_map_match else ""

html_parts.append(f'''    <div class="study-card">
      <div class="card-title"><span class="badge-num">28.Map</span> 🎯 Final Mental Map &amp; Metaprogramming Architecture</div>
      <p class="text-p">JavaScript Metaprogramming-এর ৩টি স্তম্ভ—Symbol, Proxy ও Reflect-এর সমন্বিত আর্কিটেকচার ম্যাপ:</p>
      {render_ascii_box(ascii_map, title="Metaprogramming Architecture Tree (Symbol, Proxy, Reflect)")}
      
      <div class="section-subhead">⭐ এক নজরে ৩টি প্রধান স্তম্ভের ভূমিকা</div>
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin: 5px 0;">
        <div class="def-box" style="margin: 0; padding: 6px 8px;">
          <div style="font-weight: 700; font-size: 10px; color: #065f46; margin-bottom: 2px;">1️⃣ Symbol</div>
          <div style="font-size: 9px; color: #047857; line-height: 1.35;">“আমার একটি অনন্য (Unique) কী বা অন্তর্নিহিত স্পেশাল প্রটোকল বিহেভিয়ার দরকার।”</div>
        </div>
        <div class="def-box" style="margin: 0; padding: 6px 8px;">
          <div style="font-weight: 700; font-size: 10px; color: #065f46; margin-bottom: 2px;">2️⃣ Proxy</div>
          <div style="font-size: 9px; color: #047857; line-height: 1.35;">“কেউ অবজেক্টের সাথে কী অপারেশন করছে (get, set, has), তা ইন্টারসেপ্ট করে কাস্টম লজিক চালাতে চাই।”</div>
        </div>
        <div class="def-box" style="margin: 0; padding: 6px 8px;">
          <div style="font-weight: 700; font-size: 10px; color: #065f46; margin-bottom: 2px;">3️⃣ Reflect</div>
          <div style="font-size: 9px; color: #047857; line-height: 1.35;">“ইন্টারসেপ্ট করা অপারেশনটিকে স্ট্যান্ডার্ড ও পরিষ্কারভাবে মূল টার্গেট অবজেক্টের ওপর সম্পন্ন করতে চাই।”</div>
        </div>
      </div>

      <div class="def-box" style="margin-top: 6px; padding: 6px 10px; background: #f0fdf4; border-left: 3px solid #10b981;">
        <div style="font-weight: 700; font-size: 10px; color: #065f46; margin-bottom: 2px;">📌 Next Chapter Preview:</div>
        <div style="font-family: var(--font-heading); font-size: 10px; font-weight: 700; color: #0369a1;">
          Chapter 29 — JavaScript Execution Model &amp; Event Loop
        </div>
        <div style="font-size: 9px; color: #334155; margin-top: 2px;">পরবর্তী চ্যাপ্টারে আমরা শিখব Execution Context, Call Stack, Memory Heap, Microtask Queue, Macrotask Queue, Web APIs এবং Asynchronous Order of Execution।</div>
      </div>
    </div>

  </div>

</body>
</html>
''')

full_html = ''.join(html_parts)

out_file = r'c:\Users\User\Desktop\Note-Book\Code\Chapter-28-Symbols-Proxy-Reflect.html'
with open(out_file, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f'Successfully generated {out_file} ({len(full_html)} chars, {len(full_html.splitlines())} lines)')
