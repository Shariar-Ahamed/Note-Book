import re
import sys
import html
import os

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Read raw markdown
with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-32.md', 'r', encoding='utf-8') as f:
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
            ('KEYWORD', r'\b(?:for|while|do|break|continue|if|else|let|const|var|function|return|switch|case|default|of|in|new|typeof|delete|this|super|class|extends|static|instanceof|try|catch|finally|throw|await|async|yield)\b'),
            ('BOOL_NULL', r'\b(?:true|false|null|undefined|NaN)\b'),
            ('DOM_BUILTIN', r'\b(?:console|window|document|navigator|history|location|localStorage|sessionStorage|indexedDB|Notification|Worker|BroadcastChannel|WebSocket|Blob|File|FileReader|URL|URLSearchParams|IntersectionObserver|MutationObserver|ResizeObserver|DataTransfer)\b'),
            ('ASYNC_METHOD', r'\b(?:then|catch|finally|resolve|reject|addEventListener|removeEventListener|querySelector|querySelectorAll|getElementById|pushState|replaceState|writeText|readText|requestPermission|observe|unobserve|disconnect|readAsDataURL|readAsText|createObjectURL|revokeObjectURL|postMessage|close|open|share|request|query)\b'),
            ('NUMBER', r'\b\d+(?:\.\d+)?\b'),
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
            elif kind == 'NUMBER':
                out.append(f'<span class="syn-num">{esc}</span>')
            else:
                out.append(esc)
        return ''.join(out)
    elif lang == 'html':
        t = re.sub(r'(&lt;/?)([a-zA-Z0-9-]+)', r'<span style="color:#f472b6; font-weight:600;">\1\2</span>', esc_all)
        t = re.sub(r'\b(src|href|id|class|type|value|name|placeholder|data-src)=', r'<span style="color:#38bdf8;">\1=</span>', t)
        t = re.sub(r'(&gt;)', r'<span style="color:#f472b6; font-weight:600;">\1</span>', t)
        return t
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
    
    # 3. Colorize Browser Engines & Active Observers (Mint / Emerald)
    t = re.sub(r'\b(Browser|Main Thread|Worker|IndexedDB|WebSocket|FileReader|Blob|IntersectionObserver|MutationObserver|ResizeObserver|Active|Connected|Online|Allowed)\b', r'<span style="color: #34d399; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(✓)', r'<span style="color: #4ade80; font-weight: bold;">✓</span>', t)
    
    # 4. Colorize User Actions & Inputs (Amber / Gold)
    t = re.sub(r'\b(User|Input|File|Click|Select Image|Upload|Preview|Location|Clipboard|Notification|Share|Tab 1|Tab 2|Tab Communication)\b', r'<span style="color: #fde047; font-weight: 600;">\1</span>', t)
    
    # 5. Colorize Protocols & Messaging (Lavender / Purple)
    t = re.sub(r'\b(HTTP|HTTPS|WSS|WS|BroadcastChannel|postMessage|onmessage|History|popstate|pushState|Visibility|Wake Lock)\b', r'<span style="color: #c084fc; font-weight: 700;">\1</span>', t)
    
    # 6. Colorize Units, Limits & Numbers (Orange)
    t = re.sub(r'\b(5MB|100MB|GBs|Offline|Blocked|Denied|Heavy Calculation|Lag|Freeze)\b', r'<span style="color: #fb923c; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(✗|X)', r'<span style="color: #f43f5e; font-weight: bold;">\1</span>', t)
    
    return t

def render_ascii_box(text, title=None):
    if not title:
        # Determine dynamic title based on content
        if 'Worker' in text:
            title = "WEB WORKER MULTI-THREADING ARCHITECTURE"
        elif 'Broadcast' in text or 'Tab' in text:
            title = "CROSS-TAB BROADCASTCHANNEL SYNC FLOW"
        elif 'FileReader' in text or 'Blob' in text or 'File' in text:
            title = "FILE API & BLOB PROCESSING PIPELINE"
        elif 'Intersection' in text or 'Viewport' in text:
            title = "VIEWPORT INTERSECTION OBSERVER LIFECYCLE"
        elif 'WebSocket' in text:
            title = "FULL-DUPLEX WEBSOCKET PROTOCOL PIPELINE"
        elif 'IndexedDB' in text or 'Storage' in text:
            title = "CLIENT STORAGE CAPACITY & ARCHITECTURE"
        elif 'Location' in text or 'Geolocation' in text:
            title = "GEOLOCATION HARDWARE INTEGRATION FLOW"
        elif 'Core JavaScript' in text or 'Browser APIs' in text:
            title = "CORE JAVASCRIPT VS BROWSER WEB APIS"
        else:
            title = "BROWSER API ARCHITECTURE & DATA FLOW"
            
    colorized = colorize_ascii(text)
    return f'''<div class="ascii-tree-container">
  <div class="ascii-tree-header">🌐 {title}</div>
  <pre class="ascii-tree-content">{colorized}</pre>
</div>'''

