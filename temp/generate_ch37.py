import re
import sys
import html
import os
import subprocess

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Read raw markdown
with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-37.md', 'r', encoding='utf-8') as f:
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
            ('KEYWORD', r'\b(?:for|while|do|break|continue|if|else|let|const|var|function|return|switch|case|default|of|in|new|typeof|delete|this|super|class|extends|static|instanceof|try|catch|finally|throw|await|async|yield|import|export|from|default|get|set)\b'),
            ('BOOL_NULL', r'\b(?:true|false|null|undefined|NaN)\b'),
            ('DOM_BUILTIN', r'\b(?:console|window|document|process|Object|Array|Promise|String|Number|Math|BigInt|Map|Set|WeakMap|WeakSet|Error|Date|JSON)\b'),
            ('PATTERN_METHOD', r'\b(?:getInstance|pay|create|build|subscribe|publish|unsubscribe|notify|notifyAll|execute|undo|request|handle|findUserById|saveUser|checkout|getUser|getUserData|setStrategy|handleRequest|canEdit|canDelete|canView|log|getLogs)\b'),
            ('OPERATOR', r'(?:===|!==|=>|&&|\|\||\?\?|\?\.|[+\-*/%=<>!&|^~])'),
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
            elif kind == 'PATTERN_METHOD':
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
    
    # 2. Box frames & architectural connectors (Slate)
    t = re.sub(r'([┌┐└┘├┤┬┴│┼]+)', r'<span style="color: #475569;">\1</span>', t)
    t = re.sub(r'(\-{3,})', r'<span style="color: #334155;">\1</span>', t)
    
    # 3. Main Architectural Categories & Headers (Amber / Gold)
    t = re.sub(r'\b(DESIGN PATTERNS|CREATIONAL|STRUCTURAL|BEHAVIORAL|ARCHITECTURE|SOLID|CLEAN CODE|ARCHITECTURAL FLOW)\b', r'<span style="color: #fde047; font-weight: 700;">\1</span>', t)
    
    # 4. Specific Design Patterns (Lavender / Violet)
    t = re.sub(r'\b(Factory|Builder|Singleton|Prototype|Adapter|Decorator|Facade|Proxy|Observer|Pub/Sub|Pub-Sub|Strategy|Command|State|Chain of Responsibility|Chain|Dependency Injection|DI|Repository|Service Layer|MVC|Model|View|Controller|Module Pattern)\b', r'<span style="color: #c084fc; font-weight: 700;">\1</span>', t)
    
    # 5. Engineering Principles & Positive Attributes (Emerald / Mint)
    t = re.sub(r'\b(Organized|Reusable|Maintainable|Scalable|Testable|Clean|Single Responsibility|Open/Closed|Liskov|Interface Segregation|Dependency Inversion|DRY|KISS|YAGNI|Composition|Separation of Concerns|State-safe|Decoupled)\b', r'<span style="color: #34d399; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(✓|✔)', r'<span style="color: #4ade80; font-weight: bold;">\1</span>', t)
    
    # 6. Domain Actors & Layer Components (Sky / Cyan)
    t = re.sub(r'\b(User|Order|Product|Cart|Payment|Database|API|Authentication|Notification|OrderController|OrderService|PaymentStrategy|PaymentGateway|UserRepository|EventBus|Subject|Subscribers)\b', r'<span style="color: #38bdf8; font-weight: 600;">\1</span>', t)
    
    # 7. Anti-patterns & Pitfalls (Rose / Crimson)
    t = re.sub(r'\b(Anti-pattern|Over-engineering|Tightly coupled|Spaghetti|God Object|Overuse|Tight coupling|Copy-paste code|5000\+ lines)\b', r'<span style="color: #f43f5e; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(✗|✘|X)', r'<span style="color: #f43f5e; font-weight: bold;">\1</span>', t)
    
    return t

def render_ascii_box(text, title=None):
    if not title:
        if 'DESIGN PATTERNS' in text or 'CREATIONAL' in text:
            title = "DESIGN PATTERNS TAXONOMY MAP"
        elif 'Controller' in text or 'OrderService' in text:
            title = "TIERED ENTERPRISE ARCHITECTURE FLOW"
        elif 'Organized' in text or 'Reusable' in text:
            title = "SOFTWARE QUALITY GOALS & CODE HEALTH"
        elif 'User' in text and 'Product' in text:
            title = "APPLICATION DOMAIN ENTITIES"
        elif 'Problem' in text and 'Solution' in text:
            title = "PROBLEM-TO-SOLUTION PATTERN MAPPING"
        else:
            title = "SOFTWARE ARCHITECTURE DIAGRAM"
            
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

