import re
import sys
import html
import os

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Read raw markdown
with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-36.md', 'r', encoding='utf-8') as f:
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
    
    if lang in ('javascript', 'js'):
        token_spec = [
            ('COMMENT_MULTI', r'/\*[\s\S]*?\*/'),
            ('COMMENT_LINE', r'//.*$'),
            ('REGEX_LIT', r'/(?:\\/|[^\n\r/])+/[gimsuy]*'),
            ('STRING_TMPL', r'`(?:\\.|[^`\\])*`'),
            ('STRING_DBL', r'"(?:\\.|[^"\\])*"'),
            ('STRING_SGL', r"'(?:\\.|[^'\\])*'"),
            ('KEYWORD', r'\b(?:for|while|do|break|continue|if|else|let|const|var|function|return|switch|case|default|of|in|new|typeof|delete|this|super|class|extends|static|instanceof|try|catch|finally|throw|await|async|yield|import|export|from|default|using)\b'),
            ('BOOL_NULL', r'\b(?:true|false|null|undefined|NaN)\b'),
            ('DOM_BUILTIN', r'\b(?:console|window|document|process|Object|Array|Promise|String|Number|Math|BigInt|Map|Set|WeakRef|FinalizationRegistry|AggregateError|Temporal|Error)\b'),
            ('ASYNC_METHOD', r'\b(?:then|catch|finally|resolve|reject|allSettled|any|race|all|withResolvers|at|findLast|findLastIndex|toSorted|toReversed|toSpliced|with|groupBy|hasOwn|replaceAll|isWellFormed|toWellFormed|push|slice|splice|map|filter|reduce|forEach|deposit|getBalance)\b'),
            ('OPERATOR', r'(?:\?\.|(?<!\?)\?\?(?!\?)|(?<!\?)\?\?=|&&=|\|\|=|#)'),
            ('NUMBER', r'\b\d+(?:_\d+)*(?:\.\d+)?n?\b'),
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
            elif kind == 'ASYNC_METHOD':
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
    
    # 1. Colorize arrows & directional paths (Cyan)
    t = re.sub(r'([↓↑→←▼▲►◄])', r'<span style="color: #38bdf8; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(───+|──|─►|◄─)', r'<span style="color: #0ea5e9; font-weight: 600;">\1</span>', t)
    
    # 2. Colorize Box frames & connectors (Slate)
    t = re.sub(r'([┌┐└┘├┤┬┴│┼]+)', r'<span style="color: #475569;">\1</span>', t)
    t = re.sub(r'(\-{3,})', r'<span style="color: #334155;">\1</span>', t)
    
    # 3. ECMAScript Versions & Specifications (Amber / Gold)
    t = re.sub(r'\b(ECMAScript|ES2020|ES2021|ES2022|ES2023|ES2024|ES2025|ES2026|TC39|Specification|Engine|V8|SpiderMonkey|JavaScript Engine|MODERN ECMASCRIPT|Modern JS|React|Node\.js|APIs)\b', r'<span style="color: #fde047; font-weight: 700;">\1</span>', t)
    
    # 4. Modern Operators & Methods (Lavender / Violet)
    t = re.sub(r'(\?\.|(?<!\?)\?\?(?!\?)|(?<!\?)\?\?=|&&=|\|\|=|#private|#balance|#field|#fields|#password|#connection|toSorted\(\)|toReversed\(\)|toSpliced\(\)|with\(\)|groupBy\(\)|findLast\(\)|findLastIndex\(\)|withResolvers\(\)|allSettled\(\)|any\(\)|replaceAll\(\)|Immutable Arrays|top-level await|class fields|Numeric _)', r'<span style="color: #c084fc; font-weight: 700;">\1</span>', t)
    
    # 5. Safe & Immutable States (Emerald / Mint)
    t = re.sub(r'\b(Safe|Immutable|Fulfilled|Pass|Success|Defined|Resolved|Valid|Active|State-safe|Clean)\b', r'<span style="color: #34d399; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(✓|✔)', r'<span style="color: #4ade80; font-weight: bold;">\1</span>', t)
    
    # 6. Errors, Hazards & Mutability (Rose / Crimson)
    t = re.sub(r'\b(TypeError|Cannot read properties|null or undefined|Uncaught|Error\.cause|AggregateError|Mutation|Bug|Crash|Breaking|Mutates original)\b', r'<span style="color: #f43f5e; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(✗|✘|X)', r'<span style="color: #f43f5e; font-weight: bold;">\1</span>', t)
    
    return t

def render_ascii_box(text, title=None):
    if not title:
        if 'ECMASCRIPT' in text or 'ES2020' in text:
            title = "MODERN ECMASCRIPT TIMELINE & EVOLUTION"
        elif 'Specification' in text or 'Engine' in text:
            title = "ECMASCRIPT SPECIFICATION VS RUNTIME ENGINES"
        elif 'Immutability' in text or 'toSorted' in text:
            title = "IMMUTABLE ARRAY METHODS PIPELINE"
        elif 'React' in text or 'Node' in text:
            title = "FULL-STACK MODERN JAVASCRIPT TOOLKIT"
        else:
            title = "MODERN JAVASCRIPT ARCHITECTURE FLOW"
            
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

# Part Banners configuration for Chapter 36
PART_BANNERS = {
    1: ("Part 01", "ECMAScript Standards, Specification & Evolution (36.1 – 36.3)"),
    4: ("Part 02", "Null Safety: Optional Chaining (?.) & Nullish Coalescing (??) (36.4 – 36.8)"),
    9: ("Part 03", "Logical Assignments (??=, &&=, ||=) & String Tools (36.9 – 36.12)"),
    13: ("Part 04", "Modern Promise Concurrency: allSettled, any & withResolvers (36.13 – 36.15, 36.39)"),
    16: ("Part 05", "Code Readability: Numeric Separators & Logical Assignment Patterns (36.16 – 36.17)"),
    18: ("Part 06", "Modern Class Architecture: Private Fields (#), Statics & Blocks (36.18 – 36.22)"),
    23: ("Part 07", "Top-Level Await, Negative Indexing (.at) & Error Causes (36.23 – 36.28)"),
    29: ("Part 08", "Array Querying & Immutable Methods (toSorted, toSpliced, with) (36.29 – 36.36)"),
    37: ("Part 09", "Data Grouping (Object.groupBy, Map.groupBy) & Unicode (36.37 – 36.41)"),
    42: ("Part 10", "Emerging Standards: Temporal API & Explicit Resource Management (36.42 – 36.43)"),
    44: ("Part 11", "Modern JavaScript Paradigms: Immutability, React & Node.js (36.44 – 36.49)"),
    50: ("Part 12", "Browser Compatibility, Transpilation, Polyfills & ES2020+ Map (36.50 – 36.57)"),
    58: ("Part 13", "Must Know Modern Pillars, Quick Cheat Sheet, 8 Practice Labs & Final Mental Map"),
}

# Split markdown into sections
raw_sections = re.split(r'\n(?=# 36\.\d+\s*(?:—|-)?\s*)', raw_md)
print(f"Total raw section chunks parsed: {len(raw_sections)}")

# Separate Section 57 from Must Know, Cheat Sheet, Practice Set, and Final Mental Map
sec57_full = raw_sections[57]
sec57_subparts = re.split(r'\n(?=# (?:🔥\s*MUST|🧠\s*Quick|📝\s*Practice|🎯\s*Final))', sec57_full)

sec57_clean = sec57_subparts[0].strip()
mustknow_clean = sec57_subparts[1].strip() if len(sec57_subparts) > 1 else ""
cheatsheet_clean = sec57_subparts[2].strip() if len(sec57_subparts) > 2 else ""
practice_clean = sec57_subparts[3].strip() if len(sec57_subparts) > 3 else ""
mentalmap_clean = sec57_subparts[4].strip() if len(sec57_subparts) > 4 else ""

html_parts = []

# Document Header & CSS Tokens
html_parts.append('''<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter 36 — Modern ECMAScript / ES2020+ Features | JavaScript Master Study Documentation</title>
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
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .def-box {
      background: #f8fafc;
      border-left: 3px solid #64748b;
      padding: 5px 8px;
      border-radius: 0 4px 4px 0;
      font-size: 10px;
      margin: 4px 0;
      color: #334155;
    }

    /* Code Blocks */
    .code-box {
      background: #0f172a;
      border-radius: 5px;
      margin: 4px 0 5px 0;
      overflow: hidden;
      border: 1px solid #1e293b;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }
    .code-top {
      background: #1e293b;
      color: #94a3b8;
      font-family: var(--font-code);
      font-size: 8.5px;
      padding: 2.5px 8px;
      display: flex;
      justify-content: space-between;
      border-bottom: 1px solid #334155;
      text-transform: uppercase;
    }
    .code-box pre {
      margin: 0;
      padding: 6px 10px;
      overflow-x: hidden !important;
      white-space: pre-wrap !important;
      word-break: break-word !important;
    }
    .code-box code {
      font-family: var(--font-code);
      font-size: 9px;
      line-height: 1.35;
      color: #f1f5f9;
      white-space: pre-wrap !important;
      word-break: break-word !important;
    }
    .syn-kw { color: #f472b6; font-weight: 600; }
    .syn-fn { color: #38bdf8; font-weight: 600; }
    .syn-str { color: #4ade80; }
    .syn-num { color: #fb923c; }
    .syn-com { color: #64748b; font-style: italic; }
    .syn-bool { color: #c084fc; font-weight: 600; }

    /* Output Box */
    .output-box {
      background: #182234;
      border-left: 3px solid #10b981;
    }
    .out-label {
      color: #34d399;
      font-weight: 700;
    }

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
      #sec-36-1 {
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
          <span class="chapter-badge">Chapter 36</span>
        </div>
      </div>
      <div class="banner-sub">MODERN ECMASCRIPT, ES2020–ES2026+ ADVANCED SYNTAX, IMMUTABLE APIS &amp; RUNTIME INNOVATIONS</div>
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">Total Modules</div>
          <div class="meta-val">57 Modules + 8 Practice Labs</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Curriculum Part</div>
          <div class="meta-val">Part 30 — Modern ECMAScript Standards</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Core Innovations</div>
          <div class="meta-val">Null Safety, Immutability, Private Fields</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Reference Standard</div>
          <div class="meta-val">TC39 Living Standard ES2020–ES2026</div>
        </div>
      </div>
    </header>

    <!-- Chapter Opening Statement (Page 1 Balance) -->
    <div class="opening-card">
      <div class="opening-title">
        <span>✨</span> Modern ECMAScript (ES2020+) — আধুনিক জাভাস্ক্রিপ্ট সিনট্যাক্স, ইমিউটেবিলিটি ও পারফরম্যান্স
      </div>
      <p class="text-p">
        জাভাস্ক্রিপ্ট একটি জীবন্ত ভাষা যা প্রতি বছর নতুন নতুন শক্তিশালী ফিচার ও সিনট্যাক্টিক সুবিধায় সমৃদ্ধ হচ্ছে। কোডকে নাল-পয়েন্টার এরর থেকে রক্ষা করা, স্টেট মিউটেশনের ঝুঁকিহীন ইমিউটেবল অ্যারে মেথড এবং ক্লাস এনক্যাপসুলেশন নিশ্চিত করাই আধুনিক ECMAScript-এর লক্ষ্য। এই চ্যাপ্টারে আমরা <strong>Optional Chaining (?.), Nullish Coalescing (??), Logical Assignments, Private Class Fields (#), Top-Level await, .at(), Immutable Arrays (toSorted, toSpliced, with), Object.groupBy, Promise.withResolvers</strong> এবং Temporal API শিখব।
      </p>
      <div class="roadmap-grid">
        <div class="roadmap-item"><span>📌</span> 1. Optional Chaining</div>
        <div class="roadmap-item"><span>📌</span> 2. Nullish Coalescing</div>
        <div class="roadmap-item"><span>📌</span> 3. Logical Assignments</div>
        <div class="roadmap-item"><span>📌</span> 4. Private Class Fields</div>
        <div class="roadmap-item"><span>📌</span> 5. Top-Level await</div>
        <div class="roadmap-item"><span>📌</span> 6. Negative Index (.at)</div>
        <div class="roadmap-item"><span>📌</span> 7. Immutable Arrays</div>
        <div class="roadmap-item"><span>📌</span> 8. Object.groupBy()</div>
        <div class="roadmap-item"><span>📌</span> 9. Promise.withResolvers</div>
        <div class="roadmap-item"><span>📌</span> 10. Modern React Toolkit</div>
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
            
        if ls.startswith('### '):
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

# Process sections 1 to 56
for idx in range(1, 57):
    sec_text = raw_sections[idx].strip()
    pb = check_part_banner(idx)
    if pb:
        html_parts.append(f'    {pb}\n')
        
    sec_lines = sec_text.split('\n')
    header_line = sec_lines[0]
    m_head = re.search(r'# (?:🔥\s*|⚠️\s*)?(36\.\d+)\s*(?:—|-)?\s*(.*)', header_line)
    if m_head:
        sec_num = m_head.group(1)
        sec_title = m_head.group(2)
    else:
        sec_num = f'36.{idx}'
        sec_title = header_line.replace('#', '').strip()
        
    card_extra = ''
    if idx == 1:
        card_extra = ' id="sec-36-1"'
        
    html_parts.append(f'''    <div class="study-card"{card_extra}>
      <div class="card-title"><span class="badge-num">{sec_num}</span> {inline_format(sec_title)}</div>
''')
    
    body_text = '\n'.join(sec_lines[1:]).strip()
    html_parts.append(process_section_body(body_text))
    html_parts.append('    </div>\n')

# Process Section 57 (Cleaned of subparts)
pb57 = check_part_banner(57)
if pb57:
    html_parts.append(f'    {pb57}\n')
    
sec57_lines = sec57_clean.split('\n')
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">36.57</span> Modern JavaScript Interview Questions — ইন্টারভিউ প্রশ্নোত্তর</div>
''')
html_parts.append(process_section_body('\n'.join(sec57_lines[1:]).strip()))
html_parts.append('    </div>\n')

# Part 13 Banner & Section 36.58: MUST KNOW
pb13 = check_part_banner(58)
if pb13:
    html_parts.append(f'    {pb13}\n')

html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">36.58</span> 🔥 MUST KNOW — মডার্ন ECMAScript-এর ১০টি প্রধান স্তম্ভ</div>
      <p class="text-p">আধুনিক ফুলস্ট্যাক প্রজেক্টে (React &amp; Node.js) প্রতিদিন কাজে লাগার মতো ১০টি সেরা উদ্ভাবন:</p>
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 5px;">
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #0284c7; font-size: 10px; margin-bottom: 3px;">📌 1. Null Safety &amp; Operators</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li><strong>Optional Chaining (?.):</strong> নাল বা আনডিফাইন্ডে ক্র্যাশ ছাড়া এক্সেস</li>
            <li><strong>Nullish Coalescing (??):</strong> শুধুমাত্র null/undefined-এ ফলব্যাক (0 বা "" নিরাপদ)</li>
            <li><strong>Logical Assignments:</strong> ??=, &&=, ||= দিয়ে ক্লিন কনফিগ ইনিশিয়ালাইজ</li>
            <li><strong>Numeric Separators (_):</strong> 1_000_000 লিখে বড় সংখ্যার পঠনযোগ্যতা বৃদ্ধি</li>
          </ul>
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #059669; font-size: 10px; margin-bottom: 3px;">📌 2. Modern Classes &amp; Async</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li><strong>Private Fields (#):</strong> ট্রু ল্যাঙ্গুয়েজ-লেভেল এনক্যাপসুলেশন (#balance)</li>
            <li><strong>Static Blocks:</strong> ক্লাসে কমপ্লেক্স স্ট্যাটিক মেম্বার ইনিশিয়ালাইজেশন</li>
            <li><strong>Top-Level await:</strong> মডিউল লোডিংয়ের সময় অ্যাসিনক্রোনাস ডাটা ফেচ</li>
            <li><strong>Promise.allSettled &amp; any:</strong> রেজলভ ও রিজেক্টেড প্রমিজের নির্ভরযোগ্য হ্যান্ডলিং</li>
          </ul>
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #7c3aed; font-size: 10px; margin-bottom: 3px;">📌 3. Immutable Data &amp; Grouping</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li><strong>toSorted / toSpliced:</strong> মূল অ্যারে মিউটেট না করে নতুন অ্যারে রিটার্ন</li>
            <li><strong>Array.prototype.at(-1):</strong> নেগেটিভ ইনডেক্স দিয়ে লাস্ট উপাদান বের করা</li>
            <li><strong>Object.groupBy():</strong> ডাটাকে ক্যাটাগরি অনুযায়ী ডিক্ল্যারেটিভ গ্রুপিং</li>
            <li><strong>Error.cause:</strong> এরর ট্র্যাজেক্টরি ও রুট কজ চেইনিং</li>
          </ul>
        </div>
      </div>
    </div>
''')

# Quick Cheat Sheet Card
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">36.59</span> 🧠 Quick Cheat Sheet — আধুনিক সিনট্যাক্স ও মেথড সারসংক্ষেপ</div>
''')
cheat_table = '''| Feature / Method | Introduction | Syntax / Code Snippet | Primary Benefit |
| :--- | :--- | :--- | :--- |
| **Optional Chaining** | ES2020 | `user?.address?.city` | `TypeError: Cannot read properties of undefined` চিরতরে রোধ |
| **Nullish Coalescing** | ES2020 | `const port = customPort ?? 3000` | ফলসি ভ্যালু (`0`, `""`) নষ্ট না করে শুধু `null/undefined` চেক |
| **Promise.allSettled** | ES2020 | `Promise.allSettled([p1, p2])` | একটি ব্যর্থ হলেও সব প্রমিজের পূর্ণাঙ্গ ফলাফল পাওয়া যায় |
| **String.replaceAll** | ES2021 | `'a-b-c'.replaceAll('-', ' ')` | গ্লোবাল রেজেক্স (`/g`) ছাড়াই সকল ম্যাচ প্রতিস্থাপন |
| **Logical Assignment** | ES2021 | `options.timeout ??= 5000` | ভ্যালু নাল হলে তবেই শর্ট-সার্কিট অ্যাসাইনমেন্ট |
| **Numeric Separator** | ES2021 | `const salary = 1_500_000` | কোডের ভেতরে বড় সংখ্যার পঠনযোগ্যতা বৃদ্ধি |
| **Private Class Fields** | ES2022 | `class Bank { #pin = 1234; }` | ক্লাসের বাইরে থেকে ফিল্ড এক্সেস সম্পূর্ণ ব্লক |
| **Array.prototype.at()** | ES2022 | `arr.at(-1)` | নেগেটিভ ইনডেক্স দিয়ে পেছনের উপাদান এক্সেস |
| **Object.hasOwn()** | ES2022 | `Object.hasOwn(obj, 'prop')` | `hasOwnProperty` এর নিরাপদ ও সুরক্ষিত বিকল্প |
| **Error Cause** | ES2022 | `new Error('Fail', { cause: err })` | অরিজিনাল এরর সংরক্ষণ করে রুট-কজ চেইনিং |
| **Array.toSorted()** | ES2023 | `const sorted = arr.toSorted()` | মূল অ্যারে অক্ষত রেখে নতুন সর্টেড অ্যারে তৈরি (React-safe) |
| **Array.toSpliced()** | ES2023 | `const removed = arr.toSpliced(0, 1)` | ইমিউটেবল স্লাইসিং ও উপাদান অপসারণ |
| **Array.with()** | ES2023 | `const updated = arr.with(2, 99)` | নির্দিষ্ট ইনডেক্সের মান পরিবর্তন করে ফ্রেশ কপি রিটার্ন |
| **Array.findLast()** | ES2023 | `arr.findLast(n => n > 10)` | পেছনের দিক থেকে প্রথম ম্যাচিং উপাদান খুঁজে বের করা |
| **Object.groupBy()** | ES2024 | `Object.groupBy(users, u => u.role)` | অ্যারের অবজেক্টগুলোকে শর্তানুযায়ী ক্যাটাগরিাইজড অবজেক্টে রূপান্তর |
| **Promise.withResolvers** | ES2024 | `const { promise, resolve } = Promise.withResolvers()` | প্রমিজ ও রিজলভ/রিজেক্ট ফাংশন সরাসরি ডিকনস্ট্রাক্ট |'''
html_parts.append(f'      {render_table(cheat_table)}\n')
html_parts.append('    </div>\n')