def render_output_box(text):
    text = html.escape(text.strip())
    return f'''<div class="code-box output-box">
  <div class="code-top"><span class="out-label">▶ CONSOLE / EVENT OUTPUT</span><span>Output</span></div>
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

# Part Banners configuration for Chapter 32
PART_BANNERS = {
    1: ("Part 01", "Browser Web APIs Architecture & Geolocation Integration (32.1 – 32.2)"),
    3: ("Part 02", "URL Processing, Query Strings & History Routing (32.3 – 32.6)"),
    7: ("Part 03", "System Clipboard & Push Notification Services (32.7 – 32.8)"),
    9: ("Part 04", "The Modern Observer Trio (Intersection, Mutation & Resize) (32.9 – 32.12)"),
    13: ("Part 05", "File API, FileReader, Binary Blob & Object URLs (32.13 – 32.18)"),
    19: ("Part 06", "Web Workers Concurrency & Cross-Tab BroadcastChannel (32.19 – 32.20)"),
    21: ("Part 07", "Structured Client Database (IndexedDB) & WebSockets (32.21 – 32.23)"),
    24: ("Part 08", "Hardware Integration, Page Visibility, Wake Lock & Permissions (32.24 – 32.30)"),
    31: ("Part 09", "Hands-On Real-World Mini Projects (32.31 – 32.34)"),
    35: ("Part 10", "Browser APIs Decision Matrix & Core Pillars (32.35 – 32.36)"),
    37: ("Part 11", "Quick Cheat Sheet & 15 Hands-On Practice Labs with Full Solutions"),
    38: ("Part 12", "Final Mental Map & Real-World Capability Matrix"),
}

# Split markdown into sections
raw_sections = re.split(r'\n(?=# 32\.\d+ )', raw_md)
print(f"Total raw section chunks parsed: {len(raw_sections)}")

html_parts = []

# Document Header & CSS Tokens
html_parts.append('''<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter 32 — Advanced Browser APIs | JavaScript Master Study Documentation</title>
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
      #sec-32-1 {
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
          <span class="chapter-badge">Chapter 32</span>
        </div>
      </div>
      <div class="banner-sub">ADVANCED BROWSER APIS, OBSERVERS, WORKERS &amp; REAL-TIME PLATFORM CAPABILITIES</div>
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">Total Modules</div>
          <div class="meta-val">36 Modules + Practice Lab</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Curriculum Part</div>
          <div class="meta-val">Part 26 — Advanced Browser APIs</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Core Mechanics</div>
          <div class="meta-val">Observers, Web Workers, IndexedDB, Sockets</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Reference Standard</div>
          <div class="meta-val">W3C / WHATWG Living Standard 2026</div>
        </div>
      </div>
    </header>

    <!-- Chapter Opening Statement (Page 1 Balance) -->
    <div class="opening-card">
      <div class="opening-title">
        <span>🌐</span> Advanced Browser APIs — ব্রাউজার ও ডিভাইস সক্ষমতা ব্যবহারের মূল উদ্দেশ্য
      </div>
      <p class="text-p">
        JavaScript-এর কোর ল্যাঙ্গুয়েজের সীমানা ছাড়িয়ে ব্রাউজার রানটাইম ডেভেলপারদের যেসব শক্তিশালী প্ল্যাটফর্ম এপিআই প্রদান করে, আধুনিক ওয়েব অ্যাপ্লিকেশনের প্রাণশক্তি হলো সেগুলো। এই চ্যাপ্টারে আমরা <strong>Geolocation, IntersectionObserver, MutationObserver, ResizeObserver, File API &amp; Blob, Web Workers, BroadcastChannel, IndexedDB</strong> এবং <strong>WebSockets</strong> গভীরভাবে শিখব।
      </p>
      <div class="roadmap-grid">
        <div class="roadmap-item"><span>📌</span> 1. Geolocation API</div>
        <div class="roadmap-item"><span>📌</span> 2. URL &amp; History</div>
        <div class="roadmap-item"><span>📌</span> 3. Clipboard API</div>
        <div class="roadmap-item"><span>📌</span> 4. 3 Observers Trio</div>
        <div class="roadmap-item"><span>📌</span> 5. File API &amp; Blob</div>
        <div class="roadmap-item"><span>📌</span> 6. Web Workers</div>
        <div class="roadmap-item"><span>📌</span> 7. BroadcastChannel</div>
        <div class="roadmap-item"><span>📌</span> 8. IndexedDB</div>
        <div class="roadmap-item"><span>📌</span> 9. WebSockets</div>
        <div class="roadmap-item"><span>📌</span> 10. Wake Lock &amp; Share</div>
      </div>
    </div>
''')

# Function to get part banner if applicable
def check_part_banner(sec_idx):
    if sec_idx in PART_BANNERS:
        part_tag, part_title = PART_BANNERS[sec_idx]
        return f'<div class="part-banner">{part_tag} — {part_title}</div>'
    return None

# Process sections 1 to 35
for idx in range(1, 36):
    sec_text = raw_sections[idx].strip()
    pb = check_part_banner(idx)
    if pb:
        html_parts.append(f'    {pb}\n')
        
    sec_lines = sec_text.split('\n')
    header_line = sec_lines[0]
    m_head = re.search(r'# (?:🔥\s*)?(32\.\d+)\s*(?:—|-)?\s*(.*)', header_line)
    if m_head:
        sec_num = m_head.group(1)
        sec_title = m_head.group(2)
    else:
        sec_num = f'32.{idx}'
        sec_title = header_line.replace('#', '').strip()
        
    card_extra = ''
    if idx == 1:
        card_extra = ' id="sec-32-1"'
        
    html_parts.append(f'''    <div class="study-card"{card_extra}>
      <div class="card-title"><span class="badge-num">{sec_num}</span> {inline_format(sec_title)}</div>
