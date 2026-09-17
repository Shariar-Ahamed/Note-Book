import re
import sys
import html
import os

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Read raw markdown
with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-34.md', 'r', encoding='utf-8') as f:
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
            ('DOM_BUILTIN', r'\b(?:console|window|document|process|module|exports|require|dotenv|path|fs|url|Buffer)\b'),
            ('ASYNC_METHOD', r'\b(?:then|catch|finally|resolve|reject|addEventListener|config|get|post|listen|join|resolve|readFile|writeFile)\b'),
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
        # Bash CLI syntax highlighting
        lines = esc_all.split('\n')
        out_lines = []
        for l in lines:
            if l.strip().startswith('#'):
                out_lines.append(f'<span class="syn-com">{l}</span>')
                continue
            # Flags / Options first (must be standalone tokens)
            line_hl = re.sub(r'(?<=^|\s)(--[a-zA-Z0-9_-]+|-[a-zA-Z0-9]+)(?=\s|$)', r'<span style="color:#fde047; font-weight:600;">\1</span>', l)
            # Commands & tools (standalone tokens)
            line_hl = re.sub(r'(?<=^|\s)(npm|npx|node|git|pnpm|yarn|bun|vite|eslint|prettier)(?=\s|$)', r'<span style="color:#38bdf8; font-weight:700;">\1</span>', line_hl)
            # Subcommands (standalone tokens)
            line_hl = re.sub(r'(?<=^|\s)(install|ci|run|build|dev|start|test|init|create|outdated|update|uninstall|search|info|view|exec|audit|fix|add|remove|clone|commit|push)(?=\s|$)', r'<span style="color:#4ade80; font-weight:600;">\1</span>', line_hl)
            out_lines.append(line_hl)
        return '\n'.join(out_lines)
    elif lang == 'json':
        # JSON syntax highlighting (values first, keys last so tags are not affected)
        t = re.sub(r':\s*(&quot;.*?&quot;)', r': <span style="color:#4ade80;">\1</span>', esc_all)
        t = re.sub(r':\s*\b(true|false|null)\b', r': <span style="color:#c084fc; font-weight:600;">\1</span>', t)
        t = re.sub(r':\s*(\d+(?:\.\d+)?)\s*(?=[,\n\r]|$)', r': <span style="color:#fb923c;">\1</span>', t)
        t = re.sub(r'(&quot;[a-zA-Z0-9_$-]+&quot;)\s*:', r'<span style="color:#38bdf8; font-weight:600;">\1</span>:', t)
        return t
    elif lang in ('env', 'gitignore'):
        lines = esc_all.split('\n')
        out_lines = []
        for l in lines:
            if l.strip().startswith('#'):
                out_lines.append(f'<span class="syn-com">{l}</span>')
            elif '=' in l:
                k, v = l.split('=', 1)
                out_lines.append(f'<span style="color:#38bdf8; font-weight:700;">{k}</span>=<span style="color:#4ade80;">{v}</span>')
            else:
                out_lines.append(f'<span style="color:#f1f5f9;">{l}</span>')
        return '\n'.join(out_lines)
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
    
    # 3. Tooling, Bundlers & Environments (Lavender / Violet)
    t = re.sub(r'\b(NPM|Node\.js|Vite|Rollup|esbuild|Webpack|Babel|Bundler|ESLint|Prettier|pnpm|yarn|bun|Build Tool|Development|Production)\b', r'<span style="color: #c084fc; font-weight: 700;">\1</span>', t)
    
    # 4. Manifests, Files & Directories (Amber / Gold)
    t = re.sub(r'\b(package\.json|package-lock\.json|node_modules|\.env|\.gitignore|\.eslintrc|dist/|build/|src/|index\.js|Runtime Packages|Development Tools|Reproducible Setup|Reusable Code|Package)\b', r'<span style="color: #fde047; font-weight: 600;">\1</span>', t)
    
    # 5. Commands, Scripts & Workflows (Emerald / Mint)
    t = re.sub(r'\b(npm install|npm ci|npm run|npm run dev|npm run build|npm start|npm test|npm audit|npm outdated|npx|npm init|npm create|Bundling|Tree Shaking|Minification|Production Build|Deployment|Deploy|Code)\b', r'<span style="color: #34d399; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(✓|Passed|Fast|Active|Installed|Verified|Success|Others can install and use)', r'<span style="color: #4ade80; font-weight: bold;">\1</span>', t)
    
    # 6. SemVer & Version Levels (Sky Blue)
    t = re.sub(r'\b(SemVer|MAJOR|MINOR|PATCH|Breaking|New Feature|Bug Fix|\^|\~|\*)\b', r'<span style="color: #38bdf8; font-weight: 700;">\1</span>', t)
    
    # 7. Hazards & Warnings (Rose / Crimson)
    t = re.sub(r'\b(Vulnerability|Critical|High|Security Risk|Git Commit Warning|Never commit|Leak|Do NOT commit|Audit Alert|Common Mistakes|Missing|Error)\b', r'<span style="color: #f43f5e; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(✗|X|Fail|High|Critical)', r'<span style="color: #f43f5e; font-weight: bold;">\1</span>', t)
    
    # 8. Checklist markers
    t = re.sub(r'(□)', r'<span style="color: #38bdf8; font-weight: bold;">□</span>', t)
    
    return t