# 8 Hands-on Practice Labs with Complete Solutions
html_parts.append('''    <div class="part-banner">Part 13.1 — 8 Hands-On Practice Labs with Complete Production Solutions</div>
''')

practice_solutions = [
    (
        1, "Beginner", "Falsy vs Nullish Evaluation Matrix (|| vs ??)",
        "নিচের তিনটি স্টেটমেন্টের এক্সিকিউশন আউটপুট কী হবে এবং 0 এর ক্ষেত্রে || এবং ?? কীভাবে ভিন্ন আচরণ করে তা ব্যাখ্যা করুন।",
        """// Input Evaluation Code
console.log(0 || 50);   // আউটপুট: 50
console.log(0 ?? 50);   // আউটপুট: 0
console.log(null ?? 50);// আউটপুট: 50""",
        None,
        "|| (Logical OR) অপারেটর 0-কে falsy মনে করে ডান পাশের মান (50) নেয়। কিন্তু ?? (Nullish Coalescing) শুধুমাত্র null ও undefined-কে অগ্রাহ্য করে; 0 একটি সম্পূর্ণ বৈধ সংখ্যা হওয়ায় 0-ই রিটার্ন করে।"
    ),
    (
        2, "Beginner", "Defensive Data Access with Optional Chaining (?.)",
        "nested অবজেক্ট থেকে ক্র্যাশ ছাড়া নিরাপদে ডাটা পড়তে Optional Chaining ও Nullish Coalescing ব্যবহার করে প্রোডাকশন ফাংশন লিখুন।",
        """const userA = {
  profile: {
    address: { city: 'Dhaka', zip: 1205 }
  }
};

const userB = { profile: null };

// ❌ Risky: userB-তে TypeError ক্র্যাশ করবে
// const city = userB.profile.address.city; 

// ✅ Modern Safe Navigation
function getCity(user) {
  return user?.profile?.address?.city ?? 'Unknown City';
}

console.log('User A City:', getCity(userA)); // Dhaka
console.log('User B City:', getCity(userB)); // Unknown City (No crash!)""",
        None,
        "?. অপারেটর চেইনের কোনো ধাপে null বা undefined পেলে সাথে সাথে এক্সিকিউশন থামিয়ে undefined রিটার্ন করে, ফলে TypeError চিরতরে দূর হয়।"
    ),
    (
        3, "Beginner", "Array End Indexing with Modern .at() Method",
        "Array-এর শেষ উপাদান বের করার জন্য ট্র্যাডিশনাল arr[arr.length - 1] এর বদলে আধুনিক .at(-1) মেথড প্রয়োগ করুন।",
        """const numbers = [10, 20, 30, 40];

// Old Syntax
const lastOld = numbers[numbers.length - 1];

// Modern ES2022 Syntax
const lastModern = numbers.at(-1);     // শেষ উপাদান: 40
const secondLast = numbers.at(-2);     // শেষের আগের উপাদান: 30

console.log('Last Element:', lastModern);
console.log('Second Last:', secondLast);""",
        None,
        ".at() মেথডটি শুধু অ্যারেতেই নয়, স্ট্রিং (string.at(-1)) এবং টাইপড অ্যারেতেও সমভাবে কাজ করে যা কোডকে আরও সংক্ষিপ্ত ও আধুনিক করে তোলে।"
    ),
    (
        4, "Intermediate", "True Class Encapsulation with Private Field (#balance)",
        "এমন একটি BankAccount ক্লাস তৈরি করুন যেখানে name পাবলিক, #balance প্রাইভেট এবং ভ্যালিডেশনসহ deposit() ও getBalance() মেথড থাকবে।",
        """class BankAccount {
  name;           // পাবলিক ফিল্ড
  #balance = 0;   // ট্রু প্রাইভেট ফিল্ড (ক্লাসের বাইরে সম্পূর্ণ অদৃশ্য)

  constructor(accountHolder, initialDeposit = 0) {
    this.name = accountHolder;
    if (initialDeposit > 0) this.#balance = initialDeposit;
  }

  deposit(amount) {
    if (amount <= 0) {
      throw new Error('Deposit amount must be strictly positive');
    }
    this.#balance += amount;
    return this.#balance;
  }

  getBalance() {
    return this.#balance;
  }
}

const account = new BankAccount('Tanvir', 500);
account.deposit(250);
console.log(`${account.name} Balance: $${account.getBalance()}`); // $750

// ❌ SyntaxError: Private field '#balance' must be declared in an enclosing class
// console.log(account.#balance);""",
        None,
        "জাভাস্ক্রিপ্টে পূর্বে ব্যবহৃত আন্ডারস্কোর (_balance) কেবল একটি কনভেনশন ছিল যা বাইরে থেকে মডিফাই করা যেত। #balance হলো হার্ডওয়্যার/ল্যাঙ্গুয়েজ-লেভেল প্রাইভেট মেম্বার।"
    ),
    (
        5, "Intermediate", "Immutable Array Sorting with toSorted() (React Safe)",
        "মূল অ্যারে অপরিবর্তিত রেখে [10, 5, 30, 20, 15] অ্যারেকে descending অর্ডারে সাজানোর জন্য toSorted() মেথড ব্যবহার করুন।",
        """const numbers = [10, 5, 30, 20, 15];

// ❌ Mutating sort(): মূল numbers অ্যারেকে স্থায়ীভাবে বদলে ফেলে
// numbers.sort((a, b) => b - a);

// ✅ Modern ES2023 Immutable toSorted()
const descending = numbers.toSorted((a, b) => b - a);

console.log('Original Array:', numbers);     // [10, 5, 30, 20, 15] (অক্ষত!)
console.log('Descending Sorted:', descending); // [30, 20, 15, 10, 5]""",
        None,
        "React অ্যাপ্লিকেশনে মূল স্টেট মিউটেট করলে UI রি-রেন্ডারিং সংক্রান্ত গুরুতর বাগ তৈরি হয়। toSorted() কোনো ক্লোনিং ছাড়াই ইমিউটেবল নতুন অ্যারে প্রদান করে।"
    ),
    (
        6, "Intermediate", "Fault-Tolerant Concurrent Requests with Promise.allSettled()",
        "তিনটি কনকারেন্ট এপিআই কলের মধ্যে কিছু প্রমিজ ফেইল করলেও যাতে পুরো প্রসেস ক্র্যাশ না করে প্রতিটি কলের স্টেট পরীক্ষা করুন।",
        """const fetchA = Promise.resolve({ source: 'Payment Gateway', status: 'OK' });
const fetchB = Promise.reject(new Error('Auth Service Timeout (504)'));
const fetchC = Promise.resolve({ source: 'Notification Service', status: 'Delivered' });

async function loadSystemStatus() {
  const results = await Promise.allSettled([fetchA, fetchB, fetchC]);

  results.forEach((res, index) => {
    if (res.status === 'fulfilled') {
      console.log(`Service #${index + 1} [ACTIVE ✅]:`, res.value);
    } else {
      console.warn(`Service #${index + 1} [FAILED ❌]:`, res.reason.message);
    }
  });
}

loadSystemStatus();""",
        None,
        "Promise.all() একটি রিজেক্ট হলেই পুরো পাইপলাইন থামিয়ে দেয়। Promise.allSettled() সব প্রমিজ শেষ হওয়া পর্যন্ত অপেক্ষা করে fulfilled বা rejected স্ট্যাটাস রিপোর্ট করে।"
    ),
    (
        7, "Advanced", "Declarative Data Categorization with Object.groupBy()",
        "ব্যবহারকারীর রোল (admin/user) অনুযায়ী ইউজার তালিকাকে অবজেক্ট গ্রুপিং করার জন্য আধুনিক ES2024 Object.groupBy() মেথড প্রয়োগ করুন।",
        """const users = [
  { name: 'Tanvir', role: 'admin' },
  { name: 'Sakib', role: 'user' },
  { name: 'Rahim', role: 'admin' },
  { name: 'Karim', role: 'user' },
  { name: 'Ayesha', role: 'editor' }
];

// Modern ES2024 Declarative Grouping
const groupedByRole = Object.groupBy(users, (user) => user.role);

console.log(groupedByRole);
/*
আউটপুট:
{
  admin: [ { name: 'Tanvir', role: 'admin' }, { name: 'Rahim', role: 'admin' } ],
  user: [ { name: 'Sakib', role: 'user' }, { name: 'Karim', role: 'user' } ],
  editor: [ { name: 'Ayesha', role: 'editor' } ]
}
*/""",
        None,
        "পূর্বে অ্যারের উপাদান গ্রুপ করতে জটিল Array.reduce() লজিক বা Lodash লাইব্রেরি ব্যবহার করতে হতো। Object.groupBy() এখন জাভাস্ক্রিপ্টের নেটিভ বিল্ট-ইন মেথড।"
    ),
    (
        8, "Advanced", "Fastest Responsive API Race with Promise.any()",
        "একাধিক ব্যাকআপ এপিআইয়ের মধ্যে যেটি প্রথম সফল রেসপন্স দেবে সেটি গ্রহণ করুন এবং সবগুলো ফেইল করলে AggregateError হ্যান্ডেল করুন।",
        """const mirrorCDN1 = new Promise((_, reject) => setTimeout(() => reject('CDN 1 Offline'), 100));
const mirrorCDN2 = new Promise((resolve) => setTimeout(() => resolve('CDN 2 High-Speed Data Payload'), 200));
const mirrorCDN3 = new Promise((resolve) => setTimeout(() => resolve('CDN 3 Data Payload'), 500));

async function fetchFastestAsset() {
  try {
    // যেটি প্রথম সফল হবে সেটিই ফলাফল দেবে (ব্যর্থতাগুলো ইগনোর করবে)
    const fastestResponse = await Promise.any([mirrorCDN1, mirrorCDN2, mirrorCDN3]);
    console.log('⚡ Connected via Fastest Mirror:', fastestResponse);
  } catch (error) {
    if (error instanceof AggregateError) {
      console.error('All mirror servers failed:', error.errors);
    }
  }
}

fetchFastestAsset();""",
        None,
        "Promise.race() প্রথম প্রমিজটি ফেইল করলে নিজেও ফেইল করে। কিন্তু Promise.any() প্রথম *সফল* প্রমিজটি গ্রহণ করে এবং সবগুলো ফেইল করলেই কেবল AggregateError থ্রো করে।"
    )
]

