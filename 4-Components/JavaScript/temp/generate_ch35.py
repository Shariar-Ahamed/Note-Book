import re
import sys
import html
import os

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Read raw markdown
with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-35.md', 'r', encoding='utf-8') as f:
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
            ('DOM_BUILTIN', r'\b(?:console|window|document|process|module|exports|require|jest|test|it|describe|expect|beforeEach|afterEach|beforeAll|afterAll|vi|screen|render|fireEvent|userEvent)\b'),
            ('ASYNC_METHOD', r'\b(?:then|catch|finally|resolve|reject|toBe|toEqual|toContain|toBeNull|toBeUndefined|toBeDefined|toThrow|toHaveBeenCalled|toHaveBeenCalledTimes|toHaveBeenCalledWith|mockResolvedValue|mockResolvedValueOnce|mockReturnValue|fn|spyOn|fetch|json|get|post)\b'),
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
    elif lang in ('bash', 'sh', 'shell'):
        lines = esc_all.split('\n')
        out_lines = []
        for l in lines:
            if l.strip().startswith('#'):
                out_lines.append(f'<span class="syn-com">{l}</span>')
                continue
            # Flags / Options first (must be standalone tokens)
            line_hl = re.sub(r'(?<=^|\s)(--[a-zA-Z0-9_-]+|-[a-zA-Z0-9]+)(?=\s|$)', r'<span style="color:#fde047; font-weight:600;">\1</span>', l)
            # Commands & tools (standalone tokens)
            line_hl = re.sub(r'(?<=^|\s)(npm|npx|node|git|jest|vitest|playwright)(?=\s|$)', r'<span style="color:#38bdf8; font-weight:700;">\1</span>', line_hl)
            # Subcommands (standalone tokens)
            line_hl = re.sub(r'(?<=^|\s)(install|test|run|coverage|init)(?=\s|$)', r'<span style="color:#4ade80; font-weight:600;">\1</span>', line_hl)
            out_lines.append(line_hl)
        return '\n'.join(out_lines)
    elif lang == 'json':
        # JSON syntax highlighting (values first, keys last so tags are not affected)
        t = re.sub(r':\s*(&quot;.*?&quot;)', r': <span style="color:#4ade80;">\1</span>', esc_all)
        t = re.sub(r':\s*\b(true|false|null)\b', r': <span style="color:#c084fc; font-weight:600;">\1</span>', t)
        t = re.sub(r':\s*(\d+(?:\.\d+)?)\s*(?=[,\n\r]|$)', r': <span style="color:#fb923c;">\1</span>', t)
        t = re.sub(r'(&quot;[a-zA-Z0-9_$-]+&quot;)\s*:', r'<span style="color:#38bdf8; font-weight:600;">\1</span>:', t)
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
    
    # 3. Testing Levels & Pyramids (Amber / Gold)
    t = re.sub(r'\b(Unit Testing|Integration Testing|End-to-End Testing|E2E|Component Testing|Regression Testing|Testing Pyramid|UNIT|INTEGRATION|ASSERTIONS|MOCKING|COVERAGE|TDD|CI/CD)\b', r'<span style="color: #fde047; font-weight: 700;">\1</span>', t)
    
    # 4. Testing Frameworks & Matchers (Lavender / Violet)
    t = re.sub(r'\b(Jest|Vitest|Testing Library|Playwright|Cypress|toBe|toEqual|toThrow|describe|test|expect)\b', r'<span style="color: #c084fc; font-weight: 700;">\1</span>', t)
    
    # 5. Success / Passed States (Emerald / Mint)
    t = re.sub(r'\b(PASS|Passed|Success|Match Expected|Fast|Reliable|Green|Refactor)\b', r'<span style="color: #34d399; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(✓|✔)', r'<span style="color: #4ade80; font-weight: bold;">\1</span>', t)
    
    # 6. Failure / Error States (Rose / Crimson)
    t = re.sub(r'\b(FAIL|Failed|Error|Bug|Crash|Flaky Test|Regression|Red|Slow|Expensive)\b', r'<span style="color: #f43f5e; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(✗|✘|X)', r'<span style="color: #f43f5e; font-weight: bold;">\1</span>', t)
    
    return t

