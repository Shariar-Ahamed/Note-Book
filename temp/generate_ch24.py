import re
import sys
import html
import subprocess
import os

sys.stdout.reconfigure(encoding='utf-8')

# Read source markdown
with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-24.md', 'r', encoding='utf-8') as f:
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
        ('PRIVATE_FIELD', r'#[a-zA-Z_$][a-zA-Z0-9_$]*'),
        ('KEYWORD', r'\b(?:for|while|do|break|continue|if|else|let|const|var|function|return|switch|case|default|of|in|new|typeof|delete|this|super|class|extends|static|instanceof|try|catch|finally|throw|await|async|yield|debugger|import|export|from|as|get|set)\b'),
        ('BOOL_NULL', r'\b(?:true|false|null|undefined|NaN)\b'),
        ('CLASS_NAME', r'\b[A-Z][a-zA-Z0-9_$]*\b'),
        ('DOM_BUILTIN', r'\b(?:console|window|document|Math|Object|Array|Date|JSON|Promise|Error|Map|Set|WeakMap|WeakSet|Reflect|Proxy)\b'),
        ('METHOD_CALL', r'\b[a-zA-Z_$][a-zA-Z0-9_$]*(?=\s*\()'),
        ('NUMBER', r'\b\d+(?:\.\d+)?\b'),
        ('OTHER', r'[^\s\w]+|\w+|\s+'),
    ]
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
    
    out = []
    for mo in re.finditer(tok_regex, code_str, flags=re.MULTILINE):
        kind = mo.lastgroup
        val = mo.group()
        esc = html.escape(val)
        
        # Check if token is marked as invalid
        if invalid_token and (invalid_token in val or val == invalid_token):
            out.append(f'<span class="invalid-token">{esc}</span>')
            continue
            
        if kind in ('COMMENT_MULTI', 'COMMENT_LINE'):
            out.append(f'<span class="tok-comment">{esc}</span>')
        elif kind in ('STRING_TMPL', 'STRING_DBL', 'STRING_SGL'):
            out.append(f'<span class="tok-string">{esc}</span>')
        elif kind == 'KEYWORD':
            out.append(f'<span class="tok-kw">{esc}</span>')
        elif kind == 'BOOL_NULL':
            out.append(f'<span class="tok-bool">{esc}</span>')
        elif kind == 'CLASS_NAME':
            out.append(f'<span class="tok-class">{esc}</span>')
        elif kind == 'PRIVATE_FIELD':
            out.append(f'<span class="tok-priv">{esc}</span>')
        elif kind == 'DOM_BUILTIN':
            out.append(f'<span class="tok-builtin">{esc}</span>')
        elif kind == 'METHOD_CALL':
            out.append(f'<span class="tok-fn">{esc}</span>')
        elif kind == 'NUMBER':
            out.append(f'<span class="tok-num">{esc}</span>')
        else:
            out.append(esc)
    return ''.join(out)

def render_code_box(code_text, lang='javascript', title=None, is_invalid=False, invalid_token=None, is_correct=False):
    code_text = code_text.strip()
    highlighted = highlight_js(code_text, invalid_token=invalid_token)
    
    badge_cls = 'badge-js'
    badge_label = 'JavaScript'
    box_extra_cls = ''
    header_extra = ''
    
    if is_invalid:
        box_extra_cls = ' code-box-error'
        badge_cls = 'badge-error'
        badge_label = '❌ Invalid / Error'
        header_extra = '<span class="status-tag status-error">Syntax / Runtime Error</span>'
    elif is_correct:
        box_extra_cls = ' code-box-correct'
        badge_cls = 'badge-success'
        badge_label = '✅ Correct / Valid'
        header_extra = '<span class="status-tag status-correct">Valid OOP Pattern</span>'

    display_title = title if title else badge_label

    return f'''<div class="code-box{box_extra_cls}">
    <div class="code-header">
        <div class="code-dots">
            <span class="dot dot-red"></span>
            <span class="dot dot-yellow"></span>
            <span class="dot dot-green"></span>
            <span class="code-title">{display_title}</span>
            {header_extra}
        </div>
        <div class="code-actions">
            <span class="code-badge {badge_cls}">{badge_label}</span>
            <button class="copy-btn" onclick="copyCode(this)">Copy</button>
        </div>
    </div>
    <pre><code class="language-{lang}">{highlighted}</code></pre>
</div>'''

def render_ascii_box(text, title="ASCII Concept Architecture"):
    text = html.escape(text.strip())
    return f'''<div class="ascii-tree-container">
    <div class="ascii-tree-header">
        <span class="tree-icon">🧭</span>
        <span class="tree-title">{title}</span>
    </div>
    <pre class="ascii-content">{text}</pre>
</div>'''

