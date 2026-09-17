import re
import sys
import html
import os

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Read raw markdown
with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-33.md', 'r', encoding='utf-8') as f:
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
            ('KEYWORD', r'\b(?:for|while|do|break|continue|if|else|let|const|var|function|return|switch|case|default|of|in|new|typeof|delete|this|super|class|extends|static|instanceof|try|catch|finally|throw|await|async|yield|import|export|from|default)\b'),
            ('BOOL_NULL', r'\b(?:true|false|null|undefined|NaN)\b'),
            ('DOM_BUILTIN', r'\b(?:console|window|document|navigator|performance|AbortController|IntersectionObserver|Worker|DocumentFragment|requestAnimationFrame|cancelAnimationFrame|setTimeout|clearTimeout|setInterval|clearInterval|fetch|Promise|Math|Image|URL|Response|Headers|Request)\b'),
            ('ASYNC_METHOD', r'\b(?:then|catch|finally|resolve|reject|addEventListener|removeEventListener|querySelector|querySelectorAll|getElementById|appendChild|replaceChildren|postMessage|terminate|observe|unobserve|disconnect|now|mark|measure|abort|json|clone|forEach|map|filter|reduce|push|slice|splice)\b'),
            ('NUMBER', r'\b\d+(?:\.\d+)?(?:px|ms|s|rem|em|%)?\b'),
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
        t = re.sub(r'\b(src|srcset|sizes|href|id|class|type|value|name|placeholder|loading|rel|as|defer|async|width|height|alt)=', r'<span style="color:#38bdf8;">\1=</span>', t)
        t = re.sub(r'(&gt;)', r'<span style="color:#f472b6; font-weight:600;">\1</span>', t)
        t = re.sub(r'(&quot;.*?&quot;)', r'<span style="color:#4ade80;">\1</span>', t)
        return t
    elif lang in ('http', 'headers'):
        t = re.sub(r'^([A-Za-z0-9-]+:)', r'<span style="color:#38bdf8; font-weight:700;">\1</span>', esc_all, flags=re.MULTILINE)
        t = re.sub(r'\b(max-age=\d+|public|private|no-cache|no-store|must-revalidate|immutable)\b', r'<span style="color:#4ade80; font-weight:600;">\1</span>', t)
        t = re.sub(r'(&quot;.*?&quot;)', r'<span style="color:#fde047;">\1</span>', t)
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
    
    # 3. Critical Rendering Stages (Emerald / Mint)
    t = re.sub(r'\b(DOM|CSSOM|Render Tree|Layout|Paint|Composite|Reflow|Repaint)\b', r'<span style="color: #34d399; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(✓|Fast|Optimized|Result|Fast response|Need হলে load)', r'<span style="color: #4ade80; font-weight: bold;">\1</span>', t)
    
    # 4. Network & Caching (Amber / Gold)
    t = re.sub(r'\b(DNS|TCP|TLS|HTTP|HTTPS|HTTP/2|HTTP/3|CDN|Cache|Cache-Control|ETag|Server Response|HTML Load|CSS Load|JavaScript Load|Content Render|User Interaction|Network Waterfall|Download|Assets)\b', r'<span style="color: #fde047; font-weight: 600;">\1</span>', t)
    
    # 5. Optimization Techniques (Lavender / Violet)
    t = re.sub(r'\b(Debounce|Throttle|Lazy Loading|Code Splitting|Tree Shaking|Minification|Compression|Brotli|Gzip|Web Worker|DocumentFragment|requestAnimationFrame|will-change|AbortController|Preload|Prefetch|IntersectionObserver|Small chunks)\b', r'<span style="color: #c084fc; font-weight: 700;">\1</span>', t)
    
    # 6. Core Web Vitals & Metrics (Orange / Amber)
    t = re.sub(r'\b(Core Web Vitals|LCP|INP|CLS|TTFB|FCP|FID|60FPS|16\.6ms|Target|Good|Needs Improvement|Poor)\b', r'<span style="color: #fbbf24; font-weight: 700;">\1</span>', t)
    
    # 7. Bottlenecks & Hazards (Rose / Crimson)
    t = re.sub(r'\b(Bottleneck|Layout Thrashing|Long Task|>50ms|Main Thread Freeze|Memory Leak|Lag|Heavy Calculation|Blocked|5 seconds wait|Slow|Unused code)\b', r'<span style="color: #f43f5e; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(✗|X|Fail|Poor|Unused|Remove)', r'<span style="color: #f43f5e; font-weight: bold;">\1</span>', t)
    
    # 8. Checklist markers
    t = re.sub(r'(□)', r'<span style="color: #38bdf8; font-weight: bold;">□</span>', t)
    
    return t

