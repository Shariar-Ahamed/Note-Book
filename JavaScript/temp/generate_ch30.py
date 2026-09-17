import re
import sys
import html
import subprocess
import os

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Read raw markdown
with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-30.md', 'r', encoding='utf-8') as f:
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
        ('DOM_BUILTIN', r'\b(?:console|window|document|Math|Object|Array|Date|JSON|Promise|Error|Map|Set|WeakMap|WeakSet|WeakRef|FinalizationRegistry|setTimeout|clearTimeout|setInterval|clearInterval|queueMicrotask|fetch|performance|addEventListener|removeEventListener|getElementById|structuredClone)\b'),
        ('ASYNC_METHOD', r'\b(?:then|catch|finally|resolve|reject|register|unregister|deref|takeRecords|disconnect|observe)\b'),
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
    
    # Auto-detect leak vs clean if not specified
    if not is_invalid and not is_correct:
        if any(w in code_text for w in ['window.myData =', 'setInterval(() =>', 'anonymous function', 'elements.push', 'cache[id] =', 'globalVar =', 'user = null; // But admin still points']):
            if 'clearInterval' not in code_text and 'removeEventListener' not in code_text and 'WeakMap' not in code_text:
                is_invalid = True
        elif any(w in code_text for w in ['clearInterval(', 'removeEventListener(', 'WeakMap()', 'WeakSet()', 'WeakRef(', 'FinalizationRegistry(', 'structuredClone(']):
            is_correct = True

    box_extra_cls = ''
    tag_color = '#94a3b8'
    tag_label = 'JavaScript'
    
    if is_invalid:
        box_extra_cls = ' code-box-error'
        tag_color = '#f87171'
        tag_label = '❌ Memory Leak / Anti-Pattern'
    elif is_correct:
        box_extra_cls = ' code-box-correct'
        tag_color = '#4ade80'
        tag_label = '✅ Clean / Memory Safe'

    display_title = title if title else "JavaScript Source"

    return f'''<div class="code-box{box_extra_cls}">
  <div class="code-top"><span style="color: {tag_color}; font-weight: 600;">{display_title}</span><span>{tag_label}</span></div>
  <pre><code>{highlighted}</code></pre>
</div>'''

def colorize_ascii(text):
    t = html.escape(text.strip())
    
    # 1. Colorize arrows and paths (Cyan / Blue neon)
    t = re.sub(r'([↓↑→←▼▲►◄])', r'<span style="color: #38bdf8; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(───+|──|─►|◄─)', r'<span style="color: #0ea5e9; font-weight: 600;">\1</span>', t)
    
    # 2. Colorize Box frames (Muted Slate / Light Blue)
    t = re.sub(r'([┌┐└┘├┤┬┴│┼]+)', r'<span style="color: #475569;">\1</span>', t)
    t = re.sub(r'(\-{3,})', r'<span style="color: #334155;">\1</span>', t)
    
    # 3. Colorize Roots & Architecture Pillars (Emerald Green)
    t = re.sub(r'\b(ROOT|Root|Roots|Global|Stack|Heap|Window|Execution-related|Objects/Data)\b', r'<span style="color: #34d399; font-weight: 700;">\1</span>', t)
    
    # 4. Colorize Reachable, Valid, OK & Steps (Bright Mint / Light Emerald)
    t = re.sub(r'\b(Reachable|Reclaimed|Memory Reclaimed|A = reachable|B = reachable|A ✓|B ✓|Cleaned)\b', r'<span style="color: #4ade80; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(✓)', r'<span style="color: #4ade80; font-weight: bold;">✓</span>', t)
    
    # 5. Colorize Unreachable, Traps, Crosses & Leaks (Crimson / Rose Red)
    t = re.sub(r'\b(Unreachable|C = unreachable|C ✗|Memory Leak|Leak|High memory|Retained|Memory usage বাড়ছে|Detached DOM|Detached|Huge Memory)\b', r'<span style="color: #f43f5e; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(✗|X)', r'<span style="color: #f43f5e; font-weight: bold;">\1</span>', t)
    
    # 6. Colorize Steps & Lifecycle (Purple / Violet)
    t = re.sub(r'\b(Step \d+|Allocate|1\. Allocate|2\. Use|3\. No longer reachable|4\. Garbage Collector detects|5\. Memory reclaimed|GC Eligible|Garbage Collector|Mark:|Sweep:)\b', r'<span style="color: #c084fc; font-weight: 700;">\1</span>', t)
    
    # 7. Colorize Variables & Objects (Amber / Gold)
    t = re.sub(r'\b(Object|Object A|Object B|Object C|user|user1|user2|admin|Ripon|Shariar|count|counter|closure|myData|WeakMap|WeakSet|Map|Set|Cache)\b', r'<span style="color: #fde047; font-weight: 600;">\1</span>', t)
    
    # 8. Colorize Numbers / Memory counters (Orange)
    t = re.sub(r'\b(10000|20000|30000|\d+ms)\b', r'<span style="color: #fb923c; font-weight: 700;">\1</span>', t)
    
    return t

