import re
import sys
import html
import os
import subprocess

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Read raw markdown
with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-40.md', 'r', encoding='utf-8') as f:
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

def highlight_code(code_str, lang='javascript'):
    code_text = code_str.strip()
    esc_all = html.escape(code_text)
    
    if lang in ('javascript', 'js', 'json'):
        token_spec = [
            ('COMMENT_MULTI', r'/\*[\s\S]*?\*/'),
            ('COMMENT_LINE', r'//.*$'),
            ('REGEX_LIT', r'/(?:\\/|[^\n\r/])+/[gimsuy]*'),
            ('STRING_TMPL', r'`(?:\\.|[^`\\])*`'),
            ('STRING_DBL', r'"(?:\\.|[^"\\])*"'),
            ('STRING_SGL', r"'(?:\\.|[^'\\])*'"),
            ('KEYWORD', r'\b(?:for|while|do|break|continue|if|else|let|const|var|function|return|switch|case|default|of|in|new|typeof|delete|this|super|class|extends|static|instanceof|try|catch|finally|throw|await|async|yield|import|export|from|default|get|set|require|module|exports)\b'),
            ('BOOL_NULL', r'\b(?:true|false|null|undefined|NaN)\b'),
            ('DOM_BUILTIN', r'\b(?:console|process|Buffer|Object|Array|Promise|String|Number|Math|BigInt|Map|Set|Error|Date|JSON|Math|window|document)\b'),
            ('METHODS', r'\b(?:reverseString|isPalindrome|findMax|removeDuplicates|countFrequency|split|reverse|join|max|all|allSettled|slice|push|pop|map|filter|reduce|find|forEach|test|then|catch|log|status|json|send|use|get|post|patch|delete|expect|toBe|toEqual)\b'),
            ('OPERATOR', r'(?:===|!==|=>|&&|\|\||\?\?|\?\.|[+\-*/%=<>!&|^~]|\.\.\.)'),
            ('NUMBER', r'\b\d+(?:_\d+)*(?:\.\d+)?\b'),
            ('OTHER', r'[^\s\w]+|\w+|\s+'),
        ]
        tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
        
        out = []
        for mo in re.finditer(tok_regex, code_text, flags=re.MULTILINE):
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
            elif kind == 'DOM_BUILTIN':
                out.append(f'<span class="syn-fn">{esc}</span>')
            elif kind == 'METHODS':
                out.append(f'<span style="color: #38bdf8; font-weight: 600;">{esc}</span>')
            elif kind == 'OPERATOR':
                out.append(f'<span style="color: #c084fc; font-weight: 700;">{esc}</span>')
            elif kind == 'NUMBER':
                out.append(f'<span class="syn-num">{esc}</span>')
            else:
                out.append(esc)
        return ''.join(out)
    else:
        return esc_all

def render_code_box(code_text, lang='javascript', title=None):
    code_text = code_text.strip()
    highlighted = highlight_code(code_text, lang=lang)
    display_title = title if title else (f"{lang.upper()} Source")
    
    return f'''<div class="code-box">
  <div class="code-top"><span style="color: #38bdf8; font-weight: 600;">{display_title}</span><span>{lang.upper()}</span></div>
  <pre><code>{highlighted}</code></pre>
</div>'''