def render_ascii_box(text, title=None):
    if not title:
        # Determine dynamic title based on content
        if 'Render Tree' in text or 'CSSOM' in text or 'Composite' in text:
            title = "CRITICAL RENDERING PATH & BROWSER PIPELINE"
        elif 'Thrashing' in text or 'Layout' in text:
            title = "LAYOUT THRASHING VS BATCHED EXECUTION FLOW"
        elif 'Debounce' in text or 'Wait' in text or 'Typing' in text:
            title = "DEBOUNCE VS THROTTLE EXECUTION TIMELINE"
        elif 'Network' in text or 'CDN' in text or 'Cache' in text:
            title = "NETWORK WATERFALL & CACHING PIPELINE"
        elif 'Worker' in text or 'computation' in text:
            title = "MAIN THREAD VS WEB WORKER CONCURRENCY"
        elif 'LCP' in text or 'INP' in text or 'CLS' in text:
            title = "CORE WEB VITALS METRICS & TARGET BENCHMARKS"
        elif 'Dashboard' in text:
            title = "DYNAMIC CODE SPLITTING & ROUTE LAZY LOADING"
        elif 'Optimization Checklist' in text or '□' in text:
            title = "PRODUCTION PERFORMANCE CHECKLIST"
        elif 'WEB PERFORMANCE' in text:
            title = "FULL-STACK WEB PERFORMANCE ARCHITECTURE"
        else:
            title = "PERFORMANCE LIFECYCLE & EXECUTION FLOW"
            
    colorized = colorize_ascii(text)
    return f'''<div class="ascii-tree-container">
  <div class="ascii-tree-header">⚡ {title}</div>
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

# Part Banners configuration for Chapter 33
PART_BANNERS = {
    1: ("Part 01", "Foundations of Web Performance & Page Load Lifecycle (33.1 – 33.5)"),
    6: ("Part 02", "Critical Rendering Path, Layout, Paint & Layout Thrashing (33.6 – 33.15)"),
    16: ("Part 03", "DOM Batching, Bundle Size, Tree Shaking & Compression (33.16 – 33.22)"),
    23: ("Part 04", "Media & Image Optimization, Responsive & Lazy Loading (33.23 – 33.27)"),
    28: ("Part 05", "Code Splitting & Dynamic Imports (33.28 – 33.29)"),
    30: ("Part 06", "Event Optimization: Debounce, Throttle & Passive Listeners (33.30 – 33.34)"),
    35: ("Part 07", "Rendering Performance, rAF & GPU Acceleration (33.35 – 33.39)"),
    40: ("Part 08", "Browser Caching, CDN & Network Waterfall (33.40 – 33.45)"),
    46: ("Part 09", "Profiling, Long Tasks, Web Workers & Memory Leaks (33.46 – 33.51)"),
    52: ("Part 10", "Resource Hints, Critical CSS, Fonts & API Abort (33.52 – 33.62)"),
    63: ("Part 11", "Core Web Vitals, Performance Budget & Production Checklist (33.63 – 33.70)"),
    71: ("Part 12", "Must Know Architecture, Quick Cheat Sheet, 12 Practice Labs & Final Mental Map"),
}

# Split markdown into sections
raw_sections = re.split(r'\n(?=# 33\.\d+ )', raw_md)
print(f"Total raw section chunks parsed: {len(raw_sections)}")

# Separate Section 70 from 33.71, Cheat Sheet, Practice Set, and Final Mental Map
sec70_full = raw_sections[70]
sec70_subparts = re.split(r'\n(?=# (?:🔥\s*33\.71|🧠\s*Quick|📝\s*Practice|🎯\s*Final))', sec70_full)

sec70_clean = sec70_subparts[0].strip()
sec71_clean = sec70_subparts[1].strip() if len(sec70_subparts) > 1 else ""
cheatsheet_clean = sec70_subparts[2].strip() if len(sec70_subparts) > 2 else ""
practice_clean = sec70_subparts[3].strip() if len(sec70_subparts) > 3 else ""
mentalmap_clean = sec70_subparts[4].strip() if len(sec70_subparts) > 4 else ""

html_parts = []

# Document Header & CSS Tokens
html_parts.append('''<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter 33 — Web Performance & Optimization | JavaScript Master Study Documentation</title>
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
      #sec-33-1 {
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
          <span class="chapter-badge">Chapter 33</span>
        </div>
      </div>
      <div class="banner-sub">WEB PERFORMANCE &amp; OPTIMIZATION, CRITICAL RENDERING PATH, RUNTIME EFFICIENCY &amp; CORE WEB VITALS</div>
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">Total Modules</div>
          <div class="meta-val">70 Modules + 12 Practice Labs</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Curriculum Part</div>
          <div class="meta-val">Part 27 — Web Performance</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Core Metrics</div>
          <div class="meta-val">LCP, INP, CLS, TTFB &amp; 60 FPS</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Reference Standard</div>
          <div class="meta-val">W3C / Chrome Web Vitals 2026</div>
        </div>
      </div>
    </header>

    <!-- Chapter Opening Statement (Page 1 Balance) -->
    <div class="opening-card">
      <div class="opening-title">
        <span>⚡</span> Web Performance &amp; Optimization — গতি, স্কেলাবিলিটি ও ইউজার সন্তুষ্টির মূল ভিত্তি
      </div>
      <p class="text-p">
        Web application শুধু কাজ করলেই আধুনিক ইঞ্জিনিয়ারিংয়ের দায়িত্ব শেষ হয় না—এটি যেন <strong>বিদ্যুৎ গতিতে লোড হয়, চোখের পলকে রেসপন্ড করে, ব্যাটারি ও মেমোরি সাশ্রয়ী হয় এবং মসৃণ ইউজার এক্সপেরিয়েন্স দেয়</strong>, সেটাই চূড়ান্ত লক্ষ্য। এই চ্যাপ্টারে আমরা <strong>Critical Rendering Path, Layout Thrashing, Debounce/Throttle, Lazy Loading, Code Splitting, Caching &amp; CDN, Web Workers, Core Web Vitals (LCP, INP, CLS)</strong> এবং প্রোডাকশন অপ্টিমাইজেশন পদ্ধতি শিখব।
      </p>
      <div class="roadmap-grid">
        <div class="roadmap-item"><span>📌</span> 1. CRP &amp; DOM Flow</div>
        <div class="roadmap-item"><span>📌</span> 2. Layout Thrashing</div>
        <div class="roadmap-item"><span>📌</span> 3. Bundle &amp; Tree Shake</div>
        <div class="roadmap-item"><span>📌</span> 4. Modern Image Formats</div>
        <div class="roadmap-item"><span>📌</span> 5. Dynamic Code Split</div>
        <div class="roadmap-item"><span>📌</span> 6. Debounce &amp; Throttle</div>
        <div class="roadmap-item"><span>📌</span> 7. 60 FPS &amp; rAF</div>
        <div class="roadmap-item"><span>📌</span> 8. HTTP Cache &amp; CDN</div>
        <div class="roadmap-item"><span>📌</span> 9. Workers &amp; Memory</div>
        <div class="roadmap-item"><span>📌</span> 10. Core Web Vitals</div>
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
                elif cur_lang == 'html':
                    res.append(f'      {render_code_box(code_content, lang="html", title="HTML DOM MARKUP")}\n')
                elif cur_lang in ('http', 'headers'):
                    res.append(f'      {render_code_box(code_content, lang="http", title="HTTP CACHE HEADERS")}\n')
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
            res.append(f'      <div class="section-subhead" style="font-size: 11px; color: var(--navy-deep); border-left: 2px solid var(--blue-accent); padding-left: 5px;">⚡ {inline_format(sub_title)}</div>\n')
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

