import glob, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')

def scope_css(css_text, scope_class):
    """
    Scopes all CSS rules in css_text to .scope_class.
    """
    clean_css = re.sub(r'/\*[\s\S]*?\*/', '', css_text)
    
    media_blocks = []
    pos = 0
    extracted = ""
    while pos < len(clean_css):
        media_match = re.search(r'@media[^{]+\{', clean_css[pos:])
        if not media_match:
            extracted += clean_css[pos:]
            break
        
        m_start = pos + media_match.start()
        b_start = pos + media_match.end()
        extracted += clean_css[pos:m_start]
        
        depth = 1
        i = b_start
        while i < len(clean_css) and depth > 0:
            if clean_css[i] == '{':
                depth += 1
            elif clean_css[i] == '}':
                depth -= 1
            i += 1
        
        media_header = clean_css[m_start:b_start].strip()
        media_inner = clean_css[b_start:i-1].strip()
        
        media_blocks.append((media_header, media_inner))
        extracted += f"\n/*__MEDIA_{len(media_blocks)-1}__*/\n"
        pos = i

    page_rules = []
    def replace_page(match):
        page_rules.append(match.group(0))
        return ""
    extracted = re.sub(r'@page\s*\{[\s\S]*?\}', replace_page, extracted)

    def transform_rule_block(rules_text, scope):
        out = []
        for chunk in rules_text.split('}'):
            chunk = chunk.strip()
            if not chunk or '{' not in chunk:
                continue
            sel_part, body = chunk.split('{', 1)
            sel_part = sel_part.strip()
            body = body.strip()
            if not sel_part or not body:
                continue
            
            # Don't let body background override the dark canvas
            if 'background-color:' in body and ('body' in sel_part or sel_part == ':root'):
                # keep variables, but don't force light background on .scope
                pass

            scoped_selectors = []
            for sel in sel_part.split(','):
                sel = sel.strip()
                if not sel:
                    continue
                if sel == ':root':
                    scoped_selectors.append(f".{scope}")
                elif sel == 'body':
                    scoped_selectors.append(f".{scope}")
                elif sel == '*':
                    scoped_selectors.append(f".{scope}, .{scope} *")
                elif sel == '*::before':
                    scoped_selectors.append(f".{scope} *::before")
                elif sel == '*::after':
                    scoped_selectors.append(f".{scope} *::after")
                elif sel == 'html':
                    scoped_selectors.append(f".{scope}")
                elif sel.startswith(':root'):
                    scoped_selectors.append(sel.replace(':root', f".{scope}"))
                elif sel.startswith('body'):
                    scoped_selectors.append(sel.replace('body', f".{scope}", 1))
                else:
                    scoped_selectors.append(f".{scope} {sel}")
            
            new_sel = ",\n".join(scoped_selectors)
            out.append(f"{new_sel} {{\n  {body}\n}}")
        return "\n".join(out)

    scoped_top_rules = transform_rule_block(extracted, scope_class)
    
    scoped_media_blocks = []
    for media_header, media_inner in media_blocks:
        scoped_inner = transform_rule_block(media_inner, scope_class)
        scoped_media_blocks.append(f"{media_header}\n{scoped_inner}\n}}")
        
    final_css = scoped_top_rules + "\n\n" + "\n\n".join(scoped_media_blocks)
    return final_css, page_rules