def render_ascii_box(text, title=None):
    if not title:
        # Determine dynamic title based on content
        if 'package.json' in text or 'node_modules' in text:
            title = "NPM DEPENDENCY & PROJECT ARCHITECTURE"
        elif 'Vite' in text or 'Bundling' in text or 'dist' in text:
            title = "MODERN BUILD & BUNDLING PIPELINE"
        elif 'SemVer' in text or 'MAJOR' in text:
            title = "SEMANTIC VERSIONING (SEMVER) SPECIFICATION"
        elif 'Workflow' in text or 'Deploy' in text:
            title = "JAVASCRIPT DEVELOPMENT & DEPLOYMENT LIFECYCLE"
        elif 'ESLint' in text or 'Prettier' in text:
            title = "CODE QUALITY & LINTER WORKFLOW"
        elif 'Security' in text or 'Vulnerability' in text:
            title = "NPM SUPPLY CHAIN SECURITY AUDIT"
        else:
            title = "PACKAGE MANAGEMENT & TOOLING ECOSYSTEM"
            
    colorized = colorize_ascii(text)
    return f'''<div class="ascii-tree-container">
  <div class="ascii-tree-header">📦 {title}</div>
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

# Part Banners configuration for Chapter 34
PART_BANNERS = {
    1: ("Part 01", "Package Concepts, Node Ecosystem & Project Initialization (34.1 – 34.5)"),
    6: ("Part 02", "Anatomy of package.json, Core Fields & Semantic Versioning (34.6 – 34.11)"),
    12: ("Part 03", "Package Installation, node_modules & Lockfiles (34.12 – 34.16)"),
    17: ("Part 04", "Dependencies vs DevDependencies & Package Lifecycle (34.17 – 34.22)"),
    23: ("Part 05", "NPM Registry, Package Discovery & Metadata Search (34.23 – 34.26)"),
    27: ("Part 06", "NPM Scripts Automation & Development Task Pipelines (34.27 – 34.30)"),
    31: ("Part 07", "npx Runner, Modern Bundlers & Vite Architecture (34.31 – 34.35)"),
    36: ("Part 08", "Build Pipelines, Tree Shaking, Minification & Source Maps (34.36 – 34.40)"),
    41: ("Part 09", "Code Quality Engineering: ESLint, Prettier & Linter Synergy (34.41 – 34.44)"),
    45: ("Part 10", "Environment Variables, .env, .gitignore & Supply Chain Security (34.45 – 34.48)"),
    49: ("Part 11", "Dependency Trees, SemVer Carets/Tildes & Global Packages (34.49 – 34.55)"),
    56: ("Part 12", "Real-World Scaffolding, Package Managers & CI/CD Deployment (34.56 – 34.65)"),
    66: ("Part 13", "Must Know Tooling Pillars, Quick Cheat Sheet, 13 Practice Labs & Final Mental Map"),
}

# Split markdown into sections
raw_sections = re.split(r'\n(?=# 34\.\d+ )', raw_md)
print(f"Total raw section chunks parsed: {len(raw_sections)}")

# Separate Section 65 from 34.66, Cheat Sheet, Practice Set, and Final Mental Map
sec65_full = raw_sections[65]
sec65_subparts = re.split(r'\n(?=# (?:🔥\s*34\.66|🧠\s*Quick|📝\s*Practice|🎯\s*Final))', sec65_full)

sec65_clean = sec65_subparts[0].strip()
sec66_clean = sec65_subparts[1].strip() if len(sec65_subparts) > 1 else ""
cheatsheet_clean = sec65_subparts[2].strip() if len(sec65_subparts) > 2 else ""
practice_clean = sec65_subparts[3].strip() if len(sec65_subparts) > 3 else ""
mentalmap_clean = sec65_subparts[4].strip() if len(sec65_subparts) > 4 else ""

html_parts = []

# Document Header & CSS Tokens
html_parts.append('''<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter 34 — NPM, Package Management & JavaScript Tooling | JavaScript Master Study Documentation</title>
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
      #sec-34-1 {
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
          <span class="chapter-badge">Chapter 34</span>
        </div>
      </div>
      <div class="banner-sub">NPM, PACKAGE MANAGEMENT, DEPENDENCY ARCHITECTURE, MODERN BUNDLERS &amp; JAVASCRIPT TOOLING</div>
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">Total Modules</div>
          <div class="meta-val">65 Modules + 13 Practice Labs</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Curriculum Part</div>
          <div class="meta-val">Part 28 — NPM &amp; Tooling Ecosystem</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Core Mechanics</div>
          <div class="meta-val">SemVer, Lockfiles, Vite, ESLint, Prettier</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Reference Standard</div>
          <div class="meta-val">Node.js LTS / NPM v10+ Living Standard 2026</div>
        </div>
      </div>
    </header>

    <!-- Chapter Opening Statement (Page 1 Balance) -->
    <div class="opening-card">
      <div class="opening-title">
        <span>📦</span> NPM &amp; Modern JavaScript Tooling — প্রজেক্ট আর্কিটেকচার ও প্রোডাকশন পাইপলাইন
      </div>
      <p class="text-p">
        বাস্তব দুনিয়ায় প্রফেশনাল জাভাস্ক্রিপ্ট অ্যাপ্লিকেশন কখনো শূন্য থেকে একা তৈরি করা হয় না। বিশ্বজুড়ে লক্ষ লক্ষ ডেভেলপারের তৈরি প্যাকেজ নিরাপদে ম্যানেজ করা, নির্ভুল ডিপেনডেন্সি লক রাখা এবং স্বয়ংক্রিয় বিল্ড ও লিন্টিং পাইপলাইন পরিচালনা করাই হলো আধুনিক সফটওয়্যার ইঞ্জিনিয়ারিংয়ের মূল ভিত্তি। এই চ্যাপ্টারে আমরা <strong>package.json, Semantic Versioning (SemVer), Lockfiles, npm vs npx, Vite, Bundlers, Tree Shaking, ESLint, Prettier, .env সিকিউরিটি</strong> এবং CI/CD প্রোডাকশন ডিপ্লয়মেন্ট শিখব।
      </p>
      <div class="roadmap-grid">
        <div class="roadmap-item"><span>📌</span> 1. package.json &amp; Node</div>
        <div class="roadmap-item"><span>📌</span> 2. SemVer Architecture</div>
        <div class="roadmap-item"><span>📌</span> 3. Lockfile &amp; npm ci</div>
        <div class="roadmap-item"><span>📌</span> 4. Dependencies vs Dev</div>
        <div class="roadmap-item"><span>📌</span> 5. npm scripts &amp; npx</div>
        <div class="roadmap-item"><span>📌</span> 6. Vite &amp; Bundling</div>
        <div class="roadmap-item"><span>📌</span> 7. Tree Shaking &amp; Maps</div>
        <div class="roadmap-item"><span>📌</span> 8. ESLint &amp; Prettier</div>
        <div class="roadmap-item"><span>📌</span> 9. .env &amp; Security Audit</div>
        <div class="roadmap-item"><span>📌</span> 10. CI/CD Deployment</div>
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
                    res.append(f'      {render_code_box(code_content, lang="json", title="PACKAGE MANIFEST (JSON)")}\n')
                elif cur_lang in ('env', 'gitignore'):
                    res.append(f'      {render_code_box(code_content, lang="env", title=f"CONFIG FILE ({cur_lang.upper()})")}\n')
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
            res.append(f'      <div class="section-subhead" style="font-size: 11px; color: var(--navy-deep); border-left: 2px solid var(--blue-accent); padding-left: 5px;">📦 {inline_format(sub_title)}</div>\n')
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

