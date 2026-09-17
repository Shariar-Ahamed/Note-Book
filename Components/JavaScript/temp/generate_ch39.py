import re
import sys
import html
import os
import subprocess

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Read raw markdown
with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-39.md', 'r', encoding='utf-8') as f:
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
            ('DOM_BUILTIN', r'\b(?:console|process|Buffer|Object|Array|Promise|String|Number|Math|BigInt|Map|Set|Error|Date|JSON|EventEmitter)\b'),
            ('NODE_METHOD', r'\b(?:readFile|writeFile|appendFile|unlink|mkdir|rmdir|existsSync|readFileSync|writeFileSync|createReadStream|createWriteStream|pipe|join|resolve|basename|extname|dirname|createServer|listen|emit|on|once|removeListener|all|allSettled|status|json|send|use|get|post|patch|delete|exit|uptime|platform|arch|memoryUsage|nextTick)\b'),
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
            elif kind == 'NODE_METHOD':
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
    
    # 3. Main Node.js & Architectural Headers (Amber / Gold)
    t = re.sub(r'\b(Node\.js|Node|V8|libuv|Event Loop|Runtime|Server|Backend|Express|Express\.js|REST API|JSON API|API|Cluster|Worker Threads|Full Stack JS|Full Stack)\b', r'<span style="color: #fde047; font-weight: 700;">\1</span>', t)
    
    # 4. Built-in Modules & Classes (Lavender / Violet)
    t = re.sub(r'\b(process|fs|path|os|url|events|EventEmitter|Buffer|Stream|Readable|Writable|Transform|Duplex|pipe|require|CommonJS|ES Modules|Routes|Middleware|Controllers|Service|Database|JSON|React)\b', r'<span style="color: #c084fc; font-weight: 700;">\1</span>', t)
    
    # 5. Engineering Principles & Positive Attributes (Emerald / Mint)
    t = re.sub(r'\b(Async I/O|Non-blocking|Promise|async/await|Connection Pool|Graceful Shutdown|Clean|Safe|State-safe|Valid|Active|Success)\b', r'<span style="color: #34d399; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(✓|✔)', r'<span style="color: #4ade80; font-weight: bold;">\1</span>', t)
    
    # 6. Domain Actors & Variables (Sky / Cyan)
    t = re.sub(r'\b(User|Users|Todo|Todos|Cart|Item|Product|Admin|Ripon|Rahim|Karim|HTTP|Network|Computer)\b', r'<span style="color: #38bdf8; font-weight: 600;">\1</span>', t)
    
    # 7. Hazards, Pitfalls & Anti-patterns (Rose / Crimson)
    t = re.sub(r'\b(Blocking|Callback Hell|Crash|TypeError|UncaughtException|UnhandledRejection|Memory Leak|Plain Text|Security Vulnerability)\b', r'<span style="color: #f43f5e; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(✗|✘|X)', r'<span style="color: #f43f5e; font-weight: bold;">\1</span>', t)
    
    return t

def render_ascii_box(text, title=None):
    if not title:
        if 'Node.js' in text and 'libuv' in text:
            title = "NODE.JS INTERNAL ARCHITECTURE & EVENT LOOP"
        elif 'Event Loop' in text or 'Phases' in text:
            title = "NODE.JS EVENT LOOP PHASES"
        elif 'Full Stack' in text or 'React' in text:
            title = "FULL-STACK JAVASCRIPT SYSTEM TOPOLOGY"
        elif 'Browser' in text and 'Computer' in text:
            title = "CLIENT VS SERVER EXECUTION MODEL"
        elif 'Stream' in text or 'pipe' in text:
            title = "STREAM DATA FLOW PIPELINE"
        elif 'Routes' in text or 'Express' in text:
            title = "EXPRESS BACKEND LAYERED ARCHITECTURE"
        else:
            title = "NODE.JS RUNTIME ARCHITECTURE DIAGRAM"
            
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