def build_all():
    src_dir = '4-Components/JavaScript/Code'
    files = sorted(glob.glob(os.path.join(src_dir, 'Chapter-*.html')))
    print(f"Processing {len(files)} chapters from {src_dir}...")
    assert len(files) == 40, f"Expected 40 chapters, got {len(files)}"
    
    all_scoped_css = []
    chapters_html = []
    toc_options = []
    toc_cards = []
    chapter_menu_items = []
    
    for f in files:
        fname = os.path.basename(f)
        ch_num = int(re.search(r'Chapter-(\d+)-', fname).group(1))
        ch_class = f"ch-{ch_num:02d}"
        ch_id = f"chapter-{ch_num:02d}"
        
        with open(f, 'r', encoding='utf-8') as fp:
            content = fp.read()
            
        m_title = re.search(r'class=["\']banner-title["\']>\s*(.*?)\s*</span>', content)
        title_text = m_title.group(1).strip() if m_title else f"Chapter {ch_num:02d}"
        
        m_badge = re.search(r'class=["\']chapter-badge["\']>\s*(.*?)\s*</span>', content)
        badge_text = m_badge.group(1).strip() if m_badge else f"Chapter {ch_num:02d}"
        
        m_style = re.search(r'<style>([\s\S]*?)</style>', content)
        assert m_style, f"No style in {fname}"
        raw_css = m_style.group(1)
        scoped_css, _ = scope_css(raw_css, ch_class)
        all_scoped_css.append(f"/* ==========================================\n   CHAPTER {ch_num:02d} SCOPED STYLES ({badge_text})\n   ========================================== */\n{scoped_css}")
        
        dp_start = content.find('<div class="doc-page">')
        assert dp_start != -1, f"No doc-page in {fname}"
        inner_start = dp_start + len('<div class="doc-page">')
        last_div = content.rfind('</div>')
        body_end = content.rfind('</body>')
        assert last_div != -1 and last_div < body_end, f"Malformed closing div in {fname}"
        
        inner_content = content[inner_start:last_div].strip()
        
        # Elegant Chapter Transition Divider
        sep_badge_label = f"{badge_text} — Starts Here" if ch_num == 1 else badge_text
        sep_html = f'''  <!-- CHAPTER {ch_num:02d} TRANSITION SEPARATOR -->
  <div class="chapter-separator">
    <div class="separator-line"></div>
    <div class="separator-pill">
      <div class="sep-top-row">
        <div class="sep-badge-wrap">
          <span class="sep-dot"></span>
          <span class="sep-badge">{sep_badge_label}</span>
        </div>
        <a href="#top" class="sep-top-btn" title="Back to Table of Contents">↑ Index</a>
      </div>
      <div class="sep-title">{title_text}</div>
    </div>
    <div class="separator-line"></div>
  </div>'''

        ch_html = f'''{sep_html}
  <!-- CHAPTER {ch_num:02d}: {badge_text} -->
  <section id="{ch_id}" class="chapter-section {ch_class}">
    <div class="doc-page">
{inner_content}
    </div>
  </section>'''
        chapters_html.append(ch_html)
        
        # Extract English and Bengali parts for crisp dropdown display
        if ' — ' in title_text:
            parts = title_text.split(' — ', 1)
            eng_title = parts[0].strip()
            bn_title = parts[1].strip()
        else:
            eng_title = title_text
            bn_title = ''
        
        bn_html = f'<span class="menu-bn-title">{bn_title}</span>' if bn_title else ''
        chapter_menu_items.append(f'''        <a href="#{ch_id}" class="chapter-menu-item" onclick="selectChapter('{ch_id}')" data-title="{title_text.lower()} {badge_text.lower()}">
          <span class="menu-num">{ch_num:02d}</span>
          <span class="menu-text-wrap">
            <span class="menu-eng-title">{eng_title}</span>
            {bn_html}
          </span>
        </a>''')

        toc_options.append(f'<option value="#{ch_id}">{badge_text}: {eng_title}</option>')
        toc_cards.append(f'<a href="#{ch_id}" class="toc-item"><span class="toc-num">{ch_num:02d}</span><span class="toc-name">{title_text}</span></a>')
        print(f"  Processed Chapter {ch_num:02d}: {badge_text}")

    full_css_text = "\n\n".join(all_scoped_css)
    all_chapters_body = "\n\n".join(chapters_html)
    options_html = "\n        ".join(toc_options)
    toc_cards_html = "\n        ".join(toc_cards)
    chapter_menu_html = "\n".join(chapter_menu_items)

    # Master omnibus wrapper CSS with the EXACT dark aesthetic requested by user
    omnibus_css = """
    /* =======================================================
       MASTER OMNIBUS NAVIGATION & FULL-BOOK WRAPPER STYLES
       ======================================================= */
    @page {
      size: A4;
      margin: 8mm 10mm;
    }

    *, *::before, *::after {
      box-sizing: border-box;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }

    html {
      scroll-behavior: smooth;
    }

    body {
      margin: 0;
      padding: 0;
      background-color: #0b0f19;
      color: #0f172a;
      font-family: 'Hind Siliguri', 'Plus Jakarta Sans', sans-serif;
      -webkit-font-smoothing: antialiased;
    }

    /* Top Sticky Navigation Bar */
    .omnibus-navbar {
      position: sticky;
      top: 0;
      z-index: 999999;
      background: rgba(15, 23, 42, 0.96);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      padding: 8px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 15px;
      border-bottom: 1px solid #334155;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    }

    .omnibus-brand {
      display: flex;
      align-items: center;
      gap: 10px;
      color: #f8fafc;
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 13px;
      font-weight: 800;
      letter-spacing: 0.5px;
      text-decoration: none;
      white-space: nowrap;
    }

    .omnibus-brand .logo {
      background: #f7df1e;
      color: #000000;
      font-weight: 800;
      font-size: 12px;
      padding: 2px 7px;
      border-radius: 4px;
    }

    .omnibus-controls {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }

    /* Omnibus Chapter Dropdown Menu */
    .omnibus-dropdown-container {
      position: relative;
      display: inline-block;
    }

    .chapter-dropdown-trigger {
      background: #1e293b;
      color: #f8fafc;
      border: 1px solid #475569;
      border-radius: 6px;
      padding: 6px 12px;
      font-size: 11.5px;
      font-family: 'Plus Jakarta Sans', sans-serif;
      cursor: pointer;
      outline: none;
      display: flex;
      align-items: center;
      gap: 10px;
      transition: all 0.2s ease;
      white-space: nowrap;
      min-width: 220px;
      justify-content: space-between;
    }

    .chapter-dropdown-trigger:hover, .chapter-dropdown-trigger:focus {
      border-color: #38bdf8;
      background: #243248;
    }

    .chapter-dropdown-trigger .btn-left {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .chapter-dropdown-trigger .btn-arrow {
      font-size: 10px;
      color: #94a3b8;
      transition: transform 0.2s ease;
    }

    .chapter-dropdown-trigger[aria-expanded="true"] .btn-arrow {
      transform: rotate(180deg);
      color: #38bdf8;
    }

    /* Backdrop for clicking outside */
    .chapter-menu-backdrop {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.6);
      backdrop-filter: blur(2px);
      -webkit-backdrop-filter: blur(2px);
      z-index: 999998;
    }

    .chapter-menu-backdrop.active {
      display: block;
    }

    /* Floating Dropdown Card */
    .chapter-dropdown-menu {
      display: none;
      position: absolute;
      top: calc(100% + 8px);
      left: 0;
      width: 380px;
      max-width: 92vw;
      max-height: 480px;
      background: #111827;
      border: 1px solid #374151;
      border-radius: 10px;
      box-shadow: 0 10px 32px rgba(0, 0, 0, 0.6), 0 0 16px rgba(56, 189, 248, 0.15);
      z-index: 999999;
      flex-direction: column;
      overflow: hidden;
      box-sizing: border-box;
      animation: dropdown-fade-in 0.2s ease-out;
    }

    @keyframes dropdown-fade-in {
      from { opacity: 0; transform: translateY(-6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .chapter-dropdown-menu.active {
      display: flex;
    }

    .chapter-menu-header {
      padding: 12px 14px 10px 14px;
      background: #0f172a;
      border-bottom: 1px solid #1f2937;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .chapter-menu-title-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      color: #f8fafc;
      font-size: 12px;
      font-weight: 700;
    }

    .chapter-menu-close {
      background: #1e293b;
      border: 1px solid #334155;
      color: #94a3b8;
      border-radius: 4px;
      width: 24px;
      height: 24px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 12px;
      transition: all 0.15s ease;
    }

    .chapter-menu-close:hover {
      color: #ffffff;
      background: #ef4444;
      border-color: #ef4444;
    }

    .chapter-search-input {
      width: 100%;
      background: #1e293b;
      color: #f8fafc;
      border: 1px solid #334155;
      border-radius: 6px;
      padding: 6px 10px;
      font-size: 11.5px;
      font-family: 'Plus Jakarta Sans', sans-serif;
      outline: none;
      box-sizing: border-box;
      transition: border-color 0.2s ease;
    }

    .chapter-search-input:focus {
      border-color: #38bdf8;
    }

    .chapter-menu-list {
      overflow-y: auto;
      max-height: 380px;
      padding: 6px;
      display: flex;
      flex-direction: column;
      gap: 4px;
      scrollbar-width: thin;
      scrollbar-color: #475569 transparent;
    }

    .chapter-menu-list::-webkit-scrollbar {
      width: 6px;
    }

    .chapter-menu-list::-webkit-scrollbar-thumb {
      background: #475569;
      border-radius: 3px;
    }

    .chapter-menu-item {
      display: flex;
      align-items: flex-start;
      gap: 10px;
      padding: 8px 10px;
      border-radius: 6px;
      text-decoration: none;
      color: #e2e8f0;
      background: #1f2937;
      border: 1px solid transparent;
      transition: all 0.15s ease;
      cursor: pointer;
    }

    .chapter-menu-item:hover, .chapter-menu-item.highlighted {
      background: #374151;
      border-color: #38bdf8;
      color: #ffffff;
      transform: translateX(2px);
    }

    .chapter-menu-item .menu-num {
      background: #f7df1e;
      color: #000000;
      font-family: 'Fira Code', monospace;
      font-weight: 800;
      font-size: 9.5px;
      padding: 2px 5px;
      border-radius: 3px;
      flex-shrink: 0;
      margin-top: 2px;
    }

    .chapter-menu-item .menu-text-wrap {
      display: flex;
      flex-direction: column;
      gap: 2px;
      flex: 1;
      min-width: 0;
    }

    .chapter-menu-item .menu-eng-title {
      font-size: 11.5px;
      font-weight: 600;
      line-height: 1.35;
      white-space: normal;
      word-break: break-word;
    }

    .chapter-menu-item .menu-bn-title {
      font-size: 10.5px;
      color: #94a3b8;
      line-height: 1.4;
      white-space: normal;
      word-break: break-word;
      font-family: 'Hind Siliguri', sans-serif;
    }

    .chapter-menu-no-results {
      padding: 16px;
      text-align: center;
      color: #94a3b8;
      font-size: 11.5px;
    }

    .omnibus-btn {
      background: linear-gradient(135deg, #0284c7, #0369a1);
      color: #ffffff;
      border: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 2px 6px rgba(2, 132, 199, 0.3);
      transition: all 0.2s ease;
      text-decoration: none;
    }

    .omnibus-btn:hover {
      background: linear-gradient(135deg, #0369a1, #075985);
      transform: translateY(-1px);
    }

    /* Master Cover & Table of Contents (Exact Dark Aesthetic from Screenshot) */
    .master-toc-section {
      width: 95%;
      max-width: 1160px;
      margin: 24px auto;
      background: #111827;
      border: 1px solid #1f2937;
      border-radius: 12px;
      padding: 24px 28px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
      color: #f8fafc;
    }

    .master-toc-header {
      text-align: center;
      border-bottom: 1px solid #1f2937;
      padding-bottom: 16px;
      margin-bottom: 20px;
    }

    .master-toc-title {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 20px;
      font-weight: 800;
      color: #f7df1e;
      letter-spacing: 0.5px;
      margin-bottom: 6px;
    }

    .master-toc-subtitle {
      font-size: 12px;
      color: #94a3b8;
    }

    .master-toc-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
    }

    @media (max-width: 860px) {
      .master-toc-grid {
        grid-template-columns: 1fr;
      }
    }

    .toc-item {
      display: flex;
      align-items: flex-start;
      gap: 12px;
      padding: 10px 14px;
      background: #1f2937;
      border: 1px solid #374151;
      border-radius: 6px;
      color: #e2e8f0;
      text-decoration: none;
      font-size: 12px;
      font-weight: 500;
      transition: all 0.15s ease;
      min-height: auto;
      height: auto;
      overflow: visible;
      box-sizing: border-box;
    }

    .toc-item:hover {
      background: #374151;
      border-color: #38bdf8;
      color: #ffffff;
      transform: translateX(2px);
    }

    .toc-num {
      background: #f7df1e;
      color: #000000;
      font-family: 'Fira Code', monospace;
      font-weight: 800;
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 3px;
      flex-shrink: 0;
      margin-top: 1px;
    }

    .toc-name {
      white-space: normal;
      word-break: break-word;
      overflow-wrap: anywhere;
      line-height: 1.5;
      flex: 1;
      min-width: 0;
      padding-bottom: 2px;
    }

    /* Chapter Section Separation & Dark Background Integrity */
    .chapter-section {
      margin: 0;
      padding: 0;
      background: transparent !important;
    }

    .chapter-section .doc-page {
      width: 95%;
      max-width: 860px;
      margin: 20px auto;
      background: #ffffff !important;
      padding: 24px 28px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
      border-radius: 8px;
    }

    /* =======================================================
       CHAPTER SEPARATOR & TRANSITION STYLES
       ======================================================= */
    .chapter-separator {
      width: 95%;
      max-width: 860px;
      margin: 54px auto 28px auto;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 16px;
      position: relative;
      box-sizing: border-box;
    }

    .separator-line {
      flex: 1;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.4), rgba(247, 223, 30, 0.5), transparent);
    }

    .separator-pill {
      background: rgba(17, 24, 39, 0.95);
      border: 1px solid rgba(247, 223, 30, 0.35);
      border-radius: 10px;
      padding: 10px 16px;
      display: flex;
      flex-direction: column;
      align-items: stretch;
      gap: 6px;
      min-width: 280px;
      max-width: 620px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5), 0 0 14px rgba(247, 223, 30, 0.12);
      color: #f8fafc;
      font-family: 'Plus Jakarta Sans', sans-serif;
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      transition: all 0.2s ease;
      box-sizing: border-box;
    }

    .separator-pill:hover {
      border-color: #f7df1e;
      box-shadow: 0 4px 24px rgba(247, 223, 30, 0.25);
      transform: translateY(-1px);
    }

    .sep-top-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      gap: 10px;
    }

    .sep-badge-wrap {
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }

    .sep-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #f7df1e;
      box-shadow: 0 0 8px #f7df1e;
      display: inline-block;
      flex-shrink: 0;
      animation: pulse-dot 2s infinite ease-in-out;
    }

    @keyframes pulse-dot {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.5; transform: scale(0.85); }
    }

    .sep-badge {
      background: #f7df1e;
      color: #000000;
      font-family: 'Fira Code', monospace;
      font-weight: 800;
      font-size: 10px;
      padding: 2.5px 8px;
      border-radius: 4px;
      letter-spacing: 0.5px;
      flex-shrink: 0;
      white-space: nowrap;
    }

    .sep-title {
      color: #f1f5f9;
      font-family: 'Hind Siliguri', 'Plus Jakarta Sans', sans-serif;
      font-weight: 600;
      font-size: 12px;
      line-height: 1.5;
      white-space: normal;
      word-break: break-word;
      overflow-wrap: anywhere;
      text-align: left;
    }

    .sep-top-btn {
      color: #94a3b8;
      background: rgba(30, 41, 59, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 4px;
      padding: 2.5px 9px;
      font-size: 10px;
      font-weight: 700;
      text-decoration: none;
      transition: all 0.15s ease;
      flex-shrink: 0;
      white-space: nowrap;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .sep-top-btn:hover {
      color: #38bdf8;
      border-color: #38bdf8;
      background: #1e293b;
    }

    /* Floating Back to Top Button */
    .floating-back-top {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 99999;
      background: linear-gradient(135deg, #0284c7, #0369a1);
      color: #ffffff;
      border: 1px solid rgba(255, 255, 255, 0.2);
      width: 42px;
      height: 42px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      font-weight: 800;
      cursor: pointer;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
      text-decoration: none;
      transition: all 0.2s ease;
    }

    .floating-back-top:hover {
      background: linear-gradient(135deg, #0369a1, #075985);
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(2, 132, 199, 0.4);
    }

    /* =======================================================
       RESPONSIVE DESIGN FOR TAB (TABLET) DEVICES (<= 1024px)
       ======================================================= */
    @media (max-width: 1024px) {
      .master-toc-section {
        width: 96%;
        padding: 20px 22px;
      }
      .chapter-section .doc-page {
        width: 96%;
        max-width: 820px;
        padding: 20px 22px;
      }
      .chapter-select {
        max-width: 280px;
      }
      .meta-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 6px !important;
      }
    }

    @media (max-width: 860px) {
      .master-toc-grid {
        grid-template-columns: 1fr !important;
        gap: 8px !important;
      }
      .chapter-separator {
        width: calc(100% - 16px) !important;
        max-width: 100% !important;
        margin: 32px auto 16px auto !important;
        padding: 0 !important;
        gap: 0 !important;
      }
      .separator-line {
        display: none !important;
      }
      .separator-pill {
        width: 100% !important;
        max-width: 100% !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5) !important;
      }
      .sep-title {
        font-size: 11.5px !important;
        line-height: 1.5 !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
      }
    }

    /* =======================================================
       RESPONSIVE DESIGN FOR MOBILE PHONE DEVICES (<= 768px)
       ======================================================= */
    @media (max-width: 768px) {
      html, body {
        overflow-x: clip !important;
        width: 100% !important;
        max-width: 100vw !important;
      }

      /* Top Navbar - Always Sticky on Mobile */
      .omnibus-navbar {
        position: -webkit-sticky !important;
        position: sticky !important;
        top: 0 !important;
        z-index: 999999 !important;
        padding: 8px 10px;
        flex-direction: column;
        align-items: stretch;
        gap: 8px;
        width: 100% !important;
        box-sizing: border-box !important;
      }
      .omnibus-brand {
        font-size: 11px !important;
        justify-content: center;
        white-space: normal !important;
        text-align: center;
        line-height: 1.35;
        word-break: break-word !important;
      }
      .omnibus-brand .logo {
        font-size: 10px !important;
        padding: 1px 5px !important;
      }
      .omnibus-controls {
        width: 100%;
        display: flex;
        gap: 6px;
      }
      .omnibus-dropdown-container {
        flex: 1;
        min-width: 0;
      }
      .chapter-dropdown-trigger {
        width: 100% !important;
        min-width: 0 !important;
        font-size: 10.5px !important;
        padding: 5px 8px !important;
      }
      .chapter-dropdown-menu {
        position: fixed !important;
        top: 60px !important;
        left: 10px !important;
        right: 10px !important;
        width: calc(100% - 20px) !important;
        max-width: calc(100% - 20px) !important;
        max-height: 75vh !important;
        border-radius: 10px !important;
        margin: 0 auto !important;
      }
      .chapter-menu-list {
        max-height: calc(75vh - 95px) !important;
      }
      .omnibus-btn {
        padding: 5px 9px;
        font-size: 10px;
        white-space: nowrap;
      }

      /* Table of Contents */
      .master-toc-section {
        width: calc(100% - 14px) !important;
        margin: 12px auto !important;
        padding: 14px 10px !important;
        border-radius: 8px !important;
        box-sizing: border-box !important;
      }
      .master-toc-header {
        padding-bottom: 10px !important;
        margin-bottom: 12px !important;
      }
      .master-toc-title {
        font-size: 14.5px !important;
        line-height: 1.35 !important;
        word-break: break-word !important;
      }
      .master-toc-subtitle {
        font-size: 10px !important;
        line-height: 1.4 !important;
      }
      .master-toc-grid {
        grid-template-columns: 1fr !important;
        gap: 8px !important;
        width: 100% !important;
        box-sizing: border-box !important;
      }
      .toc-item {
        width: 100% !important;
        box-sizing: border-box !important;
        padding: 10px 12px !important;
        font-size: 11.5px !important;
        min-height: auto !important;
        height: auto !important;
        overflow: visible !important;
        display: flex !important;
        align-items: flex-start !important;
        gap: 10px !important;
        border-radius: 6px !important;
      }
      .toc-num {
        font-size: 9.5px !important;
        padding: 2.5px 6px !important;
        margin-top: 1px !important;
        flex-shrink: 0 !important;
      }
      .toc-name {
        font-size: 11.5px !important;
        line-height: 1.55 !important;
        white-space: normal !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
        flex: 1 !important;
        min-width: 0 !important;
        padding-bottom: 2px !important;
      }

      /* Chapter Transition Separators on Mobile */
      .chapter-separator {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        padding: 0 8px !important;
        margin: 28px auto 14px auto !important;
        gap: 0 !important;
      }
      .separator-line {
        display: none !important;
      }
      .separator-pill {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 6px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5) !important;
        white-space: normal !important;
      }
      .sep-top-row {
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        width: 100% !important;
        gap: 8px !important;
      }
      .sep-badge-wrap {
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
      }
      .sep-badge {
        font-size: 9.5px !important;
        padding: 2.5px 7px !important;
        white-space: nowrap !important;
      }
      .sep-title {
        font-size: 11.5px !important;
        line-height: 1.5 !important;
        text-align: left !important;
        white-space: normal !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
        color: #f1f5f9 !important;
        width: 100% !important;
        max-width: 100% !important;
        padding-top: 2px !important;
      }
      .sep-top-btn {
        font-size: 9.5px !important;
        padding: 2.5px 8px !important;
        white-space: nowrap !important;
      }

      /* Chapter Documents on Mobile */
      .chapter-section {
        width: 100% !important;
        box-sizing: border-box !important;
        overflow-x: clip !important;
      }
      .chapter-section .doc-page, [class*="ch-"] .doc-page {
        width: calc(100% - 14px) !important;
        max-width: 100% !important;
        margin: 12px auto !important;
        padding: 12px 10px !important;
        border-radius: 6px !important;
        box-sizing: border-box !important;
      }

      /* Chapter Header Master Banner */
      [class*="ch-"] .master-banner, .master-banner {
        padding: 12px 12px !important;
        border-radius: 6px !important;
        width: 100% !important;
        box-sizing: border-box !important;
      }
      [class*="ch-"] .banner-top, .banner-top {
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 8px !important;
        width: 100% !important;
      }
      [class*="ch-"] .banner-left, .banner-left {
        gap: 8px !important;
        flex-wrap: wrap !important;
        width: 100% !important;
        display: flex !important;
        align-items: flex-start !important;
      }
      [class*="ch-"] .banner-icon, .banner-icon {
        font-size: 10.5px !important;
        padding: 2px 6px !important;
        flex-shrink: 0 !important;
        margin-top: 2px !important;
      }
      [class*="ch-"] .banner-title, .banner-title {
        font-size: 12px !important;
        line-height: 1.45 !important;
        white-space: normal !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
        flex: 1 !important;
        min-width: 0 !important;
      }
      [class*="ch-"] .chapter-badge, .chapter-badge {
        align-self: flex-start !important;
        font-size: 10px !important;
        padding: 2px 7px !important;
        margin-top: 2px !important;
      }
      [class*="ch-"] .meta-grid, .meta-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 4px !important;
        padding: 6px 6px !important;
        width: 100% !important;
        box-sizing: border-box !important;
      }
      [class*="ch-"] .meta-label, .meta-label {
        font-size: 7.5px !important;
      }
      [class*="ch-"] .meta-val, .meta-val {
        font-size: 8px !important;
      }

      /* Study Cards & Headers */
      [class*="ch-"] .study-card, .study-card {
        padding: 8px 8px !important;
        margin-bottom: 6px !important;
        width: 100% !important;
        box-sizing: border-box !important;
      }
      [class*="ch-"] .card-title, .card-title {
        font-size: 10.5px !important;
        line-height: 1.35 !important;
        word-break: break-word !important;
      }
      [class*="ch-"] .badge-num, .badge-num {
        font-size: 9px !important;
      }
      [class*="ch-"] .text-p, .text-p {
        font-size: 9.5px !important;
        line-height: 1.45 !important;
      }

      /* Code boxes, ASCII trees & Diagrams horizontal touch-scroll */
      [class*="ch-"] .code-box, .code-box,
      [class*="ch-"] pre, pre,
      [class*="ch-"] .ascii-tree-container, .ascii-tree-container,
      [class*="ch-"] .table-wrap, .table-wrap {
        overflow-x: auto !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        -webkit-overflow-scrolling: touch;
      }
      pre {
        font-size: 8.5px !important;
        line-height: 1.35 !important;
      }
      [class*="ch-"] .ascii-tree-container, .ascii-tree-container {
        font-size: 8px !important;
        padding: 4px 6px !important;
      }
      [class*="ch-"] .ascii-tree-content, .ascii-tree-content {
        font-size: 8px !important;
        padding: 4px 6px !important;
      }

      /* Tables auto-scroll */
      [class*="ch-"] table, table {
        display: block !important;
        max-width: 100% !important;
        overflow-x: auto !important;
        box-sizing: border-box !important;
        -webkit-overflow-scrolling: touch;
      }
      table th, table td {
        padding: 4px 5px !important;
        font-size: 8px !important;
        white-space: normal !important;
      }

      /* Definitions & memory boxes */
      [class*="ch-"] .def-box, .def-box,
      [class*="ch-"] .memory-box, .memory-box,
      [class*="ch-"] .warn-box, .warn-box,
      [class*="ch-"] .practice-item, .practice-item {
        padding: 5px 6px !important;
        font-size: 9px !important;
        box-sizing: border-box !important;
      }

      .floating-back-top {
        bottom: 14px;
        right: 14px;
        width: 36px;
        height: 36px;
        font-size: 15px;
      }
    }

    /* Smallest Mobile Devices (<= 480px) */
    @media (max-width: 480px) {
      [class*="ch-"] .meta-grid, .meta-grid {
        grid-template-columns: 1fr !important;
      }
      .chapter-section .doc-page, [class*="ch-"] .doc-page {
        width: 100% !important;
        margin: 6px auto !important;
        padding: 10px 8px !important;
        border-radius: 4px !important;
      }
    }

    @media print {
      body {
        background: #ffffff !important;
      }
      .omnibus-navbar,
      .master-toc-section,
      .action-bar,
      .floating-back-top,
      .chapter-separator {
        display: none !important;
      }
      .chapter-section {
        page-break-before: always !important;
        break-before: page !important;
        margin: 0 !important;
        padding: 0 !important;
        background: #ffffff !important;
      }
      .chapter-section:first-of-type {
        page-break-before: avoid !important;
        break-before: avoid !important;
      }
      .chapter-section .doc-page {
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        box-shadow: none !important;
      }
    }
    """

    # Combined Master CSS & JS
    master_css = f'''/* ==========================================================================
   JAVASCRIPT MASTER STUDY DOCUMENTATION — COMPLETE BOOK (CHAPTERS 01 - 40)
   MASTER STYLESHEET (css/style.css)
   Zero-Skipping Policy Edition • 100% Identical Visual Fidelity
   ========================================================================== */

{full_css_text}

/* ==========================================================================
   OMNIBUS SHELL & RESPONSIVE DESIGN SYSTEM
   ========================================================================== */
{omnibus_css}
'''

    app_js = '''/* ==========================================================================
   JAVASCRIPT MASTER STUDY DOCUMENTATION — COMPLETE BOOK (CHAPTERS 01 - 40)
   INTERACTIVE APPLICATION SCRIPT (js/app.js)
   ========================================================================== */

function toggleChapterMenu() {
  const menu = document.getElementById('chapterDropdownMenu');
  const backdrop = document.getElementById('chapterMenuBackdrop');
  const btn = document.getElementById('chapterDropdownBtn');
  const searchInput = document.getElementById('chapterSearchInput');
  const isOpen = menu && menu.classList.contains('active');
  
  if (isOpen) {
    closeChapterMenu();
  } else if (menu && backdrop && btn) {
    menu.classList.add('active');
    backdrop.classList.add('active');
    btn.setAttribute('aria-expanded', 'true');
    if (searchInput) {
      setTimeout(() => searchInput.focus(), 60);
    }
  }
}

function closeChapterMenu() {
  const menu = document.getElementById('chapterDropdownMenu');
  const backdrop = document.getElementById('chapterMenuBackdrop');
  const btn = document.getElementById('chapterDropdownBtn');
  if (menu) menu.classList.remove('active');
  if (backdrop) backdrop.classList.remove('active');
  if (btn) btn.setAttribute('aria-expanded', 'false');
}

function selectChapter(chId) {
  closeChapterMenu();
}

function filterChapters(query) {
  const q = query.trim().toLowerCase();
  const items = document.querySelectorAll('.chapter-menu-item');
  let matched = 0;
  items.forEach(item => {
    const data = item.getAttribute('data-title') || '';
    if (!q || data.includes(q)) {
      item.style.display = 'flex';
      matched++;
    } else {
      item.style.display = 'none';
    }
  });
  
  let noResults = document.getElementById('chapterMenuNoResults');
  if (matched === 0) {
    if (!noResults) {
      noResults = document.createElement('div');
      noResults.id = 'chapterMenuNoResults';
      noResults.className = 'chapter-menu-no-results';
      noResults.textContent = 'No matching chapters found';
      const list = document.getElementById('chapterMenuList');
      if (list) list.appendChild(noResults);
    }
    noResults.style.display = 'block';
  } else if (noResults) {
    noResults.style.display = 'none';
  }
}

// Close on Escape key
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    closeChapterMenu();
  }
});
'''

    # 1. Clean Linked HTML (CSS and JS separated into external files)
    linked_html = f'''<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>JavaScript Master Study Documentation — Complete Book (Chapters 01 – 40)</title>
  
  <!-- Google Fonts Preconnect & Stylesheets -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Hind+Siliguri:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
  
  <!-- Master Stylesheet -->
  <link rel="stylesheet" href="css/style.css">
</head>
<body id="top">

  <!-- Sticky Top Navigation Bar -->
  <header class="omnibus-navbar">
    <a href="#top" class="omnibus-brand">
      <span class="logo">JS</span>
      <span>MASTER STUDY DOCUMENTATION — COMPLETE BOOK</span>
    </a>
    <div class="omnibus-controls">
      <div class="omnibus-dropdown-container">
        <button id="chapterDropdownBtn" class="chapter-dropdown-trigger" onclick="toggleChapterMenu()" aria-expanded="false" aria-haspopup="true">
          <span class="btn-left">
            <span class="btn-icon">📑</span>
            <span class="btn-text">Jump to Chapter (01 – 40)...</span>
          </span>
          <span class="btn-arrow">▾</span>
        </button>
        
        <!-- Backdrop for mobile / outside click -->
        <div id="chapterMenuBackdrop" class="chapter-menu-backdrop" onclick="closeChapterMenu()"></div>
        
        <!-- Dropdown Card -->
        <div id="chapterDropdownMenu" class="chapter-dropdown-menu" role="menu">
          <div class="chapter-menu-header">
            <div class="chapter-menu-title-row">
              <span>📑 Jump to Chapter (01 – 40)</span>
              <button class="chapter-menu-close" onclick="closeChapterMenu()" title="Close menu" aria-label="Close">✕</button>
            </div>
            <input type="text" id="chapterSearchInput" class="chapter-search-input" placeholder="🔍 Search chapter (e.g. DOM, 39, Loop)..." oninput="filterChapters(this.value)" autocomplete="off">
          </div>
          <div class="chapter-menu-list" id="chapterMenuList">
{chapter_menu_html}
          </div>
        </div>
      </div>

      <button class="omnibus-btn" onclick="window.print()">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
        Print / Save PDF
      </button>
    </div>
  </header>

  <!-- Master Table of Contents Section (Matches User's Reference Screenshot) -->
  <div class="master-toc-section">
    <div class="master-toc-header">
      <div class="master-toc-title">⚡ JAVASCRIPT MASTER STUDY DOCUMENTATION</div>
      <div class="master-toc-subtitle">Comprehensive Engineering Curriculum • Chapters 01 – 40 • Zero-Skipping Policy Edition</div>
    </div>
    <div class="master-toc-grid">
        {toc_cards_html}
    </div>
  </div>

  <!-- All 40 Chapters Unbroken Content -->
{all_chapters_body}

  <!-- Floating Back to Top Button -->
  <a href="#top" class="floating-back-top" title="Back to Top" aria-label="Back to Top">↑</a>

  <!-- Interactivity Script -->
  <script src="js/app.js"></script>

</body>
</html>
'''

    # 2. Standalone HTML (Single-file version with inline CSS & JS for main.html)
    standalone_html = f'''<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>JavaScript Master Study Documentation — Complete Book (Chapters 01 – 40)</title>
  
  <!-- Google Fonts Preconnect & Stylesheets -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Hind+Siliguri:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
  
  <style>
{full_css_text}

{omnibus_css}
  </style>
</head>
<body id="top">

  <!-- Sticky Top Navigation Bar -->
  <header class="omnibus-navbar">
    <a href="#top" class="omnibus-brand">
      <span class="logo">JS</span>
      <span>MASTER STUDY DOCUMENTATION — COMPLETE BOOK</span>
    </a>
    <div class="omnibus-controls">
      <div class="omnibus-dropdown-container">
        <button id="chapterDropdownBtn" class="chapter-dropdown-trigger" onclick="toggleChapterMenu()" aria-expanded="false" aria-haspopup="true">
          <span class="btn-left">
            <span class="btn-icon">📑</span>
            <span class="btn-text">Jump to Chapter (01 – 40)...</span>
          </span>
          <span class="btn-arrow">▾</span>
        </button>
        
        <!-- Backdrop for mobile / outside click -->
        <div id="chapterMenuBackdrop" class="chapter-menu-backdrop" onclick="closeChapterMenu()"></div>
        
        <!-- Dropdown Card -->
        <div id="chapterDropdownMenu" class="chapter-dropdown-menu" role="menu">
          <div class="chapter-menu-header">
            <div class="chapter-menu-title-row">
              <span>📑 Jump to Chapter (01 – 40)</span>
              <button class="chapter-menu-close" onclick="closeChapterMenu()" title="Close menu" aria-label="Close">✕</button>
            </div>
            <input type="text" id="chapterSearchInput" class="chapter-search-input" placeholder="🔍 Search chapter (e.g. DOM, 39, Loop)..." oninput="filterChapters(this.value)" autocomplete="off">
          </div>
          <div class="chapter-menu-list" id="chapterMenuList">
{chapter_menu_html}
          </div>
        </div>
      </div>

      <button class="omnibus-btn" onclick="window.print()">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
        Print / Save PDF
      </button>
    </div>
  </header>

  <!-- Master Table of Contents Section (Matches User's Reference Screenshot) -->
  <div class="master-toc-section">
    <div class="master-toc-header">
      <div class="master-toc-title">⚡ JAVASCRIPT MASTER STUDY DOCUMENTATION</div>
      <div class="master-toc-subtitle">Comprehensive Engineering Curriculum • Chapters 01 – 40 • Zero-Skipping Policy Edition</div>
    </div>
    <div class="master-toc-grid">
        {toc_cards_html}
    </div>
  </div>

  <!-- All 40 Chapters Unbroken Content -->
{all_chapters_body}

  <!-- Floating Back to Top Button -->
  <a href="#top" class="floating-back-top" title="Back to Top" aria-label="Back to Top">↑</a>

  <!-- Interactivity Script -->
  <script>
{app_js}
  </script>

</body>
</html>
'''

    # File mappings to write
    files_to_write = [
        ('3-JavaScript/1-code/index.html', linked_html),
        ('3-JavaScript/1-code/css/style.css', master_css),
        ('3-JavaScript/1-code/js/app.js', app_js),
    ]

    for rel_path, file_content in files_to_write:
        os.makedirs(os.path.dirname(rel_path), exist_ok=True)
        with open(rel_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
        print(f"[OUTPUT] Successfully wrote {rel_path} ({len(file_content)} bytes)")

    # Dual-sync to secondary drive: e:\Git All Repo\Note-Book\
    sec_repo = r'e:\Git All Repo\Note-Book'
    if os.path.exists(sec_repo):
        for rel_path, file_content in files_to_write:
            dest = os.path.join(sec_repo, rel_path)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, 'w', encoding='utf-8') as f:
                f.write(file_content)
        print(f"[SYNC] Successfully dual-synced all files to {sec_repo}")

if __name__ == '__main__':
    build_all()