# Part Banners configuration for Chapter 37
PART_BANNERS = {
    1: ("Part 01", "Design Patterns Fundamentals & Categories (37.1 – 37.8)"),
    9: ("Part 02", "Creational Patterns: Module, Singleton, Factory, Builder & Prototype (37.9 – 37.18)"),
    19: ("Part 03", "Structural Patterns: Adapter, Decorator, Facade & Proxy (37.19 – 37.27)"),
    28: ("Part 04", "Behavioral Patterns: Observer, Pub/Sub, Strategy, Command, State & Chain (37.28 – 37.41)"),
    42: ("Part 05", "Architectural Patterns & Clean Software Engineering (37.42 – 37.55)"),
    56: ("Part 06", "Modern React & Full-Stack Application Patterns (37.56 – 37.66)"),
    67: ("Part 07", "Must Know Architecture Pillars, Quick Cheat Sheet, 9 Practice Labs & Final Mental Map"),
}

# Split markdown into sections
raw_sections = re.split(r'\n(?=# 37\.\d+\s*(?:—|-)?\s*)', raw_md)
print(f"Total raw section chunks parsed: {len(raw_sections)}")

# Separate Section 66 from Must Know, Cheat Sheet, Practice Set, and Final Mental Map
sec66_full = raw_sections[66]
sec66_subparts = re.split(r'\n(?=# (?:🔥\s*MUST|🧠\s*Quick|📝\s*Practice|🎯\s*Final))', sec66_full)

sec66_clean = sec66_subparts[0].strip()
mustknow_clean = sec66_subparts[1].strip() if len(sec66_subparts) > 1 else ""
cheatsheet_clean = sec66_subparts[2].strip() if len(sec66_subparts) > 2 else ""
practice_clean = sec66_subparts[3].strip() if len(sec66_subparts) > 3 else ""
mentalmap_clean = sec66_subparts[4].strip() if len(sec66_subparts) > 4 else ""

html_parts = []

# Document Header & CSS Tokens
html_parts.append('''<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter 37 — JavaScript Design Patterns | JavaScript Master Study Documentation</title>
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
      #sec-37-1 {
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
          <span class="chapter-badge">Chapter 37</span>
        </div>
      </div>
      <div class="banner-sub">SOFTWARE DESIGN PATTERNS, ARCHITECTURAL PRINCIPLES, ENTERPRISE PATTERNS &amp; REACT/NODE.JS PRACTICES</div>
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">Total Modules</div>
          <div class="meta-val">66 Modules + 9 Practice Labs</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Curriculum Part</div>
          <div class="meta-val">Part 31 — Software Architecture &amp; Patterns</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Core Innovations</div>
          <div class="meta-val">Creational, Structural &amp; Behavioral Patterns</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Target Architecture</div>
          <div class="meta-val">Clean Code, SOLID, React &amp; Node.js</div>
        </div>
      </div>
    </header>

    <!-- Chapter Opening Statement (Page 1 Balance) -->
    <div class="opening-card">
      <div class="opening-title">
        <span>✨</span> JavaScript Design Patterns — মডার্ন আর্কিটেকচার, ক্লিন কোড ও স্কেলেবিলিটি
      </div>
      <p class="text-p">
        সফটওয়্যার ডেভেলপমেন্টে রিয়ুজ্যাবল, টেস্টেবল ও মেইনটেইনেবল কোড লেখার জন্য ডিজাইন প্যাটার্ন অপরিহার্য। এটি কোনো কপি-পেস্ট কোড নয়, বরং বারবার ঘটা সফটওয়্যার সমস্যার একটি প্রমাণিত স্ট্রাকচারাল সমাধান। এই চ্যাপ্টারে আমরা <strong>Creational (Factory, Singleton, Builder), Structural (Adapter, Decorator, Facade, Proxy), Behavioral (Observer, Pub/Sub, Strategy, Command, State, Chain), Architectural (MVC, Repository, Service Layer, Dependency Injection)</strong> এবং React ও Node.js-এর বাস্তব প্যাটার্নসমূহ সম্পূর্ণ কোড সহ শিখব।
      </p>
      <div class="roadmap-grid">
        <div class="roadmap-item"><span>📌</span> 1. Creational Patterns</div>
        <div class="roadmap-item"><span>📌</span> 2. Structural Patterns</div>
        <div class="roadmap-item"><span>📌</span> 3. Behavioral Patterns</div>
        <div class="roadmap-item"><span>📌</span> 4. Module &amp; Singleton</div>
        <div class="roadmap-item"><span>📌</span> 5. Factory &amp; Builder</div>
        <div class="roadmap-item"><span>📌</span> 6. Observer &amp; Pub/Sub</div>
        <div class="roadmap-item"><span>📌</span> 7. Strategy &amp; Command</div>
        <div class="roadmap-item"><span>📌</span> 8. Dependency Injection</div>
        <div class="roadmap-item"><span>📌</span> 9. Repository &amp; Service</div>
        <div class="roadmap-item"><span>📌</span> 10. React &amp; Enterprise</div>
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

# Process sections 1 to 65
for idx in range(1, 66):
    sec_text = raw_sections[idx].strip()
    pb = check_part_banner(idx)
    if pb:
        html_parts.append(f'    {pb}\n')
        
    sec_lines = sec_text.split('\n')
    header_line = sec_lines[0]
    m_head = re.search(r'# (?:🔥\s*|⚠️\s*)?(37\.\d+)\s*(?:—|-)?\s*(.*)', header_line)
    if m_head:
        sec_num = m_head.group(1)
        sec_title = m_head.group(2)
    else:
        sec_num = f'37.{idx}'
        sec_title = header_line.replace('#', '').strip()
        
    card_extra = ''
    if idx == 1:
        card_extra = ' id="sec-37-1"'
        
    html_parts.append(f'''    <div class="study-card"{card_extra}>
      <div class="card-title"><span class="badge-num">{sec_num}</span> {inline_format(sec_title)}</div>
''')
    
    body_text = '\n'.join(sec_lines[1:]).strip()
    html_parts.append(process_section_body(body_text))
    html_parts.append('    </div>\n')

# Process Section 66 (Cleaned of subparts)
pb66 = check_part_banner(66)
if pb66:
    html_parts.append(f'    {pb66}\n')
    
sec66_lines = sec66_clean.split('\n')
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">37.66</span> Mini Real-World Example — E-Commerce Checkout Architecture</div>
''')
html_parts.append(process_section_body('\n'.join(sec66_lines[1:]).strip()))
html_parts.append('    </div>\n')