# Process sections 1 to 64
for idx in range(1, 65):
    sec_text = raw_sections[idx].strip()
    pb = check_part_banner(idx)
    if pb:
        html_parts.append(f'    {pb}\n')
        
    sec_lines = sec_text.split('\n')
    header_line = sec_lines[0]
    m_head = re.search(r'# (?:🔥\s*|⚠️\s*)?(34\.\d+)\s*(?:—|-)?\s*(.*)', header_line)
    if m_head:
        sec_num = m_head.group(1)
        sec_title = m_head.group(2)
    else:
        sec_num = f'34.{idx}'
        sec_title = header_line.replace('#', '').strip()
        
    card_extra = ''
    if idx == 1:
        card_extra = ' id="sec-34-1"'
        
    html_parts.append(f'''    <div class="study-card"{card_extra}>
      <div class="card-title"><span class="badge-num">{sec_num}</span> {inline_format(sec_title)}</div>
''')
    
    body_text = '\n'.join(sec_lines[1:]).strip()
    html_parts.append(process_section_body(body_text))
    html_parts.append('    </div>\n')

# Process Section 65 (Cleaned of subparts)
pb65 = check_part_banner(65)
if pb65:
    html_parts.append(f'    {pb65}\n')
    
sec65_lines = sec65_clean.split('\n')
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">34.65</span> Common Mistakes — প্যাকেজ ও টুলিংয়ের সাধারণ ভুলসমূহ</div>
''')
html_parts.append(process_section_body('\n'.join(sec65_lines[1:]).strip()))
html_parts.append('    </div>\n')

# Part 13 Banner & Section 34.66: MUST KNOW
pb13 = check_part_banner(66)
if pb13:
    html_parts.append(f'    {pb13}\n')

html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">34.66</span> 🔥 MUST KNOW — জাভাস্ক্রিপ্ট টুলিংয়ের ১০টি প্রধান স্তম্ভ</div>
      <p class="text-p">প্রফেশনাল ডেভেলপার হিসেবে প্রজেক্ট পরিচালনা ও ডিপ্লয়মেন্টে এই ১০টি মূল স্তম্ভ সর্বদা মেনে চলতে হবে:</p>
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 5px;">
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #0284c7; font-size: 10px; margin-bottom: 3px;">📌 1. Manifest &amp; Dependencies</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li><strong>package.json:</strong> প্রজেক্টের মেটাডাটা ও ডিপেনডেন্সি ম্যানিফেস্ট</li>
            <li><strong>package-lock.json:</strong> হুবহু আইডেন্টিক্যাল সাব-ডিপেনডেন্সি ট্রি লক</li>
            <li><strong>node_modules:</strong> লোকাল ইনস্টল ফোল্ডার (কখনো গিটে কমিট করবেন না)</li>
            <li><strong>dependencies vs dev:</strong> রানটাইম লাইব্রেরি বনাম ডেভেলপমেন্ট টুলস</li>
          </ul>
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #059669; font-size: 10px; margin-bottom: 3px;">📌 2. Versioning &amp; Automation</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li><strong>SemVer (MAJOR.MINOR.PATCH):</strong> ব্রেকিং চেঞ্জ ও বাগফিক্স নিয়ম</li>
            <li><strong>npm ci:</strong> সিআই/সিডি সার্ভারে ক্লিন ও অপরিবর্তনীয় ডিপেনডেন্সি ইনস্টলেশন</li>
            <li><strong>npm scripts:</strong> dev, build, lint এবং test টাস্ক অটোমেশন</li>
            <li><strong>npx Runner:</strong> গ্লোবাল ইনস্টল ছাড়া তাৎক্ষণিক প্যাকেজ এক্সিকিউট</li>
          </ul>
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #7c3aed; font-size: 10px; margin-bottom: 3px;">📌 3. Build Tooling &amp; Quality</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li><strong>Vite / Rollup:</strong> ইলেকট্রন-স্পিড নেটিভ ESM ডেভেলপমেন্ট সার্ভার</li>
            <li><strong>Tree Shaking &amp; Minify:</strong> ডেড-কোড বাদ দিয়ে প্রোডাকশন বান্ডেল সংকোচন</li>
            <li><strong>ESLint &amp; Prettier:</strong> কোড স্ট্যান্ডার্ড ও ফরম্যাটিং স্বয়ংক্রিয়করণ</li>
            <li><strong>.env Security:</strong> সিক্রেট ও এপিআই কি গিট ট্র্যাকিং থেকে সুরক্ষিত রাখা</li>
          </ul>
        </div>
      </div>
    </div>
''')