def colorize_ascii(text):
    t = html.escape(text.strip())
    
    # 1. Directional paths & flow arrows (Cyan)
    t = re.sub(r'([↓↑→←▼▲►◄])', r'<span style="color: #38bdf8; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(───+|──|─►|◄─)', r'<span style="color: #0ea5e9; font-weight: 600;">\1</span>', t)
    
    # 2. Box frames & structural connectors (Slate)
    t = re.sub(r'([┌┐└┘├┤┬┴│┼]+)', r'<span style="color: #475569;">\1</span>', t)
    t = re.sub(r'(\-{3,})', r'<span style="color: #334155;">\1</span>', t)
    
    # 3. Main Framework & Career Taxonomies (Amber / Gold)
    t = re.sub(r'\b(JAVASCRIPT|Fundamentals|Advanced|Browser|Modern JavaScript|Full Stack JS|Professional Developer|React|Node\.js|Node|Express|MongoDB|PostgreSQL|Production Apps|Real Projects|System Design)\b', r'<span style="color: #fde047; font-weight: 700;">\1</span>', t)
    
    # 4. Clean Architecture Components & Layers (Lavender / Violet)
    t = re.sub(r'\b(Controller|Service|Repository|Frontend|Backend|Database|API|Routes|Middleware|Controllers|Auth|Authentication|Business Logic|Response|UI|Shallow|Deep Copy|Event Loop|Promise\.all|async/await)\b', r'<span style="color: #c084fc; font-weight: 700;">\1</span>', t)
    
    # 5. Engineering Principles & Positive Attributes (Emerald / Mint)
    t = re.sub(r'\b(Clean Code|DRY|KISS|YAGNI|Separation of Concerns|Unit Test|Security|Performance|Scalability|Maintainability|Testable|Deployable|Active|Valid|Success|Clean|Best simple solution)\b', r'<span style="color: #34d399; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(✓|✔|☑)', r'<span style="color: #4ade80; font-weight: bold;">\1</span>', t)
    
    # 6. Domain Actors & Variables (Sky / Cyan)
    t = re.sub(r'\b(User|Ripon|Admin|Client|Computer|Server)\b', r'<span style="color: #38bdf8; font-weight: 600;">\1</span>', t)
    
    # 7. Mistakes, Pitfalls & Anti-patterns (Rose / Crimson)
    t = re.sub(r'\b(Unnecessary re-render|No validation|Secrets in GitHub|No error handling|Huge components|No tests|Overengineering|Copy-paste programming|1000\+ lines|Everything in one file)\b', r'<span style="color: #f43f5e; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(✗|✘|❌|X)', r'<span style="color: #f43f5e; font-weight: bold;">\1</span>', t)
    
    return t

def render_ascii_box(text, title=None):
    if not title:
        if 'JAVASCRIPT' in text and 'Full Stack' in text:
            title = "FULL-STACK JAVASCRIPT SYSTEM BLUEPRINT"
        elif 'Event Loop' in text or 'Microtask' in text:
            title = "RUNTIME ASYNC EXECUTION ARCHITECTURE"
        elif 'Controller' in text or 'Repository' in text:
            title = "TIERED CLEAN ENTERPRISE DATA FLOW"
        elif 'Beginner' in text and 'Professional' in text:
            title = "DEVELOPER CAREER MASTERY STAGES"
        elif 'User' in text and 'Frontend' in text:
            title = "REAL-WORLD APPLICATION DATA LIFECYCLE"
        else:
            title = "SYSTEM ARCHITECTURE & ROADMAP"
            
    colorized = colorize_ascii(text)
    return f'''<div class="ascii-tree-container">
  <div class="ascii-tree-header">✨ {title}</div>
  <pre class="ascii-tree-content">{colorized}</pre>
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
        
    th_html = ''.join(f'<th>{inline_format(h)}</th>' for h in headers)
    tr_html = []
    for r in rows:
        tds = ''.join(f'<td>{inline_format(c)}</td>' for c in r)
        tr_html.append(f'<tr>{tds}</tr>')
        
    return f'''<div class="table-container">
  <table class="master-table">
    <thead>
      <tr>{th_html}</tr>
    </thead>
    <tbody>
      {''.join(tr_html)}
    </tbody>
  </table>