# Part 07 Banner & Section 37.67: MUST KNOW
pb07 = check_part_banner(67)
if pb07:
    html_parts.append(f'    {pb07}\n')

html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">37.67</span> 🔥 MUST KNOW — ডিজাইন প্যাটার্নের ২৫টি মূল ভিত্তি ও নীতি</div>
      <p class="text-p">সফটওয়্যার ইঞ্জিনিয়ারিং ও ফুলস্ট্যাক ডেভেলপমেন্টে সিনিয়র লেভেলে উত্তীর্ণ হতে এই ২৫টি কনসেপ্ট অত্যন্ত জরুরি:</p>
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 5px;">
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #0284c7; font-size: 10px; margin-bottom: 3px;">📌 1. Creational &amp; Structural</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li><strong>Factory:</strong> অবজেক্ট তৈরির লজিক সেন্ট্রালাইজড করা</li>
            <li><strong>Singleton:</strong> পুরো অ্যাপ্লিকেশনে শেয়ার্ড একটিমাত্র ইনস্ট্যান্স</li>
            <li><strong>Builder:</strong> ধাপে ধাপে জটিল অবজেক্ট কনস্ট্রাকশন</li>
            <li><strong>Adapter:</strong> ইনকম্প্যাটিবল ইন্টারফেসকে রূপান্তর</li>
            <li><strong>Decorator:</strong> অবজেক্ট পরিবর্তন ছাড়া ফিচার যুক্ত</li>
            <li><strong>Facade:</strong> জটিল সাবসিস্টেমের সহজ এন্ট্রি পয়েন্ট</li>
            <li><strong>Proxy:</strong> অবজেক্ট অপারেশন ইন্টারসেপ্ট ও ক্যাশিং</li>
            <li><strong>Module:</strong> প্রাইভেট স্কোপ ও পাবলিক API এক্সপোজ</li>
          </ul>
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #059669; font-size: 10px; margin-bottom: 3px;">📌 2. Behavioral Patterns</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li><strong>Observer:</strong> ডিপেন্ডেন্ট অবজেক্টে স্টেট চেঞ্জ ব্রডকাস্ট</li>
            <li><strong>Pub/Sub:</strong> ইভেন্ট বাস দিয়ে সম্পূর্ণ ডিকাপল্ড কমিউনিকেশন</li>
            <li><strong>Strategy:</strong> রানটাইমে অ্যালগরিদম বা পেমেন্ট পরিবর্তন</li>
            <li><strong>Command:</strong> অ্যাকশনকে অবজেক্ট বানিয়ে কিউ বা আনডু</li>
            <li><strong>State:</strong> ইন্টারনাল স্টেট অনুযায়ী অবজেক্টের আচরণ বদল</li>
            <li><strong>Chain of Resp.:</strong> হ্যান্ডলার চেইন দিয়ে রিকোয়েস্ট পাস (Middleware)</li>
            <li><strong>Template Method:</strong> স্কেলিটন ক্লাস দিয়ে সাবক্লাসে স্টেপ নির্ধারণ</li>
            <li><strong>Iterator:</strong> সিকোয়েন্সের ভেতরের ডেটা ট্রাভার্সাল</li>
          </ul>
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #7c3aed; font-size: 10px; margin-bottom: 3px;">📌 3. Architecture &amp; Clean Code</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li><strong>Dependency Injection (DI):</strong> বাইরে থেকে ডিপেন্ডেন্সি পুশ</li>
            <li><strong>Repository:</strong> ডাটাবেস এক্সেস বিজনেস লজিক থেকে পৃথক</li>
            <li><strong>Service Layer:</strong> কোর বিজনেস রুলসের সেন্ট্রাল লেয়ার</li>
            <li><strong>MVC:</strong> Model, View এবং Controller সেপারেশন</li>
            <li><strong>Separation of Concerns:</strong> প্রতিটি লেয়ারের নির্দিষ্ট কাজ</li>
            <li><strong>DRY, KISS, YAGNI:</strong> সিম্পল ও আননেসেসারি কোড মুক্ত রাখা</li>
            <li><strong>Composition over Inheritance:</strong> নমনীয় অবজেক্ট কম্পোজিশন</li>
            <li><strong>Pragmatism:</strong> প্রয়োজনের অতিরিক্ত প্যাটার্ন ব্যবহার পরিহার</li>
          </ul>
        </div>
      </div>
    </div>