for lab_num, level, title, problem, code_snippet, extra, explanation in practice_solutions:
    html_parts.append(f'''    <div class="practice-item">
      <div class="card-title"><span class="badge-num">Lab #{lab_num}</span> [{level.upper()}] — {inline_format(title)}</div>
      <p class="text-p"><strong>সমস্যা ও লক্ষ্য:</strong> {inline_format(problem)}</p>
''')
    if code_snippet:
        html_parts.append(f'      {render_code_box(code_snippet, lang="javascript", title=f"MODERN IMPLEMENTATION (LAB #{lab_num})")}\n')
    if explanation:
        html_parts.append(f'      <div class="def-box">💡 <strong>প্রোডাকশন অন্তর্দৃষ্টি:</strong> {inline_format(explanation)}</div>\n')
    html_parts.append('    </div>\n')

# Final Mental Map Card
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">36.60</span> 🎯 Final Mental Map — মডার্ন ECMAScript-এর পূর্ণাঙ্গ মানচিত্র</div>
      <p class="text-p">পুরো Chapter 36-এর আধুনিক ফিচার ও ফুলস্ট্যাক অ্যাপ্লিকেশন একসাথে:</p>
''')

final_map_ascii = """                    MODERN ECMASCRIPT ECOSYSTEM
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
     NULL SAFETY             CLASS & OOP             IMMUTABLE DATA
         │                       │                       │
   ?. (Optional Chain)     #private fields         Array.prototype
   ?? (Nullish Coalesce)   static blocks           ├── toSorted()
   ??= ||= &&=             Top-Level await         ├── toReversed()
   Numeric Separators (_)  Error.cause             ├── toSpliced()
         │                       │                 └── with()
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                                 ▼
                     CONCURRENCY & GROUPING
                                 │
         ┌───────────────────────┴───────────────────────┐
         │                                               │
   Promise.allSettled()                            Object.groupBy()
   Promise.any() (Fallback)                        Map.groupBy()
   Promise.withResolvers()                         Temporal (Upcoming)
                                 │
                                 ▼
                     FULL-STACK JAVASCRIPT TOOLKIT
                                 │
            ┌────────────────────┼────────────────────┐
            │                    │                    │
          REACT               NODE.JS                APIs
       State-Safe         Secure Classes         Fault-Tolerant
       Immutability       Encapsulation          Data Pipelines"""

html_parts.append(f'      {render_ascii_box(final_map_ascii, title="MODERN ECMASCRIPT ARCHITECTURE MAP")}\n')

html_parts.append('''      <div class="def-box" style="margin-top: 6px;">
        🏆 <strong>এক লাইনে Chapter 36:</strong> Modern ECMAScript (ES2020+) হলো নাল-সেফটি, ইমিউটেবল ডাটা ম্যানিপুলেশন, ক্লাস এনক্যাপসুলেশন ও কনকারেন্ট প্রমিজ পরিচালনার এমন এক সমন্বিত রূপ যা রিঅ্যাক্ট ফ্রন্টএন্ড ও নোড ব্যাকএন্ড কোডকে করে তোলে আরও সংক্ষিপ্ত, ক্র্যাশ-প্রুফ ও পারফরম্যান্ট।
      </div>

      <div class="section-subhead" style="margin-top: 8px;">🔗 Curriculum Progression: Chapter 35 → 36 → 37</div>