# Part Banners configuration for Chapter 39
PART_BANNERS = {
    1: ("Part 01", "Node.js Foundations, V8 Engine & Event Loop Architecture (39.1 – 39.7)"),
    8: ("Part 02", "Process Object, CLI Arguments & Environment Variables (39.8 – 39.17)"),
    18: ("Part 03", "Module Systems: CommonJS vs ES Modules & Core Modules (39.18 – 39.23)"),
    24: ("Part 04", "Built-in Modules: File System (fs), Path, OS & URL (39.24 – 39.35)"),
    36: ("Part 05", "Events, Buffers & Streaming Architecture (Streams & Pipe) (39.36 – 39.45)"),
    46: ("Part 06", "Non-blocking Async I/O & Robust Error Handling (39.46 – 39.51)"),
    52: ("Part 07", "HTTP Server, REST APIs & Express Middleware Mechanics (39.52 – 39.59)"),
    60: ("Part 08", "Database Integration, Security, Performance & Login Architecture (39.60 – 39.71)"),
    72: ("Part 09", "Promise Concurrency (all/allSettled) & Node.js JS Foundations (39.72 – 39.75)"),
    76: ("Part 10", "Must Know Node Pillars, Quick Cheat Sheet, 10 Practice Labs & Final Mental Map"),
}

# Split markdown into sections
raw_sections = re.split(r'\n(?=# (?:[^\n]*?)?39\.\d+\s*(?:—|-)?\s*)', raw_md)
print(f"Total raw section chunks parsed: {len(raw_sections)}")

# Separate Section 76 (which contains Must Know, Cheat Sheet, Practice Set, and Final Mental Map)
sec76_full = raw_sections[76]
sec76_subparts = re.split(r'\n(?=# (?:🧠\s*Quick|📝\s*Practice|🎯\s*Chapter))', sec76_full)

mustknow_clean = sec76_subparts[0].strip()
cheatsheet_clean = sec76_subparts[1].strip() if len(sec76_subparts) > 1 else ""
practice_clean = sec76_subparts[2].strip() if len(sec76_subparts) > 2 else ""
mentalmap_clean = sec76_subparts[3].strip() if len(sec76_subparts) > 3 else ""

html_parts = []