''')

# Quick Cheat Sheet Card
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">37.68</span> 🧠 Quick Cheat Sheet — ডিজাইন প্যাটার্ন নির্বাচন নির্দেশিকা</div>
''')
cheat_table = '''| Pattern Name | Category | Primary Intent | Production Real-World Example |
| :--- | :--- | :--- | :--- |
| **Factory Pattern** | Creational | অবজেক্ট তৈরির মেকানিজম এনক্যাপসুলেট করা | `document.createElement()`, Auth User Factory |
| **Singleton Pattern** | Creational | একটিমাত্র ইনস্ট্যান্স নিশ্চিত ও শেয়ার করা | Database Connection Pool, Global State Manager |
| **Builder Pattern** | Creational | ধাপে ধাপে জটিল কনফিগারেশন তৈরি | Knex/Prisma Query Builder, Form Builder |
| **Adapter Pattern** | Structural | ভিন্ন ইন্টারফেসকে প্রত্যাশিত ফরম্যাটে মেলানো | Legacy Payment API to Modern Interface |
| **Decorator Pattern** | Structural | অবজেক্ট মডিফাই না করে ডায়নামিক আচরণ বৃদ্ধি | Express Middleware, HOC (Higher-Order Components) |
| **Facade Pattern** | Structural | জটিল সাবসিস্টেমের সামনে একটি সহজ API দেওয়া | Axios facade over `fetch`/`XMLHttpRequest` |
| **Proxy Pattern** | Structural | অবজেক্টের অ্যাক্সেস নিয়ন্ত্রণ বা ক্যাশিং | Vue 3 Reactive System, Validation Proxy |
| **Observer Pattern** | Behavioral | ১-টু-মেনি অবজেক্ট নোটিফিকেশন সিস্টেম | DOM `addEventListener`, MobX Observables |
| **Pub/Sub Pattern** | Behavioral | মধ্যবর্তী চ্যানেল দ্বারা সম্পূর্ণ ডিকাপল্ড ইভেন্ট | Node.js EventEmitter, Redux Actions, Redis Pub/Sub |
| **Strategy Pattern** | Behavioral | রানটাইমে অ্যালগরিদম অদলবদল করা | Multi-gateway Payment (Card/bKash/Bank) |
| **Command Pattern** | Behavioral | রিকোয়েস্টকে অবজেক্টে রূপান্তর (Undo/Redo) | Rich Text Editor actions, Task Queues |
| **State Pattern** | Behavioral | অবজেক্টের অভ্যন্তরীণ স্টেট অনুযায়ী আচরণ বদলানো | Order Status Machine (Pending -> Paid -> Shipped) |
| **Chain of Responsibility** | Behavioral | হ্যান্ডলার চেইনে রিকোয়েস্ট পাস করা | Express/Koa middleware pipeline |
| **Dependency Injection** | Architectural | ক্লাসের বাইরে থেকে ডিপেন্ডেন্সি পাস করা | NestJS DI Container, Unit Testing Mocking |
| **Repository Pattern** | Architectural | ডাটা অ্যাক্সেস লজিক বিজনেস লজিক থেকে পৃথক | ORM Repositories (Prisma, TypeORM) |
| **Service Layer** | Architectural | বিজনেস লজিক এক জায়গায় সেন্ট্রালাইজ করা | Enterprise Node.js / NestJS Backend |'''

html_parts.append(f'      {render_table(cheat_table)}\n')
html_parts.append('    </div>\n')

# 9 Hands-on Practice Labs with Complete Solutions
html_parts.append('''    <div class="part-banner">Part 07.1 — 9 Hands-On Practice Labs with Complete Production Solutions</div>
''')