# Quick Cheat Sheet Card
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">34.67</span> 🧠 Quick Cheat Sheet — কমান্ড ও কনফিগারেশন সারসংক্ষেপ</div>
''')
cheat_table = '''| Command / Concept | Syntax / Option | Main Purpose & Mechanism |
| :--- | :--- | :--- |
| **npm init -y** | `npm init -y` | ডিফল্ট কনফিগারেশনে তাৎক্ষণিক `package.json` তৈরি |
| **npm install** | `npm i <pkg>` | রানটাইম ডিপেনডেন্সি ইনস্টল ও `package.json`-এ যুক্ত |
| **npm install -D** | `npm i -D <pkg>` | শুধু ডেভেলপমেন্টে প্রয়োজনীয় প্যাকেজ ইনস্টল (`devDependencies`) |
| **npm install -g** | `npm i -g <pkg>` | সিস্টেম-ওয়াইড গ্লোবাল সিএলআই টুল ইনস্টল |
| **npm ci** | `npm ci` | লকফাইল অনুযায়ী কঠোর ও ক্লিন ইনস্টলেশন (CI/CD-তে বাধ্যতামূলক) |
| **npm run** | `npm run <script>` | `package.json`-এ সংজ্ঞায়িত কাস্টম স্ক্রিপ্ট এক্সিকিউট |
| **npx** | `npx <package>` | প্যাকেজ লোকালি ইনস্টল না করে রিমোট থেকে সরাসরি রান |
| **npm outdated** | `npm outdated` | প্রজেক্টের কোন কোন প্যাকেজ পুরনো হয়েছে তা অডিট |
| **npm update** | `npm update` | SemVer রেঞ্জ মেনে অনুমোদিত মাইনর ও প্যাচ ভার্সন আপডেট |
| **npm uninstall** | `npm un <pkg>` | প্যাকেজ ও তার রেফারেন্স সম্পূর্ণ মুছে ফেলা |
| **npm audit** | `npm audit` | ডিপেনডেন্সি ট্রিতে পরিচিত সিকিউরিটি দুর্বলতা স্ক্যান |
| **npm audit fix** | `npm audit fix` | অটোমেটিক সিকিউরিটি প্যাচ ইনস্টল করে নিরাপত্তা নিশ্চিত |
| **Caret (^)** | `"^1.2.3"` | MAJOR অপরিবর্তিত রেখে MINOR ও PATCH অটো আপডেট |
| **Tilde (~)** | `"~1.2.3"` | MAJOR ও MINOR অপরিবর্তিত রেখে শুধু PATCH অটো আপডেট |
| **Exact** | `"1.2.3"` | কোনো অটো আপডেট হবে না, হুবহু এই ভার্সন থাকবে |
| **Vite Dev** | `vite` / `npm run dev` | নো-বান্ডলিং নেটিভ ESM দিয়ে ইন্সট্যান্ট ডেভ সার্ভার বুট |
| **Vite Build** | `vite build` | Rollup ও esbuild দিয়ে অপ্টিমাইজড প্রোডাকশন বান্ডলিং |
| **ESLint** | `npx eslint .` | জাভাস্ক্রিপ্ট সিনট্যাক্স ভুল ও অ্যান্টি-প্যাটার্ন শনাক্ত |
| **Prettier** | `npx prettier --write .` | কোড ফরম্যাটিং ও স্পেসিং স্বয়ংক্রিয়ভাবে সাজানো |
| **.gitignore** | `node_modules/`, `.env` | সংবেদনশীল ও হেভি ফাইল গিট ট্র্যাকিং থেকে বাদ দেওয়া |'''
html_parts.append(f'      {render_table(cheat_table)}\n')
html_parts.append('    </div>\n')

# 13 Hands-on Practice Labs with Complete Solutions
html_parts.append('''    <div class="part-banner">Part 13.1 — 13 Hands-On Practice Labs with Complete Production Solutions</div>
''')

practice_solutions = [
    (
        1, "Beginner", "Project Initialization with npm init -y",
        "একটি নতুন NPM project তৈরি করুন (`npm init -y`) এবং স্বয়ংক্রিয়ভাবে তৈরি হওয়া `package.json`-এর স্ট্রাকচার বিশ্লেষণ করুন।",
        """# টার্মিনালে নতুন ফোল্ডার তৈরি করে প্রজেক্ট ইনিশিয়ালাইজেশন
mkdir my-js-project
cd my-js-project
npm init -y""",
        """{
  "name": "my-js-project",
  "version": "1.0.0",
  "description": "Enterprise JavaScript Package",
  "main": "src/index.js",
  "type": "module",
  "scripts": {
    "test": "echo \\"Error: no test specified\\" && exit 1"
  },
  "keywords": ["javascript", "tooling", "npm"],
  "author": "FullStack Engineer",
  "license": "MIT"
}""",
        "npm init -y কোনো প্রশ্ন ছাড়াই তাৎক্ষণিক একটি স্ট্যান্ডার্ড package.json তৈরি করে। আধুনিক প্রজেক্টে ES Module ইমপোর্ট ব্যবহারের জন্য \"type\": \"module\" যোগ করা অত্যন্ত গুরুত্বপূর্ণ।"
    ),
    (
        2, "Beginner", "Runtime Dependency Installation & ESM Usage",
        "একটি থার্ড-পার্টি লাইব্রেরি (lodash-es) ইনস্টল করুন এবং মডার্ন জাভাস্ক্রিপ্ট ফাইলে ইমপোর্ট করে অ্যারে অপারেশন পরিচালনা করুন।",
        """# টার্মিনালে lodash-es ইনস্টল
npm install lodash-es""",
        """// src/index.js
import { chunk, shuffle, uniq } from 'lodash-es';

const rawScores = [10, 20, 30, 20, 40, 50, 10, 60, 70, 80];

// ডুপ্লিকেট সরানো
const uniqueScores = uniq(rawScores);
console.log('Unique Scores:', uniqueScores);

// ৩টি করে চাঙ্কে বিভক্ত করা
const scoreChunks = chunk(uniqueScores, 3);
console.log('Score Chunks:', scoreChunks);

// অ্যারে এলোমেলো করা
console.log('Shuffled:', shuffle(uniqueScores));""",
        "npm install রানটাইম লাইব্রেরিগুলোকে dependencies ফিল্ডে যুক্ত করে যা ব্রাউজার বা প্রোডাকশন সার্ভারে একচুয়াল কোড রান করতে প্রয়োজন হয়।"
    ),
    (
        3, "Beginner", "DevDependency Installation with -D Flag",
        "একটি ডেভেলপমেন্ট-অনলি প্যাকেজ (eslint) ইনস্টল করুন এবং devDependencies-এর তাৎপর্য বুঝুন।",
        """# ডেভেলপমেন্ট টুল হিসেবে ESLint ইনস্টল
npm install -D eslint""",
        """{
  "name": "my-js-project",
  "version": "1.0.0",
  "type": "module",
  "dependencies": {
    "lodash-es": "^4.17.21"
  },
  "devDependencies": {
    "eslint": "^9.0.0"
  }
}""",
        "-D বা --save-dev ফ্ল্যাগ নির্দেশ করে যে এই টুলটি কেবল কোড লেখা, লিন্টিং বা টেস্টিংয়ের সময় প্রয়োজন; প্রোডাকশন বিল্ডে বা ক্লায়েন্টের কাছে এটি শিপ করার প্রয়োজন নেই।"
    ),
    (
        4, "Beginner", "Custom NPM Scripts Creation (dev, build, start)",
        "package.json-এ আধুনিক স্ক্রিপ্ট পাইপলাইন কনফিগার করুন এবং টার্মিনাল থেকে npm run দিয়ে এক্সিকিউট করুন।",
        """# স্ক্রিপ্ট রান করার কমান্ড
npm run dev     # ওয়াচ মোডে লাইভ রান
npm run build   # প্রোডাকশন বিল্ড ও অ্যাসেট তৈরি
npm start       # প্রোডাকশন সার্ভার স্টার্ট""",
        """{
  "scripts": {
    "dev": "node --watch src/index.js",
    "build": "echo 'Building production bundle...' && mkdir -p dist && cp -r src/* dist/",
    "start": "node dist/index.js",
    "lint": "eslint src/**/*.js"
  }
}""",
        "npm scripts টার্মিনালে দীর্ঘ ও জটিল কমান্ড বারবার টাইপ করার ঝামেলা দূর করে এবং দলের সকল ডেভেলপারের জন্য একীভূত ও স্ট্যান্ডার্ডাইজড কমান্ড ইন্টারফেস তৈরি করে।"
    ),
    (
        5, "Beginner", "Critical .gitignore Configuration for Node Projects",
        "node_modules এবং .env ফাইল যেন কখনো গিট রিপোজিটরিতে পুশ না হয় তার জন্য প্রোডাকশন গ্রেড .gitignore ফাইল তৈরি করুন।",
        """# গিট স্ট্যাটাস চেক করে ইগনোর হওয়া নিশ্চিত করা
git status""",
        """# Dependencies (কখনো গিটে পুশ করবেন না, হাজার হাজার ফাইল থাকে)
node_modules/
/.pnp
.pnp.js

# Environment Variables & Secrets (সিকিউরিটি রিস্ক)
.env
.env.local
.env.production

# Build Outputs & Cache
dist/
build/
.npm/
.eslintcache

# Operating System Files
.DS_Store
Thumbs.db
npm-debug.log*
yarn-debug.log*""",
        "node_modules গিটে পুশ করলে রিপোজিটরি সাইজ শত শত মেগাবাইট হয়ে যায়। আর .env পুশ করলে পাসওয়ার্ড বা এপিআই কি ইন্টারনেটে লিক হয়ে মারাত্মক সিকিউরিটি ব্রিচ ঘটে।"
    ),
    (
        6, "Intermediate", "Clean Node.js Application Architecture with Watch Mode",
        "একটি স্ট্যান্ডার্ড Node.js প্রজেক্ট ফোল্ডার স্ট্রাকচার তৈরি করুন এবং Node 20+ এর নেটিভ --watch ফ্ল্যাগ দিয়ে হট-রিলোড ডেভ সার্ভার চালান।",
        """# প্রজেক্ট রান
npm run dev""",
        """// src/index.js
import http from 'node:http';

const PORT = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({
    status: 'online',
    runtime: 'Node.js LTS',
    timestamp: new Date().toISOString()
  }));
});

server.listen(PORT, () => {
  console.log(`🚀 Server active at http://localhost:${PORT}`);
  console.log('⚡ Watching src/ for instant code changes...');
});""",
        "নোডজেএস ভার্সন ১৮.১১+ থেকে নোডমনের (nodemon) কোনো প্রয়োজন নেই; নেটিভ --watch ফ্ল্যাগ দিয়ে কোড এডিট করার সাথে সাথে নোড স্বয়ংক্রিয়ভাবে রিস্টার্ট হয়।"
    ),
    (
        7, "Intermediate", "Modern Frontend Scaffolding with Vite",
        "npm create vite@latest দিয়ে একটি আধুনিক, হাই-পারফরম্যান্স ভ্যানিলা বা রিঅ্যাক্ট ফ্রন্টএন্ড প্রজেক্ট তৈরি করুন।",
        """# ১. Vite দিয়ে প্রজেক্ট স্ক্যাফোল্ড করা
npm create vite@latest enterprise-frontend -- --template vanilla

# ২. ডিরেক্টরিতে প্রবেশ করে ডিপেনডেন্সি ইনস্টল
cd enterprise-frontend
npm install

# ৩. লাইভ ডেভ সার্ভার বুট
npm run dev""",
        """// vite.config.js (Production Ready Configuration)
import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    port: 5173,
    open: true
  },
  build: {
    outDir: 'dist',
    minify: 'esbuild',
    sourcemap: false
  }
});""",
        "Vite ডেভেলপমেন্ট টাইমে কোনো বান্ডলিং করে না; ব্রাউজারের নেটিভ ES Modules ব্যবহার করে মিলিসেকেন্ডে ডেভ সার্ভার লোড করে, যা ওয়েপ্যাকের তুলনায় ৫০ গুণ দ্রুত।"
    ),
    (
        8, "Intermediate", "Production Build Pipeline & Asset Inspection",
        "একটি প্রোডাকশন বিল্ড তৈরি করুন (`npm run build`) এবং dist/ ফোল্ডারের মিনিফাইড জাভাস্ক্রিপ্ট ও হ্যাশড অ্যাসেট পরীক্ষা করুন।",
        """# বিল্ড কমান্ড রান
npm run build

# বিল্ড আউটপুট প্রিভিউ
npm run preview""",
        """<!-- dist/index.html (মিনিফাইড প্রোডাকশন আর্কিটেকচার) -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" crossorigin href="/assets/index-D7h2k9La.css">
  <script type="module" crossorigin src="/assets/index-Bq1x90Lm.js"></script>
</head>
<body>
  <div id="app"></div>
</body>
</html>""",
        "বিল্ডের সময় Rollup অপ্রয়োজনীয় কোড মুছে ফেলে (Tree Shaking), ভ্যারিয়েবলের নাম ছোট করে (Minification) এবং ক্যাশিংয়ের জন্য ফাইলের নামের সাথে হ্যাশ (যেমন: index-Bq1x90Lm.js) যোগ করে।"
    ),
    (
        9, "Intermediate", "Deep Comparative Matrix: npm install vs npm ci vs npm update",
        "npm install, npm ci এবং npm update-এর প্রযুক্তিগত পার্থক্য, কাজের মেকানিজম এবং কখন কোনটি ব্যবহার করতে হবে তা তুলনামূলক চার্টে উপস্থাপন করুন।",
        """# প্রজেক্ট ও সিআই পাইপলাইনে সঠিক কমান্ড নির্বাচন
npm install    # নতুন প্যাকেজ যোগ বা লোকাল ডেভেলপমেন্ট শুরুর সময়
npm ci         # GitHub Actions বা Jenkins সিআই/সিডি বিল্ডে ১০০% নির্ভরযোগ্য
npm update     # প্যাকেজগুলোর অনুমোদিত লেটেস্ট মাইনর/প্যাচ আপগ্রেড করতে""",
        None,
        "npm install লকফাইল পরিবর্তন করতে পারে, কিন্তু npm ci কখনো লকফাইল স্পর্শ করে না; লকফাইলে কোনো অসঙ্গতি থাকলে npm ci সঙ্গে সঙ্গে এরর দিয়ে বিল্ড থামিয়ে দেয়।"
    ),
    (
        10, "Advanced", "Full-Stack Multi-Package Monorepo Architecture",
        "frontend/ (Vite) এবং backend/ (Express) আলাদা package.json ও লকফাইল দিয়ে ম্যানেজ করার একটি স্বয়ংসম্পূর্ণ প্রোডাকশন আর্কিটেকচার।",
        """# রুট লেভেল থেকে সাব-প্রজেক্ট চালানোর কমান্ড
npm run dev:frontend   # ফ্রন্টএন্ড স্টার্ট
npm run dev:backend    # ব্যাকএন্ড স্টার্ট""",
        """{
  "name": "fullstack-platform-root",
  "private": true,
  "scripts": {
    "install:all": "npm --prefix backend install && npm --prefix frontend install",
    "dev:backend": "npm --prefix backend run dev",
    "dev:frontend": "npm --prefix frontend run dev",
    "build:frontend": "npm --prefix frontend run build"
  }
}""",
        "মোনোরিপো স্ট্রাকচারে ক্লায়েন্ট ও সার্ভারের কোড একই রিপোজিটরিতে আলাদা মডিউলে থাকে, ফলে একই সাথে সম্পূর্ণ ফুলস্ট্যাক প্রজেক্ট গিটহাবে মেইনটেইন করা সহজ হয়।"
    ),
    (
        11, "Advanced", "Automated Code Quality Pipeline: ESLint + Prettier Synergy",
        "প্রজেক্টে ESLint ও Prettier কনফিগার করুন যাতে কোড সেভ করার সাথে সাথে এরর ধরা পড়ে এবং অটো-ফরম্যাটিং সম্পন্ন হয়।",
        """# লিন্টার ও ফরম্যাটার ডিপেনডেন্সি ইনস্টল
npm install -D eslint prettier eslint-config-prettier""",
        """// .eslintrc.json
{
  "env": {
    "browser": true,
    "es2024": true,
    "node": true
  },
  "extends": ["eslint:recommended", "prettier"],
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module"
  },
  "rules": {
    "no-unused-vars": "warn",
    "no-console": "off",
    "prefer-const": "error"
  }
}

// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}""",
        "ESLint মূলত কোডের কোয়ালিটি (বাগ, অব্যবহৃত ভ্যারিয়েবল) চেক করে আর Prettier কোডের স্টাইল ও বিউটিফিকেশন (ইন্ডেন্টেশন, কোটেশন) নিয়ন্ত্রণ করে।"
    ),
    (
        12, "Advanced", "Secure Environment Variables Management with dotenv",
        "ডেভেলপমেন্ট ও প্রোডাকশনে পোর্ট, ডেটাবেস স্ট্রিং এবং এপিআই কি নিরাপদে হ্যান্ডেল করার প্রোডাকশন আর্কিটেকচার।",
        """# dotenv লাইব্রেরি ইনস্টল
npm install dotenv""",
        """// .env (Secret Credentials - Git Ignored)
PORT=5000
DATABASE_URL="postgresql://admin:superSecretPassword@localhost:5432/production_db"
JWT_SECRET="d83f98a21f7c8e9b4a123456789abcdef"

// .env.example (Public Template - Committed to Git)
PORT=5000
DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
JWT_SECRET="your_jwt_secret_key_here"

// src/config.js (ESM Environment Loader)
import 'dotenv/config';

export const config = {
  port: process.env.PORT || 3000,
  dbUrl: process.env.DATABASE_URL,
  jwtSecret: process.env.JWT_SECRET
};

if (!config.jwtSecret) {
  throw new Error('FATAL: JWT_SECRET environment variable is missing!');
}""",
        ".env ফাইল সবসময় গিট ইগনোর থাকবে এবং রিপোজিটরিতে কেবল .env.example কমিট করতে হবে যাতে অন্য ডেভেলপাররা প্রয়োজনীয় ভ্যারিয়েবলের তালিকা দেখতে পায়।"
    ),
    (
        13, "Advanced", "Supply Chain Security Audit & Vulnerability Remediation",
        "npm audit চালিয়ে ডিপেনডেন্সির সিকিউরিটি ত্রুটি পরীক্ষা, সিভিই (CVE) স্কোর বিশ্লেষণ এবং নিরাপদে ফিক্স করার বাস্তব কমান্ড।",
        """# ১. ডিপেনডেন্সি সিকিউরিটি স্ক্যান
npm audit

# ২. সেমিকম্প্যাটিবল অটো-ফিক্স
npm audit fix

# ৩. ব্রেকিং চেঞ্জ রিভিউসহ ফোর্স ফিক্স (সতর্কতার সাথে)
npm audit fix --force

# ৪. প্রোডাকশন অনলি অডিট (devDependencies বাদ দিয়ে)
npm audit --omit=dev""",
        """# NPM Security Audit Summary
found 0 vulnerabilities (Dependencies Verified Safe ✅)
# যদি কোনো হাই/ক্রিটিক্যাল রিস্ক পাওয়া যায়:
# 1 High Severity Vulnerability found in 'cross-spawn'
# Fixed by upgrading package to >=7.0.5""",
        "সফটওয়্যার সাপ্লাই চেইন অ্যাটাক (যেমন ক্ষতিকর ম্যালওয়্যার লাইব্রেরি ইনজেকশন) থেকে সুরক্ষা নিশ্চিত করতে নিয়মিত npm audit চালানো বাধ্যতামূলক।"
    )
]

for lab_num, level, title, problem, bash_code, extra_code, explanation in practice_solutions:
    html_parts.append(f'''    <div class="practice-item">
      <div class="card-title"><span class="badge-num">Lab #{lab_num}</span> [{level.upper()}] — {inline_format(title)}</div>
      <p class="text-p"><strong>সমস্যা ও লক্ষ্য:</strong> {inline_format(problem)}</p>