def render_ascii_box(text, title=None):
    if not title:
        # Determine title dynamically
        if 'Stack' in text and 'Heap' in text:
            title = "STACK VS HEAP CONCEPTUAL ARCHITECTURE"
        elif 'Allocate' in text or 'Lifecycle' in text or 'Use Memory' in text:
            title = "MEMORY LIFECYCLE & RECLAMATION FLOW"
        elif 'Mark:' in text or 'Sweep:' in text or 'Root' in text:
            title = "MARK-AND-SWEEP GC REACHABILITY GRAPH"
        elif 'user1' in text and 'user2' in text:
            title = "OBJECT REFERENCE POINTER MODEL"
        elif 'DOM Node' in text or 'Detached' in text:
            title = "DETACHED DOM NODE RETENTION GRAPH"
        elif 'WeakMap' in text or 'WeakSet' in text:
            title = "WEAK REFERENCE MEMORY ASSOCIATION"
        elif 'Closure' in text or 'closure' in text:
            title = "CLOSURE LEXICAL SCOPE MEMORY RETENTION"
        else:
            title = "ARCHITECTURE & MEMORY GRAPH DIAGRAM"
            
    colorized = colorize_ascii(text)
    return f'''<div class="ascii-tree-container">
  <div class="ascii-tree-header">🧭 {title}</div>
  <pre class="ascii-tree-content">{colorized}</pre>
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

def render_checklist(checklist_text):
    lines = [l.strip() for l in checklist_text.strip().split('\n') if l.strip()]
    items_html = []
    for line in lines:
        cleaned = re.sub(r'^[□■\-*x]\s*', '', line).strip()
        items_html.append(f'''<div class="check-item">
  <span class="check-box">✔</span>
  <span class="check-text">{inline_format(cleaned)}</span>
</div>''')
    return f'''<div class="checklist-container">
  <div class="checklist-header">🛡️ 12-POINT MEMORY AUDIT &amp; LEAK CHECKLIST</div>
  <div class="checklist-grid">
    {''.join(items_html)}
  </div>