practice_solutions = [
    (
        1, "Beginner", "Factory Pattern — Dynamic User Creation with Role Permissions",
        "একটি createUser(\"admin\" | \"user\" | \"guest\") Factory তৈরি করুন যা ইউজারের রোল অনুযায়ী নির্দিষ্ট পারমিশন (canEdit, canDelete, canView) যুক্ত অবজেক্ট রিটার্ন করবে।",
        """function createUser(role, name) {
  const baseUser = { name, role, createdAt: new Date().toISOString() };
  
  switch (role) {
    case 'admin':
      return {
        ...baseUser,
        permissions: { canView: true, canEdit: true, canDelete: true },
        describe() { return `${this.name} [ADMIN] - Full Access`; }
      };
    case 'user':
      return {
        ...baseUser,
        permissions: { canView: true, canEdit: true, canDelete: false },
        describe() { return `${this.name} [USER] - Edit Access`; }
      };
    case 'guest':
    default:
      return {
        ...baseUser,
        permissions: { canView: true, canEdit: false, canDelete: false },
        describe() { return `${this.name} [GUEST] - Read-Only Access`; }
      };
  }
}

// Verification
const admin = createUser('admin', 'Tanvir');
const guest = createUser('guest', 'Rahim');
console.log(admin.describe()); // Tanvir [ADMIN] - Full Access
console.log('Guest Delete Allowed:', guest.permissions.canDelete); // false""",
        None,
        "Factory Pattern অবজেক্ট তৈরির কমপ্লেক্স লজিক ও রুলস একটি সাধারণ ফাংশনের ভেতরে এনক্যাপসুলেট করে দেয়, ফলে ক্লায়েন্ট কোডে বারবার `if/else` চেক করার দরকার হয় না।"
    ),
    (
        2, "Beginner", "Singleton Pattern — Centralized Application Logger",
        "একটি Logger ক্লাস তৈরি করুন যেখানে যতবারই `new Logger()` করা হোক না কেন, সবসময় একই শেয়ার্ড ইনস্ট্যান্স রিটার্ন হবে (logger1 === logger2 হবে true)।",
        """class Logger {
  constructor() {
    if (Logger.instance) {
      return Logger.instance;
    }
    this.logs = [];
    Logger.instance = this;
  }

  log(message) {
    const timestamp = new Date().toLocaleTimeString();
    const entry = `[${timestamp}] ${message}`;
    this.logs.push(entry);
    console.log(entry);
  }

  getLogCount() {
    return this.logs.length;
  }
}

// Verification
const logger1 = new Logger();
const logger2 = new Logger();

logger1.log('Application started successfully');
logger2.log('Database connected');

console.log('Is Identical Instance?', logger1 === logger2); // true
console.log('Total Logs Recorded:', logger1.getLogCount());  // 2""",
        None,
        "Singleton Pattern নিশ্চিত করে যে কোনো রিসোর্স-ইনটেনসিভ বা স্টেটফুল ক্লাসের পুরো অ্যাপ্লিকেশনে শুধুমাত্র একটিমাত্র ইনস্ট্যান্স বিদ্যমান থাকবে।"
    ),
    (
        3, "Beginner", "Adapter Pattern — Bridging Legacy API to Modern Interface",
        "একটি পুরোনো সিস্টেমের API মেথড `oldAPI.getUserData()` রিটার্ন করে `{ first_name, last_name, user_email }`। এটিকে ক্লায়েন্টের প্রত্যাশিত আধুনিক ইন্টারফেস `userService.getUser()` অর্থাৎ `{ fullName, email }` ফরম্যাটে রূপান্তর করতে একটি Adapter লিখুন।",
        """// Legacy Service (Cannot modify directly)
class LegacyUserAPI {
  getUserData() {
    return {
      first_name: 'Shariar',
      last_name: 'Ahamed',
      user_email: 'shariar@example.com'
    };
  }
}

// Adapter implementing Modern Target Interface
class UserAdapter {
  constructor(legacyApi) {
    this.legacyApi = legacyApi;
  }

  getUser() {
    const data = this.legacyApi.getUserData();
    return {
      fullName: `${data.first_name} ${data.last_name}`,
      email: data.user_email
    };
  }
}

// Client Usage
const legacyAPI = new LegacyUserAPI();
const userService = new UserAdapter(legacyAPI);

const user = userService.getUser();
console.log('Modern Format:', user);
// Output: Modern Format: { fullName: 'Shariar Ahamed', email: 'shariar@example.com' }""",
        None,
        "Adapter Pattern বিদ্যমান কোনো ক্লাসের কোড পরিবর্তন না করেই দুটি অসঙ্গতিপূর্ণ ইন্টারফেসের মধ্যে একটি সুসংগত সেতু তৈরি করে দেয়।"
    ),
    (
        4, "Intermediate", "Strategy Pattern — Interchangeable Multi-Gateway Payment System",
        "একটি ই-কমার্স পেমেন্ট সিস্টেম তৈরি করুন যাতে Card, Bank Transfer এবং Mobile Banking (bKash/Nagad) স্ট্র্যাটেজি আলাদা অবজেক্ট হিসেবে থাকবে এবং পেমেন্ট সার্ভিস রানটাইমে কৌশল অদলবদল করতে পারবে।",
        """// 1. Concrete Strategies
const CardPaymentStrategy = {
  pay(amount) {
    return `Paid ৳${amount} via Credit/Debit Card (Gateway Fee: 1.5%)`;
  }
};

const BankTransferStrategy = {
  pay(amount) {
    return `Paid ৳${amount} via Direct Bank Wire (Routing: 092834)`;
  }
};

const MobileBankingStrategy = {
  pay(amount) {
    return `Paid ৳${amount} via bKash/Nagad Wallet (Instant SMS TrxID)`;
  }
};

// 2. Context Service
class CheckoutService {
  constructor(strategy) {
    this.strategy = strategy;
  }

  setStrategy(newStrategy) {
    this.strategy = newStrategy;
  }

  processPayment(amount) {
    return this.strategy.pay(amount);
  }
}

// Usage
const checkout = new CheckoutService(CardPaymentStrategy);
console.log(checkout.processPayment(5000));

// Switch strategy at runtime without breaking CheckoutService
checkout.setStrategy(MobileBankingStrategy);
console.log(checkout.processPayment(1200));""",
        None,
        "Strategy Pattern অ্যালগরিদম বা বিজনেস মেকানিজমকে আলাদা ক্লাসে বিভক্ত করে, যার ফলে মূল কনটেক্সট ক্লাস পরিবর্তন না করেই নতুন নতুন পেমেন্ট মেথড যুক্ত করা যায় (Open/Closed Principle)।"
    ),
    (
        5, "Intermediate", "Observer Pattern — Real-Time Notification Broadcast",
        "এমন একটি Subject তৈরি করুন যা মেসেজ আসলে তার সকল রেজিস্টার্ড Observer (User 1, User 2, User 3)-কে স্বয়ংক্রিয়ভাবে নোটিফাই করবে।",
        """class NotificationSubject {
  constructor() {
    this.observers = [];
  }

  subscribe(observer) {
    this.observers.push(observer);
  }

  unsubscribe(observer) {
    this.observers = this.observers.filter(obs => obs !== observer);
  }

  notify(message) {
    this.observers.forEach(observer => observer.update(message));
  }
}

class UserObserver {
  constructor(username) {
    this.username = username;
  }

  update(message) {
    console.log(`[Notification to ${this.username}]: ${message}`);
  }
}

// Execution
const channel = new NotificationSubject();
const user1 = new UserObserver('Abrar');
const user2 = new UserObserver('Fatima');

channel.subscribe(user1);
channel.subscribe(user2);

channel.notify('🎉 JavaScript Master Chapter 37 is now available!');
// Both Abrar and Fatima receive notifications simultaneously""",
        None,
        "Observer Pattern-এ সাবজেক্টের স্টেটে কোনো পরিবর্তন ঘটলে সকল সাবস্ক্রাইবার অবজেক্ট তা তৎক্ষণাৎ জানতে পারে, যা রিয়েল-টাইম ডাটা সিঙ্ক্রোনাইজেশনে অপরিহার্য।"
    ),
    (
        6, "Intermediate", "Pub/Sub Pattern — Fully Decoupled Global Event Bus",
        "একটি গ্লোবাল EventBus তৈরি করুন যাতে subscribe(event, callback) এবং publish(event, data) মেথড থাকবে, যেখানে পাবলিশার এবং সাবস্ক্রাইবার একে অপরকে সরাসরি চেনে না।",
        """class EventBus {
  constructor() {
    this.events = {};
  }

  subscribe(event, callback) {
    if (!this.events[event]) {
      this.events[event] = [];
    }
    this.events[event].push(callback);
    
    // Return unsubscribe function
    return () => {
      this.events[event] = this.events[event].filter(cb => cb !== callback);
    };
  }

  publish(event, data) {
    if (this.events[event]) {
      this.events[event].forEach(callback => callback(data));
    }
  }
}

// Global Bus Usage
const bus = new EventBus();

const unsubAuth = bus.subscribe('user:login', user => {
  console.log(`Auth System: Welcome back ${user.name}!`);
});

bus.subscribe('user:login', user => {
  console.log(`Analytics System: Logged in event for ID ${user.id}`);
});

bus.publish('user:login', { id: 101, name: 'Tanvir' });
unsubAuth(); // Cleanly detach auth listener""",
        None,
        "Pub/Sub-এ একটি সেন্ট্রাল ব্রোকার (Event Bus) থাকে। ফলে সেন্ডার ও রিসিভার কেউ কাউকে চেনে না; তারা কেবল ইভেন্টের নামের ভিত্তিতে স্বাধীনভাবে যোগাযোগ করে।"
    ),
    (
        7, "Advanced", "Dependency Injection — Decoupling Service from Concrete Database",
        "এমন একটি `UserService` তৈরি করুন যা কনস্ট্রাক্টরের মাধ্যমে ডাটাবেস ইন্সট্যান্স ইনজেক্ট করে নেয়। এর মাধ্যমে প্রোডাকশন DB এবং টেস্ট মক DB উভয়েই যাতে একই সার্ভিস ব্যবহার করতে পারে তা দেখান।",
        """// Database Implementations
class MongoDatabase {
  find(id) {
    return { id, name: 'Prod User', source: 'MongoDB Atlas' };
  }
}

class MockTestDatabase {
  find(id) {
    return { id, name: 'Test Fixture User', source: 'In-Memory Mock' };
  }
}

// Service with Injected Dependency
class UserService {
  constructor(database) {
    this.db = database; // Injected externally
  }

  getUserProfile(id) {
    const record = this.db.find(id);
    return `User: ${record.name} (Retrieved via ${record.source})`;
  }
}

// In Production
const prodService = new UserService(new MongoDatabase());
console.log(prodService.getUserProfile(1));

// In Unit Testing
const testService = new UserService(new MockTestDatabase());
console.log(testService.getUserProfile(1));""",
        None,
        "Dependency Injection (DI) ক্লাসের ভেতরে সরাসরি `new Class()` কল বন্ধ করে বাইরে থেকে ইনস্ট্যান্স সাপ্লাই করে। এটি কোডকে 100% টেস্টেবল ও মডুলার বানায়।"
    ),
    (
        8, "Advanced", "Repository Pattern — Clean Architecture Data Access Layer",
        "Controller -> Service -> Repository -> Database এই লেয়ারড আর্কিটেকচার মেনে একটি সম্পূর্ণ ইউজার রেজিস্ট্রেশন ও ফেচিং সিস্টেম লিখুন।",
        """// 1. Repository Layer (Only talks to DB)
class UserRepository {
  constructor() {
    this.storage = new Map();
  }

  create(user) {
    this.storage.set(user.id, user);
    return user;
  }

  findById(id) {
    return this.storage.get(id) || null;
  }
}

// 2. Service Layer (Pure Business Logic & Validations)
class UserService {
  constructor(userRepo) {
    this.userRepo = userRepo;
  }

  register(id, name, email) {
    if (!email.includes('@')) throw new Error('Invalid email address');
    return this.userRepo.create({ id, name, email });
  }

  getDetails(id) {
    const user = this.userRepo.findById(id);
    if (!user) throw new Error('User not found');
    return user;
  }
}

// 3. Controller Layer (HTTP / Client Interface)
class UserController {
  constructor(userService) {
    this.userService = userService;
  }

  handleRegister(id, name, email) {
    try {
      const created = this.userService.register(id, name, email);
      return { status: 201, data: created };
    } catch (err) {
      return { status: 400, error: err.message };
    }
  }
}

// Wire-up
const repo = new UserRepository();
const service = new UserService(repo);
const controller = new UserController(service);

console.log(controller.handleRegister(1, 'Kabir', 'kabir@code.bd'));""",
        None,
        "Repository Pattern বিজনেস লজিককে ডাটা স্টোরেজ মেকানিজম থেকে সম্পূর্ণ আলাদা রাখে। কাল যদি SQL থেকে NoSQL-এ শিফট করা হয়, তবে শুধুমাত্র Repository ক্লাস পরিবর্তন করলেই চলে।"
    ),
    (
        9, "Advanced", "Full Enterprise Mini-Project — E-Commerce Checkout System",
        "Factory, Strategy, Service, Repository এবং Observer প্যাটার্নগুলোর সমন্বয়ে একটি সম্পূর্ণ এন্ড-টু-এন্ড E-Commerce Checkout System তৈরি করুন।",
        """// 1. Strategy: Payment Methods
const BkashStrategy = { pay: amount => `Bkash: ৳${amount} confirmed` };
const CardStrategy = { pay: amount => `Visa/Mastercard: ৳${amount} settled` };

// 2. Observer: Order Notification Event Bus
class OrderNotifier {
  constructor() { this.listeners = []; }
  onOrderSuccess(fn) { this.listeners.push(fn); }
  broadcast(order) { this.listeners.forEach(fn => fn(order)); }
}

// 3. Repository: Order Storage
class OrderRepository {
  constructor() { this.orders = []; }
  save(order) { this.orders.push(order); return order; }
}

// 4. Service: Business Logic & Orchestration
class OrderService {
  constructor(orderRepo, notifier) {
    this.orderRepo = orderRepo;
    this.notifier = notifier;
  }

  checkout(orderId, items, amount, paymentStrategy) {
    // 1. Process payment via strategy
    const paymentReceipt = paymentStrategy.pay(amount);
    
    // 2. Persist order via repository
    const order = this.orderRepo.save({
      id: orderId,
      items,
      amount,
      paymentReceipt,
      status: 'PAID',
      date: new Date().toISOString()
    });

    // 3. Notify all listeners via observer
    this.notifier.broadcast(order);
    return order;
  }
}

// --- Application Assembly & Execution ---
const notifier = new OrderNotifier();
notifier.onOrderSuccess(order => console.log(`[SMS Gateway]: Order #${order.id} paid ৳${order.amount}`));
notifier.onOrderSuccess(order => console.log(`[Warehouse]: Pack items for Order #${order.id}`));

const repo = new OrderRepository();
const orderService = new OrderService(repo, notifier);

const completedOrder = orderService.checkout(
  'ORD-9821', 
  ['JavaScript Master Book', 'Coffee Mug'], 
  1450, 
  BkashStrategy
);

console.log('Final Order Result:', completedOrder.status);""",
        None,
        "বাস্তব সফটওয়্যারে কোনো একক প্যাটার্ন একা চলে না। বিভিন্ন প্যাটার্নের সমন্বয়ে একটি আর্কিটেকচার তৈরি হয় যা অত্যন্ত স্কেলেবল, পরিবর্তনশীল এবং এন্টারপ্রাইজ-রেডি।"
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
        html_parts.append(f'      <div class="def-box">💡 <strong>আর্কিটেকচারাল ব্যাখ্যা:</strong> {inline_format(lab_expl)}</div>\n')
    html_parts.append('    </div>\n')

# Section 37.70: Final Mental Map
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">37.70</span> 🎯 Final Mental Map — ডিজাইন প্যাটার্নের পূর্ণাঙ্গ মানচিত্র</div>
      <p class="text-p">পুরো Chapter 37-এর ডিজাইন প্যাটার্ন ও সফটওয়্যার আর্কিটেকচার একনজরে:</p>
''')

final_tree = """                 DESIGN PATTERNS
                       │
       ┌───────────────┼────────────────┐
       │               │                │
  CREATIONAL       STRUCTURAL       BEHAVIORAL
       │               │                │
    Factory           Adapter          Observer
    Builder           Decorator        Pub/Sub
    Singleton         Facade            Strategy
    Prototype         Proxy             Command
                                       State
                                       Chain
                       │
                       ▼
                ARCHITECTURE
                       │
              ┌────────┼────────┐
              │        │        │
          Controller Service Repository
              │        │        │
              └────────┼────────┘
                       │
                 Dependency
                  Injection
                       │
                       ▼
                  Database/API"""

html_parts.append(f'      {render_ascii_box(final_tree, title="DESIGN PATTERNS TAXONOMY & ARCHITECTURE MAP")}\n')
html_parts.append('''      <div class="def-box" style="margin-top: 6px; border-left: 3px solid #d97706; background: #fffbeb;">
        🏆 <strong>এক লাইনে Chapter 37:</strong> Design Pattern কোনো মুখস্থ কোড নয়—এটি একটি প্রমাণিত আর্কিটেকচারাল সমাধান যা কোডকে সহজে পরিবর্তনযোগ্য, বাগ-মুক্ত এবং প্রোডাকশন স্কেলে বজায় রাখতে সাহায্য করে।
      </div>
    </div>
''')

# Curriculum Progression Card (Chapter 36 -> 37 -> 38)
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">37.71</span> 🔗 Curriculum Progression: Chapter 36 → 37 → 38</div>
''')

curriculum_tree = """Chapter 36: Modern ECMAScript / ES2020+ Features
       ↓
Optional Chaining, Nullish Coalescing, Top-level Await, toSorted, Object.groupBy
       ↓
Chapter 37: JavaScript Design Patterns (THIS CHAPTER)
       ↓
Creational, Structural, Behavioral, MVC, Dependency Injection & Repository
       ↓
Chapter 38: Advanced JavaScript for React
       ↓
Reactivity Engine, Custom Hooks Architecture, State Machines & Virtual DOM Deep Dive"""

html_parts.append(f'      {render_ascii_box(curriculum_tree, title="ROADMAP CONTINUITY PIPELINE")}\n')
html_parts.append('    </div>\n')

# Document Closure
html_parts.append('''
  </div>
</body>
</html>''')

# Write complete HTML file
output_html_path = r'c:\Users\User\Desktop\Note-Book\Code\Chapter-37-JavaScript-Design-Patterns.html'
with open(output_html_path, 'w', encoding='utf-8') as f:
    f.write(''.join(html_parts))

print(f"HTML successfully generated at: {output_html_path}")
print(f"File size: {os.path.getsize(output_html_path)} bytes")