def render_ascii_box(text, title=None):
    if not title:
        if 'Pyramid' in text or 'E2E' in text:
            title = "TESTING PYRAMID & LEVEL DISTRIBUTION"
        elif 'TDD' in text or 'Red' in text or 'Green' in text:
            title = "TEST-DRIVEN DEVELOPMENT (TDD) CYCLE"
        elif 'Assertion' in text or 'expect' in text:
            title = "TEST ASSERTION & EXECUTION FLOW"
        elif 'Workflow' in text or 'CI/CD' in text:
            title = "AUTOMATED TESTING & CI/CD PIPELINE"
        elif 'Unit vs Integration' in text:
            title = "UNIT VS INTEGRATION ARCHITECTURE"
        else:
            title = "TESTING ARCHITECTURE & EXECUTION FLOW"
            
    colorized = colorize_ascii(text)
    return f'''<div class="ascii-tree-container">
  <div class="ascii-tree-header">🧪 {title}</div>
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

# Part Banners configuration for Chapter 35
PART_BANNERS = {
    1: ("Part 01", "Testing Fundamentals, Motivations & Automated Testing (35.1 – 35.5)"),
    6: ("Part 02", "Testing Pyramid & Test Types (Unit, Integration, E2E, Regression) (35.6 – 35.12)"),
    13: ("Part 03", "Test Cases, Scenarios, Assertions & Jest Setup (35.13 – 35.18)"),
    19: ("Part 04", "Core Jest Matchers (toBe, toEqual, toContain, Truthy/Falsy) (35.19 – 35.28)"),
    29: ("Part 05", "Test Suites (describe) & Lifecycle Hooks (Setup & Teardown) (35.29 – 35.34)"),
    35: ("Part 06", "Asynchronous Testing: Promises, Async/Await & Errors (35.35 – 35.37)"),
    38: ("Part 07", "Mocking Architecture, Spy Functions & Test Doubles (35.38 – 35.42)"),
    43: ("Part 08", "Code Coverage Metrics & Testing Library Paradigm (35.43 – 35.47)"),
    48: ("Part 09", "End-to-End Testing with Playwright & Testing Pyramid (35.48 – 35.50)"),
    51: ("Part 10", "Test-Driven Development (TDD), BDD & Test Strategies (35.51 – 35.59)"),
    60: ("Part 11", "Writing Clean Tests, Independence & Flaky Test Prevention (35.60 – 35.63)"),
    64: ("Part 12", "Full-Stack Testing, CI/CD Pipeline & Complete Mini Project (35.64 – 35.72)"),
    73: ("Part 13", "Must Know Testing Pillars, Quick Cheat Sheet, 6 Practice Labs & Final Mental Map"),
}

# Split markdown into sections
raw_sections = re.split(r'\n(?=# 35\.\d+\s*(?:—|-)?\s*)', raw_md)
print(f"Total raw section chunks parsed: {len(raw_sections)}")

# Separate Section 72 from Must Know, Cheat Sheet, Practice Set, and Final Mental Map
sec72_full = raw_sections[72]
sec72_subparts = re.split(r'\n(?=# (?:🔥\s*MUST|🧠\s*Quick|📝\s*Practice|🎯\s*Final))', sec72_full)

sec72_clean = sec72_subparts[0].strip()
mustknow_clean = sec72_subparts[1].strip() if len(sec72_subparts) > 1 else ""
cheatsheet_clean = sec72_subparts[2].strip() if len(sec72_subparts) > 2 else ""
practice_clean = sec72_subparts[3].strip() if len(sec72_subparts) > 3 else ""
mentalmap_clean = sec72_subparts[4].strip() if len(sec72_subparts) > 4 else ""

html_parts = []

# Document Header & CSS Tokens
html_parts.append('''<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter 35 — Testing JavaScript | JavaScript Master Study Documentation</title>
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
      #sec-35-1 {
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
          <span class="chapter-badge">Chapter 35</span>
        </div>
      </div>
      <div class="banner-sub">TESTING JAVASCRIPT, UNIT &amp; INTEGRATION TESTING, JEST, VITEST, MOCKING, TDD &amp; CI/CD AUTOMATION</div>
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">Total Modules</div>
          <div class="meta-val">72 Modules + 6 Practice Labs</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Curriculum Part</div>
          <div class="meta-val">Part 29 — Quality Assurance &amp; Testing</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Core Mechanics</div>
          <div class="meta-val">Unit, Integration, E2E, Mocks &amp; TDD</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Reference Standard</div>
          <div class="meta-val">Jest / Vitest / Playwright 2026</div>
        </div>
      </div>
    </header>

    <!-- Chapter Opening Statement (Page 1 Balance) -->
    <div class="opening-card">
      <div class="opening-title">
        <span>🧪</span> Testing JavaScript — নির্ভরযোগ্যতা, বাগ প্রতিরোধ ও আত্মবিশ্বাসী রিফ্যাক্টরিং
      </div>
      <p class="text-p">
        প্রফেশনাল সফটওয়্যার ডেভেলপমেন্টে কোড শুধু কাজ করলেই যথেষ্ট নয়—ভবিষ্যতে নতুন ফিচার যুক্ত করার পর পূর্বের কোনো কার্যকারিতা ভেঙে পড়ল কিনা (Regression) তা স্বয়ংক্রিয়ভাবে নিশ্চিত করাই টেস্টিংয়ের লক্ষ্য। এই চ্যাপ্টারে আমরা <strong>Unit Testing, Integration Testing, E2E Testing, Testing Pyramid, Jest/Vitest Assertions, Setup &amp; Teardown Hooks, Async Testing, Mocking, Code Coverage, Test-Driven Development (TDD)</strong> এবং CI/CD টেস্ট অটোমেশন পাইপলাইন শিখব।
      </p>
      <div class="roadmap-grid">
        <div class="roadmap-item"><span>📌</span> 1. Testing Fundamentals</div>
        <div class="roadmap-item"><span>📌</span> 2. Testing Pyramid</div>
        <div class="roadmap-item"><span>📌</span> 3. Jest &amp; Assertions</div>
        <div class="roadmap-item"><span>📌</span> 4. Matchers &amp; Suites</div>
        <div class="roadmap-item"><span>📌</span> 5. Async Testing</div>
        <div class="roadmap-item"><span>📌</span> 6. Mocking &amp; Spies</div>
        <div class="roadmap-item"><span>📌</span> 7. Code Coverage</div>
        <div class="roadmap-item"><span>📌</span> 8. TDD Red-Green-Refactor</div>
        <div class="roadmap-item"><span>📌</span> 9. E2E with Playwright</div>
        <div class="roadmap-item"><span>📌</span> 10. CI/CD Pipeline</div>
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
                    res.append(f'      {render_code_box(code_content, lang="bash", title="TERMINAL TEST COMMAND")}\n')
                elif cur_lang == 'json':
                    res.append(f'      {render_code_box(code_content, lang="json", title="PACKAGE JSON TEST CONFIG")}\n')
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
            res.append(f'      <div class="section-subhead" style="font-size: 11px; color: var(--navy-deep); border-left: 2px solid var(--blue-accent); padding-left: 5px;">🧪 {inline_format(sub_title)}</div>\n')
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