''')
    if bash_code:
        html_parts.append(f'      {render_code_box(bash_code, lang="bash", title="TERMINAL EXECUTION COMMANDS")}\n')
    if extra_code:
        lang_type = 'json' if ('{' in extra_code and '}' in extra_code and '"' in extra_code and not '<' in extra_code and not '//' in extra_code) else ('javascript' if ('import' in extra_code or 'const' in extra_code) else ('html' if '<' in extra_code else 'env'))
        html_parts.append(f'      {render_code_box(extra_code, lang=lang_type, title=f"CONFIGURATION & IMPLEMENTATION (LAB #{lab_num})")}\n')
    if explanation:
        html_parts.append(f'      <div class="def-box">💡 <strong>প্রোডাকশন অন্তর্দৃষ্টি:</strong> {inline_format(explanation)}</div>\n')
    html_parts.append('    </div>\n')

# Final Mental Map Card
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">34.68</span> 🎯 Final Mental Map — আধুনিক জাভাস্ক্রিপ্ট টুলিংয়ের পূর্ণাঙ্গ মানচিত্র</div>
      <p class="text-p">পুরো Chapter 34-এর টুলিং, প্যাকেজ ও আর্কিটেকচারাল পাইপলাইন একসাথে:</p>
''')

final_map_ascii = """                    JAVASCRIPT TOOLING ECOSYSTEM
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
      PROJECT                 PACKAGE                 MODERN
     MANIFEST               DEPENDENCIES             BUILDING
         │                       │                       │
    package.json            node_modules               Vite
    ├── name & version      ├── Direct Deps            Rollup
    ├── scripts (run/dev)   └── Transitive Deps        esbuild
    └── type: "module"           │                     Tree Shaking
         │                  package-lock.json          Minification
         │                  (Deterministic Lock)       Source Maps
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                                 ▼
                     DEVELOPER WORKFLOW & PIPELINE
                                 │
       ┌─────────────────────────┼─────────────────────────┐
       │                         │                         │
   CODE QUALITY              SECURITY                 DEPLOYMENT
       │                         │                         │
   ESLint (Linter)          npm audit                npm ci (CI/CD)
   Prettier (Formatter)     .env (Secrets)           dist/ Output
   Git Hooks (Husky)        .gitignore (Ignored)     Production Ready"""