</div>'''

# Part Banners configuration for Chapter 40
PART_BANNERS = {
    1: ("Part 01", "Real-World Engineering, Architecture & Scalable Folder Structures (40.1 – 40.6)"),
    7: ("Part 02", "Clean Code, SOLID Principles & Multi-Tier Validation (40.7 – 40.17)"),
    18: ("Part 03", "Error Handling Strategy, Security Checklist & Professional Git Workflow (40.18 – 40.25)"),
    26: ("Part 04", "REST API Design, Testing Strategy, Debugging & Production Deployment (40.26 – 40.38)"),
    39: ("Part 05", "Comprehensive JavaScript Technical Interview Mastery (15 Core Questions) (40.39 – 40.53)"),
    54: ("Part 06", "Live Coding Interview Algorithms & Data Structure Challenges (40.54 – 40.58)"),
    59: ("Part 07", "Common Pitfalls, Senior Developer Mindset & Complete 40-Chapter Checklist (40.59 – 40.61)"),
    62: ("Part 08", "Skill Progression Tiers, Grand 40-Chapter Final Mental Map & The Journey Forward (40.62 – 40.63)"),
}

# Split markdown into sections
raw_sections = re.split(r'\n(?=# (?:[^\n]*?)?40\.\d+\s*(?:—|-)?\s*)', raw_md)
print(f"Total raw section chunks parsed: {len(raw_sections)}")

html_parts = []

# Document Header & CSS Tokens
html_parts.append('''<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter 40 — Real-World Projects, Best Practices & Interview Preparation | JavaScript Master Study Documentation</title>
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
      --font-code: 'Fira Code', monospace;
      --font-body: 'Hind Siliguri', sans-serif;
      --font-heading: 'Plus Jakarta Sans', sans-serif;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }

    body {
      background-color: #cbd5e1;
      font-family: var(--font-body);
      font-size: 11px;
      line-height: 1.55;
      color: var(--text-main);
    }

    /* Screen Action Bar */
    .action-bar {
      position: sticky;
      top: 0;
      z-index: 1000;
      background: #0f172a;
      padding: 10px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #0284c7;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .brand-title {
      font-family: var(--font-heading);
      font-weight: 700;
      font-size: 13px;
      color: #f8fafc;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .print-btn {
      background: linear-gradient(135deg, #0284c7, #0369a1);
      color: white;
      border: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-family: var(--font-heading);
      font-weight: 600;
      font-size: 11px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .print-btn:hover {
      background: linear-gradient(135deg, #0369a1, #075985);
      transform: translateY(-1px);
    }

    /* A4 Document Container */
    .doc-page {
      max-width: 210mm;
      margin: 20px auto;
      background: var(--bg-page);
      padding: 12mm 14mm;
      box-shadow: 0 8px 24px rgba(0,0,0,0.12);
      border-radius: 4px;
    }

    /* Master Top Banner (Chapter 40 Badge in TOP RIGHT as requested!) */
    .master-banner {
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0369a1 100%);
      color: #ffffff;
      padding: 12px 16px;
      border-radius: 8px;
      margin-bottom: 8px;
      box-shadow: 0 4px 12px rgba(3, 105, 161, 0.2);
    }
    .banner-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 4px;
    }
    .banner-left {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .banner-icon {
      background: #f7df1e;
      color: #000000;
      font-family: var(--font-heading);
      font-weight: 800;
      font-size: 13px;
      padding: 2px 7px;
      border-radius: 4px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.25);
    }
    .banner-title {
      font-family: var(--font-heading);
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.5px;
      color: #ffffff;
    }
    .chapter-badge {
      background: #f7df1e;
      color: #000000;
      font-family: var(--font-heading);
      font-size: 12px;
      font-weight: 800;
      padding: 2px 8px;
      border-radius: 4px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.2);
      letter-spacing: 0.5px;
    }
    .banner-sub {
      font-size: 9.5px;
      opacity: 0.95;
      font-weight: 500;
      letter-spacing: 0.3px;
      margin-bottom: 8px;
      color: #e0f2fe;
    }
    .meta-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      background: rgba(15, 23, 42, 0.35);
      padding: 6px 10px;
      border-radius: 6px;
      border: 1px solid rgba(255, 255, 255, 0.12);
    }
    .meta-item {
      font-size: 8.5px;
    }
    .meta-label {
      color: #93c5fd;
      text-transform: uppercase;
      font-weight: 600;
      font-size: 7.5px;
      letter-spacing: 0.5px;
    }
    .meta-val {
      font-weight: 600;
      color: #ffffff;
    }

    /* Chapter Opening Statement Card */
    .opening-card {
      background: #f0f9ff;
      border: 1px solid #bae6fd;
      border-left: 3px solid var(--blue-accent);
      border-radius: 6px;
      padding: 8px 12px;
      margin-bottom: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
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
      grid-template-columns: repeat(5, 1fr);
      gap: 4px;
      margin-top: 5px;
      padding-top: 5px;
      border-top: 1px dashed #bae6fd;
    }
    .roadmap-item {
      background: white;
      border: 1px solid #e0f2fe;
      border-radius: 4px;
      padding: 3px 5px;
      font-size: 8.5px;
      color: #0369a1;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 3px;
    }

    /* Part Banners */
    .part-banner {
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
      color: #ffffff;
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
      border-bottom: 1px solid #f1f5f9;
      padding-bottom: 4px;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .badge-num {
      background: #e0f2fe;
      color: #0369a1;
      font-family: var(--font-code);
      font-weight: 700;
      font-size: 9px;
      padding: 1px 5px;
      border-radius: 3px;
      border: 1px solid #bae6fd;
    }

    /* Section Subheadings */
    .section-subhead {
      font-family: var(--font-heading);
      font-size: 10.5px;
      font-weight: 700;
      color: var(--blue-dark);
      margin: 6px 0 3px 0;
      display: flex;
      align-items: center;
      gap: 5px;
    }

    /* Paragraphs and Text */
    .text-p {
      margin-bottom: 5px;
      text-align: justify;
      color: #334155;
      font-size: 10.5px;
      line-height: 1.5;
    }
    .text-p strong {
      color: #0f172a;
      font-weight: 600;
    }

    /* Definitions / Quotes / Tips */
    .def-box {
      background: #f8fafc;
      border-left: 3px solid var(--blue-accent);
      padding: 5px 9px;
      border-radius: 0 4px 4px 0;
      margin: 4px 0 6px 0;
      font-size: 10px;
      color: #1e293b;
    }

    /* Code Blocks */
    .code-box {
      background: #0f172a;
      border-radius: 6px;
      margin: 5px 0;
      overflow: hidden;
      box-shadow: 0 2px 6px rgba(0,0,0,0.15);
      border: 1px solid #1e293b;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }
    .code-top {
      background: #1e293b;
      padding: 3px 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--font-code);
      font-size: 8.5px;
      color: #94a3b8;
      border-bottom: 1px solid #334155;
    }
    pre {
      margin: 0;
      padding: 7px 10px;
      overflow-x: hidden !important;
      white-space: pre-wrap !important;
      word-break: break-word !important;
      font-family: var(--font-code) !important;
      font-size: 9.5px !important;
      line-height: 1.4 !important;
      color: #e2e8f0;
    }

    /* Syntax Highlighting */
    .syn-kw { color: #f43f5e; font-weight: 600; }
    .syn-fn { color: #38bdf8; font-weight: 600; }
    .syn-str { color: #34d399; }
    .syn-num { color: #fbbf24; }
    .syn-com { color: #64748b; font-style: italic; }
    .syn-bool { color: #c084fc; font-weight: 600; }

    /* ASCII Diagrams with Pre & White-space: Pre & Colorful Highlights */
    .ascii-tree-container {
      background: #090d16;
      border: 1px solid #1e293b;
      border-radius: 6px;
      margin: 5px 0;
      overflow: hidden;
      box-shadow: 0 2px 6px rgba(0,0,0,0.18);
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }
    .ascii-tree-header {
      background: #111c2e;
      color: #38bdf8;
      font-family: var(--font-code);
      font-size: 9px;
      font-weight: 700;
      padding: 4px 10px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      border-bottom: 1px solid #1e293b;
    }
    .ascii-tree-content {
      color: #e2e8f0 !important;
      font-family: var(--font-code) !important;
      font-size: 9.5px !important;
      line-height: 1.35 !important;
      padding: 8px 12px !important;
      background: transparent !important;
      border: none !important;
      white-space: pre !important;
      overflow-x: hidden !important;
      word-break: normal !important;
      margin: 0 !important;
    }

    /* Master Tables */
    .table-container {
      margin: 6px 0;
      border-radius: 6px;
      overflow: hidden;
      border: 1px solid #e2e8f0;
    }
    .master-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 9.5px;
    }
    .master-table th {
      background: #1e293b;
      color: #f8fafc;
      font-weight: 700;
      padding: 5px 8px;
      text-align: left;
      border-bottom: 1px solid #334155;
    }
    .master-table td {
      padding: 5px 8px;
      border-bottom: 1px solid #f1f5f9;
      color: #334155;
    }
    .master-table tr:nth-child(even) {
      background: #f8fafc;
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
      #sec-40-1 {
        page-break-after: always !important;
        break-after: page !important;
        margin-bottom: 0 !important;
      }
      .study-card {
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        border: 1px solid #cbd5e1;
      }
      .part-banner {
        page-break-after: avoid !important;
        break-after: avoid !important;
      }
      .code-box, pre, .ascii-tree-container, .table-container, .def-box, .output-box {
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

    <!-- Header Master Banner (Chapter 40 Badge in TOP RIGHT as requested!) -->
    <header class="master-banner">
      <div class="banner-top">
        <div class="banner-left">
          <div class="banner-icon">JS</div>
          <span class="banner-title">JavaScript Master Study Documentation</span>
        </div>
        <span class="chapter-badge">Chapter 40</span>
      </div>
      <div class="banner-sub">REAL-WORLD PROJECTS, ARCHITECTURAL BEST PRACTICES, PRODUCTION STANDARDS &amp; INTERVIEW MASTERY</div>
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">Total Modules</div>
          <div class="meta-val">63 Modules + 5 Coding Labs + 15 Q&amp;As</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Curriculum Part</div>
          <div class="meta-val">Part 34 — Grand Finale &amp; Career Mastery</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Core Disciplines</div>
          <div class="meta-val">Clean Architecture, Production Git &amp; APIs</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Target Profile</div>
          <div class="meta-val">Full Stack JavaScript Production Engineer</div>
        </div>
      </div>
    </header>

    <!-- Chapter Opening Statement (Page 1 Balance) -->
    <div class="opening-card">
      <div class="opening-title">
        <span>✨</span> Real-World Projects, Best Practices &amp; Interview Preparation — গ্র্যান্ড ফিনালে
      </div>
      <p class="text-p">
        ৪০টি অধ্যায়ের এই সুদীর্ঘ ও সমৃদ্ধ যাত্রায় আমরা জাভাস্ক্রিপ্ট ফান্ডামেন্টালস থেকে শুরু করে রিয়্যাক্ট ফ্রন্টএন্ড এবং নোড ব্যাকএন্ডের গভীরতম আর্কিটেকচার আয়ত্ত করেছি। এই চূড়ান্ত অধ্যায়ে আমরা পুরো জ্ঞানের বাস্তব সমন্বয় ঘটিয়ে রিয়েল-ওয়ার্ল্ড প্রজেক্ট আর্কিটেকচার, ক্লিন কোড (DRY/KISS/YAGNI), সিকিউরিটি চেকলিস্ট, গিট ওয়ার্কফ্লো, এপিআই ডিজাইন, প্রোডাকশন চেকলিস্ট, ১৫টি প্রধান ইন্টারভিউ প্রশ্নোত্তর এবং লাইভ কোডিং অ্যালগরিদম সমাধান করব।
      </p>
      <div class="roadmap-grid">
        <div class="roadmap-item"><span>📌</span> 1. Real-World Arch</div>
        <div class="roadmap-item"><span>📌</span> 2. Clean Code &amp; SOLID</div>
        <div class="roadmap-item"><span>📌</span> 3. Security &amp; Secrets</div>
        <div class="roadmap-item"><span>📌</span> 4. Professional Git</div>
        <div class="roadmap-item"><span>📌</span> 5. REST API Design</div>
        <div class="roadmap-item"><span>📌</span> 6. Testing &amp; Debugging</div>
        <div class="roadmap-item"><span>📌</span> 7. Production Checklist</div>
        <div class="roadmap-item"><span>📌</span> 8. 15 Interview Q&amp;As</div>
        <div class="roadmap-item"><span>📌</span> 9. 5 Coding Labs</div>
        <div class="roadmap-item"><span>📌</span> 10. 40-Chapter Roadmap</div>
      </div>
    </div>
''')

# Function to get part banner if applicable
def check_part_banner(sec_idx):
    if sec_idx in PART_BANNERS:
        part_tag, part_title = PART_BANNERS[sec_idx]
        return f'<div class="part-banner">{part_tag} — {part_title}</div>'
    return None

def process_section_body(body_text):
    body_lines = body_text.split('\n')
    in_code = False
    cur_lang = ''
    code_lines = []
    p_acc = []
    in_list = False
    in_table = False
    table_lines = []
    res = []
    
    for l in body_lines:
        ls = l.strip()
        
        # Table detection
        if ls.startswith('|') and ls.endswith('|'):
            if not in_table:
                if in_list:
                    res.append('      </ul>\n')
                    in_list = False
                if p_acc:
                    p_text = " ".join(p_acc).strip()
                    if p_text and p_text != '---':
                        res.append(f'      <p class="text-p">{inline_format(p_text)}</p>\n')
                    p_acc = []
                in_table = True
                table_lines = []
            table_lines.append(ls)
            continue
        elif in_table:
            in_table = False
            res.append(f'      {render_table(chr(10).join(table_lines))}\n')
            table_lines = []
            
        # Code fence detection
        if ls.startswith('```'):
            if not in_code:
                if in_list:
                    res.append('      </ul>\n')
                    in_list = False
                if p_acc:
                    p_text = " ".join(p_acc).strip()
                    if p_text and p_text != '---':
                        res.append(f'      <p class="text-p">{inline_format(p_text)}</p>\n')
                    p_acc = []
                in_code = True
                cur_lang = ls[3:].strip().lower()
                code_lines = []
            else:
                in_code = False
                code_content = '\n'.join(code_lines)
                if cur_lang in ('javascript', 'js'):
                    res.append(f'      {render_code_box(code_content, lang="javascript")}\n')
                elif cur_lang in ('bash', 'sh', 'shell'):
                    res.append(f'      {render_code_box(code_content, lang="bash", title="TERMINAL COMMAND")}\n')
                elif cur_lang == 'json':
                    res.append(f'      {render_code_box(code_content, lang="json", title="JSON PAYLOAD")}\n')
                else: # text or empty
                    res.append(f'      {render_ascii_box(code_content)}\n')
            continue
            
        if in_code:
            code_lines.append(l)
            continue
            
        # Outside code fence
        if not ls:
            continue
        if ls == '---' or ls.startswith('---') or ls == '***':
            continue
        if ls.endswith('---'):
            ls = ls[:-3].strip()
        if not ls:
            continue
            
        # Headings handling
        if ls.startswith('# '):
            if in_list:
                res.append('      </ul>\n')
                in_list = False
            if p_acc:
                p_text = " ".join(p_acc).strip()
                if p_text and p_text != '---':
                    res.append(f'      <p class="text-p">{inline_format(p_text)}</p>\n')
                p_acc = []
            sub_title = ls[2:].strip()
            res.append(f'      <div class="def-box" style="border-left: 3px solid #f59e0b; background: #fffbeb; font-weight: 700; color: #b45309;">⚡ {inline_format(sub_title)}</div>\n')
        elif ls.startswith('### '):
            if in_list:
                res.append('      </ul>\n')
                in_list = False
            if p_acc:
                p_text = " ".join(p_acc).strip()
                if p_text and p_text != '---':
                    res.append(f'      <p class="text-p">{inline_format(p_text)}</p>\n')
                p_acc = []
            sub_title = ls[4:].strip()
            res.append(f'      <div class="section-subhead">🔹 {inline_format(sub_title)}</div>\n')
        elif ls.startswith('## '):
            if in_list:
                res.append('      </ul>\n')
                in_list = False
            if p_acc:
                p_text = " ".join(p_acc).strip()
                if p_text and p_text != '---':
                    res.append(f'      <p class="text-p">{inline_format(p_text)}</p>\n')
                p_acc = []
            sub_title = ls[3:].strip()
            res.append(f'      <div class="section-subhead" style="font-size: 11px; color: var(--navy-deep); border-left: 2px solid var(--blue-accent); padding-left: 5px;">✨ {inline_format(sub_title)}</div>\n')
        elif ls.startswith('* ') or ls.startswith('- '):
            if not in_list:
                if p_acc:
                    p_text = " ".join(p_acc).strip()
                    if p_text and p_text != '---':
                        res.append(f'      <p class="text-p">{inline_format(p_text)}</p>\n')
                    p_acc = []
                res.append('      <ul style="margin: 2px 0 5px 16px; color: #334155; font-size: 10.5px;">\n')
                in_list = True
            res.append(f'        <li>{inline_format(ls[2:])}</li>\n')
        elif ls.startswith('> '):
            if in_list:
                res.append('      </ul>\n')
                in_list = False
            if p_acc:
                p_text = " ".join(p_acc).strip()
                if p_text and p_text != '---':
                    res.append(f'      <p class="text-p">{inline_format(p_text)}</p>\n')
                p_acc = []
            quote_text = ls[2:].strip()
            res.append(f'      <div class="def-box">💡 {inline_format(quote_text)}</div>\n')
        else:
            if in_list:
                res.append('      </ul>\n')
                in_list = False
            p_acc.append(ls)
            
    if in_table:
        res.append(f'      {render_table(chr(10).join(table_lines))}\n')
    if in_list:
        res.append('      </ul>\n')
    if p_acc:
        p_text = " ".join(p_acc).strip()
        if p_text and p_text != '---':
            res.append(f'      <p class="text-p">{inline_format(p_text)}</p>\n')
            
    return ''.join(res)

# Process sections 1 to 63
for idx in range(1, 64):
    sec_text = raw_sections[idx].strip()
    pb = check_part_banner(idx)
    if pb:
        html_parts.append(f'    {pb}\n')
        
    sec_lines = sec_text.split('\n')
    header_line = sec_lines[0]
    m_head = re.search(r'# (?:🔥\s*|⚠️\s*|🧠\s*)?(40\.\d+)\s*(?:—|-)?\s*(.*)', header_line)
    if m_head:
        sec_num = m_head.group(1)
        sec_title = m_head.group(2)
    else:
        sec_num = f'40.{idx}'
        sec_title = header_line.replace('#', '').strip()
        
    card_extra = ''
    if idx == 1:
        card_extra = ' id="sec-40-1"'
        
    html_parts.append(f'''    <div class="study-card"{card_extra}>
      <div class="card-title"><span class="badge-num">{sec_num}</span> {inline_format(sec_title)}</div>
''')
    
    body_text = '\n'.join(sec_lines[1:]).strip()
    html_parts.append(process_section_body(body_text))
    html_parts.append('    </div>\n')

# Grand Conclusion Card
html_parts.append('''    <div class="study-card" style="border: 2px solid #0284c7; background: #f0f9ff;">
      <div class="card-title" style="color: #0369a1; font-size: 12px;"><span class="badge-num" style="background: #0284c7; color: white;">40.64</span> 🏆 40-Chapter JavaScript Master Book — Grand Finale & Completion Honor</div>
      <p class="text-p" style="font-size: 11px; line-height: 1.6;">
        🎉 <strong>অভিনন্দন!</strong> আপনি সফলভাবে JavaScript Master Study Documentation-এর <strong>১ থেকে ৪০টি পূর্ণাঙ্গ চ্যাপ্টার</strong> সম্পন্ন করেছেন। এটি শুধুমাত্র একটি টিউটোরিয়াল নোট নয়—এটি প্রফেশনাল সফটওয়্যার ইঞ্জিনিয়ারিং, ক্লিন আর্কিটেকচার, রিয়্যাক্ট ফ্রন্টএন্ড এবং নোড.জেএস ব্যাকএন্ডের একটি পরিপূর্ণ ও ত্রুটিমুক্ত এনসাইক্লোপিডিয়া।
      </p>
      <div class="def-box" style="margin-top: 6px; border-left: 3px solid #059669; background: #ecfdf5; color: #065f46; font-size: 10.5px;">
        🌟 <strong>The Senior Engineer's Creed:</strong> ভালো কোডার সিনট্যাক্স মুখস্থ করে না; সে সিস্টেমের ডেটা-ফ্লো, এরর বাউন্ডারি, মেমোরি লাইফসাইকেল, টেস্টাবিলিটি এবং সিকিউরিটি আর্কিটেকচারকে গুরুত্ব দেয়।
      </div>
    </div>
''')

# Document Closure
html_parts.append('''
  </div>
</body>
</html>''')

# Write complete HTML file
output_html_path = r'c:\Users\User\Desktop\Note-Book\Code\Chapter-40-Real-World-Projects-Best-Practices-Interview-Preparation.html'
with open(output_html_path, 'w', encoding='utf-8') as f:
    f.write(''.join(html_parts))

print(f"HTML successfully generated at: {output_html_path}")
print(f"File size: {os.path.getsize(output_html_path)} bytes")