''')

roadmap_conn_ascii = """Chapter 35: Testing JavaScript
       ↓
Unit Testing, Integration Testing, Assertions, Jest/Vitest, Mocking & CI/CD
       ↓
Chapter 36: Modern ECMAScript / ES2020+ Features (THIS CHAPTER)
       ↓
Optional Chaining, Nullish Coalescing, Top-level Await, toSorted, Object.groupBy
       ↓
Chapter 37: JavaScript Design Patterns
       ↓
Singleton, Factory, Observer, Module, Prototype, Proxy & MVC/MVVM Architectural Patterns"""

html_parts.append(f'      {render_ascii_box(roadmap_conn_ascii, title="ROADMAP CONTINUITY PIPELINE")}\n')
html_parts.append('    </div>\n')

# Document Footer
html_parts.append('''  </div>
</body>
</html>''')

# Write complete HTML
output_html_path = r'c:\Users\User\Desktop\Note-Book\Code\Chapter-36-Modern-ECMAScript-ES2020-Features.html'
os.makedirs(os.path.dirname(output_html_path), exist_ok=True)

with open(output_html_path, 'w', encoding='utf-8') as f:
    f.write(''.join(html_parts))

print(f"Successfully generated HTML: {output_html_path} (Total size: {len(''.join(html_parts))} bytes)")