def render_output_box(text):
    text = html.escape(text.strip())
    return f'''<div class="output-box">
    <div class="output-header">
        <span class="output-icon">▶</span>
        <span class="output-title">Console Output</span>
    </div>
    <pre class="output-content">{text}</pre>
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
        
    html_out = ['<div class="table-wrap"><table class="data-table"><thead><tr>']
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
pattern = r'\n(?=# (?:(?:🔥\s*)?24\.\d+|🧠\s*Quick Cheat Sheet|📝\s*Practice Set|🎯\s*Final Mental Map))'
raw_sections = re.split(pattern, raw_md)

print(f'Total raw sections parsed: {len(raw_sections)}')

# Process Section 0 (Master Banner + Opening Card)
sec0 = raw_sections[0].strip()

# Extract learning goals from sec0
goals_match = re.search(r'# 🎯 Chapter 24 Learning Goals\s*([\s\S]*?)$', sec0)
learning_goals = []
if goals_match:
    for g in re.findall(r'^\*\s*(.*)$', goals_match.group(1), re.M):
        learning_goals.append(g.strip())

# Build Header & Styles
html_parts = []
html_parts.append('''<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chapter 24 — OOP & JavaScript Classes | JavaScript Master Study Documentation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Hind+Siliguri:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-body: #0a0d14;
            --bg-card: #111722;
            --bg-card-hover: #151d2c;
            --border-card: #1f293d;
            --border-focus: #38bdf8;
            --text-main: #e2e8f0;
            --text-muted: #94a3b8;
            --text-dim: #64748b;
            --accent-blue: #38bdf8;
            --accent-purple: #c084fc;
            --accent-emerald: #34d399;
            --accent-amber: #fbbf24;
            --accent-rose: #f43f5e;
            --code-bg: #070a0f;
            --code-border: #1e293b;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-body);
            color: var(--text-main);
            font-family: 'Inter', 'Hind Siliguri', sans-serif;
            line-height: 1.6;
            font-size: 14.5px;
            -webkit-font-smoothing: antialiased;
        }

        .doc-page {
            max-width: 1060px;
            margin: 0 auto;
            padding: 24px 20px;
        }

        /* Master Banner */
        .master-banner {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
            border: 1px solid #312e81;
            border-radius: 12px;
            padding: 12px 18px;
            margin-bottom: 8px;
            box-shadow: 0 4px 12px -6px rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
        }

        .banner-left {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .banner-logo {
            width: 48px;
            height: 48px;
            background: #f7df1e;
            color: #000;
            font-weight: 800;
            font-size: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(247, 223, 30, 0.35);
        }

        .banner-titles h1 {
            font-size: 20px;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.02em;
            margin-bottom: 3px;
        }

        .banner-titles h2 {
            font-size: 13.5px;
            font-weight: 500;
            color: #93c5fd;
        }

        .banner-right {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: flex-end;
        }

        .pill-badge {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.14);
            color: #e2e8f0;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 11.5px;
            font-weight: 600;
            letter-spacing: 0.01em;
        }

        .pill-highlight {
            background: rgba(56, 189, 248, 0.15);
            border-color: rgba(56, 189, 248, 0.4);
            color: #38bdf8;
        }

        /* Opening Card */
        .opening-card {
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 12px;
            padding: 10px 14px;
            margin-bottom: 8px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        }

        .opening-title {
            font-size: 16px;
            font-weight: 700;
            color: var(--accent-blue);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .opening-desc {
            font-size: 13.5px;
            color: #cbd5e1;
            margin-bottom: 14px;
            line-height: 1.6;
        }

        .goals-flex {
            display: flex;
            flex-wrap: wrap;
            gap: 4px 6px;
            margin-top: 6px;
        }

        .goal-tag {
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid #1e293b;
            padding: 2px 7px;
            border-radius: 4px;
            font-size: 10px;
            color: #cbd5e1;
            white-space: nowrap;
        }

        .goal-tag::before {
            content: "✓ ";
            color: #34d399;
            font-weight: 700;
        }

        /* Part Banners */
        .part-banner {
            background: linear-gradient(90deg, #1e1b4b 0%, #0f172a 100%);
            border-left: 4px solid var(--accent-purple);
            border-radius: 8px;
            padding: 10px 16px;
            margin: 12px 0 8px 0;
            font-size: 15px;
            font-weight: 700;
            color: #f1f5f9;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
            page-break-after: avoid !important;
            break-after: avoid !important;
        }

        /* Study Cards */
        .study-card {
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 16px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.25);
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }

        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.07);
        }

        .card-title {
            font-size: 15.5px;
            font-weight: 700;
            color: #f8fafc;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .card-badge {
            font-size: 11px;
            font-weight: 600;
            background: rgba(99, 102, 241, 0.15);
            color: #a5b4fc;
            border: 1px solid rgba(99, 102, 241, 0.3);
            padding: 2px 8px;
            border-radius: 4px;
        }

        .card-subheading {
            font-size: 13.5px;
            font-weight: 700;
            color: #38bdf8;
            margin: 14px 0 6px 0;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .card-body p {
            margin-bottom: 10px;
            color: #cbd5e1;
            font-size: 13.5px;
        }

        .card-body ul, .card-body ol {
            margin: 8px 0 12px 20px;
            color: #cbd5e1;
            font-size: 13.5px;
        }

        .card-body li {
            margin-bottom: 4px;
        }

        /* Code Boxes */
        .code-box {
            background: var(--code-bg);
            border: 1px solid var(--code-border);
            border-radius: 8px;
            margin: 10px 0 14px 0;
            overflow: hidden;
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }

        .code-box-error {
            border-color: rgba(239, 68, 68, 0.4) !important;
            background: rgba(239, 68, 68, 0.02) !important;
        }

        .code-box-correct {
            border-color: rgba(34, 197, 94, 0.4) !important;
            background: rgba(34, 197, 94, 0.02) !important;
        }

        .code-header {
            background: #0d121c;
            border-bottom: 1px solid #1e293b;
            padding: 6px 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .code-dots {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .dot {
            width: 9px;
            height: 9px;
            border-radius: 50%;
            display: inline-block;
        }

        .dot-red { background: #ef4444; }
        .dot-yellow { background: #eab308; }
        .dot-green { background: #22c55e; }

        .code-title {
            font-size: 11px;
            font-family: 'Fira Code', monospace;
            color: #94a3b8;
            margin-left: 8px;
        }

        .status-tag {
            font-size: 10.5px;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 4px;
            margin-left: 8px;
        }

        .status-error {
            background: rgba(239, 68, 68, 0.2);
            color: #fca5a5;
            border: 1px solid rgba(239, 68, 68, 0.4);
        }

        .status-correct {
            background: rgba(34, 197, 94, 0.2);
            color: #86efac;
            border: 1px solid rgba(34, 197, 94, 0.4);
        }

        .code-actions {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .code-badge {
            font-size: 10px;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 4px;
            text-transform: uppercase;
        }

        .badge-js {
            background: rgba(247, 223, 30, 0.15);
            color: #f7df1e;
        }

        .badge-error {
            background: rgba(239, 68, 68, 0.2);
            color: #ef4444;
        }

        .badge-success {
            background: rgba(34, 197, 94, 0.2);
            color: #22c55e;
        }

        .copy-btn {
            background: transparent;
            border: 1px solid #334155;
            color: #94a3b8;
            font-size: 10px;
            padding: 2px 7px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .copy-btn:hover {
            background: #1e293b;
            color: #e2e8f0;
        }

        pre {
            padding: 12px 16px;
            margin: 0;
            overflow-x: hidden !important;
            white-space: pre-wrap !important;
            word-break: break-word !important;
            font-family: 'Fira Code', monospace;
            font-size: 12.5px;
            line-height: 1.5;
        }

        code {
            font-family: 'Fira Code', monospace;
        }

        p code, li code {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid #273549;
            color: #38bdf8;
            padding: 1px 5px;
            border-radius: 4px;
            font-size: 12px;
        }

        /* Invalid token highlighting */
        .invalid-token {
            text-decoration: underline wavy #ef4444 !important;
            text-decoration-skip-ink: none !important;
            color: #fca5a5 !important;
            font-weight: 700 !important;
            background: rgba(239, 68, 68, 0.18) !important;
            padding: 0 3px !important;
            border-radius: 3px !important;
        }

        /* Syntax colors */
        .tok-kw { color: #ff7b72; font-weight: 600; }
        .tok-class { color: #ffa657; font-weight: 600; }
        .tok-priv { color: #f0883e; font-weight: 600; }
        .tok-fn { color: #7ee787; }
        .tok-string { color: #a5d6a7; }
        .tok-num { color: #79c0ff; }
        .tok-bool { color: #79c0ff; font-weight: 600; }
        .tok-builtin { color: #d2a8ff; font-weight: 600; }
        .tok-comment { color: #94a3b8; font-style: italic; }

        /* ASCII Container */
        .ascii-tree-container {
            background: #090e17;
            border: 1px solid #1e293b;
            border-left: 3px solid #38bdf8;
            border-radius: 8px;
            margin: 12px 0 16px 0;
            overflow: hidden;
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }

        .ascii-tree-header {
            background: #0d1522;
            border-bottom: 1px solid #1e293b;
            padding: 6px 12px;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 11px;
            font-weight: 600;
            color: #94a3b8;
        }

        .ascii-content {
            color: #38bdf8;
            font-family: 'Fira Code', monospace;
            font-size: 12px;
            line-height: 1.4;
            padding: 12px 14px;
            margin: 0;
            white-space: pre-wrap !important;
            word-break: break-word !important;
            overflow-x: hidden !important;
        }

        /* Output Box */
        .output-box {
            background: #070a0e;
            border: 1px solid #1f2937;
            border-left: 3px solid #22c55e;
            border-radius: 8px;
            margin: 10px 0 14px 0;
            overflow: hidden;
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }

        .output-header {
            background: #0b111a;
            border-bottom: 1px solid #1f2937;
            padding: 5px 12px;
            font-size: 11px;
            font-weight: 600;
            color: #86efac;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .output-content {
            color: #e2e8f0;
            font-family: 'Fira Code', monospace;
            font-size: 12px;
            padding: 10px 14px;
            margin: 0;
            white-space: pre-wrap !important;
            word-break: break-word !important;
            overflow-x: hidden !important;
        }

        /* Table */
        .table-wrap {
            overflow-x: auto;
            margin: 12px 0 16px 0;
            border: 1px solid var(--border-card);
            border-radius: 8px;
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }

        .data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12.5px;
            text-align: left;
        }

        .data-table th {
            background: #151f30;
            color: #f8fafc;
            padding: 9px 12px;
            font-weight: 600;
            border-bottom: 1px solid #273549;
        }

        .data-table td {
            padding: 8px 12px;
            border-bottom: 1px solid #1a2332;
            color: #cbd5e1;
        }

        .data-table tr:nth-child(even) {
            background: rgba(255, 255, 255, 0.02);
        }

        /* Callout Boxes */
        .callout-box {
            padding: 12px 16px;
            border-radius: 8px;
            margin: 12px 0;
            font-size: 13.5px;
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }

        .callout-info {
            background: rgba(56, 189, 248, 0.08);
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-left: 3px solid #38bdf8;
            color: #e2e8f0;
        }

        .callout-warn {
            background: rgba(245, 158, 11, 0.08);
            border: 1px solid rgba(245, 158, 11, 0.25);
            border-left: 3px solid #f59e0b;
            color: #e2e8f0;
        }

        /* Practice Problem Item */
        .practice-item {
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 16px;
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }

        .practice-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 10px;
        }

        .practice-level {
            font-size: 11px;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 4px;
        }

        .level-beginner { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
        .level-intermediate { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
        .level-advanced { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }

        /* Print Strict Settings */
        @media print {
            @page {
                size: A4;
                margin: 8mm 10mm;
            }

            body {
                background: #0a0d14 !important;
                color: #e2e8f0 !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }

            .doc-page {
                max-width: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
            }

            .copy-btn {
                display: none !important;
            }

            /* Page 1 Strict Balance */
            #sec-24-1 {
                page-break-after: always !important;
                break-after: page !important;
                margin-bottom: 0 !important;
            }

            .study-card, .practice-item, .code-box, pre, .ascii-tree-container, .table-wrap, .callout-box {
                page-break-inside: avoid !important;
                break-inside: avoid !important;
            }
        }
    </style>
</head>
<body>
<div class="doc-page">

    <!-- MASTER BANNER -->
    <header class="master-banner">
        <div class="banner-left">
            <div class="banner-logo">JS</div>
            <div class="banner-titles">
                <h1>Chapter 24 — OOP &amp; JavaScript Classes</h1>
                <h2>JavaScript Master Study Documentation • ECMAScript 2026 Standard</h2>
            </div>
        </div>
        <div class="banner-right">
            <span class="pill-badge pill-highlight">50 Core Modules</span>
            <span class="pill-badge">OOP 4 Pillars</span>
            <span class="pill-badge">Private Fields (#)</span>
            <span class="pill-badge">Prototypes &amp; Extends</span>
            <span class="pill-badge pill-highlight">Practice Lab</span>
        </div>
    </header>

    <!-- OPENING STATEMENT CARD -->
    <div class="opening-card">
        <div class="opening-title">
            <span>🎯</span> Chapter 24 Learning Goals &amp; Architecture Roadmap
        </div>
        <p class="opening-desc">
            OOP (Object-Oriented Programming) হলো আধুনিক সফটওয়্যার ইঞ্জিনিয়ারিংয়ের মূল ভিত্তি। বিশেষ করে <strong>React, Node.js, Express, NestJS, এবং large-scale enterprise application</strong> ডেভেলপমেন্টে পরিষ্কার ডেটা মডেলিং এবং মডুলার কোড স্ট্রাকচার সাজাতে ক্লাস এবং অবজেক্টের কনসেপ্ট অপরিহার্য। এই চ্যাপ্টারে আমরা একদম গ্রাউন্ড লেভেল থেকে ইন্টারনাল প্রোটোটাইপ মেকানিজম পর্যন্ত নিখুঁতভাবে শিখব।
        </p>
        <div class="goals-flex">
''')

for g in learning_goals:
    html_parts.append(f'            <span class="goal-tag">{inline_format(g)}</span>\n')

html_parts.append('''        </div>
    </div>
''')

# Now process sections 1 to 50
current_part = 0

def get_part_banner(num):
    if num == 1:
        return '<div class="part-banner part-banner-1">Part 01 — OOP Fundamentals, Objects &amp; Class Syntax (24.1 – 24.10)</div>'
    elif num == 11:
        return '<div class="part-banner">Part 02 — Methods, Properties, Accessors &amp; Encapsulation (24.11 – 24.23)</div>'
    elif num == 24:
        return '<div class="part-banner">Part 03 — Inheritance, Polymorphism, Abstraction &amp; Composition (24.24 – 24.33)</div>'
    elif num == 34:
        return '<div class="part-banner">Part 04 — Under the Hood: Prototypes, Class Fields &amp; Practical Architecture (24.34 – 24.43)</div>'
    elif num == 44:
        return '<div class="part-banner">Part 05 — Common Mistakes, Edge Cases &amp; Mental Models (24.44 – 24.49)</div>'
    elif num == 50:
        return '<div class="part-banner">Part 06 — OOP Mastery: Must Know, Quick Cheat Sheet, Practice Lab &amp; Mental Map</div>'
    return None

for idx in range(1, 51):
    sec_text = raw_sections[idx].strip()
    
    # Check part banner
    pb = get_part_banner(idx)
    if pb:
        html_parts.append(f'    {pb}\n')
        
    # Extract header
    sec_lines = sec_text.split('\n')
    header_line = sec_lines[0]
    m_head = re.search(r'# (?:🔥\s*)?(24\.\d+)\s*—\s*(.*)', header_line)
    if m_head:
        sec_num = m_head.group(1)
        sec_title = m_head.group(2)
    else:
        sec_num = f'24.{idx}'
        sec_title = header_line.replace('#', '').strip()
        
    # Special card id & style for 24.1
    card_extra = ''
    if idx == 1:
        card_extra = ' id="sec-24-1"'
        
    html_parts.append(f'''    <div class="study-card"{card_extra}>
        <div class="card-header">
            <h3 class="card-title"><span>📌</span> {sec_num} — {inline_format(sec_title)}</h3>
            <span class="card-badge">Module {sec_num}</span>
        </div>
        <div class="card-body">
''')
    
    # Process section body
    body_text = '\n'.join(sec_lines[1:]).strip()
    
    # Handle common mistakes specifically for Semantic Code Correctness Policy
    if idx in [44, 45, 46, 47, 48]:
        if idx == 44:
            invalid_c = "class Student {}\n\nconst student = Student();"
            correct_c = "class Student {}\n\nconst student = new Student();"
            html_parts.append(f'''            <p>Class constructor কখনো <code>new</code> কীওয়ার্ড ছাড়া সরাসরি ফাংশনের মতো কল করা যায় না। এভাবে কল করলে <code>TypeError</code> ছুঁড়ে দেয়।</p>
            {render_code_box(invalid_c, is_invalid=True, invalid_token='Student()', title='ভুল পদ্ধতি: new কীওয়ার্ড ছাড়া কল')}
            <div class="output-box" style="border-left-color: #ef4444;">
                <div class="output-header" style="color: #fca5a5;"><span class="output-icon">✖</span> Runtime Error</div>
                <pre class="output-content">TypeError: Class constructor Student cannot be invoked without 'new'</pre>
            </div>
            <p><strong>সঠিক সমাধান:</strong> অবজেক্ট ইনস্ট্যান্স তৈরি করতে সর্বদা <code>new</code> ব্যবহার করুন।</p>
            {render_code_box(correct_c, is_correct=True, title='সঠিক পদ্ধতি: new ব্যবহার')}
''')
        elif idx == 45:
            invalid_c = "class Animal {\n    constructor(name) {\n        this.name = name;\n    }\n}\n\nclass Dog extends Animal {\n    constructor(name, breed) {\n        this.breed = breed;\n    }\n}"
            correct_c = "class Animal {\n    constructor(name) {\n        this.name = name;\n    }\n}\n\nclass Dog extends Animal {\n    constructor(name, breed) {\n        super(name);\n        this.breed = breed;\n    }\n}"
            html_parts.append(f'''            <p>Inheritance ব্যবহার করার সময় চাইল্ড ক্লাসের <code>constructor</code>-এ <code>this</code> অ্যাক্সেস করার পূর্বে অবশ্যই প্যারেন্ট ক্লাসের <code>super()</code> কল করতে হবে।</p>
            {render_code_box(invalid_c, is_invalid=True, invalid_token='this.breed = breed;', title='ভুল পদ্ধতি: super() না ডেকে this অ্যাক্সেস')}
            <div class="output-box" style="border-left-color: #ef4444;">
                <div class="output-header" style="color: #fca5a5;"><span class="output-icon">✖</span> Runtime ReferenceError</div>
                <pre class="output-content">ReferenceError: Must call super constructor in derived class before accessing 'this'</pre>
            </div>
            <p><strong>সঠিক সমাধান:</strong> প্যারেন্ট কনস্ট্রাক্টরে প্যারামিটার পাস করতে প্রথমে <code>super(...)</code> কল করুন।</p>
            {render_code_box(correct_c, is_correct=True, title='সঠিক পদ্ধতি: super(name) কল')}
''')
        elif idx == 46:
            invalid_c = "class User {\n    #password = \"12345\";\n}\n\nconst user = new User();\nconsole.log(user.#password);"
            correct_c = "class User {\n    #password = \"12345\";\n\n    verifyPassword(input) {\n        return this.#password === input;\n    }\n}\n\nconst user = new User();\nconsole.log(user.verifyPassword(\"12345\")); // true"
            html_parts.append(f'''            <p>Private field (<code>#field</code>) ক্লাসের বাইরে থেকে সরাসরি ডট নোটেশনে অ্যাক্সেস করা যায় না। এটি করলে সিনট্যাক্স এরর দেয়।</p>
            {render_code_box(invalid_c, is_invalid=True, invalid_token='user.#password', title='ভুল পদ্ধতি: ক্লাসের বাইরে Private Field অ্যাক্সেস')}
            <div class="output-box" style="border-left-color: #ef4444;">
                <div class="output-header" style="color: #fca5a5;"><span class="output-icon">✖</span> SyntaxError</div>
                <pre class="output-content">SyntaxError: Private field '#password' must be declared in an enclosing class</pre>
            </div>
            <p><strong>সঠিক সমাধান:</strong> ক্লাসের নিজস্ব মেথড বা গেটারের মাধ্যমে প্রাইভেট ডেটা ভ্যালিডেট বা এক্সেস করুন।</p>
            {render_code_box(correct_c, is_correct=True, title='সঠিক পদ্ধতি: মেথড বা গেটারের মাধ্যমে এক্সেস')}
''')
        elif idx == 47:
            invalid_c = "class Test {\n    static hello() {\n        console.log(\"Hello\");\n    }\n}\n\nconst test = new Test();\ntest.hello();"
            correct_c = "class Test {\n    static hello() {\n        console.log(\"Hello\");\n    }\n}\n\nTest.hello(); // Hello"
            html_parts.append(f'''            <p>Static method সরাসরি ক্লাসের প্রপার্টি, এটি ইনস্ট্যান্স অবজেক্টে উত্তরাধিকারসূত্রে থাকে না। অবজেক্ট ইনস্ট্যান্স দিয়ে কল করলে TypeError দেয়।</p>
            {render_code_box(invalid_c, is_invalid=True, invalid_token='test.hello()', title='ভুল পদ্ধতি: অবজেক্ট দিয়ে Static মেথড কল')}
            <div class="output-box" style="border-left-color: #ef4444;">
                <div class="output-header" style="color: #fca5a5;"><span class="output-icon">✖</span> TypeError</div>
                <pre class="output-content">TypeError: test.hello is not a function</pre>
            </div>
            <p><strong>সঠিক সমাধান:</strong> সরাসরি ক্লাসের নাম ধরে কল করুন: <code>Test.hello()</code></p>
            {render_code_box(correct_c, is_correct=True, title='সঠিক পদ্ধতি: ক্লাসের নাম ধরে কল')}
''')
        elif idx == 48:
            invalid_c = "class Student {\n    constructor(name) {\n        name = name; // প্যারামিটার নিজের উপর অ্যাসাইন হচ্ছে, ইনস্ট্যান্সে নয়!\n    }\n}\n\nconst s = new Student(\"Shariar\");\nconsole.log(s.name); // undefined"
            correct_c = "class Student {\n    constructor(name) {\n        this.name = name; // ইনস্ট্যান্স অবজেক্টে প্রপার্টি সেট হলো\n    }\n}\n\nconst s = new Student(\"Shariar\");\nconsole.log(s.name); // 'Shariar'"
            html_parts.append(f'''            <p>কনস্ট্রাক্টরের ভেতর <code>this.property = value</code> না লিখলে অবজেক্টের প্রপার্টি ইনিশিয়ালাইজ হয় না; শুধু লোকাল ভেরিয়েবল অ্যাসাইন হয়।</p>
            {render_code_box(invalid_c, is_invalid=True, invalid_token='name = name;', title='ভুল পদ্ধতি: this ছাড়া নাম অ্যাসাইন')}
            <div class="output-box" style="border-left-color: #ef4444;">
                <div class="output-header" style="color: #fca5a5;"><span class="output-icon">▶</span> Output Mismatch</div>
                <pre class="output-content">undefined</pre>
            </div>
            <p><strong>সঠিক সমাধান:</strong> অবজেক্টের প্রপার্টি সেট করতে সর্বদা <code>this.name</code> ব্যবহার করুন।</p>
            {render_code_box(correct_c, is_correct=True, title='সঠিক পদ্ধতি: this.name ব্যবহার')}
''')
    else:
        # Standard section rendering
        # Tokenize body into paragraphs, headings, code blocks, ascii diagrams
        chunks = re.split(r'(```[\s\S]*?```|###[^\n]+)', body_text)
        for ch in chunks:
            ch_str = ch.strip()
            if not ch_str:
                continue
            if ch_str.startswith('```'):
                cb_match = re.match(r'```([a-zA-Z0-9_-]*)\n([\s\S]*?)```', ch_str)
                if cb_match:
                    clang = cb_match.group(1).lower()
                    code_val = cb_match.group(2)
                    if clang in ('javascript', 'js'):
                        html_parts.append(render_code_box(code_val))
                    elif clang == 'text':
                        if any(c in code_val for c in ['│', '┌', '└', '├', '──', '─', '↓', '→', 'OOP']):
                            html_parts.append(render_ascii_box(code_val))
                        else:
                            # It's output or simple text
                            html_parts.append(render_output_box(code_val))
                    else:
                        html_parts.append(render_code_box(code_val, lang=clang, title=clang.upper()))
            elif ch_str.startswith('###'):
                sub_title = ch_str.replace('###', '').strip()
                if sub_title.lower() == 'output':
                    pass # Output is rendered via box
                else:
                    html_parts.append(f'            <div class="card-subheading"><span>🔹</span> {inline_format(sub_title)}</div>\n')
            else:
                # Normal paragraph or bullets
                lines = ch_str.split('\n')
                p_acc = []
                in_list = False
                for l in lines:
                    ls = l.strip()
                    if not ls:
                        continue
                    if ls.startswith('* ') or ls.startswith('- '):
                        if not in_list:
                            if p_acc:
                                html_parts.append(f'            <p>{inline_format(" ".join(p_acc))}</p>\n')
                                p_acc = []
                            html_parts.append('            <ul>\n')
                            in_list = True
                        html_parts.append(f'                <li>{inline_format(ls[2:])}</li>\n')
                    else:
                        if in_list:
                            html_parts.append('            </ul>\n')
                            in_list = False
                        p_acc.append(ls)
                if in_list:
                    html_parts.append('            </ul>\n')
                if p_acc:
                    html_parts.append(f'            <p>{inline_format(" ".join(p_acc))}</p>\n')
                    
    html_parts.append('''        </div>
    </div>
''')

# Section 51: Quick Cheat Sheet
sec51 = raw_sections[51].strip()
m_table = re.search(r'(\|[\s\S]*\|)', sec51)
if m_table:
    html_parts.append(f'''    <div class="study-card">
        <div class="card-header">
            <h3 class="card-title"><span>🧠</span> Quick Cheat Sheet — Class &amp; OOP Syntax Reference</h3>
            <span class="card-badge">Summary</span>
        </div>
        <div class="card-body">
            <p>JavaScript Class এবং Object-Oriented Programming এর দ্রুত রেফারেন্সের জন্য সম্পূর্ণ সিনট্যাক্স টেবিল:</p>
            {render_table(m_table.group(1))}
        </div>
    </div>
''')

# Section 52: Practice Set
sec52 = raw_sections[52].strip()
practice_solutions = [
    {
        "id": "Practice 1",
        "level": "Beginner",
        "level_cls": "level-beginner",
        "title": "Car Class — Brand, Model, Year & showInfo() Method",
        "req": "<code>Car</code> নামে একটি ক্লাস বানান যাতে <code>brand</code>, <code>model</code>, <code>year</code> প্রোপার্টি থাকবে এবং <code>showInfo()</code> মেথড গাড়ির সম্পূর্ণ বিবরণ প্রিন্ট করবে।",
        "code": """class Car {
    constructor(brand, model, year) {
        this.brand = brand;
        this.model = model;
        this.year = year;
    }

    showInfo() {
        console.log(`Car Info: ${this.brand} ${this.model} (${this.year})`);
    }
}

// Verification
const myCar = new Car("Toyota", "Camry", 2024);
myCar.showInfo();""",
        "output": "Car Info: Toyota Camry (2024)"
    },
    {
        "id": "Practice 2",
        "level": "Beginner",
        "level_cls": "level-beginner",
        "title": "Student Class — Name, ID, Department & introduce() Method",
        "req": "<code>Student</code> নামে একটি ক্লাস বানান যাতে <code>name</code>, <code>id</code>, <code>department</code> প্রোপার্টি থাকবে এবং <code>introduce()</code> মেথড শিক্ষার্থীর পরিচয় প্রিন্ট করবে।",
        "code": """class Student {
    constructor(name, id, department) {
        this.name = name;
        this.id = id;
        this.department = department;
    }

    introduce() {
        console.log(`Hello, I am ${this.name}, ID: ${this.id}, Department of ${this.department}.`);
    }
}

// Verification
const s1 = new Student("Rahim Ahmed", "CSE-1024", "Computer Science");
s1.introduce();""",
        "output": "Hello, I am Rahim Ahmed, ID: CSE-1024, Department of Computer Science."
    },
    {
        "id": "Practice 3",
        "level": "Beginner",
        "level_cls": "level-beginner",
        "title": "Rectangle Class — Width, Height, area() & perimeter() Calculation",
        "req": "<code>Rectangle</code> নামে একটি ক্লাস বানান যার <code>width</code> ও <code>height</code> প্রোপার্টি থাকবে এবং আয়তক্ষেত্রের ক্ষেত্রফল ও পরিসীমা নির্ণয়ের জন্য <code>area()</code> ও <code>perimeter()</code> মেথড থাকবে।",
        "code": """class Rectangle {
    constructor(width, height) {
        this.width = width;
        this.height = height;
    }

    area() {
        return this.width * this.height;
    }

    perimeter() {
        return 2 * (this.width + this.height);
    }
}

// Verification
const rect = new Rectangle(10, 5);
console.log("Area:", rect.area());
console.log("Perimeter:", rect.perimeter());""",
        "output": "Area: 50\nPerimeter: 30"
    },
    {
        "id": "Practice 4",
        "level": "Intermediate",
        "level_cls": "level-intermediate",
        "title": "BankAccount with Private #balance, Deposit & Withdraw Validations",
        "req": "<code>BankAccount</code> ক্লাস বানান যাতে ব্যালেন্স প্রাইভেট (<code>#balance</code>) থাকবে এবং <code>deposit(amount)</code>, <code>withdraw(amount)</code>, ও <code>getBalance()</code> মেথডের মাধ্যমে সুরক্ষিতভাবে লেনদেন করা যাবে।",
        "code": """class BankAccount {
    #balance;

    constructor(initialBalance = 0) {
        this.#balance = initialBalance >= 0 ? initialBalance : 0;
    }

    deposit(amount) {
        if (amount > 0) {
            this.#balance += amount;
            console.log(`Deposited $${amount}. New balance: $${this.#balance}`);
        } else {
            console.log("Deposit amount must be positive.");
        }
    }

    withdraw(amount) {
        if (amount <= 0) {
            console.log("Invalid withdrawal amount.");
        } else if (amount > this.#balance) {
            console.log("Insufficient funds!");
        } else {
            this.#balance -= amount;
            console.log(`Withdrawn $${amount}. Remaining balance: $${this.#balance}`);
        }
    }

    getBalance() {
        return this.#balance;
    }
}

// Verification
const account = new BankAccount(500);
account.deposit(200);
account.withdraw(150);
console.log("Final Balance:", account.getBalance());
// console.log(account.#balance); // ❌ SyntaxError (Fully Protected)""",
        "output": "Deposited $200. New balance: $700\nWithdrawn $150. Remaining balance: $550\nFinal Balance: 550"
    },
    {
        "id": "Practice 5",
        "level": "Intermediate",
        "level_cls": "level-intermediate",
        "title": "Inheritance Architecture: Employee Base Class to Developer Derived Class",
        "req": "<code>Employee</code> (name, salary) বেস ক্লাস থেকে <code>Developer</code> (language, code()) চাইল্ড ক্লাস তৈরি করুন এবং <code>super()</code> এর মাধ্যমে প্যারেন্ট প্রোপার্টি ইনিশিয়ালাইজ করুন।",
        "code": """class Employee {
    constructor(name, salary) {
        this.name = name;
        this.salary = salary;
    }

    getDetails() {
        return `${this.name} earns $${this.salary}/year`;
    }
}

class Developer extends Employee {
    constructor(name, salary, language) {
        super(name, salary); // Call parent constructor
        this.language = language;
    }

    code() {
        console.log(`${this.name} is writing code in ${this.language}.`);
    }
}

// Verification
const dev = new Developer("Shariar", 95000, "JavaScript");
console.log(dev.getDetails());
dev.code();""",
        "output": "Shariar earns $95000/year\nShariar is writing code in JavaScript."
    },
    {
        "id": "Practice 6",
        "level": "Advanced",
        "level_cls": "level-advanced",
        "title": "Mini E-commerce Architecture: Product, Cart, Order & User Interaction",
        "req": "একটি পূর্ণাঙ্গ অবজেক্ট-ওরিয়েন্টেড মিনি ই-কমার্স আর্কিটেকচার তৈরি করুন যাতে <code>Product</code>, <code>Cart</code>, <code>Order</code>, এবং <code>User</code> ক্লাসগুলো একে অপরের সাথে ইন্টারঅ্যাক্ট করে মোট মূল্য ও কার্ট প্রসেসিং সম্পন্ন করবে।",
        "code": """class Product {
    constructor(id, name, price) {
        this.id = id;
        this.name = name;
        this.price = price;
    }
}

class Cart {
    constructor() {
        this.items = [];
    }

    addProduct(product, quantity = 1) {
        this.items.push({ product, quantity });
        console.log(`Added ${quantity}x ${product.name} to cart.`);
    }

    getTotal() {
        return this.items.reduce((sum, item) => sum + item.product.price * item.quantity, 0);
    }
}

class Order {
    constructor(user, cart) {
        this.user = user;
        this.items = [...cart.items];
        this.totalAmount = cart.getTotal();
        this.orderDate = new Date();
    }

    printReceipt() {
        console.log(`=== RECEIPT FOR ${this.user.name} ===`);
        this.items.forEach(i => console.log(`- ${i.product.name} x${i.quantity}: $${i.product.price * i.quantity}`));
        console.log(`Total: $${this.totalAmount}`);
    }
}

class User {
    constructor(name, email) {
        this.name = name;
        this.email = email;
    }
}

// Complete System Simulation
const user = new User("Tanjim", "tanjim@example.com");
const laptop = new Product(101, "MacBook Pro", 1999);
const mouse = new Product(102, "Magic Mouse", 79);

const cart = new Cart();
cart.addProduct(laptop, 1);
cart.addProduct(mouse, 2);

const order = new Order(user, cart);
order.printReceipt();""",
        "output": "Added 1x MacBook Pro to cart.\nAdded 2x Magic Mouse to cart.\n=== RECEIPT FOR Tanjim ===\n- MacBook Pro x1: $1999\n- Magic Mouse x2: $158\nTotal: $2157"
    }
]

html_parts.append('''    <div class="study-card">
        <div class="card-header">
            <h3 class="card-title"><span>📝</span> Hands-On Practice Lab — 6 Real-World OOP Challenges</h3>
            <span class="card-badge">Practical Lab</span>
        </div>
        <div class="card-body">
            <p>থিওরি এবং কনসেপ্ট আয়ত্ত করার পর বাস্তব প্রজেক্টে ক্লাস ব্যবহারের দক্ষতা যাচাই করার জন্য নিচে ৬টি প্র্যাকটিস প্রবলেমের বিস্তারিত সমাধান দেওয়া হলো:</p>
''')

for p in practice_solutions:
    html_parts.append(f'''            <div class="practice-item">
                <div class="practice-header">
                    <div style="font-weight: 700; font-size: 14px; color: #f8fafc;">{p["id"]}: {p["title"]}</div>
                    <span class="practice-level {p["level_cls"]}">{p["level"]}</span>
                </div>
                <p style="margin-bottom: 8px;"><strong>Problem Requirement:</strong> {p["req"]}</p>
                {render_code_box(p["code"], is_correct=True, title=f'{p["id"]} Model Solution')}
                {render_output_box(p["output"])}
            </div>
''')

html_parts.append('''        </div>
    </div>
''')

# Section 53: Final Mental Map
sec53 = raw_sections[53].strip()
ascii_map_match = re.search(r'```text([\s\S]*?)```', sec53)
ascii_map = ascii_map_match.group(1).strip() if ascii_map_match else ""

html_parts.append(f'''    <div class="study-card">
        <div class="card-header">
            <h3 class="card-title"><span>🎯</span> Final Mental Map &amp; Prototype Connection</h3>
            <span class="card-badge">Concept Architecture</span>
        </div>
        <div class="card-body">
            <p>JavaScript-এর সম্পূর্ণ Object-Oriented Programming ইকোসিস্টেম, ক্লাস ফিল্ডস, ইনহেরিট্যান্স এবং মেথড স্ট্রাকচারের সামগ্রিক ভিজ্যুয়াল আর্কিটেকচার:</p>
            {render_ascii_box(ascii_map, title="JavaScript OOP Master Architecture Tree")}
            
            <div class="card-subheading"><span>⭐</span> সবচেয়ে গুরুত্বপূর্ণ Connection</div>
            <p>তুমি <strong>Chapter 10-এ Objects</strong>, <strong>Chapter 11-এ Prototypes</strong>, এবং <strong>Chapter 24-এ Classes/OOP</strong> পড়ার পর এই তিনটির পারস্পরিক যোগসূত্র এভাবে মনে রাখবে:</p>
            {render_ascii_box("Object\\n  ↓\\nPrototype\\n  ↓\\nClass syntax\\n  ↓\\nInheritance\\n  ↓\\nOOP architecture", title="Evolution of JavaScript Object System")}
            
            <div class="callout-box callout-info" style="margin-top: 14px;">
                <strong>Key Takeaway:</strong> JavaScript-এ <code>class</code> কোনো সম্পূর্ণ নতুন অবজেক্ট মডেল নয়; এটি আসলে JavaScript-এর বিদ্যমান <strong>Prototypal Inheritance</strong> সিস্টেমের ওপর নির্মিত অত্যন্ত মার্জিত এবং আধুনিক সিনট্যাকটিক সুগার (Syntactic Sugar)। এই কনসেপ্টটি আয়ত্ত করলে React এর ক্লাস কম্পোনেন্ট, TypeScript এর ক্লাস মডেলিং এবং Node.js/NestJS আর্কিটেকচার বোঝা অত্যন্ত সহজ হয়ে যাবে।
            </div>
        </div>
    </div>
''')

# Footer & Copy Script
html_parts.append('''    <footer style="text-align: center; padding: 24px 0; color: #64748b; font-size: 12px; border-top: 1px solid #1e293b; margin-top: 30px;">
        <p>JavaScript Master Study Documentation • Chapter 24: OOP &amp; JavaScript Classes</p>
        <p>Verified with 100% Zero-Skipping Policy • ECMAScript 2026 Ready</p>
    </footer>

</div>

<script>
function copyCode(btn) {
    const pre = btn.closest('.code-box').querySelector('pre code');
    if (!pre) return;
    navigator.clipboard.writeText(pre.innerText).then(() => {
        const orig = btn.innerText;
        btn.innerText = 'Copied!';
        btn.style.color = '#34d399';
        setTimeout(() => {
            btn.innerText = orig;
            btn.style.color = '';
        }, 1800);
    });
}
</script>
</body>
</html>
''')

full_html = ''.join(html_parts)

out_file = r'c:\Users\User\Desktop\Note-Book\Code\Chapter-24-OOP-Classes.html'
with open(out_file, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f'Successfully generated {out_file} ({len(full_html)} chars, {len(full_html.splitlines())} lines)')