# Document Header & CSS Tokens
html_parts.append('''<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter 39 — Advanced JavaScript for Node.js | JavaScript Master Study Documentation</title>
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

    /* Master Top Banner (Chapter 39 in Top Right) */
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
      #sec-39-1 {
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

    <!-- Header Master Banner (Chapter 39 Badge in TOP RIGHT as requested!) -->
    <header class="master-banner">
      <div class="banner-top">
        <div class="banner-left">
          <div class="banner-icon">JS</div>
          <span class="banner-title">JavaScript Master Study Documentation</span>
        </div>
        <span class="chapter-badge">Chapter 39</span>
      </div>
      <div class="banner-sub">ADVANCED JAVASCRIPT FOR NODE.JS: ARCHITECTURE, EVENT LOOP, STREAMS, APIS &amp; PRODUCTION BACKEND</div>
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">Total Modules</div>
          <div class="meta-val">76 Modules + 10 Practice Labs</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Curriculum Part</div>
          <div class="meta-val">Part 33 — Backend Architecture &amp; Node.js</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Core Innovations</div>
          <div class="meta-val">V8, Libuv, Streams, Buffers, Async I/O</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Target Architecture</div>
          <div class="meta-val">REST APIs, Express, Microservices &amp; Security</div>
        </div>
      </div>
    </header>

    <!-- Chapter Opening Statement (Page 1 Balance) -->
    <div class="opening-card">
      <div class="opening-title">
        <span>✨</span> Advanced JavaScript for Node.js — সার্ভার-সাইড জাভাস্ক্রিপ্ট ও ফুলস্ট্যাক ব্যাকএন্ড
      </div>
      <p class="text-p">
        Node.js কোনো আলাদা প্রোগ্রামিং ভাষা নয়, বরং এটি একটি শক্তিশালী <strong>JavaScript Runtime Environment</strong> যা ব্রাউজারের বাইরে সার্ভারে জাভাস্ক্রিপ্ট চালানোর সুযোগ করে দেয়। V8 ইঞ্জিন, Libuv, ইভেন্ট লুপ, নন-ব্লকিং অ্যাসিনক্রোনাস I/O, প্রসেস অবজেক্ট, এনভায়রনমেন্ট ভ্যারিয়েবল, কমনজেএস বনাম ইএস মডিউল, <code>fs</code>, <code>path</code>, <code>os</code>, <code>events</code>, <code>Buffer</code>, <code>Streams</code> এবং সিকিউর এক্সপ্রেস আর্কিটেকচার এই চ্যাপ্টারের মূল উপজীব্য।
      </p>
      <div class="roadmap-grid">
        <div class="roadmap-item"><span>📌</span> 1. V8 &amp; Event Loop</div>
        <div class="roadmap-item"><span>📌</span> 2. process &amp; env</div>
        <div class="roadmap-item"><span>📌</span> 3. CommonJS vs ESM</div>
        <div class="roadmap-item"><span>📌</span> 4. File System (fs)</div>
        <div class="roadmap-item"><span>📌</span> 5. path &amp; os Modules</div>
        <div class="roadmap-item"><span>📌</span> 6. EventEmitter &amp; once</div>
        <div class="roadmap-item"><span>📌</span> 7. Buffer &amp; Streams</div>
        <div class="roadmap-item"><span>📌</span> 8. HTTP &amp; Express APIs</div>
        <div class="roadmap-item"><span>📌</span> 9. Auth &amp; Pool Security</div>
        <div class="roadmap-item"><span>📌</span> 10. Graceful Shutdown</div>
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

# Process sections 1 to 75
for idx in range(1, 76):
    sec_text = raw_sections[idx].strip()
    pb = check_part_banner(idx)
    if pb:
        html_parts.append(f'    {pb}\n')
        
    sec_lines = sec_text.split('\n')
    header_line = sec_lines[0]
    m_head = re.search(r'# (?:🔥\s*|⚠️\s*)?(39\.\d+)\s*(?:—|-)?\s*(.*)', header_line)
    if m_head:
        sec_num = m_head.group(1)
        sec_title = m_head.group(2)
    else:
        sec_num = f'39.{idx}'
        sec_title = header_line.replace('#', '').strip()
        
    card_extra = ''
    if idx == 1:
        card_extra = ' id="sec-39-1"'
        
    html_parts.append(f'''    <div class="study-card"{card_extra}>
      <div class="card-title"><span class="badge-num">{sec_num}</span> {inline_format(sec_title)}</div>
''')
    
    body_text = '\n'.join(sec_lines[1:]).strip()
    html_parts.append(process_section_body(body_text))
    html_parts.append('    </div>\n')

# Process Section 76: MUST KNOW
pb76 = check_part_banner(76)
if pb76:
    html_parts.append(f'    {pb76}\n')

mustknow_lines = mustknow_clean.split('\n')
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">39.76</span> 🔥 MUST KNOW — Node.js-এর জন্য অত্যন্ত গুরুত্বপূর্ণ JavaScript কনসেপ্ট</div>
''')
html_parts.append(process_section_body('\n'.join(mustknow_lines[1:]).strip()))
html_parts.append('    </div>\n')