# Process sections 1 to 71
for idx in range(1, 72):
    sec_text = raw_sections[idx].strip()
    pb = check_part_banner(idx)
    if pb:
        html_parts.append(f'    {pb}\n')
        
    sec_lines = sec_text.split('\n')
    header_line = sec_lines[0]
    m_head = re.search(r'# (?:🔥\s*|⚠️\s*)?(35\.\d+)\s*(?:—|-)?\s*(.*)', header_line)
    if m_head:
        sec_num = m_head.group(1)
        sec_title = m_head.group(2)
    else:
        sec_num = f'35.{idx}'
        sec_title = header_line.replace('#', '').strip()
        
    card_extra = ''
    if idx == 1:
        card_extra = ' id="sec-35-1"'
        
    html_parts.append(f'''    <div class="study-card"{card_extra}>
      <div class="card-title"><span class="badge-num">{sec_num}</span> {inline_format(sec_title)}</div>
''')
    
    body_text = '\n'.join(sec_lines[1:]).strip()
    html_parts.append(process_section_body(body_text))
    html_parts.append('    </div>\n')

# Process Section 72 (Cleaned of subparts)
pb72 = check_part_banner(72)
if pb72:
    html_parts.append(f'    {pb72}\n')
    
sec72_lines = sec72_clean.split('\n')
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">35.72</span> একটি Complete Mini Project — সম্পূর্ণ টেস্ট স্যুট</div>
''')
html_parts.append(process_section_body('\n'.join(sec72_lines[1:]).strip()))
html_parts.append('    </div>\n')

# Part 13 Banner & Section 35.73: MUST KNOW
pb13 = check_part_banner(73)
if pb13:
    html_parts.append(f'    {pb13}\n')

html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">35.73</span> 🔥 MUST KNOW — জাভাস্ক্রিপ্ট টেস্টিংয়ের ১০টি প্রধান স্তম্ভ</div>
      <p class="text-p">প্রোডাকশন মানের নির্ভরযোগ্য অ্যাপ্লিকেশন তৈরিতে এই ১০টি টেস্ট আর্কিটেকচার নীতি অপরিহার্য:</p>
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 5px;">
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #0284c7; font-size: 10px; margin-bottom: 3px;">📌 1. Test Pyramid &amp; Matchers</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li><strong>Unit Testing (70%):</strong> স্বতন্ত্র পিওর ফাংশন টেস্ট</li>
            <li><strong>Integration Testing (20%):</strong> একাধিক মডিউল ও এপিআই ইন্টারঅ্যাকশন</li>
            <li><strong>toBe vs toEqual:</strong> প্রিমিটিভ ভ্যালু বনাম ডিপ অবজেক্ট তুলনা</li>
            <li><strong>toThrow:</strong> এক্সেপশন ও এরর হ্যান্ডলিং নিখুঁতভাবে যাচাই</li>
          </ul>
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #059669; font-size: 10px; margin-bottom: 3px;">📌 2. Async, Mocks &amp; Lifecycle</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li><strong>Async/Await Testing:</strong> প্রমিজ রেজলভ ও রিজেক্ট হ্যান্ডলিং</li>
            <li><strong>Setup &amp; Teardown:</strong> beforeEach/afterEach দিয়ে স্টেট রিসেট</li>
            <li><strong>Mock Functions:</strong> নেটওয়ার্ক ও ডেটাবেস কল বিচ্ছিন্নকরণ</li>
            <li><strong>Test Independence:</strong> একটি টেস্টের স্টেট যেন অন্যটিকে প্রভাবিত না করে</li>
          </ul>
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #7c3aed; font-size: 10px; margin-bottom: 3px;">📌 3. TDD, Coverage &amp; CI/CD</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li><strong>TDD Cycle:</strong> Red (Fail) → Green (Pass) → Refactor</li>
            <li><strong>Code Coverage:</strong> Statements, Branches, Functions কভারেজ</li>
            <li><strong>Testing Library:</strong> ইমপ্লিমেন্টেশন ডিটেইল নয়, ইউজার আচরণ টেস্ট</li>
            <li><strong>CI/CD Gate:</strong> গিটহাবে পুশ করার পর স্বয়ংক্রিয় টেস্ট রান</li>
          </ul>
        </div>
      </div>
    </div>
''')