# Process sections 1 to 69
for idx in range(1, 70):
    sec_text = raw_sections[idx].strip()
    pb = check_part_banner(idx)
    if pb:
        html_parts.append(f'    {pb}\n')
        
    sec_lines = sec_text.split('\n')
    header_line = sec_lines[0]
    m_head = re.search(r'# (?:🔥\s*)?(33\.\d+)\s*(?:—|-)?\s*(.*)', header_line)
    if m_head:
        sec_num = m_head.group(1)
        sec_title = m_head.group(2)
    else:
        sec_num = f'33.{idx}'
        sec_title = header_line.replace('#', '').strip()
        
    card_extra = ''
    if idx == 1:
        card_extra = ' id="sec-33-1"'
        
    html_parts.append(f'''    <div class="study-card"{card_extra}>
      <div class="card-title"><span class="badge-num">{sec_num}</span> {inline_format(sec_title)}</div>
''')
    
    body_text = '\n'.join(sec_lines[1:]).strip()
    html_parts.append(process_section_body(body_text))
    html_parts.append('    </div>\n')

# Process Section 70 (Cleaned of subparts)
pb70 = check_part_banner(70)
if pb70:
    html_parts.append(f'    {pb70}\n')
    
sec70_lines = sec70_clean.split('\n')
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">33.70</span> Production Optimization Checklist</div>
''')
html_parts.append(process_section_body('\n'.join(sec70_lines[1:]).strip()))
html_parts.append('    </div>\n')

# Part 12 Banner & Section 33.71: MUST KNOW
pb12 = check_part_banner(71)
if pb12:
    html_parts.append(f'    {pb12}\n')

html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">33.71</span> 🔥 MUST KNOW — পারফরম্যান্স অপ্টিমাইজেশনের ১০টি মূল স্তম্ভ</div>
      <p class="text-p">প্রোডাকশন গ্রেড ওয়েব অ্যাপ্লিকেশনের গতি ও রেসপন্সিভনেস নিশ্চিত করার জন্য এই ১০টি আর্কিটেকচারাল প্যাটার্ন সর্বদা মনে রাখা প্রয়োজন:</p>
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 5px;">
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #0284c7; font-size: 10px; margin-bottom: 3px;">📌 1. Rendering Pipeline &amp; DOM</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li><strong>DOM + CSSOM:</strong> Render Tree গঠন করে লেআউট তৈরি</li>
            <li><strong>Layout &amp; Paint:</strong> রিফ্লো কমানো ও GPU কম্পোজিটিং ব্যবহার</li>
            <li><strong>DocumentFragment:</strong> ১০০০টি নোড মাত্র ১টি রিফ্লোতে ইনসার্ট</li>
            <li><strong>will-change &amp; CSS Transform:</strong> সিপিইউ থ্রেড বাদ দিয়ে জিপিইউতে এনিমেশন</li>
          </ul>
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #059669; font-size: 10px; margin-bottom: 3px;">📌 2. Runtime Execution &amp; Events</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li><strong>Debounce:</strong> সার্চ ইনপুটে টাইপিং থামা পর্যন্ত অপেক্ষা</li>
            <li><strong>Throttle:</strong> স্ক্রল বা রিসাইজে নির্দিষ্ট ইন্টারভালে এক্সিকিউশন</li>
            <li><strong>Passive Listeners:</strong> স্ক্রলিংয়ে preventDefault ব্লকিং রোধ</li>
            <li><strong>Web Workers:</strong> মেইন থ্রেডকে ফ্রি রেখে ব্যাকগ্রাউন্ডে ক্যালকুলেশন</li>
          </ul>
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #7c3aed; font-size: 10px; margin-bottom: 3px;">📌 3. Delivery &amp; Core Web Vitals</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li><strong>Code Splitting:</strong> ডাইনামিক import() দিয়ে অন-ডিমান্ড মডিউল লোড</li>
            <li><strong>Brotli &amp; Tree Shaking:</strong> অব্যবহৃত কোড বাদ দিয়ে সাইজ ৭০% হ্রাস</li>
            <li><strong>Cache-Control &amp; CDN:</strong> ব্যবহারকারীর নিকটবর্তী নোড থেকে ক্যাশ ডেলিভারি</li>
            <li><strong>Core Web Vitals:</strong> LCP (&lt;2.5s), INP (&lt;200ms), CLS (&lt;0.1) লক্ষ্য পূরণ</li>
          </ul>
        </div>
      </div>
    </div>
''')

