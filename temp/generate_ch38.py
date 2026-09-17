import re
import sys
import html
import os
import subprocess

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Read raw markdown
with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-38.md', 'r', encoding='utf-8') as f:
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
    
    if lang in ('javascript', 'js', 'jsx'):
        token_spec = [
            ('COMMENT_MULTI', r'/\*[\s\S]*?\*/'),
            ('COMMENT_LINE', r'//.*$'),
            ('REGEX_LIT', r'/(?:\\/|[^\n\r/])+/[gimsuy]*'),
            ('STRING_TMPL', r'`(?:\\.|[^`\\])*`'),
            ('STRING_DBL', r'"(?:\\.|[^"\\])*"'),
            ('STRING_SGL', r"'(?:\\.|[^'\\])*'"),
            ('KEYWORD', r'\b(?:for|while|do|break|continue|if|else|let|const|var|function|return|switch|case|default|of|in|new|typeof|delete|this|super|class|extends|static|instanceof|try|catch|finally|throw|await|async|yield|import|export|from|default|get|set)\b'),
            ('BOOL_NULL', r'\b(?:true|false|null|undefined|NaN)\b'),
            ('DOM_BUILTIN', r'\b(?:console|window|document|process|Object|Array|Promise|String|Number|Math|BigInt|Map|Set|WeakMap|WeakSet|Error|Date|JSON|React|useState|useEffect|useMemo|useCallback|useRef|useContext|useReducer)\b'),
            ('REACT_METHOD', r'\b(?:map|filter|reduce|find|findIndex|some|every|forEach|push|pop|shift|unshift|slice|splice|includes|indexOf|setUser|setUsers|setCount|setTodos|setItems|preventDefault|stopPropagation|addEventListener|removeEventListener|debounce|throttle)\b'),
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
            elif kind == 'REACT_METHOD':
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
    
    # 3. Main React & Framework Headers (Amber / Gold)
    t = re.sub(r'\b(Advanced JS for React|React|Next\.js|Full Stack|Modern JavaScript|React State|React UI|API / Async|Syntax|Data|Logic)\b', r'<span style="color: #fde047; font-weight: 700;">\1</span>', t)
    
    # 4. Specific Methods & Patterns (Lavender / Violet)
    t = re.sub(r'\b(Destructuring|Spread/Rest|spread|rest|map/filter|map|filter|find/reduce|find|reduce|some/every|some|every|Arrow Function|ternary|\&\& / \?\?|optional chaining|Promise / await|Add|Update|Delete)\b', r'<span style="color: #c084fc; font-weight: 700;">\1</span>', t)
    
    # 5. Engineering Principles & Positive Attributes (Emerald / Mint)
    t = re.sub(r'\b(Immutability|Immutable|Pure Function|Shallow Copy|Deep Copy|Clean|Safe|State-safe|Valid|Success)\b', r'<span style="color: #34d399; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(✓|✔)', r'<span style="color: #4ade80; font-weight: bold;">\1</span>', t)
    
    # 6. Domain Actors & Variables (Sky / Cyan)
    t = re.sub(r'\b(User|Users|Todo|Todos|Cart|Item|Product|Admin|Ripon|Rahim|Karim|count|setCount)\b', r'<span style="color: #38bdf8; font-weight: 600;">\1</span>', t)
    
    # 7. Mutations, Hazards & Pitfalls (Rose / Crimson)
    t = re.sub(r'\b(Mutation|Bug|Crash|Anti-pattern|Stale closure|Direct mutation|Index as key)\b', r'<span style="color: #f43f5e; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(✗|✘|X)', r'<span style="color: #f43f5e; font-weight: bold;">\1</span>', t)
    
    return t

def render_ascii_box(text, title=None):
    if not title:
        if 'Advanced JS for React' in text or 'Mental Map' in text:
            title = "REACT JAVASCRIPT ARCHITECTURE TAXONOMY"
        elif 'Immutability' in text or 'State' in text:
            title = "IMMUTABLE REACT STATE LIFECYCLE"
        elif 'JavaScript' in text and 'Next.js' in text:
            title = "FULL-STACK JAVASCRIPT TO REACT PROGRESSION"
        elif 'Syntax' in text or 'Logic' in text:
            title = "CORE JAVASCRIPT PILLARS FOR REACT"
        else:
            title = "REACT ARCHITECTURAL DIAGRAM"
            
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

# Part Banners configuration for Chapter 38
PART_BANNERS = {
    1: ("Part 01", "Modern Syntax in React: Destructuring, Spread & Rest (38.1 – 38.5)"),
    6: ("Part 02", "Array Transformations & Iteration in React (map, filter, find, reduce) (38.6 – 38.12)"),
    13: ("Part 03", "Immutability, State Updates & Reference vs Value (38.13 – 38.20)"),
    21: ("Part 04", "Safe Access, Short-Circuiting, Ternaries & Higher-Order Functions (38.21 – 38.27)"),
    28: ("Part 05", "Closures, State Mechanics, Pure Functions & ES Modules (38.28 – 38.35)"),
    36: ("Part 06", "Async Data Fetching, Event System, Debounce & Throttle (38.36 – 38.44)"),
    45: ("Part 07", "Advanced State Updates, Common React Pitfalls & Real Todo Architecture (38.45 – 38.54)"),
    55: ("Part 08", "Must Know Pillars, Quick Cheat Sheet, 8 Practice Labs & Final Mental Map"),
}

# Split markdown into sections
raw_sections = re.split(r'\n(?=# (?:[^\n]*?)?38\.\d+\s*(?:—|-)?\s*)', raw_md)
print(f"Total raw section chunks parsed: {len(raw_sections)}")

# Separate Section 55 (which contains Must Know, Cheat Sheet, Practice Set, and Final Mental Map)
sec55_full = raw_sections[55]
sec55_subparts = re.split(r'\n(?=# (?:🧠\s*Quick|📝\s*Practice|🎯\s*Final))', sec55_full)

mustknow_clean = sec55_subparts[0].strip()
cheatsheet_clean = sec55_subparts[1].strip() if len(sec55_subparts) > 1 else ""
practice_clean = sec55_subparts[2].strip() if len(sec55_subparts) > 2 else ""
mentalmap_clean = sec55_subparts[3].strip() if len(sec55_subparts) > 3 else ""

html_parts = []

# Document Header & CSS Tokens
html_parts.append('''<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter 38 — Advanced JavaScript for React | JavaScript Master Study Documentation</title>
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

    /* Master Top Banner */
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
      gap: 10px;
      margin-bottom: 4px;
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
    .banner-title-group {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
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

    /* Practice Lab Items */
    .practice-item {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-left: 3px solid var(--blue-accent);
      border-radius: 6px;
      padding: 8px 11px;
      margin-bottom: 7px;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
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
      #sec-38-1 {
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

    <!-- Header Master Banner (Classic 1-10 Style + JS Yellow & Prominent Chapter Title) -->
    <header class="master-banner">
      <div class="banner-top">
        <div class="banner-icon">JS</div>
        <div class="banner-title-group">
          <span class="banner-title">JavaScript Master Study Documentation</span>
          <span class="chapter-badge">Chapter 38</span>
        </div>
      </div>
      <div class="banner-sub">ADVANCED JAVASCRIPT FOR REACT: IMMUTABILITY, STATE MECHANICS, CLOSURES &amp; RENDERING PATTERNS</div>
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">Total Modules</div>
          <div class="meta-val">55 Modules + 8 Practice Labs</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Curriculum Part</div>
          <div class="meta-val">Part 32 — React Engineering Foundations</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Core Innovations</div>
          <div class="meta-val">Immutability, State Pipelines, Closures</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Target Architecture</div>
          <div class="meta-val">React 18/19, Next.js &amp; Component Model</div>
        </div>
      </div>
    </header>

    <!-- Chapter Opening Statement (Page 1 Balance) -->
    <div class="opening-card">
      <div class="opening-title">
        <span>✨</span> Advanced JavaScript for React — আধুনিক ফ্রন্টএন্ডের মূল চালিকাশক্তি
      </div>
      <p class="text-p">
        React শেখা মানে মূলত আধুনিক JavaScript-এর অ্যাডভান্সড ফিচার ও প্যাটার্নসমূহ আয়ত্ত করা। শুধু JSX বা <code>useState()</code> জানলেই চলে না—ইমিউটেবল স্টেট আপডেট, ক্লোজার, হাইয়ার-অর্ডার ফাংশন, রেফারেন্স বনাম ভ্যালু, অ্যারে ট্রান্সফর্মেশন (<code>map/filter/reduce</code>), অপশনাল চেইনিং, ইভেন্ট ডেলিগেশন এবং ডিবউন্সিং/থ্রটলিং জানা অপরিহার্য। এই চ্যাপ্টারে আমরা এই প্রতিটি বিষয় বাস্তব কোডসহ বিশদভাবে শিখব।
      </p>
      <div class="roadmap-grid">
        <div class="roadmap-item"><span>📌</span> 1. Destructuring &amp; Spread</div>
        <div class="roadmap-item"><span>📌</span> 2. map() &amp; filter()</div>
        <div class="roadmap-item"><span>📌</span> 3. Immutability &amp; State</div>
        <div class="roadmap-item"><span>📌</span> 4. Reference vs Value</div>
        <div class="roadmap-item"><span>📌</span> 5. Closures in React</div>
        <div class="roadmap-item"><span>📌</span> 6. Async/Await in React</div>
        <div class="roadmap-item"><span>📌</span> 7. Synthetic Events</div>
        <div class="roadmap-item"><span>📌</span> 8. Debounce &amp; Throttle</div>
        <div class="roadmap-item"><span>📌</span> 9. Nested State Updates</div>
        <div class="roadmap-item"><span>📌</span> 10. Common React Mistakes</div>
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
                if cur_lang in ('javascript', 'js', 'jsx'):
                    res.append(f'      {render_code_box(code_content, lang=cur_lang if cur_lang else "javascript")}\n')
                elif cur_lang in ('bash', 'sh', 'shell'):
                    res.append(f'      {render_code_box(code_content, lang="bash", title="TERMINAL COMMAND")}\n')
                elif cur_lang == 'json':
                    res.append(f'      {render_code_box(code_content, lang="json", title="JSON CONFIG")}\n')
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

# Process sections 1 to 54
for idx in range(1, 55):
    sec_text = raw_sections[idx].strip()
    pb = check_part_banner(idx)
    if pb:
        html_parts.append(f'    {pb}\n')
        
    sec_lines = sec_text.split('\n')
    header_line = sec_lines[0]
    m_head = re.search(r'# (?:🔥\s*|⚠️\s*)?(38\.\d+)\s*(?:—|-)?\s*(.*)', header_line)
    if m_head:
        sec_num = m_head.group(1)
        sec_title = m_head.group(2)
    else:
        sec_num = f'38.{idx}'
        sec_title = header_line.replace('#', '').strip()
        
    card_extra = ''
    if idx == 1:
        card_extra = ' id="sec-38-1"'
        
    html_parts.append(f'''    <div class="study-card"{card_extra}>
      <div class="card-title"><span class="badge-num">{sec_num}</span> {inline_format(sec_title)}</div>
''')
    
    body_text = '\n'.join(sec_lines[1:]).strip()
    html_parts.append(process_section_body(body_text))
    html_parts.append('    </div>\n')

# Process Section 55: MUST KNOW & Importance Table
pb55 = check_part_banner(55)
if pb55:
    html_parts.append(f'    {pb55}\n')

mustknow_lines = mustknow_clean.split('\n')
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">38.55</span> 🔥 MUST KNOW — React-এর জন্য অপরিহার্য JavaScript কনসেপ্ট</div>
''')
html_parts.append(process_section_body('\n'.join(mustknow_lines[1:]).strip()))
html_parts.append('    </div>\n')

# Quick Cheat Sheet Card
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">38.56</span> 🧠 Quick Cheat Sheet — React JavaScript সিনট্যাক্স সামারি</div>
''')
cheatsheet_lines = cheatsheet_clean.split('\n')
html_parts.append(process_section_body('\n'.join(cheatsheet_lines[1:]).strip()))
html_parts.append('    </div>\n')

# 8 Hands-on Practice Labs with Complete Solutions
html_parts.append('''    <div class="part-banner">Part 08.1 — 8 Hands-On Practice Labs with Complete Production Solutions</div>
''')

practice_solutions = [
    (
        1, "Beginner", "Array Filtering — Extracting Adults (Age >= 18)",
        "প্রদত্ত ইউজার অ্যারে থেকে filter() মেথড ব্যবহার করে শুধুমাত্র ১৮ বা তার বেশি বয়সের ইউজারদের ফিল্টার করুন।",
        """const users = [
  { name: "A", age: 15 },
  { name: "B", age: 20 },
  { name: "C", age: 25 }
];

// Modern ES6+ / React Pattern
const adultUsers = users.filter(user => user.age >= 18);

console.log(adultUsers);
// Output: [ { name: 'B', age: 20 }, { name: 'C', age: 25 } ]""",
        None,
        "filter() মূল অ্যারে মিউটেট না করে একটি সম্পূর্ণ নতুন অ্যারে তৈরি করে, যা React-এর স্টেট ফিল্টারিং ও সার্চ ফিচারে শতভাগ নিরাপদ।"
    ),
    (
        2, "Beginner", "Array Projection — Mapping Array of Names",
        "ইউজার অবজেক্ট অ্যারে থেকে map() ব্যবহার করে শুধুমাত্র ইউজারদের নামের একটি স্ট্রিং অ্যারে তৈরি করুন।",
        """const users = [
  { name: "A", age: 15 },
  { name: "B", age: 20 },
  { name: "C", age: 25 }
];

// React Projection Pattern
const userNames = users.map(user => user.name);

console.log(userNames);
// Output: ["A", "B", "C"]""",
        None,
        "map() মেথডটি মূল অ্যারের প্রতিটি উপাদান রূপান্তর করে সমপরিমাণ উপাদানের নতুন অ্যারে বানায়—যা React-এ ডেটা থেকে JSX এলিমেন্ট রেন্ডারিংয়ের মূল ভিত্তি।"
    ),
    (
        3, "Beginner", "Immutable Item Update — Updating Object by ID",
        "map() এবং Spread Operator ব্যবহার করে id = 2 ইউজারের নাম পরিবর্তন করে 'Ripon' করুন (অন্যান্য উপাদান অক্ষত রেখে)।",
        """const users = [
  { id: 1, name: "Tanvir" },
  { id: 2, name: "OldName" },
  { id: 3, name: "Karim" }
];

// Immutable Update Pattern
const targetId = 2;
const updatedUsers = users.map(user => 
  user.id === targetId 
    ? { ...user, name: "Ripon" } 
    : user
);

console.log(updatedUsers);
// Output: [ { id: 1, name: 'Tanvir' }, { id: 2, name: 'Ripon' }, { id: 3, name: 'Karim' } ]""",
        None,
        "React স্টেটে কোনো অবজেক্ট সরাসরি মিউটেট করা নিষিদ্ধ। টার্নারি অপারেটর এবং অবজেক্ট স্প্রেড({...user}) দিয়ে টার্গেট আইটেমটির কপি তৈরি করে আপডেট করতে হয়।"
    ),
    (
        4, "Beginner", "Immutable Item Deletion — Removing Object by ID",
        "filter() মেথড ব্যবহার করে id = 3 ইউজারটিকে অ্যারে থেকে নিরাপদে মুছে ফেলুন।",
        """const users = [
  { id: 1, name: "Tanvir" },
  { id: 2, name: "Ripon" },
  { id: 3, name: "Karim" }
];

// Immutable Delete Pattern
const deleteId = 3;
const remainingUsers = users.filter(user => user.id !== deleteId);

console.log(remainingUsers);
// Output: [ { id: 1, name: 'Tanvir' }, { id: 2, name: 'Ripon' } ]""",
        None,
        "React-এ Delete অপারেশনের জন্য splice() ব্যবহার করলে মূল অ্যারে পরিবর্তিত হয়ে যায়। filter() মেথড শর্ত না মেলা আইটেমগুলো বাদ দিয়ে নতুন অ্যারে দেয়।"
    ),
    (
        5, "Intermediate", "Array Aggregation — Shopping Cart Total via reduce()",
        "reduce() মেথড ব্যবহার করে শপিং কার্টের সকল আইটেমের মোট মূল্য (Total Price) বের করুন।",
        """const cart = [
  { name: "Laptop", price: 80000 },
  { name: "Mouse", price: 1000 },
  { name: "Keyboard", price: 3000 }
];

// React / E-Commerce Accumulator Pattern
const totalPrice = cart.reduce((accumulator, item) => accumulator + item.price, 0);

console.log('Total Cart Amount: ৳' + totalPrice);
// Output: Total Cart Amount: ৳84000""",
        None,
        "reduce() মেথডে প্রারম্ভিক মান (Initial Value: 0) উল্লেখ করা বাধ্যতামূলক। এটি কার্ট টোটাল, ট্যাক্স বা ডিসকাউন্ট ক্যালকুলেশনের স্ট্যান্ডার্ড পদ্ধতি।"
    ),
    (
        6, "Intermediate", "React Component Bug Fix — Missing Return in map()",
        "নিচের কম্পোনেন্টটিতে map() এ ব্র্যাকেট দেওয়ার কারণে JSX রিটার্ন হচ্ছে না। এরর খুঁজে বের করে প্রোডাকশন-রেডি ফিক্স লিখুন।",
        """// ❌ Buggy Version (Returns undefined for each item)
// function Users({ users }) {
//   return (<div>{users.map(user => { <p>{user.name}</p> })}</div>);
// }

// ✅ Fixed Version 1: Implicit Return with Parentheses
function UsersImplicit({ users }) {
  return (
    <div>
      {users.map(user => (
        <p key={user.id}>{user.name}</p>
      ))}
    </div>
  );
}

// ✅ Fixed Version 2: Explicit Return Keyword with Curly Braces
function UsersExplicit({ users }) {
  return (
    <div>
      {users.map(user => {
        return <p key={user.id}>{user.name}</p>;
      })}
    </div>
  );
}""",
        None,
        "অ্যারো ফাংশনে কার্লি ব্রেস {} দিলে বডি তৈরি হয়, ফলে রিটার্ন করতে হলে 'return' কিওয়ার্ড লিখতে হয়। অথবা প্যারেন্থেসিস () দিয়ে ইমপ্লিসিট রিটার্ন করতে হয়। সাথে অনন্য key প্রপ যুক্ত করা জরুরি।"
    ),
    (
        7, "Intermediate", "Functional State Update — Immutable Top-Level Property",
        "React Functional setState প্যাটার্ন মেনে user অবজেক্টের age প্রপার্টি ২৩ থেকে ২৪ এ আপডেট করুন।",
        """const [user, setUser] = [
  { name: "Ripon", age: 23 },
  newUser => console.log('Updated User State:', newUser)
];

// React Functional State Update Pattern
setUser(prevUser => ({
  ...prevUser,
  age: 24
}));

// Output: Updated User State: { name: 'Ripon', age: 24 }""",
        None,
        "setState-এ ফাংশনাল আপডেট (prev => ({ ...prev, prop })) ব্যবহার করলে রেস কন্ডিশন ও স্টেল স্টেট (Stale State) এরর সম্পূর্ণ দূর হয়।"
    ),
    (
        8, "Advanced", "Deep Immutable Update — Nested Object State Modification",
        "Nested অবজেক্টের গভীরের প্রপার্টি (address.city) মিউটেট না করে স্প্রেড অপারেটর দিয়ে 'Dhaka' থেকে 'Dinajpur' এ আপডেট করুন।",
        """const user = {
  name: "Ripon",
  address: {
    city: "Dhaka",
    country: "Bangladesh"
  }
};

// ❌ Buggy Shallow Spread: user.address মিউটেট হয়ে যায়
// const wrong = { ...user, address: { city: 'Dinajpur' } }; // country হারিয়ে যাবে!

// ✅ Correct Deep Immutable Spread
const updatedUser = {
  ...user,
  address: {
    ...user.address,
    city: "Dinajpur"
  }
};

console.log(updatedUser);
// Output: { name: 'Ripon', address: { city: 'Dinajpur', country: 'Bangladesh' } }""",
        None,
        "Shallow Spread কেবল প্রথম লেভেলের প্রপার্টি কপি করে। নেস্টেড অবজেক্ট থাকলে ভেতরের অবজেক্টকেও আলাদাভাবে স্প্রেড ({...user.address}) করতে হয়, নতুবা অবজেক্টের অন্যান্য প্রপার্টি মুছে যাবে।"
    )
]

for lab_num, lab_level, lab_title, lab_desc, lab_code, lab_output, lab_expl in practice_solutions:
    html_parts.append(f'''    <div class="practice-item">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
        <span style="font-weight: 700; font-size: 11px; color: var(--navy-deep);">Lab {lab_num}: {inline_format(lab_title)}</span>
        <span style="background: #e0f2fe; color: #0284c7; font-size: 8px; font-weight: 700; padding: 1px 6px; border-radius: 3px; text-transform: uppercase;">{lab_level}</span>
      </div>
      <p class="text-p"><strong>সমস্যা ও লক্ষ্য:</strong> {inline_format(lab_desc)}</p>
      {render_code_box(lab_code, lang='javascript', title=f'PRODUCTION SOLUTION: LAB {lab_num}')}
''')
    if lab_output:
        html_parts.append(f'      {render_ascii_box(lab_output, title="EXECUTION OUTPUT")}\n')
    if lab_expl:
        html_parts.append(f'      <div class="def-box">💡 <strong>রিঅ্যাক্ট আর্কিটেকচারাল ব্যাখ্যা:</strong> {inline_format(lab_expl)}</div>\n')
    html_parts.append('    </div>\n')

# Section 38.57: Final Mental Map
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">38.57</span> 🎯 Final Mental Map — React-এর জন্য JavaScript আর্কিটেকচার মানচিত্র</div>
      <p class="text-p">পুরো Chapter 38-এর JavaScript ও React সমন্বয় একনজরে:</p>
''')