''')
    
    body_text = '\n'.join(sec_lines[1:]).strip()
    
    # Check if section contains table (like 32.12 or 32.22 or 32.35)
    body_lines = body_text.split('\n')
    in_code = False
    cur_lang = ''
    code_lines = []
    p_acc = []
    in_list = False
    in_table = False
    table_lines = []
    
    for l in body_lines:
        ls = l.strip()
        
        # Table detection
        if ls.startswith('|') and ls.endswith('|'):
            if not in_table:
                if in_list:
                    html_parts.append('      </ul>\n')
                    in_list = False
                if p_acc:
                    p_text = " ".join(p_acc).strip()
                    if p_text and p_text != '---':
                        html_parts.append(f'      <p class="text-p">{inline_format(p_text)}</p>\n')
                    p_acc = []
                in_table = True
                table_lines = []
            table_lines.append(ls)
            continue
        elif in_table:
            in_table = False
            html_parts.append(f'      {render_table(chr(10).join(table_lines))}\n')
            table_lines = []
            
        # Code fence detection
        if ls.startswith('```'):
            if not in_code:
                if in_list:
                    html_parts.append('      </ul>\n')
                    in_list = False
                if p_acc:
                    p_text = " ".join(p_acc).strip()
                    if p_text and p_text != '---':
                        html_parts.append(f'      <p class="text-p">{inline_format(p_text)}</p>\n')
                    p_acc = []
                in_code = True
                cur_lang = ls[3:].strip().lower()
                code_lines = []
            else:
                in_code = False
                code_content = '\n'.join(code_lines)
                if cur_lang in ('javascript', 'js'):
                    html_parts.append(f'      {render_code_box(code_content, lang="javascript")}\n')
                elif cur_lang == 'html':
                    html_parts.append(f'      {render_code_box(code_content, lang="html", title="HTML DOM MARKUP")}\n')
                else: # text or empty
                    html_parts.append(f'      {render_ascii_box(code_content)}\n')
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
                html_parts.append('      </ul>\n')
                in_list = False
            if p_acc:
                p_text = " ".join(p_acc).strip()
                if p_text and p_text != '---':
                    html_parts.append(f'      <p class="text-p">{inline_format(p_text)}</p>\n')
                p_acc = []
            sub_title = ls[4:].strip()
            html_parts.append(f'      <div class="section-subhead">🔹 {inline_format(sub_title)}</div>\n')
        elif ls.startswith('## '):
            if in_list:
                html_parts.append('      </ul>\n')
                in_list = False
            if p_acc:
                p_text = " ".join(p_acc).strip()
                if p_text and p_text != '---':
                    html_parts.append(f'      <p class="text-p">{inline_format(p_text)}</p>\n')
                p_acc = []
            sub_title = ls[3:].strip()
            html_parts.append(f'      <div class="section-subhead" style="font-size: 11px; color: var(--navy-deep); border-left: 2px solid var(--blue-accent); padding-left: 5px;">🌐 {inline_format(sub_title)}</div>\n')
        elif ls.startswith('* ') or ls.startswith('- '):
            if not in_list:
                if p_acc:
                    p_text = " ".join(p_acc).strip()
                    if p_text and p_text != '---':
                        html_parts.append(f'      <p class="text-p">{inline_format(p_text)}</p>\n')
                    p_acc = []
                html_parts.append('      <ul style="margin: 2px 0 5px 16px; color: #334155; font-size: 10.5px;">\n')
                in_list = True
            html_parts.append(f'        <li>{inline_format(ls[2:])}</li>\n')
        elif ls.startswith('> '):
            if in_list:
                html_parts.append('      </ul>\n')
                in_list = False
            if p_acc:
                p_text = " ".join(p_acc).strip()
                if p_text and p_text != '---':
                    html_parts.append(f'      <p class="text-p">{inline_format(p_text)}</p>\n')
                p_acc = []
            quote_text = ls[2:].strip()
            html_parts.append(f'      <div class="def-box">💡 {inline_format(quote_text)}</div>\n')
        else:
            if in_list:
                html_parts.append('      </ul>\n')
                in_list = False
            p_acc.append(ls)
            
    if in_table:
        html_parts.append(f'      {render_table(chr(10).join(table_lines))}\n')
    if in_list:
        html_parts.append('      </ul>\n')
    if p_acc:
        p_text = " ".join(p_acc).strip()
        if p_text and p_text != '---':
            html_parts.append(f'      <p class="text-p">{inline_format(p_text)}</p>\n')
            
    html_parts.append('    </div>\n')

# Section 32.36: MUST KNOW
sec36_text = raw_sections[35].strip() # Note: index 35 is Section 32.35 which had # 🔥 32.36 MUST KNOW after it

html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">32.36</span> 🔥 MUST KNOW — ব্রাউজার প্ল্যাটফর্মের ১৪টি প্রধান স্তম্ভ</div>
      <p class="text-p">মডার্ন ওয়েব অ্যাপ্লিকেশনের জন্য যেসব ব্রাউজার এপিআই প্রতিটি ইঞ্জিনিয়ারের নখদর্পণে থাকা প্রয়োজন:</p>
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 5px;">
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #0284c7; font-size: 10px; margin-bottom: 3px;">📌 1. Navigation &amp; Hardware</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li><strong>URL &amp; URLSearchParams:</strong> Query string parsing</li>
            <li><strong>History API:</strong> pushState/popstate SPA router</li>
            <li><strong>Geolocation:</strong> GPS coordinate tracking</li>
            <li><strong>Clipboard API:</strong> Async copy/paste text</li>
            <li><strong>Notifications:</strong> Desktop push notifications</li>
          </ul>
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #059669; font-size: 10px; margin-bottom: 3px;">📌 2. Observers &amp; File Pipeline</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li><strong>IntersectionObserver:</strong> Lazy loading &amp; infinite scroll</li>
            <li><strong>MutationObserver:</strong> DOM tree mutation listening</li>
            <li><strong>ResizeObserver:</strong> Container query size changes</li>
            <li><strong>File API &amp; FileReader:</strong> Local file stream read</li>
            <li><strong>Blob &amp; Object URL:</strong> In-memory binary URLs</li>
          </ul>
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #7c3aed; font-size: 10px; margin-bottom: 3px;">📌 3. Concurrency &amp; Storage</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li><strong>Web Workers:</strong> Heavy tasks on separate threads</li>
            <li><strong>BroadcastChannel:</strong> Multi-tab real-time sync</li>
            <li><strong>IndexedDB:</strong> High-capacity client NoSQL DB</li>
            <li><strong>WebSockets:</strong> Full-duplex instant communication</li>
            <li><strong>Page Visibility:</strong> Background tab power saving</li>
          </ul>
        </div>
      </div>
    </div>
''')