# Quick Cheat Sheet Card
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">33.72</span> 🧠 Quick Cheat Sheet — পারফরম্যান্স ধারণাসমূহের সারসংক্ষেপ</div>
''')
cheat_table = '''| Topic | Main Concept & Mechanism |
| :--- | :--- |
| **DOM** | HTML ডকুমেন্টের ইন-মেমোরি নোড ট্রি গঠন |
| **CSSOM** | CSS সিলেক্টর ও স্টাইল রুলসের ক্যাস্কেডিং অবজেক্ট ট্রি |
| **Layout (Reflow)** | উপাদানের জ্যামিতিক সাইজ ও স্ক্রিনে সঠিক পজিশন গণনা |
| **Paint (Repaint)** | পিক্সেল ড্রয়িং (রং, ব্যাকগ্রাউন্ড, শ্যাডো, বর্ডার রেন্ডারিং) |
| **Composite** | আলাদা জিপিইউ লেয়ারসমূহকে স্ক্রিনে একত্রিত করা |
| **Debounce** | ব্যবহারকারীর অ্যাকশন থামা পর্যন্ত ফাংশন এক্সিকিউশন স্থগিত রাখা |
| **Throttle** | নির্দিষ্ট সময় ব্যবধানে সর্বোচ্চ একবার ফাংশন এক্সিকিউট করা |
| **Lazy Loading** | উপাদান স্ক্রিনে আসার ঠিক আগ মুহূর্তে লোড করা (`loading="lazy"`) |
| **Code Splitting** | বিশাল বান্ডেল ভেঙে ছোট ছোট অন-ডিমান্ড চাঙ্ক তৈরি করা |
| **Tree Shaking** | বিল্ড টাইমে অব্যবহৃত ডেড-কোড স্বয়ংক্রিয়ভাবে মুছে ফেলা |
| **Minification** | হোয়াইটস্পেস ও ভ্যারিয়েবল নাম ছোট করে সাইজ সংকুচিত করা |
| **Compression** | ট্রান্সফারের সময় Brotli/Gzip দিয়ে ফাইল সাইজ কমানো |
| **CDN** | ভৌগোলিকভাবে ব্যবহারকারীর নিকটবর্তী এজ-সার্ভার থেকে ফাইল পরিবেশন |
| **HTTP Cache** | `Cache-Control: max-age` দিয়ে ব্রাউজারে রিসোর্স পুনব্যবহার |
| **Web Worker** | মেইন থ্রেডকে ফ্রি রেখে ব্যাকগ্রাউন্ড থ্রেডে হেভি প্রসেসিং |
| **requestAnimationFrame** | ব্রাউজারের রিফ্রেশ রেটের (60FPS/16.6ms) সাথে সিঙ্ক করে স্মুথ অ্যানিমেশন |
| **AbortController** | অপ্রয়োজনীয় বা পুরাতন ফেচ রিকোয়েস্ট তৎক্ষণাৎ বাতিল করা |
| **LCP (Largest Contentful Paint)** | পেজের সবচেয়ে বড় কন্টেন্ট রেন্ডার হওয়ার সময় (লক্ষ্য: &lt; 2.5s) |
| **INP (Interaction to Next Paint)** | ইউজার ক্লিকের পর ভিজ্যুয়াল রেসপন্স পেতে দেরি (লক্ষ্য: &lt; 200ms) |
| **CLS (Cumulative Layout Shift)** | পেজ লোড হওয়ার সময় কন্টেন্টের অনাকাঙ্ক্ষিত নড়াচড়া (লক্ষ্য: &lt; 0.1) |'''
html_parts.append(f'      {render_table(cheat_table)}\n')
html_parts.append('    </div>\n')

# 12 Hands-on Practice Labs with Complete Solutions
html_parts.append('''    <div class="part-banner">Part 12.1 — 12 Hands-On Practice Labs with Complete Production Solutions</div>
''')

practice_solutions = [
    (
        1, "Beginner", "Debounced Search Input with Live Console Logging",
        "একটি search input তৈরি করুন এবং debounce ব্যবহার করে console-এ search value print করুন। টাইপিং থামার ৫০০ms পর রিকোয়েস্ট কার্যকর হবে।",
        """// 1. Debounce Utility Function
function debounce(func, delay = 500) {
  let timerId = null;
  return function(...args) {
    clearTimeout(timerId); // পূর্বের টাইমার বাতিল
    timerId = setTimeout(() => {
      func.apply(this, args); // বিলম্ব শেষে মূল ফাংশন কল
    }, delay);
  };
}

// 2. Search Handler Function
function handleSearch(query) {
  console.log(`[API Search Triggered]: "${query}" at ${new Date().toLocaleTimeString()}`);
}

// 3. Debounced Wrapper & Event Listener
const debouncedSearch = debounce((event) => {
  handleSearch(event.target.value.trim());
}, 500);

const searchInput = document.getElementById('search-input');
searchInput.addEventListener('input', debouncedSearch);""",
        """<!-- HTML Search Input Markup -->
<div class="search-box">
  <input type="text" id="search-input" placeholder="Search products, documentation..." autocomplete="off">
  <div id="search-status">Typing triggers debounced API call after 500ms idle</div>
</div>""",
        "ব্যবহারকারী প্রতি ক্লিকে কিপ্রেস করলেও অপ্রয়োজনীয় ২০টি রিকোয়েস্ট না পাঠিয়ে টাইপিং থামার পর মাত্র ১টি নেটওয়ার্ক কল করবে, যা ব্যান্ডউইথ ও সার্ভার লোড বাঁচায়।"
    ),
    (
        2, "Beginner", "Throttled Window Scroll Event Listener",
        "একটি scroll event-এ throttle ব্যবহার করুন যাতে প্রতি ৩০০ms-এ সর্বোচ্চ একবার স্ক্রল পজিশন গণনা ও কনসোলে লগ হয়।",
        """// 1. Timestamp-based Throttle Utility
function throttle(func, interval = 300) {
  let lastTime = 0;
  return function(...args) {
    const now = Date.now();
    if (now - lastTime >= interval) {
      lastTime = now;
      func.apply(this, args);
    }
  };
}

// 2. Scroll Progress Tracker
function logScrollPosition() {
  const scrollTop = window.scrollY || document.documentElement.scrollTop;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = Math.round((scrollTop / docHeight) * 100);
  console.log(`[Throttled Scroll] Position: ${scrollTop}px | Read: ${progress}%`);
}

// 3. Throttled Listener Attachment with Passive Flag
window.addEventListener('scroll', throttle(logScrollPosition, 300), { passive: true });""",
        None,
        "ইউজার দ্রুত স্ক্রল করলে প্রতি সেকেন্ডে ৬০টির বেশি ইভেন্ট ফায়ার হয়। থ্রটলিংয়ের মাধ্যমে একে প্রতি সেকেন্ডে মাত্র ৩ বারে সীমাবদ্ধ রাখা হয়, যা লেআউট থ্র্যাশিং দূর করে।"
    ),
    (
        3, "Beginner", "Native Responsive Image Lazy Loading",
        "একটি image-এ loading=\"lazy\" ও srcset ব্যবহার করে আধুনিক নেটিভ লেজি লোডিং টেস্ট ও পরিমাপ করুন।",
        """// Image Load Event Listener & Metrics
const lazyImg = document.querySelector('img.perf-lazy');

lazyImg.addEventListener('load', () => {
  console.log('✅ Image loaded successfully on viewport entry!');
  lazyImg.classList.add('loaded'); // CSS ফেইড-ইন ট্রানজিশন
});

lazyImg.addEventListener('error', () => {
  console.error('❌ Failed to load high-res image. Fallback triggered.');
});""",
        """<!-- High-Performance Native Responsive Lazy Image -->
<picture>
  <source srcset="hero-large.avif 1200w, hero-medium.avif 800w" type="image/avif">
  <source srcset="hero-large.webp 1200w, hero-medium.webp 800w" type="image/webp">
  <img 
    src="hero-fallback.jpg" 
    loading="lazy" 
    decoding="async"
    width="800" 
    height="450" 
    alt="Performance Dashboard Mockup"
    class="perf-lazy"
  >
</picture>""",
        "decoding=\"async\" ব্রাউজারের ডিকোডিং মেইন থ্রেড থেকে সরিয়ে নেয় এবং স্পষ্ট width/height থাকায় কোনো Layout Shift (CLS = 0) হয় না।"
    ),
    (
        4, "Beginner", "Smooth 60FPS Animation with requestAnimationFrame",
        "requestAnimationFrame() ব্যবহার করে একটি box-কে স্ক্রিনে মসৃণভাবে মুভ করান এবং ডেল্টা টাইম অনুযায়ী ফ্রেম ড্রপ পরিহার করুন।",
        """const box = document.getElementById('animated-box');
let startTimestamp = null;
const duration = 2000; // ২ সেকেন্ডে এনিমেশন শেষ হবে
const targetDistance = 400; // ৪০০ পিক্সেল ডানে সরবে

function animateBox(timestamp) {
  if (!startTimestamp) startTimestamp = timestamp;
  const elapsed = timestamp - startTimestamp;
  const progress = Math.min(elapsed / duration, 1); // ০ থেকে ১ পর্যন্ত প্রগ্রেস

  // Easing function (easeOutQuad)
  const easeProgress = 1 - (1 - progress) * (1 - progress);
  const currentX = easeProgress * targetDistance;

  // GPU-accelerated 3D Transform ব্যবহার (Reflow ও Repaint শূন্য)
  box.style.transform = `translate3d(${currentX}px, 0, 0)`;

  if (progress < 1) {
    requestAnimationFrame(animateBox); // পরবর্তী ফ্রেমের জন্য রিকোয়েস্ট
  } else {
    console.log('🏁 60FPS Smooth Animation Complete!');
  }
}

// এনিমেশন শুরু
requestAnimationFrame(animateBox);""",
        None,
        "setInterval এর বদলে rAF ব্রাউজারের 60Hz রিফ্রেশ হারের সাথে নিখুঁতভাবে টাইমিং মেলায় এবং ট্যাব ব্যাকগ্রাউন্ডে গেলে ব্যাটারি বাঁচিয়ে পজ করে।"
    ),
    (
        5, "Intermediate", "High-Performance DOM Batching with DocumentFragment",
        "১০০০টি DOM element তৈরি করুন এবং সাধারণ লুপের বদলে DocumentFragment ব্যবহার করে মাত্র ১টি Reflow ও Repaint-এ অ্যাপেন্ড করুন।",
        """const container = document.getElementById('user-list');

// ❌ Bad Approach: প্রতি লুপে অ্যাপেন্ড (১০০০ বার রিফ্লো ও রিপেইন্ট)
// for (let i = 0; i < 1000; i++) container.appendChild(createNode(i));

// ✅ Master Production Approach: DocumentFragment ব্যবহার
console.time('DocumentFragment Insertion');

const fragment = document.createDocumentFragment(); // ভার্চুয়াল মেমোরি কন্টেইনার

for (let i = 1; i <= 1000; i++) {
  const item = document.createElement('li');
  item.className = 'list-item';
  item.textContent = `Customer Record #${i} — Verified Active`;
  fragment.appendChild(item); // মেমোরিতে নোড যুক্ত (কোনো DOM রিফ্লো নেই)
}

// মূল DOM-এ মাত্র ১টি ট্রানজেকশনে ১০০০টি নোড অ্যাপেন্ড
container.appendChild(fragment);

console.timeEnd('DocumentFragment Insertion');
console.log('✅ 1,000 DOM Nodes rendered in a single Composite tick!');""",
        None,
        "DocumentFragment কোনো মূল DOM নোড নয়, এটি ইন-মেমোরি র‍্যাপার। এটি DOM ট্রি-তে যুক্ত হওয়ার পর নিজেই অদৃশ্য হয়ে যায় এবং শুধু চাইল্ড নোডগুলো সংযুক্ত থাকে।"
    ),
    (
        6, "Intermediate", "IntersectionObserver Image Lazy Loader with Skeleton Placeholder",
        "IntersectionObserver দিয়ে 'Loading...' স্কেলেটন থেকে একচুয়াল ইমেজ ভিউপোর্টে প্রবেশ করার পর লোড করুন ও আন-অবজার্ভ করুন।",
        """// 1. Observer Configuration
const observerOptions = {
  root: null, // ভিউপোর্ট ডিটেকশন
  rootMargin: '100px', // স্ক্রিনে আসার ১০০ পিক্সেল আগেই প্রি-লোড শুরু হবে
  threshold: 0.01 // ১% দৃশ্যমান হলেই ট্রিগার
};

// 2. IntersectionObserver Instance
const lazyObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      const actualSrc = img.getAttribute('data-src');

      // Placeholder থেকে আসল সোর্সে রূপান্তর
      img.src = actualSrc;
      img.onload = () => {
        img.classList.remove('skeleton-loading');
        img.classList.add('img-visible');
      };

      // মেমোরি লিক রোধে টাস্ক শেষে আন-অবজার্ভ
      observer.unobserve(img);
      console.log(`[LazyLoaded] ${actualSrc}`);
    }
  });
}, observerOptions);

// 3. Observe All Data-Src Images
document.querySelectorAll('img[data-src]').forEach(img => lazyObserver.observe(img));""",
        """<img data-src="https://images.unsplash.com/photo-perf.jpg" src="data:image/svg+xml,...placeholder..." class="skeleton-loading" width="600" height="400" alt="Product Showcase">""",
        "স্ক্রল ইভেন্ট লিসেনারের তুলনায় IntersectionObserver সম্পূর্ণ অ্যাসিনক্রোনাস এবং ব্রাউজারের কম্পোজিটর থ্রেডে চলে, ফলে মেইন থ্রেড ল্যাগ হয় না।"
    ),
    (
        7, "Intermediate", "Dynamic import() for Module Lazy-Loading & Code Splitting",
        "Dynamic import() ব্যবহার করে ইউজার বাটনে ক্লিক করলে তবেই একটি ভারী গ্রাফ চার্টিং মডিউল lazy-load করুন।",
        """const chartBtn = document.getElementById('load-chart-btn');
const chartContainer = document.getElementById('chart-container');

chartBtn.addEventListener('click', async () => {
  try {
    chartBtn.disabled = true;
    chartBtn.textContent = 'Loading Chart Engine...';

    // ডাইনামিক ইমপোর্টের মাধ্যমে মডিউল শুধু প্রয়োজনে নেটওয়ার্ক থেকে নামবে
    const { renderSalesChart } = await import('./modules/heavyChart.js');

    const sampleData = [120, 190, 300, 500, 200, 350];
    renderSalesChart(chartContainer, sampleData);

    chartBtn.textContent = '✅ Chart Rendered';
  } catch (error) {
    console.error('Failed to dynamically load chart module:', error);
    chartBtn.textContent = '❌ Loading Failed';
    chartBtn.disabled = false;
  }
});""",
        None,
        "অ্যাপ্লিকেশন বুট হওয়ার সময় পুরো চার্টিং লাইব্রেরির ৪০০KB লোড না করে ইনিশিয়াল JS বান্ডেল হালকা রাখা যায়, যা LCP এবং TBT স্কোর উল্লেখযোগ্যভাবে বাড়ায়।"
    ),
    (
        8, "Intermediate", "Debounced Search API with AbortController Stale Request Cancellation",
        "Typing -> Debounce -> fetch() -> AbortController আর্কিটেকচারে পুরাতন পেন্ডিং রিকোয়েস্ট বাতিল করার সম্পূর্ণ প্রোডাকশন সলিউশন।",
        """let currentAbortController = null;

// Debounced Search with Abort Signal
const searchProducts = debounce(async (searchTerm) => {
  if (!searchTerm) return;

  // ১. পূর্বের রিকোয়েস্ট যদি এখনো পেন্ডিং থাকে, তাকে বাতিল করুন
  if (currentAbortController) {
    currentAbortController.abort();
    console.warn('[Request Aborted]: Canceled stale pending query');
  }

  // ২. নতুন রিকোয়েস্টের জন্য ফ্রেশ কন্ট্রোলার তৈরি
  currentAbortController = new AbortController();
  const { signal } = currentAbortController;

  try {
    const response = await fetch(`/api/products?search=${encodeURIComponent(searchTerm)}`, { signal });
    const data = await response.json();
    displayResults(data.results);
    console.log(`[Search Results Loaded] Count: ${data.results.length}`);
  } catch (err) {
    if (err.name === 'AbortError') {
      console.log('ℹ️ Request successfully aborted as user typed new characters.');
    } else {
      console.error('Network Error:', err);
    }
  } finally {
    currentAbortController = null;
  }
}, 400);

document.getElementById('api-search-input').addEventListener('input', (e) => {
  searchProducts(e.target.value.trim());
});""",
        None,
        "নেটওয়ার্কের রেস কন্ডিশন (stale response overwriting latest result) সম্পূর্ণ দূর করে এবং অপ্রয়োজনীয় ব্যান্ডউইথ খরচ বন্ধ করে।"
    ),
    (
        9, "Advanced", "Multi-Route SPA Dashboard Lazy-Loader with Component Caching",
        "Dashboard-এর Overview, Analytics, Reports, Settings ট্যাবসমূহ অন-ডিমান্ড lazy-load ও মডিউল ক্যাশ করার ক্লায়েন্ট-সাইড আর্কিটেকচার।",
        """// Route-to-Module Manifest
const routeManifest = {
  overview: () => import('./views/overview.js'),
  analytics: () => import('./views/analytics.js'),
  reports: () => import('./views/reports.js'),
  settings: () => import('./views/settings.js')
};

// In-Memory Component Cache (একবার লোড হলে আর নেটওয়ার্ক কল হবে না)
const componentCache = new Map();
const contentArea = document.getElementById('dashboard-view');

async function navigateTab(routeKey) {
  if (!routeManifest[routeKey]) return;

  // ক্যাশ চেক
  if (componentCache.has(routeKey)) {
    console.log(`⚡ [Cache Hit] Rendering cached tab: ${routeKey}`);
    const cachedRender = componentCache.get(routeKey);
    cachedRender(contentArea);
    return;
  }

  // ক্যাশ মিস: নেটওয়ার্ক থেকে চাঙ্ক লোড
  contentArea.innerHTML = '<div class="loader-spinner">Loading view module...</div>';
  try {
    const module = await routeManifest[routeKey]();
    componentCache.set(routeKey, module.render); // ক্যাশে সেভ
    module.render(contentArea);
    console.log(`🌐 [Network Load] Module loaded & cached: ${routeKey}`);
  } catch (err) {
    contentArea.innerHTML = '<div class="error-msg">Failed to load view. Check connection.</div>';
  }
}

// Event Delegation on Tab Buttons
document.getElementById('tab-nav').addEventListener('click', (e) => {
  if (e.target.matches('button[data-route]')) {
    navigateTab(e.target.dataset.route);
  }
});""",
        None,
        "রুট-বেসড কোড স্প্লিটিং ইনিশিয়াল লোড সাইজ ৬০-৮০% কমিয়ে দেয় এবং ইন-মেমোরি ক্যাশিংয়ের কারণে একবার ভিজিট করা ট্যাবে ইন্সট্যান্ট সুইচিং ঘটে।"
    ),
    (
        10, "Advanced", "Off-Main-Thread 100k JSON Data Processing with Web Worker",
        "১ লক্ষ আইটেমের বিশাল JSON ডেটাসেট ফিল্টারিং ও সর্টিং করার সময় মেইন থ্রেড যাতে ১ মিলিমিটারও ফ্রিজ না হয় তার জন্য Web Worker সলিউশন।",
        """// --- MAIN THREAD SCRIPT (app.js) ---
const worker = new Worker('./workers/dataProcessor.worker.js');
const statusBadge = document.getElementById('status-badge');

// ১. বিশাল ডেটাসেট প্রসেসিংয়ের জন্য ওয়ার্কারের কাছে পাঠানো
function processDataset(heavyData, filterKeyword) {
  statusBadge.textContent = 'Processing 100k items in Background Worker...';
  console.time('Worker Processing Time');

  worker.postMessage({
    action: 'FILTER_AND_SORT',
    payload: heavyData,
    keyword: filterKeyword
  });
}

// ২. ওয়ার্কার থেকে ফলাফল রিসিভ
worker.onmessage = function(e) {
  const { sortedData, executionMs } = e.data;
  console.timeEnd('Worker Processing Time');
  statusBadge.textContent = `✅ Processed ${sortedData.length} records in ${executionMs}ms (Main thread stayed 60FPS!)`;
  renderTopResults(sortedData.slice(0, 50));
};

// --- WORKER SCRIPT (dataProcessor.worker.js) ---
// self.onmessage = function(e) {
//   const { payload, keyword } = e.data;
//   const t0 = performance.now();
//   const filtered = payload
//     .filter(item => item.name.toLowerCase().includes(keyword.toLowerCase()))
//     .sort((a, b) => b.score - a.score);
//   self.postMessage({ sortedData: filtered, executionMs: Math.round(performance.now() - t0) });
// };""",
        None,
        "মেইন থ্রেড মুক্ত থাকায় ইউজার ড্রপডাউন ওপেন করা, টাইপ করা বা স্ক্রল করার সময় কোনো লং-টাস্ক (&gt;50ms) তৈরি হয় না এবং INP স্কোর চমৎকার থাকে।"
    ),
    (
        11, "Advanced", "Programmatic Performance Profiling with User Timing API",
        "Chrome DevTools Performance প্যানেলে কাস্টম টাইমলাইন মেজারমেন্ট দেখতে performance.mark() ও performance.measure() দিয়ে কোড প্রোফাইলিং।",
        """// ১. শুরু চিহ্নিত করা
performance.mark('data-fetch-start');

async function benchmarkDataFetch() {
  const res = await fetch('https://jsonplaceholder.typicode.com/posts');
  const data = await res.json();
  
  performance.mark('data-fetch-end');
  
  // ২. ফেচিংয়ের সময় পরিমাপ
  performance.measure('Data Fetch Duration', 'data-fetch-start', 'data-fetch-end');

  // ৩. DOM রেন্ডারিং পরিমাপ
  performance.mark('dom-render-start');
  const frag = document.createDocumentFragment();
  data.slice(0, 100).forEach(post => {
    const div = document.createElement('div');
    div.textContent = post.title;
    frag.appendChild(div);
  });
  document.getElementById('benchmark-container').appendChild(frag);
  performance.mark('dom-render-end');

  performance.measure('DOM Batch Rendering Duration', 'dom-render-start', 'dom-render-end');

  // ৪. মেজারমেন্ট ফলাফল কনসোলে বিশ্লেষণ
  const measures = performance.getEntriesByType('measure');
  measures.forEach(m => console.log(`⏱️ [Metric] ${m.name}: ${m.duration.toFixed(2)} ms`));
  
  // মেমোরি পরিষ্কার
  performance.clearMarks();
  performance.clearMeasures();
}

benchmarkDataFetch();""",
        None,
        "User Timing API এর মাধ্যমে মেজারগুলো সরাসরি Chrome DevTools Performance ট্যাব-এর 'Timings' ট্র্যাকে দেখা যায়, যা বটleneck চিহ্নিত করতে অত্যন্ত কার্যকর।"
    ),
    (
        12, "Advanced", "End-to-End Production Performance Case Study & Audit Scorecard",
        "একটি ধীরগতির ইকমার্স প্রোডাক্ট পেজ অপ্টিমাইজেশনের বাস্তব কেস স্টাডি: Before vs After মেজারমেন্ট এবং স্পষ্ট অডিট রিপোর্ট।",
        """/*
================================================================================
  REAL-WORLD E-COMMERCE PERFORMANCE CASE STUDY (BEFORE VS AFTER AUDIT)
================================================================================

[PROBLEM AUDIT - BEFORE OPTIMIZATION]:
  * Initial JS Bundle: 1.8 MB (Monolithic bundle, zero code splitting)
  * Hero & Product Images: Uncompressed PNGs (Total 4.5 MB, no lazy loading)
  * Scroll Listener: Un-throttled scroll event recalculating layout on every tick
  * HTTP Cache: Missing Cache-Control headers, re-downloading static files on reload
  * Lighthouse Performance Score: 38 / 100
  * LCP (Largest Contentful Paint): 5.4 seconds (POOR ❌)
  * INP (Interaction to Next Paint): 480 ms (POOR ❌)
  * CLS (Cumulative Layout Shift): 0.38 (POOR ❌)

[OPTIMIZATION INTERVENTIONS APPLIED]:
  1. Image Pipeline: Converted all PNGs to AVIF/WebP, added width/height & loading="lazy".
  2. Code Splitting: Split checkout & heavy charts via dynamic import() (Bundle reduced to 280 KB).
  3. Layout Thrashing Elimination: Replaced synchronous DOM reads with DocumentFragment & rAF.
  4. Network & Cache: Configured Cloudflare CDN with Cache-Control: max-age=31536000, immutable.
  5. Scroll Events: Added throttle(300ms) with { passive: true } on window scroll listeners.

[VERIFICATION RESULTS - AFTER OPTIMIZATION]:
  * Initial JS Bundle: 280 KB (84% Size Reduction ✅)
  * Image Transfer Weight: 420 KB (90% Size Reduction ✅)
  * Lighthouse Performance Score: 98 / 100 (FAST 🚀)
  * LCP: 1.2 seconds (GOOD ✅ < 2.5s)
  * INP: 45 ms (GOOD ✅ < 200ms)
  * CLS: 0.02 (GOOD ✅ < 0.1)
================================================================================
*/""",
        None,
        "প্রোডাকশনে পারফরম্যান্স অপ্টিমাইজেশন শুধু একটি টেকনিক নয়; এটি নেটওয়ার্ক, বান্ডলিং, ব্রাউজার রেন্ডারিং এবং ডেটাবেস ক্যাশিংয়ের একটি সামগ্রিক ইঞ্জিনিয়ারিং কালচার।"
    )
]

for lab_num, level, title, problem, js_code, html_code, explanation in practice_solutions:
    html_parts.append(f'''    <div class="practice-item">
      <div class="card-title"><span class="badge-num">Lab #{lab_num}</span> [{level.upper()}] — {inline_format(title)}</div>
      <p class="text-p"><strong>সমস্যা ও লক্ষ্য:</strong> {inline_format(problem)}</p>