</div>'''

# Part Banners configuration
PART_BANNERS = {
    1: ("Part 01", "Core Concepts, Runtime Architecture & Memory Allocation (30.1 – 30.9)"),
    10: ("Part 02", "Reachability, Active Roots & Object Graphs (30.10 – 30.13)"),
    14: ("Part 03", "Garbage Collection Engine & Mark-and-Sweep Algorithm (30.14 – 30.21)"),
    22: ("Part 04", "Memory Leaks, Retained References & Detached DOM Nodes (30.22 – 30.28)"),
    29: ("Part 05", "Closures & Lexical Scope Memory Lifecycle (30.29 – 30.32)"),
    33: ("Part 06", "Weak References & Memory-Safe Collections (WeakMap / WeakSet) (30.33 – 30.37)"),
    38: ("Part 07", "Memory Pressure, High Usage & Optimization Rules (30.38 – 30.43)"),
    44: ("Part 08", "Chrome DevTools Profiling, Heap Snapshots & Retainers (30.44 – 30.47)"),
    48: ("Part 09", "Advanced WeakRef, FinalizationRegistry & Explicit Cleanup (30.48 – 30.55)"),
    56: ("Part 10", "React Component Memory Architecture & Lifecycle Leaks (30.56 – 30.58)"),
    59: ("Part 11", "Interview Deep Dives, Golden Rules & Memory Leak Checklist (30.59 – 30.64)"),
    65: ("Part 12", "Quick Cheat Sheet, Practice Lab with Detailed Solutions & Final Mental Map"),
}

# Split markdown into sections
raw_sections = re.split(r'\n(?=# 30\.\d+ )', raw_md)
print(f"Total raw section chunks parsed: {len(raw_sections)}")

html_parts = []

# Document Header & CSS Tokens
html_parts.append('''<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter 30 — JavaScript Memory Management &amp; Garbage Collection | JavaScript Master Study Documentation</title>
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
    .warn-box {
      background: #fff1f2;
      border-left: 3px solid #f43f5e;
      padding: 5px 8px;
      border-radius: 0 4px 4px 0;
      font-size: 10px;
      margin: 4px 0;
      color: #9f1239;
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
    .code-box-error {
      border: 1px solid rgba(239, 68, 68, 0.4);
      border-left: 3px solid #ef4444;
    }
    .code-box-correct {
      border: 1px solid rgba(34, 197, 94, 0.4);
      border-left: 3px solid #22c55e;
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
    .invalid-token {
      color: #fca5a5 !important;
      text-decoration: underline wavy #ef4444 1.5px !important;
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

    /* Checklist Grid */
    .checklist-container {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      overflow: hidden;
      margin: 6px 0;
    }
    .checklist-header {
      background: #1e293b;
      color: #38bdf8;
      font-family: var(--font-heading);
      font-size: 10px;
      font-weight: 700;
      padding: 5px 12px;
      letter-spacing: 0.5px;
    }
    .checklist-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
      padding: 8px 12px;
    }
    .check-item {
      display: flex;
      align-items: center;
      gap: 6px;
      background: white;
      padding: 4px 8px;
      border: 1px solid #e2e8f0;
      border-radius: 4px;
      font-size: 9.5px;
    }
    .check-box {
      color: #059669;
      font-weight: bold;
      font-size: 11px;
    }
    .check-text {
      color: #1e293b;
      font-weight: 600;
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
      #sec-30-1 {
        page-break-after: always !important;
        break-after: page !important;
        margin-bottom: 0 !important;
      }
      .study-card, .practice-item, .checklist-container {
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        border: 1px solid #cbd5e1;
      }
      .part-banner {
        page-break-after: avoid !important;
        break-after: avoid !important;
      }
      .code-box, pre, .ascii-tree-container, .table-container, .def-box, .output-box, .warn-box {
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
          <span class="chapter-badge">Chapter 30</span>
        </div>
      </div>
      <div class="banner-sub">JAVASCRIPT MEMORY MANAGEMENT, GARBAGE COLLECTION &amp; RUNTIME LIFECYCLE OPTIMIZATION</div>
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">Total Modules</div>
          <div class="meta-val">64 Modules + Practice Lab</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Curriculum Part</div>
          <div class="meta-val">Part 24 — Memory &amp; GC Architecture</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Core Mechanics</div>
          <div class="meta-val">Stack vs Heap, Mark &amp; Sweep, WeakRef</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Reference Standard</div>
          <div class="meta-val">ECMAScript 2026 / V8 GC Engine Spec</div>
        </div>
      </div>
    </header>

    <!-- Chapter Opening Statement (Page 1 Balance) -->
    <div class="opening-card">
      <div class="opening-title">
        <span>🎯</span> JavaScript Memory Management &amp; Garbage Collection — মেমরি আর্কিটেকচার শেখার মূল উদ্দেশ্য
      </div>
      <p class="text-p">
        JavaScript-এ মেমরি কীভাবে বরাদ্দ হয়, অবজেক্ট রেফারেন্স কীভাবে কাজ করে এবং মেমরি লিক এড়াতে কী কী সতর্কতা প্রয়োজন—তা জানা একজন প্রোডাকশন ইঞ্জিনিয়ারের জন্য অপরিহার্য। এই চ্যাপ্টারে আমরা <strong>Stack vs Heap</strong>, <strong>Mark-and-Sweep Garbage Collection</strong>, <strong>Reachability Tree</strong>, <strong>Closure Memory</strong>, <strong>Detached DOM Nodes</strong>, <strong>WeakMap/WeakSet</strong> এবং <strong>Chrome DevTools Heap Profiling</strong> গভীরভাবে শিখব।
      </p>
      <div class="roadmap-grid">
        <div class="roadmap-item"><span>📌</span> 1. Memory Allocation</div>
        <div class="roadmap-item"><span>📌</span> 2. Stack vs Heap</div>
        <div class="roadmap-item"><span>📌</span> 3. References &amp; Values</div>
        <div class="roadmap-item"><span>📌</span> 4. Reachability &amp; Roots</div>
        <div class="roadmap-item"><span>📌</span> 5. Mark-and-Sweep GC</div>
        <div class="roadmap-item"><span>📌</span> 6. Circular References</div>
        <div class="roadmap-item"><span>📌</span> 7. Memory Leak Traps</div>
        <div class="roadmap-item"><span>📌</span> 8. Detached DOM Nodes</div>
        <div class="roadmap-item"><span>📌</span> 9. WeakMap &amp; WeakRef</div>
        <div class="roadmap-item"><span>📌</span> 10. Heap Profiling</div>
      </div>
    </div>
''')

# Function to get part banner if applicable
def check_part_banner(sec_idx):
    if sec_idx in PART_BANNERS:
        part_tag, part_title = PART_BANNERS[sec_idx]
        return f'<div class="part-banner">{part_tag} — {part_title}</div>'
    return None

# Parse Sections 1 to 63
for idx in range(1, 64):
    sec_text = raw_sections[idx].strip()
    pb = check_part_banner(idx)
    if pb:
        html_parts.append(f'    {pb}\n')
        
    sec_lines = sec_text.split('\n')
    header_line = sec_lines[0]
    m_head = re.search(r'# (?:🔥\s*)?(30\.\d+)\s*(?:—|-)?\s*(.*)', header_line)
    if m_head:
        sec_num = m_head.group(1)
        sec_title = m_head.group(2)
    else:
        sec_num = f'30.{idx}'
        sec_title = header_line.replace('#', '').strip()
        
    card_extra = ''
    if idx == 1:
        card_extra = ' id="sec-30-1"'
        
    html_parts.append(f'''    <div class="study-card"{card_extra}>
      <div class="card-title"><span class="badge-num">{sec_num}</span> {inline_format(sec_title)}</div>
''')
    
    body_text = '\n'.join(sec_lines[1:]).strip()
    
    # Check if section contains checklist (like Section 30.63)
    if idx == 63 and '□' in body_text:
        chk_match = re.search(r'```text([\s\S]*?)```', body_text)
        if chk_match:
            chk_raw = chk_match.group(1)
            # Render text before checklist
            pre_chk = body_text[:chk_match.start()].strip()
            if pre_chk:
                for pl in pre_chk.split('\n'):
                    if pl.strip() and pl.strip() != '---':
                        html_parts.append(f'      <p class="text-p">{inline_format(pl.strip())}</p>\n')
            html_parts.append(f'      {render_checklist(chk_raw)}\n')
            post_chk = body_text[chk_match.end():].strip()
            if post_chk:
                for pl in post_chk.split('\n'):
                    if pl.strip() and pl.strip() != '---':
                        html_parts.append(f'      <p class="text-p">{inline_format(pl.strip())}</p>\n')
            html_parts.append('    </div>\n')
            continue

    # Standard parsing with markdown table extraction and separator filtering
    chunks = re.split(r'(```[\s\S]*?```|###[^\n]+|\|[^\n]+\|\n\|[\s:-|-]+\|\n(?:\|[^\n]+\|\n?)+)', body_text)
    last_text_was_output = False
    
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
                elif clang in ('text', 'ascii', ''):
                    # Check if output
                    if last_text_was_output or code_val.strip() in ('Shariar', '10', '20', 'true', 'false'):
                        html_parts.append(render_output_box(code_val))
                        last_text_was_output = False
                    else:
                        html_parts.append(render_ascii_box(code_val))
                else:
                    html_parts.append(render_code_box(code_val, lang=clang, title=clang.upper()))
        elif ch_str.startswith('###'):
            sub_title = ch_str.replace('###', '').strip()
            if sub_title.lower() == 'output':
                last_text_was_output = True
            else:
                html_parts.append(f'      <div class="section-subhead">🔹 {inline_format(sub_title)}</div>\n')
        else:
            if 'Output:' in ch_str or 'output:' in ch_str.lower():
                last_text_was_output = True
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
                            if p_text and p_text != '---' and not p_text.lower().startswith('output:'):
                                html_parts.append(f'      <p class="text-p">{inline_format(p_text)}</p>\n')
                            p_acc = []
                        html_parts.append('      <ul style="margin: 2px 0 5px 16px; color: #334155; font-size: 10.5px;">\n')
                        in_list = True
                    html_parts.append(f'        <li>{inline_format(ls[2:])}</li>\n')
                else:
                    if in_list:
                        html_parts.append('      </ul>\n')
                        in_list = False
                    if ls.lower().startswith('output:'):
                        last_text_was_output = True
                    else:
                        p_acc.append(ls)
            if in_list:
                html_parts.append('      </ul>\n')
            if p_acc:
                p_text = " ".join(p_acc).strip()
                if p_text and p_text != '---':
                    html_parts.append(f'      <p class="text-p">{inline_format(p_text)}</p>\n')
                
    html_parts.append('    </div>\n')

# Section 64: MUST KNOW
sec64_text = raw_sections[64].strip()
pb64 = check_part_banner(59) # Part 11 already started at 59

# Extract sub-sections in 64
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">30.64</span> 🔥 MUST KNOW — মেমরি ম্যানেজমেন্টের প্রধান স্তম্ভসমূহ</div>
      <p class="text-p">চ্যাপ্টার ৩০ থেকে প্রতিটি সফটওয়্যার ইঞ্জিনিয়ারের যেসব বিষয় মুখস্থ নয়, সরাসরি মস্তিষ্কে গেঁথে থাকা বাধ্যতামূলক:</p>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 4px;">
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #0369a1; font-size: 10px; margin-bottom: 3px;">📌 1. Memory Basics</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li>Memory Allocation (Primitive vs Object)</li>
            <li>Stack (Execution contexts &amp; primitive values)</li>
            <li>Heap (Dynamic collections, objects &amp; arrays)</li>
            <li>References &amp; Memory Addresses</li>
            <li>Reachability &amp; Active Root Graphs</li>
          </ul>
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #059669; font-size: 10px; margin-bottom: 3px;">📌 2. Garbage Collection</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li>Mark-and-Sweep Core Engine Algorithm</li>
            <li>Active Roots Traversal &amp; Mark Bit Setting</li>
            <li>Unreachable vs Nullified References</li>
            <li>Circular References handled cleanly by GC</li>
            <li>GC Runs Asynchronously (Non-deterministic)</li>
          </ul>
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #dc2626; font-size: 10px; margin-bottom: 3px;">📌 3. Memory Leaks Traps</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li>Accidental Global Variables (window.data)</li>
            <li>Uncleared Timers (setInterval/setTimeout)</li>
            <li>Forgotten Event Listeners on unmounted DOM</li>
            <li>Detached DOM Nodes retained in JS collections</li>
            <li>Closures retaining heavy parent lexical scopes</li>
          </ul>
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #7c3aed; font-size: 10px; margin-bottom: 3px;">📌 4. Advanced Diagnostics</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li>WeakMap &amp; WeakSet (Garbage-collectible keys)</li>
            <li>WeakRef &amp; FinalizationRegistry</li>
            <li>Chrome DevTools Heap Snapshots &amp; Retainers</li>
            <li>Allocation Instrumentation on timeline</li>
            <li>Explicit Resource Cleanup (Freeing buffers)</li>
          </ul>
        </div>
      </div>
    </div>
''')

# Part 12: Cheat Sheet, Practice Lab & Final Mental Map
pb12 = check_part_banner(65)
if pb12:
    html_parts.append(f'    {pb12}\n')

# Quick Cheat Sheet
m_table = re.search(r'(\|[\s\S]*\|)', sec64_text)
html_parts.append(f'''    <div class="study-card">
      <div class="card-title"><span class="badge-num">30.Cheat</span> 🧠 Quick Cheat Sheet — JavaScript Memory &amp; GC Terminology</div>
      <p class="text-p">মেমরি ম্যানেজমেন্টের সর্বাধিক ব্যবহৃত টার্মগুলোর তাৎক্ষণিক অর্থ ও ভূমিকা:</p>
      {render_table(m_table.group(1)) if m_table else ""}
    </div>
''')

# Practice Lab with Full Solutions (6 Real-World Challenges)
practice_solutions = [
    {
        "id": "Practice 1",
        "level": "Beginner",
        "title": "Object Eligibility for Garbage Collection",
        "question": "Object কি garbage collection-এর জন্য eligible হতে পারে? কেন?",
        "code": """let user = {
    name: "Ripon"
};

user = null;""",
        "output": "Eligible for Garbage Collection",
        "answer": """১. হ্যাঁ, অবজেক্টটি Garbage Collection-এর জন্য নিশ্চিতভাবে Eligible হবে।
২. কারণ: শুরুতে Global/Stack-এর 'user' ভেরিয়েবলটি Memory Heap-এ থাকা '{ name: "Ripon" }' অবজেক্টকে রেফারেন্স করছিল।
৩. যখন 'user = null' অ্যাসাইন করা হলো, তখন অবজেক্টটির সাথে রুট (Root)-এর একমাত্র রেফারেন্স সংযোগটি বিচ্ছিন্ন হয়ে যায়।
৪. অবজেক্টটি সম্পূর্ণ 'Unreachable' হয়ে পড়ে। Mark-and-Sweep অ্যালগরিদম পরবর্তী GC সাইকেলে রুট থেকে ট্রাভার্স করার সময় এই অবজেক্টে পৌঁছাতে পারবে না, ফলে এর দখলকৃত মেমরি রিক্লেইম (মুক্ত) করে দেবে।"""
    },
    {
        "id": "Practice 2",
        "level": "Beginner",
        "title": "Object Reference Copy vs Value Mutability",
        "question": "নিচের কোডটি রান করলে আউটপুট কী আসবে এবং মেমরিতে কী ঘটবে?",
        "code": """const a = {
    value: 10
};

const b = a;

b.value = 20;

console.log(a.value);""",
        "output": "20",
        "answer": """১. আউটপুট আসবে '20'।
২. মেমরি বিশ্লেষণ: JavaScript-এ অবজেক্ট সরাসরি ভ্যালু হিসেবে কপি হয় না। যখন 'const b = a' লেখা হয়, তখন অবজেক্টের মেমরি অ্যাড্রেস (Reference Pointer) 'b'-তে কপি হয়।
৩. ফলে 'a' এবং 'b' উভয়েই Memory Heap-এর একই ফিজিক্যাল অবজেক্টকে পয়েন্ট করে থাকে।
৪. সুতরাং 'b.value = 20' মিউটেট করলে একই অবজেক্টের অভ্যন্তরীণ প্রোপার্টি পরিবর্তিত হয়, তাই 'a.value'-ও ২০ প্রিন্ট করে।"""
    },
    {
        "id": "Practice 3",
        "level": "Intermediate",
        "title": "Active Multi-Reference Reachability Check",
        "question": "নিচের কোডে user = null করার পরও অবজেক্ট কি reachable থাকবে?",
        "code": """let user = {
    name: "Ripon"
};

let admin = user;

user = null;""",
        "output": "Object remains Reachable (Retained)",
        "answer": """১. হ্যাঁ, অবজেক্টটি এখনো সম্পূর্ণ Reachable থাকবে এবং Garbage Collector এটিকে মুছবে না।
২. কারণ: যদিও 'user = null' করে একটি রেফারেন্স মুছে ফেলা হয়েছে, কিন্তু 'admin' ভেরিয়েবলটি এখনো সেই অবজেক্টের মেমরি অ্যাড্রেস ধরে রেখেছে।
৩. রুট থেকে অবজেক্টে পৌঁছানোর পথ এখনো অক্ষত আছে: (Global Scope → admin → Heap Object)।
৪. অবজেক্ট তখনই Unreachable হবে যখন 'admin'-কেও null বা অন্য ভ্যালুতে রি-অ্যাসাইন করা হবে।"""
    },
    {
        "id": "Practice 4",
        "level": "Intermediate",
        "title": "Complete Unreachability Point Determination",
        "question": "ঠিক কোন লাইনের এক্সিকিউশনের পর অবজেক্টটি GC-এর জন্য eligible হবে?",
        "code": """let user = {
    name: "Ripon"
};

let admin = user;

user = null;
admin = null; // <--- Critical Transition Point""",
        "output": "Eligible right after 'admin = null;'",
        "answer": """১. ঠিক 'admin = null;' স্টেটমেন্টটি এক্সিকিউট হওয়ার পরপরই অবজেক্টটি GC-এর জন্য Eligible হবে।
২. ধাপ ১: 'user = null' করার পর অবজেক্টের রেফারেন্স কাউন্ট ১ ছিল (admin রেফারেন্স করছিল)।
৩. ধাপ ২: যখন 'admin = null' কার্যকর হলো, তখন অবজেক্টটির দিকে কোনো সক্রিয় রুট রেফারেন্স অবশিষ্ট থাকল না।
৪. ফলশ্রুতিতে অবজেক্টটি পুরোপুরি আনরিচেবল গ্রাফ আইল্যান্ডে পরিণত হলো এবং পরবর্তী ইঞ্জিন সুইপ ফেজে মেমরি ফ্রি করার জন্য চূড়ান্তভাবে প্রস্তুত হলো।"""
    },
    {
        "id": "Practice 5",
        "level": "Advanced 🔥",
        "title": "Closure Lexical Environment Retention",
        "question": "createCounter() এর এক্সিকিউশন শেষ হওয়ার পরও 'count' ভেরিয়েবল মেমরিতে কীভাবে বাঁচে?",
        "code": """function createCounter() {
    let count = 0;

    return function () {
        count++;
        return count;
    };
}

const counter = createCounter();
console.log(counter()); // 1
console.log(counter()); // 2""",
        "output": "1\n2",
        "answer": """১. সাধারণ ফাংশনের ক্ষেত্রে এক্সিকিউশন শেষ হওয়ামাত্রই কল স্ট্যাক ফ্রেম ধ্বংস হয়ে যায় এবং লোকাল ভেরিয়েবল মুছে যায়।
২. কিন্তু এখানে 'createCounter' একটি ইনার ফাংশন রিটার্ন করেছে যা তার প্যারেন্ট স্কোপের 'count' ভেরিয়েবলকে ব্যবহার করে (Closure)।
৩. JavaScript ইঞ্জিন দেখে যে রিটার্ন করা ফাংশনটি গ্লোবাল ভেরিয়েবল 'counter'-এ অ্যাসাইন করা হয়েছে (Reachable Root)।
৪. ইঞ্জিন ফাংশনটির Lexical Environment-কে স্ট্যাক থেকে হিপে স্থানান্তরিত করে জিইয়ে রাখে, যতক্ষণ 'counter' ভেরিয়েবলটি মেমরিতে সক্রিয় থাকবে।
৫. মেমরি সতর্কতা: ক্লোজার যদি ভারী ডেটা রেফারেন্স করে রাখে, তবে কাজ শেষে 'counter = null' না করলে মেমরি রিটেইনড থাকে।"""
    },
    {
        "id": "Practice 6",
        "level": "Advanced 🔥",
        "title": "Timer Interval Memory Leak Audit & Production Lifecycle Cleanup",
        "question": "নিচের কোডে সম্ভাব্য Memory Leak কী এবং কীভাবে ক্লিনআপ করতে হবে?",
        "code": """// ❌ Leaky Implementation:
function start() {
    setInterval(() => {
        console.log("Running...");
    }, 1000);
}
start();

// ✅ Production Clean Lifecycle Pattern:
let timerId = null;

function startService() {
    if (timerId !== null) return;
    timerId = setInterval(() => {
        console.log("Service pulse active...");
    }, 1000);
}

function stopService() {
    if (timerId !== null) {
        clearInterval(timerId);
        timerId = null;
        console.log("Timer destroyed & memory released cleanly.");
    }
}""",
        "output": "Service pulse active...\nTimer destroyed & memory released cleanly.",
        "answer": """১. মেমরি সমস্যা: 'setInterval' ব্রাউজার বা Node.js হোস্ট এনভায়রনমেন্টের ইন্টারনাল টাইমার টেবিলে রেজিস্টার হয়ে থাকে। ফাংশন শেষ হলেও টাইমার অবজেক্ট এবং তার কলব্যাকটি মেমরিতে চিরতরে আটকে থাকে।
২. কলব্যাকের ভেতরে কোনো ভ্যারিয়েবল, অবজেক্ট বা DOM রেফারেন্স থাকলে তারা কখনো GC হবে না।
৩. প্রতিকার: টাইমার আইডিটি সংরক্ষণ করতে হবে এবং কম্পোনেন্ট আনমাউন্ট বা কাজ শেষ হলে 'clearInterval(timerId)' ও 'timerId = null' কল করে হোস্ট মেমরি মুক্ত করতে হবে।
৪. React কম্পোনেন্টে এটি useEffect-এর return cleanup ফাংশনে হ্যান্ডল করা বাধ্যতামূলক।"""
    }
]

html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">30.Lab</span> 📝 Hands-On Practice Lab — 6 Memory Lifecycle &amp; GC Trace Problems</div>
      <p class="text-p">মেমরি ম্যানেজমেন্ট ও রিচেবিলিটির খুঁটিনাটি যাচাই করার জন্য নিচে ৬টি প্রোডাকশন ইন্টারভিউ চ্যালেঞ্জের পূর্ণাঙ্গ ব্যাখ্যাসহ সমাধান দেওয়া হলো:</p>
''')

for p in practice_solutions:
    lvl_color = "#059669" if p["level"] == "Beginner" else ("#d97706" if "Intermediate" in p["level"] else "#dc2626")
    html_parts.append(f'''      <div class="practice-item">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 3px;">
          <span style="font-weight: 700; font-size: 11px; color: var(--navy-deep);">{p["id"]}: {p["title"]}</span>
          <span style="background: {lvl_color}; color: white; font-size: 8px; font-weight: 700; padding: 1px 6px; border-radius: 3px; text-transform: uppercase;">{p["level"]}</span>
        </div>
        <p class="text-p" style="margin-bottom: 3px; font-weight: 600; color: #0f172a;">❓ {p["question"]}</p>
        {render_code_box(p["code"], title=f'{p["id"]} Code Challenge')}
        {render_output_box(p["output"])}
        <div class="def-box" style="margin-top: 3px; background: #f8fafc; border-left: 3px solid var(--blue-accent);">
          <div style="font-weight: 700; font-size: 9px; color: var(--blue-dark); margin-bottom: 2px;">🔍 Model Solution &amp; Memory Mechanics:</div>
          <div style="font-size: 8.5px; color: #334155; line-height: 1.4; white-space: pre-wrap;">{p["answer"]}</div>
        </div>
      </div>
''')

html_parts.append('    </div>\n')

# Final Mental Map
final_map_match = re.search(r'# 🎯 Final Mental Map[\s\S]*?```text([\s\S]*?)```', raw_sections[64])
final_map_ascii = final_map_match.group(1).strip() if final_map_match else ""

html_parts.append(f'''    <div class="study-card">
      <div class="card-title"><span class="badge-num">30.Map</span> 🎯 Final Mental Map — JavaScript Memory Architecture</div>
      <p class="text-p">JavaScript রানটাইমে মেমরি রূপান্তর, রিচেবিলিটি চেক এবং গার্বেজ কালেকশন প্রবাহের পূর্ণাঙ্গ মানসিক মানচিত্র:</p>
      {render_ascii_box(final_map_ascii, title="JavaScript Memory & GC Global Coordination Tree")}
      
      <div class="def-box" style="margin-top: 6px; padding: 6px 10px; background: #f8fafc; border-left: 3px solid #38bdf8;">
        <div style="font-weight: 700; font-size: 10px; color: #0369a1; margin-bottom: 3px;">⭐ সবচেয়ে গুরুত্বপূর্ণ ৫টি গোল্ডেন রুল:</div>
        <div style="font-size: 9px; color: #334155; line-height: 1.45;">
          1️⃣ <strong>স্বয়ংক্রিয় মেমরি পরিচালনা:</strong> JavaScript স্বয়ংক্রিয়ভাবে মেমরি বরাদ্দ ও মুক্ত করে, কোনো ম্যানুয়াল free() প্রয়োজন হয় না।<br>
          2️⃣ <strong>রেফারেন্সের মাধ্যমে অবজেক্ট অ্যাক্সেস:</strong> অবজেক্ট ভ্যালু আকারে কপি হয় না, কেবল পয়েন্টার রেফারেন্স শেয়ার হয়।<br>
          3️⃣ <strong>সক্রিয় অবজেক্ট রিচেবল থাকে:</strong> রুট (Root) থেকে পৌঁছানো যায় এমন সব ডেটাকে ইঞ্জিন বাঁচিয়ে রাখে।<br>
          4️⃣ <strong>আনরিচেবল অবজেক্টই GC যোগ্য:</strong> কোনো অবজেক্টের রেফারেন্স চেইন ছিন্ন হলেই কেবল তা গার্বেজ কালেকশন উপযোগী হয়।<br>
          5️⃣ <strong>মেমরি লিকের মূল কারণ:</strong> প্রয়োজনহীন ডেটা যখন ভুলে কোনো সক্রিয় রুট রেফারেন্সের সাথে আবদ্ধ থাকে।
        </div>
      </div>

      <div class="def-box" style="margin-top: 6px; padding: 6px 10px; background: #f0fdf4; border-left: 3px solid #10b981;">
        <div style="font-weight: 700; font-size: 10px; color: #065f46; margin-bottom: 2px;">🔥 এক নজরে মূল কথা (Core Essence):</div>
        <div style="font-size: 9.5px; color: #047857; line-height: 1.45;">
          JavaScript-এর Garbage Collector মেমরি নিজে থেকে পরিষ্কার করে, কিন্তু কোনো অপ্রয়োজনীয় অবজেক্ট যদি এখনও কোনো সক্রিয় রেফারেন্সের মাধ্যমে রিচেবল থাকে, তাহলে Garbage Collector সেটাকে রিক্লেইম করতে পারে না—এটাই মেমরি ম্যানেজমেন্ট বোঝার মূল চাবিকাঠি।
        </div>
      </div>

      <div class="def-box" style="margin-top: 6px; padding: 6px 10px; background: #eff6ff; border-left: 3px solid #2563eb;">
        <div style="font-weight: 700; font-size: 10px; color: #1e40af; margin-bottom: 2px;">🚀 Next Chapter Preview:</div>
        <div style="font-family: var(--font-heading); font-size: 10px; font-weight: 700; color: #0369a1;">
          Chapter 31 — JavaScript Security &amp; Web Security
        </div>
        <div style="font-size: 9px; color: #334155; margin-top: 2px;">পরবর্তী চ্যাপ্টারে আমরা শিখব XSS, CSRF, CORS, CSP, DOM-based attacks, Prototype Pollution, Token &amp; Storage Security এবং স্যানিটাইজেশন প্রোডাকশন প্যাটার্ন।</div>
      </div>
    </div>

  </div>

</body>
</html>
''')

# Write complete HTML file
output_html_path = r'c:\Users\User\Desktop\Note-Book\Code\Chapter-30-Memory-Management-Garbage-Collection.html'
with open(output_html_path, 'w', encoding='utf-8') as f:
    f.write(''.join(html_parts))

print(f"Successfully generated Chapter 30 HTML: {output_html_path}")
print(f"File size: {os.path.getsize(output_html_path)} bytes")