# Part 11: Quick Cheat Sheet & Practice Lab
pb11 = check_part_banner(37)
if pb11:
    html_parts.append(f'    {pb11}\n')

# Quick Cheat Sheet
cheat_match = re.search(r'# 🧠 Quick Cheat Sheet[\s\S]*?```javascript([\s\S]*?)```', raw_md)
cheat_code = cheat_match.group(1).strip() if cheat_match else ""

html_parts.append(f'''    <div class="study-card">
      <div class="card-title"><span class="badge-num">32.Cheat</span> 🧠 Quick Cheat Sheet — Browser APIs Rapid Reference</div>
      <p class="text-p">দৈনন্দিন প্রোডাকশন ডেভেলপমেন্টে বহুল ব্যবহৃত ব্রাউজার এপিআই মেথডগুলোর দ্রুত সিনট্যাক্স গাইড:</p>
      {render_code_box(cheat_code, lang="javascript", title="BROWSER APIS RAPID CHEAT SHEET")}
    </div>
''')

# Practice Lab with 15 Problems & Complete Solutions
practice_solutions = [
    {
        "id": "Practice 1",
        "level": "Beginner",
        "title": "URL Hostname Extraction",
        "question": "বর্তমান ব্রাউজার URL থেকে hostname বের করার নিরাপদ উপায় কী?",
        "code": """// Method 1: Using window.location directly
const host1 = window.location.hostname; // e.g. "developer.mozilla.org"

// Method 2: Using the modern URL API for any string
const parsedUrl = new URL("https://github.com/Shariar-Ahamed/Note-Book?tab=readme");
console.log(parsedUrl.hostname); // "github.com"
console.log(parsedUrl.pathname); // "/Shariar-Ahamed/Note-Book" """,
        "output": "github.com",
        "answer": """১. 'window.location.hostname' প্রোপার্টি দিয়ে বর্তমান পেজের ডোমেইন বা আইপি পাওয়া যায়।
২. যেকোনো ডায়নামিক URL স্ট্রিং পার্স করার জন্য 'new URL(urlString)' সবচেয়ে নিরাপদ ও আদর্শ মেকানিজম।"""
    },
    {
        "id": "Practice 2",
        "level": "Beginner",
        "title": "URL Query Parameter Parsing with URLSearchParams",
        "question": "URL থেকে 'id' কুয়েরি প্যারামিটার কীভাবে সহজে বের করবে?",
        "code": """const searchParams = new URLSearchParams(window.location.search);
// Example URL: https://site.com/products?id=42&category=laptops

if (searchParams.has("id")) {
    const productId = searchParams.get("id");
    console.log("Found Product ID:", productId); // "42"
}""",
        "output": "Found Product ID: 42",
        "answer": """১. 'new URLSearchParams(window.location.search)' দিয়ে ব্রাউজারের সার্চ স্ট্রিং তাৎক্ষণিকভাবে ম্যাপে কনভার্ট হয়।
২. '.get("id")' দিয়ে সরাসরি ভ্যালু পাওয়া যায় এবং '.has("id")' দিয়ে উপস্থিতি চেক করা যায়।"""
    },
    {
        "id": "Practice 3",
        "level": "Beginner",
        "title": "Async Clipboard API One-Click Copy Button",
        "question": "আধুনিক ব্রাউজারে একটি সুরক্ষিত ও অ্যাসিঙ্ক কপি বাটন কীভাবে তৈরি করবে?",
        "code": """async function copyToClipboard(textToCopy) {
    try {
        await navigator.clipboard.writeText(textToCopy);
        console.log("Copied to clipboard successfully!");
    } catch (err) {
        console.error("Clipboard permission denied or error:", err);
    }
}

// User trigger:
document.querySelector("#copyBtn").addEventListener("click", () => {
    copyToClipboard("npm install antigravity-ide");
});""",
        "output": "Copied to clipboard successfully!",
        "answer": """১. 'navigator.clipboard.writeText()' একটি প্রমিজ রিটার্ন করে এবং ব্যাকগ্রাউন্ডে নন-ব্লকিংভাবে কাজ করে।
২. সিকিউরিটি নোট: এটি কেবল HTTPS এবং ইউজার ইন্টারঅ্যাকশন (click gesture)-এর ভেতরেই কাজ করতে পারে।"""
    },
    {
        "id": "Practice 4",
        "level": "Beginner",
        "title": "Local Image File Preview with FileReader",
        "question": "ইউজার ইমেজ ফাইল আপলোড করলে তা সার্ভারে না পাঠিয়ে লোকাল প্রিভিউ কীভাবে দেখাবে?",
        "code": """const fileInput = document.querySelector("#imageInput");
const previewImg = document.querySelector("#preview");

fileInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith("image/")) {
        const reader = new FileReader();
        reader.onload = (event) => {
            previewImg.src = event.target.result; // Base64 DataURL
        };
        reader.readAsDataURL(file);
    }
});""",
        "output": "data:image/png;base64,iVBORw0KGgo...",
        "answer": """১. 'e.target.files[0]' দিয়ে File অবজেক্ট পাওয়া যায়।
২. 'FileReader'-এর 'readAsDataURL()' মেথড ইমেজটিকে Base64 স্ট্রিংয়ে রূপান্তর করে ইমেজ ট্যাগের src-তে বসিয়ে দেয়।"""
    },
    {
        "id": "Practice 5",
        "level": "Beginner",
        "title": "Web Notifications API Permission & Trigger",
        "question": "ইউজারের অনুমতি নিয়ে কীভাবে ব্রাউজার নোটিফিকেশন পাঠাবে?",
        "code": """async function triggerDesktopNotification(title, message) {
    if (!("Notification" in window)) return;
    
    let perm = Notification.permission;
    if (perm === "default") {
        perm = await Notification.requestPermission();
    }
    
    if (perm === "granted") {
        new Notification(title, {
            body: message,
            icon: "/assets/bell.png"
        });
    }
}""",
        "output": "Desktop Push Notification Displayed",
        "answer": """১. 'Notification.requestPermission()' ইউজারের কাছে প্রোম্পট দেখায় ('granted', 'denied', বা 'default')।
২. অনুমতি থাকলে 'new Notification(title, options)' কল করে সিস্টেম নোটিফিকেশন প্রদর্শন করা যায়।"""
    },
    {
        "id": "Practice 6",
        "level": "Intermediate",
        "title": "High-Performance Lazy Image Loader with IntersectionObserver",
        "question": "স্ক্রল ইভেন্ট লিসেনার ছাড়া শুধুমাত্র IntersectionObserver দিয়ে ইমেজ লেজি লোড কীভাবে করবে?",
        "code": """const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src; // Swap placeholder with real image
            img.classList.add("loaded");
            obs.unobserve(img); // Disconnect after load to save resources
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll("img.lazy").forEach(img => observer.observe(img));""",
        "output": "Zero-Lag Lazy Loading Active (Images load as they enter viewport)",
        "answer": """১. IntersectionObserver ব্রাউজারের ইন্টারনাল রেন্ডারিং থ্রেডে চলে, ফলে স্ক্রল ইভেন্টের মতো মেইন থ্রেড ব্লক করে না।
২. ইমেজ ভিউপোর্টে আসামাত্র 'entry.isIntersecting' সত্য হয়; ডেটাসেট থেকে আসল URL বসিয়ে 'unobserve()' কল করে ক্লিনআপ করা হয়।"""
    },
    {
        "id": "Practice 7",
        "level": "Intermediate",
        "title": "DOM Tree Mutation Tracking with MutationObserver",
        "question": "কোনো এলিমেন্টে নতুন চাইল্ড নোড যুক্ত বা মুছে ফেলা হলে তা কীভাবে ট্র্যাক করবে?",
        "code": """const targetContainer = document.querySelector("#chatBox");

const observer = new MutationObserver((mutations) => {
    mutations.forEach(mutation => {
        if (mutation.type === "childList") {
            console.log("Nodes added:", mutation.addedNodes.length);
            console.log("Nodes removed:", mutation.removedNodes.length);
        }
    });
});

observer.observe(targetContainer, { childList: true, subtree: true });""",
        "output": "Nodes added: 1 | Chat Auto-Scrolled",
        "answer": """১. MutationObserver পুরানো ডিপ্রিকেটেড Mutation Events-এর তুলনায় হাজার গুণ দ্রুত ও পারফরম্যান্ট।
২. 'childList: true' এবং 'subtree: true' অপশন দিয়ে যেকোনো নেস্টেড চাইল্ড পরিবর্তনের ব্যাচ রেসপন্স পাওয়া যায়।"""
    },
    {
        "id": "Practice 8",
        "level": "Intermediate",
        "title": "Responsive Container Sizing with ResizeObserver",
        "question": "উইন্ডো রিসাইজ ছাড়াই নির্দিষ্ট কোনো কার্ড বা ডিভাইসের সাইজ পরিবর্তন কীভাবে মনিটর করবে?",
        "code": """const card = document.querySelector(".resizable-card");

const resizeObserver = new ResizeObserver((entries) => {
    for (let entry of entries) {
        const { width, height } = entry.contentRect;
        card.querySelector(".size-label").textContent = `${Math.round(width)}px × ${Math.round(height)}px`;
    }
});

resizeObserver.observe(card);""",
        "output": "Real-time dimensions: 320px × 180px",
        "answer": """১. ResizeObserver সরাসরি এলিমেন্টের 'contentRect' প্রদান করে।
২. এটি আধুনিক Container Queries এবং রেসপনসিভ কম্পোনেন্ট ডিজাইনের জন্য সর্বোত্তম।"""
    },
    {
        "id": "Practice 9",
        "level": "Intermediate",
        "title": "Drag and Drop File Dropzone Uploader",
        "question": "ব্রাউজারে একটি ড্র্যাগ অ্যান্ড ড্রপ ফাইল ড্রপজোন কীভাবে তৈরি করবে?",
        "code": """const dropzone = document.querySelector("#dropzone");

dropzone.addEventListener("dragover", (e) => {
    e.preventDefault(); // Required to allow drop!
    dropzone.classList.add("drag-active");
});

dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("drag-active");
});

dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("drag-active");
    
    const files = e.dataTransfer.files;
    console.log("Dropped files count:", files.length);
    handleFileUpload(files[0]);
});""",
        "output": "Dropped files count: 1 | Upload triggered",
        "answer": """১. 'dragover' ইভেন্টে 'e.preventDefault()' কল করা বাধ্যতামূলক, নইলে ব্রাউজার ডিফল্টভাবে ফাইলটি ওপেন করে ফেলে।
২. 'e.dataTransfer.files' দিয়ে সরাসরি ড্রপ করা ফাইলগুলোর লিস্ট অ্যাক্সেস করা যায়।"""
    },
    {
        "id": "Practice 10",
        "level": "Intermediate",
        "title": "Multi-Tab State Synchronization with BroadcastChannel",
        "question": "একই অ্যাপ্লিকেশনের দুটি ওপেন ট্যাবের মধ্যে কীভাবে লাইভ মেসেজ পাস করবে?",
        "code": """// Run this code in Tab 1 and Tab 2:
const authChannel = new BroadcastChannel("auth_sync_channel");

// Tab 2 (Sender): When user logs out
function logoutUser() {
    authChannel.postMessage({ type: "LOGOUT", timestamp: Date.now() });
}

// Tab 1 (Listener): Auto logout
authChannel.onmessage = (event) => {
    if (event.data.type === "LOGOUT") {
        console.log("User logged out in another tab! Redirecting to login...");
        window.location.reload();
    }
};""",
        "output": "User logged out in another tab! Redirecting to login...",
        "answer": """১. BroadcastChannel একই অরিজিনের সব উইন্ডো, ট্যাব এবং আইফ্রেমের মধ্যে নন-ব্লকিং ব্রডকাস্ট মেসেজিং নিশ্চিত করে।
২. সেশন সিঙ্ক, থিম চেঞ্জ বা শপিং কার্ট আপডেটের জন্য এটি localStorage ইভেন্টের চেয়ে শতভাগ ক্লিন।"""
    },
    {
        "id": "Practice 11",
        "level": "Advanced 🔥",
        "title": "Heavy Computation Offloading with Web Workers",
        "question": "ভারী কোনো হিসাব মেইন থ্রেড ব্লক না করে কীভাবে Web Worker দিয়ে চালাবে?",
        "code": """// main.js:
const worker = new Worker("heavy_worker.js");

worker.postMessage({ number: 45 }); // Offload heavy task
console.log("UI remains 100% responsive and silky smooth!");

worker.onmessage = (e) => {
    console.log("Calculation Result from Worker:", e.data.result);
};

// heavy_worker.js (Isolated background thread):
self.onmessage = (e) => {
    function fibonacci(n) {
        return n <= 1 ? n : fibonacci(n - 1) + fibonacci(n - 2);
    }
    const result = fibonacci(e.data.number);
    self.postMessage({ result });
};""",
        "output": "UI remains 100% responsive! | Result: 1134903170",
        "answer": """১. Web Worker আলাদা OS থ্রেডে চলে, ফলে ভারী ম্যাথমেটিক্যাল ক্যালকুলেশন বা ইমেজ প্রসেসিং মেইন UI থ্রেডকে (60fps) কখনোই ফ্রিজ করে না।
২. এটি মেসেজ পাসিং ('postMessage') দিয়ে মেইন থ্রেডের সাথে যোগাযোগ করে।"""
    },
    {
        "id": "Practice 12",
        "level": "Advanced 🔥",
        "title": "Structured Storage with IndexedDB",
        "question": "ব্রাউজারে বড় আকারের অবজেক্ট কীভাবে IndexedDB-তে স্টোর ও রিট্রিভ করবে?",
        "code": """const req = indexedDB.open("OfflineStore", 1);

req.onupgradeneeded = (e) => {
    const db = e.target.result;
    db.createObjectStore("notes", { keyPath: "id", autoIncrement: true });
};

req.onsuccess = (e) => {
    const db = e.target.result;
    const tx = db.transaction("notes", "readwrite");
    const store = tx.objectStore("notes");
    
    store.add({ title: "Master JS Notes", date: new Date().toISOString() });
    
    tx.oncomplete = () => console.log("Transaction saved to IndexedDB!");
};""",
        "output": "Transaction saved to IndexedDB!",
        "answer": """১. IndexedDB একটি সম্পূর্ণ ট্রানজ্যাকশনাল NoSQL অবজেক্ট ডেটাবেস যা গিগাবাইট সাইজের ডেটা অফলাইনে ধরে রাখতে পারে।
২. এটি অ্যাসিনক্রোনাস হওয়ায় ব্রাউজার পারফরম্যান্স অক্ষুণ্ণ রাখে।"""
    },
    {
        "id": "Practice 13",
        "level": "Advanced 🔥",
        "title": "Real-Time Full-Duplex Chat Client with WebSockets",
        "question": "সার্ভারের সাথে ফুল-ডুপ্লেক্স WebSocket কানেকশন কীভাবে হ্যান্ডল করবে?",
        "code": """const socket = new WebSocket("wss://echo.websocket.events");

socket.onopen = () => {
    console.log("Connected to Real-time WebSocket Server!");
    socket.send(JSON.stringify({ text: "Hello from Client!" }));
};

socket.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    console.log("Message received from Server:", msg.text);
};

socket.onerror = (err) => console.error("Socket error:", err);
socket.onclose = () => console.log("Socket connection terminated cleanly.");""",
        "output": "Connected to WebSocket! | Message received: Hello from Client!",
        "answer": """১. WebSocket একটি স্থায়ী TCP কানেকশন তৈরি করে যাতে সার্ভার ও ক্লায়েন্ট উভয়ই যেকোনো সময় ডেটা পুশ করতে পারে।
২. এটি সাধারণ HTTP লং-পোলিংয়ের বিশাল ওভারহেড দূর করে সাব-মিলিমিটারে ডেটা ট্রান্সমিট করে।"""
    },
    {
        "id": "Practice 14",
        "level": "Advanced 🔥",
        "title": "Client-Side SPA Routing Engine with History API",
        "question": "পেজ রিলোড ছাড়া History API দিয়ে সিঙ্গেল পেজ রাউটিং কীভাবে কাজ করে?",
        "code": """function navigateTo(urlPath) {
    history.pushState({ path: urlPath }, "", urlPath);
    renderPage(urlPath);
}

window.addEventListener("popstate", (event) => {
    // Triggered when user presses Browser Back or Forward buttons!
    renderPage(window.location.pathname);
});

function renderPage(path) {
    console.log("Rendered SPA view for route:", path);
}""",
        "output": "Rendered SPA view for route: /dashboard",
        "answer": """১. 'history.pushState()' ব্রাউজারের অ্যাড্রেস বার ও হিস্ট্রি ট্র্যাকে নতুন URL যোগ করে কোনো সার্ভার রিলোড ছাড়াই।
২. 'popstate' ইভেন্ট হ্যান্ডলার ব্রাউজারের Back/Forward বাটনের ন্যাভিগেশন নিখুঁতভাবে হ্যান্ডল করে।"""
    },
    {
        "id": "Practice 15",
        "level": "Advanced 🔥",
        "title": "Dynamic In-Memory File Generation & Download with Blob & Object URL",
        "question": "সার্ভার ছাড়া ব্রাউজার মেমরিতে টেক্সট/JSON ফাইল বানিয়ে স্বয়ংক্রিয়ভাবে কীভাবে ডাউনলোড করাবে?",
        "code": """function downloadJsonFile(dataObj, filename = "export.json") {
    const jsonStr = JSON.stringify(dataObj, null, 2);
    const blob = new Blob([jsonStr], { type: "application/json" });
    
    const downloadUrl = URL.createObjectURL(blob);
    const tempLink = document.createElement("a");
    tempLink.href = downloadUrl;
    tempLink.download = filename;
    
    document.body.appendChild(tempLink);
    tempLink.click();
    
    // Clean up memory
    document.body.removeChild(tempLink);
    URL.revokeObjectURL(downloadUrl);
    console.log("File downloaded & memory revoked cleanly.");
}""",
        "output": "File downloaded & memory revoked cleanly.",
        "answer": """১. 'new Blob()' ক্লায়েন্ট-সাইড মেমরিতে বাইনারি ডেটা কন্টেইনার তৈরি করে।
২. 'URL.createObjectURL(blob)' একটি অস্থায়ী 'blob:http...' URL তৈরি করে যা লিঙ্কের ডাউনলোড হিসেবে কাজ করে।
৩. মেমরি লিক এড়াতে ডাউনলোড শেষে 'URL.revokeObjectURL()' কল করা প্রোডাকশন কোডের গোল্ডেন স্ট্যান্ডার্ড।"""
    }
]