# Quick Cheat Sheet Card
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">35.74</span> 🧠 Quick Cheat Sheet — টেস্টিং সিনট্যাক্স ও ম্যাচার সারসংক্ষেপ</div>
''')
cheat_table = '''| Matcher / Hook | Syntax Example | Primary Use Case |
| :--- | :--- | :--- |
| **toBe** | `expect(add(1, 2)).toBe(3)` | প্রিমিটিভ ভ্যালু (Primitive equality `===`) পরীক্ষা |
| **toEqual** | `expect(user).toEqual({ id: 1 })` | অবজেক্ট বা অ্যারের গভীর সমতা (Deep equality) |
| **toBeTruthy** | `expect(isValid).toBeTruthy()` | ট্রুথি ভ্যালু নিশ্চিতকরণ (`Boolean(val) === true`) |
| **toBeFalsy** | `expect(hasError).toBeFalsy()` | ফলসি ভ্যালু নিশ্চিতকরণ (`null, undefined, 0, ""` ইত্যাদি) |
| **toContain** | `expect(fruits).toContain('apple')` | অ্যারে বা স্ট্রিংয়ে উপাদান বিদ্যমান থাকা যাচাই |
| **toBeNull** | `expect(res).toBeNull()` | ভ্যালু ঠিক `null` কিনা তা পরীক্ষা |
| **toBeDefined** | `expect(val).toBeDefined()` | ভ্যারিয়েবল ডিফাইন করা আছে কিনা (`!== undefined`) |
| **toThrow** | `expect(() => fn()).toThrow("Error")` | ফাংশন কাঙ্ক্ষিত এরর থ্রো করে কিনা যাচাই |
| **describe** | `describe('Auth Service', () => {})` | সম্পর্কিত টেস্টগুলোকে একটি সুসংগঠিত ব্লকে গ্রুপ করা |
| **test / it** | `test('should calculate tax', () => {})` | একটি স্বতন্ত্র টেস্ট কেস তৈরি করা |
| **beforeEach** | `beforeEach(() => { resetDB(); })` | প্রতিটি একক টেস্ট রানের পূর্বে স্টেট রিসেট করা |
| **afterEach** | `afterEach(() => { jest.clearAllMocks(); })` | প্রতিটি টেস্ট শেষে ক্লিনআপ ও মক ক্লিয়ার করা |
| **beforeAll** | `beforeAll(async () => { await connect(); })` | পুরো টেস্ট স্যুটের শুরুতে মাত্র একবার রান |
| **afterAll** | `afterAll(async () => { await close(); })` | সম্পূর্ণ টেস্ট স্যুট সমাপ্তির পর কানেকশন বন্ধ |
| **jest.fn()** | `const mock = jest.fn()` | ফেক ফাংশন তৈরি এবং কল কাউন্ট/আর্গুমেন্ট পর্যবেক্ষণ |
| **mockResolvedValue** | `mockFetch.mockResolvedValue({ ok: true })` | অ্যাসিনক্রোনাস প্রমিজ রিটার্ন সিমুলেশন |
| **npm test** | `npm test` / `npm test -- --coverage` | সম্পূর্ণ টেস্ট স্যুট ও কোড কভারেজ রিপোর্ট তৈরি |'''
html_parts.append(f'      {render_table(cheat_table)}\n')
html_parts.append('    </div>\n')

# 6 Hands-on Practice Labs with Complete Solutions
html_parts.append('''    <div class="part-banner">Part 13.1 — 6 Hands-On Practice Labs with Complete Production Solutions</div>
''')

practice_solutions = [
    (
        1, "Beginner", "Unit Test Suite for add(a, b) Function (5 Test Cases)",
        "`add(a, b)` ফাংশনের জন্য ৫টি বৈচিত্র্যময় ও নির্ভুল ইউনিট টেস্ট কেস লিখুন যা পজিটিভ, নেগেটিভ, ফ্লোটিং পয়েন্ট, জিরো এবং স্ট্রিং টাইপ এরর টেস্ট কভার করে।",
        """// src/math.js
export function add(a, b) {
  if (typeof a !== 'number' || typeof b !== 'number') {
    throw new TypeError('Both arguments must be numbers');
  }
  return a + b;
}""",
        """// tests/math.test.js
import { describe, test, expect } from '@jest/globals';
import { add } from '../src/math.js';

describe('Math Module: add(a, b)', () => {
  test('Case 1: adds two positive integers correctly', () => {
    expect(add(5, 7)).toBe(12);
  });

  test('Case 2: handles negative numbers properly', () => {
    expect(add(-10, -5)).toBe(-15);
    expect(add(-10, 20)).toBe(10);
  });

  test('Case 3: adds floating point numbers with precision', () => {
    expect(add(0.1, 0.2)).toBeCloseTo(0.3, 5); // ফ্লোটিং পয়েন্ট নির্ভুলতা
  });

  test('Case 4: returns correct value when adding with zero', () => {
    expect(add(42, 0)).toBe(42);
    expect(add(0, 0)).toBe(0);
  });

  test('Case 5: throws TypeError when invalid types are supplied', () => {
    expect(() => add('5', 10)).toThrow(TypeError);
    expect(() => add(null, 5)).toThrow('Both arguments must be numbers');
  });
});""",
        "ফ্লোটিং পয়েন্ট নাম্বারের ক্ষেত্রে toBe() এর বদলে toBeCloseTo() ব্যবহার করা উচিত, কারণ জাভাস্ক্রিপ্টে 0.1 + 0.2 = 0.30000000000000004 হয়ে থাকে।"
    ),
    (
        2, "Beginner", "Exhaustive Parity Test Suite for isEven(number)",
        "`isEven(number)` ফাংশনটির জন্য ২, ৪, ৭, ০, -২ ইনপুটের জন্য পূর্ণাঙ্গ টেস্ট কেস লিখুন।",
        """// src/utils.js
export function isEven(number) {
  if (!Number.isInteger(number)) {
    throw new Error('Input must be an integer');
  }
  return number % 2 === 0;
}""",
        """// tests/utils.test.js
import { describe, test, expect } from '@jest/globals';
import { isEven } from '../src/utils.js';

describe('Parity Logic: isEven(number)', () => {
  test('returns true for positive even numbers (2 and 4)', () => {
    expect(isEven(2)).toBe(true);
    expect(isEven(4)).toBe(true);
  });

  test('returns false for positive odd numbers (7)', () => {
    expect(isEven(7)).toBe(false);
  });

  test('returns true for zero (0 is an even number)', () => {
    expect(isEven(0)).toBe(true);
  });

  test('returns true for negative even numbers (-2)', () => {
    expect(isEven(-2)).toBe(true);
  });

  test('handles edge cases: throws error on non-integer input', () => {
    expect(() => isEven(3.14)).toThrow('Input must be an integer');
  });
});""",
        "গাণিতিক নিয়মানুযায়ী ০ এবং ঋণাত্মক জোড় সংখ্যা (যেমন -২, -৪) সবই বৈধ জোড় সংখ্যা। টেস্টে এ ধরনের বাউন্ডারি ও নেগেটিভ কেস যাচাই করা জরুরি।"
    ),
    (
        3, "Intermediate", "Boundary & Negative Value Testing for isAdult(age)",
        "`isAdult(age)` ফাংশনটির বাউন্ডারি টেস্ট লিখুন: ১৭, ১৮, ১৯, ০ এবং ঋণাত্মক বয়সের জন্য।",
        """// src/auth.js
export function isAdult(age) {
  if (typeof age !== 'number' || age < 0) {
    throw new RangeError('Age must be a non-negative number');
  }
  return age >= 18;
}""",
        """// tests/auth.test.js
import { describe, test, expect } from '@jest/globals';
import { isAdult } from '../src/auth.js';

describe('Boundary Testing: isAdult(age)', () => {
  test('Boundary - 1 (age 17): should return false', () => {
    expect(isAdult(17)).toBe(false);
  });

  test('Exact Boundary (age 18): should return true', () => {
    expect(isAdult(18)).toBe(true);
  });

  test('Boundary + 1 (age 19): should return true', () => {
    expect(isAdult(19)).toBe(true);
  });

  test('Lower Extreme (age 0): should return false', () => {
    expect(isAdult(0)).toBe(false);
  });

  test('Negative Boundary: throws RangeError on negative age', () => {
    expect(() => isAdult(-1)).toThrow(RangeError);
    expect(() => isAdult(-25)).toThrow('Age must be a non-negative number');
  });
});""",
        "বাউন্ডারি ভ্যালু এনালাইসিস (BVA) হলো বাগ শনাক্ত করার অন্যতম কার্যকর পদ্ধতি। ১৮ বছর শর্ত হলে ১৭, ১৮ ও ১৯ এই তিনটি মান টেস্ট করা বাধ্যতামূলক।"
    ),
    (
        4, "Intermediate", "Exception Handling & Balance Deduction Test for withdraw()",
        "`withdraw(balance, amount)` ফাংশনে অপর্যাপ্ত ব্যালেন্স থাকলে এরর থ্রো করা এবং পর্যাপ্ত ব্যালেন্সে সঠিক অবশিষ্ট টাকা রিটার্ন করা টেস্ট করুন।",
        """// src/bank.js
export function withdraw(balance, amount) {
  if (amount <= 0) {
    throw new Error('Withdrawal amount must be greater than zero');
  }
  if (amount > balance) {
    throw new Error('Insufficient balance');
  }
  return balance - amount;
}""",
        """// tests/bank.test.js
import { describe, test, expect } from '@jest/globals';
import { withdraw } from '../src/bank.js';

describe('Banking Service: withdraw(balance, amount)', () => {
  test('successfully deducts balance when funds are sufficient', () => {
    const initialBalance = 1000;
    const withdrawAmount = 400;
    const remaining = withdraw(initialBalance, withdrawAmount);
    expect(remaining).toBe(600);
  });

  test('allows full withdrawal to zero balance', () => {
    expect(withdraw(500, 500)).toBe(0);
  });

  test('throws "Insufficient balance" error when withdrawal exceeds funds', () => {
    expect(() => {
      withdraw(100, 250);
    }).toThrow('Insufficient balance');
  });

  test('throws error when withdrawing zero or negative amount', () => {
    expect(() => withdraw(100, 0)).toThrow('Withdrawal amount must be greater than zero');
    expect(() => withdraw(100, -50)).toThrow('Withdrawal amount must be greater than zero');
  });
});""",
        "toThrow() দিয়ে এরর টেস্ট করার সময় ফাংশনটিকে সরাসরি কল না করে একটি অ্যারো ফাংশনের মধ্যে র‍্যাপ করে পাস করতে হয়: `() => withdraw(...)`।"
    ),
    (
        5, "Advanced", "Asynchronous API Testing with Jest Mock Functions (fetchUser)",
        "বাস্তব নেটওয়ার্ক কল ছাড়াই `fetchUser(id)` ফাংশনের সাকসেস ও ফেইলিউর সিনারিও মক রেসপন্স দিয়ে টেস্ট করার সম্পূর্ণ প্রোডাকশন সলিউশন।",
        """// src/userService.js
export async function fetchUser(userId) {
  const response = await fetch(`https://api.example.com/users/${userId}`);
  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`);
  }
  return await response.json();
}""",
        """// tests/userService.test.js
import { describe, test, expect, beforeEach, afterEach, jest } from '@jest/globals';
import { fetchUser } from '../src/userService.js';

// গ্লোবাল ফেচ মক করা
const originalFetch = global.fetch;

describe('UserService: fetchUser(id) with API Mocking', () => {
  beforeEach(() => {
    global.fetch = jest.fn(); // ফেক ফেচ ফাংশন তৈরি
  });

  afterEach(() => {
    global.fetch = originalFetch; // টেস্ট শেষে মূল ফেচ ফিরিয়ে দেওয়া
  });

  test('resolves user profile successfully on 200 OK', async () => {
    const mockUserData = { id: 101, name: 'Tanvir Ahamed', role: 'Engineer' };
    
    global.fetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => mockUserData
    });

    const user = await fetchUser(101);

    expect(global.fetch).toHaveBeenCalledTimes(1);
    expect(global.fetch).toHaveBeenCalledWith('https://api.example.com/users/101');
    expect(user).toEqual(mockUserData);
  });

  test('rejects with descriptive error when API returns 404', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
      status: 404
    });

    await expect(fetchUser(999)).rejects.toThrow('API Error: 404');
  });
});""",
        "টেস্টিংয়ে কখনোই বাস্তব প্রোডাকশন বা থার্ড-পার্টি এপিআই কল করা উচিত নয়; মকিংয়ের মাধ্যমে নেটওয়ার্কের বিলম্ব ও খরচ ছাড়াই টেস্ট অতি দ্রুত ও নির্ভরযোগ্য হয়।"
    ),
    (
        6, "Advanced", "Full Component Test Plan & Automated Testing Library Suite",
        "Login কম্পোনেন্টের ৮টি গুরুত্বপূর্ণ টেস্ট সিনারিও (Valid, Invalid Password, Empty Fields, Loading State, Error Banner, Redirect) বিশিষ্ট টেস্ট প্ল্যান ও কোড।",
        """/*
================================================================================
  LOGIN COMPONENT PRODUCTION TEST PLAN SPECIFICATION
================================================================================
1. [Happy Path]: ইউজার সঠিক ইমেইল ও পাসওয়ার্ড দিলে লোডিং স্টেট দেখাবে এবং ড্যাশবোর্ডে রিডাইরেক্ট করবে।
2. [Invalid Password]: ভুল পাসওয়ার্ডে "Invalid credentials" এরর ব্যানার প্রদর্শিত হবে।
3. [Empty Email]: ইমেইল ফাঁকা রেখে সাবমিট করলে "Email is required" ভ্যালিডেশন টেক্সট আসবে।
4. [Empty Password]: পাসওয়ার্ড ফাঁকা রেখে সাবমিট করলে "Password is required" সতর্কবার্তা আসবে।
5. [Invalid Email Format]: "@" ছাড়া টেক্সট দিলে "Invalid email address" ভ্যালিডেশন দেখাবে।
6. [Loading State]: রিকোয়েস্ট চলাকালীন সাবমিট বাটন ডিসেবল হবে এবং স্পিনার দেখাবে।
7. [Network Failure]: সার্ভার ডাউন থাকলে "Unable to connect to server" এরর ব্যানার আসবে।
8. [Post-Login Redirect]: সফল লগন শেষে রিঅ্যাক্ট রাউটার /dashboard পাথে নেভিগেট করবে।
================================================================================
*/""",
        """// tests/LoginComponent.test.js (Testing Library Paradigm)
import { describe, test, expect, jest } from '@jest/globals';

describe('Login Component Automated Suite', () => {
  test('validates required fields on empty submit', () => {
    // সিমুলেশন: ইমেইল ও পাসওয়ার্ড ছাড়া সাবমিট
    const validateForm = (email, pass) => {
      const errors = {};
      if (!email) errors.email = 'Email is required';
      if (!pass) errors.password = 'Password is required';
      return errors;
    };

    const errors = validateForm('', '');
    expect(errors.email).toBe('Email is required');
    expect(errors.password).toBe('Password is required');
  });

  test('authenticates valid credentials and triggers navigation', async () => {
    const mockAuthService = jest.fn().mockResolvedValue({ token: 'jwt-xyz-123' });
    const mockNavigate = jest.fn();

    async function handleLogin(email, password) {
      const res = await mockAuthService(email, password);
      if (res.token) mockNavigate('/dashboard');
    }

    await handleLogin('dev@example.com', 'SecurePass123!');

    expect(mockAuthService).toHaveBeenCalledWith('dev@example.com', 'SecurePass123!');
    expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
  });
});""",
        "কম্পোনেন্ট টেস্টিংয়ে ইন্টারনাল স্টেট টেস্ট না করে ইউজার যা স্ক্রিনে দেখে ও করে (ইউজার ইনপুট টাইপ, বাটন ক্লিক) তার ফলাফল টেস্ট করাই বেস্ট প্র্যাকটিস।"
    )
]

for lab_num, level, title, problem, code_1, code_2, explanation in practice_solutions:
    html_parts.append(f'''    <div class="practice-item">
      <div class="card-title"><span class="badge-num">Lab #{lab_num}</span> [{level.upper()}] — {inline_format(title)}</div>
      <p class="text-p"><strong>সমস্যা ও লক্ষ্য:</strong> {inline_format(problem)}</p>