''')
    if html_code:
        html_parts.append(f'      {render_code_box(html_code, lang="html", title="HTML DOM STRUCTURE")}\n')
    if js_code:
        html_parts.append(f'      {render_code_box(js_code, lang="javascript", title=f"SOLUTION IMPLEMENTATION (LAB #{lab_num})")}\n')
    if explanation:
        html_parts.append(f'      <div class="def-box">💡 <strong>প্রোডাকশন অন্তর্দৃষ্টি:</strong> {inline_format(explanation)}</div>\n')
    html_parts.append('    </div>\n')

# Final Mental Map Card
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">33.73</span> 🎯 Final Mental Map — পারফরম্যান্স অপ্টিমাইজেশনের পূর্ণাঙ্গ মানচিত্র</div>
      <p class="text-p">পুরো Chapter 33-এর সকল মেকানিজম ও আর্কিটেকচারাল কানেকশন একসাথে:</p>
''')

final_map_ascii = """                    WEB PERFORMANCE ECOSYSTEM
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
     NETWORK                BROWSER                JAVASCRIPT
        │                      │                      │
     HTTP/2 & HTTP/3        DOM + CSSOM            Code Splitting
     CDN Edge Delivery      Critical Path          Tree Shaking
     Brotli Compression     Layout & Reflow        Minification
     Cache-Control Headers  Paint & GPU Composite  Debounce & Throttle
     Preload & Prefetch     DocumentFragment       Web Workers
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
                               ▼
                        USER EXPERIENCE
                               │
            ┌──────────────────┼──────────────────┐
            │                  │                  │
           LCP                INP                CLS
       (Loading Speed)    (Responsiveness)   (Visual Stability)
          < 2.5s              < 200ms             < 0.10
        [GOOD ✓]             [GOOD ✓]            [GOOD ✓]"""