html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">32.Lab</span> 📝 Hands-On Practice Lab — 15 Browser API Challenges &amp; Full Model Solutions</div>
      <p class="text-p">রিয়েল-ওয়ার্ল্ড ব্রাউজার এপিআই দক্ষতায় পূর্ণাঙ্গ পারদর্শিতা অর্জন করতে ১৫টি ইন্টারভিউ প্রবলেমের সমাধান:</p>
''')

for p in practice_solutions:
    lvl_color = "#059669" if p["level"] == "Beginner" else ("#d97706" if "Intermediate" in p["level"] else "#dc2626")
    html_parts.append(f'''      <div class="practice-item">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 3px;">
          <span style="font-weight: 700; font-size: 11px; color: var(--navy-deep);">{p["id"]}: {p["title"]}</span>
          <span style="background: {lvl_color}; color: white; font-size: 8px; font-weight: 700; padding: 1px 6px; border-radius: 3px; text-transform: uppercase;">{p["level"]}</span>
        </div>
        <p class="text-p" style="margin-bottom: 3px; font-weight: 600; color: #0f172a;">❓ {p["question"]}</p>
        {render_code_box(p["code"], lang="javascript", title=f'{p["id"]} Implementation')}
        {render_output_box(p["output"])}
        <div class="def-box" style="margin-top: 3px; background: #f8fafc; border-left: 3px solid var(--blue-accent);">
          <div style="font-weight: 700; font-size: 9px; color: var(--blue-dark); margin-bottom: 2px;">🔍 Model Architecture &amp; Solution Breakdown:</div>
          <div style="font-size: 8.5px; color: #334155; line-height: 1.4; white-space: pre-wrap;">{p["answer"]}</div>
        </div>
      </div>