final_tree = """                 Advanced JS for React
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
     Syntax             Data             Logic
       │                 │                 │
 Destructuring       map/filter        ternary
 Spread/Rest         find/reduce       && / ??
 Arrow Function      some/every        optional chaining
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
                    React State
                         │
                  Immutability
                         │
             ┌───────────┼───────────┐
             │           │           │
            Add        Update       Delete
             │           │           │
           spread       map        filter
                         │
                         ↓
                    API / Async
                         │
                   Promise / await
                         │
                         ↓
                    React UI"""

html_parts.append(f'      {render_ascii_box(final_tree, title="REACT JAVASCRIPT TAXONOMY MAP")}\n')
html_parts.append('''      <div class="def-box" style="margin-top: 6px; border-left: 3px solid #d97706; background: #fffbeb;">
        🏆 <strong>এক লাইনে Chapter 38:</strong> React ফ্রেমওয়ার্ক শেখার প্রথম ও প্রধান ভিত্তি হলো আধুনিক JavaScript-এর Destructuring, Spread, map/filter/reduce, Immutability এবং Async/Await—এগুলো আয়ত্ত করলেই React কোড পানির মতো সহজ মনে হবে।
      </div>
    </div>
''')

# Curriculum Progression Card (Chapter 37 -> 38 -> 39)
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">38.58</span> 🔗 Curriculum Progression: Chapter 37 → 38 → 39</div>
''')

curriculum_tree = """Chapter 37: JavaScript Design Patterns
       ↓
Creational, Structural, Behavioral, MVC, Dependency Injection & Repository
       ↓
Chapter 38: Advanced JavaScript for React (THIS CHAPTER)
       ↓
Destructuring, Spread, map/filter, Immutability, Closures, Synthetic Events
       ↓
Chapter 39: Advanced JavaScript for Node.js
       ↓
Node.js Architecture, Libuv, Event Loop Phases, Streams, Buffer, Worker Threads"""

html_parts.append(f'      {render_ascii_box(curriculum_tree, title="ROADMAP CONTINUITY PIPELINE")}\n')
html_parts.append('    </div>\n')

# Document Closure
html_parts.append('''
  </div>
</body>
</html>''')

# Write complete HTML file
output_html_path = r'c:\Users\User\Desktop\Note-Book\Code\Chapter-38-Advanced-JavaScript-for-React.html'
with open(output_html_path, 'w', encoding='utf-8') as f:
    f.write(''.join(html_parts))

print(f"HTML successfully generated at: {output_html_path}")
print(f"File size: {os.path.getsize(output_html_path)} bytes")