# Quick Cheat Sheet Card
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">39.77</span> 🧠 Quick Cheat Sheet — Node.js ব্যাকএন্ড সিনট্যাক্স সারসংক্ষেপ</div>
''')
cheatsheet_lines = cheatsheet_clean.split('\n')
html_parts.append(process_section_body('\n'.join(cheatsheet_lines[1:]).strip()))
html_parts.append('    </div>\n')

# 10 Hands-on Practice Labs with Complete Solutions
html_parts.append('''    <div class="part-banner">Part 10.1 — 10 Hands-On Practice Labs with Complete Production Solutions</div>
''')

practice_solutions = [
    (
        1, "Beginner", "CLI Greeting via process.argv",
        "`node app.js Ripon` কমান্ডের মাধ্যমে টার্মিনাল আর্গুমেন্ট গ্রহণ করে 'Hello Ripon' প্রিন্ট করুন। কোনো নাম না দিলে 'Hello Guest' ফলব্যাক দিন।",
        """// app.js
const args = process.argv.slice(2);
const userName = args[0] ?? 'Guest';

console.log(`Hello ${userName}`);

// Verification in terminal:
// $ node app.js Ripon   -> Output: Hello Ripon
// $ node app.js         -> Output: Hello Guest""",
        None,
        "process.argv হলো একটি অ্যারে যার ইনডেক্স ০-তে থাকে নোড পাথ, ১-এ স্ক্রিপ্ট পাথ এবং ২ থেকে ইউজার পাস করা কমান্ড লাইন আর্গুমেন্টস শুরু হয়।"
    ),
    (
        2, "Beginner", "Asynchronous File Reading via fs/promises",
        "`message.txt` ফাইলটি নন-ব্লকিং অ্যাসিনক্রোনাস পদ্ধতিতে পড়ে কনসোলে আউটপুট প্রদর্শন করুন এবং এরর হ্যান্ডেল করুন।",
        """import fs from 'fs/promises';

async function readMessageFile() {
  try {
    const data = await fs.readFile('message.txt', 'utf-8');
    console.log('File Content:\n' + data);
  } catch (err) {
    if (err.code === 'ENOENT') {
      console.error('❌ Error: message.txt file does not exist!');
    } else {
      console.error('❌ Read Error:', err.message);
    }
  }
}

readMessageFile();""",
        None,
        "প্রোডাকশন ব্যাকএন্ডে কখনোই `readFileSync` ব্যবহার করা উচিত নয়। `fs/promises`-এর `readFile` ইভেন্ট লুপকে ফ্রি রেখে ব্যাকগ্রাউন্ড থ্রেডপুলে ফাইল রিড সম্পন্ন করে।"
    ),
    (
        3, "Beginner", "Asynchronous File Writing via fs/promises",
        "`output.txt` ফাইলে 'Hello from Node.js' টেক্সটটি অ্যাসিনক্রোনাসভাবে সেভ করুন।",
        """import fs from 'fs/promises';

async function writeOutputFile() {
  try {
    const content = 'Hello from Node.js\nCreated on: ' + new Date().toISOString();
    await fs.writeFile('output.txt', content, 'utf-8');
    console.log('✅ File successfully written to output.txt');
  } catch (err) {
    console.error('❌ Write Failed:', err.message);
  }
}

writeOutputFile();""",
        None,
        "fs.writeFile ফাইল না থাকলে স্বয়ংক্রিয়ভাবে নতুন ফাইল তৈরি করে এবং থাকলে পূর্বের কন্টেন্ট ওভাররাইট করে। অ্যাপেন্ড করতে চাইলে `{ flag: 'a' }` অপশন দেওয়া যায়।"
    ),
    (
        4, "Intermediate", "High-Performance File Streaming via pipe()",
        "একটি বড় ফাইল (`source.txt`) থেকে অন্য ফাইলে (`destination.txt`) মেমোরি লোড না করে স্ট্রিম পাইপলাইনের মাধ্যমে কপি করুন।",
        """import fs from 'fs';
import { pipeline } from 'stream/promises';

async function copyFileViaStream() {
  try {
    const sourceStream = fs.createReadStream('source.txt');
    const destStream = fs.createWriteStream('destination.txt');

    // Modern pipeline with auto-cleanup & backpressure management
    await pipeline(sourceStream, destStream);
    console.log('✅ File stream copied successfully without memory leak!');
  } catch (err) {
    console.error('❌ Stream Error:', err.message);
  }
}

copyFileViaStream();""",
        None,
        "বড় সাইজের ফাইল (যেমন 1GB+) একবারেই মেমোরিতে না এনে চাংক আকারে (Chunk by chunk) স্ট্রিম পাইপ করলে সার্ভারে কখনো RAM ক্র্যাশ বা মেমোরি স্পাইক হয় না।"
    ),
    (
        5, "Intermediate", "Decoupled Event Architecture via EventEmitter",
        "একটি `userRegistered` কাস্টম ইভেন্ট তৈরি করুন এবং তাতে লিসেনার অ্যাটাচ করে ইউজার সাইন-আপের সাথে সাথে নোটিফিকেশন লগ প্রিন্ট করুন।",
        """import { EventEmitter } from 'events';

class UserService extends EventEmitter {
  register(name, email) {
    console.log(`Processing registration for ${name}...`);
    // Emit event asynchronously or synchronously
    this.emit('userRegistered', { name, email, time: Date.now() });
  }
}

const userService = new UserService();

// Listener 1: Welcome Email
userService.on('userRegistered', user => {
  console.log(`📧 [Email Service]: Sent welcome mail to ${user.email}`);
});

// Listener 2: Activity Logger
userService.on('userRegistered', user => {
  console.log(`📝 [Audit Log]: New user registered: ${user.name}`);
});

userService.register('Ripon', 'ripon@example.com');""",
        None,
        "EventEmitter নোড ব্যাকএন্ডে মডিউলগুলোর মধ্যে লুজ কাপলিং (Loose Coupling) নিশ্চিত করে। কোর রেজিস্ট্রেশন লজিক পরিবর্তন ছাড়াই নতুন লিসেনার যুক্ত করা যায়।"
    ),
    (
        6, "Intermediate", "Pure Native Node.js HTTP Web Server",
        "কোনো এক্সটার্নাল প্যাকেজ ছাড়া পিওর `http` মডিউল দিয়ে পোর্ট ৩০০০-এ একটি সার্ভার তৈরি করুন যা `/` এ 'Home Page' এবং `/about` এ 'About Page' রেসপন্স দেয়।",
        """import http from 'http';

const server = http.createServer((req, res) => {
  const { url, method } = req;
  res.setHeader('Content-Type', 'text/plain; charset=utf-8');

  if (url === '/' && method === 'GET') {
    res.statusCode = 200;
    res.end('🏠 Welcome to Home Page');
  } else if (url === '/about' && method === 'GET') {
    res.statusCode = 200;
    res.end('ℹ️ Welcome to About Page');
  } else {
    res.statusCode = 404;
    res.end('❌ 404 Route Not Found');
  }
});

const PORT = 3000;
server.listen(PORT, () => {
  console.log(`🚀 Native HTTP Server listening at http://localhost:${PORT}`);
});""",
        None,
        "Express বা Fastify ফ্রেমওয়ার্কগুলো ইন্টারনালি এই নেটিভ `http.createServer` এর উপর ভিত্তি করেই তৈরি। নেটিভ রিকোয়েস্ট-রেসপন্স লাইফসাইকেল বোঝা অত্যন্ত গুরুত্বপূর্ণ।"
    ),
    (
        7, "Intermediate", "RESTful JSON API Endpoint",
        "`/api/user` রাউটে ক্লায়েন্টকে স্ট্যান্ডার্ড হেডারসহ JSON অবজেক্ট রেসপন্স পাঠান।",
        """import http from 'http';

const server = http.createServer((req, res) => {
  if (req.url === '/api/user' && req.method === 'GET') {
    const userPayload = {
      id: 101,
      name: 'Ripon',
      role: 'Full Stack Developer',
      stack: ['JavaScript', 'Node.js', 'React'],
      verified: true
    };

    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(userPayload));
  } else {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Endpoint Not Found' }));
  }
});

server.listen(3001, () => {
  console.log('📡 JSON API Server running at http://localhost:3001/api/user');
});""",
        None,
        "JSON রেসপন্স দেওয়ার সময় অবশ্যই `'Content-Type': 'application/json'` হেডার সেট করতে হয় এবং JavaScript অবজেক্টকে `JSON.stringify()` করে পাঠাতে হয়।"
    ),
    (
        8, "Advanced", "Async/Await Data Pipeline with Timeout & Retry",
        "ডাটাবেস বা এক্সটার্নাল API থেকে ডেটা আনার জন্য একটি অ্যাসিনক্রোনাস ফাংশন লিখুন যা এরর হ্যান্ডলিং ও টাইমাউট সাপোর্ট করে।",
        """// Simulated DB Call with Promise
function fetchDatabaseRecord(id) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id > 0) {
        resolve({ id, username: `user_${id}`, status: 'ACTIVE' });
      } else {
        reject(new Error('Invalid record ID provided'));
      }
    }, 150);
  });
}

async function getUserData(id) {
  try {
    console.log(`Fetching record for ID ${id}...`);
    const data = await fetchDatabaseRecord(id);
    console.log('✅ Record Retrieved:', data);
    return data;
  } catch (err) {
    console.error('❌ Fetch Failure:', err.message);
    return null;
  }
}

getUserData(42);
getUserData(-1); // Triggers safe catch block""",
        None,
        "নোড ব্যাকএন্ডে প্রতিটি অ্যাসিনক্রোনাস অপারেশনকে `try/catch` ব্লকের ভেতরে রাখা জরুরি, যাতে আনহ্যান্ডল্ড রিজেকশন ঘটে সার্ভার প্রসেস ক্র্যাশ না করে।"
    ),
    (
        9, "Advanced", "Parallel API Aggregation via Promise.all()",
        "`getUsers()`, `getProducts()`, এবং `getOrders()` তিনটি স্বাধীন অপারেশনকে প্যারালালে এক্সিকিউট করে এক্সিকিউশন টাইম অপ্টিমাইজ করুন।",
        """const fakeFetch = (name, delay) => 
  new Promise(res => setTimeout(() => res(`${name} Data [OK]`), delay));

async function fetchDashboardData() {
  console.time('Parallel Execution Time');
  
  try {
    // Run all 3 asynchronous calls concurrently in parallel
    const [users, products, orders] = await Promise.all([
      fakeFetch('Users', 200),
      fakeFetch('Products', 300),
      fakeFetch('Orders', 150)
    ]);

    console.log('Aggregation Results:');
    console.log({ users, products, orders });
  } catch (err) {
    console.error('One or more operations failed:', err);
  } finally {
    console.timeEnd('Parallel Execution Time'); // ~300ms total, NOT 650ms!
  }
}

fetchDashboardData();""",
        None,
        "একটির পর একটি await করলে মোট সময় লাগত ২০০+৩০০+১৫০ = ৬৫০ms। `Promise.all()` ব্যবহার করায় সর্বোচ্চ সময় (~৩০০ms)-এ সবগুলো কল সম্পন্ন হয়।"
    ),
    (
        10, "Advanced", "Full Production REST API with Routing & Validation",
        "Express/Node.js প্যাটার্ন মেনে ইন-মেমোরি ডেটাসহ একটি সম্পূর্ণ ইউজার ম্যানেজমেন্ট CRUD ব্যাকএন্ড সিস্টেম লিখুন।",
        """import http from 'http';

let users = [
  { id: 1, name: 'Ripon', role: 'Admin' },
  { id: 2, name: 'Tanvir', role: 'Editor' }
];

function sendJson(res, status, data) {
  res.writeHead(status, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(data));
}

const server = http.createServer((req, res) => {
  const { method, url } = req;

  // 1. GET /users
  if (method === 'GET' && url === '/users') {
    return sendJson(res, 200, users);
  }

  // 2. GET /users/:id
  if (method === 'GET' && url.startsWith('/users/')) {
    const id = parseInt(url.split('/')[2]);
    const user = users.find(u => u.id === id);
    if (!user) return sendJson(res, 404, { error: 'User not found' });
    return sendJson(res, 200, user);
  }

  // 3. POST /users
  if (method === 'POST' && url === '/users') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      try {
        const { name, role } = JSON.parse(body);
        if (!name) return sendJson(res, 400, { error: 'Name is required' });
        const newUser = { id: users.length + 1, name, role: role || 'User' };
        users.push(newUser);
        return sendJson(res, 201, newUser);
      } catch (err) {
        return sendJson(res, 400, { error: 'Invalid JSON payload' });
      }
    });
    return;
  }

  // 4. DELETE /users/:id
  if (method === 'DELETE' && url.startsWith('/users/')) {
    const id = parseInt(url.split('/')[2]);
    const initialLen = users.length;
    users = users.filter(u => u.id !== id);
    if (users.length === initialLen) return sendJson(res, 404, { error: 'User not found' });
    return sendJson(res, 200, { message: `User ${id} deleted successfully` });
  }

  sendJson(res, 404, { error: 'Route not supported' });
});

server.listen(4000, () => {
  console.log('🚀 Complete User CRUD API running at http://localhost:4000/users');
});""",
        None,
        "এটি একটি স্বয়ংসম্পূর্ণ RESTful API কন্ট্রোলার যা ইনকামিং রিকোয়েস্ট বডি পার্সিং, স্ট্যাটাস কোড হ্যান্ডলিং (200, 201, 400, 404) এবং CRUD অপারেশন সম্পন্ন করে।"
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
        html_parts.append(f'      <div class="def-box">💡 <strong>নোড ব্যাকএন্ড আর্কিটেকচারাল ব্যাখ্যা:</strong> {inline_format(lab_expl)}</div>\n')
    html_parts.append('    </div>\n')

# Section 39.78: Final Mental Map
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">39.78</span> 🎯 Final Mental Map — Node.js ব্যাকএন্ড আর্কিটেকচার মানচিত্র</div>
      <p class="text-p">পুরো Chapter 39-এর Node.js ব্যাকএন্ড ইকোসিস্টেম একনজরে:</p>
''')