''')
    if code_1:
        lang_1 = 'bash' if code_1.startswith('#') else 'javascript'
        title_1 = "SOURCE MODULE / SPECIFICATION" if lang_1 == 'javascript' else "EXECUTION COMMANDS"
        html_parts.append(f'      {render_code_box(code_1, lang=lang_1, title=title_1)}\n')
    if code_2:
        html_parts.append(f'      {render_code_box(code_2, lang="javascript", title=f"TEST IMPLEMENTATION (LAB #{lab_num})")}\n')
    if explanation:
        html_parts.append(f'      <div class="def-box">💡 <strong>প্রোডাকশন অন্তর্দৃষ্টি:</strong> {inline_format(explanation)}</div>\n')
    html_parts.append('    </div>\n')

# Final Mental Map Card
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">35.75</span> 🎯 Final Mental Map — জাভাস্ক্রিপ্ট টেস্টিংয়ের পূর্ণাঙ্গ মানচিত্র</div>
      <p class="text-p">পুরো Chapter 35-এর টেস্টিং আর্কিটেকচার ও ওয়ার্কফ্লো একসাথে:</p>
''')

final_map_ascii = """                    JAVASCRIPT TESTING ECOSYSTEM
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
     UNIT TESTS          INTEGRATION TESTS          E2E TESTS
   (70% - Fast)            (20% - Medium)          (10% - Slow)
         │                       │                       │
  Pure Functions          API Endpoints & DB       User Journey
  Isolated Logic          Component + Hooks        Full Browser
  Jest / Vitest           Supertest / RTL          Playwright
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                                 ▼
                     CORE TESTING MECHANICS
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
    ASSERTIONS                MOCKING                COVERAGE
         │                       │                       │
   toBe / toEqual          jest.fn()               Statements
   toThrow / toContain     mockResolvedValue       Branches
   toBeCloseTo             Test Doubles & Spies    Functions / Lines
                                 │
                                 ▼
                    TDD & PRODUCTION PIPELINE
                                 │
                   Red → Green → Refactor
                                 │
                    Automated CI/CD Gates
                    (Zero Broken Production)"""