html_parts.append(f'      {render_ascii_box(final_map_ascii, title="FULL PERFORMANCE ARCHITECTURE MAP")}\n')

html_parts.append('''      <div class="def-box" style="margin-top: 6px;">
        🏆 <strong>এক লাইনে Chapter 33:</strong> Web Performance &amp; Optimization হলো ব্রাউজারের নেটওয়ার্ক, ক্রিটিক্যাল রেন্ডারিং পাথ, জাভাস্ক্রিপ্ট বান্ডেল, মেমোরি ও ইভেন্ট এক্সিকিউশনকে এমনভাবে অপ্টিমাইজ করা যাতে অ্যাপ্লিকেশন চোখের পলকে লোড হয়, ফ্রেম ড্রপ ছাড়া রেসপন্ড করে এবং কম রিসোর্সে সর্বোচ্চ ইউজার এক্সপেরিয়েন্স দেয়।
      </div>

      <div class="section-subhead" style="margin-top: 8px;">🔗 Curriculum Progression: Chapter 32 → 33 → 34</div>
''')

roadmap_conn_ascii = """Chapter 32: Advanced Browser APIs
       ↓
Browser-এর গভীর প্ল্যাটফর্ম সক্ষমতা (Workers, Observers, Sockets, IndexedDB)
       ↓
Chapter 33: Web Performance & Optimization (THIS CHAPTER)
       ↓
ব্রাউজারের সেই সক্ষমতা সর্বোচ্চ গতি, রিসোর্স সাশ্রয় ও 60FPS-এ পরিচালনা
       ↓
Chapter 34: NPM & Modern JavaScript Tooling
       ↓
প্যাকেজ ম্যানেজমেন্ট, বিল্ড টুলস (Vite/Webpack), ট্রান্সপাইলার ও অটোমেটেড ওয়ার্কফ্লো"""

html_parts.append(f'      {render_ascii_box(roadmap_conn_ascii, title="ROADMAP CONTINUITY PIPELINE")}\n')
html_parts.append('    </div>\n')

# Document Footer
html_parts.append('''  </div>
</body>
</html>''')

# Write complete HTML
output_html_path = r'c:\Users\User\Desktop\Note-Book\Code\Chapter-33-Web-Performance-Optimization.html'
os.makedirs(os.path.dirname(output_html_path), exist_ok=True)

with open(output_html_path, 'w', encoding='utf-8') as f:
    f.write(''.join(html_parts))

print(f"Successfully generated HTML: {output_html_path} (Total size: {len(''.join(html_parts))} bytes)")