final_tree = """                    Node.js
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
         V8         Node APIs     libuv
          │            │            │
          └────────────┼────────────┘
                       ↓
                  Event Loop
                       │
            ┌──────────┼──────────┐
            ↓          ↓          ↓
           HTTP        FS        Network
            │          │          │
            └──────────┼──────────┘
                       ↓
                  Async I/O
                       │
                       ↓
                 Express.js
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
       Routes      Middleware    Controllers
                                    │
                                    ↓
                                 Service
                                    │
                                    ↓
                                Database
                                    │
                                    ↓
                                  JSON
                                    │
                                    ↓
                                  React"""

html_parts.append(f'      {render_ascii_box(final_tree, title="NODE.JS ARCHITECTURAL TAXONOMY MAP")}\n')
html_parts.append('''      <div class="def-box" style="margin-top: 6px; border-left: 3px solid #d97706; background: #fffbeb;">
        🏆 <strong>এক লাইনে Chapter 39:</strong> Node.js হলো JavaScript-এর server-side runtime, যেখানে V8 + Event Loop + Asynchronous I/O + Node APIs ব্যবহার করে scalable backend, REST APIs, file/network processing এবং full-stack application তৈরি করা যায়।
      </div>
    </div>
''')

# Curriculum Progression Card (Chapter 38 -> 39 -> 40)
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">39.79</span> 🔗 Curriculum Progression: Chapter 38 → 39 → 40</div>
''')

curriculum_tree = """Chapter 38: Advanced JavaScript for React (Frontend)
       ↓
Destructuring, Spread, map/filter, Immutability, Closures, Synthetic Events
       ↓
Chapter 39: Advanced JavaScript for Node.js (Backend - THIS CHAPTER)
       ↓
V8, Libuv, Event Loop, Buffer, Streams, fs/path, REST API, Express Middleware
       ↓
Chapter 40: Real-World Projects, Best Practices & Interview Preparation (Grand Finale)
       ↓
Production Architecture, Git Workflow, Security Audits, Full-Stack Project & Interview Mastery"""

html_parts.append(f'      {render_ascii_box(curriculum_tree, title="ROADMAP CONTINUITY PIPELINE")}\n')
html_parts.append('    </div>\n')

# Document Closure
html_parts.append('''
  </div>
</body>
</html>''')

# Write complete HTML file
output_html_path = r'c:\Users\User\Desktop\Note-Book\Code\Chapter-39-Advanced-JavaScript-for-NodeJS.html'
with open(output_html_path, 'w', encoding='utf-8') as f:
    f.write(''.join(html_parts))

print(f"HTML successfully generated at: {output_html_path}")
print(f"File size: {os.path.getsize(output_html_path)} bytes")