html_parts.append(f'      {render_ascii_box(final_map_ascii, title="FULL TOOLING & NPM ARCHITECTURE MAP")}\n')

html_parts.append('''      <div class="def-box" style="margin-top: 6px;">
        🏆 <strong>এক লাইনে Chapter 34:</strong> NPM হলো জাভাস্ক্রিপ্ট প্রজেক্টের প্যাকেজ ও ডিপেনডেন্সি ম্যানেজমেন্ট সিস্টেম; আর package.json, lockfile, scripts, Vite এবং কোয়ালিটি টুলস (ESLint/Prettier) মিলে একটি মডার্ন জাভাস্ক্রিপ্ট প্রজেক্টের সম্পূর্ণ লাইফসাইকেল ও প্রোডাকশন পাইপলাইন পরিচালনা করে।
      </div>

      <div class="section-subhead" style="margin-top: 8px;">🔗 Curriculum Progression: Chapter 33 → 34 → 35</div>
''')

roadmap_conn_ascii = """Chapter 33: Web Performance & Optimization
       ↓
অ্যাপ্লিকেশনের লোড টাইম, রেন্ডারিং স্পিড ও কোর ওয়েব ভাইটালস অপ্টিমাইজেশন
       ↓
Chapter 34: NPM & Modern JavaScript Tooling (THIS CHAPTER)
       ↓
প্যাকেজ ম্যানেজমেন্ট, প্রজেক্ট স্ক্যাফোল্ডিং, বান্ডলিং (Vite) ও ওয়ার্কফ্লো অটোমেশন
       ↓
Chapter 35: Testing JavaScript
       ↓
Unit Testing, Integration Testing, Assertions, Vitest/Jest, Mocking & TDD"""

html_parts.append(f'      {render_ascii_box(roadmap_conn_ascii, title="ROADMAP CONTINUITY PIPELINE")}\n')
html_parts.append('    </div>\n')

# Document Footer
html_parts.append('''  </div>
</body>
</html>''')

# Write complete HTML
output_html_path = r'c:\Users\User\Desktop\Note-Book\Code\Chapter-34-NPM-Package-Management-Tooling.html'
os.makedirs(os.path.dirname(output_html_path), exist_ok=True)

with open(output_html_path, 'w', encoding='utf-8') as f:
    f.write(''.join(html_parts))

print(f"Successfully generated HTML: {output_html_path} (Total size: {len(''.join(html_parts))} bytes)")