html_parts.append(f'      {render_ascii_box(final_map_ascii, title="FULL TESTING ARCHITECTURE MAP")}\n')

html_parts.append('''      <div class="def-box" style="margin-top: 6px;">
        🏆 <strong>এক লাইনে Chapter 35:</strong> Testing হলো সফটওয়্যারের প্রতিটি লজিক্যাল ইউনিট, মডিউল ইন্টিগ্রেশন ও ইউজার জার্নিকে স্বয়ংক্রিয় অ্যাসার্শন ও মকিংয়ের মাধ্যমে এমনভাবে সুরক্ষিত করা যাতে নতুন কোড যোগ বা রিফ্যাক্টরিংয়ের পরেও সিস্টেম ১০০% বিশ্বস্ত ও বাগ-মুক্ত থাকে।
      </div>

      <div class="section-subhead" style="margin-top: 8px;">🔗 Curriculum Progression: Chapter 34 → 35 → 36</div>
''')

roadmap_conn_ascii = """Chapter 34: NPM & Modern JavaScript Tooling
       ↓
প্যাকেজ ম্যানেজমেন্ট, প্রজেক্ট স্ক্যাফোল্ডিং, বান্ডলিং (Vite) ও ওয়ার্কফ্লো অটোমেশন
       ↓
Chapter 35: Testing JavaScript (THIS CHAPTER)
       ↓
Unit Test, Integration Test, Jest/Vitest, Mocking, Coverage, TDD & CI/CD
       ↓
Chapter 36: Modern ECMAScript / ES2020+ Features
       ↓
Optional Chaining, Nullish Coalescing, Top-level Await, WeakRef, Temporal API"""

html_parts.append(f'      {render_ascii_box(roadmap_conn_ascii, title="ROADMAP CONTINUITY PIPELINE")}\n')
html_parts.append('    </div>\n')

# Document Footer
html_parts.append('''  </div>
</body>
</html>''')

# Write complete HTML
output_html_path = r'c:\Users\User\Desktop\Note-Book\Code\Chapter-35-Testing-JavaScript.html'
os.makedirs(os.path.dirname(output_html_path), exist_ok=True)

with open(output_html_path, 'w', encoding='utf-8') as f:
    f.write(''.join(html_parts))

print(f"Successfully generated HTML: {output_html_path} (Total size: {len(''.join(html_parts))} bytes)")