''')

html_parts.append('    </div>\n')

# Final Mental Map
final_map_match = re.search(r'# 🎯 Final Mental Map[\s\S]*?```text([\s\S]*?)```', raw_md)
final_map_ascii = final_map_match.group(1).strip() if final_map_match else ""

# Core capability list
core_caps_match = re.search(r'এর মতো real-world functionality তৈরি করতে পারবে।', raw_md)

html_parts.append(f'''    <div class="study-card">
      <div class="card-title"><span class="badge-num">32.Map</span> 🎯 Final Mental Map — Advanced Browser APIs Global Ecosystem</div>
      <p class="text-p">ব্রাউজার ফিচার, ভিউপোর্ট অবজারভার, ডেটা স্টোরেজ ও থ্রেডিং কমিউনিকেশনের সামগ্রিক মানচিত্র:</p>
      {render_ascii_box(final_map_ascii, title="Browser APIs Global Architectural Coordination Tree")}
      
      <div class="def-box" style="margin-top: 6px; padding: 6px 10px; background: #f0fdf4; border-left: 3px solid #10b981;">
        <div style="font-weight: 700; font-size: 10px; color: #065f46; margin-bottom: 2px;">🚀 Chapter 32-এর মূল দর্শন:</div>
        <div style="font-size: 9.5px; color: #047857; line-height: 1.45;">
          <strong>Browser API = JavaScript + Browser-এর extra capabilities।</strong> JavaScript কেবল সাধারণ ক্যালকুলেশন বা DOM ম্যানিপুলেশন নয়—লোকেশন ট্র্যাকিং, পুশ নোটিফিকেশন, ব্যাকগ্রাউন্ড মাল্টি-থ্রেডিং, জিগাবাইট স্টোরেজ ও রিয়েল-টাইম ফুল-ডুপ্লেক্স কমিউনিকেশনের মাধ্যমে পূর্ণাঙ্গ নেটিভ অ্যাপ সমতুল্য অভিজ্ঞতা দেয়।
        </div>
      </div>

      <div class="def-box" style="margin-top: 6px; padding: 6px 10px; background: #eff6ff; border-left: 3px solid #2563eb;">
        <div style="font-weight: 700; font-size: 10px; color: #1e40af; margin-bottom: 2px;">🚀 Next Chapter Preview:</div>
        <div style="font-family: var(--font-heading); font-size: 10px; font-weight: 700; color: #0369a1;">
          Chapter 33 — JavaScript Web Performance &amp; Optimization
        </div>
        <div style="font-size: 9px; color: #334155; margin-top: 2px;">পরবর্তী চ্যাপ্টারে আমরা শিখব Critical Rendering Path, Repaint &amp; Reflow, Debounce/Throttle, Code Splitting, Bundle Analysis, Memory Profiling এবং Web Vitals (LCP, FID/INP, CLS)।</div>
      </div>
    </div>

  </div>

</body>
</html>
''')

# Write complete HTML file
output_html_path = r'c:\Users\User\Desktop\Note-Book\Code\Chapter-32-Advanced-Browser-APIs.html'
with open(output_html_path, 'w', encoding='utf-8') as f:
    f.write(''.join(html_parts))

print(f"Successfully generated Chapter 32 HTML: {output_html_path}")
print(f"File size: {os.path.getsize(output_html_path)} bytes")
